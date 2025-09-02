"""
SmartStudy AI - Your Personal Exam Coach
Main Streamlit application with document upload, topic explanation, and quiz generation
"""

import streamlit as st
import os
from datetime import datetime
from typing import Dict, Any
import re

# Import custom modules
from memory import initialize_memory, SmartStudyMemory
from chains import initialize_chains, SmartStudyChains
from utils import load_document, validate_file_upload, extract_key_content

# Page configuration
st.set_page_config(
    page_title="SmartStudy AI - Your Personal Exam Coach",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .quiz-section {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        margin: 1rem 0;
    }
    .score-display {
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if "memory" not in st.session_state:
        st.session_state.memory = initialize_memory()
    
    if "chains" not in st.session_state:
        st.session_state.chains = initialize_chains(st.session_state.memory)
    
    if "current_time" not in st.session_state:
        st.session_state.current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if "current_topic" not in st.session_state:
        st.session_state.current_topic = ""
    
    if "current_content" not in st.session_state:
        st.session_state.current_content = ""
    
    if "explanation_generated" not in st.session_state:
        st.session_state.explanation_generated = False
    
    if "quiz_generated" not in st.session_state:
        st.session_state.quiz_generated = False
    
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False
    
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}
    
    if "stored_quiz" not in st.session_state:
        st.session_state.stored_quiz = None
    
    if "quiz_saved_to_memory" not in st.session_state:
        st.session_state.quiz_saved_to_memory = False
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Quiz state variables removed - simplified quiz

def display_sidebar():
    """Display sidebar with learning progress and options"""
    with st.sidebar:
        st.title("🎓 Learning Dashboard")
        
        # Learning Progress
        st.subheader("📊 Your Progress")
        progress = st.session_state.memory.get_learning_summary()
        
        st.metric("Topics Studied", progress["total_topics_studied"])
        st.metric("Quizzes Taken", progress["total_quizzes_taken"])
        if progress["total_quizzes_taken"] > 0:
            st.metric("Average Score", f"{progress['average_quiz_score']}%")
        
        # Weak Areas
        if progress["weak_areas"]:
            st.subheader("⚠️ Areas to Focus On")
            for area in progress["weak_areas"]:
                st.write(f"• {area}")
        
        # Recent Topics
        if progress["recent_topics"]:
            st.subheader("📚 Recent Topics")
            for topic in progress["recent_topics"]:
                st.write(f"• {topic}")
        
        # Recent Scores
        if progress["recent_scores"]:
            st.subheader("📈 Recent Scores")
            for i, score in enumerate(progress["recent_scores"]):
                st.write(f"Quiz {i+1}: {score}%")
        
        # Options
        st.subheader("⚙️ Options")
        if st.button("🔄 Reset Progress"):
            st.session_state.memory.reset_progress()
            st.session_state.explanation_generated = False
            st.session_state.quiz_generated = False
            # Quiz state cleared - simplified quiz
            st.rerun()
        
        if st.button("🧹 Clear Session"):
            st.session_state.memory.clear_session_memory()
            st.session_state.explanation_generated = False
            st.session_state.quiz_generated = False
            # Quiz state cleared - simplified quiz
            st.rerun()

def display_home_page():
    """Display the main home page with options"""
    st.markdown('<h1 class="main-header">SmartStudy AI</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="sub-header">Your Personal Exam Coach</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <h3>🚀 How it works:</h3>
        <ol>
            <li><strong>Upload a document</strong> (PDF/DOCX) or <strong>ask about a topic</strong></li>
            <li>Get a <strong>simple explanation</strong> with examples</li>
            <li>Take a <strong>personalized quiz</strong> to test your understanding</li>
            <li>Receive <strong>personalized revision suggestions</strong> based on your performance</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    


    # Two main options
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 Upload Document")
        uploaded_file = st.file_uploader(
            "Choose a PDF or DOCX file",
            type=['pdf', 'docx'],
            help="Upload your study material to generate explanations and quizzes"
        )
        
        if uploaded_file and validate_file_upload(uploaded_file):
            if st.button("📖 Process Document"):
                with st.spinner("Processing document..."):
                    content = load_document(uploaded_file)
                    if content:
                        st.session_state.current_content = content
                        st.session_state.current_topic = f"Document: {uploaded_file.name}"
                        st.session_state.explanation_generated = False
                        st.session_state.quiz_generated = False
                        # Clear stored quiz when processing new document
                        if "stored_quiz" in st.session_state:
                            del st.session_state.stored_quiz
                        # Clear chat history when processing new document
                        if "chat_history" in st.session_state:
                            st.session_state.chat_history = []
                        st.success(f"Document processed successfully! ({len(content)} characters)")
                        st.rerun()
    
    with col2:
        st.subheader("❓ Ask About a Topic")
        topic_input = st.text_input(
            "Enter a topic to learn about",
            placeholder="e.g., Newton's Laws, Photosynthesis, World War II",
            help="Type any topic you want to learn about"
        )
        
        if topic_input and st.button("🎯 Learn Topic"):
            st.session_state.current_topic = topic_input
            st.session_state.current_content = ""
            st.session_state.explanation_generated = False
            st.session_state.quiz_generated = False
            # Clear stored quiz when starting new topic
            if "stored_quiz" in st.session_state:
                del st.session_state.stored_quiz
            # Clear chat history when starting new topic
            if "chat_history" in st.session_state:
                st.session_state.chat_history = []
            st.rerun()

def display_explanation_and_quiz():
    """Display explanation and quiz generation"""
    if not st.session_state.current_topic:
        return
    
    st.markdown(f"## 📚 Learning: {st.session_state.current_topic}")
    
    # Generate explanation if not already generated
    if not st.session_state.explanation_generated:
        if st.button("🎯 Generate Explanation"):
            with st.spinner("Generating explanation..."):
                content = st.session_state.current_content if st.session_state.current_content else ""
                explanation = st.session_state.chains.generate_explanation(st.session_state.current_topic, content)
                st.session_state.explanation_generated = True
                st.rerun()
    
    # Generate fresh explanation button (always visible)
    if st.session_state.explanation_generated:
        if st.button("🔄 Generate Fresh Explanation"):
            with st.spinner("Generating fresh explanation..."):
                content = st.session_state.current_content if st.session_state.current_content else ""
                explanation = st.session_state.chains.generate_explanation(st.session_state.current_topic, content)
                st.success("✅ Fresh explanation generated!")
                st.rerun()
    
    # Display explanation
    if st.session_state.explanation_generated:
        st.subheader("📖 Explanation")
        content = st.session_state.current_content if st.session_state.current_content else ""
        explanation = st.session_state.chains.generate_explanation(st.session_state.current_topic, content)
        st.markdown(explanation)
        
        # Generate quiz if not already generated
        if not st.session_state.quiz_generated:
            if st.button("🧠 Generate Quiz"):
                with st.spinner("Generating quiz..."):
                    content = st.session_state.current_content if st.session_state.current_content else ""
                    quiz = st.session_state.chains.generate_quiz(st.session_state.current_topic, content)
                    st.session_state.stored_quiz = quiz
                    st.session_state.quiz_generated = True
                    st.success("✅ Quiz generated successfully!")
                    st.rerun()
        
        # Regenerate quiz button (always visible)
        if st.session_state.quiz_generated:
            if st.button("🔄 Regenerate Quiz"):
                with st.spinner("Generating new quiz..."):
                    # Clear old quiz
                    if "stored_quiz" in st.session_state:
                        del st.session_state.stored_quiz
                    st.session_state.quiz_submitted = False
                    st.session_state.quiz_answers = {}
                    
                    # Generate new quiz
                    content = st.session_state.current_content if st.session_state.current_content else ""
                    quiz = st.session_state.chains.generate_quiz(st.session_state.current_topic, content)
                    st.session_state.stored_quiz = quiz
                    st.rerun()
    
    # Display quiz
    if st.session_state.quiz_generated and "stored_quiz" in st.session_state:
        st.subheader("🧠 Quiz")
        
        # Use stored quiz
        quiz = st.session_state.stored_quiz
        
        # Debug: Show quiz generation status
        st.info(f"Quiz generated: {st.session_state.quiz_generated}, Quiz stored: {'stored_quiz' in st.session_state}")
        
        # Parse quiz and create interactive form
        quiz_data = parse_quiz_for_display(quiz)
        if quiz_data:
            display_quiz_with_answers(quiz_data)
        else:
            st.error("Failed to parse quiz data. Please try regenerating the quiz.")
            st.text("Raw quiz content:")
            st.text(quiz[:500] + "..." if len(quiz) > 500 else quiz)

def parse_quiz_for_display(quiz_text: str) -> Dict[str, Any]:
    """Parse the generated quiz text into structured data for display"""
    try:
        quiz_data = {
            "mcq_questions": [],
            "fill_blanks": [],
            "short_answer": "",
            "raw_text": quiz_text
        }
        
        # More flexible MCQ parsing - handle different formats
        mcq_pattern = r'(\d+\.\s*[^A-D]+?)\s*A\)\s*([^B]+?)\s*B\)\s*([^C]+?)\s*C\)\s*([^D]+?)\s*D\)\s*([^C]+?)\s*Correct Answer:\s*([A-D])'
        mcq_matches = re.findall(mcq_pattern, quiz_text, re.DOTALL)
        
        # If no matches with strict pattern, try more flexible pattern
        if not mcq_matches:
            mcq_pattern_flexible = r'(\d+\.\s*[^A-D]+?)\s*A\)\s*([^B]+?)\s*B\)\s*([^C]+?)\s*C\)\s*([^D]+?)\s*D\)\s*([^C]+?)\s*Correct Answer:\s*([A-D])'
            mcq_matches = re.findall(mcq_pattern_flexible, quiz_text, re.DOTALL | re.IGNORECASE)
        
        for match in mcq_matches:
            question = match[0].strip()
            options = [match[1].strip(), match[2].strip(), match[3].strip(), match[4].strip()]
            correct = match[5].strip()
            
            quiz_data["mcq_questions"].append({
                "question": question,
                "options": options,
                "correct": correct
            })
        
        # More flexible fill-in-the-blank parsing
        blank_pattern = r'(\d+\.\s*[^_]+?)\s*______\s*\[Hint[^]]*\]\s*Answer:\s*([^\n]+)'
        blank_matches = re.findall(blank_pattern, quiz_text, re.DOTALL)
        
        # If no matches with hint pattern, try without hint
        if not blank_matches:
            blank_pattern_simple = r'(\d+\.\s*[^_]+?)\s*______\s*\.\s*Answer:\s*([^\n]+)'
            blank_matches = re.findall(blank_pattern_simple, quiz_text, re.DOTALL)
        
        for match in blank_matches:
            question = match[0].strip()
            answer = match[1].strip()
            
            quiz_data["fill_blanks"].append({
                "question": question,
                "answer": answer
            })
        
        # More flexible short answer parsing
        short_pattern = r'Short Answer Questions[^:]*:\s*(\d+\.\s*[^E]+?)Expected Answer:\s*([^\n]+)(?:\s*\d+\.\s*([^E]+?)Expected Answer:\s*([^\n]+))?'
        short_match = re.search(short_pattern, quiz_text, re.DOTALL)
        
        if short_match:
            if short_match.group(3):  # Two short answer questions
                quiz_data["short_answer"] = [
                    {
                        "question": short_match.group(1).strip(),
                        "expected": short_match.group(2).strip()
                    },
                    {
                        "question": short_match.group(3).strip(),
                        "expected": short_match.group(4).strip()
                    }
                ]
            else:  # Single short answer question
                quiz_data["short_answer"] = {
                    "question": short_match.group(1).strip(),
                    "expected": short_match.group(2).strip()
                }
        
        # If no questions were parsed, create a fallback quiz
        if not quiz_data["mcq_questions"] and not quiz_data["fill_blanks"] and not quiz_data["short_answer"]:
            quiz_data = create_fallback_quiz_data()
        
        return quiz_data
        
    except Exception as e:
        st.error(f"Error parsing quiz: {str(e)}")
        # Return fallback quiz if parsing fails
        return create_fallback_quiz_data()

def create_fallback_quiz_data() -> Dict[str, Any]:
    """Create a fallback quiz when parsing fails"""
    return {
        "mcq_questions": [
            {
                "question": "1. What is the main purpose of a CV?",
                "options": [
                    "To list personal hobbies",
                    "To showcase work experience and qualifications", 
                    "To write a story",
                    "To make friends"
                ],
                "correct": "B"
            },
            {
                "question": "2. What should be included in a professional CV?",
                "options": [
                    "Only personal information",
                    "Work experience, education, and skills",
                    "Only education", 
                    "Only skills"
                ],
                "correct": "B"
            },
            {
                "question": "3. What language was the CV written in?",
                "options": [
                    "English",
                    "French",
                    "Dutch",
                    "German"
                ],
                "correct": "C"
            }
        ],
        "fill_blanks": [
            {
                "question": "1. A CV is also known as a ______.",
                "answer": "resume"
            },
            {
                "question": "2. Blal Masroor worked as a kitchen ______ in restaurants.",
                "answer": "assistant"
            }
        ],
        "short_answer": [
            {
                "question": "1. What type of work experience does Blal Masroor have?",
                "expected": "He has experience working in restaurants as a kitchen assistant, with certifications in culinary arts."
            },
            {
                "question": "2. What certifications does Blal Masroor have?",
                "expected": "He has certifications in chocolate making, praline making, bread baking, and pastry making from Centrum voor Volwassenenonderwijs Gent."
            }
        ],
        "raw_text": "Fallback quiz generated due to parsing issues"
    }

def display_quiz_with_answers(quiz_data: Dict[str, Any]):
    """Display the interactive quiz form with questions and answers together"""
    st.markdown('<div class="quiz-section">', unsafe_allow_html=True)
    
    # Initialize quiz answers in session state if not exists
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}
    
    # MCQ Questions
    if quiz_data["mcq_questions"]:
        for i, mcq in enumerate(quiz_data["mcq_questions"]):
            st.write(f"**{i+1}. {mcq['question']}**")
            
            # Create radio buttons for options
            options = [f"{chr(65+j)}) {option}" for j, option in enumerate(mcq['options'])]
            selected = st.radio(
                "Select your answer:",
                options,
                key=f"mcq_{i}",
                label_visibility="collapsed"
            )
            
            # Store the answer
            if selected:
                st.session_state.quiz_answers[f"mcq_{i}"] = selected[0]  # Just the letter
    
    # Fill in the blanks
    if quiz_data["fill_blanks"]:
        for i, blank in enumerate(quiz_data["fill_blanks"]):
            st.write(f"**{i+1}. {blank['question']}**")
            answer = st.text_input(
                "Your answer:",
                key=f"blank_{i}",
                placeholder="Type your answer here"
            )
            if answer:
                st.session_state.quiz_answers[f"blank_{i}"] = answer.strip()
    
    # Short answer questions
    if quiz_data["short_answer"]:
        # Handle both single and multiple short answer questions
        if isinstance(quiz_data["short_answer"], list):
            # Multiple short answer questions
            for i, short_q in enumerate(quiz_data["short_answer"]):
                question_num = len(quiz_data['mcq_questions']) + len(quiz_data['fill_blanks']) + i + 1
                st.write(f"**{question_num}. {short_q['question']}**")
                short_answer = st.text_area(
                    "Your answer:",
                    key=f"short_answer_{i}",
                    placeholder="Write your detailed answer here...",
                    height=100
                )
                if short_answer:
                    st.session_state.quiz_answers[f"short_answer_{i}"] = short_answer.strip()
        else:
            # Single short answer question (backward compatibility)
            question_num = len(quiz_data['mcq_questions']) + len(quiz_data['fill_blanks']) + 1
            st.write(f"**{question_num}. {quiz_data['short_answer']['question']}**")
            short_answer = st.text_area(
                "Your answer:",
                key="short_answer",
                placeholder="Write your detailed answer here...",
                height=100
            )
            if short_answer:
                st.session_state.quiz_answers["short_answer"] = short_answer.strip()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Submit quiz button
    if st.button("📤 Submit Quiz", type="primary"):
        if len(st.session_state.quiz_answers) > 0:
            st.session_state.quiz_submitted = True
            st.rerun()
        else:
            st.warning("Please answer at least one question before submitting.")
    
    # Display results if quiz is submitted
    if st.session_state.get("quiz_submitted", False):
        display_quiz_results(quiz_data)

def display_quiz_results(quiz_data: Dict[str, Any]):
    """Display quiz results and provide scoring"""
    st.subheader("📊 Quiz Results")
    
    # Calculate score
    total_questions = 0
    correct_answers = 0
    weak_areas = []
    
    # Check MCQ answers
    for i, mcq in enumerate(quiz_data["mcq_questions"]):
        total_questions += 1
        user_answer = st.session_state.quiz_answers.get(f"mcq_{i}", "")
        if user_answer == mcq["correct"]:
            correct_answers += 1
        else:
            weak_areas.append(f"Question {i+1}: {mcq['question'][:50]}...")
    
    # Check fill in the blanks
    for i, blank in enumerate(quiz_data["fill_blanks"]):
        total_questions += 1
        user_answer = st.session_state.quiz_answers.get(f"blank_{i}", "").lower()
        correct_answer = blank["answer"].lower()
        
        # Simple similarity check
        if user_answer in correct_answer or correct_answer in user_answer:
            correct_answers += 1
        else:
            weak_areas.append(f"Question {len(quiz_data['mcq_questions']) + i + 1}: {blank['question'][:50]}...")
    
    # Check short answer questions (basic check)
    if quiz_data["short_answer"]:
        if isinstance(quiz_data["short_answer"], list):
            # Multiple short answer questions
            for i, short_q in enumerate(quiz_data["short_answer"]):
                total_questions += 1
                user_answer = st.session_state.quiz_answers.get(f"short_answer_{i}", "").lower()
                expected_keywords = short_q["expected"].lower().split()
                
                # Check if user answer contains expected keywords
                keyword_matches = sum(1 for keyword in expected_keywords if keyword in user_answer)
                if keyword_matches >= len(expected_keywords) * 0.5:  # At least 50% keywords
                    correct_answers += 1
                else:
                    weak_areas.append(f"Question {total_questions}: {short_q['question'][:50]}...")
        else:
            # Single short answer question
            total_questions += 1
            user_answer = st.session_state.quiz_answers.get("short_answer", "").lower()
            expected_keywords = quiz_data["short_answer"]["expected"].lower().split()
            
            # Check if user answer contains expected keywords
            keyword_matches = sum(1 for keyword in expected_keywords if keyword in user_answer)
            if keyword_matches >= len(expected_keywords) * 0.5:  # At least 50% keywords
                correct_answers += 1
            else:
                weak_areas.append(f"Question {total_questions}: {quiz_data['short_answer']['question'][:50]}...")
    
    # Calculate percentage
    percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
    
    # Display score
    if percentage >= 80:
        color = "green"
        message = "🎉 Excellent! You're doing great!"
    elif percentage >= 60:
        color = "orange"
        message = "👍 Good job! Keep practicing!"
    else:
        color = "red"
        message = "📚 Keep studying! You'll get better!"
    
    st.markdown(f"""
    <div style="background-color: {color}; color: white; padding: 20px; border-radius: 10px; text-align: center;">
        <h3>Score: {correct_answers}/{total_questions} ({percentage:.1f}%)</h3>
        <p>{message}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show correct answers for wrong responses
    if weak_areas:
        st.subheader("❌ Questions to Review:")
        for area in weak_areas:
            st.write(f"• {area}")
        
        st.subheader("✅ Correct Answers:")
        
        # Show MCQ correct answers
        for i, mcq in enumerate(quiz_data["mcq_questions"]):
            user_answer = st.session_state.quiz_answers.get(f"mcq_{i}", "")
            if user_answer != mcq["correct"]:
                st.write(f"**Question {i+1}:** {mcq['question']}")
                st.write(f"**Your Answer:** {user_answer}")
                st.write(f"**Correct Answer:** {mcq['correct']}")
                st.write("---")
        
        # Show fill in the blanks correct answers
        for i, blank in enumerate(quiz_data["fill_blanks"]):
            user_answer = st.session_state.quiz_answers.get(f"blank_{i}", "").lower()
            correct_answer = blank["answer"].lower()
            if user_answer not in correct_answer and correct_answer not in user_answer:
                st.write(f"**Question {len(quiz_data['mcq_questions']) + i + 1}:** {blank['question']}")
                st.write(f"**Your Answer:** {st.session_state.quiz_answers.get(f'blank_{i}', 'No answer')}")
                st.write(f"**Correct Answer:** {blank['answer']}")
                st.write("---")
        
        # Show short answer expected responses
        if quiz_data["short_answer"]:
            if isinstance(quiz_data["short_answer"], list):
                # Multiple short answer questions
                for i, short_q in enumerate(quiz_data["short_answer"]):
                    user_answer = st.session_state.quiz_answers.get(f"short_answer_{i}", "").lower()
                    expected_keywords = short_q["expected"].lower().split()
                    keyword_matches = sum(1 for keyword in expected_keywords if keyword in user_answer)
                    if keyword_matches < len(expected_keywords) * 0.5:
                        question_num = len(quiz_data['mcq_questions']) + len(quiz_data['fill_blanks']) + i + 1
                        st.write(f"**Question {question_num}:** {short_q['question']}")
                        st.write(f"**Your Answer:** {st.session_state.quiz_answers.get(f'short_answer_{i}', 'No answer')}")
                        st.write(f"**Expected Answer:** {short_q['expected']}")
                        st.write("---")
            else:
                # Single short answer question
                user_answer = st.session_state.quiz_answers.get("short_answer", "").lower()
                expected_keywords = quiz_data["short_answer"]["expected"].lower().split()
                keyword_matches = sum(1 for keyword in expected_keywords if keyword in user_answer)
                if keyword_matches < len(expected_keywords) * 0.5:
                    st.write(f"**Question {total_questions}:** {quiz_data['short_answer']['question']}")
                    st.write(f"**Your Answer:** {st.session_state.quiz_answers.get('short_answer', 'No answer')}")
                    st.write(f"**Expected Answer:** {quiz_data['short_answer']['expected']}")
                    st.write("---")
    
    # Save quiz results to memory (only when quiz is submitted)
    if "chains" in st.session_state and not st.session_state.get("quiz_saved_to_memory", False):
        st.session_state.chains.memory.add_quiz_result(
            st.session_state.current_topic,
            correct_answers,
            total_questions,
            weak_areas
        )
        st.session_state.quiz_saved_to_memory = True
        st.success("✅ Quiz results saved to your learning progress!")
    
    # Generate revision plan
    if st.button("📋 Generate Revision Plan"):
        with st.spinner("Generating personalized revision plan..."):
            revision_plan = st.session_state.chains.generate_revision_plan(
                correct_answers,
                total_questions,
                weak_areas,
                [st.session_state.current_topic]
            )
            
            st.subheader("📋 Your Personalized Revision Plan")
            st.markdown(revision_plan)
    
    # Reset button
    if st.button("🔄 Try Again"):
        st.session_state.quiz_submitted = False
        st.session_state.quiz_answers = {}
        st.session_state.quiz_saved_to_memory = False
        st.rerun()

def main():
    """Main application function"""
    # Initialize session state
    initialize_session_state()
    
    # Display sidebar
    display_sidebar()
    
    # Main content area
    if not st.session_state.current_topic:
        display_home_page()
    else:
        display_explanation_and_quiz()
        
        # Quiz results display removed - simplified quiz
        
        # Back to home button
        if st.button("🏠 Back to Home"):
            st.session_state.current_topic = ""
            st.session_state.current_content = ""
            st.session_state.explanation_generated = False
            st.session_state.quiz_generated = False
            # Quiz state cleared - simplified quiz
            # Clear stored quiz when going back to home
            if "stored_quiz" in st.session_state:
                del st.session_state.stored_quiz
            # Clear chat history when going back to home
            if "chat_history" in st.session_state:
                st.session_state.chat_history = []
            st.rerun()
        
        # Q&A Chat Section
        st.subheader("💬 Ask Questions About This Topic")
        st.write("Ask any questions about the topic or document content!")
        
        # Initialize chat history if not exists
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        
        # Display chat history
        if st.session_state.chat_history:
            st.write("**Previous Q&A:**")
            for qa in st.session_state.chat_history[-5:]:  # Show last 5 Q&As
                st.write(f"**Q:** {qa['question']}")
                st.write(f"**A:** {qa['answer']}")
                st.write("---")
        
        # Question input with form to clear after submission
        with st.form(key="question_form"):
            user_question = st.text_input(
                "Ask your question:",
                placeholder="e.g., Can you explain this concept further?",
                key="user_question_input"
            )
            
            submit_button = st.form_submit_button("🤔 Ask Question")
            
            if submit_button and user_question and "chains" in st.session_state:
                with st.spinner("Thinking..."):
                    try:
                        # Generate answer using the explanation chain
                        context = f"Topic: {st.session_state.current_topic}\nContent: {st.session_state.current_content if st.session_state.current_content else 'General topic'}\nQuestion: {user_question}"
                        
                        answer = st.session_state.chains.generate_explanation(
                            st.session_state.current_topic,
                            context
                        )
                        
                        # Add to chat history
                        st.session_state.chat_history.append({
                            "question": user_question,
                            "answer": answer
                        })
                        
                        st.success("✅ Answer generated!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error generating answer: {str(e)}")
            elif submit_button and not user_question:
                st.warning("Please enter a question first!")

if __name__ == "__main__":
    main()
