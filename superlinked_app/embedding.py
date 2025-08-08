import numpy as np
from google import genai
from google.genai.types import EmbedContentConfig
from superlinked_app.config import settings


class GeminiHandler:
    def __init__(self, client: genai.Client):
        self.model_id = settings.GEMINI_MODEL_ID
        self.client = client

    def embed(self, texts: list[str]) -> np.ndarray:
        response = self.client.models.embed_content(
            model=self.model_id,
            contents=texts,
            config=EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
        )
        vectors = [e.values for e in response.embeddings]
        return np.array(vectors, dtype=np.float32)
