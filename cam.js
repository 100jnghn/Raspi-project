//웹 페이지에서 버튼을 누르면 이미지 전송

var canvas;
var context;
var img;
//load 이벤트 리스터 등록. 웹페이지가 로딩된 후 실행
window.addEventListener("load", function() {
        canvas = document.getElementById("myCanvas"); //이미지를 출력할 캔버스 id
        context = canvas.getContext("2d");

        img = new Image();
        img.onload = function() {
                context.drawImage(img,
                0,
                0,
                canvas.width, canvas.height);
        }
});

//drawImage()는 'image' 토픽 도착 시 onMessageArrived()에 의해 호출
function drawImage(imgUrl) { //imgUrl은 이미지의 url
        img.src = imgUrl; //img.onload에 등록된 코드에 의해 그려짐
}

var isImageSubscribed = false;

function recognize() {
        var canvas = document.getElementById('myCanvas');
        if(canvas.style.display=="none")
                canvas.style.display="block"
        else
                canvas.style.display="none"

        subscribe('image'); //토픽 image 등록
}