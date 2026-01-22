"""
Base analyzer class for deepfake detection.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Optional
from pathlib import Path


@dataclass
class AnalysisResult:
    """Results from deepfake analysis."""
    
    file_path: str
    file_type: str
    is_likely_ai_generated: bool
    confidence_score: float
    anomalies_detected: Dict[str, Any]
    analysis_details: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "file_path": self.file_path,
            "file_type": self.file_type,
            "is_likely_ai_generated": self.is_likely_ai_generated,
            "confidence_score": self.confidence_score,
            "anomalies_detected": self.anomalies_detected,
            "analysis_details": self.analysis_details,
        }


class BaseAnalyzer(ABC):
    """Base class for all deepfake analyzers."""
    
    def __init__(self, verbose: bool = False):
        """
        Initialize the analyzer.
        
        Args:
            verbose: Enable verbose logging
        """
        self.verbose = verbose
    
    @abstractmethod
    def analyze(self, file_path: str) -> AnalysisResult:
        """
        Analyze a file for AI generation/manipulation.
        
        Args:
            file_path: Path to the file to analyze
            
        Returns:
            AnalysisResult object with analysis results
        """
        pass
    
    @abstractmethod
    def supports_file(self, file_path: str) -> bool:
        """
        Check if this analyzer supports the given file.
        
        Args:
            file_path: Path to check
            
        Returns:
            True if file is supported, False otherwise
        """
        pass
    
    def _log(self, message: str):
        """Log a message if verbose mode is enabled."""
        if self.verbose:
            print(f"[{self.__class__.__name__}] {message}")
