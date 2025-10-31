import json

# League inference map: club → league question
CLUB_TO_LEAGUE = {
    # Premier League
    "Manchester United": "Is this player playing in the Premier League?",
    "Liverpool": "Is this player playing in the Premier League?",
    "Manchester City": "Is this player playing in the Premier League?",
    "Chelsea": "Is this player playing in the Premier League?",
    "Arsenal": "Is this player playing in the Premier League?",
    "Tottenham Hotspur": "Is this player playing in the Premier League?",
    "Aston Villa": "Is this player playing in the Premier League?",
    "Newcastle United": "Is this player playing in the Premier League?",
    "Brighton & Hove Albion": "Is this player playing in the Premier League?",
    "West Ham United": "Is this player playing in the Premier League?",
    "Brentford": "Is this player playing in the Premier League?",
    "Crystal Palace": "Is this player playing in the Premier League?",
    "Fulham": "Is this player playing in the Premier League?",
    "Everton": "Is this player playing in the Premier League?",
    "Nottingham Forest": "Is this player playing in the Premier League?",
    "Bournemouth": "Is this player playing in the Premier League?",
    "Wolverhampton Wanderers": "Is this player playing in the Premier League?",
    "Burnley": "Is this player playing in the Premier League?",
    "Sheffield United": "Is this player playing in the Premier League?",
    "Luton Town": "Is this player playing in the Premier League?",
    "Sunderland": "Is this player playing in the Premier League?",
    
    # La Liga
    "Real Madrid": "Is this player playing in La Liga?",
    "FC Barcelona": "Is this player playing in La Liga?",
    "Atlético Madrid": "Is this player playing in La Liga?",
    "Girona FC": "Is this player playing in La Liga?",
    "Athletic Bilbao": "Is this player playing in La Liga?",
    "Real Sociedad": "Is this player playing in La Liga?",
    "Real Betis": "Is this player playing in La Liga?",
    "Villarreal CF": "Is this player playing in La Liga?",
    "Valencia CF": "Is this player playing in La Liga?",
    "Osasuna": "Is this player playing in La Liga?",
    "Sevilla FC": "Is this player playing in La Liga?",
    "Las Palmas": "Is this player playing in La Liga?",
    "Mallorca": "Is this player playing in La Liga?",
    "Rayo Vallecano": "Is this player playing in La Liga?",
    "Celta Vigo": "Is this player playing in La Liga?",
    "Alavés": "Is this player playing in La Liga?",
    "Getafe CF": "Is this player playing in La Liga?",
    "Elche": "Is this player playing in La Liga?",
    "Levante UD": "Is this player playing in La Liga?",
    "RCD Espanyol": "Is this player playing in La Liga?",
    
    # Serie A
    "Inter Milan": "Is this player playing in Serie A?",
    "AC Milan": "Is this player playing in Serie A?",
    "Juventus": "Is this player playing in Serie A?",
    "Napoli": "Is this player playing in Serie A?",
    "Roma": "Is this player playing in Serie A?",
    "Lazio": "Is this player playing in Serie A?",
    "Atalanta": "Is this player playing in Serie A?",
    "Fiorentina": "Is this player playing in Serie A?",
    "Bologna": "Is this player playing in Serie A?",
    "Torino": "Is this player playing in Serie A?",
    "Udinese": "Is this player playing in Serie A?",
    "Monza": "Is this player playing in Serie A?",
    "Genoa": "Is this player playing in Serie A?",
    "Lecce": "Is this player playing in Serie A?",
    "Hellas Verona": "Is this player playing in Serie A?",
    "Cagliari": "Is this player playing in Serie A?",
    "Empoli": "Is this player playing in Serie A?",
    "Salernitana": "Is this player playing in Serie A?",
    "Parma": "Is this player playing in Serie A?",
    "Como": "Is this player playing in Serie A?",
    
    # Bundesliga
    "Bayern Munich": "Is this player playing in the Bundesliga?",
    "Borussia Dortmund": "Is this player playing in the Bundesliga?",
    "RB Leipzig": "Is this player playing in the Bundesliga?",
    "Bayer Leverkusen": "Is this player playing in the Bundesliga?",
    "Eintracht Frankfurt": "Is this player playing in the Bundesliga?",
    "VfB Stuttgart": "Is this player playing in the Bundesliga?",
    "Borussia Mönchengladbach": "Is this player playing in the Bundesliga?",
    "Wolfsburg": "Is this player playing in the Bundesliga?",
    "Mainz 05": "Is this player playing in the Bundesliga?",
    "SC Freiburg": "Is this player playing in the Bundesliga?",
    "Union Berlin": "Is this player playing in the Bundesliga?",
    "Hoffenheim": "Is this player playing in the Bundesliga?",
    "Augsburg": "Is this player playing in the Bundesliga?",
    "Werder Bremen": "Is this player playing in the Bundesliga?",
    "Heidenheim": "Is this player playing in the Bundesliga?",
    "Holstein Kiel": "Is this player playing in the Bundesliga?",
    "St. Pauli": "Is this player playing in the Bundesliga?",
    "Bochum": "Is this player playing in the Bundesliga?",
    
    # Ligue 1
    "Paris Saint-Germain": "Is this player playing in Ligue 1?",
    "Marseille": "Is this player playing in Ligue 1?",
    "Monaco": "Is this player playing in Ligue 1?",
    "Lyon": "Is this player playing in Ligue 1?",
    "Lille": "Is this player playing in Ligue 1?",
    "Nice": "Is this player playing in Ligue 1?",
    "Rennes": "Is this player playing in Ligue 1?",
    "Lens": "Is this player playing in Ligue 1?",
    "Reims": "Is this player playing in Ligue 1?",
    "Strasbourg": "Is this player playing in Ligue 1?",
    "Montpellier": "Is this player playing in Ligue 1?",
    "Nantes": "Is this player playing in Ligue 1?",
    "Toulouse": "Is this player playing in Ligue 1?",
    "Brest": "Is this player playing in Ligue 1?",
    "Le Havre": "Is this player playing in Ligue 1?",
    "Metz": "Is this player playing in Ligue 1?",
    "Paris F.C": "Is this player playing in Ligue 1?",
    "Angers": "Is this player playing in Ligue 1?",
    
    # MLS
    "Inter Miami": "Is this player playing in MLS?",
    "LAFC": "Is this player playing in MLS?",
    "Seattle Sounders": "Is this player playing in MLS?",
    "Atlanta United": "Is this player playing in MLS?",
    "Toronto FC": "Is this player playing in MLS?",
    "New York City FC": "Is this player playing in MLS?",
    "Columbus Crew": "Is this player playing in MLS?",
    "Philadelphia Union": "Is this player playing in MLS?",
    "FC Cincinnati": "Is this player playing in MLS?",
    "Nashville SC": "Is this player playing in MLS?",
    "Portland Timbers": "Is this player playing in MLS?",
    "Vancouver Whitecaps": "Is this player playing in MLS?",
    "Sporting Kansas City": "Is this player playing in MLS?",
    "Houston Dynamo": "Is this player playing in MLS?",
    "Austin FC": "Is this player playing in MLS?",
    "Minnesota United": "Is this player playing in MLS?",
    "New England Revolution": "Is this player playing in MLS?",
    "Chicago Fire": "Is this player playing in MLS?",
    "San Jose Earthquakes": "Is this player playing in MLS?",
    "Colorado Rapids": "Is this player playing in MLS?",
    "Real Salt Lake": "Is this player playing in MLS?",
    "D.C. United": "Is this player playing in MLS?",
    "St. Louis City SC": "Is this player playing in MLS?",
    "Charlotte FC": "Is this player playing in MLS?",
    "Orlando City": "Is this player playing in MLS?",
    
    # Liga MX
    "Club América": "Is this player playing in Liga MX?",
    "Tigres UANL": "Is this player playing in Liga MX?",
    "Chivas": "Is this player playing in Liga MX?",
    "Monterrey": "Is this player playing in Liga MX?",
    "Pumas UNAM": "Is this player playing in Liga MX?",
    "Santos Laguna": "Is this player playing in Liga MX?",
    "Toluca": "Is this player playing in Liga MX?",
    "León": "Is this player playing in Liga MX?",
    "Pachuca": "Is this player playing in Liga MX?",
    "Atlas": "Is this player playing in Liga MX?",
    "Mazatlán": "Is this player playing in Liga MX?",
    "Juárez": "Is this player playing in Liga MX?",
    "Necaxa": "Is this player playing in Liga MX?",
    "Querétaro": "Is this player playing in Liga MX?",
    "Tijuana": "Is this player playing in Liga MX?",
    "Guadalajara": "Is this player playing in Liga MX?",
    "San Luis": "Is this player playing in Liga MX?",
    
    # Ghana Premier League
    "Hearts of Oak": "Is this player playing in the Ghana Premier League?",
    "Aduana Stars": "Is this player playing in the Ghana Premier League?",
    "Accra Great Olympics": "Is this player playing in the Ghana Premier League?",
    "Elmina Sharks": "Is this player playing in the Ghana Premier League?",
    "WAFA": "Is this player playing in the Ghana Premier League?",
    
    # Algerian Ligue 1
    "CR Belouizdad": "Is this player playing in the Algerian Ligue professionelle 1?",
    "USM Alger": "Is this player playing in the Algerian Ligue professionelle 1?",
    "MC Alger": "Is this player playing in the Algerian Ligue professionelle 1?",
    "JS Kabylie": "Is this player playing in the Algerian Ligue professionelle 1?",
    "CS Constantine": "Is this player playing in the Algerian Ligue professionelle 1?",
    "Paradou AC": "Is this player playing in the Algerian Ligue professionelle 1?",
    "MC Oran": "Is this player playing in the Algerian Ligue professionelle 1?",
    "USM Khenchela": "Is this player playing in the Algerian Ligue professionelle 1?",
    "NC Magra": "Is this player playing in the Algerian Ligue professionelle 1?",
    "ASO Chlef": "Is this player playing in the Algerian Ligue professionelle 1?",
    
    # Botola Pro (Morocco)
    "Wydad AC": "Is this player playing in Botola Pro?",
    "Raja Casablanca": "Is this player playing in Botola Pro?",
    "AS FAR": "Is this player playing in Botola Pro?",
    "FUS Rabat": "Is this player playing in Botola Pro?",
    "RS Berkane": "Is this player playing in Botola Pro?",
    "Moghreb Tétouan": "Is this player playing in Botola Pro?",
    "Hassania Agadir": "Is this player playing in Botola Pro?",
    "Ittihad Tanger": "Is this player playing in Botola Pro?",
    "Olympique Khouribga": "Is this player playing in Botola Pro?",
    "Chabab Mohammédia": "Is this player playing in Botola Pro?",
    
    # Others (add more as needed)
}

def main():
    with open("football_characters.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    fixed = 0
    for name, player in data.items():
        if not isinstance(player, dict):
            continue
        answers = player.get("answers", {})
        
        # Find club question that is "yes"
        club = None
        for q, ans in answers.items():
            if ans == "yes" and "playing for " in q:
                # Extract club name: "Is this player playing for Manchester City?" → "Manchester City"
                try:
                    club = q.split("playing for ")[1].rstrip("?")
                except:
                    continue
                break
        
        if club and club in CLUB_TO_LEAGUE:
            league_question = CLUB_TO_LEAGUE[club]
            if league_question not in answers:
                answers[league_question] = "yes"
                fixed += 1
    
    with open("football_characters_fixed.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Fixed {fixed} players. Saved as 'football_characters_fixed.json'")
    print("➡️  Now rename this file to 'football_characters.json' and restart your app.")

if __name__ == "__main__":
    main()