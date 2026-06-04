import AsyncStorage from '@react-native-async-storage/async-storage';

const LEADERBOARD_KEY = '@leaderboard';

export const getLeaderboard = async () => {
  try {
    const data = await AsyncStorage.getItem(LEADERBOARD_KEY);
    return data ? JSON.parse(data) : [];
  } catch (e) {
    return [];
  }
};

export const addToLeaderboard = async (playerName, score, questionsUsed) => {
  try {
    const leaderboard = await getLeaderboard();
    
    const entry = {
      name: playerName || 'Anonymous',
      score,
      questions: questionsUsed,
      date: new Date().toISOString(),
    };

    leaderboard.push(entry);
    leaderboard.sort((a, b) => {
      if (b.score !== a.score) return b.score - a.score;
      return a.questions - b.questions; // Fewer questions is better
    });

    // Keep top 100
    const top100 = leaderboard.slice(0, 100);
    await AsyncStorage.setItem(LEADERBOARD_KEY, JSON.stringify(top100));
    
    return top100;
  } catch (e) {
    return [];
  }
};

export const getPlayerRank = async (score) => {
  const leaderboard = await getLeaderboard();
  const rank = leaderboard.findIndex(entry => entry.score <= score) + 1;
  return rank || leaderboard.length + 1;
};
