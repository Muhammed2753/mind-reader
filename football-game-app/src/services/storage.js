import AsyncStorage from '@react-native-async-storage/async-storage';

const STATS_KEY = '@football_game_stats';

export const getStats = async () => {
  try {
    const data = await AsyncStorage.getItem(STATS_KEY);
    return data ? JSON.parse(data) : {
      gamesPlayed: 0,
      wins: 0,
      losses: 0,
      currentStreak: 0,
      bestStreak: 0,
      totalQuestions: 0,
      coins: 0,
      achievements: [],
      dailyChallenges: 0,
    };
  } catch (e) {
    return {};
  }
};

export const saveStats = async (stats) => {
  try {
    await AsyncStorage.setItem(STATS_KEY, JSON.stringify(stats));
  } catch (e) {
    console.error('Failed to save stats', e);
  }
};

export const updateStats = async (won, questionsAsked) => {
  const stats = await getStats();
  stats.gamesPlayed += 1;
  stats.totalQuestions += questionsAsked;
  
  if (won) {
    stats.wins += 1;
    stats.currentStreak += 1;
    stats.bestStreak = Math.max(stats.bestStreak, stats.currentStreak);
  } else {
    stats.losses += 1;
    stats.currentStreak = 0;
  }
  
  await saveStats(stats);
  return stats;
};

export const addCoins = async (amount) => {
  const stats = await getStats();
  stats.coins += amount;
  await saveStats(stats);
  return stats.coins;
};

export const spendCoins = async (amount) => {
  const stats = await getStats();
  if (stats.coins >= amount) {
    stats.coins -= amount;
    await saveStats(stats);
    return true;
  }
  return false;
};
