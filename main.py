import sys
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import *

import shutil
import winsound as sd
import fsrcnn
import carDetection
import carDetection_video
import Use_Classification
import Recog_easyOCR

import os
import cv2
#UI파일 연결
#단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.

form_class = uic.loadUiType("test.ui")[0]

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class) :
    app = QApplication(sys.argv)
    app.addLibraryPath(os.path.abspath(".\plugins"))
    clicked = pyqtSignal()

    def __init__(self) :
        
        super().__init__()
        self.setupUi(self)


        #처리된 이미지들이 저장될 경로 생성
        root_path="d:\\carz_operated"
        #경로 없는 경우 생성
        if not os.path.exists(root_path):
            os.mkdir(root_path)
        
        #있는 경우 폴더 삭제 후 재생성(파일 꼬임 등을 방지하기 위해)
        else:
            shutil.rmtree(r"d:\\carz_operated")
            os.mkdir(root_path)
        
        self.ch = 0
        self.fsrcnn_img=""
        self.croped_img_path=""
        self.ocr_operated_text=""
        self.car_information=[]
        self.explain.setAlignment(Qt.AlignCenter)
        self.imageview2.setAlignment(Qt.AlignCenter)
        self.l6.setAlignment(Qt.AlignCenter)
        self.explain.setText("이미지 선택 방식을 결정해주세요.")
        self.btn_main.hide()

        #타이틀
        self.setWindowTitle("알려줘! 카즈")

        #메인 이미지 설정
        self.qPixmapVar = QPixmap()
        self.qPixmapVar.load("core_imgs\\carz.png")
        self.qPixmapVar = self.qPixmapVar.scaledToWidth(600)

        #메인 이미지 불러와서 적용
        self.imageview.setPixmap(self.qPixmapVar)

        #불필요한 내용 숨김
        self.progressBar.setValue(0)
        self.progressBar.hide()
        self.time_edit.hide()
        self.btn_edit.hide()
        self.label_anounce.hide()

        self.imageview2.hide()
        self.l1.hide()
        self.l2.hide()
        self.l3.hide()
        self.l4.hide()
        self.l5.hide()
        self.l6.hide()
        self.result_area.hide()
        
        #버튼 클릭 이벤트
        self.btn_upload.clicked.connect(self.loadImageFromFile)
        self.btn_ok.clicked.connect(self.doOperation)
        self.btn_edit.clicked.connect(self.video_time_edit)
        self.btn_video_capture.clicked.connect(self.live_operation)
        self.btn_main.clicked.connect(self.return_main)

    #업로드 버튼 클릭 시
    def loadImageFromFile(self):

        self.explain.setText("이미지를 다시 선택하거나, 해상도처리를 진행해주세요.")

        #파일탐색기 제목, 선택 확장자 명, 확장자
        filename = QtWidgets.QFileDialog.getOpenFileName(self,'영상 선택','','Image File(*.jpg *png);; Video File(*.avi *mp4)')

        #파일 이름, 확장자 분리
        fn,fe=os.path.splitext(filename[0])

        #해당 파일명 저장
        self.file_path = filename[0]

        #이미지 인 경우
        if fe[1:4] == 'png' or fe[1:4] == 'jpg':

            #해당 이미지를 메인화면으로 변경
            self.qPixmapVar.load(filename[0])
            self.qPixmapVar = self.qPixmapVar.scaledToWidth(600)
            self.imageview.setPixmap(self.qPixmapVar)

            #확인 버튼 처리용
            self.ch=1

        #영상의 경우
        elif fe[1:4] == 'mp4' or fe[1:4] == 'avi':
            #버튼 숨김
            self.btn_ok.hide()
            self.btn_video_capture.hide()

            #진행바 보이게 함
            self.progressBar.setVisible(True)

            #비디오 캡쳐
            vidcap = cv2.VideoCapture(filename[0])
            success,cutimage = vidcap.read()
            cnt = 1
            success=True

            #최초 로딩 이미지 설정
            self.qPixmapVar.load("core_imgs\\wait0.png")
            self.qPixmapVar = self.qPixmapVar.scaledToWidth(600)
            self.imageview.setPixmap(self.qPixmapVar)

            #분할이미지 저장경로 지정
            save_path="d:\\carz_operated\\cuted_img"

            #경로 없는 경우 생성
            if not os.path.exists(save_path):
                os.mkdir(save_path)
            
            #있는 경우 폴더 삭제 후 재생성(파일 꼬임 등을 방지하기 위해)
            else:
                shutil.rmtree(r"d:\\carz_operated\\cuted_img")
                os.mkdir(save_path)

            #20프레임 단위로 자름
            vidcount = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))//20

            #처리 중 업로드 방지를 위해 버튼 숨김
            self.btn_upload.hide()

            #끝날때 까지 반복
            while success:

                #이미지 캡쳐
                success,cutimage = vidcap.read()

                #캡쳐된 프레임이 20 단위인 경우
                if(int(vidcap.get(1))%20==0 and cutimage is not None):

                    #진행바 표시변경
                    self.progressBar.setValue((cnt/vidcount)*100)
                    
                    print(cnt,vidcap.get(1));
                    #분할 이미지 저장
                    cv2.imwrite(save_path+"\\%d.jpg" % cnt,cutimage)

                    #콘솔표시
                    print("saved image %d.jpg" % cnt)

                    #이미지 수 카운트
                    self.img_list_cnt = cnt
                    cnt+=1

                    #이미지 불러오기
                    self.qPixmapVar.load("core_imgs\\wait"+str(cnt%3)+".png")
                    self.qPixmapVar = self.qPixmapVar.scaledToWidth(600)
                    self.imageview.setPixmap(self.qPixmapVar)

                #종료조건 키입력
                if cv2.waitKey(10) == 27:
                    break
            
            #이미지 선택으로 넘어간다.
            self.img_list_select()

        #콘솔창에 선택된 이미지나 동영상의 이름 출력
        print(filename[0])

        #처리 후 버튼 텍스트 수정
        self.btn_ok.setText("UpScaling")

    #확인버튼 동작
    def doOperation(self):
        self.btn_edit.hide()
        self.time_edit.hide()
        self.label_anounce.hide()
        
        #아무 영상도 선택되지 않았을 경우 경고 메세지 출력
        if self.ch == 0:
            print("choose file")
            sd.PlaySound('SystemQuestion',sd.SND_ASYNC)
            buttonReply = QMessageBox.question(self, '경고!', "이미지가 선택되지 않았습니다!", QMessageBox.Yes)

        #ch==1일때 즉, 동영상에서 혹은 이미지 한장을 선택한경우
        elif self.ch==1:
            self.explain.setText("이미지를 다시 선택하거나, 번호판 인식을 진행해주세요.")
            self.btn_video_capture.setVisible(True)
            self.btn_ok.setText("Do LPD")
            #동영상의 경우 이미지 선택할 때 스크롤화면만 보이게 하기위해 숨겨둠
            #다시 활성화
            self.imageview.setVisible(True)
            """
            self.loding_img=QMovie('loding.gif',QByteArray(),self)
            self.loding_img.setCacheMode(QMovie.CacheAll)
            self.imageview.setMovie(self.loding_img)
            self.loding_img.start()
            """

            #다시 확인버튼시 오류방지, 다시누르면 경고창뜨게함
            self.ch=0

            #스크롤화면을 가리기위함
            try:
                self.scrollArea.hide()
            except AttributeError:
                print("")

            
            #SR모델 적용한 이미지 경로 받아오기
            
            self.fsrcnn_img = fsrcnn.sr_operate(self.file_path)

            #콘솔에 경로 출력
            print(self.fsrcnn_img)

            #처리된 이미지를 메인화면으로 띄워줌
            self.qPixmapVar.load(self.fsrcnn_img)
            self.qPixmapVar = self.qPixmapVar.scaledToWidth(600)
            self.imageview.setPixmap(self.qPixmapVar)

            #동영상처리 중 오류방지를 위해 숨겨둔 버튼 다시 활성화
            self.btn_upload.setVisible(True)

            #SR처리가 완료됨을 알림
            sd.PlaySound('SystemQuestion',sd.SND_ASYNC)
            buttonReply = QMessageBox.question(self, '안내', "Up Scaling 완료", QMessageBox.Yes)
            self.ch=2
        #SR처리 완료시
        elif self.ch==2:
            self.explain.setText("이미지를 다시 선택하거나, 번호인식처리를 진행해주세요.")
            self.btn_ok.setText("Do OCR")
            self.croped_img_path=carDetection.plate_detect(self.fsrcnn_img)
            #해당 이미지를 메인화면으로 변경
            self.qPixmapVar.load(self.croped_img_path)
            self.qPixmapVar = self.qPixmapVar.scaledToWidth(600)
            self.imageview.setPixmap(self.qPixmapVar)

            print(self.croped_img_path)

            

            self.ch=3
        #실시간 영상에서 자동차 번호판을 가져온 경우 DLP생략을 위해 별도 처리
        elif self.ch==4:
            self.explain.setText("이미지를 다시 선택하거나, 번호인식처리를 진행해주세요.")
            self.btn_ok.setText("Do OCR")

            #SR모델 적용한 이미지 경로 받아오기
            
            self.fsrcnn_img = fsrcnn.sr_operate(self.file_path)
            #콘솔에 경로 출력
            print(self.fsrcnn_img)
            self.croped_img_path=self.fsrcnn_img
            #처리된 이미지를 메인화면으로 띄워줌
            self.qPixmapVar.load(self.fsrcnn_img)
            self.qPixmapVar = self.qPixmapVar.scaledToWidth(600)
            self.imageview.setPixmap(self.qPixmapVar)

            #SR처리가 완료됨을 알림
            sd.PlaySound('SystemQuestion',sd.SND_ASYNC)
            buttonReply = QMessageBox.question(self, '안내', "Up Scaling 완료", QMessageBox.Yes)
            self.ch=3
        #sr이후 LPD까지 끝난 경우 OCR 처리
        elif self.ch==3:

            self.explain.setText("이미지를 다시 선택하거나, 분류처리를 진행해주세요.")
            self.btn_ok.setText("용도분류")
            self.ocr_operated_text=Recog_easyOCR.operate_OCR(self.croped_img_path)
            print(self.ocr_operated_text)

            #SR처리가 완료됨을 알림
            sd.PlaySound('SystemQuestion',sd.SND_ASYNC)
            buttonReply = QMessageBox.question(self, '안내', "OCR 완료", QMessageBox.Yes)

            self.ch=5
        elif self.ch==5:
            self.car_information=Use_Classification.use_classification(self.ocr_operated_text)
            print(self.car_information)
            self.view_information()


    #동영상에서 이미지 선택화면
    def img_list_select(self):
        self.explain.setText("이미지를 선택하거나, 영상의 범위를 정해주세요.")
        self.btn_ok.setVisible(True)
        #잘린 이미지들을 불러옴
        self.img_list = os.listdir("d:\\carz_operated\\cuted_img")

        #여기부터는 불필요한 작업일 수 있음
        self.FILE_LIST=[]
        png_list =[]
        self.PNG_LIST=[]

        #이미지들이 존재한다면 png_list에 파일명들을 저장
        if len(self.img_list) > 0:
            for file_name in self.img_list:
                if (file_name.find('.png') == len(file_name)-4) or (file_name.find('.jpg') == len(file_name)-4):
                    png_list.append(file_name)
        
        #저장된 파일명들이 존재하는 경우
        if len(png_list) > 0 :

            #각각의 이미지 경로로부터 이미지 오브젝트 생성
            for png_file in png_list:
                pixmap = QPixmap("d:\\carz_operated\\cuted_img"+'\\'+png_file)

                #해당 이미지 경로 저장
                png_path = "d:\\carz_operated\\cuted_img"+'\\'+png_file
                self.PNG_LIST.append(png_path)
        
        #해당 과정 중 불필요한 오브젝트들을 숨긴다
        self.imageview.hide()
        self.progressBar.hide()
        self.progressBar.setValue(0)
        
        #레이아웃생성, 스크롤 영역 설정, 스크롤영역에 추가될 오브젝트 생성,
        #생성된 오브젝트에 그리드 레이아웃 적용, 스크롤 영역에 오브젝트 추가, 최종 레이아웃에 스크롤영역 추가
        self.layout = QtWidgets.QHBoxLayout(self)
        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.resize(780,490)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        #self.layout.addWidget(self.scrollArea)


        #이미지 카운트용 변수
        index = 0

        #각 이미지 라벨 저장용 리스트
        self.label_list = []

        #한줄에 2개씩 배치하기 위한 반복문
        for i in range((self.img_list_cnt+1)//2):
            for j in range(2):
                
                #각각의 라벨 생성
                img_label = QLabel(self)

                #클릭 가능하게 하기 위한 함수
                self.clickable(img_label).connect(self.pictureListClicked)
                
                #라벨에 들어갈 이미지 오브젝트
                listpixmap = QPixmap()
                listpixmap.load(self.PNG_LIST[index])
                listpixmap=listpixmap.scaled(350,250)
                img_label.setPixmap(listpixmap)

                #그리드 레이아웃 해당 위치에 저장
                self.gridLayout.addWidget(img_label,i,j)

                #추후 접근을 위한 리스트에 저장
                self.label_list.append(img_label)
                
                index+=1

                #홀수일 때 out of range 방지를 위함
                if index == self.img_list_cnt:
                    break
        
        #설정된 스크롤 영역을 보이게 함
        self.scrollArea.setVisible(True)

        #동영상 부분 입력 활성화
        self.btn_edit.setVisible(True)
        self.time_edit.setVisible(True)
        self.time_edit.setPlaceholderText("MM:SS")
        self.label_anounce.setVisible(True)

        
        
    
    #이미지 클릭 가능하게 하는 함수
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
            
    #이미지를 각각 클릭 가능하게 하는 함수
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
            self.label_list[index].setStyleSheet("border-style: solid;" "border-width: 3px;""border-color: green")
            self.update()
            self.ch=1
            self.file_path=png_path

            self.time_edit.hide()
            self.btn_edit.hide()
            self.label_anounce.hide()

        
    def video_time_edit(self):
        self.explain.setText("이미지를 다시 선택하거나, 해상도처리를 진행해주세요.")
        self.scrollArea.hide()
        self.imageview.setVisible(True)
        self.btn_edit.hide()
        self.time_edit.hide()
        self.label_anounce.hide()

        time_str = self.time_edit.text()

        start_time_ms = int(time_str[:2])*60+int(time_str[3:])-500
        stop_time_ms = start_time_ms+1000
        vidcap = cv2.VideoCapture(self.file_path)

        count = 1
        success = True
        #분할이미지 저장경로 지정
        save_path="d:\\carz_operated\\cuted_img"

        #경로 없는 경우 생성
        if not os.path.exists(save_path):
            os.mkdir(save_path)
            
        #있는 경우 폴더 삭제 후 재생성(파일 꼬임 등을 방지하기 위해)
        else:
            shutil.rmtree(r"d:\\carz_operated\\cuted_img")
            os.mkdir(save_path)

        """
        #최초 로딩 이미지 설정
        self.qPixmapVar.load("wait0.png")
        self.qPixmapVar = self.qPixmapVar.scaledToWidth(600)
        self.imageview.setPixmap(self.qPixmapVar)
        """
        
        while success and vidcap.get(cv2.CAP_PROP_POS_MSEC) < start_time_ms:
            success, image = vidcap.read()

        #vidcount = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        while success and vidcap.get(cv2.CAP_PROP_POS_MSEC) <= stop_time_ms:
            #진행바 표시변경
            #self.progressBar.setValue((count/vidcount)*100)

            success, image = vidcap.read()
            print('Read a new frame: ', success)
            
            cv2.imwrite(save_path+"\%d.jpg" % count,image)
            self.img_list_cnt=count    
            count += 1

            #이미지 불러오기
            """print("core_imgs\\wait"+str(count%3)+".png")
            self.qPixmapVar.load("core_imgs\\wait"+str(count%3)+".png")
            self.qPixmapVar = self.qPixmapVar.scaledToWidth(600)
            self.imageview.setPixmap(self.qPixmapVar)"""

        #처리가 완료됨을 알림
        sd.PlaySound('SystemQuestion',sd.SND_ASYNC)
        buttonReply = QMessageBox.question(self, '안내', "지정 분할 완료", QMessageBox.Yes)
        self.img_list_select()

    def live_operation(self):
        self.explain.setText("이미지를 다시 선택하거나, 해상도처리를 진행해주세요.")
        self.btn_upload.hide()
        self.btn_ok.hide()
        self.btn_video_capture.hide()
        self.btn_ok.setText("UpScailing")
        

        self.file_path = carDetection_video.live_capture()
        #해당 이미지를 메인화면으로 변경
        self.qPixmapVar.load(self.file_path)
        self.qPixmapVar = self.qPixmapVar.scaledToWidth(600)
        self.imageview.setPixmap(self.qPixmapVar)

        #확인 버튼 처리용
        self.ch=4

        print("라이브 캡쳐"+self.file_path)

        self.btn_upload.setVisible(True)
        self.btn_ok.setVisible(True)
        self.btn_video_capture.setVisible(True)

    def view_information(self):
        self.explain.setText("")
        self.imageview2.setVisible(True)
        self.l1.setVisible(True)
        self.l2.setVisible(True)
        self.l3.setVisible(True)
        self.l4.setVisible(True)
        self.l5.setVisible(True)
        self.l6.setVisible(True)
        self.btn_main.setVisible(True)
        self.result_area.setVisible(True)
        self.result_area.setText(self.ocr_operated_text)

        #해당 이미지를 메인화면으로 변경
        self.qPixmapVar.load(self.croped_img_path)
        self.qPixmapVar = self.qPixmapVar.scaledToWidth(230)
        self.imageview2.setPixmap(self.qPixmapVar)

        self.imageview.hide()
        self.btn_ok.hide()
        self.btn_upload.hide()
        self.btn_video_capture.hide()
        
        
        self.l6.setText("특이사항 : "+self.car_information.pop())
        self.l5.setText("차량번호 : "+self.car_information.pop())
        self.l4.setText("용도 : "+self.car_information.pop())
        self.l3.setText("차종 : "+self.car_information.pop())
        self.l2.setText("관할지 : "+self.car_information.pop())
        self.l1.setText("지역 : "+self.car_information.pop())

        
        
    def return_main(self):
        self.imageview2.hide()
        self.l1.hide()
        self.l2.hide()
        self.l3.hide()
        self.l4.hide()
        self.l5.hide()
        self.l6.hide()
        self.btn_main.hide()
        self.result_area.hide()
        self.result_area.setText("")

        #메인 이미지 설정
        self.imageview.setVisible(True)
        self.qPixmapVar = QPixmap()
        self.qPixmapVar.load("core_imgs\\carz.png")
        self.qPixmapVar = self.qPixmapVar.scaledToWidth(600)
        #메인 이미지 불러와서 적용
        self.imageview.setPixmap(self.qPixmapVar)
        
        self.btn_ok.setVisible(True)
        self.btn_upload.setVisible(True)
        self.btn_video_capture.setVisible(True)
        
        self.btn_ok.setText("확인")
        self.explain.setText("이미지 선택 방식을 결정해주세요.")
        self.ch=0

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()