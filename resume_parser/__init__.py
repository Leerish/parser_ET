# resume_parser/__init__.py

from .readers import parse_resume
from .extractors import parse_information

__all__ = ["parse_resume", "parse_information"]
