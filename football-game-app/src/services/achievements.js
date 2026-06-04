export const ACHIEVEMENTS = {
  first_win: { id: 'first_win', name: 'First Blood', icon: '🏆', desc: 'Win your first game', coins: 10 },
  win_3: { id: 'win_3', name: 'Hat Trick', icon: '⚽', desc: 'Win 3 games', coins: 25 },
  win_10: { id: 'win_10', name: 'Legend', icon: '👑', desc: 'Win 10 games', coins: 50 },
  streak_3: { id: 'streak_3', name: 'On Fire', icon: '🔥', desc: '3 win streak', coins: 30 },
  streak_5: { id: 'streak_5', name: 'Unstoppable', icon: '💪', desc: '5 win streak', coins: 75 },
  guess_in_3: { id: 'guess_in_3', name: 'Mind Reader', icon: '🧠', desc: 'Guess in 3 questions', coins: 40 },
  guess_in_5: { id: 'guess_in_5', name: 'Quick Thinker', icon: '⚡', desc: 'Guess in 5 questions', coins: 20 },
  speed_demon: { id: 'speed_demon', name: 'Speed Demon', icon: '🏃', desc: 'Win Time Attack with 30s left', coins: 50 },
  perfect_week: { id: 'perfect_week', name: 'Perfect Week', icon: '🌟', desc: 'Complete 7 daily challenges', coins: 100 },
};

export const checkAchievements = (stats) => {
  const unlocked = [];
  
  if (stats.wins === 1 && !stats.achievements?.includes('first_win')) {
    unlocked.push(ACHIEVEMENTS.first_win);
  }
  if (stats.wins === 3 && !stats.achievements?.includes('win_3')) {
    unlocked.push(ACHIEVEMENTS.win_3);
  }
  if (stats.wins === 10 && !stats.achievements?.includes('win_10')) {
    unlocked.push(ACHIEVEMENTS.win_10);
  }
  if (stats.currentStreak === 3 && !stats.achievements?.includes('streak_3')) {
    unlocked.push(ACHIEVEMENTS.streak_3);
  }
  if (stats.currentStreak === 5 && !stats.achievements?.includes('streak_5')) {
    unlocked.push(ACHIEVEMENTS.streak_5);
  }
  
  return unlocked;
};
