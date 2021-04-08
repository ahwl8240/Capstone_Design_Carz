import sys
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import *

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
    clicked = pyqtSignal()

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

            vidcount = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))//20
            self.btn_upload.hide()
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
            self.img_list_select()
        print(filename[0])
        
    def doOperation(self):
        
        if self.ch == 0:
            print("choose file")
            sd.PlaySound('SystemQuestion',sd.SND_ASYNC)
            buttonReply = QMessageBox.question(self, '경고!', "이미지가 선택되지 않았습니다!", QMessageBox.Yes)
        else:
            self.imageview.setVisible(True)
            """
            self.loding_img=QMovie('loding.gif',QByteArray(),self)
            self.loding_img.setCacheMode(QMovie.CacheAll)
            self.imageview.setMovie(self.loding_img)
            self.loding_img.start()
            """

            self.ch=0
            self.scrollArea.hide()
            
            

            fsrcnn_img = fsrcnn.sr_operate(self.file_path)
            print(fsrcnn_img)

            self.qPixmapVar.load(fsrcnn_img)
            self.qPixmapVar = self.qPixmapVar.scaledToWidth(600)
            self.imageview.setPixmap(self.qPixmapVar)
            self.btn_upload.setVisible(True)

            sd.PlaySound('SystemQuestion',sd.SND_ASYNC)
            buttonReply = QMessageBox.question(self, '안내', "Up Scaling 완료", QMessageBox.Yes)

    
    def img_list_select(self):
        self.img_list = os.listdir("d:\cuted_img")
        self.FILE_LIST=[]
        png_list =[]
        self.PNG_LIST=[]
        if len(self.img_list) > 0:
            for file_name in self.img_list:
                if (file_name.find('.png') == len(file_name)-4) or (file_name.find('.jpg') == len(file_name)-4):
                    png_list.append(file_name)
            
        if len(png_list) > 0 :
            for png_file in png_list:
                pixmap = QPixmap("d:\cuted_img"+'\\'+png_file)

                png_path = "d:\cuted_img"+'\\'+png_file
                self.PNG_LIST.append(png_path)
        
        self.imageview.hide()
        self.progressBar.hide()
        self.progressBar.setValue(0)
        
        self.layout = QtWidgets.QHBoxLayout(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.layout.addWidget(self.scrollArea)



        index = 0
        
        self.label_list = []
        for i in range((self.img_list_cnt+1)//2):
            for j in range(2):
                
                img_label = QLabel(self)
                self.clickable(img_label).connect(self.pictureListClicked)
                
                listpixmap = QPixmap()
                listpixmap.load(self.PNG_LIST[index])
                listpixmap=listpixmap.scaled(350,250)
                img_label.setPixmap(listpixmap)
                self.gridLayout.addWidget(img_label,i,j)
                self.label_list.append(img_label)
                
                index+=1
        
        self.scrollArea.setVisible(True)
    

    def clickable(self,widget):
        class Filter(QObject):
            clicked = pyqtSignal()

            def eventFilter(self, obj, event):
                if obj == widget:
                    if event.type() == QEvent.MouseButtonRelease:
                        if obj.rect().contains(event.pos()):
                            self.clicked.emit()
                            return True

                return False
        filter = Filter(widget)
        widget.installEventFilter(filter)
        self.FILE_LIST.append(filter)
        return filter.clicked
            
    
    def pictureListClicked(self):
        png_path = ''
        for i, object_name in enumerate(self.FILE_LIST):
            if object_name == self.sender():
                index = i
                selected_img = object_name
                png_path = self.PNG_LIST[i]
                break;

        if png_path != '':
            print(png_path)
            for i in range(len(self.label_list)):
                self.label_list[i].setStyleSheet("")
            self.label_list[index].setStyleSheet("color: red;" "border-style: solid;" "border-width: 2px;""border-color: #FA8072;" "border-radius: 3px")
            self.update()
            self.ch=1
            self.file_path=png_path
        



if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()