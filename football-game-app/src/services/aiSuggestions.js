// AI that suggests the best question to ask
export const suggestBestQuestion = (remainingPlayers, availableQuestions, playersData) => {
  if (remainingPlayers.length <= 1 || availableQuestions.length === 0) return null;

  let bestQuestion = null;
  let bestScore = Infinity;

  availableQuestions.forEach(question => {
    let yesCount = 0;
    let noCount = 0;

    remainingPlayers.forEach(player => {
      const answer = playersData[player]?.answers[question];
      if (answer === 'yes') yesCount++;
      else if (answer === 'no') noCount++;
    });

    // Best question splits players ~50/50
    const score = Math.abs(yesCount - noCount);
    if (score < bestScore) {
      bestScore = score;
      bestQuestion = question;
    }
  });

  return bestQuestion;
};

export const calculateQuestionEfficiency = (question, remainingPlayers, playersData) => {
  let yesCount = 0;
  remainingPlayers.forEach(player => {
    if (playersData[player]?.answers[question] === 'yes') yesCount++;
  });
  const efficiency = Math.min(yesCount, remainingPlayers.length - yesCount);
  return Math.round((efficiency / remainingPlayers.length) * 100);
};
