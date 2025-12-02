# Text-Generation-WebUI용 SillyTavern 감정 이미지 연동 (Emotion Image Linker)

이 확장 기능은 **Text-Generation-WebUI (Oobabooga)**에서 AI의 답변 내용을 분석하여, 감정에 맞는 **SillyTavern**의 이미지를 자동으로 채팅창에 띄워줍니다.

일반적인 3단계(긍정/부정/중립) 감정 분석 모델을 사용하여, SillyTavern에서 자주 사용하는 7가지 감정으로 세분화하여 매핑합니다:
`anger`(분노), `disgust`(혐오), `fear`(공포), `joy`(기쁨), `neutral`(중립), `sadness`(슬픔), `surprise`(놀람)

## ✨ 주요 기능
- **실시간 감정 분석:** AI의 답변을 분석하여 가장 적절한 감정을 찾습니다.
- **할루시네이션 방지:** AI가 스스로 생성한 가짜 이미지 태그나 잘못된 링크를 자동으로 감지하고 삭제합니다.
- **랜덤 이미지 출력:** 감정 폴더 안에 있는 이미지 중 하나를 무작위로 선택해 보여줍니다.
- **에러 방지 (Safe Mode):** 해당 감정의 폴더나 파일이 없을 경우, 엑박(404 에러)을 띄우는 대신 이미지를 표시하지 않습니다.

## 🛠️ 설치 방법 (Installation)

### 1. 스크립트 설치
WebUI의 `extensions` 폴더 안에 새로운 폴더(예: `st_emotion_linker`)를 만들고, 그 안에 `script.py`를 넣으세요.
- 경로: `text-generation-webui/extensions/st_emotion_linker/script.py`

### 2. 감정 분석 모델 다운로드
1. 확장 기능 폴더 안에 `model`이라는 이름의 새 폴더를 만듭니다.
2. [cardiffnlp/twitter-xlm-roberta-base-sentiment](https://huggingface.co/cardiffnlp/twitter-xlm-roberta-base-sentiment) (혹은 사용하고 싶은 모델) 페이지로 이동합니다.
3. `Files and versions` 탭에서 모델 파일들(`config.json`, `pytorch_model.bin` 등)을 전부 다운로드하여 `model` 폴더 안에 넣습니다.

### 3. 경로 설정 (필수!)
`script.py` 파일을 메모장이나 VSCode로 열고, `IMAGE_ROOT_PATH` 변수를 **본인의 SillyTavern 경로**에 맞게 수정해야 합니다.

```python
# [예시] 본인의 윈도우 사용자 이름(User)에 맞게 수정하세요.
IMAGE_ROOT_PATH = r"C:\Users\내이름\Desktop\SillyTavern\public\emotion_images"