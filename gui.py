import sys
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
import math
import winsound as sd
import fsrcnn

import os
import cv2
#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.

form_class = uic.loadUiType("test.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    app = QApplication(sys.argv)
    app.addLibraryPath("./plugins")
    
    def __init__(self) :
        
        super().__init__()
        self.setupUi(self)
        
        self.ch = 0

        self.setWindowTitle("알려줘! 카즈")
        self.qPixmapVar = QPixmap()
        self.qPixmapVar.load("carz.png")
        self.qPixmapVar = self.qPixmapVar.scaledToWidth(600)

        self.imageview.setPixmap(self.qPixmapVar)

        self.progressBar.setValue(0)
        self.progressBar.hide()

        self.scrollArea.hide()

        self.btn_upload.clicked.connect(self.loadImageFromFile)
        self.btn_ok.clicked.connect(self.doOperation)

    def loadImageFromFile(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self,'Open File','','Image File(*.jpg *png);; Video File(*.avi *mp4)')
        fn,fe=os.path.splitext(filename[0])
        if fe[1:4] == 'png' or fe[1:4] == 'jpg':
            self.qPixmapVar.load(filename[0])
            self.qPixmapVar = self.qPixmapVar.scaledToWidth(600)
            self.imageview.setPixmap(self.qPixmapVar)
            self.file_path = filename[0]
            self.ch=1
        elif fe[1:4] == 'mp4' or fe[1:4] == 'avi':
            self.progressBar.setVisible(True)
            vidcap = cv2.VideoCapture(filename[0])
            success,cutimage = vidcap.read()
            cnt = 1
            success=True
            self.qPixmapVar.load("wait0.png")
            self.qPixmapVar = self.qPixmapVar.scaledToWidth(600)
            self.imageview.setPixmap(self.qPixmapVar)
            save_path="d:\cuted_img"
            if not os.path.exists(save_path):
                os.mkdir(save_path)
        
            """self.loding_img=QMovie('loding.gif',QByteArray(),self)
            self.loding_img.setCacheMode(QMovie.CacheAll)
            self.imageview.setMovie(self.loding_img)
            self.loding_img.start()"""


            vidcount = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))//20
            while success:
                success,cutimage = vidcap.read()
                if(int(vidcap.get(1))%20==0):
                    self.progressBar.setValue((cnt/vidcount)*100)
                    
                    cv2.imwrite(save_path+"\%d.jpg" % cnt,cutimage)
                    print("saved image %d.jpg" % cnt)
                    self.img_list_cnt = cnt
                    cnt+=1
                    self.qPixmapVar.load("wait"+str(cnt%3)+".png")
                    self.qPixmapVar = self.qPixmapVar.scaledToWidth(600)
                    self.imageview.setPixmap(self.qPixmapVar)
                if cv2.waitKey(10) == 27:
                    break
            self.ch=1
            self.img_list_select()
        print(filename[0])
        
    def doOperation(self):
        if self.ch == 0:
            print("choose file")
            sd.PlaySound('SystemQuestion',sd.SND_ASYNC)
            buttonReply = QMessageBox.question(self, '경고!', "이미지가 선택되지 않았습니다!", QMessageBox.Yes)
        else:
            operated = fsrcnn.sr_operate(self.file_path)
            print(operated)
    def img_list_select(self):
        img_list = os.listdir("d:\cuted_img")
        png_list =[]
        PNG_LIST=[]
        if len(img_list) > 0:
            for file_name in img_list:
                if (file_name.find('.png') == len(file_name)-4) or (file_name.find('.jpg') == len(file_name)-4):
                    png_list.append(file_name)
            
        if len(png_list) > 0 :
            for png_file in png_list:
                pixmap = QPixmap("d:\cuted_img"+'\\'+png_file)

                png_path = "d:\cuted_img"+'\\'+png_file
                PNG_LIST.append(png_path)
        
        self.imageview.hide()
        self.progressBar.hide()
        self.progressBar.setValue(0)
        
        #self.scrollArea.setWidgetResizable(True)

        for i in range(self.img_list_cnt):
            for j in range(2):
                img_label = QLabel('imglabel'+str(i+1),self)

                listpixmap = QPixmap()
                listpixmap.load(PNG_LIST[i])
                listpixmap=listpixmap.scaledToWidth(400)
                img_label.setPixmap(listpixmap)
                self.gridLayout.addWidget(img_label,i//2,j)
                
                
                #self.qPixmapVar = QPixmap()
                #self.qPixmapVar.load("carz.png")
                #self.qPixmapVar = self.qPixmapVar.scaledToWidth(600)
                #self.imageview.setPixmap(self.qPixmapVar)
        self.scrollArea.setVisible(True)
        
        
            

        



if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()