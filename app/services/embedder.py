from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec
from app.utils.content_loader import load_educational_content
from app.config import settings

pc = Pinecone(api_key=settings.PINECONE_API_KEY)

client = OpenAI(api_key=settings.OPENAI_API_KEY)

INDEX_NAME = "learnly-content"

if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region=settings.PINECONE_ENV
        )
    )

index = pc.Index(INDEX_NAME)


def embed_text(text: str) -> list:
    """Return OpenAI embedding for the input text."""
    response = client.embeddings.create(model="text-embedding-ada-002",input=text)
    return response.data[0].embedding


def upsert_documents():
    """Embed and push educational content to Pinecone."""
    content = load_educational_content()
    vectors = [(item["id"], embed_text(item["text"]), item) for item in content]
    index.upsert(vectors=vectors)


def query_similar_docs(query: str, top_k=3) -> list:
    """Given a user query, return top-k relevant content chunks."""
    query_embedding = embed_text(query)
    response = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
    return [match.metadata for match in response.matches]