import re
from typing import List

def chunk_text(text: str, max_chars: int = 1500) -> List[str]:
    """
    Splits text into chunks strictly under max_chars.
    Falls back from paragraphs to sentences to words to characters if necessary.
    """
    if not text:
        return []

    # If the whole text is small enough, return it.
    if len(text) <= max_chars:
        return [text]

    chunks = []
    
    # Simple recursive splitting approach
    def add_chunk(current_chunk: str):
        if len(current_chunk) <= max_chars:
            chunks.append(current_chunk)
        else:
            # Fallback to smaller split delimiters
            _split_and_add(current_chunk)

    def _split_and_add(text_to_split: str):
        # Determine best delimiter
        if '\n\n' in text_to_split:
            parts = text_to_split.split('\n\n')
            delimeter = '\n\n'
        elif '\n' in text_to_split:
            parts = text_to_split.split('\n')
            delimeter = '\n'
        elif '. ' in text_to_split:
            parts = text_to_split.split('. ')
            delimeter = '. '
        elif ' ' in text_to_split:
            parts = text_to_split.split(' ')
            delimeter = ' '
        else:
            # No delimiters, hard chop
            parts = [text_to_split[i:i+max_chars] for i in range(0, len(text_to_split), max_chars)]
            for p in parts:
                add_chunk(p)
            return

        current = ""
        for i, part in enumerate(parts):
            # re-attach delimiter for all but last part
            piece = part + delimeter if i < len(parts) - 1 else part
            
            if len(current) + len(piece) <= max_chars:
                current += piece
            else:
                if current:
                    chunks.append(current)
                if len(piece) <= max_chars:
                    current = piece
                else:
                    # the piece itself is too big, need to recursive split it
                    current = ""
                    _split_and_add(piece)
        if current:
            chunks.append(current)

    _split_and_add(text)
    
    return [c.strip() for c in chunks if c.strip()]
