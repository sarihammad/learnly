# Learnly

Learnly is an AI-powered personalized learning path generator built with FastAPI and OpenAI’s GPT models. It creates structured, goal-oriented learning curriculums tailored to a user’s background and interests by combining LLMs with vector search for relevant content retrieval.

## Features

- Generate personalized learning paths based on user goals and known skills
- Supports JSON-structured output for easy integration
- Uses OpenAI GPT for curriculum generation and Pinecone vector database for retrieval-augmented generation (RAG)
- Modular backend built with FastAPI
- Dockerized for easy deployment

## How to Run

1. Build the Docker image:

```bash
docker build -t learnly .
```

2. Run the container:

```bash
docker run -p 8000:8000 learnly
```

Make sure your .env file contains your OpenAI and Pinecone API keys.

3. Make a test request:

```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"goal": "Learn AI for finance", "known_skills": "Python, linear algebra"}'
```

You will receive a JSON response with a structured personalized learning path.
