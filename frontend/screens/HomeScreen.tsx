import React from "react";
import { ScrollView, View, Text, SafeAreaView } from "react-native";
import { StatusBar } from "./StatusBar";
import { Header } from "./Header";
import { SectionHeader } from "./SectionHeader";
import { ImageCard } from "./ImageCard";
import { BottomNavigation } from "./BottomNavigation";

export const HomeScreen = () => {
  return (
    <SafeAreaView className="flex-1 bg-white">
      <StatusBar />
      <Header />
      <ScrollView className="flex-1">
        <View className="px-4 py-2">
          <View className="mb-6">
            <SectionHeader title="Recommended for you" showSeeAll />
            <ScrollView
              horizontal
              showsHorizontalScrollIndicator={false}
              className="mt-4"
            >
              <ImageCard
                imageUrl="https://cdn.builder.io/api/v1/image/assets/TEMP/df2d3e96c27ab8e0a72a5a0d7d4f956380db3cec"
                altText="ASL Event"
                className="mr-4"
              />
              <ImageCard
                imageUrl="https://cdn.builder.io/api/v1/image/assets/TEMP/54b9c56a8aceff66f8c0f0494490e58fe51a388b"
                altText="QA Event"
                className="mr-4"
              />
            </ScrollView>
          </View>

          <View className="mb-6">
            <Text className="text-lg font-semibold mb-4">Academic</Text>
            <ScrollView horizontal showsHorizontalScrollIndicator={false}>
              <ImageCard
                imageUrl="https://cdn.builder.io/api/v1/image/assets/TEMP/33258e09e8c8e0c579a0016be001f3e676b25d80"
                altText="Calculus Study"
                className="mr-4"
              />
              <ImageCard
                imageUrl="https://cdn.builder.io/api/v1/image/assets/TEMP/cc7f9e2c2d7a874110bf211b74359fcdbd7d85e2"
                altText="Biology Study"
                className="mr-4"
              />
            </ScrollView>
          </View>

          <View className="mb-6">
            <Text className="text-lg font-semibold mb-4">Sports</Text>
            <ScrollView horizontal showsHorizontalScrollIndicator={false}>
              <ImageCard
                imageUrl="https://cdn.builder.io/api/v1/image/assets/TEMP/a47bf8c565fe01a86bca147dcfc98b2eaa46f386"
                altText="Soccer Event"
                className="mr-4"
              />
              <ImageCard
                imageUrl="https://cdn.builder.io/api/v1/image/assets/TEMP/e2cf559ce35a1fb3be163dbbc8a3af55ea8cd37c"
                altText="Fencing Event"
                className="mr-4"
              />
            </ScrollView>
          </View>
        </View>
      </ScrollView>
      <BottomNavigation />
    </SafeAreaView>
  );
};
