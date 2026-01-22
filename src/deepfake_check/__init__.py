"""
Deepfake Check: Audio & Video analyzer to detect AI generated content.
"""

__version__ = "0.1.0"

from .analyzer import DeepfakeAnalyzer
from .audio.analyzer import AudioAnalyzer
from .video.analyzer import VideoAnalyzer

__all__ = ["DeepfakeAnalyzer", "AudioAnalyzer", "VideoAnalyzer"]
