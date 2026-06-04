import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Alert } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { getDailyChallenge, completeDailyChallenge } from '../services/dailyChallenge';
import { addCoins } from '../services/storage';
import playersData from '../data/players.json';

export default function DailyChallengeScreen({ navigation }) {
  const [challenge, setChallenge] = useState(null);

  useEffect(() => {
    loadChallenge();
  }, []);

  const loadChallenge = async () => {
    const daily = await getDailyChallenge(playersData);
    setChallenge(daily);
  };

  const startChallenge = () => {
    if (challenge.completed) {
      Alert.alert('Already Completed', 'Come back tomorrow for a new challenge!');
      return;
    }
    navigation.navigate('Game', { mode: 'daily', targetPlayer: challenge.player });
  };

  if (!challenge) return null;

  return (
    <LinearGradient colors={['#1a1a2e', '#16213e']} style={styles.container}>
      <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backBtn}>
        <Text style={styles.backText}>← Back</Text>
      </TouchableOpacity>

      <Text style={styles.title}>🌟 Daily Challenge</Text>
      <Text style={styles.date}>{challenge.date}</Text>

      <View style={styles.card}>
        <Text style={styles.cardTitle}>Today's Challenge</Text>
        <Text style={styles.reward}>Reward: {challenge.reward} 🪙</Text>
        
        {challenge.completed ? (
          <Text style={styles.completed}>✅ Completed!</Text>
        ) : (
          <TouchableOpacity style={styles.startBtn} onPress={startChallenge}>
            <Text style={styles.startText}>Start Challenge</Text>
          </TouchableOpacity>
        )}
      </View>

      <Text style={styles.hint}>Guess today's mystery player!</Text>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  backBtn: { marginBottom: 20 },
  backText: { color: '#4ecca3', fontSize: 18 },
  title: { fontSize: 36, fontWeight: 'bold', color: '#fff', textAlign: 'center', marginBottom: 10 },
  date: { fontSize: 16, color: '#aaa', textAlign: 'center', marginBottom: 30 },
  card: { backgroundColor: '#16213e', padding: 30, borderRadius: 20, alignItems: 'center' },
  cardTitle: { fontSize: 24, color: '#fff', marginBottom: 10 },
  reward: { fontSize: 20, color: '#ffd700', marginBottom: 20 },
  completed: { fontSize: 24, color: '#4ecca3', fontWeight: 'bold' },
  startBtn: { backgroundColor: '#4ecca3', padding: 15, borderRadius: 10, width: 200 },
  startText: { fontSize: 18, fontWeight: 'bold', textAlign: 'center', color: '#1a1a2e' },
  hint: { fontSize: 14, color: '#aaa', textAlign: 'center', marginTop: 20 },
});
