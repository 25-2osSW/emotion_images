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

    # 1. 로컬 모델 로딩
    if emotion_classifier is None:
        try:
            base_path = os.path.dirname(__file__)
            local_model_path = os.path.join(base_path, "model")
            
            if not os.path.exists(local_model_path):
                print(f"[Error] 'model' 폴더가 없습니다. 경로: {local_model_path}")
                return string

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
        # top_k=None: 모든 점수 가져오기
        raw_results = emotion_classifier(string, truncation=True, max_length=512, top_k=None)
        
        results = raw_results
        if isinstance(raw_results, list) and len(raw_results) > 0 and isinstance(raw_results[0], list):
            results = raw_results[0]

        # 점수 변수 초기화
        score_neg = 0.0
        score_neu = 0.0
        score_pos = 0.0
        
        # 라벨 이름이 달라도(LABEL_0 vs negative) 알아서 찾아넣기
        for item in results:
            label = item['label'].lower() # 소문자로 변환해서 비교
            score = item['score']
            
            # 부정 (LABEL_0 or negative)
            if 'label_0' in label or 'negative' in label:
                score_neg = score
            # 중립 (LABEL_1 or neutral)
            elif 'label_1' in label or 'neutral' in label:
                score_neu = score
            # 긍정 (LABEL_2 or positive)
            elif 'label_2' in label or 'positive' in label:
                score_pos = score

        # 가장 높은 점수의 라벨 찾기
        sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)
        top_label_raw = sorted_results[0]['label'].lower()
        
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
        # 부정 처리
        if 'label_0' in top_label_raw or 'negative' in top_label_raw:
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

        # 긍정 처리
        elif 'label_2' in top_label_raw or 'positive' in top_label_raw:
            if any(word in string for word in keywords_surprise):
                final_emotion = "surprise"
                match_reason = "긍정 + 키워드(놀람)"
            elif any(word in string for word in keywords_joy):
                final_emotion = "joy"
                match_reason = "긍정 + 키워드(기쁨)"
            else:
                final_emotion = "joy"
                match_reason = "긍정(키워드 없음) -> 기쁨"

        # 중립 처리
        else: 
            if any(word in string for word in keywords_disgust): final_emotion = "disgust"
            elif any(word in string for word in keywords_joy): final_emotion = "joy"
            elif any(word in string for word in keywords_anger): final_emotion = "anger"
            elif any(word in string for word in keywords_sadness): final_emotion = "sadness"
            elif any(word in string for word in keywords_surprise): final_emotion = "surprise"
            else:
                final_emotion = "neutral"
                match_reason = "중립 판단"

        # 5. CMD 창 출력
        print("\n" + "="*40)
        print(f"[입력 텍스트]: {string[:30]}...")
        print("-" * 40)
        print(f"[모델 분석 점수]")
        print(f" - 부정 (Negative): {score_neg*100:.2f}%")
        print(f" - 중립 (Neutral) : {score_neu*100:.2f}%")
        print(f" - 긍정 (Positive): {score_pos*100:.2f}%")
        print("-" * 40)
        print(f"[최종 판정]: {final_emotion}")
        print(f"[판정 사유]: {match_reason}")
        print("="*40 + "\n")
        
        # 이미지 출력
        base_path = os.path.dirname(__file__)
        image_folder = os.path.join(base_path, "images", final_emotion)
        
        image_url = None
        if os.path.exists(image_folder):
            valid_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.webp')
            files = [f for f in os.listdir(image_folder) if f.lower().endswith(valid_extensions)]
            if files:
                selected = random.choice(files)
                image_url = f"file/extensions/emotion_images/images/{final_emotion}/{selected}"
        
        if image_url:
            img_html = f'<div style="margin-top: 10px;"><img src="{image_url}" alt="{final_emotion}" style="width: 300px; border-radius: 10px;"></div>'
            debug_info = f"<div style='font-size: 12px; color: gray; margin-top: 5px;'>감정: <b>{final_emotion}</b> ({match_reason})</div>"
            return string + "\n" + img_html + debug_info
        
        return string

    except Exception as e:
        print(f"[Runtime Error] {e}")
        print(f"DEBUG: {raw_results}") 
        return string

def ui():
    pass