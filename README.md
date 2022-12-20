# Raspi-project
라즈베리파이를 활용한 지하철 승강장 관리 시스템 입니다.

--하드웨어 정보--
카메라 1대, LED 2개, 스위치 1개, 초음파 센서 1개, 온습도 센서 1개, 조도 센서 1개

<LED1> – GPIO5 (어두울 때 켜지는 led-white)
<LED2> – GPIO6 (지하철 접근 시 작동하는 led-red)
<LED3> – GPIO13 (온습도 조절 장치 – 관리자가 웹 페이지에서 작동시킴. led-green)
<스위치> – GPIO23 (누르면 직원 호출 메시지 전송)
<초음파 센서> – trig=GPIO20, echo=GPIO16
<온습도 센서> – SDA1, SCL1
<조도 센서> – SPICEO, SPISCLK, SPIMISO, SPIMOSI
<파이 카메라>

--소프트웨어 정보--
<mqtt.py> - mqtt publish로 led, camera 토픽을 관리한다. connect 시 led와 camera 토픽을 등록하고, while 문을 계속 돌며 1초에 한 번 초음파센서, 조도센서, 온습도센서, 버튼, 카메라에서 오는 정보들을 publish 한다.
<circuit.py> - led 제어, 초음파 센서와 조도 센서, 온습도 센서, 버튼을 제어
<camera.py> - 카메라 제어
<app.py> - 웹브라우저로부터 접속과 요청을 받아 처리하는 플라스크 앱
<project.html> - 사용자가 접속하는 웹 페이지. 접속하면 사용자 이름을 입력하도록 하고 입력된 값을 웹 페이지에 출력. mqtt값을 전송함으로써 웹 페이지에서 라즈베리파이의 하드웨어 부분을 제어한다. (주석은 모두 // 로 표현)
<mqttio5.js> - 웹 페이지 구현과 토픽을 불러오는 js파일. mqtt와 웹브라우저를 연결하고 하드웨어 센서들의 정보를 읽어 웹에 출력한다. 
<cam.js> - 라즈베리파이에서 카메라로 찍은 사진을 웹에 출력하는 js파일. mjpeg이 작동하지 않아 1초에 한 번씩 사진을 찍고 전송하여 대체
<myChart.js>
라즈베리파이에서 초음파 센서로 측정한 값을 웹에 출력하는 js파일. 지하철 도착 정보를 다음과 같이 나타낸다.
          ( A역 ======지하철 --------------------- B역 )
          ( A역 ====================지하철 ------- B역 )