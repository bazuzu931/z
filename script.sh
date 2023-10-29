#!/bin/bash



# lsof -n -i4TCP:5037 | grep LISTEN;

# kill -9;


echo $AVD_NAME ;
adb devices ;
emulator -avd $AVD_NAME -no-boot-anim -gpu swiftshader_indirect -no-audio  & 

echo 'start sleep ...' ;
sleep 70 ;

appium='appium';
"${appium}" & disown;

sleep 7;
python3 main.py ;
