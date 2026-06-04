import React, { useEffect } from 'react';
import { View, StyleSheet, Animated, Dimensions } from 'react-native';

const { width, height } = Dimensions.get('window');

export default function Confetti({ show }) {
  const confettiPieces = Array(50).fill(0).map(() => ({
    x: new Animated.Value(Math.random() * width),
    y: new Animated.Value(-50),
    rotation: new Animated.Value(0),
  }));

  useEffect(() => {
    if (show) {
      confettiPieces.forEach((piece, i) => {
        Animated.parallel([
          Animated.timing(piece.y, {
            toValue: height + 100,
            duration: 3000 + Math.random() * 2000,
            useNativeDriver: true,
          }),
          Animated.timing(piece.rotation, {
            toValue: 360 * (Math.random() > 0.5 ? 1 : -1),
            duration: 2000,
            useNativeDriver: true,
          }),
        ]).start();
      });
    }
  }, [show]);

  if (!show) return null;

  return (
    <View style={styles.container} pointerEvents="none">
      {confettiPieces.map((piece, i) => (
        <Animated.View
          key={i}
          style={[
            styles.confetti,
            {
              backgroundColor: ['#4ecca3', '#e94560', '#ffd700', '#00d4ff'][i % 4],
              transform: [
                { translateX: piece.x },
                { translateY: piece.y },
                { rotate: piece.rotation.interpolate({
                  inputRange: [0, 360],
                  outputRange: ['0deg', '360deg'],
                })},
              ],
            },
          ]}
        />
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    zIndex: 1000,
  },
  confetti: {
    position: 'absolute',
    width: 10,
    height: 10,
    borderRadius: 5,
  },
});
