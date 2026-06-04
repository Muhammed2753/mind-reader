import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Alert } from 'react-native';

export default function HintSystem({ player, playersData, coins, onUseHint }) {
  const hints = [
    { type: 'position', label: '🎯 Position', cost: 10 },
    { type: 'team', label: '👕 Team', cost: 15 },
    { type: 'nationality', label: '🌍 Country', cost: 20 },
    { type: 'eliminate', label: '❌ Eliminate 50%', cost: 25 },
  ];

  const useHint = (hint) => {
    if (coins < hint.cost) {
      Alert.alert('Not Enough Coins', `You need ${hint.cost} coins for this hint`);
      return;
    }

    let hintText = '';
    const answers = playersData[player].answers;

    switch (hint.type) {
      case 'position':
        const positionQ = Object.keys(answers).find(q => q.includes('position'));
        hintText = positionQ ? positionQ.replace('Is this player natural position a ', '') : 'Unknown';
        break;
      case 'team':
        const teamQ = Object.keys(answers).find(q => q.includes('playing for'));
        hintText = teamQ ? teamQ.replace('Is this player playing for ', '').replace('?', '') : 'Unknown';
        break;
      case 'nationality':
        const countryQ = Object.keys(answers).find(q => q.includes('born in'));
        hintText = countryQ ? countryQ.replace('Was this player born in ', '').replace('?', '') : 'Unknown';
        break;
      case 'eliminate':
        hintText = 'Eliminated 50% of players!';
        break;
    }

    Alert.alert(`${hint.label} Hint`, hintText);
    onUseHint(hint.type, hint.cost);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>💡 Hints (Coins: {coins})</Text>
      <View style={styles.hints}>
        {hints.map((hint, i) => (
          <TouchableOpacity key={i} style={styles.hintBtn} onPress={() => useHint(hint)}>
            <Text style={styles.hintText}>{hint.label}</Text>
            <Text style={styles.cost}>{hint.cost} 🪙</Text>
          </TouchableOpacity>
        ))}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { backgroundColor: '#16213e', borderRadius: 10, padding: 10, marginBottom: 10 },
  title: { color: '#4ecca3', fontSize: 16, fontWeight: 'bold', marginBottom: 10 },
  hints: { flexDirection: 'row', flexWrap: 'wrap', gap: 5 },
  hintBtn: { backgroundColor: '#0f3460', padding: 10, borderRadius: 5, marginRight: 5, marginBottom: 5 },
  hintText: { color: '#fff', fontSize: 12 },
  cost: { color: '#ffd700', fontSize: 10, marginTop: 2 },
});
