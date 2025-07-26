from faster_whisper import WhisperModel
import os
import wave
import sounddevice as sd
import time
from alive_progress import alive_bar
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from flask import Flask, render_template, request, jsonify

faster_whisper_cache = os.path.expanduser("./.cache/faster_whisper")
os.makedirs(faster_whisper_cache, exist_ok=True)
default = os.environ.get("HF_HOME")
print(f"[🔍]Default cache directory: {default}")
# Set the cache directory for Hugging Face models
os.environ["HF_HOME"] = faster_whisper_cache
print(f"[📂]Using cache directory: {faster_whisper_cache}")

print("[👀]Generating sentiment dictionary")
# Score to sentiment for vader sentiment analysis
sentiment_dict = {
    "neg": "Negative",
    "neu": "Neutral",
    "pos": "Positive",
    "compound": "Compound"
}


SYSTEM_LOG_PATH = "./system/logs/"
os.makedirs(os.path.dirname(SYSTEM_LOG_PATH),
            exist_ok=True)  # Ensure the directory

# Change to "base.en", "small.en", "medium.en", or "large-v2" as needed
MODEL_SIZE = "small.en"
RECORD_SECONDS = 20  # Duration of the recording in seconds
SAMPLE_RATE = 16000  # Sample rate for the audio recording


model = WhisperModel(MODEL_SIZE, device="cuda" if os.environ.get(
    "CUDA_VISIBLE_DEVICES") else "cpu")


def record(length=RECORD_SECONDS):
    print("[🎧]Start recodring for {0} sec at {1} samplerate".format(
        RECORD_SECONDS, SAMPLE_RATE))
    recording = sd.rec(int(RECORD_SECONDS * SAMPLE_RATE),
                       samplerate=SAMPLE_RATE, channels=1, dtype='int16')
    with alive_bar(length, title="Recording", spinner="dots") as bar:
        for _ in range(length):
            time.sleep(1)
            bar()
    sd.wait()  # Wait until recording is finished
    print("[🎧]Recording finished")
    print("[🎧]Saving recording to file...")
    with wave.open("recording.wav", 'wb') as wf:
        wf.setnchannels(1)  # Mono
        wf.setsampwidth(2)  # 16-bit samples
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(recording.tobytes())


def analyze_sentiment(text):
    print("[🔍]Analyzing sentiment...")
    analyzer = SentimentIntensityAnalyzer()
    sentiment = analyzer.polarity_scores(text)
    print(f"[🔍]Sentiment analysis result: {sentiment}")
    compound = sentiment['compound']
    if compound > 0.05:
        return "Positive"
    elif compound < -0.05:
        return "Negative"
    else:
        return "Neutral"


def transcribe():
    print("[📝]Transcribing audio...")
    segments, info = model.transcribe("recording.wav", beam_size=5)
    print(f"[📝]Detected language: {info.language}")
    text = " ".join([segment.text for segment in segments])
    print(f"[📝]Transcription: {text.strip()}")
    print("[📝]Transcription finished... Saving")
    logPath = "./recording_logs/"
    os.makedirs(logPath, exist_ok=True)  # Ensure the directory exists
    sentiment = analyze_sentiment(text)
    print(f"[🔍]Sentiment: {sentiment}")
    logName = "log-" + sentiment + \
        time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) + ".txt"
    with open(logPath + logName, "w", encoding='utf-8') as f:
        f.write(text.strip())
    print(f"[📝]Log saved to {logPath + logName}")


app = Flask(__name__)
# Write the system log when starting the app
oneTimeSystemLogName = "system-" + \
    time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) + ".txt"
with open(SYSTEM_LOG_PATH + oneTimeSystemLogName, "w", encoding='utf-8') as f:
    f.write(
        f"App started at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}\n")
    f.write(f"Model size: {MODEL_SIZE}\n")
    f.write(f"Sample rate: {SAMPLE_RATE}\n")
    f.write(f"Recording duration: {RECORD_SECONDS} seconds\n")
    f.write(f"Cache directory: {faster_whisper_cache}\n")
    f.write(
        "---------------------------------------------------------------------------\n")


@app.route('/')
def index():

    return render_template('index.htm')


@app.route('/list_models')
def list_models():
    """List available Whisper models from HuggingFace cache"""
    with open(SYSTEM_LOG_PATH + oneTimeSystemLogName, "a", encoding='utf-8') as log:
        log.write(
            f"[List Models API] Request received at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}\n")
        models = []
        log.write(
            f"[List Models API] Searching for models in path: {faster_whisper_cache}\n")
        for d in os.listdir(faster_whisper_cache+"/hub/"):
            log.write(f"[List Models API] Checking directory: {d}\n")
            if any(name in d for name in ["tiny.en", "base.en", "small.en", "medium.en", "large-v2"]):

                models.append(d)
        # 如果没检测到就返回默认支持列表
        if not models:
            log.write(
                "[List Models API] No models found in cache, using default list.\n")
            models = ["tiny.en", "base.en",
                      "small.en", "medium.en", "large-v2"]
        log.write(f"[List Models API] Models found: {models}\n")
        log.write("[List Models API] Response sent - End of request\n")
    return jsonify(models)


@app.route('/clear_logs', methods=['POST'])
def clear_logs():
    """Clear all logs"""
    logPath = SYSTEM_LOG_PATH
    if os.path.exists(logPath):
        for fname in os.listdir(logPath):
            os.remove(os.path.join(logPath, fname))
    return 'ok', 200


@app.route('/transcribe', methods=['POST'])
def transcribe_api():
    with open(SYSTEM_LOG_PATH + oneTimeSystemLogName, "a", encoding='utf-8') as log:
        log.write(
            f"[Transcript API] Request received at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}\n")
        audio = request.files['audio']
        audio.save('recording.wav')
        # 获取模型参数
        model_name = request.form.get('model', MODEL_SIZE)
        # What the brower would return like models--Systran--faster-whisper-base.en
        # Turn this into a valid model name
        model_name = model_name.split(
            '--')[-1] if '--' in model_name else model_name
        model_name = model_name.split(
            '-')[-1] if '-' in model_name else model_name
        # 使用选定模型
        log.write("[Transcript API] Using model: " + model_name + "\n")
        log.write("[Transcript API] Loading model....\n")
        try:
            whisper_model = WhisperModel(
                model_name, device="cuda" if os.environ.get("CUDA_VISIBLE_DEVICES") else "cpu")

            log.write("[Transcript API] Model loaded successfully.\n")
            log.write("[Transcript API] Transcribing audio...\n")
        except Exception as e:
            log.write(f"[Transcript API] Error loading model: {str(e)}\n")
            return jsonify({"error": "Model loading failed"}), 500
        segments, info = whisper_model.transcribe("recording.wav", beam_size=5)
        text = " ".join([segment.text for segment in segments])
        sentiment = analyze_sentiment(text)
        logPath = "./recording_logs/"
        os.makedirs(logPath, exist_ok=True)
        logName = "log-" + sentiment + \
            time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime()) + ".txt"

        with open(logPath + logName, "w", encoding='utf-8') as f:
            f.write(text.strip())
        log.write(
            f"[Transcript API] Transcription saved: {logPath + logName}\n")
        os.remove("recording.wav")
        log.write(f"[Transcript API] Temporary audio file removed\n")
        log.write("[Transcript API] Response sent - End of request\n")
        return jsonify({"transcription": text.strip(), "sentiment": sentiment})


@app.route('/logs')
def get_logs():
    with open(SYSTEM_LOG_PATH + oneTimeSystemLogName, "a", encoding='utf-8') as log:
        # log.write(
        #    f"[Logs API] Request received at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}\n")
        logPath = SYSTEM_LOG_PATH
        logs = []
        if os.path.exists(logPath):
            for fname in sorted(os.listdir(logPath), reverse=True):
                with open(os.path.join(logPath, fname), encoding='utf-8') as f:
                    logs.append(f"{fname}:\n {f.read()}")
        # log.write(f"[Logs API] Logs retrieved: {len(logs)} entries\n")
        # log.write("[Logs API] Response sent - End of request\n")
        return jsonify(logs)


if __name__ == "__main__":
    app.run(debug=True)

# if __name__ == "__main__":
#     length = input(
#         "How long would you like to record? Press Enter to start...\n(Press Enter for default 20 seconds): ")
#     record(int(length) if length.isdigit() else RECORD_SECONDS)
#     transcribe()
#     print("[✅]Process completed successfully!")
#     input("Press Enter to exit...")
#     os.remove("recording.wav")  # Clean up the recording file
#     print("[🗑️]Recording file removed.")
