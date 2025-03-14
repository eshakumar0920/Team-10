import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Link } from 'expo-router';
import { Activity } from 'lucide-react-native';

export default function LoginScreen() {
  return (
    <View style={styles.container}>
      <View style={styles.content}>
        <View style={styles.logoContainer}>
          <Activity size={64} color="#000000" strokeWidth={1.5} />
          <View style={styles.logoAccent} />
          <View style={[styles.logoAccent, styles.logoAccentRight]} />
        </View>

        <Text style={styles.welcomeTitle}>Welcome to</Text>
        <Text style={styles.impulseTitle}>impulse</Text>
        
        <View style={styles.taglineContainer}>
          <Text style={styles.taglineText}>Where students</Text>
          <Text style={styles.taglineText}>meet</Text>
          <Text style={styles.taglineText}>connection</Text>
        </View>

        <View style={styles.buttonContainer}>
          <TouchableOpacity style={styles.button}>
            <Text style={styles.buttonText}>Register</Text>
          </TouchableOpacity>

          <Link href="/(tabs)" asChild>
            <TouchableOpacity style={[styles.button, styles.signInButton]}>
              <Text style={styles.buttonText}>Sign in</Text>
            </TouchableOpacity>
          </Link>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#FFFFFF',
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  logoContainer: {
    position: 'relative',
    marginBottom: 48,
  },
  logoAccent: {
    position: 'absolute',
    width: 8,
    height: 8,
    backgroundColor: '#EAB308',
    borderRadius: 4,
    top: 0,
    left: -4,
  },
  logoAccentRight: {
    left: 'auto',
    right: -4,
  },
  welcomeTitle: {
    fontSize: 32,
    fontFamily: 'Inter_400Regular',
    color: '#000000',
    textAlign: 'center',
  },
  impulseTitle: {
    fontSize: 40,
    fontFamily: 'Inter_700Bold',
    color: '#000000',
    textAlign: 'center',
    marginBottom: 32,
  },
  taglineContainer: {
    alignItems: 'center',
    marginBottom: 64,
  },
  taglineText: {
    fontSize: 36,
    fontFamily: 'Inter_600SemiBold',
    color: '#000000',
    textAlign: 'center',
    lineHeight: 44,
  },
  buttonContainer: {
    width: '100%',
    gap: 16,
  },
  button: {
    backgroundColor: '#FEF9C3',
    paddingVertical: 16,
    borderRadius: 100,
    width: '100%',
  },
  signInButton: {
    backgroundColor: '#FEF3C7',
  },
  buttonText: {
    color: '#000000',
    fontSize: 16,
    fontFamily: 'Inter_600SemiBold',
    textAlign: 'center',
  },
});