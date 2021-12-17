import { StatusBar } from 'expo-status-bar';
import React from 'react';
import { StyleSheet, Text, View ,SafeAreaView} from 'react-native';
import OpenCamera from './OpenCamera.js'
// import OpenCamera from './try.js'
export default function App() {
  
  return (
    <OpenCamera/>
    
  );
}

// const styles = StyleSheet.create({
//   container: {
//     flex: 1,
//     justifyContent: 'center',
//   },
//   button:{
//     justifyContent: "center",
//     alignItems: 'center',
//     backgroundColor: '#121212',
//     margin: 20,
//     borderRadius: 10,
//     height: 50

//   }
// });
