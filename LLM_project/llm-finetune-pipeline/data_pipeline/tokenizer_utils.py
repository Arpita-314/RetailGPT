"""Tokenization helpers and sequence formatting.
Placeholder utilities — wire your tokenizer (HuggingFace, sentencepiece, etc.) here.
"""

from typing import List


def tokenize_examples(texts: List[str], tokenizer, max_length: int):
    """Tokenize and format into fixed-length sequences."""
    return tokenizer(texts, truncation=True, padding='max_length', max_length=max_length)
