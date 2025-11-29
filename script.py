import os
import random
import torch
from transformers import pipeline
# 다국어 모델
# 전역 변수
emotion_classifier = None

def output_modifier(string, state):
    global emotion_classifier
    
    if not string:
        return string

    # 1. 로컬 모델 로딩 (
    if emotion_classifier is None:
        try:
    
            base_path = os.path.dirname(__file__)
            local_model_path = os.path.join(base_path, "model")
            
            # 모델 폴더 확인
            if not os.path.exists(local_model_path):
                print(f"[Error] 'model' 폴더가 없습니다. 경로: {local_model_path}")
                return string

            # 로컬 경로에서 모델 로딩
 
            emotion_classifier = pipeline(
                "text-classification", 
                model=local_model_path, 
                device=-1 
            )
            print("[Info] 로컬 모델 로딩 성공!")
            
        except Exception as e:
            print(f"[Error] 모델 로딩 실패: {e}")
            return string

    try:

        # 2. 텍스트 분석
        # 긴 문장은 자르고, 최대 길이는 512토큰
        results = emotion_classifier(string, truncation=True, max_length=512)
        raw_label = results[0]['label'] 
        
     
        # 3. 키워드 설정 
        keywords_fear = ['무서', '공포', '겁', '소름', '불안', '두려', '오싹', '섬뜩', '비명', '도망', '살려']
        keywords_disgust = ['구역질', '토', '우웩', '역겨', '극혐', '더러', '비위', '냄새', '썩', '징그', '오물']
        keywords_sadness = ['슬퍼', '눈물', '울', '우울', '흑흑', 'ㅠㅠ', '실망', '비참', '좌절', '괴로', '후회', '상처']
        keywords_anger = ['짜증', '화나', '미친', '닥쳐', '죽', '열받', '멍청', '놈', '꺼져', '분노', '씨', '발', '재수']
        
        keywords_surprise = ['놀라', '깜짝', '헉', '대박', '맙소사', '충격', '헐', '세상에', '믿을 수', '?!']
        keywords_joy = ['흥분', '신나', '기분 좋', '행복', '최고', '사랑', '기뻐', '웃', '하하', 'ㅋㅋ', '굿', '감동', '환상']

        final_emotion = "neutral" 
        match_reason = "기본값"


        # 4. 감정 매칭 로직
        # 부정(Negative) -> LABEL_0
        if raw_label == 'LABEL_0' or raw_label == 'negative':
            if any(word in string for word in keywords_disgust):
                final_emotion = "disgust"
                match_reason = "부정 + 키워드(혐오)"
            elif any(word in string for word in keywords_fear):
                final_emotion = "fear"
                match_reason = "부정 + 키워드(공포)"
            elif any(word in string for word in keywords_sadness):
                final_emotion = "sadness"
                match_reason = "부정 + 키워드(슬픔)"
            elif any(word in string for word in keywords_anger):
                final_emotion = "anger"
                match_reason = "부정 + 키워드(분노)"
            else:
                final_emotion = "anger"
                match_reason = "부정(키워드 없음) -> 분노"

        # 긍정(Positive) -> LABEL_2
        elif raw_label == 'LABEL_2' or raw_label == 'positive':
            if any(word in string for word in keywords_surprise):
                final_emotion = "surprise"
                match_reason = "긍정 + 키워드(놀람)"
            elif any(word in string for word in keywords_joy):
                final_emotion = "joy"
                match_reason = "긍정 + 키워드(기쁨)"
            else:
                final_emotion = "joy"
                match_reason = "긍정(키워드 없음) -> 기쁨"

        # 중립(Neutral) -> LABEL_1
        else: 
            if any(word in string for word in keywords_disgust): final_emotion = "disgust"
            elif any(word in string for word in keywords_joy): final_emotion = "joy"
            elif any(word in string for word in keywords_anger): final_emotion = "anger"
            elif any(word in string for word in keywords_sadness): final_emotion = "sadness"
            elif any(word in string for word in keywords_surprise): final_emotion = "surprise"
            else:
                final_emotion = "neutral"
                match_reason = "중립 판단"


        # 5. 이미지 출력

        print(f"입력: {string[:30]}...")
        print(f"분석: {raw_label} -> 매칭: {final_emotion} (사유: {match_reason})")
        
        base_path = os.path.dirname(__file__)
        image_folder = os.path.join(base_path, "images", final_emotion)
        
        image_url = None
        
        # 해당 감정 폴더가 실제로 있는지 확인
        if os.path.exists(image_folder):
            valid_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.webp')
            files = [f for f in os.listdir(image_folder) if f.lower().endswith(valid_extensions)]
            
            if files:
                selected = random.choice(files)
                
                image_url = f"file/extensions/emotion_images/images/{final_emotion}/{selected}"
        
        # 이미지가 있으면 HTML 태그를 추가해서 리턴
        if image_url:
            img_html = f'<div style="margin-top: 10px;"><img src="{image_url}" alt="{final_emotion}" style="width: 300px; border-radius: 10px;"></div>'
            # 디버그용 텍스트 
            debug_info = f"<div style='font-size: 12px; color: gray; margin-top: 5px;'>감정: <b>{final_emotion}</b> ({match_reason})</div>"
            return string + "\n" + img_html + debug_info
        
        return string

    except Exception as e:
        print(f"[Runtime Error] {e}")
        return string

def ui():
    pass