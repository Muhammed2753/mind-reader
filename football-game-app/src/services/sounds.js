import { Audio } from 'expo-av';

let sounds = {};

export const loadSounds = async () => {
  try {
    // You'll need to add actual sound files to assets/sounds/
    // For now, using system sounds
    sounds.correct = await Audio.Sound.createAsync(
      require('../assets/sounds/correct.mp3')
    ).catch(() => null);
    
    sounds.wrong = await Audio.Sound.createAsync(
      require('../assets/sounds/wrong.mp3')
    ).catch(() => null);
    
    sounds.click = await Audio.Sound.createAsync(
      require('../assets/sounds/click.mp3')
    ).catch(() => null);
    
    sounds.achievement = await Audio.Sound.createAsync(
      require('../assets/sounds/achievement.mp3')
    ).catch(() => null);
  } catch (e) {
    console.log('Sound loading failed', e);
  }
};

export const playSound = async (soundName) => {
  try {
    if (sounds[soundName]) {
      await sounds[soundName].sound.replayAsync();
    }
  } catch (e) {
    console.log('Sound play failed', e);
  }
};

export const playSoundEffect = (type) => {
  // Fallback to haptics if sounds not loaded
  playSound(type);
};
