# 1. 라이브러리 호출
# OMP 에러 처리용 2줄
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
import cv2
import easyocr
reader = easyocr.Reader(['ko'])

# 인식한 문자열 처리 함수
def process(chars):
    result = ''
    plate = []
    i = 0
    last = -1

    for x, y, z in chars:
        result_chars = ''
        num_digit = 0
        for c in y:
            if ord('가') <= ord(c) <= ord('힣') or c.isdigit():
                if c.isdigit():
                    num_digit += 1
                if c == '율' or c == '움':
                    result_chars += '울'
                    continue
                result_chars += c
        if num_digit >= 4:
            last = i
        if len(result_chars)>0:
            plate.append(result_chars)
            i += 1

    for i, s in enumerate(plate):
        if i != last:
            result += s
    if last != -1:
        result += plate[last]
    result = result.replace(" ", "")
    return result


# 전처리 전, 후 중 더 쓸만한 번호 인식
def lastselect(before, after):
    charset = ['외', '교', '영', '사', '준', '국', '기', '합', '육', '해', '공',
               '강', '원', '경', '기', '남', '북', '광', '주', '대', '구', '전',
               '산', '서', '울', '세', '종', '인', '천', '전', '제', '주', '충',
               '가', '나', '다', '라', '마',
               '거', '너', '더', '러', '머', '버', '서', '어', '저',
               '고', '노', '도', '로', '모', '보', '소', '오', '조',
               '구', '누', '두', '루', '무', '부', '수', '우', '주',
               '하', '허', '호', '배']
    a = len(after)
    b = len(before)
    score_a = 0
    score_b = 0

    if before == after:
        return before

    if b == 0:
        if a == 0:
            return None
        return after
    if a == 0:
        return before

    if 7 <= a <= 9:
        score_a += 1
    if 7 <= b <= 9:
        score_b += 1

    if after[-1].isdigit():
        score_a += 1
    if before[-1].isdigit():
        score_b += 1

    for c in after:
        if not c.isdigit():
            if c in charset:
                score_a += 1
            else:
                score_a -= 1

    for c in before:
        if not c.isdigit():
            if c in charset:
                score_b += 1
            else:
                score_b -= 1

    if score_a > score_b:
        return after

    return before



# 2. Read Input Image
def operate_OCR(img_path):
    img_ori = cv2.imread(img_path)

    chars = reader.readtext(img_ori)
    before = process(chars)
    #print('----전처리 전----')
    #print(before)

    # 3. Convert Image to Grayscale
    gray = cv2.cvtColor(img_ori, cv2.COLOR_BGR2GRAY)

    # 4. Adaptive Thresholding
    img_blurred = cv2.GaussianBlur(gray, ksize=(1, 1), sigmaX=0)

    img_blur_thresh = cv2.adaptiveThreshold(
        img_blurred,
        maxValue=255.0,
        adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        thresholdType=cv2.THRESH_BINARY_INV,
        blockSize=19,
        C=9
    )

    img_result = cv2.resize(img_blur_thresh, dsize=(0, 0), fx=1.6, fy=1.6)
    _, img_result = cv2.threshold(img_result, thresh=0.0, maxval=255.0, type=cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    img_result = cv2.copyMakeBorder(img_result, top=10, bottom=10, left=10, right=10, borderType=cv2.BORDER_CONSTANT,
                                    value=(0, 0, 0))

    chars = reader.readtext(img_result)
    after = process(chars)
    #print('----전처리 후----')
    #print(after)

    # 인식된 번호 선택 후 출력
    lastplate = lastselect(before, after)
    #print('----선택된 번호----')

    return lastplate

    """
    if lastplate is None:
        print('번호를 인식하지 못했습니다.')
    else :
        print(lastplate)
    """

