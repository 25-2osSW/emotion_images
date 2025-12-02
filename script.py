import os
import random
import urllib.parse
import re  
from transformers import pipeline
# 다국어 모델
# 이미지 경로 바꿔야돼요!!!!!!!!
IMAGE_ROOT_PATH = r"C:\Users\user\Desktop\OpenSW\SillyTavern\public\emotion_images" 

# 사용할 폴더 이름
VALID_EMOTIONS = ["anger", "disgust", "fear", "joy", "neutral", "sadness", "surprise"]

# 전역 변수
emotion_classifier = None

def get_final_emotion(label, text):
    label = str(label).lower()
    text = str(text).lower() 

    keywords_fear = ['무서', '공포', '겁', '소름', '불안', '살려', '도망', 'scared', 'afraid', 'fear']
    keywords_disgust = ['구역질', '토', '우웩', '역겨', '극혐', '더러', '비위', 'disgust', 'gross', 'eww']
    keywords_sadness = ['슬퍼', '눈물', '울', '우울', '흑흑', 'ㅠㅠ', '좌절', '실망', 'sad', 'cry', 'tear', 'depressed']
    keywords_surprise = ['놀라', '깜짝', '헉', '대박', '헐', '?!', '세상에', 'surprise', 'shock', 'omg', 'wow']

    if 'label_0' in label or 'negative' in label:
        if any(w in text for w in keywords_disgust): return "disgust"
        if any(w in text for w in keywords_fear): return "fear"
        if any(w in text for w in keywords_sadness): return "sadness"
        return "anger" 

    elif 'label_2' in label or 'positive' in label:
        if any(w in text for w in keywords_surprise): return "surprise"
        return "joy" 

    else:
        if any(w in text for w in keywords_surprise): return "surprise"
        return "neutral"

def output_modifier(string, state):
    global emotion_classifier
    
    if not string: return string

    # 1. 마크다운 이미지 태그 제거 (AI가 만든 태그 삭제)
    clean_string = re.sub(r'!\[.*?\]\(.*?\)', '', string)
    # 2. HTML 이미지 태그 제거 (<img ...>)
    clean_string = re.sub(r'<img[^>]+>', '', clean_string)
    # 3. 앞뒤 공백 정리
    clean_string = clean_string.strip()

    # 1. 모델 로딩
    if emotion_classifier is None:
        try:
            script_dir = os.path.dirname(__file__)
            local_model_path = os.path.join(script_dir, "model")
            if not os.path.exists(local_model_path): return clean_string 
            emotion_classifier = pipeline("text-classification", model=local_model_path, device=-1)
        except Exception as e:
            print(f"[Error] 모델 로드 실패: {e}")
            return clean_string

    try:
        # 2. 분석 실행
        raw_results = emotion_classifier(clean_string, truncation=True, max_length=512, top_k=None)
        
        if isinstance(raw_results, list) and len(raw_results) > 0 and isinstance(raw_results[0], list):
            results = raw_results[0]
        elif isinstance(raw_results, list):
            results = raw_results
        elif isinstance(raw_results, dict):
            results = [raw_results]
        else:
            return clean_string

        # 3. 감정 결정
        sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)
        top_label = sorted_results[0]['label']
        final_emotion = get_final_emotion(top_label, clean_string)

        if final_emotion not in VALID_EMOTIONS:
            final_emotion = "neutral"

        # 로그 출력
        print(f"\n[분석] {clean_string[:15]}... -> 결과: {final_emotion}")

        # 4. 이미지 생성
        target_folder = os.path.join(IMAGE_ROOT_PATH, final_emotion)
        
        if os.path.exists(target_folder):
            valid_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.webp')
            files = [f for f in os.listdir(target_folder) if f.lower().endswith(valid_extensions)]
            
            if files:
                selected = random.choice(files)
                encoded_filename = urllib.parse.quote(selected)
                image_url = f"http://127.0.0.1:8000/emotion_images/{final_emotion}/{encoded_filename}"
                
                
                return clean_string + f'\n\n<img src="{image_url}" alt="{final_emotion}" style="width: 350px; border-radius: 15px; display: block; margin-top: 5px;">'
        
        return clean_string

    except Exception as e:
        print(f"[Critical Error] {e}")
        return clean_string 

def ui():
    pass