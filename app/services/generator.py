from openai import OpenAI
import json
from app.config import settings
from app.schemas import CurriculumRequest
from app.services.embedder import query_similar_docs

client = OpenAI(api_key=settings.OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are an AI assistant that creates personalized learning paths. 
Return the path as a JSON object with this exact structure:
{
  "Learning Path": {
    "Introduction": {
      "Courses": [
        { "Course Name": "...", "Link": "..." }
      ]
    },
    "Core Topics": {
      "Courses": [
        ...
      ]
    }
  }
}
"""


def generate_learning_path(request: CurriculumRequest):
    """
    Generates a structured learning path based on user goal and known skills.

    Args:
        request (CurriculumRequest): User input containing goal and optionally known skills.

    Returns:
        dict: Parsed JSON learning path if successful, else raw response with error.
    """
    context_docs = query_similar_docs(request.goal, top_k=3)
    context_text = "\n".join(
        f"Title: {doc['title']}\nSummary: {doc['text']}\nLink: {doc['url']}" for doc in context_docs
    )
    prompt = f"""
    Goal: {request.goal}
    Known Skills: {request.known_skills or "None"}

    Use the following background content to improve the learning path:
    {context_text}

    Generate a structured learning path.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )

    raw_content = response.choices[0].message.content
    
    try:
        parsed = json.loads(raw_content)
        return parsed
    except json.JSONDecodeError:
        return {"error": "Failed to parse response", "raw": raw_content}