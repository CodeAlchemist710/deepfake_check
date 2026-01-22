"""
Tests for the base analyzer module.
"""

import pytest
from deepfake_check.base import BaseAnalyzer, AnalysisResult


def test_analysis_result_creation():
    """Test AnalysisResult dataclass creation."""
    result = AnalysisResult(
        file_path="/path/to/file.mp3",
        file_type="audio",
        is_likely_ai_generated=True,
        confidence_score=0.75,
        anomalies_detected={"test_anomaly": {"detected": True}},
        analysis_details={"test": "details"}
    )
    
    assert result.file_path == "/path/to/file.mp3"
    assert result.file_type == "audio"
    assert result.is_likely_ai_generated is True
    assert result.confidence_score == 0.75


def test_analysis_result_to_dict():
    """Test AnalysisResult conversion to dictionary."""
    result = AnalysisResult(
        file_path="/path/to/file.mp3",
        file_type="audio",
        is_likely_ai_generated=False,
        confidence_score=0.25,
        anomalies_detected={},
        analysis_details={}
    )
    
    result_dict = result.to_dict()
    
    assert isinstance(result_dict, dict)
    assert result_dict["file_path"] == "/path/to/file.mp3"
    assert result_dict["file_type"] == "audio"
    assert result_dict["is_likely_ai_generated"] is False
    assert result_dict["confidence_score"] == 0.25


class TestAnalyzer(BaseAnalyzer):
    """Concrete implementation for testing."""
    
    def analyze(self, file_path: str):
        return AnalysisResult(
            file_path=file_path,
            file_type="test",
            is_likely_ai_generated=False,
            confidence_score=0.0,
            anomalies_detected={},
            analysis_details={}
        )
    
    def supports_file(self, file_path: str) -> bool:
        return file_path.endswith(".test")


def test_base_analyzer_verbose():
    """Test verbose mode in base analyzer."""
    analyzer = TestAnalyzer(verbose=True)
    assert analyzer.verbose is True
    
    analyzer = TestAnalyzer(verbose=False)
    assert analyzer.verbose is False


def test_base_analyzer_supports_file():
    """Test file support checking."""
    analyzer = TestAnalyzer()
    assert analyzer.supports_file("file.test") is True
    assert analyzer.supports_file("file.other") is False
