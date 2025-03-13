import React from "react";
import { View, Image } from "react-native";

interface ImageCardProps {
  imageUrl: string;
  altText: string;
  className?: string;
}

export const ImageCard: React.FC<ImageCardProps> = ({
  imageUrl,
  altText,
  className = "",
}) => {
  return (
    <View className={`rounded-lg overflow-hidden ${className}`}>
      <Image
        source={{ uri: imageUrl }}
        className="w-40 h-40"
        accessibilityLabel={altText}
      />
    </View>
  );
};
