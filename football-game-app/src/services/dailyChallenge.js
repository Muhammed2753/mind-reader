import AsyncStorage from '@react-native-async-storage/async-storage';

const DAILY_KEY = '@daily_challenge';

export const getDailyChallenge = async (playersData) => {
  try {
    const today = new Date().toDateString();
    const stored = await AsyncStorage.getItem(DAILY_KEY);
    const data = stored ? JSON.parse(stored) : null;

    if (data && data.date === today) {
      return data;
    }

    // Generate new daily challenge
    const players = Object.keys(playersData);
    const seed = new Date().getDate() + new Date().getMonth() * 31;
    const playerIndex = seed % players.length;
    const dailyPlayer = players[playerIndex];

    const newChallenge = {
      date: today,
      player: dailyPlayer,
      completed: false,
      reward: 50,
    };

    await AsyncStorage.setItem(DAILY_KEY, JSON.stringify(newChallenge));
    return newChallenge;
  } catch (e) {
    return null;
  }
};

export const completeDailyChallenge = async () => {
  try {
    const stored = await AsyncStorage.getItem(DAILY_KEY);
    if (stored) {
      const data = JSON.parse(stored);
      data.completed = true;
      await AsyncStorage.setItem(DAILY_KEY, JSON.stringify(data));
      return data.reward;
    }
  } catch (e) {
    return 0;
  }
};

export const isDailyChallengeCompleted = async () => {
  try {
    const stored = await AsyncStorage.getItem(DAILY_KEY);
    if (stored) {
      const data = JSON.parse(stored);
      return data.completed && data.date === new Date().toDateString();
    }
  } catch (e) {
    return false;
  }
};
