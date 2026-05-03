import re
from typing import List, Dict

def parse_questions_from_text(text: str) -> List[Dict]:
    """
    Extract exam questions from raw PDF text.
    Looks for numbered questions, Q1/Q2 patterns, etc.
    """
    questions = []
    
    # Pattern: Q1, Q2... or 1. 2. or Question 1:
    patterns = [
        r'(?:Q\.?\s*(\d+)[\.\):\s])(.*?)(?=Q\.?\s*\d+[\.\):\s]|$)',
        r'(?:Question\s+(\d+)[\.\):\s])(.*?)(?=Question\s+\d+|$)',
        r'(?:^\s*(\d+)[\.\)]\s)(.*?)(?=^\s*\d+[\.\)]|$)',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.DOTALL | re.MULTILINE | re.IGNORECASE)
        if matches and len(matches) > 1:
            for num, content in matches:
                content = content.strip()
                if len(content) > 20:
                    questions.append({
                        "question_number": int(num),
                        "text": content[:500],
                        "difficulty": classify_difficulty(content),
                        "marks": extract_marks(content),
                    })
            break
    
    # Fallback: split by double newlines and filter meaningful chunks
    if not questions:
        chunks = [c.strip() for c in text.split('\n\n') if len(c.strip()) > 40]
        for i, chunk in enumerate(chunks[:20]):
            if any(kw in chunk.lower() for kw in ['find', 'calculate', 'derive', 'explain', 'state', 'prove', 'show', 'determine', 'evaluate']):
                questions.append({
                    "question_number": i + 1,
                    "text": chunk[:500],
                    "difficulty": classify_difficulty(chunk),
                    "marks": extract_marks(chunk),
                })
    
    return questions


def classify_difficulty(text: str) -> str:
    text_lower = text.lower()
    hard_keywords = ['derive', 'prove', 'analyse', 'critically', 'evaluate', 'synthesis', 'complex', 'advanced']
    easy_keywords = ['state', 'define', 'list', 'name', 'what is', 'write down']
    
    if any(kw in text_lower for kw in hard_keywords):
        return "Hard"
    elif any(kw in text_lower for kw in easy_keywords):
        return "Easy"
    return "Medium"


def extract_marks(text: str) -> int:
    match = re.search(r'\[(\d+)\s*marks?\]|\((\d+)\s*marks?\)', text, re.IGNORECASE)
    if match:
        return int(match.group(1) or match.group(2))
    return 0


def extract_topics_from_text(text: str) -> List[str]:
    """
    Extract likely topic keywords from exam paper text.
    """
    topic_keywords = [
        'thermodynamics', 'quantum mechanics', 'electromagnetic', 'fluid dynamics',
        'calculus', 'algebra', 'mechanics', 'optics', 'nuclear', 'relativity',
        'entropy', 'enthalpy', 'fourier', 'laplace', 'differential equations',
        'probability', 'statistics', 'matrices', 'vectors', 'integration',
        'differentiation', 'kinematics', 'dynamics', 'oscillations', 'waves',
        'circuit', 'transistor', 'semiconductor', 'digital logic', 'algorithms',
        'data structures', 'operating systems', 'networking', 'database',
    ]
    
    found = []
    text_lower = text.lower()
    for topic in topic_keywords:
        if topic in text_lower:
            found.append(topic.title())
    
    return list(set(found))
