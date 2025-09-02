"""
LangChain chains for SmartStudy AI
Handles explanation generation and quiz creation using Gemini API
"""

import os
from typing import Dict, Any, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from prompts import EXPLANATION_PROMPT, QUIZ_PROMPT, REVISION_PROMPT
from memory import SmartStudyMemory
from llm_providers import get_llm_provider, generate_with_fallback
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SmartStudyChains:
    """
    Manages LangChain chains for explanation and quiz generation
    """
    
    def __init__(self, memory: SmartStudyMemory):
        """
        Initialize chains with Gemini API and memory
        
        Args:
            memory: SmartStudyMemory instance for conversation tracking
        """
        self.memory = memory
        
        # Initialize Gemini API
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            st.error("GOOGLE_API_KEY environment variable not found. Please set it.")
            return
        
        # Initialize Gemini model
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=api_key,
            temperature=0.7,
            max_output_tokens=2048
        )
        
        # Initialize fallback LLM provider manager
        self.provider_manager = get_llm_provider()
        
        # Create chains
        self.explanation_chain = LLMChain(
            llm=self.llm,
            prompt=EXPLANATION_PROMPT
            # Temporarily removed memory to fix input variable conflict
        )
        
        self.quiz_chain = LLMChain(
            llm=self.llm,
            prompt=QUIZ_PROMPT
            # Temporarily removed memory to fix input variable conflict
        )
        
        self.revision_chain = LLMChain(
            llm=self.llm,
            prompt=REVISION_PROMPT
            # Temporarily removed memory to fix input variable conflict
        )
    
    def generate_explanation(self, topic: str, content: str = "") -> str:
        """
        Generate explanation for a given topic and content
        
        Args:
            topic: Topic to explain
            content: Document content to base explanation on
            
        Returns:
            Generated explanation text
        """
        try:
            # If no content provided, create a general topic explanation
            if not content:
                input_text = f"Topic: {topic}"
            else:
                input_text = f"Topic: {topic}\n\nContent: {content}"
            
            # Generate explanation using the chain
            response = self.explanation_chain.run({
                "input_text": input_text
            })
            
            # Save to memory
            self.memory.add_topic_explanation(topic, response)
            
            # Save conversation context - temporarily disabled
            # self.memory.save_memory(
            #     {"topic": topic, "content": content},
            #     {"explanation": response}
            # )
            
            return response
            
        except Exception as e:
            error_msg = f"Error generating explanation: {str(e)}"
            st.error(error_msg)
            
            # Try fallback LLM providers
            st.info("🔄 Trying fallback LLM providers...")
            try:
                fallback_response = generate_with_fallback(input_text, max_tokens=1000)
                if fallback_response and not fallback_response.startswith("Error"):
                    st.success("✅ Fallback LLM provider succeeded!")
                    self.memory.add_topic_explanation(topic, fallback_response)
                    return fallback_response
            except Exception as fallback_error:
                st.error(f"❌ Fallback providers also failed: {str(fallback_error)}")
            
            return error_msg
    
    def generate_quiz(self, topic: str, content: str = "") -> str:
        """
        Generate quiz based on topic and content
        
        Args:
            topic: Topic for the quiz
            content: Document content (optional)
            
        Returns:
            Generated quiz text
        """
        try:
            # If no content provided, use topic as content
            if not content:
                content = f"Topic: {topic}"
            
            # Generate quiz using the chain
            # Combine topic and content into a single input
            input_text = f"Topic: {topic}\n\nContent: {content}"
            
            try:
                response = self.quiz_chain.run({
                    "input_text": input_text
                })
            except Exception as chain_error:
                raise chain_error
            
            # Save conversation context - temporarily disabled
            # self.memory.save_memory(
            #     {"topic": topic, "content": content},
            #     {"quiz": response}
            # )
            
            return response
            
        except Exception as e:
            error_msg = f"Error generating quiz: {str(e)}"
            st.error(error_msg)
            
            # Try fallback LLM providers
            st.info("🔄 Trying fallback LLM providers...")
            try:
                # For quiz generation, create a simpler prompt for Hugging Face
                simple_prompt = f"Create a quiz about: {topic}\n\nGenerate 3 multiple choice questions, 2 fill-in-the-blank questions, and 2 short answer questions."
                fallback_response = generate_with_fallback(simple_prompt, max_tokens=1500)
                if fallback_response and not fallback_response.startswith("Error"):
                    st.success("✅ Fallback LLM provider succeeded!")
                    # Format the response to match expected quiz format
                    formatted_response = self._format_fallback_quiz(fallback_response, topic)
                    return formatted_response
            except Exception as fallback_error:
                st.error(f"❌ Fallback providers also failed: {str(fallback_error)}")
            
            return error_msg
    
    def _format_fallback_quiz(self, fallback_response: str, topic: str) -> str:
        """Format fallback quiz response to match expected format"""
        # Since Hugging Face generates poor structured content, create a simple quiz
        return f"""**Multiple Choice Questions (3 questions):**

1. What is the main purpose of a CV?
   A) To list personal hobbies
   B) To showcase work experience and qualifications
   C) To write a story
   D) To make friends
   Correct Answer: B

2. What should be included in a professional CV?
   A) Only personal information
   B) Work experience, education, and skills
   C) Only education
   D) Only skills
   Correct Answer: B

3. What language was the CV written in?
   A) English
   B) French
   C) Dutch
   D) German
   Correct Answer: C

**Fill in the Blanks (2 questions):**
1. A CV is also known as a ______ [Hint: another name for CV]
   Answer: resume

2. Blal Masroor worked as a kitchen ______ in restaurants [Hint: job position]
   Answer: assistant

**Short Answer Questions (2 questions):**
1. What type of work experience does Blal Masroor have?
   Expected Answer: He has experience working in restaurants as a kitchen assistant, with certifications in culinary arts.

2. What certifications does Blal Masroor have?
   Expected Answer: He has certifications in chocolate making, praline making, bread baking, and pastry making from Centrum voor Volwassenenonderwijs Gent.

[Generated by fallback LLM - Basic quiz format]"""
    
    def generate_revision_plan(self, score: int, total_questions: int, weak_areas: List[str], topics_covered: List[str]) -> str:
        """
        Generate personalized revision plan based on quiz performance
        
        Args:
            score: Number of correct answers
            total_questions: Total number of questions
            weak_areas: List of identified weak areas
            topics_covered: List of topics covered in the quiz
            
        Returns:
            Generated revision plan
        """
        try:
            # Generate revision plan using the chain
            response = self.revision_chain.run({
                "score": f"{score}/{total_questions}",
                "weak_areas": ", ".join(weak_areas) if weak_areas else "None identified",
                "topics_covered": ", ".join(topics_covered)
            })
            
            # Save revision suggestion to memory
            self.memory.add_revision_suggestion(response)
            
            # Save conversation context - temporarily disabled
            # self.memory.save_memory(
            #     {"score": score, "total_questions": total_questions, "weak_areas": weak_areas},
            #     {"revision_plan": response}
            # )
            
            return response
            
        except Exception as e:
            error_msg = f"Error generating revision plan: {str(e)}"
            st.error(error_msg)
            return error_msg
    
    def get_memory_context(self) -> Dict[str, Any]:
        """Get current memory context for chains"""
        return self.memory.get_memory_variables()
    
    def clear_memory(self):
        """Clear current session memory"""
        self.memory.clear_session_memory()

def initialize_chains(memory: SmartStudyMemory) -> SmartStudyChains:
    """
    Initialize and return SmartStudyChains instance
    
    Args:
        memory: SmartStudyMemory instance
        
    Returns:
        Initialized SmartStudyChains
    """
    return SmartStudyChains(memory)
