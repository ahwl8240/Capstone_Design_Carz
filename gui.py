import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
import os
import cv2
#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("test.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.qPixmapVar = QPixmap()
        self.qPixmapVar.load("carz.png")
        self.qPixmapVar = self.qPixmapVar.scaledToWidth(600)
        self.imageview.setPixmap(self.qPixmapVar)
        
        self.btn_upload.clicked.connect(self.loadImageFromFile)

    def loadImageFromFile(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self,'Open File')
        fn,fe=os.path.splitext(filename[0])
        if fe[1:4] == 'png' or fe[1:4] == 'jpg':
            self.qPixmapVar.load(filename[0])
            self.qPixmapVar = self.qPixmapVar.scaledToWidth(600)
            self.imageview.setPixmap(self.qPixmapVar)
        elif fe[1:4] == 'mp4' or fe[1:4] == 'avi':
            vidcap = cv2.VideoCapture(filename[0])
            success,cutimage = vidcap.read()
            cnt = 1
            success=True
            while success:
                success,cutimage = vidcap.read()
                if(int(vidcap.get(1))%20==0):
                    cv2.imwrite("D:\cuted_image\%d.jpg" % cnt,cutimage)
                    print("saved image %d.jpg" % cnt)
                    cnt+=1
                if cv2.waitKey(10) == 5:
                    break
                
        print(filename[0])

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()