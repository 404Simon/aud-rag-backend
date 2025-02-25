import warnings

import numpy as np
from sentence_transformers import SentenceTransformer

warnings.filterwarnings("ignore", category=FutureWarning)


def generate_embedding(text: str) -> str:
    model = SentenceTransformer("distiluse-base-multilingual-cased-v1")
    query_embedding = model.encode([text])[0]
    return np.array2string(query_embedding, separator=",", precision=6).replace(
        "\n", ""
    )


def generate_embeddings(chunks: list[tuple[str, int]]) -> np.ndarray:
    model = SentenceTransformer("distiluse-base-multilingual-cased-v1")
    embeddings: np.ndarray = model.encode([chunk for chunk, _ in chunks])
    return embeddings
