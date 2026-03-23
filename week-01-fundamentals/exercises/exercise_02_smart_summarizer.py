"""
Exercise 2: Smart Summarizer
==============================
Difficulty: Beginner | Time: 2 hours

Task:
Build an LLM-powered text analyzer that returns structured output
with: summary, key_terms, and sentiment.

Instructions:
1. Set up your OpenAI API key
2. Create a Pydantic model for the output schema
3. Use .with_structured_output() for guaranteed schema compliance
4. Test with at least 2 different paragraphs
5. Bonus: Add Phoenix tracing to view the LLM call

Run: python exercise_02_smart_summarizer.py
"""

from pydantic import BaseModel, Field
from typing import List, Literal
import os
from dotenv import load_dotenv

load_dotenv("config/.env")
load_dotenv()

# Bonus: Add Phoenix tracing
try:
    from phoenix.otel import register
    from openinference.instrumentation.langchain import LangChainInstrumentor
    
    tracer_provider = register(
        project_name="exercise-02-smart-summarizer",
        endpoint="http://127.0.0.1:4317"
    )
    LangChainInstrumentor().instrument(tracer_provider=tracer_provider)
    print("Phoenix tracing enabled")
except ImportError:
    print("Phoenix not available, tracing disabled")


class TextAnalysis(BaseModel):
    """Define the output schema here."""
    summary: str = Field(description="A concise summary of the text in 2-3 sentences")
    key_terms: List[str] = Field(description="List of 3-5 key terms or concepts from the text")
    sentiment: Literal["positive", "negative", "neutral"] = Field(description="Overall sentiment of the text")


def analyze_text(text: str) -> TextAnalysis:
    """Analyze text and return structured insights.

    Args:
        text: The text to analyze

    Returns:
        TextAnalysis with summary, key_terms, and sentiment
    """
    # Use Groq since OpenAI quota is exceeded
    from langchain_groq import ChatGroq
    
    # Initialize ChatGroq with a capable model
    llm = ChatGroq(model="llama-3.3-70b-versatile")
    
    # Use .with_structured_output(TextAnalysis)
    structured_llm = llm.with_structured_output(TextAnalysis)
    
    # Create a clear prompt asking for summary, key terms, and sentiment
    prompt = f"""
    Analyze the following text and provide:
    1. A concise summary in 2-3 sentences
    2. 3-5 key terms or concepts
    3. Overall sentiment (positive, negative, or neutral)
    
    Text to analyze:
    {text}
    """
    
    # Return the structured result
    return structured_llm.invoke(prompt)


if __name__ == "__main__":
    sample = """
    AI agents represent a paradigm shift in software development.
    Unlike traditional programs, agents can reason about their
    environment, use tools autonomously, and improve through
    self-reflection. Companies like Klarna have deployed agents
    that handle millions of customer interactions.
    """

    print("Analyzing text...")
    result = analyze_text(sample)
    print(f"Summary: {result.summary}")
    print(f"Key Terms: {result.key_terms}")
    print(f"Sentiment: {result.sentiment}")
    
    # Test with a second paragraph
    print("\n" + "="*50)
    print("Testing with second paragraph...")
    second_sample = """
    The rapid advancement of artificial intelligence has raised significant concerns
    about job displacement and ethical implications. While AI can automate routine
    tasks and improve efficiency, it may also lead to widespread unemployment in
    certain sectors. Critics argue that without proper regulation, AI systems could
    perpetuate existing biases and privacy violations.
    """
    
    result2 = analyze_text(second_sample)
    print(f"Summary: {result2.summary}")
    print(f"Key Terms: {result2.key_terms}")
    print(f"Sentiment: {result2.sentiment}")
