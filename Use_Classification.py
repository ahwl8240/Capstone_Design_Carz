def use_classification(carplate):
    car_plate = carplate
    car_model = []
    plate_kor = []
    car_code=""
    result_purpose=""
    result_car=""
    special_note=""
    local=""
    local_sub=""

    #숫자와 한글 분리
    for k in car_plate:
        if '가'<=k<='힣':
            plate_kor.append(k)
        elif '0'<=k<='9':
            car_model.append(k)

    #한글 분류----------------------------------

    #구식(지역 포함) 번호판의 경우
    if(len(plate_kor)>1):
        #지역정보 포함 분류
        local=plate_kor.pop(0)+plate_kor.pop(0)

    #오토바이의 경우
    if(len(plate_kor)>1):
        special_note="오토바이 입니다."
        result_car="오토바이"
        while(len(plate_kor)>1):
            local_sub+=plate_kor.pop(0)

    use_purpose=plate_kor[0]
    if('아'==use_purpose or '바'==use_purpose or '사'==use_purpose or '자'==use_purpose):
        result_purpose="사업용"
    elif('배'==use_purpose):
        result_purpose="사업용-택배차량"
    elif('하'==use_purpose or '허'==use_purpose or '호'==use_purpose):
        result_purpose="사업용-렌트차량"
    elif('육'==use_purpose):
        result_purpose="육군 차량"
        special_note="군용 차량입니다."
    elif('합'==use_purpose):
        result_purpose="합동참모본부 차량"
        special_note="군용 차량입니다."
    elif('국'==use_purpose):
        result_purpose="국방부 차량"
        special_note="군용 차량입니다."
    elif('해'==use_purpose):
        result_purpose="해군 차량"
        special_note="군용 차량입니다."
    elif('공'==use_purpose):
        result_purpose="공군 차량"
        special_note="군용 차량입니다."
    elif('가'<=use_purpose<='마' or '거'<=use_purpose<='저' or '고'<=use_purpose<='조' or '구'<=use_purpose<='주'):
        result_purpose="비상업용/일반차량"

    #숫자 분류----------------------------------
    #구식의 경우
    #구분번호가 2자리
    if(len(car_model)==6):
        use_num=car_model.pop(0)+car_model.pop(0)
        if('01'<=use_num<='69'):
            result_car="승용차"
        elif('70'<=use_num<='79'):
            result_car="승합차"
        elif('80'<=use_num<='97'):
            result_car="화물차"
        elif('98'<=use_num<='99'):
            result_car="특수차"
    #구분번호가 3자리
    elif(len(car_model)==7):
        use_num=car_model.pop(0)+car_model.pop(0)+car_model.pop(0)
        if('100'<=use_num<='699'):
            result_car="승용차"
        elif('700'<=use_num<='799'):
            result_car="승합차"
        elif('800'<=use_num<='979'):
            result_car="화물차"
        elif('980'<=use_num<='997'):
            result_car="특수차"
        elif('998'<=use_num<='999'):
            result_car="긴급자동차"
            special_note="소방차, 구급차 등의 긴급 차량 입니다."
    car_code=car_model.pop(0)+car_model.pop(0)+car_model.pop(0)+car_model.pop(0)

    if(len(local)!=0):
        print("지역: "+local)
    if(len(local_sub)!=0):
        print("관할지: "+local_sub)
    print("차종: "+result_car)
    print("용도: "+result_purpose)
    print("번호: "+car_code)
    print("특이사항: "+special_note)

    result_list=[local,local_sub,result_car,result_purpose,car_code,special_note]
    return result_list