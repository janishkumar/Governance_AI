"""
Roadmap generation using OpenAI or Groq
"""
import os
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()

USE_GROQ = os.getenv("USE_GROQ", "false").lower() == "true"

if USE_GROQ:
    from groq import Groq
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
else:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


ROADMAP_PROMPT = """You are a career roadmap expert. Generate a clear, structured roadmap for someone who wants to become: {goal}

Create a roadmap with 4-6 phases, each with 2-4 specific, actionable steps.

Return ONLY valid JSON in this exact format:
{{
  "title": "Roadmap to {goal}",
  "phases": [
    {{
      "title": "Phase 1 Name",
      "duration": "3-6 months",
      "steps": [
        "Specific actionable step 1",
        "Specific actionable step 2"
      ]
    }}
  ]
}}

Make it practical, specific, and achievable. Focus on entertainment industry paths when relevant."""


def generate_roadmap(goal: str) -> Dict:
    """Generate a career roadmap using LLM"""
    
    try:
        if USE_GROQ:
            response = client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a career advisor specializing in entertainment careers."},
                    {"role": "user", "content": ROADMAP_PROMPT.format(goal=goal)}
                ],
                temperature=0.7,
                max_tokens=2000
            )
        else:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a career advisor specializing in entertainment careers."},
                    {"role": "user", "content": ROADMAP_PROMPT.format(goal=goal)}
                ],
                temperature=0.7,
                max_tokens=2000
            )
        
        import json
        import re
        
        content = response.choices[0].message.content.strip()
        
        # Remove markdown code fences
        content = re.sub(r'^```json\s*', '', content)
        content = re.sub(r'^```\s*', '', content)
        content = re.sub(r'\s*```$', '', content)
        content = content.strip()
        
        roadmap = json.loads(content)
        return roadmap
        
    except Exception as e:
        print(f"Error generating roadmap: {e}")
        # Fallback roadmap
        return {
            "title": f"Roadmap to {goal}",
            "phases": [
                {
                    "title": "Foundation",
                    "duration": "3-6 months",
                    "steps": ["Learn the basics", "Build foundational skills"]
                },
                {
                    "title": "Development",
                    "duration": "6-12 months",
                    "steps": ["Practice regularly", "Build projects"]
                },
                {
                    "title": "Professional",
                    "duration": "12+ months",
                    "steps": ["Get experience", "Network in the industry"]
                }
            ]
        }