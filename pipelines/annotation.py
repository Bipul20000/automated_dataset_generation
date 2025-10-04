# pipelines/annotation.py
from typing import List, Dict

def generate_caption(text: str) -> str:
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if not lines:
        return "(no readable text)"
    return lines[0][:200]

def generate_qa_pairs(text: str) -> List[Dict[str, str]]:
    s = text.strip()
    if not s:
        return []
    first = s.split('.')
    return [{"question": "What is the first sentence of the page?", "answer": first[0].strip()}]
