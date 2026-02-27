import pytest
from src.processing.chunker import chunk_text

def test_chunk_text_basic():
    # Create a long text of ~2000 characters
    long_text = "This is a sentence. " * 100
    
    # Assert total length is around 2000
    assert len(long_text) > 1500

    chunks = chunk_text(long_text, max_chars=1500)

    # Check that we got more than one chunk
    assert len(chunks) > 1

    # Check that each chunk is within the limit
    for chunk in chunks:
        assert len(chunk) <= 1500
        assert len(chunk) > 0
