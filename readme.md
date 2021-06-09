<h1>사용시 요구사항</h1>
<p>LPD 기능에 필요한 weight 파일을 별도로 다운로드해야 합니다.
이 파일을 main.py가 있는 위치에 두시고, pyinstaller 사용시(spec 설정 사용시) files 폴더에도 복사해주세요.</p>
<p>https://drive.google.com/file/d/1_kvRWrSQZzQK5P4918mBC4Rzeb_RD_Tl/view?usp=sharing</p>

<p>이하의 프로그램 및 라이브러리 설치가 필요합니다.</p>

<p>ocr 진행시 gpu를 사용할시 더 빠르며, 꼭 설치하지 않아도 cpu를 사용하여 진행할 수 있습니다. 단 gpu를 사용할 경우 동작이 훨씬 빠르며, 설치후 코드 수정 필요 합니다.</p>
<p>CUDA 11.0</p>
<p>cuDNN 8.0</p>

<p>실시간 영상을 처리하는 경우 opencv를 통해 처리하므로 opencv가 인식하는 카메라를 연결해야 합니다. 예시에는 PC와 스마트폰에 DroidCam을 설치하였습니다.</p>

~~~
reader = easyocr.Reader(['ko']) #gpu 모드(cuda 사용)
#reader = easyocr.Reader(['ko'], gpu=False) #cpu모드
~~~


<p>라이브러리 목록</p>
<p>Package                   Version</p>
<p>------------------------- ------------</p>

<p>easyocr                   1.3.2</p>


<p></p>
<p>matplotlib                3.3.4</p>
<p></p>

<p>numpy                     1.19.5</p>
<p></p>
<p>opencv-contrib-python     4.5.2.52</p>
<p>opencv-python             4.5.2.52</p>
<p></p>
<p>pip                       21.1.2</p>
<p></p>
<p>pyinstaller               5.0.dev0</p>
<p>pyinstaller-hooks-contrib 2021.1</p>
<p></p>
<p>PyQt5                     5.15.2</p>

<br/>
<br/>

<h2>사용방법</h2>
<p>main.py를 실행합니다.</p>

![image](https://user-images.githubusercontent.com/65153512/121291236-e308ae00-c922-11eb-99a0-5e5dd50ceace.png)

<p>메인화면에서 업로드 버튼이나 비디오 캡처를 눌러 이미지나 동영상을 선택합니다.</p>

<p>업로드 버튼을 선택한 경우 동영상과 이미지를 선택할 수 있으며, 동영상의 예시만 설명하겠습니다.</p>

<p>진행 중 업로드와 비디오 캡쳐 버튼이 활성화되있다면 언제든지 영상을 교체할 수 있습니다. 단 처음 과정부터 되돌아가 진행하게 됩니다.</p>

![image](https://user-images.githubusercontent.com/65153512/121291617-88238680-c923-11eb-8c5c-037889c713c4.png)

<p>파일탐색기에서 원하는 동영상을 선택하면 자동으로 지정된 프레임 만큼 잘라 이미지를 저장하게 됩니다.</p>

![image](https://user-images.githubusercontent.com/65153512/121291676-a093a100-c923-11eb-8edb-e30cfc029a22.png)

<p>이때 분할된 이미지 중 원하는 것을 선택하거나 하단의 창에 mm:ss 로 원하는 지점을 입력하여 그 시점을 기준으로 분할된 사진을 선택할 수 있습니다.</p>

![image](https://user-images.githubusercontent.com/65153512/121291769-cd47b880-c923-11eb-9653-4aea24bcb23a.png)

<p>이미지 선택후 upscaling 버튼을 눌러 SR처리를 진행합니다. 이미지의 경우 선택된 이미지가 메인 이미지로 변경된 후 마찬가지로 버튼을 눌러 SR처리를 하게 됩니다. 동영상과 이미지 선택 후 SR처리가 끝나면 처리된 이미지로 메인 이미지가 변경됩니다.</p>

![image](https://user-images.githubusercontent.com/65153512/121291924-06802880-c924-11eb-9513-6264260f1fd0.png)

<p>Do LPD버튼을 누르게되면 해당 이미지에서 번호판의 위치를 찾아 잘라내어 메인 이미지로 교체됩니다. 이후 Do OCR을 진행하면 해당 번호판으로부터 글자를 추출하게 됩니다.</p>

![image](https://user-images.githubusercontent.com/65153512/121292085-55c65900-c924-11eb-96bc-382d57370ec7.png)

<p>용도 조회버튼을 누르면 추출된 글자를 기반으로 해당 차량에 대한 정보를 나타냅니다. 예시에서는 더 다양한 정보가 포함된 번호판으로 이미지를 바꿔 진행했습니다.</p>

![image](https://user-images.githubusercontent.com/65153512/121292148-72fb2780-c924-11eb-95a1-197e1108b721.png)

<br/>
<br/>

<p>실시간 캡쳐를 눌렀을 경우입니다.</p>

![image](https://user-images.githubusercontent.com/65153512/121292777-75aa4c80-c925-11eb-99e0-f2f9d2e5bb62.png)

<p>카메라를 통해 번호판을 인식하게 되는 경우 다음과 같이 번호판인식과 동시에 LPD가 이루어지고, 번호판 부분만 저장하게 됩니다. 본 코드에서는 사진 흔들림의 방지를 위해 처음 인식된 후 일정시간 후의 번호판을 이용하도록 하였습니다.</p>

![image](https://user-images.githubusercontent.com/65153512/121293028-e6e9ff80-c925-11eb-9ae8-1afd1cfddb06.png)

<p>앞의과정과 마찬가지로 SR 과 OCR 과정을 거치고 용도분류를 하게되면 다음과 같은 결과를 얻게 됩니다.</p>

![image](https://user-images.githubusercontent.com/65153512/121293210-33cdd600-c926-11eb-99b2-6c8b7e75dae3.png)

<br/>
<br/>
<br/>

<p>spec 파일을 통해 exe 화 하는 경우, pyinstaller를 설치하고, pyinstaller --onedir main.spec 을 입력후 생성된 dist 폴더의 main.exe 파일을 실행하시면 됩니다.</p>