# FastAPI Image Processing API

이 프로젝트는 FastAPI를 사용하여 nsfw 이미지 처리 API를 구현한 것입니다. 업로드된 이미지에 대해 객체 탐지를 수행하고 결과를 반환합니다.

## 기능

- 이미지 업로드 및 처리
- 객체 탐지 수행
- 결과를 JSON 형식으로 반환

## 필요 조건

- Python 3.7+
- pip

## 설치 방법

1. 리포지토리를 클론합니다:
   ```
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. 가상 환경을 생성하고 활성화합니다:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. 필요한 패키지를 설치합니다:
   ```
   pip install -r requirements.txt
   ```

## 사용 방법

### 개발 모드로 실행

uvicorn을 사용하여 개발 모드로 실행할 수 있습니다:

```
uvicorn app:app --reload
```

### 프로덕션 모드로 실행

gunicorn을 사용하여 프로덕션 모드로 실행할 수 있습니다:

```
gunicorn app:application -c gunicorn_config.py
```

서버가 실행되면, `http://localhost:8001/docs`에서 Swagger UI를 통해 API를 테스트할 수 있습니다.

## API 엔드포인트

### POST /process_image/

이미지를 업로드하고 처리합니다.

**Parameters**
- `file`: 업로드할 이미지 파일 (선택 사항, url이 제공되지 않은 경우 필수)
- `url`: 처리할 이미지의 URL(선택 사항, 파일이 제공되지 않은 경우 필수)
- `conf_threshold`: 신뢰도 임계값 (기본값: 0.25)
- `iou_threshold`: IoU

**Returns**
객체 감지 결과 및 주석이 포함된 JSON 응답입니다.
```
{
  "result": "nsfw"
}
```

**Example**
이미지 파일 또는 URL과 함께 POST 요청을 전송하여 API를 테스트할 수 있습니다:
```
# Using a file
curl -X POST "http://localhost:8001/process_image/" \
-H "accept: application/json" \
-F "file=@path_to_your_image.jpg" \
-F "conf_threshold=0.3" \
-F "iou_threshold=0.5"

# Using a URL
curl -X POST "http://localhost:8001/process_image/" \
-H "accept: application/json" \
-F "url=https://example.com/image.jpg" \
-F "conf_threshold=0.3" \
-F "iou_threshold=0.5"
```

**License**
이 프로젝트는 MIT 라이선스에 따라 라이선스가 부여됩니다. 자세한 내용은 라이선스 파일을 참조하세요.