import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, ScrollView, StyleSheet, Image, Alert } from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import * as Haptics from 'expo-haptics';
import playersData from '../data/players.json';

export default function GameScreen({ route, navigation }) {
  const { mode } = route.params;
  const [player, setPlayer] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [remaining, setRemaining] = useState([]);
  const [gameOver, setGameOver] = useState(false);
  const [timer, setTimer] = useState(mode === 'timeattack' ? 60 : null);

  useEffect(() => {
    startGame();
  }, []);

  useEffect(() => {
    if (mode === 'timeattack' && timer > 0 && !gameOver) {
      const interval = setInterval(() => setTimer(t => t - 1), 1000);
      return () => clearInterval(interval);
    }
    if (timer === 0) endGame(false);
  }, [timer, gameOver]);

  const startGame = () => {
    const players = Object.keys(playersData);
    const random = players[Math.floor(Math.random() * players.length)];
    setPlayer(random);
    setRemaining(players);
    setQuestions([]);
    setGameOver(false);
  };

  const askQuestion = (q) => {
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    const answer = playersData[player].answers[q];
    const newQuestions = [...questions, { q, answer }];
    setQuestions(newQuestions);
    
    const filtered = remaining.filter(p => {
      return newQuestions.every(qa => playersData[p].answers[qa.q] === qa.answer);
    });
    setRemaining(filtered);
  };

  const makeGuess = (name) => {
    Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
    if (name === player) {
      Alert.alert('🎉 Correct!', `You guessed ${player}!`);
      endGame(true);
    } else {
      Alert.alert('❌ Wrong!', `It was ${player}`);
      endGame(false);
    }
  };

  const endGame = (won) => {
    setGameOver(true);
  };

  const availableQuestions = player 
    ? Object.keys(playersData[player].answers).filter(q => !questions.find(qa => qa.q === q))
    : [];

  return (
    <LinearGradient colors={['#1a1a2e', '#16213e']} style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Text style={styles.backBtn}>← Back</Text>
        </TouchableOpacity>
        {timer !== null && <Text style={styles.timer}>⏱️ {timer}s</Text>}
      </View>

      {!gameOver ? (
        <>
          <View style={styles.info}>
            <Text style={styles.infoText}>Questions: {questions.length}</Text>
            <Text style={styles.infoText}>Remaining: {remaining.length}</Text>
          </View>

          <ScrollView style={styles.section}>
            <Text style={styles.sectionTitle}>Asked Questions:</Text>
            {questions.map((qa, i) => (
              <View key={i} style={styles.questionItem}>
                <Text style={styles.qText}>{qa.q}</Text>
                <Text style={[styles.answer, qa.answer === 'yes' ? styles.yes : styles.no]}>
                  {qa.answer}
                </Text>
              </View>
            ))}
          </ScrollView>

          <ScrollView style={styles.section}>
            <Text style={styles.sectionTitle}>Ask Question:</Text>
            {availableQuestions.slice(0, 5).map((q, i) => (
              <TouchableOpacity key={i} style={styles.qBtn} onPress={() => askQuestion(q)}>
                <Text style={styles.qBtnText}>{q}</Text>
              </TouchableOpacity>
            ))}
          </ScrollView>

          <ScrollView horizontal style={styles.guessSection}>
            {remaining.slice(0, 10).map((p, i) => (
              <TouchableOpacity key={i} style={styles.playerBtn} onPress={() => makeGuess(p)}>
                <Text style={styles.playerText}>{p}</Text>
              </TouchableOpacity>
            ))}
          </ScrollView>
        </>
      ) : (
        <View style={styles.gameOver}>
          <Text style={styles.gameOverText}>Game Over!</Text>
          <Image source={{ uri: playersData[player].image_url }} style={styles.img} />
          <Text style={styles.playerName}>{player}</Text>
          <TouchableOpacity style={styles.newGameBtn} onPress={startGame}>
            <Text style={styles.newGameText}>New Game</Text>
          </TouchableOpacity>
        </View>
      )}
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 10 },
  header: { flexDirection: 'row', justifyContent: 'space-between', padding: 15 },
  backBtn: { color: '#4ecca3', fontSize: 18 },
  timer: { color: '#e94560', fontSize: 20, fontWeight: 'bold' },
  info: { flexDirection: 'row', justifyContent: 'space-around', padding: 10, backgroundColor: '#16213e', borderRadius: 10, marginBottom: 10 },
  infoText: { color: '#fff', fontSize: 14 },
  section: { flex: 1, backgroundColor: '#16213e', borderRadius: 10, padding: 10, marginBottom: 10 },
  sectionTitle: { fontSize: 16, fontWeight: 'bold', color: '#4ecca3', marginBottom: 10 },
  questionItem: { flexDirection: 'row', justifyContent: 'space-between', padding: 10, backgroundColor: '#0f3460', borderRadius: 5, marginBottom: 5 },
  qText: { color: '#fff', flex: 1, fontSize: 12 },
  answer: { fontWeight: 'bold', fontSize: 12 },
  yes: { color: '#4ecca3' },
  no: { color: '#e94560' },
  qBtn: { backgroundColor: '#0f3460', padding: 12, borderRadius: 5, marginBottom: 5 },
  qBtnText: { color: '#fff', fontSize: 12 },
  guessSection: { maxHeight: 80, backgroundColor: '#16213e', borderRadius: 10, padding: 10 },
  playerBtn: { backgroundColor: '#4ecca3', padding: 15, borderRadius: 5, marginRight: 10 },
  playerText: { color: '#1a1a2e', fontWeight: 'bold' },
  gameOver: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  gameOverText: { fontSize: 32, fontWeight: 'bold', color: '#4ecca3', marginBottom: 20 },
  img: { width: 200, height: 200, borderRadius: 100, marginBottom: 20 },
  playerName: { fontSize: 24, color: '#fff', marginBottom: 30 },
  newGameBtn: { backgroundColor: '#4ecca3', padding: 15, borderRadius: 10, width: 200 },
  newGameText: { fontSize: 18, fontWeight: 'bold', textAlign: 'center', color: '#1a1a2e' },
});
