"""
Main deepfake analyzer that coordinates audio and video analysis.
"""

from pathlib import Path
from typing import Optional, Union
import json

from .base import AnalysisResult
from .audio.analyzer import AudioAnalyzer
from .video.analyzer import VideoAnalyzer


class DeepfakeAnalyzer:
    """
    Main analyzer for detecting AI-generated content in audio and video files.
    """
    
    def __init__(self, verbose: bool = False):
        """
        Initialize the deepfake analyzer.
        
        Args:
            verbose: Enable verbose logging
        """
        self.verbose = verbose
        self.audio_analyzer = None
        self.video_analyzer = None
    
    def _get_audio_analyzer(self) -> AudioAnalyzer:
        """Lazy initialization of audio analyzer."""
        if self.audio_analyzer is None:
            self.audio_analyzer = AudioAnalyzer(verbose=self.verbose)
        return self.audio_analyzer
    
    def _get_video_analyzer(self) -> VideoAnalyzer:
        """Lazy initialization of video analyzer."""
        if self.video_analyzer is None:
            self.video_analyzer = VideoAnalyzer(verbose=self.verbose)
        return self.video_analyzer
    
    def analyze(self, file_path: str) -> AnalysisResult:
        """
        Analyze a file for AI generation/manipulation.
        
        Automatically detects file type and uses appropriate analyzer.
        
        Args:
            file_path: Path to the file to analyze
            
        Returns:
            AnalysisResult with analysis findings
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is not supported
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Determine file type and use appropriate analyzer
        suffix = path.suffix.lower()
        
        # Check if it's an audio file
        if suffix in AudioAnalyzer.SUPPORTED_FORMATS:
            analyzer = self._get_audio_analyzer()
            return analyzer.analyze(file_path)
        
        # Check if it's a video file
        elif suffix in VideoAnalyzer.SUPPORTED_FORMATS:
            analyzer = self._get_video_analyzer()
            return analyzer.analyze(file_path)
        
        else:
            raise ValueError(
                f"Unsupported file format: {suffix}. "
                f"Supported formats: {AudioAnalyzer.SUPPORTED_FORMATS | VideoAnalyzer.SUPPORTED_FORMATS}"
            )
    
    def analyze_audio(self, file_path: str) -> AnalysisResult:
        """
        Explicitly analyze an audio file.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            AnalysisResult with analysis findings
        """
        analyzer = self._get_audio_analyzer()
        return analyzer.analyze(file_path)
    
    def analyze_video(self, file_path: str) -> AnalysisResult:
        """
        Explicitly analyze a video file.
        
        Args:
            file_path: Path to the video file
            
        Returns:
            AnalysisResult with analysis findings
        """
        analyzer = self._get_video_analyzer()
        return analyzer.analyze(file_path)
    
    def save_report(self, result: AnalysisResult, output_path: str):
        """
        Save analysis result to a JSON file.
        
        Args:
            result: AnalysisResult to save
            output_path: Path to save the report
        """
        with open(output_path, 'w') as f:
            json.dump(result.to_dict(), f, indent=2)
