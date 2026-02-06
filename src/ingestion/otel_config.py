"""
OpenTelemetry configuration for ingestion pipelines.

This module initializes the OTEL SDK with an OTLP exporter pointing to
Arize Phoenix (default gRPC endpoint: http://localhost:4317).
"""

from __future__ import annotations

from typing import Optional

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def setup_tracer(service_name: str) -> trace.Tracer:
    """
    Initialize the OpenTelemetry SDK and return a tracer.

    Args:
        service_name: Logical name used for the tracing service.
    """
    resource = Resource.create({"service.name": service_name})
    provider = TracerProvider(resource=resource)
    exporter = OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)
    processor = BatchSpanProcessor(exporter)
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)
    return trace.get_tracer(service_name)