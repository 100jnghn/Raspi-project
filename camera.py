import os
import io
import time
import cv2
from PIL import Image, ImageFilter
import numpy as np

# 전역 변수 선언 및 초기화
fileName = ""
stream = io.BytesIO()
haar = cv2.CascadeClassifier('./haarCascades/haar-cascade-\
files-master/haarcascade_frontalface_default.xml')

camera = cv2.VideoCapture(0, cv2.CAP_V4L) # 0번 카메라
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
camera.set(cv2.CAP_PROP_BUFFERSIZE, 1) # 버퍼크기는 1~10까지 유효함
buffersize = camera.get(cv2.CAP_PROP_BUFFERSIZE)
print("버퍼 개수는 %d " % buffersize)

#사진 촬영 함수
def takePicture() :
        global fileName
        global stream
        global camera
        global buffersize

        # 이전에 만들어둔 사진 파일이 있으면 삭제
        if len(fileName) != 0:
                os.unlink(fileName)

        stream.seek(0) # 파일 포인터를 스트림 맨 앞으로 위치시킴. 이곳에서부터 >이미지 데이터 저장
        stream.truncate()
        # cv2의 버퍼에 저장된 프레임 제거하고 최신 프레임을 읽기 위한 코드
        for i in range(int(buffersize)+1):
                ret, frame = camera.read() # 프레임 읽기

        if not(ret):    # 프레임정보를 정상적으로 읽지 못하면
                print("사진 촬영 실패")

        pilim = Image.fromarray(frame)
        pilim.save(stream, 'jpeg') # 프레임을 jpeg 형태로 바꾸기
        data = np.frombuffer(stream.getvalue(), dtype=np.uint8) # stream에 저장된 프레임을 unit8로
        image = cv2.imdecode(data, 1)
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = haar.detectMultiScale(image_gray,1.1,3) # 얼굴 인식후 얼굴 부위 사각형 정보 리턴

        for x, y, w, h in faces:
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2) # 프레임에 사각형 그리기

        takeTime = time.time() # 현재 시간 알아내기
        fileName = "./static/%d.jpg" % (takeTime * 10) # 현재 시간으로 파일 이름 생성
        cv2.imwrite(fileName, image) # 사각형이 그려진 프레임 이미지를 파일에 저장
        return fileName

if __name__ == '__main__' :
        takePicture()

if __name__ == 'myCamera' :
        pass
