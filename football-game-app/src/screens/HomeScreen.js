import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';

export default function HomeScreen({ navigation }) {
  return (
    <LinearGradient colors={['#1a1a2e', '#16213e', '#0f3460']} style={styles.container}>
      <Text style={styles.title}>⚽ Football Guess</Text>
      <Text style={styles.subtitle}>Guess the Player</Text>
      
      <TouchableOpacity style={styles.btn} onPress={() => navigation.navigate('Game', { mode: 'classic' })}>
        <Text style={styles.btnText}>🎮 Classic Mode</Text>
      </TouchableOpacity>
      
      <TouchableOpacity style={styles.btn} onPress={() => navigation.navigate('Game', { mode: 'timeattack' })}>
        <Text style={styles.btnText}>⏱️ Time Attack</Text>
      </TouchableOpacity>
      
      <TouchableOpacity style={styles.btn} onPress={() => navigation.navigate('DailyChallenge')}>        <Text style={styles.btnText}>🌟 Daily Challenge</Text>
      </TouchableOpacity>
      
      <TouchableOpacity style={styles.btn} onPress={() => navigation.navigate('Leaderboard')}>        <Text style={styles.btnText}>🏆 Leaderboard</Text>
      </TouchableOpacity>
      
      <TouchableOpacity style={styles.btn} onPress={() => navigation.navigate('Stats')}>
        <Text style={styles.btnText}>📊 Statistics</Text>
      </TouchableOpacity>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 20 },
  title: { fontSize: 48, fontWeight: 'bold', color: '#4ecca3', marginBottom: 10 },
  subtitle: { fontSize: 20, color: '#fff', marginBottom: 50 },
  btn: { backgroundColor: '#4ecca3', padding: 20, borderRadius: 15, width: '80%', marginBottom: 15 },
  btnText: { fontSize: 20, fontWeight: 'bold', textAlign: 'center', color: '#1a1a2e' },
});
