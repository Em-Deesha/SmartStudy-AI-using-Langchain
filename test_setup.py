#!/usr/bin/env python3
"""
Test script to verify SmartStudy AI project setup
Run this to check if all dependencies and modules are working correctly
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing module imports...")
    
    try:
        import streamlit
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False
    
    try:
        import langchain
        print("✅ LangChain imported successfully")
    except ImportError as e:
        print(f"❌ LangChain import failed: {e}")
        return False
    
    try:
        import langchain_google_genai
        print("✅ LangChain Google GenAI imported successfully")
    except ImportError as e:
        print(f"❌ LangChain Google GenAI import failed: {e}")
        return False
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        print("✅ ChatGoogleGenerativeAI imported successfully")
    except ImportError as e:
        print(f"❌ ChatGoogleGenerativeAI import failed: {e}")
        return False
    
    try:
        import PyPDF2
        print("✅ PyPDF2 imported successfully")
    except ImportError as e:
        print(f"❌ PyPDF2 import failed: {e}")
        return False
    
    try:
        from docx import Document
        print("✅ python-docx imported successfully")
    except ImportError as e:
        print(f"❌ python-docx import failed: {e}")
        return False
    
    return True

def test_custom_modules():
    """Test if custom project modules can be imported"""
    print("\n🔍 Testing custom modules...")
    
    try:
        from prompts import EXPLANATION_PROMPT, QUIZ_PROMPT, REVISION_PROMPT
        print("✅ Prompts module imported successfully")
    except ImportError as e:
        print(f"❌ Prompts module import failed: {e}")
        return False
    
    try:
        from memory import SmartStudyMemory, initialize_memory
        print("✅ Memory module imported successfully")
    except ImportError as e:
        print(f"❌ Memory module import failed: {e}")
        return False
    
    try:
        from utils import load_document, validate_file_upload
        print("✅ Utils module imported successfully")
    except ImportError as e:
        print(f"❌ Utils module import failed: {e}")
        return False
    
    try:
        from chains import SmartStudyChains, initialize_chains
        print("✅ Chains module imported successfully")
    except ImportError as e:
        print(f"❌ Chains module import failed: {e}")
        return False
    
    return True

def test_environment():
    """Test environment variables and configuration"""
    print("\n🔍 Testing environment configuration...")
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✅ .env file found")
    else:
        print("⚠️  .env file not found (create one from env_example.txt)")
    
    # Check for API key
    api_key = os.getenv('GOOGLE_API_KEY')
    if api_key:
        if api_key == 'your_gemini_api_key_here':
            print("⚠️  GOOGLE_API_KEY not set (still using placeholder)")
        else:
            print("✅ GOOGLE_API_KEY is set")
    else:
        print("❌ GOOGLE_API_KEY environment variable not found")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major >= 3 and python_version.minor >= 8:
        print(f"✅ Python version {python_version.major}.{python_version.minor}.{python_version.micro} is compatible")
    else:
        print(f"❌ Python version {python_version.major}.{python_version.minor}.{python_version.micro} is too old (need 3.8+)")
        return False
    
    return True

def test_langchain_functionality():
    """Test basic LangChain functionality"""
    print("\n🔍 Testing LangChain functionality...")
    
    try:
        from langchain.prompts import PromptTemplate
        prompt = PromptTemplate(
            input_variables=["topic"],
            template="Explain {topic} in simple terms."
        )
        print("✅ PromptTemplate creation successful")
    except Exception as e:
        print(f"❌ PromptTemplate test failed: {e}")
        return False
    
    try:
        from langchain.memory import ConversationBufferMemory
        memory = ConversationBufferMemory()
        print("✅ ConversationBufferMemory creation successful")
    except Exception as e:
        print(f"❌ ConversationBufferMemory test failed: {e}")
        return False
    
    return True

def main():
    """Main test function"""
    print("🚀 SmartStudy AI - Project Setup Test")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Run all tests
    if not test_imports():
        all_tests_passed = False
    
    if not test_custom_modules():
        all_tests_passed = False
    
    if not test_environment():
        all_tests_passed = False
    
    if not test_langchain_functionality():
        all_tests_passed = False
    
    # Summary
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 All tests passed! Your project is ready to run.")
        print("\n📋 Next steps:")
        print("1. Set your GOOGLE_API_KEY in the .env file")
        print("2. Run: streamlit run app.py")
        print("3. Open your browser to the provided URL")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure you're in the virtual environment")
        print("2. Install missing dependencies: pip install -r requirements.txt")
        print("3. Check Python version compatibility")
    
    print("\n📚 For more help, see README.md")

if __name__ == "__main__":
    main()
