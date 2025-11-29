🎭 Emotion Images Extension (감정 분석 이미지 확장)
감정분석 모델 입니다.

📂 폴더 구조 (Directory Structure)
설치 후 폴더 구조는 다음과 같아야 합니다.

text-generation-webui/
├── start_windows.bat
├── install_protobuf.bat  <-- [중요] 여기에 옮겨서 실행!
└── extensions/
    └── emotion_images/   <-- 이 레포지토리 폴더
        ├── script.py
        ├── images/       <-- 감정별 이미지 폴더
        └── model/        <-- 모델 파일 넣는 곳
모델 다운로드
https://huggingface.co/j-hartmann/emotion-english-distilroberta-base/tree/main 여기 들어가셔서 config.json , merges.txt , pytorch_model.bin , special_tokens_map.json , tokenizer.json , tokenizer_config.json , vocab.json 파일 다운받아주시고 model 파일안에 넣어주세요