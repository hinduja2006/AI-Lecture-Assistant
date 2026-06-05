📚 AI Lecture Assistant

An AI-powered Streamlit web application that converts lecture audio into transcripts, structured notes, quizzes, and an interactive AI tutor using Whisper and Google Gemini API.


🚀 Live Features

- 🎤 Speech-to-Text conversion using OpenAI Whisper
- 📚 AI-generated structured notes (summary + key points)
- 🎯 Auto-generated MCQ quiz with scoring system
- 🤖 AI tutor to answer questions from lecture transcript
- 🔄 Reset and retry functionality
- 💾 Session state management for smooth user experience


🛠️ Tech Stack

- Python
- Streamlit
- OpenAI Whisper
- Google Gemini API (Generative AI)
- JSON parsing
- Session State Management


⚙️ Installation & Setup

1. Clone the repository
git clone https://github.com/hinduja2006/ai-lecture-assistant.git
cd ai-lecture-assistant

2. Install dependencies
pip install -r requirements.txt

3. Set up API Key
Create a .env file in the root directory:
.env
GEMINI_API_KEY=your_api_key_here OR set it as an environment variable in your system or deployment platform.

4. Run the application
bash
streamlit run app.py


🔑 Environment Variables

| Variable       | Description               |
| -------------- | ------------------------- |
| GEMINI_API_KEY | API key for Google Gemini |


📌 How It Works

1. Upload a lecture audio file (MP3/WAV)
2. Whisper converts speech → text transcript
3. Gemini processes transcript to:
   * Generate structured notes
   * Create MCQ quiz
   * Answer user questions
4. Streamlit UI displays everything in interactive tabs


🎯 Features in Detail

📝 Transcript Generation
Converts uploaded lecture audio into readable text using Whisper.

📚 AI Notes
Automatically summarizes lecture into:
* Key points
* Simple explanation
* Short summary

🎯 Quiz Generator
* Generates 5 MCQs from lecture
* Shows score after submission
* Highlights correct and wrong answers

🤖 AI Tutor
Ask any question related to the lecture and get context-aware answers.


📸 UI Sections

* Sidebar with feature overview
* Transcript tab
* Notes tab
* Quiz tab
* AI Tutor tab


🔒 Security Note

* Do NOT upload .env file to GitHub
* API keys should always be stored securely using environment variables


📈 Future Improvements

* PDF export for notes
* Voice-based Q&A
* Multi-language transcription
* Better quiz difficulty levels
* Cloud deployment integration


👨‍💻 Author
Built by Hinduja


⭐ Support
If you like this project:
 Give it a ⭐ on GitHub
 Fork and improve it
