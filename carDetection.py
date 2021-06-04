import cv2
import os
import numpy as np
def plate_detect(img_path):
    #기본 정보 읽어오기, 세팅

    #분할이미지 저장경로 지정
    save_path="d:\\carz_operated\\cuted_img"
    #경로 없는 경우 생성
    if not os.path.exists(save_path):
        os.mkdir(save_path)
        
    print(img_path)
    net = cv2.dnn.readNet("custom_final2.weights","custom.cfg")
    classes = []
    with open("custom.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]

    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0]-1]for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    #세팅 끝
    #input_name = input()        
    img = cv2.imread(img_path) #매개변수로 입력받은 파일경로 입력

    #img = cv2.resize(img, None, fx=0.4, fy=0.4)

    height, width, channels = img.shape                         #입력받은 이미지의 높이 너비 읽어오기

    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False) #입력받은 이미지 yolo연산을 위해 크기 조정
    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids=[]
    confidences=[]
    boxes=[]

    for out in outs:                    #outs = 감지된 모든 개체에 대한 정보
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:
                center_x = int(detection[0]*width)  #찾은 객체의 가운데 x 좌표
                center_y = int(detection[1]*height) #찾은 객체의 가운데 y 좌표
                w = int(detection[2]*width)         #찾은 객체의 너비
                h = int(detection[3]*height)        #찾은 객체의 높이

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])          #표시할 박스의 x,y좌표와 높이 너비 boxes에 저장
                confidences.append(float(confidence))   #각각 박스의 정확도를 confidences에 저장
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)    #노이즈 제거
    crop_img = []
    cnt = 0
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]                   #박스의 x,y좌표 너비 높이 불러오기
            #label = str(classes[class_ids[i]])     #탐지한 물체의 class 이름 label에 저장
            crop_img.append(img[y+1:y+h, x+1: x+w]) #표시된 부분만 잘라내기
            #crop_img[cnt] = cv2.resize(crop_img[cnt], (height, width))  
            cnt += 1                                #찾은 번호판의 갯수
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255),1)  #번호판에 사각형 표시
            #cv2.putText(img, label, (x, y-2), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255), 1)

    #cv2.imshow("Image", crop_img)
    #cv2.imwrite("d:\\cuted_img\\" + input_name + "_detection.jpg",img)    #result폴더에 원본사진이름_detection으로 저장

    #찾아낸 번호판들의 위치를 저장할 리스트
    img_list=[]

    croped_img_path=""
    for i in range(cnt):
            croped_img_path="d:\\carz_operated\\cuted_img\\" + "detection_crop" + str(i) + ".jpg"
            cv2.imwrite(croped_img_path,crop_img[i]) #번호판 부분만 result폴더에 원본사진_detuction+ 0,1,2...으로 저장
            img_list.append(croped_img_path)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return croped_img_path