import { View, Text, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';
import { Search, MapPin } from 'lucide-react-native';
import MapView, { Marker } from 'react-native-maps';

const LOCATIONS = [
  {
    id: 1,
    title: 'Chess Club Tournament',
    location: 'Student Center',
    coordinate: { latitude: 32.9858, longitude: -96.7501 },
  },
  {
    id: 2,
    title: 'Web Development Workshop',
    location: 'ECSW 1.355',
    coordinate: { latitude: 32.9868, longitude: -96.7511 },
  },
  {
    id: 3,
    title: 'Ultimate Frisbee',
    location: 'Soccer Fields',
    coordinate: { latitude: 32.9848, longitude: -96.7491 },
  },
];

export default function MapScreen() {
  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.appTitle}>impulse</Text>
        <Text style={styles.title}>Campus Map</Text>
        <Text style={styles.subtitle}>Find events happening around you</Text>
      </View>

      <View style={styles.searchContainer}>
        <View style={styles.searchBar}>
          <Search size={20} color="#6B7280" />
          <Text style={styles.searchPlaceholder}>Search locations...</Text>
        </View>
      </View>

      <View style={styles.mapContainer}>
        <MapView
          style={styles.map}
          initialRegion={{
            latitude: 32.9858,
            longitude: -96.7501,
            latitudeDelta: 0.01,
            longitudeDelta: 0.01,
          }}
        >
          {LOCATIONS.map((location) => (
            <Marker
              key={location.id}
              coordinate={location.coordinate}
              title={location.title}
              description={location.location}
            />
          ))}
        </MapView>
      </View>

      <ScrollView
        style={styles.locationList}
        horizontal
        showsHorizontalScrollIndicator={false}
      >
        {LOCATIONS.map((location) => (
          <TouchableOpacity key={location.id} style={styles.locationCard}>
            <View style={styles.locationIcon}>
              <MapPin size={20} color="#CA8A04" />
            </View>
            <View>
              <Text style={styles.locationTitle}>{location.title}</Text>
              <Text style={styles.locationAddress}>{location.location}</Text>
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
    paddingHorizontal: 20,
    paddingVertical: 12,
    backgroundColor: '#FFFFFF',
    borderBottomWidth: 1,
    borderBottomColor: '#E5E7EB',
  },
  searchBar: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#F3F4F6',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 8,
  },
  searchPlaceholder: {
    marginLeft: 8,
    color: '#6B7280',
    fontFamily: 'Inter_400Regular',
  },
  mapContainer: {
    flex: 1,
    overflow: 'hidden',
  },
  map: {
    width: '100%',
    height: '100%',
  },
  locationList: {
    position: 'absolute',
    bottom: 20,
    left: 0,
    right: 0,
    paddingHorizontal: 20,
  },
  locationCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFFFFF',
    padding: 16,
    borderRadius: 12,
    marginRight: 12,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  locationIcon: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#FEF3C7',
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 12,
  },
  locationTitle: {
    fontSize: 14,
    fontFamily: 'Inter_600SemiBold',
    color: '#111827',
    marginBottom: 4,
  },
  locationAddress: {
    fontSize: 12,
    fontFamily: 'Inter_400Regular',
    color: '#6B7280',
  },
});