import { StatusBar } from 'expo-status-bar';
import React, { useState, useEffect ,useRef, Component} from 'react';
import { StyleSheet, Text, View ,TouchableOpacity, SafeAreaView,Modal,Image} from 'react-native';
import { Camera } from 'expo-camera';
import {FontAwesome } from "@expo/vector-icons"
// import io from 'socket.io-client'
// import useSocket from 'use-socket.io-client';



export default function OpenCamera() {
  const camRef = useRef(null);
  const [hasPermission, setHasPermission] = useState(null);
  const [type, setType] = useState(Camera.Constants.Type.back);
  const [capturedPhoto, setCapturedPhoto] = useState(null);
  const [Open, setOpen] = useState(false);
  const [mode, setmode] = useState(0);
//   const [socket] = useSocket('ws://192.168.1.2:5000')
  
//   useEffect(()=>{
//     // fetch('http://192.168.1.2:5000/mode',{method:'GET'}).then(response=> response.json()).then(data=> console.log(data.mode));
//     console.log("msg")
//     socket = io("ws://192.168.1.2:5000");
//     socket.on('connect', (data)=>{
//         console.log(data)
//     })
//   })

  useEffect(() => {
    (async () => {
      const { status } = await Camera.requestPermissionsAsync();
      setHasPermission(status === 'granted');
    })();
  }, []);

  if (hasPermission === null) {
    return <View />;
  }
  if (hasPermission === false) {
    return <Text>No access to camera</Text>;
  }

  async function takePicture(){
    if(camRef){
      const data = await camRef.current.takePictureAsync({
        quality: 0.1,
        base64: true,
        skipProcessing:false,
        

      });
      
        fetch('http://192.168.1.2:5000/photo', {
            method: 'POST',
            // mode:'no-cors',
            headers: {
              Accept: 'application/json',
              'Content-Type': 'application/json',
            },
            
            body: JSON.stringify({
              photo: data.base64
              
            }),
          });
            
      
        setCapturedPhoto(data.uri);
        setOpen(true);
        // console.log(data.base64);

    }
  }
  return (
    <SafeAreaView style={styles.container}>
      <Camera 
      style={{ flex: 1 }} 
      type={type}
      ref={camRef}
      >
        
      </Camera>
      <TouchableOpacity style={styles.button}
        onPress={takePicture}
      >
       <FontAwesome name="camera"
        size={23}
        color="#FFF"
        />

      </TouchableOpacity>

      {/* {capturedPhoto && 
      <Modal
      animationType="slide"
      transparent={false}
      visible={Open}
      >
        <View style={{flex:1 , justifyContent:'center', alignItems:'center', margin:20}}>
          <TouchableOpacity style={{ margin:10}} onPress={()=> setOpen(false)}>
          <FontAwesome name="window-close"
          size={50} color="#FF0000"/>
          </TouchableOpacity>
        <Image
        style={{ width:"100%", height:'75%',borderRadius:20}}
        source={{ uri: capturedPhoto}}
        />
        </View>
        
      </Modal>
        } */}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
  },
  button:{
    justifyContent: "center",
    alignItems: 'center',
    backgroundColor: '#121212',
    margin: 20,
    borderRadius: 10,
    height: 50

  }
});
