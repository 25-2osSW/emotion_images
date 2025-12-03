import os
import random
import urllib.parse
import re
from transformers import pipeline
# 다국어 모델
# 본인의 SilyTavern/public/emotion_images 경로를 넣어주세요!!!
IMAGE_ROOT_PATH = r"C:\Users\user\Desktop\OpenSW\SillyTavern\public\emotion_images" 

# 폴더 이름 
VALID_EMOTIONS = ["anger", "disgust", "fear", "joy", "neutral", "sadness", "surprise"]

# 전역 변수
emotion_classifier = None

def output_modifier(string, state):
    global emotion_classifier
    
    if not string: return string

    # 1. 가짜 태그 제거
    clean_string = re.sub(r'!\[.*?\]\(.*?\)', '', string)
    clean_string = re.sub(r'<img[^>]+>', '', clean_string)
    clean_string = clean_string.strip()

    # 2. 모델 로딩
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
        # 3. 텍스트 분석 
        raw_results = emotion_classifier(clean_string, truncation=True, max_length=512, top_k=None)
        
        # 데이터 형태 안전 처리
        if isinstance(raw_results, list) and len(raw_results) > 0 and isinstance(raw_results[0], list):
            results = raw_results[0]
        elif isinstance(raw_results, list):
            results = raw_results
        elif isinstance(raw_results, dict):
            results = [raw_results]
        else:
            return clean_string

        # 점수 변수 초기화
        score_neg = 0.0
        score_neu = 0.0
        score_pos = 0.0
        
        # 점수 추출
        for item in results:
            label = item['label'].lower()
            score = item['score']
            
            if 'label_0' in label or 'negative' in label: score_neg = score
            elif 'label_1' in label or 'neutral' in label: score_neu = score
            elif 'label_2' in label or 'positive' in label: score_pos = score

        # 가장 높은 라벨 찾기
        sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)
        top_label_raw = sorted_results[0]['label'].lower()
        
        # 키워드 목록
        keywords_fear = ['무서', '공포', '겁', '소름', '불안', '두려', '오싹', '섬뜩', '비명', '도망', '살려']
        keywords_disgust = ['구역질', '토', '우웩', '역겨', '극혐', '더러', '비위', '냄새', '썩', '징그', '오물']
        keywords_sadness = ['슬퍼', '눈물', '울', '우울', '흑흑', 'ㅠㅠ', '실망', '비참', '좌절', '괴로', '후회', '상처']
        keywords_anger = ['짜증', '화나', '미친', '닥쳐', '죽', '열받', '멍청', '놈', '꺼져', '분노', '씨', '발', '재수']
        
        keywords_surprise = ['놀라', '깜짝', '헉', '대박', '맙소사', '충격', '헐', '세상에', '믿을 수', '?!']
        keywords_joy = ['흥분', '신나', '기분 좋', '행복', '최고', '사랑', '기뻐', '웃', '하하', 'ㅋㅋ', '굿', '감동', '환상']

        final_emotion = "neutral" 
        match_reason = "기본값"

        # 감정 매칙 로직
        
        # 부정 처리
        if 'label_0' in top_label_raw or 'negative' in top_label_raw:
            if any(word in clean_string for word in keywords_disgust):
                final_emotion = "disgust"
                match_reason = "부정 + 키워드(혐오)"
            elif any(word in clean_string for word in keywords_fear):
                final_emotion = "fear"
                match_reason = "부정 + 키워드(공포)"
            elif any(word in clean_string for word in keywords_sadness):
                final_emotion = "sadness"
                match_reason = "부정 + 키워드(슬픔)"
            elif any(word in clean_string for word in keywords_anger):
                final_emotion = "anger"
                match_reason = "부정 + 키워드(분노)"
            else:
                final_emotion = "anger"
                match_reason = "부정(키워드 없음) -> 분노"

        # 긍정 처리
        elif 'label_2' in top_label_raw or 'positive' in top_label_raw:
            if any(word in clean_string for word in keywords_surprise):
                final_emotion = "surprise"
                match_reason = "긍정 + 키워드(놀람)"
            elif any(word in clean_string for word in keywords_joy):
                final_emotion = "joy"
                match_reason = "긍정 + 키워드(기쁨)"
            else:
                final_emotion = "joy"
                match_reason = "긍정(키워드 없음) -> 기쁨"

        # 중립 처리
        else: 
            if any(word in clean_string for word in keywords_disgust): 
                final_emotion = "disgust"
                match_reason = "중립 + 키워드(혐오)"
            elif any(word in clean_string for word in keywords_joy): 
                final_emotion = "joy"
                match_reason = "중립 + 키워드(기쁨)"
            elif any(word in clean_string for word in keywords_anger): 
                final_emotion = "anger"
                match_reason = "중립 + 키워드(분노)"
            elif any(word in clean_string for word in keywords_sadness): 
                final_emotion = "sadness"
                match_reason = "중립 + 키워드(슬픔)"
            elif any(word in clean_string for word in keywords_surprise): 
                final_emotion = "surprise"
                match_reason = "중립 + 키워드(놀람)"
            else:
                final_emotion = "neutral"
                match_reason = "중립 판단"

        # 폴더명 검사
        if final_emotion not in VALID_EMOTIONS:
            final_emotion = "neutral"

        # 4. 로그 출력
        print("\n" + "="*50)
        print(f"📝 텍스트: {clean_string[:30]}...")
        print(f"📊 점수: 부정({score_neg:.2f}) / 중립({score_neu:.2f}) / 긍정({score_pos:.2f})")
        print(f"🧐 판단 이유: {match_reason}")
        print(f"👉 최종 결정: 【 {final_emotion} 】")
        print("="*50 + "\n")

        # 5. 이미지 생성
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