import * as React from 'react';
import { StyleSheet } from 'react-native';

import EditScreenInfo from '../components/EditScreenInfo';
import { Text, View } from '../components/Themed';
import { MonoText } from '../components/StyledText';

function RobotStatusComponent(){
  return (
    <View>
      <MonoText>Cloud Server Connection  : </MonoText>
      <MonoText>Cloud Server Public IP : </MonoText>
      <MonoText>Cloud - Robot Connection : </MonoText>
      <MonoText>Robot Public Ip : </MonoText>
      <MonoText>Robot Internal IP : </MonoText>
      <MonoText>Robot SLAM ROS Status : </MonoText>
    </View>
  )
}

export default function ConnectionStatusScreen() {
  return (
    <View style={styles.container}>
      <MonoText style={styles.title}>Connection Status</MonoText>
      <View style={styles.separator} lightColor="#eee" darkColor="rgba(255,255,255,0.1)" />
      <RobotStatusComponent/>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  separator: {
    marginVertical: 30,
    height: 1,
    width: '80%',
  },
});
