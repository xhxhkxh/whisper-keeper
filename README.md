# 🎙️ Whisper Keeper

A beautiful web application that allows you to record audio, transcribe it using OpenAI's Whisper models, and analyze the sentiment of your recordings. Perfect for digital journaling, note-taking, or capturing your thoughts with AI-powered insights.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-v2.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

- 🎤 **Real-time Audio Recording** - Record audio directly in your browser with customizable duration (1-60 seconds)
- 🤖 **AI-Powered Transcription** - Uses Faster-Whisper models for accurate speech-to-text conversion
- 😊 **Sentiment Analysis** - Analyzes the emotional tone of your recordings using VADER sentiment analysis
- 🎨 **Beautiful UI** - Modern, responsive design with real-time progress indicators and animations
- 📊 **Multiple Model Support** - Choose from various Whisper model sizes (tiny, small, medium, large)
- 📝 **Automatic Logging** - All transcriptions are automatically saved with timestamps and sentiment labels
- 💫 **Motivational Quotes** - Contextual inspirational messages based on detected sentiment
- 🔄 **Real-time Updates** - Live progress tracking and system logs

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- CUDA-compatible GPU (optional, for faster processing)
- Microphone access in your browser

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/xhxhkxh/whisper-keeper.git
   cd whisper-keeper
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

### Dependencies

Create a `requirements.txt` file with:

```txt
faster-whisper>=0.9.0
flask>=2.0.0
sounddevice>=0.4.0
wave
alive-progress>=3.0.0
vaderSentiment>=3.3.0
```

## 🎛️ Configuration

### Environment Variables

- `CUDA_VISIBLE_DEVICES` - Set to use GPU acceleration (optional)
- `HF_HOME` - Custom cache directory for Hugging Face models (optional)

### Model Configuration

Edit the following variables in `app.py`:

```python
MODEL_SIZE = "small.en"  # Options: tiny.en, base.en, small.en, medium.en, large-v2
RECORD_SECONDS = 20      # Default recording duration
SAMPLE_RATE = 16000      # Audio sample rate
```

## 📁 Project Structure

```
whisper-keeper/
├── app.py                 # Main Flask application
├── templates/
│   └── index.htm         # Web interface
├── recording_logs/       # Transcribed text files (auto-created)
├── system/
│   └── logs/            # System operation logs (auto-created)
├── .cache/
│   └── faster_whisper/  # Model cache (auto-created)
└── README.md
```

## 🎯 Usage

1. **Select a Model**: Choose your preferred Whisper model from the dropdown
2. **Set Duration**: Use the slider to set recording length (1-60 seconds)
3. **Start Recording**: Click the record button and grant microphone permissions
4. **View Results**: See your transcription and sentiment analysis
5. **Check Logs**: Monitor system logs and review past recordings

## 🔧 API Endpoints

- `GET /` - Main web interface
- `POST /transcribe` - Upload audio for transcription
- `GET /list_models` - Get available Whisper models
- `GET /logs` - Retrieve system logs
- `POST /clear_logs` - Clear all system logs

## 🎨 Features in Detail

### Real-time Recording
- Visual progress bar with countdown timer
- Automatic stop after selected duration
- Live audio level indicators

### Sentiment Analysis
- **Positive**: Encouraging messages with celebration emojis
- **Negative**: Supportive messages with motivational quotes
- **Neutral**: Balanced, mindful responses

### Smart Logging
- Automatic file naming with sentiment and timestamp
- Organized log structure for easy review
- System operation tracking

## 🔧 Troubleshooting

### Common Issues

1. **Microphone not working**
   - Ensure browser has microphone permissions
   - Check system audio settings
   - Try refreshing the page

2. **Model loading errors**
   - Check internet connection for initial model download
   - Verify sufficient disk space for model cache
   - Try a smaller model size first

3. **CUDA errors**
   - Install appropriate CUDA drivers
   - Set `CUDA_VISIBLE_DEVICES=""` to force CPU usage

4. **Performance issues**
   - Use smaller models (tiny.en or base.en) for faster processing
   - Reduce recording duration
   - Close other resource-intensive applications

## 🤝 Contributing

Contributions are welcome! Here are some ways you can help:

- 🐛 Report bugs and issues
- 💡 Suggest new features
- 🔧 Submit pull requests
- 📖 Improve documentation
- 🎨 Enhance the UI/UX

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -am 'Add new feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) - For the amazing speech recognition models
- [Faster-Whisper](https://github.com/guillaumekln/faster-whisper) - For the optimized inference implementation
- [VADER Sentiment](https://github.com/cjhutto/vaderSentiment) - For sentiment analysis capabilities
- [Flask](https://flask.palletsprojects.com/) - For the web framework

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/xhxhkxh/whisper-keeper/issues) page
2. Create a new issue with detailed information
3. Include your Python version, OS, and error messages

---

**Made with ❤️ by the Xteclab team**

*Capture your thoughts, understand your emotions, and keep your digital diary with AI.*
