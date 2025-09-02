"""
Simplified LLM Provider for SmartStudy AI
Only uses Hugging Face as fallback when Gemini fails
"""

import streamlit as st
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch

class HuggingFaceProvider:
    """Hugging Face LLM Provider - Simple and Clean"""
    
    def __init__(self):
        self.model_name = "distilgpt2"
        self.tokenizer = None
        self.model = None
        self.pipeline = None
        self._load_model()
    
    def _load_model(self):
        """Load Hugging Face model"""
        try:
            st.info("🔄 Loading Hugging Face model... This may take a moment.")
            
            # Use a smaller, faster model
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else None
            )
            
            # Add padding token if not present
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            self.pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                max_length=512,
                do_sample=True,
                temperature=0.7,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            st.success("✅ Hugging Face model loaded successfully!")
            
        except Exception as e:
            st.error(f"❌ Failed to load Hugging Face model: {e}")
            raise Exception(f"Failed to load Hugging Face model: {e}")
    
    def generate_text(self, prompt: str, max_tokens: int = 1000) -> str:
        """Generate text using Hugging Face model"""
        try:
            # Truncate prompt if too long
            max_prompt_length = 200
            if len(prompt) > max_prompt_length:
                prompt = prompt[:max_prompt_length] + "..."
            
            # Generate text
            result = self.pipeline(
                prompt,
                max_length=min(max_tokens, 512),
                num_return_sequences=1,
                truncation=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            generated_text = result[0]['generated_text']
            
            # Remove the original prompt from the generated text
            if generated_text.startswith(prompt):
                generated_text = generated_text[len(prompt):].strip()
            
            # Clean up the text
            generated_text = self._clean_text(generated_text)
            
            return generated_text if generated_text else "I apologize, but I couldn't generate a proper response. Please try again."
            
        except Exception as e:
            return f"Error generating text with Hugging Face: {str(e)}"
    
    def _clean_text(self, text: str) -> str:
        """Clean generated text"""
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove incomplete sentences at the end
        sentences = text.split('.')
        if len(sentences) > 1 and len(sentences[-1].strip()) < 10:
            text = '.'.join(sentences[:-1]) + '.'
        
        return text.strip()

# Global Hugging Face provider instance
_huggingface_provider = None

def get_llm_provider() -> HuggingFaceProvider:
    """Get the Hugging Face provider instance"""
    global _huggingface_provider
    if _huggingface_provider is None:
        _huggingface_provider = HuggingFaceProvider()
    return _huggingface_provider

def generate_with_fallback(prompt: str, max_tokens: int = 1000) -> str:
    """Generate text using Hugging Face as fallback"""
    provider = get_llm_provider()
    return provider.generate_text(prompt, max_tokens)