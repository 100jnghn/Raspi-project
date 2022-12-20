# publisher

import time
from datetime import datetime
import paho.mqtt.client as mqtt
import circuit #초음파 센서 입력 모듈 임포트
import camera #카메라 제어 모듈 임포트

import RPi.GPIO as GPIO

flag = False

def on_connect(client, userdata, flag, rc): #connect시 led와 camera 토픽 등록
        client.subscribe("led", qos = 0)
        client.subscribe("camera", qos = 0)

def on_message(client, userdata, msg) : #메시지가 오면 호출. 
        #카메라 image 코드
        global flag
        command = msg.payload.decode("utf-8")
        if command == "action": #카메라 촬영 command
                print("action msg received..")
                flag = True


        msg = int(msg.payload);
        if msg == 0 or msg == 1: #msg가 0 or 1이면 led 제어
                circuit.controlLedByUser(msg)

broker_ip = "localhost" # 현재 이 컴퓨터를 브로커로 설정

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_ip, 1883)
client.loop_start()

while(True):

        #지하철 거리 측정 -  웹에 거리 전송, 가까워지면 LED on
        distance = circuit.measureDistance() #초음파 센서로 거리 측정한 값

        if distance < 20: #측정한 거리가 20 미만이면
                circuit.ledOnOff(circuit.ledBySubway, GPIO.HIGH) #led on
        else: #측정한 거리가 20 이상이면
                circuit.ledOnOff(circuit.ledBySubway, GPIO.LOW) #led off

        #거리 publish
        client.publish("ultrasonic", distance, qos=0)

        #조도 측정 -  어두워지면 LED on
        circuit.controlLedByDark()

        #온도 측정, publish
        temp = circuit.getTemperature()
        client.publish("temparature", temp, qos=0)

        #습도 측정, publish
        humi = circuit.getHumidity()
        client.publish("humidity", humi, qos=0)

        #버튼 상태, 버튼이 눌리면 publish
        circuit.btnStatus = GPIO.input(circuit.button)
        if circuit.btnStatus==1:
                client.publish("button", circuit.btnStatus, qos=0)
                print(circuit.btnStatus)

        #사진 촬영, publish
        imageFileName = myCamera.takePicture()
        client.publish("image", imageFileName, qos=0)

        time.sleep(1) #while문 1초에 한 번 실행

client.loop_stop()
client.disconnect()
