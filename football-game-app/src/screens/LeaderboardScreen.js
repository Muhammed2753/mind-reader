import React, { useState, useEffect } from 'react';
import { View, Text, ScrollView, StyleSheet, TouchableOpacity } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { getLeaderboard } from '../services/leaderboard';

export default function LeaderboardScreen({ navigation }) {
  const [leaderboard, setLeaderboard] = useState([]);

  useEffect(() => {
    loadLeaderboard();
  }, []);

  const loadLeaderboard = async () => {
    const data = await getLeaderboard();
    setLeaderboard(data);
  };

  return (
    <LinearGradient colors={['#1a1a2e', '#16213e']} style={styles.container}>
      <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backBtn}>
        <Text style={styles.backText}>← Back</Text>
      </TouchableOpacity>

      <Text style={styles.title}>🏆 Leaderboard</Text>

      <ScrollView style={styles.list}>
        {leaderboard.length === 0 ? (
          <Text style={styles.empty}>No entries yet. Be the first!</Text>
        ) : (
          leaderboard.map((entry, i) => (
            <View key={i} style={[styles.entry, i < 3 && styles.topThree]}>
              <Text style={styles.rank}>
                {i === 0 ? '🥇' : i === 1 ? '🥈' : i === 2 ? '🥉' : `#${i + 1}`}
              </Text>
              <View style={styles.info}>
                <Text style={styles.name}>{entry.name}</Text>
                <Text style={styles.details}>
                  Score: {entry.score} | Questions: {entry.questions}
                </Text>
              </View>
            </View>
          ))
        )}
      </ScrollView>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  backBtn: { marginBottom: 20 },
  backText: { color: '#4ecca3', fontSize: 18 },
  title: { fontSize: 36, fontWeight: 'bold', color: '#fff', textAlign: 'center', marginBottom: 20 },
  list: { flex: 1 },
  empty: { color: '#aaa', textAlign: 'center', marginTop: 50, fontSize: 16 },
  entry: { backgroundColor: '#16213e', padding: 15, borderRadius: 10, marginBottom: 10, flexDirection: 'row', alignItems: 'center' },
  topThree: { borderWidth: 2, borderColor: '#ffd700' },
  rank: { fontSize: 24, marginRight: 15, width: 40 },
  info: { flex: 1 },
  name: { color: '#fff', fontSize: 18, fontWeight: 'bold' },
  details: { color: '#aaa', fontSize: 14, marginTop: 5 },
});
