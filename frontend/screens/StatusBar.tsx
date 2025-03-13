import React from "react";
import { View, Text } from "react-native";

export const StatusBar = () => {
  return (
    <View className="h-12 bg-white px-4 flex-row items-center justify-between">
      <Text className="text-base font-medium">9:41</Text>
      <View className="flex-row items-center space-x-2">
        <View className="w-4 h-4 bg-black rounded-full" />
        <View className="w-4 h-4 bg-black rounded-full" />
        <View className="w-6 h-3 bg-black rounded-md" />
      </View>
    </View>
  );
};
