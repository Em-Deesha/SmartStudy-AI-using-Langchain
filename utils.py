"""
Utility functions for SmartStudy AI
Handles document loading, text extraction, and text splitting
"""

import os
from typing import List, Optional
from langchain_community.document_loaders import PyPDFLoader, UnstructuredWordDocumentLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document
import streamlit as st

def load_document(file) -> Optional[str]:
    """
    Load and extract text from uploaded document (PDF or DOCX)
    
    Args:
        file: Streamlit uploaded file object
        
    Returns:
        Extracted text as string or None if error
    """
    try:
        # Get file extension
        file_extension = os.path.splitext(file.name)[1].lower()
        
        if file_extension == '.pdf':
            # Save PDF temporarily and load
            with open("temp.pdf", "wb") as f:
                f.write(file.getbuffer())
            
            loader = PyPDFLoader("temp.pdf")
            documents = loader.load()
            
            # Clean up temp file
            os.remove("temp.pdf")
            
        elif file_extension == '.docx':
            # Save DOCX temporarily and load
            with open("temp.docx", "wb") as f:
                f.write(file.getbuffer())
            
            loader = UnstructuredWordDocumentLoader("temp.docx")
            documents = loader.load()
            
            # Clean up temp file
            os.remove("temp.docx")
            
        else:
            st.error("Unsupported file format. Please upload a PDF or DOCX file.")
            return None
        
        # Extract text from documents
        text = ""
        for doc in documents:
            text += doc.page_content + "\n"
        
        return text.strip()
        
    except Exception as e:
        st.error(f"Error loading document: {str(e)}")
        return None

def split_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
    """
    Split text into chunks for processing
    
    Args:
        text: Input text to split
        chunk_size: Maximum size of each chunk
        chunk_overlap: Overlap between consecutive chunks
        
    Returns:
        List of text chunks
    """
    try:
        # Create text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Split text
        chunks = text_splitter.split_text(text)
        
        return chunks
        
    except Exception as e:
        st.error(f"Error splitting text: {str(e)}")
        return [text]  # Return original text as single chunk

def extract_key_content(text: str, max_length: int = 2000) -> str:
    """
    Extract key content from text, limiting length for API calls
    
    Args:
        text: Input text
        max_length: Maximum length of extracted content
        
    Returns:
        Truncated text content
    """
    if len(text) <= max_length:
        return text
    
    # Take first part and last part to maintain context
    half_length = max_length // 2
    return text[:half_length] + "\n\n... [Content truncated for processing] ...\n\n" + text[-half_length:]

def validate_file_upload(file) -> bool:
    """
    Validate uploaded file format and size
    
    Args:
        file: Streamlit uploaded file object
        
    Returns:
        True if valid, False otherwise
    """
    if file is None:
        return False
    
    # Check file extension
    allowed_extensions = ['.pdf', '.docx']
    file_extension = os.path.splitext(file.name)[1].lower()
    
    if file_extension not in allowed_extensions:
        st.error(f"Unsupported file format: {file_extension}. Please upload a PDF or DOCX file.")
        return False
    
    # Check file size (max 10MB)
    max_size = 10 * 1024 * 1024  # 10MB in bytes
    if file.size > max_size:
        st.error(f"File too large: {file.size / (1024*1024):.1f}MB. Maximum size is 10MB.")
        return False
    
    return True
