"""
Prompt templates for SmartStudy AI
Contains all the prompts used for generating explanations and quizzes
"""

from langchain.prompts import PromptTemplate

# Prompt for generating topic explanations
EXPLANATION_PROMPT = PromptTemplate(
    input_variables=["input_text"],
    template="""You are an expert tutor. Explain the following topic and content:

{input_text}

Your explanation should:
1. Start with a simple definition
2. Use clear, student-friendly language
3. Include 2 practical examples
4. Break down complex concepts into simple parts

If the content is just a topic name (like "Topic: what is programming"), then provide a general explanation of that topic with examples.

If there's specific content provided, focus on explaining that content.

Format your response as:
**Definition:**
[Simple definition]

**Explanation:**
[Clear explanation in simple terms]

**Examples:**
1. [First example]
2. [Second example]

**Key Points:**
- [Key point 1]
- [Key point 2]
- [Key point 3]

Always provide a helpful explanation, whether it's based on specific content or a general topic."""
)

# Prompt for generating quizzes based on topic or document content
QUIZ_PROMPT = PromptTemplate(
    input_variables=["input_text"],
    template="""You are a quiz generator. Based on the following input, create a comprehensive quiz:

    Input: {input_text}

    Generate exactly: 3 MCQs, 2 fill-in-the-blanks, 2 short answer questions (7 total questions)
    
    **Multiple Choice Questions (3 questions):**
    1. [Question 1 with 4 options A, B, C, D]
       A) [Option A]
       B) [Option B] 
       C) [Option C]
       D) [Option D]
       Correct Answer: [Letter of correct option]
    
    2. [Question 2 with 4 options A, B, C, D]
       A) [Option A]
       B) [Option B]
       C) [Option C] 
       D) [Option D]
       Correct Answer: [Letter of correct option]
    
    3. [Question 3 with 4 options A, B, C, D]
       A) [Option A]
       B) [Option B]
       C) [Option C] 
       D) [Option D]
       Correct Answer: [Letter of correct option]

    **Fill in the Blanks (2 questions):**
    1. [Sentence with blank] ______ [Hint: what should go in the blank]
       Answer: [Correct answer]
    
    2. [Sentence with blank] ______ [Hint: what should go in the blank]
       Answer: [Correct answer]

    **Short Answer Questions (2 questions):**
    1. [Question requiring a brief explanation]
       Expected Answer: [Sample answer showing what you're looking for]
    
    2. [Question requiring a brief explanation]
       Expected Answer: [Sample answer showing what you're looking for]

    Keep all questions simple and appropriate for students. Base them on the content provided.

    [UPDATED PROMPT - 7 TOTAL QUESTIONS: 3 MCQs + 2 Fill-in-the-blanks + 2 Short Answer]"""
)

# Prompt for generating revision suggestions
REVISION_PROMPT = PromptTemplate(
    input_variables=["score", "weak_areas", "topics_covered"],
    template="""Based on the student's quiz performance, provide personalized revision suggestions:

    Quiz Score: {score}
    Weak Areas Identified: {weak_areas}
    Topics Covered: {topics_covered}

    Generate a revision plan that:
    1. Addresses the specific weak areas
    2. Suggests study strategies
    3. Recommends practice exercises
    4. Provides encouragement and motivation

    Format as:
    **Performance Analysis:**
    [Brief analysis of performance]

    **Areas to Focus On:**
    [List specific weak areas with explanations]

    **Revision Plan:**
    1. [First revision activity]
    2. [Second revision activity]
    3. [Third revision activity]

    **Study Tips:**
    - [Tip 1]
    - [Tip 2]
    - [Tip 3]

    **Encouragement:**
    [Motivational message]"""
)
