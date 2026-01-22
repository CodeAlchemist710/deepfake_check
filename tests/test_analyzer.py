"""
Tests for the main DeepfakeAnalyzer.
"""

import pytest
import tempfile
from pathlib import Path
from deepfake_check import DeepfakeAnalyzer
from deepfake_check.base import AnalysisResult


def test_analyzer_initialization():
    """Test DeepfakeAnalyzer initialization."""
    analyzer = DeepfakeAnalyzer(verbose=True)
    assert analyzer.verbose is True
    assert analyzer.audio_analyzer is None
    assert analyzer.video_analyzer is None


def test_unsupported_file_format():
    """Test handling of unsupported file formats."""
    analyzer = DeepfakeAnalyzer()
    
    with tempfile.NamedTemporaryFile(suffix=".unsupported") as tmp:
        with pytest.raises(ValueError, match="Unsupported file format"):
            analyzer.analyze(tmp.name)


def test_file_not_found():
    """Test handling of non-existent files."""
    analyzer = DeepfakeAnalyzer()
    
    with pytest.raises(FileNotFoundError):
        analyzer.analyze("/non/existent/file.mp3")


def test_save_report():
    """Test saving analysis report to JSON."""
    analyzer = DeepfakeAnalyzer()
    
    result = AnalysisResult(
        file_path="/test/file.mp3",
        file_type="audio",
        is_likely_ai_generated=True,
        confidence_score=0.8,
        anomalies_detected={"test": "anomaly"},
        analysis_details={"test": "details"}
    )
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
        tmp_path = tmp.name
    
    try:
        analyzer.save_report(result, tmp_path)
        
        # Verify file was created and contains valid JSON
        import json
        with open(tmp_path, 'r') as f:
            data = json.load(f)
        
        assert data["file_path"] == "/test/file.mp3"
        assert data["file_type"] == "audio"
        assert data["is_likely_ai_generated"] is True
        assert data["confidence_score"] == 0.8
    finally:
        Path(tmp_path).unlink(missing_ok=True)
