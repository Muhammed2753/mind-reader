import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, TouchableOpacity, ScrollView, TextInput, ActivityIndicator } from 'react-native';
import axios from 'axios';

// CHANGE THIS TO YOUR COMPUTER'S IP ADDRESS
const API_URL = 'http://192.168.1.100:5000';

export default function App() {
  const [gameStarted, setGameStarted] = useState(false);
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [questionNumber, setQuestionNumber] = useState(0);

  const startGame = async () => {
    setLoading(true);
    try {
      await axios.post(`${API_URL}/start`);
      await loadQuestion();
      setGameStarted(true);
    } catch (error) {
      alert('Error connecting to server. Make sure Flask app is running.');
    }
    setLoading(false);
  };

  const loadQuestion = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_URL}/question`);
      setQuestion(response.data.question);
      setProgress(response.data.progress);
      setQuestionNumber(response.data.question_number);
    } catch (error) {
      alert('Error loading question');
    }
    setLoading(false);
  };

  const answerQuestion = async (answer) => {
    setLoading(true);
    try {
      await axios.post(`${API_URL}/question`, { answer });
      await loadQuestion();
    } catch (error) {
      alert('Error submitting answer');
    }
    setLoading(false);
  };

  if (!gameStarted) {
    return (
      <View style={styles.container}>
        <Text style={styles.title}>⚽ Football Akinator</Text>
        <Text style={styles.subtitle}>Think of a football player, manager, or owner</Text>
        <TouchableOpacity style={styles.startButton} onPress={startGame}>
          <Text style={styles.buttonText}>Start Game</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.questionNumber}>Question {questionNumber}</Text>
        <View style={styles.progressBar}>
          <View style={[styles.progressFill, { width: `${progress}%` }]} />
        </View>
      </View>

      <ScrollView style={styles.content}>
        {loading ? (
          <ActivityIndicator size="large" color="#4CAF50" />
        ) : (
          <>
            <Text style={styles.question}>{question}</Text>
            
            <View style={styles.buttonContainer}>
              <TouchableOpacity 
                style={[styles.answerButton, styles.yesButton]} 
                onPress={() => answerQuestion('yes')}
              >
                <Text style={styles.buttonText}>✓ Yes</Text>
              </TouchableOpacity>

              <TouchableOpacity 
                style={[styles.answerButton, styles.noButton]} 
                onPress={() => answerQuestion('no')}
              >
                <Text style={styles.buttonText}>✗ No</Text>
              </TouchableOpacity>

              <TouchableOpacity 
                style={[styles.answerButton, styles.idkButton]} 
                onPress={() => answerQuestion("i don't know")}
              >
                <Text style={styles.buttonText}>? I Don't Know</Text>
              </TouchableOpacity>
            </View>
          </>
        )}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1a1a2e',
    paddingTop: 50,
  },
  header: {
    padding: 20,
  },
  title: {
    fontSize: 36,
    fontWeight: 'bold',
    color: '#fff',
    textAlign: 'center',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 16,
    color: '#aaa',
    textAlign: 'center',
    marginBottom: 30,
  },
  questionNumber: {
    fontSize: 18,
    color: '#4CAF50',
    marginBottom: 10,
  },
  progressBar: {
    height: 8,
    backgroundColor: '#333',
    borderRadius: 4,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#4CAF50',
  },
  content: {
    flex: 1,
    padding: 20,
  },
  question: {
    fontSize: 24,
    color: '#fff',
    textAlign: 'center',
    marginVertical: 40,
    fontWeight: '600',
  },
  buttonContainer: {
    gap: 15,
  },
  startButton: {
    backgroundColor: '#4CAF50',
    padding: 20,
    borderRadius: 12,
    marginHorizontal: 40,
  },
  answerButton: {
    padding: 18,
    borderRadius: 12,
    marginBottom: 12,
  },
  yesButton: {
    backgroundColor: '#4CAF50',
  },
  noButton: {
    backgroundColor: '#f44336',
  },
  idkButton: {
    backgroundColor: '#FF9800',
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
    textAlign: 'center',
  },
});
