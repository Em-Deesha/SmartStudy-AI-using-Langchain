"""
Memory management for SmartStudy AI
Handles conversation memory and learning progress tracking
"""

from langchain.memory import ConversationBufferMemory
from langchain.schema import BaseMemory
from typing import Dict, Any, List
import streamlit as st

class SmartStudyMemory:
    """
    Custom memory class that combines conversation buffer and summary memory
    for tracking learning progress and conversation history
    """
    
    def __init__(self):
        """Initialize memory components"""
        # Buffer memory for current session
        self.buffer_memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Summary memory for long-term learning progress
        # Note: ConversationSummaryMemory requires an LLM, so we'll use a simpler approach
        self.summary_memory = None  # We'll implement custom summary logic
        
        # Custom tracking for learning progress
        self.learning_progress = {
            "topics_explained": [],
            "quiz_scores": [],
            "weak_areas": [],
            "strengths": [],
            "revision_suggestions": []
        }
    
    def add_topic_explanation(self, topic: str, explanation: str):
        """Add a new topic explanation to memory"""
        # Check if topic already exists (case-insensitive)
        existing_topics = [t["topic"].lower() for t in self.learning_progress["topics_explained"]]
        
        if topic.lower() not in existing_topics:
            self.learning_progress["topics_explained"].append({
                "topic": topic,
                "explanation": explanation,
                "timestamp": st.session_state.get("current_time", "Unknown")
            })
        else:
            # Update existing topic with new explanation
            for t in self.learning_progress["topics_explained"]:
                if t["topic"].lower() == topic.lower():
                    t["explanation"] = explanation
                    t["timestamp"] = st.session_state.get("current_time", "Unknown")
                    break
    
    def add_quiz_result(self, topic: str, score: int, total_questions: int, weak_areas: List[str]):
        """Add quiz results to memory"""
        quiz_result = {
            "topic": topic,
            "score": score,
            "total_questions": total_questions,
            "percentage": (score / total_questions) * 100,
            "weak_areas": weak_areas,
            "timestamp": st.session_state.get("current_time", "Unknown")
        }
        
        self.learning_progress["quiz_scores"].append(quiz_result)
        
        # Update weak areas tracking
        for area in weak_areas:
            if area not in self.learning_progress["weak_areas"]:
                self.learning_progress["weak_areas"].append(area)
    
    def add_revision_suggestion(self, suggestion: str):
        """Add revision suggestion to memory"""
        self.learning_progress["revision_suggestions"].append({
            "suggestion": suggestion,
            "timestamp": st.session_state.get("current_time", "Unknown")
        })
    
    def get_learning_summary(self) -> Dict[str, Any]:
        """Get a summary of learning progress"""
        # Remove duplicate topics (keep only unique ones)
        unique_topics = []
        seen_topics = set()
        for topic in self.learning_progress["topics_explained"]:
            if topic["topic"].lower() not in seen_topics:
                unique_topics.append(topic)
                seen_topics.add(topic["topic"].lower())
        
        # Update the list with unique topics
        self.learning_progress["topics_explained"] = unique_topics
        
        total_topics = len(unique_topics)
        total_quizzes = len(self.learning_progress["quiz_scores"])
        
        if total_quizzes > 0:
            avg_score = sum(q["percentage"] for q in self.learning_progress["quiz_scores"]) / total_quizzes
        else:
            avg_score = 0
        
        return {
            "total_topics_studied": total_topics,
            "total_quizzes_taken": total_quizzes,
            "average_quiz_score": round(avg_score, 1),
            "weak_areas": self.learning_progress["weak_areas"],
            "recent_topics": [t["topic"] for t in unique_topics[-5:]],  # Last 5 unique topics
            "recent_scores": [q["percentage"] for q in self.learning_progress["quiz_scores"][-5:]]  # Last 5 scores
        }
    
    def get_topic_history(self) -> List[Dict[str, Any]]:
        """Get history of explained topics"""
        return self.learning_progress["topics_explained"]
    
    def get_quiz_history(self) -> List[Dict[str, Any]]:
        """Get history of quiz results"""
        return self.learning_progress["quiz_scores"]
    
    def get_weak_areas(self) -> List[str]:
        """Get list of identified weak areas"""
        return self.learning_progress["weak_areas"]
    
    def clear_session_memory(self):
        """Clear current session buffer memory"""
        self.buffer_memory.clear()
    
    def get_memory_variables(self) -> Dict[str, Any]:
        """Get memory variables for LangChain chains"""
        buffer_vars = self.buffer_memory.load_memory_variables({})
        
        # Since we're not using ConversationSummaryMemory, we'll create a simple summary
        summary_vars = {
            "learning_summary": self._generate_learning_summary()
        }
        
        return {
            **buffer_vars,
            **summary_vars,
            "learning_progress": self.learning_progress
        }
    
    def save_memory(self, inputs: Dict[str, Any], outputs: Dict[str, Any]):
        """Save conversation to both memory types"""
        self.buffer_memory.save_context(inputs, outputs)
        # Note: We're not using ConversationSummaryMemory, so we just track in learning_progress
    
    def _generate_learning_summary(self) -> str:
        """Generate a simple learning summary from progress data"""
        if not self.learning_progress["topics_explained"]:
            return "No learning activity yet. Start by asking about a topic or uploading a document!"
        
        topics_count = len(self.learning_progress["topics_explained"])
        quizzes_count = len(self.learning_progress["quiz_scores"])
        
        summary = f"Learning Progress: Studied {topics_count} topics, took {quizzes_count} quizzes."
        
        if self.learning_progress["weak_areas"]:
            summary += f" Areas to focus on: {', '.join(self.learning_progress['weak_areas'][:3])}"
        
        return summary
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the current conversation"""
        return self._generate_learning_summary()
    
    def reset_progress(self):
        """Reset all learning progress (for testing purposes)"""
        self.learning_progress = {
            "topics_explained": [],
            "quiz_scores": [],
            "weak_areas": [],
            "strengths": [],
            "revision_suggestions": []
        }
        self.clear_session_memory()
        # Note: summary_memory is None, so no need to clear it
    
    def clear_duplicates(self):
        """Clear duplicate topics and quiz results"""
        # Clear duplicate topics
        unique_topics = []
        seen_topics = set()
        for topic in self.learning_progress["topics_explained"]:
            if topic["topic"].lower() not in seen_topics:
                unique_topics.append(topic)
                seen_topics.add(topic["topic"].lower())
        
        self.learning_progress["topics_explained"] = unique_topics
        
        # Clear duplicate quiz results (keep only latest for each topic)
        unique_quizzes = []
        seen_quiz_topics = set()
        for quiz in reversed(self.learning_progress["quiz_scores"]):  # Start from latest
            if quiz["topic"].lower() not in seen_quiz_topics:
                unique_quizzes.append(quiz)
                seen_quiz_topics.add(quiz["topic"].lower())
        
        self.learning_progress["quiz_scores"] = list(reversed(unique_quizzes))  # Restore order

def initialize_memory() -> SmartStudyMemory:
    """Initialize and return a new memory instance"""
    return SmartStudyMemory()
