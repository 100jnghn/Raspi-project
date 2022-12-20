import time
import RPi.GPIO as GPIO
import Adafruit_MCP3008
from datetime import datetime
from adafruit_htu21d import HTU21D
import busio

#전역 변수 선언 및 초기화
#초음파 센서 trig=20, echo=16
trig = 20
echo = 16
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)
GPIO.output(trig, False)

#초음파 센서를 활용한 거리 측정 함수
def measureDistance():
        global trig, echo
        GPIO.output(trig, True) # 신호 1 발생
        GPIO.output(trig, False) # 신호 0 발생

        while(GPIO.input(echo) == 0):
                pass
        pulse_start = time.time() # 신호 1. 초음파 발생이 시작되었음을 알림
        while(GPIO.input(echo) == 1):
                pass
        pulse_end = time.time() # 신호 0. 초음파 수신 완료를 알림

        pulse_duration = pulse_end - pulse_start
        return 340*100/2*pulse_duration #측정된 값 return


#지하철 접근하면 LED on
ledBySubway = 6 #led-red, GPIO=6
GPIO.setup(ledBySubway, GPIO.OUT)

def ledOnOff(led, onOff): #6번 led on off
        GPIO.output(led, onOff)


#조도 값 측정 후 어두우면 LED on
ledByDark = 5 #led-white, GPIO=5
GPIO.setup(ledByDark, GPIO.OUT)
mcp = Adafruit_MCP3008.MCP3008(clk=11, cs=8, miso=9, mosi=10)

#조도에 의한 led 작동 함수
def controlLedByDark():
        lightPower = mcp.read_adc(0) #조도값 측정
        if lightPower < 250: #조도가 250 미만이면 
                ledOnOff(ledByDark, GPIO.HIGH) #led on
        else: #조도가 250 이상
                ledOnOff(ledByDark, GPIO.LOW) #led off


#사용자 LED 컨트롤 (온습도)
ledByUser = 13 #led-green, GPIO=13
GPIO.setup(ledByUser, GPIO.OUT)

#웹 페이지에서 전송된 값으로 led 제어
def controlLedByUser(onOff):
        GPIO.output(ledByUser, onOff)

#온습도 측정
sda = 2
scl = 3
i2c = busio.I2C(scl, sda)
sensor = HTU21D(i2c)

def getTemperature(): #온도값 return 함수
        return float(sensor.temperature)

def getHumidity(): #습도값 return 함수
        return float(sensor.relative_humidity)

#버튼 제어
button = 21 #button GPIO=21
GPIO.setup(button,GPIO.IN,GPIO.PUD_DOWN)
#btnStatus = GPIO.input(button)
