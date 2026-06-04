import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';

export default function StatsScreen({ navigation }) {
  return (
    <LinearGradient colors={['#1a1a2e', '#16213e']} style={styles.container}>
      <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backBtn}>
        <Text style={styles.backText}>← Back</Text>
      </TouchableOpacity>
      
      <Text style={styles.title}>📊 Statistics</Text>
      
      <View style={styles.statCard}>
        <Text style={styles.statLabel}>Games Played</Text>
        <Text style={styles.statValue}>0</Text>
      </View>
      
      <View style={styles.statCard}>
        <Text style={styles.statLabel}>Win Rate</Text>
        <Text style={styles.statValue}>0%</Text>
      </View>
      
      <View style={styles.statCard}>
        <Text style={styles.statLabel}>Best Streak</Text>
        <Text style={styles.statValue}>0</Text>
      </View>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  backBtn: { marginBottom: 20 },
  backText: { color: '#4ecca3', fontSize: 18 },
  title: { fontSize: 32, fontWeight: 'bold', color: '#fff', marginBottom: 30, textAlign: 'center' },
  statCard: { backgroundColor: '#16213e', padding: 20, borderRadius: 15, marginBottom: 15 },
  statLabel: { color: '#fff', fontSize: 16, marginBottom: 5 },
  statValue: { color: '#4ecca3', fontSize: 32, fontWeight: 'bold' },
});
