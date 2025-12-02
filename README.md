# Text-Generation-WebUI용 SillyTavern 감정 이미지 연동 

이 확장 기능은 **Text-Generation-WebUI (Oobabooga)**에서 AI의 답변 내용을 분석하여, 감정에 맞는 **SillyTavern**의 이미지를 자동으로 채팅창에 띄워줍니다.

일반적인 3단계(긍정/부정/중립) 감정 분석 모델을 사용하여, 키워드와 함께 세부적인 7가지 감정으로 나눕니다.
`anger`(분노), `disgust`(혐오), `fear`(공포), `joy`(기쁨), `neutral`(중립), `sadness`(슬픔), `surprise`(놀람)

## ✨ 주요 기능
- **실시간 감정 분석:** AI의 답변을 분석하여 가장 적절한 감정을 찾습니다.
- **할루시네이션 방지:** AI가 스스로 생성한 가짜 이미지 태그나 잘못된 링크를 자동으로 감지하고 삭제합니다.
- **랜덤 이미지 출력:** 감정 폴더 안에 있는 이미지 중 하나를 무작위로 선택해 보여줍니다.
- **에러 방지 (Safe Mode):** 해당 감정의 폴더나 파일이 없을 경우, 엑박(404 에러)을 띄우는 대신 이미지를 표시하지 않습니다.

## 🛠️ 설치 방법 (Installation)

### 1. 스크립트 설치
extensions안에 클론해서 가져가시면 됩니다.
- 경로: `text-generation-webui/extensions/emotion_images/` 이렇게 되있어야 합니다.

### 2. 감정 분석 모델 다운로드
1. emotion_images안에 model이라는 빈 폴더가 있을탠데 밑에 허깅페이스 주소로가서 
2. [cardiffnlp/twitter-xlm-roberta-base-sentiment](https://huggingface.co/cardiffnlp/twitter-xlm-roberta-base-sentiment) 
3. `config.json , pytorch_model.bin, sentencepiece.bpe.model , special_tokens_map.json`을 다운받은뒤 model파일 안에 넣어주세요

### 3. SillyTavern 설정 필수!
**SillyTavern안에 public폴더로 가신다음 emotion_images 폴더를 하나 만들어주세요 그안에 위에서 다운받은 images폴더안에 7개의 감정 사진폴더를 넣어주세요**
### 4. 경로 설정 필수!
`script.py` 파일을 메모장이나 VSCode로 열고, `IMAGE_ROOT_PATH` 변수를 **본인의 SillyTavern 안에 public/emotion_images **로 맞게 수정해야 합니다.
예: C:\Users\user\Desktop\OpenSW\SillyTavern\public\emotion_images


```python
# [예시] 본인의 윈도우 사용자 이름(User)에 맞게 수정하세요.
IMAGE_ROOT_PATH = r"C:\Users\내이름\Desktop\SillyTavern\public\emotion_images"
