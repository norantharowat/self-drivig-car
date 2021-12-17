import 'react-native-gesture-handler';
import { StatusBar } from 'expo-status-bar';
import React from 'react';
import { StyleSheet, Text, View , TouchableOpacity,Image} from 'react-native';
import ManualAuto from "./Mnual_Auto"
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import Control from './Control'

const Stack = createStackNavigator();
export default function App() {
  return (
    <NavigationContainer>
      
      <Stack.Navigator>
        <Stack.Screen name="Home" component={ManualAuto} />
        <Stack.Screen name="Control" component={Control} />
      </Stack.Navigator>


{/* 
      <View style={styles.container}>
        <ManualAuto/>
      </View> */}
    </NavigationContainer>
     
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#d0f7f5',
    alignItems: 'center',
    justifyContent: 'center',
    

  },
  
});
