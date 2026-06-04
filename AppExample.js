import React, { useState } from 'react';
import { StyleSheet, Text, View, TouchableOpacity, ScrollView, SafeAreaView } from 'react-native';

// Import your football_characters.json here
const playersData = require('./football_characters.json');

export default function App() {
  const [player, setPlayer] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [gameOver, setGameOver] = useState(false);

  const startGame = () => {
    const players = Object.keys(playersData);
    const random = players[Math.floor(Math.random() * players.length)];
    setPlayer(random);
    setQuestions([]);
    setGameOver(false);
  };

  const askQuestion = (q) => {
    const answer = playersData[player].answers[q];
    setQuestions([...questions, { q, answer }]);
  };

  const guess = (name) => {
    alert(name === player ? 'Correct!' : `Wrong! It was ${player}`);
    setGameOver(true);
  };

  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.title}>⚽ Football Guess</Text>
      
      {!player && (
        <TouchableOpacity style={styles.btn} onPress={startGame}>
          <Text style={styles.btnText}>Start Game</Text>
        </TouchableOpacity>
      )}

      {player && !gameOver && (
        <ScrollView>
          {questions.map((qa, i) => (
            <Text key={i} style={styles.text}>{qa.q}: {qa.answer}</Text>
          ))}
          
          <TouchableOpacity style={styles.btn} onPress={() => askQuestion(Object.keys(playersData[player].answers)[0])}>
            <Text style={styles.btnText}>Ask Question</Text>
          </TouchableOpacity>

          <TouchableOpacity style={styles.btn} onPress={() => guess(player)}>
            <Text style={styles.btnText}>Guess: {player}</Text>
          </TouchableOpacity>
        </ScrollView>
      )}

      {gameOver && (
        <TouchableOpacity style={styles.btn} onPress={startGame}>
          <Text style={styles.btnText}>New Game</Text>
        </TouchableOpacity>
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#1a1a2e', padding: 20 },
  title: { fontSize: 28, color: '#fff', textAlign: 'center', marginBottom: 20 },
  text: { color: '#fff', marginBottom: 10 },
  btn: { backgroundColor: '#4ecca3', padding: 15, borderRadius: 10, marginTop: 10 },
  btnText: { color: '#1a1a2e', fontSize: 16, textAlign: 'center', fontWeight: 'bold' },
});
