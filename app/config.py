import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """
    Loads and stores environment variables for external API configurations.
    """
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENV = os.getenv("PINECONE_ENV", "us-east-1")

settings = Settings()