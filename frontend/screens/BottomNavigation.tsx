import React from "react";
import { View, TouchableOpacity } from "react-native";
import { Svg, Path } from "react-native-svg";

export const BottomNavigation = () => {
  return (
    <View className="h-16 bg-white border-t border-gray-200 flex-row justify-around items-center px-4">
      <TouchableOpacity>
        <View className="w-8 h-8 bg-gray-200 rounded-full" />
      </TouchableOpacity>
      <TouchableOpacity>
        <View className="w-8 h-8 bg-gray-200 rounded-full" />
      </TouchableOpacity>
      <TouchableOpacity className="bg-white rounded-full p-3 -mt-8 shadow-lg">
        <Svg width="48" height="48" viewBox="0 0 48 48" fill="none">
          <Path
            d="M26.8853 16.0853C26.9178 16.0528 26.952 16.0228 26.9903 15.9974C27.3586 15.7525 29.485 14.5145 31.799 16.8284C34.113 19.1424 32.8749 21.2688 32.6301 21.6371C32.6046 21.6754 32.5746 21.7096 32.5421 21.7421L22.8217 31.4625C22.6993 31.585 22.5471 31.6736 22.3801 31.7195L16.5253 33.3317C15.7772 33.5377 15.0897 32.8503 15.2957 32.1021L16.9079 26.2473C16.9539 26.0803 17.0424 25.9281 17.1649 25.8057L26.8853 16.0853Z"
            fill="#222222"
          />
        </Svg>
      </TouchableOpacity>
      <TouchableOpacity>
        <View className="w-8 h-8 bg-gray-200 rounded-full" />
      </TouchableOpacity>
      <TouchableOpacity>
        <View className="w-8 h-8 bg-gray-200 rounded-full" />
      </TouchableOpacity>
    </View>
  );
};
