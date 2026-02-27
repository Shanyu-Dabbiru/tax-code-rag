import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from src.api.main import app
from src.api.retriever import ChunkResponse

client = TestClient(app)

@patch("src.api.main.retriever")
def test_search_endpoint_valid(mock_retriever):
    # Setup mock return value
    mock_retriever.search.return_value = [
        ChunkResponse(
            chunk_id="123e4567-e89b-12d3-a456-426614174000",
            text="Mocked tax chunk text for testing.",
            title="Section 162: Trade or business expenses",
            hierarchy=["Title 26", "Subtitle A", "Chapter 1"],
            section_number="26 U.S.C. § 162",
            score=0.98
        )
    ]

    # Perform the test request
    response = client.post("/search", json={"query": "business expenses", "top_k": 3})

    # Assert response
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) == 1
    
    first_result = data["results"][0]
    assert first_result["chunk_id"] == "123e4567-e89b-12d3-a456-426614174000"
    assert first_result["section_number"] == "26 U.S.C. § 162"
    
    # Verify the mock was called with correct arguments
    mock_retriever.search.assert_called_once_with(query="business expenses", top_k=3)


def test_search_endpoint_invalid():
    # Case 1: Missing query parameter completely -> Should be 422 Unprocessable Entity
    response = client.post("/search", json={"top_k": 5})
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data
    
    # Case 2: Empty query string -> Custom 400 error in main.py
    response = client.post("/search", json={"query": "", "top_k": 5})
    assert response.status_code == 400
    assert response.json()["detail"] == "Query cannot be empty."

    # Case 3: Invalid top_k (less than 1) -> Pydantic validation error (422)
    response = client.post("/search", json={"query": "tax", "top_k": 0})
    assert response.status_code == 422
