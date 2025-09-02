# 🚀 SmartStudy AI - Quick Start Guide

## ⚡ Get Started in 3 Steps

### 1. **Set Your API Key**
Edit the `.env` file and replace the placeholder:
```bash
GOOGLE_API_KEY=your_actual_gemini_api_key_here
```

**Get your API key from:** [Google AI Studio](https://makersuite.google.com/app/apikey)

### 2. **Run the App**
```bash
# Activate virtual environment
source venv/bin/activate

# Start the app
streamlit run app.py
```

### 3. **Open Your Browser**
The app will open at: `http://localhost:8501`

## 🎯 What You Can Do

- **📄 Upload PDF/DOCX** documents for AI analysis
- **❓ Ask about any topic** and get simple explanations
- **🧠 Take personalized quizzes** with instant feedback
- **📊 Track your progress** and identify weak areas
- **📋 Get revision plans** tailored to your performance

## 🔧 Troubleshooting

**If you get API errors:**
- Check your `.env` file has the correct API key
- Verify the API key is valid at Google AI Studio

**If modules fail to import:**
- Make sure you're in the virtual environment
- Run: `pip install -r requirements.txt`

**For more help:** See `README.md` or run `python test_setup.py`

---

**Happy Learning! 🎓✨**
