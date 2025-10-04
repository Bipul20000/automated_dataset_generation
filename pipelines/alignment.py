"""Alignment stub: compute embeddings for images and text and compute similarity.

This is a lightweight stub using sentence-transformers for text and CLIP for images.
"""
from typing import List, Tuple
from PIL import Image
import numpy as np


def image_embedding_stub(image_path: str) -> np.ndarray:
    # Placeholder: returns a random vector. Replace with CLIP embedding.
    import numpy as np
    rng = np.random.RandomState(hash(image_path) % (2 ** 32))
    return rng.rand(512)


def text_embedding_stub(text: str) -> np.ndarray:
    # Placeholder: returns a random vector. Replace with sentence-transformers.
    import numpy as np
    rng = np.random.RandomState(abs(hash(text)) % (2 ** 32))
    return rng.rand(512)


def align_images_texts(image_paths: List[str], texts: List[str]) -> List[Tuple[str, str, float]]:
    """Return best-match pairs (image_path, text, score)

    Score is cosine similarity between embeddings.
    """
    import numpy as np
    def cos(a, b):
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10))

    img_embs = [image_embedding_stub(p) for p in image_paths]
    txt_embs = [text_embedding_stub(t) for t in texts]

    pairs = []
    for i, ie in enumerate(img_embs):
        best_j = None
        best_s = -1
        for j, te in enumerate(txt_embs):
            s = cos(ie, te)
            if s > best_s:
                best_s = s
                best_j = j
        pairs.append((image_paths[i], texts[best_j], best_s))
    return pairs


if __name__ == "__main__":
    print("alignment module - import and call align_images_texts")
