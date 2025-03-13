import React from "react";
import { View, Text, TouchableOpacity } from "react-native";

interface SectionHeaderProps {
  title: string;
  showSeeAll?: boolean;
  onSeeAllPress?: () => void;
}

export const SectionHeader: React.FC<SectionHeaderProps> = ({
  title,
  showSeeAll = false,
  onSeeAllPress,
}) => {
  return (
    <View className="flex-row justify-between items-center">
      <Text className="text-lg font-semibold">{title}</Text>
      {showSeeAll && (
        <TouchableOpacity onPress={onSeeAllPress}>
          <Text className="text-blue-500">See all</Text>
        </TouchableOpacity>
      )}
    </View>
  );
};
