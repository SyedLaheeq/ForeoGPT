import cv2
import time
import base64
import requests
import threading

VISION_API_URL = "https://openrouter.ai/api/v1/chat/completions"
VISION_API_KEY = "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"
VISION_MODEL = "anthropic/claude-sonnet-5"



EUROLLM_API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
EUROLLM_API_KEY = "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"  

latest_vision = "Waiting for Vision..."
latest_eurollm = "Waiting for EuroLLM..."
latest_latency = 0.0
is_processing = False

def encode_image(frame):
    small_frame = cv2.resize(frame, (512, 512), interpolation=cv2.INTER_AREA)
    _, buffer = cv2.imencode('.jpg', small_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 60])
    return base64.b64encode(buffer).decode('utf-8')

def hybrid_pipeline_worker(frame_copy):
    global latest_vision, latest_eurollm, latest_latency, is_processing
    start_time = time.time()
    
    # STEP 1: Vision via OpenRouter
    base64_image = encode_image(frame_copy)
    vision_headers = {
        "Authorization": f"Bearer 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",
        "Content-Type": "application/json"
    }
    vision_payload = {
        "model": VISION_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this webcam frame in under 8 words."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }
        ],
        "max_tokens": 20
    }

    english_text = None
    try:
        vision_resp = requests.post(VISION_API_URL, headers=vision_headers, json=vision_payload, timeout=8.0)
        if vision_resp.status_code == 200:
            english_text = vision_resp.json()['choices'][0]['message']['content'].strip()
            latest_vision = english_text
        else:
            latest_vision = f"Vision Error: {vision_resp.status_code}"
    except Exception as e:
        latest_vision = f"Vision Exception: {str(e)[:20]}"
    # STEP 2: Translation via Cloud EuroLLM (NVIDIA NIM)
        if english_text:
            nim_headers = {
                "Authorization": f"Bearer {EUROLLM_API_KEY}",
                "Content-Type": "application/json"
            }
            nim_payload = {
                "model": "utter-project/eurollm-9b-instruct",
                "messages": [
                    {"role": "system", "content": "You are a precise translator. Translate this text to Spanish."},
                    {"role": "user", "content": english_text}
                ],
                "max_tokens": 40
            }
            
            try:
                euro_resp = requests.post(EUROLLM_API_URL, headers=nim_headers, json=nim_payload, timeout=10.0)
                if euro_resp.status_code == 200:
                    latest_eurollm = euro_resp.json()['choices'][0]['message']['content'].strip()
                else:
                    latest_eurollm = f"NIM Error: {euro_resp.status_code}"
            except Exception as e:
                latest_eurollm = f"Euro Error: {type(e).__name__}"
            
    latest_latency = time.time() - start_time
    is_processing = False

cap = cv2.VideoCapture(0)
last_ai_check = time.time()
INTERVAL = 4.0  

print("Starting 100% Cloud Pipeline... Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret: break

    norm_frame = cv2.convertScaleAbs(frame, alpha=1.2, beta=15)
    
    current_time = time.time()
    if current_time - last_ai_check > INTERVAL and not is_processing:
        is_processing = True
        last_ai_check = current_time
        threading.Thread(target=hybrid_pipeline_worker, args=(norm_frame.copy(),), daemon=True).start()

    cv2.rectangle(norm_frame, (10, 10), (620, 100), (0, 0, 0), -1)
    
    cv2.putText(norm_frame, f"Vision: {latest_vision}", (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    cv2.putText(norm_frame, f"EuroLLM: {latest_eurollm}", (20, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 165, 0), 2)
    
    status = "Processing Pipeline..." if is_processing else "Idle"
    cv2.putText(norm_frame, f"Latency: {latest_latency:.2f}s | {status}", (20, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

    cv2.imshow("Cloud Hybrid App", norm_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()