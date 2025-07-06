import numpy as np
from google import genai
from google.genai.types import EmbedContentConfig
from superlinked.framework.common.space.embedding.model_based.model_handler import TextModelHandler

class VertexGeminiHandler(TextModelHandler):
    def __init__(self, client: genai.Client):
        self.client = client

def embed(self, texts: list[str]) -> np.ndarray:
    response = client.models.embed_content( 
        model="gemini-embedding-001",
        contents=texts,
        config=EmbedContentConfig(
            task_type="RETRIEVAL_DOCUMENT"
        )
    )
    vectors = [e.values for e in response.embeddings]
    return np.array(vectors, dtype=np.float32)
