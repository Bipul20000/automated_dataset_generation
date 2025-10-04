"""Annotation generator stub: produce captions and simple Q&A from text
"""
from typing import List, Dict


def generate_caption(text: str) -> str:
    # Very simple heuristic caption
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if not lines:
        return "(no readable text)"
    return lines[0][:200]


def generate_qa_pairs(text: str) -> List[Dict[str, str]]:
    # Stub: create one question asking for the first sentence.
    s = text.strip()
    if not s:
        return []
    first = s.split('.')
    q = f"What is the first sentence of the page?"
    a = first[0].strip()
    return [{"question": q, "answer": a}]


if __name__ == "__main__":
    print("annotation module - generate_caption / generate_qa_pairs")
