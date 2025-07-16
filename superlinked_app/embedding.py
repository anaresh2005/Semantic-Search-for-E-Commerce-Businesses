import numpy as np
from google import genai
from google.genai.types import EmbedContentConfig
from superlinked.framework.common.space.embedding.model_based.model_handler import (
    TextModelHandler,
)
from superlinked_app.config import settings


class VertexGeminiHandler(TextModelHandler):
    def __init__(self, client: genai.Client):
        genai.configure(api_key=settings.GEMINI_API_KEY.get_secret_value())
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
