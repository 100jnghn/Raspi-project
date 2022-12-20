var port = 9001 // mosquitto의 디폴트 웹 포트
var client = null; // null이면 연결되지 않았음 

function startConnect() { // 접속을 시도하는 함수

        clientID = "clientID-" + parseInt(Math.random() * 100); // 랜덤한 사용자 ID 생성

        // 사용자가 입력한 브로커의 IP 주소와 포트 번호 알아내기
        broker = document.getElementById("broker").value; // 브로커의 IP 주소

        // id가 message인 DIV 객체에 브로커의 IP와 포트 번호 출력
        // MQTT 메시지 전송 기능을 모두 가징 Paho client 객체 생성
        client = new Paho.MQTT.Client(broker, Number(port), clientID);

        // client 객체에 콜백 함수 등록
        client.onConnectionLost = onConnectionLost; // 접속이 끊어졌을 때 실행되는 함수 등록
        client.onMessageArrived = onMessageArrived; // 메시지가 도착하였을 때 실행되는 함수 등록

        // 브로커에 접속. 매개변수는 객체 {onSuccess : onConnect}로서, 객체의 프로퍼티는 onSuccess이고 >그 값이 onConnect.
        // 접속에 성공하면 onConnect 함수를 실행하라는 지시
        client.connect({
                onSuccess: onConnect,
        });
}


var isConnected = false;

// 브로커로의 접속이 성공할 때 호출되는 함수
function onConnect() {
        isConnected = true;

        //document.getElementById("messages").innerHTML += '<span>Connected</span><br/>'; //Connected 출력

        subscribe("temparature"); //접속하면 토픽 temparature를 subscribe한다
        subscribe("humidity"); // 접속하면 토픽 humidity를 subscribe한다.
        subscribe("button"); // 접속하면 토픽 button을 subscribe 한다.
}
var topicSave;
function subscribe(topic) { //subscribe하는 함수
        if(client == null) return;
        if(isConnected != true) {
                topicSave = topic;
                window.setTimeout("subscribe(topicSave)", 500);
                return
        }

        client.subscribe(topic); // 브로커에 subscribe
}

function publish(topic, msg) { //publish 하는 함수
        if(client == null) return; // 연결되지 않았음
        client.send(topic, msg, 0, false);
}

function unsubscribe(topic) { //unsubscribe 함수. 해당 토픽에 대한 subscribe 중지
        if(client == null || isConnected != true) return;
     
        client.unsubscribe(topic, null); // 브로커에 subscribe
}

// 접속이 끊어졌을 때 호출되는 함수
function onConnectionLost(responseObject) { // 매개변수인 responseObject는 응답 패킷의 정보를 담은 개체
        //주석문을 지우면 출력됨.
        //document.getElementById("messages").innerHTML += '<span>오류 : 접속 끊어짐</span><br/>';
        //if (responseObject.errorCode !== 0) {
                //document.getElementById("messages").innerHTML += '<span>오류 : ' + + responseObject.errorMessage + '</span><br/>';
        //}
}

// 메시지가 도착할 때 호출되는 함수
function onMessageArrived(msg) { // 매개변수 msg는 도착한 MQTT 메시지를 담고 있는 객체
        console.log("onMessageArrived: " + msg.payloadString);

        //도착한 메시지 출력.
        if(msg.destinationName == "ultrasonic"){ //메시지가 ultrasonic인 경우
                //addChartData(100-parseFloat(msg.payloadString));
                distance = 100-parseInt(msg.payloadString);
                if(distance < 0){ //측정거리 100 이상이면 0을 차트에 추가. 웹에 “도착정보없음” 메시지 전송
                        distance = 0;
                        addChartData(distance);
                        document.getElementById ("distance").innerHTML='<span>'+'도착정보없음...'+ '</span><br/>';
                }
               
                else{ //측정거리가 100 이하면 차트에 distance 값 추가.
                        addChartData(distance); 
                        if(distance>=0 && distance<90) //distance 0~90이면 
                                document.getElementById ("distance").innerHTML='<span>'+'한성대입구  접근중...   '+Math.round(10-distance/10)+'분 후 도착'+'</span><br/>'; //웹페이지에 “ ~접근중, n분후 도착” 메시지 전송
                        else if (distance>=90) //distance 90이상
                                document.getElementById ("distance").innerHTML='<span>'+'한성대입구  도착!'+'</span><br/>'; //웹페이지에 “ ~도착! 메시지 전송”

                }
        }

        if(msg.destinationName == "image") { //메시지가 image인 경우
                drawImage(msg.payloadString); //이미지 출력
        }

        if(msg.destinationName == "temparature") { //메시지가 temparatur인 경우
                document .getElementById ("temparature").innerHTML  = '<span>' + Math .round (msg .payloadString ) + '°C</span><br/>'; //측정한 값 전송
                if(msg .payloadString > 25) //측정한 값이 25를 초과하면
                        document .getElementById ("tempControl").innerHTML  = '<span>'+'에어컨  가동 요망!'+ '</span><br/>';
                else if(msg.payloadString < 20) //측정한 값이 20 미만이면
                        document .getElementById ("tempControl").innerHTML  = '<span>'+'히터 가동 요망!'+ '</span><br/>';
                else //그 외에는 적정 온도로 간주한다.
                        document.getElementById ("tempControl").innerHTML = '<span>'+'적정 온도 유지중...'+ '</span><br/>';


        }

        if(msg.destinationName == "humidity") { //메시지가 humidity인 경우
                document .getElementById ("humidity").innerHTML  = '<span>' + Math .round (msg .payloadString ) + '%</span><br/>'; //습도값 전송
        }

        if(msg.destinationName == "button") { //메시지가 button인 경우(버튼이 눌린 상황)
                alert("상황 발생!!"); //웹 페이지에 알림창 띄운다
        }
}

// disconnection 버튼이 선택되었을 때 호출되는 함수
function startDisconnect() {
        client.disconnect(); // 브로커에 접속 해제
        document.getElementById("messages").innerHTML += '<span>Disconnected</span><br/>'; //Disconnected 출력
}