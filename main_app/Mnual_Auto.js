import React ,{ useState, useEffect ,useRef, Component}from 'react';
import { StyleSheet, Text, View , TouchableOpacity,Image} from 'react-native';
// import io from "socket.io-client/dist/socket.io";
import io from "socket.io-client";
// const socket = io("http://127.0.0.1:5000",{transports: ['websocket']});
const socket = io("http://192.168.1.2:5000",{transports: ['websocket']});
export default function ManualAuto({ navigation }) {
  // const [mode, setmode] = useState(0);
  // console.log(mode)

  useEffect(() => {
    

    // console.log(socket)
    
    socket.on('connect', ()=>{
      console.log("socket connected")
    })

    
  //   socket.on("mode", msg => {
  //        console.log(msg)
  // });
  }, []);

  

  return (
    <View style={styles.container}>
      <Image source={require('./assets/car.png')} style={styles.logo} />

      <View style={{flexDirection:"row"}}>
      <TouchableOpacity  onPress={() => {
          // fetch('http://172.28.135.5:5000/mode', {
          //   method: 'POST',
          //   // mode:'no-cors',
          //   headers: {
          //     Accept: 'application/json',
          //     'Content-Type': 'application/json',
          //   },
            
          //   body: JSON.stringify({
          //     mode: 0
              
          //   }),
          // })
          
          // setmode(0);
          // socket.send(0)
          socket.emit('mode', 0);
          navigation.navigate('Control')
        
        
        }
        
        
        } 
          
          style={styles.button}>
        <Text style={styles.buttonText}>Manual</Text>
      </TouchableOpacity>

      <TouchableOpacity 
      onPress={  ()=>{ 
        // setmode(1);
        socket.emit('mode', 1);
      //    fetch('http://172.28.135.5:5000/mode', {
      //   method: 'POST',
      //   // mode:'no-cors',
      //   headers: {
      //     Accept: 'application/json',
      //     'Content-Type': 'application/json',
      //   },
        
      //   body: JSON.stringify({
      //     mode: 1
          
      //   }),
      // })
    }
        }
           style={styles.button}>
        <Text style={styles.buttonText}>Automatic</Text>
      </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#d0f7f5',
    alignItems: 'center',
    justifyContent: 'center',
    

  },
  button: {
    backgroundColor: "#805111",
    padding: 20,
    borderRadius: 5,
    marginRight:20,
    marginLeft:30
    
    
  },
  buttonText: {
    fontSize: 20,
    color: '#fff',
  }, 
  logo: {
    width: 305,
    height: 190,
    marginBottom: 100,
    
  },
});
