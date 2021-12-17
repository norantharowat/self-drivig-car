import React from 'react';
import { StyleSheet, Text , View , TouchableOpacity,Image} from 'react-native';

export default function Control() {
  return (
    <View style={styles.container}>    
            
        <TouchableOpacity onPress={()=>{
          fetch('http://172.28.128.66:80/direction', {
            method: 'POST',
            // mode:'no-cors',
            headers: {
              Accept: 'application/json',
              'Content-Type': 'application/json',
            },
            
            body: "F",
          })
        }
          
        } 
        style={styles.arrowUp}></TouchableOpacity>  

        <TouchableOpacity 
        onPress={() => {
          fetch('http://172.28.128.66:80/direction', {
            method: 'POST',
            // mode:'no-cors',
            headers: {
              Accept: 'application/json',
              'Content-Type': 'application/json',
            },
            
            body: "B",
          })
        }} 
        style={styles.arrowDown}></TouchableOpacity>

        <TouchableOpacity onPress={() => {
          fetch('http://172.28.128.66:80/direction', {
            method: 'POST',
            // mode:'no-cors',
            headers: {
              Accept: 'application/json',
              'Content-Type': 'application/json',
            },
            
            body: "L",
          })
        }} style={styles.arrowLeft}></TouchableOpacity>

        <TouchableOpacity onPress={() => 
        {
          fetch('http://172.28.128.66:80/direction', {
            method: 'POST',
            // mode:'no-cors',
            headers: {
              Accept: 'application/json',
              'Content-Type': 'application/json',
            },
            
            body: "R",
          })
        }} style={styles.arrowRight}></TouchableOpacity>

        <TouchableOpacity onPress={() => 
        {
          fetch('http://172.28.128.66:80/direction', {
            method: 'POST',
            // mode:'no-cors',
            headers: {
              Accept: 'application/json',
              'Content-Type': 'application/json',
            },
            
            body: "S",
          })
        }} style={styles.dot}>
          {/* <Text>Stop</Text> */}
        </TouchableOpacity>

        
        
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#d0f7f5',
 
  },
  arrowUp: {
    borderTopWidth: 0,
    borderRightWidth: 70,
    borderBottomWidth: 70,
    borderLeftWidth: 70,
    borderTopColor: 'transparent',
    borderRightColor: 'transparent',
    borderBottomColor: "#805111",
    borderLeftColor: 'transparent',
    position:'absolute',
    top:200,
    left:145
},

arrowDown: {
    borderTopWidth: 70,
    borderRightWidth: 70,
    borderBottomWidth: 0,
    borderLeftWidth: 70,
    borderTopColor: "#805111",
    borderRightColor: 'transparent',
    borderBottomColor: 'transparent',
    borderLeftColor: 'transparent',
    position:'absolute',
    top:450,
    left:145
    
},

arrowLeft: {
    borderTopWidth: 70,
    borderRightWidth: 70,
    borderBottomWidth: 70,
    borderLeftWidth: 0,
    borderTopColor: 'transparent',
    borderRightColor: "#805111",
    borderBottomColor: 'transparent',
    borderLeftColor: 'transparent',
    position:'absolute',
    left:50,
    top:300
    
},

arrowRight: {
    borderTopWidth: 70,
    borderRightWidth: 0,
    borderBottomWidth: 70,
    borderLeftWidth: 70,
    borderTopColor: 'transparent',
    borderRightColor: 'transparent',
    borderBottomColor: 'transparent',
    borderLeftColor: "#805111",
    position:'absolute',
    right:30,
    top:300
},
dot:{
  height: 100,
  width: 100,
  position:'absolute',
  top:300,
  left:168,
  backgroundColor: '#F08080',
  borderRadius: 250,
 
}
});
