# 🎓 SmartStudy AI - Your Personal Exam Coach

A comprehensive AI-powered study assistant built with **LangChain** and **Google Gemini API** that helps students prepare for exams through personalized learning, document analysis, and adaptive quizzes.

## ✨ Features

### 🚀 Core Functionality
- **📄 Document Upload**: Support for PDF and DOCX files
- **❓ Topic Learning**: Ask about any topic and get simple explanations
- **🧠 Smart Quiz Generation**: Personalized quizzes with multiple question types
- **📊 Performance Tracking**: Monitor your learning progress and identify weak areas
- **📋 Revision Planning**: Get personalized study recommendations
- **🔄 Fallback System**: Automatic fallback to Hugging Face models when Gemini quota is exceeded

### 🎯 Question Types
- **Multiple Choice Questions** (MCQs) with 4 options
- **Fill in the Blanks** with hints
- **Short Answer Questions** with expected answers

### 🧠 AI-Powered Features
- **Simple Explanations**: Complex topics explained in beginner-friendly language
- **Adaptive Learning**: Tracks your performance and suggests areas for improvement
- **Memory System**: Remembers your learning history and progress
- **Personalized Feedback**: Custom revision plans based on quiz performance
- **Robust Error Handling**: Graceful fallback when primary AI service is unavailable

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python + LangChain
- **Primary AI Model**: Google Gemini API (Gemini 1.5 Flash)
- **Fallback AI Model**: Hugging Face Transformers (distilgpt2)
- **Memory**: LangChain Conversation Memory System
- **Document Processing**: PyPDF2, python-docx
- **Text Processing**: LangChain Text Splitters

## 📋 Prerequisites

- Python 3.8+
- Google Gemini API key
- Virtual environment (recommended)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd langchain
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the project root:
```bash
GOOGLE_API_KEY=your_gemini_api_key_here
```

**To get a Google Gemini API key:**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key to your `.env` file

### 5. Run the Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📁 Project Structure & File Descriptions

```
langchain/
│
├── 📱 app.py                    # Main Streamlit application
│   ├── User interface and navigation
│   ├── Document upload handling
│   ├── Topic input processing
│   ├── Quiz generation and display
│   ├── Interactive quiz interface
│   ├── Progress tracking dashboard
│   └── Session state management
│
├── ⚡ chains.py                 # LangChain AI operations
│   ├── SmartStudyChains class
│   ├── Explanation generation
│   ├── Quiz creation with fallback
│   ├── Revision plan generation
│   ├── LLM provider integration
│   └── Error handling and fallback logic
│
├── 🧠 memory.py                 # Memory management system
│   ├── SmartStudyMemory class
│   ├── Conversation buffer memory
│   ├── Learning progress tracking
│   ├── Topic and score history
│   ├── Duplicate detection
│   └── Session persistence
│
├── 🔧 utils.py                  # Document processing utilities
│   ├── PDF and DOCX loading
│   ├── Text extraction
│   ├── Content validation
│   ├── Text splitting
│   └── File format checking
│
├── 📝 prompts.py                # AI prompt templates
│   ├── Explanation generation prompts
│   ├── Quiz creation prompts
│   ├── Revision planning prompts
│   └── Prompt customization
│
├── 🤖 llm_providers.py          # LLM provider management
│   ├── HuggingFaceProvider class
│   ├── Fallback LLM system
│   ├── Model loading and caching
│   ├── Text generation
│   └── Error handling
│
├── 🧪 test_setup.py             # Setup verification script
│   ├── Import testing
│   ├── Environment validation
│   ├── API key verification
│   ├── Dependency checking
│   └── System diagnostics
│
├── 📋 requirements.txt          # Python dependencies
│   ├── Streamlit for UI
│   ├── LangChain for AI chains
│   ├── Google Gemini API
│   ├── Hugging Face Transformers
│   ├── Document processing libraries
│   └── Other supporting packages
│
├── 🔑 env_example.txt           # Environment variables template
│   ├── API key configuration
│   ├── Model settings
│   └── Customization options
│
├── 📖 README.md                 # Project documentation
│   ├── Installation guide
│   ├── Usage instructions
│   ├── File descriptions
│   ├── Troubleshooting
│   └── Contributing guidelines
│
├── ⚡ QUICK_START.md            # Quick start guide
│   ├── 3-step setup
│   ├── Basic usage
│   ├── Common issues
│   └── Quick troubleshooting
│
└── 📁 venv/                     # Virtual environment
    ├── Python packages
    ├── Dependencies
    └── Isolated environment
```

## 🎮 How to Use

### 1. **Upload a Document**
- Click "Upload Document" and select a PDF or DOCX file
- Click "Process Document" to extract content
- The AI will generate explanations and quizzes based on your document

### 2. **Ask About a Topic**
- Type any topic in the "Ask About a Topic" section
- Click "Learn Topic" to get a simple explanation
- Generate quizzes to test your understanding

### 3. **Take Quizzes**
- Answer multiple choice questions, fill in the blanks, and short answer questions
- Submit your answers to get immediate feedback
- View your score and performance analysis

### 4. **Track Progress**
- Monitor your learning progress in the sidebar
- View weak areas and strengths
- Get personalized revision suggestions

## 🔧 Configuration

### Environment Variables
- `GOOGLE_API_KEY`: Your Google Gemini API key (required)

### Customization
You can modify the following in `prompts.py`:
- Explanation generation prompts
- Quiz generation prompts
- Revision planning prompts

## 📊 Memory System

The app uses LangChain's advanced memory system:
- **ConversationBufferMemory**: Tracks current session
- **ConversationSummaryMemory**: Maintains long-term learning progress
- **Custom Progress Tracking**: Monitors topics, scores, and weak areas

## 🔄 Fallback System

When the primary Gemini API quota is exceeded:
- **Automatic Detection**: System detects API quota issues
- **Seamless Fallback**: Switches to Hugging Face distilgpt2 model
- **Structured Output**: Ensures consistent quiz format even with fallback
- **User Notification**: Informs users when fallback is active

## 🚨 Troubleshooting

### Common Issues

1. **API Key Error**
   - Ensure `GOOGLE_API_KEY` is set in your `.env` file
   - Verify the API key is valid and has sufficient quota

2. **Document Upload Issues**
   - Check file format (PDF/DOCX only)
   - Ensure file size is under 200MB
   - Verify file is not corrupted

3. **Memory Issues**
   - Use "Clear Session" to reset current session
   - Use "Reset Progress" to clear all learning data

4. **Performance Issues**
   - Large documents may take longer to process
   - Consider splitting very large documents

5. **Fallback System Issues**
   - If you see "Generated by fallback LLM" messages, your Gemini quota is exceeded
   - The app will still work with the fallback model
   - Wait for your Gemini quota to reset or upgrade your plan

## 🧪 Testing Your Setup

Run the test script to verify everything is working:
```bash
python test_setup.py
```

This will check:
- ✅ All required modules are installed
- ✅ Environment variables are set
- ✅ API key is valid
- ✅ All components are working

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **LangChain** for the powerful AI framework
- **Google Gemini** for the advanced language model
- **Hugging Face** for the fallback transformer models
- **Streamlit** for the beautiful web interface
- **Open Source Community** for various supporting libraries

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section
2. Run `python test_setup.py` to diagnose issues
3. Review the error messages in the app
4. Open an issue on GitHub
5. Check the LangChain and Google Gemini documentation

## 🎯 Quick Start

For a faster setup, see `QUICK_START.md` for a 3-step guide.

---

**Happy Learning! 🎓✨**