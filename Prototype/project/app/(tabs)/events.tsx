import { View, Text, StyleSheet, ScrollView, Image, TouchableOpacity } from 'react-native';
import { Search, Filter, MapPin, Users, Clock } from 'lucide-react-native';

const EVENTS = [
  {
    id: 1,
    title: 'Chess Club Tournament',
    time: 'Today, 2:00 PM',
    location: 'Student Center',
    attendees: 24,
    image: 'https://images.unsplash.com/photo-1529699211952-734e80c4d42b?w=500',
    category: 'Games',
  },
  {
    id: 2,
    title: 'Web Development Workshop',
    time: 'Tomorrow, 4:00 PM',
    location: 'ECSW 1.355',
    attendees: 45,
    image: 'https://images.unsplash.com/photo-1531403009284-440f080d1e12?w=500',
    category: 'Technology',
  },
  {
    id: 3,
    title: 'Ultimate Frisbee',
    time: 'Saturday, 10:00 AM',
    location: 'Soccer Fields',
    attendees: 16,
    image: 'https://images.unsplash.com/photo-1591591473429-3d9c89b55ca6?w=500',
    category: 'Sports',
  },
];

export default function EventsScreen() {
  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.appTitle}>impulse</Text>
        <Text style={styles.title}>Campus Events</Text>
        <Text style={styles.subtitle}>Find and join activities near you</Text>
      </View>

      <View style={styles.searchContainer}>
        <View style={styles.searchBar}>
          <Search size={20} color="#6B7280" />
          <Text style={styles.searchPlaceholder}>Search events...</Text>
        </View>
        <TouchableOpacity style={styles.filterButton}>
          <Filter size={20} color="#CA8A04" />
        </TouchableOpacity>
      </View>

      <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
        {EVENTS.map((event) => (
          <TouchableOpacity key={event.id} style={styles.eventCard}>
            <Image source={{ uri: event.image }} style={styles.eventImage} />
            <View style={styles.categoryBadge}>
              <Text style={styles.categoryText}>{event.category}</Text>
            </View>
            <View style={styles.eventInfo}>
              <Text style={styles.eventTitle}>{event.title}</Text>
              
              <View style={styles.eventMetaContainer}>
                <View style={styles.eventMeta}>
                  <Clock size={16} color="#6B7280" />
                  <Text style={styles.eventMetaText}>{event.time}</Text>
                </View>
                
                <View style={styles.eventMeta}>
                  <MapPin size={16} color="#6B7280" />
                  <Text style={styles.eventMetaText}>{event.location}</Text>
                </View>

                <View style={styles.eventMeta}>
                  <Users size={16} color="#6B7280" />
                  <Text style={styles.eventMetaText}>{event.attendees} attending</Text>
                </View>
              </View>
            </View>
          </TouchableOpacity>
        ))}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F9FAFB',
  },
  header: {
    paddingTop: 60,
    paddingHorizontal: 20,
    paddingBottom: 20,
    backgroundColor: '#FFFFFF',
  },
  appTitle: {
    fontSize: 24,
    fontFamily: 'Inter_700Bold',
    color: '#111827',
    marginBottom: 12,
  },
  title: {
    fontSize: 28,
    fontFamily: 'Inter_700Bold',
    color: '#111827',
  },
  subtitle: {
    fontSize: 16,
    fontFamily: 'Inter_400Regular',
    color: '#6B7280',
    marginTop: 4,
  },
  searchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 12,
    backgroundColor: '#FFFFFF',
    borderBottomWidth: 1,
    borderBottomColor: '#E5E7EB',
  },
  searchBar: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#F3F4F6',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 8,
    marginRight: 12,
  },
  searchPlaceholder: {
    marginLeft: 8,
    color: '#6B7280',
    fontFamily: 'Inter_400Regular',
  },
  filterButton: {
    padding: 8,
    backgroundColor: '#FEF3C7',
    borderRadius: 8,
  },
  content: {
    flex: 1,
    padding: 20,
  },
  eventCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    marginBottom: 20,
    overflow: 'hidden',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  eventImage: {
    width: '100%',
    height: 200,
  },
  categoryBadge: {
    position: 'absolute',
    top: 16,
    left: 16,
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
  },
  categoryText: {
    color: '#CA8A04',
    fontSize: 12,
    fontFamily: 'Inter_600SemiBold',
  },
  eventInfo: {
    padding: 16,
  },
  eventTitle: {
    fontSize: 18,
    fontFamily: 'Inter_600SemiBold',
    color: '#111827',
    marginBottom: 12,
  },
  eventMetaContainer: {
    gap: 8,
  },
  eventMeta: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  eventMetaText: {
    marginLeft: 8,
    fontSize: 14,
    fontFamily: 'Inter_400Regular',
    color: '#6B7280',
  },
});