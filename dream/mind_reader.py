import os
import re
import json
import random
import math
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ----------------------------
# Config
# ----------------------------
TREE_PATH = "tree.json"
KNOW_PATH = "knowledge_db.json"
QUESTIONS_PATH = "characterquestions.jsonl"   # JSONL file (1 question per line)
RANDOM_QUESTION_COUNT = 30
STRICT_THRESHOLD = 0.90
random.seed(42)

CONF_WEIGHTS = {
    "yes": 0.1,
    "no": 0,
    "sometimes": 0.1,
    "not really": 0,
    "i don't know": 0.05
}

# Expanded seed guesses for characters, athletes, and celebrities
SEED_GUESSES = {
    "character": [
        "Sherlock Holmes", "Harry Potter", "Darth Vader", "Elizabeth Bennet", "Spock",
        "Wonder Woman", "Hannibal Lecter", "Luke Skywalker", "Tony Stark", "Frodo Baggins"
    ],
    "athlete": [
        "Cristiano Ronaldo", "Lionel Messi", "Serena Williams", "LeBron James", "Michael Jordan",
        "Roger Federer", "Usain Bolt", "Tom Brady", "Michael Phelps", "Rafa Nadal"
    ],
    "celebrity": [
        "Beyoncé", "Elon Musk", "Bill Gates", "Taylor Swift", "Oprah Winfrey",
        "Jennifer Aniston", "Dwayne Johnson", "Kanye West", "Rihanna", "Johnny Depp"
    ]
}
ALL_SEED = sum(SEED_GUESSES.values(), [])

# ----------------------------
# Question generator
# ----------------------------
def needs_regen(path):
    """Check if file is missing, empty, or still has (Q123) junk."""
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return True
    with open(path, "r", encoding="utf-8") as f:
        for _ in range(50):
            line = f.readline()
            if not line:
                break
            if re.search(r'\(Q\d+\)', line):
                return True
    return False

def generate_questions_file():
    if not needs_regen(QUESTIONS_PATH):
        return
    print("⚡ Generating characterquestions.jsonl...")
    categories = [
        "Is this character from a movie?",
        "Is this person an athlete?",
        "Is this character a superhero?",
        "Is this celebrity a musician?",
        "Has this person won an Oscar?",
        "Is this athlete known for basketball?",
        "Is this character from a book?",
        "Does this celebrity have a social media presence?",
        "Is this athlete a football player?",
        "Is this character animated?"
    ]
    total = 500_000  # Adjust as necessary
    chunk_size = 20_000
    with open(QUESTIONS_PATH, "w", encoding="utf-8") as f:
        written = 0
        while written < total:
            batch = []
            for _ in range(min(chunk_size, total - written)):
                base = random.choice(categories)
                batch.append(base + "\n")
            f.writelines(batch)
            written += len(batch)
    print("✅ charactersquestions.jsonl created/cleaned.")

generate_questions_file()

# ----------------------------
# Helpers
# ----------------------------
def clean_question_text(q: str) -> str:
    if not q:
        return q
    q = q.strip()
    q = re.sub(r'\s*\(Q\d+\)\s*$', '', q)  # remove old suffix
    return q

def get_random_question(asked_set):
    """Uniform random sample (reservoir) from file."""
    chosen = None
    count = 0
    with open(QUESTIONS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            q = clean_question_text(line)
            if not q or q in asked_set:  # Check if question has been asked
                continue
            count += 1
            if random.randrange(count) == 0:
                chosen = q
    return chosen

# ----------------------------
# Load tree & guesses
# ----------------------------
if os.path.exists(TREE_PATH):
    with open(TREE_PATH, "r", encoding="utf-8") as f:
        TREE = json.load(f)
else:
    TREE = None

def build_guess_pool(tree):
    if not tree:
        return []
    pool = set()
    for nid, node in tree.items():
        if node.get("is_leaf"):
            pool.add(node.get("text"))
    return sorted(pool)

GUESS_POOL = build_guess_pool(TREE) or ALL_SEED[:]

# ----------------------------
# Knowledge DB
# ----------------------------
if os.path.exists(KNOW_PATH):
    with open(KNOW_PATH, "r", encoding="utf-8") as f:
        KNOW = json.load(f)
else:
    KNOW = {}

def save_know():
    with open(KNOW_PATH, "w", encoding="utf-8") as f:
        json.dump(KNOW, f, indent=2, ensure_ascii=False)

# ----------------------------
# Learning + candidate scoring
# ----------------------------
def normalize_answer(raw):
    if not raw:
        return "i don't know"
    s = raw.strip().lower()
    if s in ("idk", "i don't know", "i do not know", "dont know", "don't know"):
        return "i don't know"
    if s in ("sometimes", "maybe", "occasionally"):
        return "sometimes"
    if s in ("not really", "not_really"):
        return "not really"
    if s in ("yes", "y", "yeah", "yep", "true", "sure"):
        return "yes"
    if s in ("no", "n", "nope", "nah", "false"):
        return "no"
    return s

def teach_correct_answer(correct_answer, session_answers):
    if not correct_answer:
        return
    if correct_answer not in KNOW:
        KNOW[correct_answer] = {}
    for qtext, ans in session_answers:
        stats = KNOW[correct_answer].setdefault(str(qtext), {})
        stats[ans] = stats.get(ans, 0) + 1
    save_know()

def remember_wrong_guess(guess):
    if not guess:
        return
    KNOW.setdefault("_wrong", [])
    KNOW["_wrong"].append(guess)
    save_know()

def candidate_logscore(candidate, session_answers):
    stats = KNOW.get(candidate)
    if not stats:
        return None
    score = 0.0
    matched = 0
    for qtext, ans in session_answers:
        counts = stats.get(str(qtext), {})
        total = sum(counts.values())
        if total == 0:
            continue
        prob = (counts.get(ans, 0) + 1e-3) / (total + 1e-3 * (len(counts) + 1))
        score += math.log(prob)
        matched += 1
    score += math.log(1 + matched)  # bonus for more evidence
    return score

# ----------------------------
# Routes
# ----------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST", "GET"])
def start():
    session.clear()
    session["answers"] = []
    session["confidence"] = 0.0
    session["result"] = None
    session["attempts"] = 0
    session["tried"] = []
    session["asked_random"] = []
    session["asked_tree"] = []
    session["random_phase"] = True
    session["node"] = "0" if TREE else None
    return redirect(url_for("question"))

@app.route("/question", methods=["GET", "POST"])
def question():
    if session.get("confidence", 0.0) >= STRICT_THRESHOLD:
        return redirect(url_for("answer"))

    # --- Random phase ---
    if session.get("random_phase", True):
        if request.method == "POST":
            ans = normalize_answer(request.form.get("answer", ""))
            q = session.get("current_question")
            if q:
                session["answers"].append((q, ans))
                session["confidence"] = min(1.0, session.get("confidence", 0.0) + CONF_WEIGHTS.get(ans, 0.0))
                session["asked_random"].append(q)

        if len(session["asked_random"]) >= RANDOM_QUESTION_COUNT:
            session["random_phase"] = False
            return redirect(url_for("question"))

        asked = set(session.get("asked_random", []) + session.get("asked_tree", []))
        q = get_random_question(asked)
        if not q:
            session["random_phase"] = False
            return redirect(url_for("question"))
        session["current_question"] = q
        return render_template("question.html", question=q,
                               progress=int(session.get("confidence", 0) * 100))

    # --- Tree phase ---
    if TREE:
        node_id = session.get("node", "0")
        node = TREE.get(str(node_id))
        if not node:
            return redirect(url_for("answer"))

        if request.method == "POST":
            ans = normalize_answer(request.form.get("answer", ""))
            qtext = clean_question_text(node.get("text"))
            if qtext not in session.get("asked_tree", []):
                session["answers"].append((qtext, ans))
                session["asked_tree"].append(qtext)
                session["confidence"] = min(1.0, session.get("confidence", 0.0) + CONF_WEIGHTS.get(ans, 0.0))
            branch = "yes" if ans in ("yes", "sometimes") else "no"
            next_node = node.get(branch) or node.get("yes") or node.get("no")
            if next_node:
                session["node"] = str(next_node)
            return redirect(url_for("question"))

        if node.get("is_leaf"):
            return redirect(url_for("answer"))

        qtext = clean_question_text(node.get("text"))
        session["current_question"] = qtext
        return render_template("question.html", question=qtext,
                               progress=int(session.get("confidence", 0) * 100))

    return redirect(url_for("answer"))

@app.route("/answer", methods=["GET", "POST"])
def answer():
    if request.method == "POST":
        feedback = request.form.get("feedback")
        if feedback == "yes":
            return render_template("answer.html", guess=session.get("result"), confidence=100, done=True)
        else:
            wrong = session.get("result")
            if wrong:
                remember_wrong_guess(wrong)
            if session.get("attempts", 0) >= 5:
                return redirect(url_for("learn"))
            return redirect(url_for("answer"))

    session_answers = session.get("answers", [])
    tried = set(session.get("tried", []))
    wrong = set(KNOW.get("_wrong", []))

    pool = list(dict.fromkeys(GUESS_POOL + [k for k in KNOW.keys() if k != "_wrong"] + ALL_SEED))
    pool = [p for p in pool if p not in tried and p not in wrong]  # Filter out tried or wrong guesses

    scored = {}
    for cand in pool:
        s = candidate_logscore(cand, session_answers)
        if s is not None:
            scored[cand] = s

    guess, conf = None, 0
    if scored:
        max_log = max(scored.values())
        exps = {c: math.exp(scored[c] - max_log) for c in scored}
        total = sum(exps.values())
        probs = {c: exps[c] / total for c in exps}
        ranked = sorted(probs.items(), key=lambda x: x[1], reverse=True)
        guess, prob = ranked[0]
        conf = int(prob * 100)

    if not guess:
        remaining = [g for g in ALL_SEED if g not in tried and g not in wrong] or GUESS_POOL
        guess = random.choice(remaining)
        conf = int(session.get("confidence", 0.0) * 100)

    session["result"] = guess
    session["attempts"] = session.get("attempts", 0) + 1
    if guess not in session["tried"]:
        session["tried"].append(guess)

    return render_template("answer.html", guess=guess, confidence=conf, ask_confirm=True)

@app.route("/learn", methods=["GET", "POST"])
def learn():
    if request.method == "POST":
        correct = request.form.get("correct_answer", "").strip()
        if not correct:
            return render_template("learn.html", error="Please provide the correct answer.")
        teach_correct_answer(correct, session.get("answers", []))
        session["result"] = correct
        return render_template("answer.html", guess=f"Thanks — I learned {correct}!", confidence=100, done=True)
    return render_template("learn.html")

@app.route("/undo", methods=["POST"])
def undo():
    history = session.get("answers", [])
    if history:
        history.pop()
        session["answers"] = history
        session["current_question"] = history[-1][0] if history else None
        session["confidence"] = max(0.0, session.get("confidence", 0.0) - 0.05)
    return redirect(url_for("question"))

# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)