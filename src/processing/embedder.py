"""Embedding utilities for tax code content."""

from __future__ import annotations

from typing import List

from opentelemetry import trace
from sentence_transformers import SentenceTransformer


class TaxEmbedder:
	"""Embed tax code text using a sentence-transformers model."""

	def __init__(self) -> None:
		self.model_name = "BAAI/bge-small-en-v1.5"
		self.device = "cpu"
		self._model = SentenceTransformer(self.model_name, device=self.device)
		self._tracer = trace.get_tracer(__name__)

	def get_embedding_dim(self) -> int:
		"""Get the embedding dimension (vector size) of the model."""
		return self._model.get_sentence_embedding_dimension()

	def embed_text(self, text: str) -> List[float]:
		"""Embed a single text string into a vector."""
		with self._tracer.start_as_current_span("embed_text") as span:
			span.set_attribute("text_length", len(text))
			span.set_attribute("model_name", self.model_name)
			span.set_attribute("device", self.device)
			vector = self._model.encode(
				text,
				convert_to_numpy=True,
				show_progress_bar=False,
			)
			return vector.tolist()

	def embed_batch(self, texts: List[str]) -> List[List[float]]:
		"""Embed a batch of text strings into vectors."""
		with self._tracer.start_as_current_span("embed_batch") as span:
			span.set_attribute("batch_size", len(texts))
			span.set_attribute("model_name", self.model_name)
			span.set_attribute("device", self.device)
			vectors = self._model.encode(
				texts,
				batch_size=32,
				convert_to_numpy=True,
				show_progress_bar=False,
			)
			return vectors.tolist()
