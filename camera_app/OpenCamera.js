import { StatusBar } from 'expo-status-bar';
import React, { useState, useEffect ,useRef} from 'react';
import { StyleSheet, Text, View ,TouchableOpacity, SafeAreaView,Modal,Image} from 'react-native';
import { Camera } from 'expo-camera';
import {FontAwesome } from "@expo/vector-icons"
import io from "socket.io-client";
// const socket = io("http://127.0.0.1:5000",{transports: ['websocket']});
const socket = io("http://192.168.1.2:5000",{transports: ['websocket']});


export default function OpenCamera() {
  
  const camRef = useRef(null);
  const [hasPermission, setHasPermission] = useState(null);
  const [type, setType] = useState(Camera.Constants.Type.back);
  const [capturedPhoto, setCapturedPhoto] = useState(null);
  const [Open, setOpen] = useState(false);
  // const [pick, setPick] = useState(0);
  let mode = 0;
  let myvar;
  
  useEffect(() => {


    (async () => {
      const { status } = await Camera.requestPermissionsAsync();
      setHasPermission(status === 'granted');
    })();
    
  

  },[]);
  
  useEffect(() => {
    
    
    socket.on('connect', ()=>{
      console.log("socket connected")
    })
    
    socket.on("mode", msg => {
      if (msg === 0){
        // console.log("msg is 0")
        // setPick(0);
        mode =0 ;
      }else if(msg === 1){
        // console.log("msg is 1")
        // setPick(1);
        mode = 1;
      }
      
      
      console.log(mode);
      if (mode === 1){
        myvar = setInterval(()=>{
          takePicture();
        // socket.emit("test" , "tessssst");
        // console.log("test");
      } , 1000)
    } else {
      clearInterval(myvar);
    } 
    
  });
  

  
  
},[]);
  

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
        skipProcessing:false

      });
        // fetch('http://172.28.135.5:5000/photo', {
        //     method: 'POST',
        //     // mode:'no-cors',
        //     headers: {
        //       Accept: 'application/json',
        //       'Content-Type': 'application/json',
        //     },
            
        //     body: JSON.stringify({
        //       photo: data.base64
              
        //     }),
        //   });
            
      
        // setCapturedPhoto(data.base64);
        // setCapturedPhoto(data.base64);
        
        setOpen(true);
        socket.emit('picture', data.base64);
        console.log(data.uri)
        // console.log(data.base64);

    }
  }


  // function takePicture(){
  //   if(camRef){
  //     const data = camRef.current.takePictureAsync({
  //       quality: 0.5,
  //       base64: true,
  //       skipProcessing:false

  //     });
  //       // fetch('http://172.28.135.5:5000/photo', {
  //       //     method: 'POST',
  //       //     // mode:'no-cors',
  //       //     headers: {
  //       //       Accept: 'application/json',
  //       //       'Content-Type': 'application/json',
  //       //     },
            
  //       //     body: JSON.stringify({
  //       //       photo: data.base64
              
  //       //     }),
  //       //   });
            
      
  //       // setCapturedPhoto(data.base64);
  //       setCapturedPhoto(data.base64);
  //       socket.emit('picture', capturedPhoto);
  //       setOpen(true);
  //       // console.log(data.base64);

  //   }
  // }

  // if(mode === 1){
  //   setTimeout(function(){
  //     takePicture();
  //     // socket.emit('test', "Tessssssssst");
  //   }, 5000)
  // }
  // if(mode === 1){
  //   setTimeout(function(){
  //     console.log("Iam here")
  //     // takePicture();
  //   }, 4000)
  // }

  return (
    <SafeAreaView style={styles.container}>
      <Camera 
      style={{ flex: 1 }} 
      type={type}
      ref={camRef}
      >
        
      </Camera>
      
      {/* <TouchableOpacity style={styles.button}
        onPress={takePicture}
      >
       <FontAwesome name="camera"
        size={23}
        color="#FFF"
        />

      </TouchableOpacity> */}
       
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
