"""
Audio analysis module for detecting AI-generated audio.
"""

import numpy as np
from pathlib import Path
from typing import Dict, Any, List
import warnings

# Suppress warnings from librosa
warnings.filterwarnings('ignore')

try:
    import librosa
    import scipy.stats
    AUDIO_LIBS_AVAILABLE = True
except ImportError:
    AUDIO_LIBS_AVAILABLE = False

from ..base import BaseAnalyzer, AnalysisResult


class AudioAnalyzer(BaseAnalyzer):
    """Analyzer for detecting AI-generated or manipulated audio."""
    
    SUPPORTED_FORMATS = {'.mp3', '.wav', '.m4a', '.flac', '.ogg', '.aac', '.wma'}
    
    def __init__(self, verbose: bool = False):
        """
        Initialize the audio analyzer.
        
        Args:
            verbose: Enable verbose logging
        """
        super().__init__(verbose)
        if not AUDIO_LIBS_AVAILABLE:
            raise ImportError(
                "Audio analysis requires librosa and scipy. "
                "Install them with: pip install librosa scipy"
            )
    
    def supports_file(self, file_path: str) -> bool:
        """Check if this analyzer supports the given audio file."""
        path = Path(file_path)
        return path.suffix.lower() in self.SUPPORTED_FORMATS
    
    def analyze(self, file_path: str) -> AnalysisResult:
        """
        Analyze an audio file for AI generation/manipulation.
        
        Args:
            file_path: Path to the audio file
            
        Returns:
            AnalysisResult with analysis findings
        """
        self._log(f"Analyzing audio file: {file_path}")
        
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Audio file not found: {file_path}")
        
        if not self.supports_file(file_path):
            raise ValueError(f"Unsupported audio format: {path.suffix}")
        
        # Load audio file
        try:
            y, sr = librosa.load(file_path, sr=None)
            self._log(f"Loaded audio: sample_rate={sr}, duration={len(y)/sr:.2f}s")
        except Exception as e:
            raise RuntimeError(f"Failed to load audio file: {e}")
        
        # Extract features and detect anomalies
        anomalies = {}
        analysis_details = {}
        
        # 1. Spectral analysis
        spectral_anomalies = self._analyze_spectral_features(y, sr)
        anomalies.update(spectral_anomalies)
        analysis_details['spectral'] = spectral_anomalies
        
        # 2. Temporal analysis
        temporal_anomalies = self._analyze_temporal_features(y, sr)
        anomalies.update(temporal_anomalies)
        analysis_details['temporal'] = temporal_anomalies
        
        # 3. Statistical analysis
        statistical_anomalies = self._analyze_statistical_features(y)
        anomalies.update(statistical_anomalies)
        analysis_details['statistical'] = statistical_anomalies
        
        # Calculate confidence score based on anomalies
        confidence_score = self._calculate_confidence(anomalies)
        is_likely_ai = confidence_score > 0.5
        
        self._log(f"Analysis complete. Confidence: {confidence_score:.2f}")
        
        return AnalysisResult(
            file_path=str(path),
            file_type="audio",
            is_likely_ai_generated=is_likely_ai,
            confidence_score=confidence_score,
            anomalies_detected=anomalies,
            analysis_details=analysis_details
        )
    
    def _analyze_spectral_features(self, y: np.ndarray, sr: int) -> Dict[str, Any]:
        """Analyze spectral features for anomalies."""
        self._log("Analyzing spectral features...")
        
        anomalies = {}
        
        # Spectral centroid
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        centroid_mean = np.mean(spectral_centroids)
        centroid_std = np.std(spectral_centroids)
        
        # AI-generated audio often has unusual spectral centroid distributions
        if centroid_std < 500 or centroid_std > 5000:
            anomalies['spectral_centroid_anomaly'] = {
                'detected': True,
                'mean': float(centroid_mean),
                'std': float(centroid_std),
                'reason': 'Unusual spectral centroid distribution'
            }
        
        # Spectral rolloff
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
        rolloff_mean = np.mean(spectral_rolloff)
        
        # Check for abnormal spectral rolloff
        if rolloff_mean > sr * 0.9:
            anomalies['spectral_rolloff_anomaly'] = {
                'detected': True,
                'mean': float(rolloff_mean),
                'reason': 'Abnormally high spectral rolloff'
            }
        
        # Zero crossing rate
        zcr = librosa.feature.zero_crossing_rate(y)[0]
        zcr_mean = np.mean(zcr)
        
        # AI audio sometimes has very consistent zero crossing rates
        if np.std(zcr) < 0.01:
            anomalies['zero_crossing_anomaly'] = {
                'detected': True,
                'mean': float(zcr_mean),
                'std': float(np.std(zcr)),
                'reason': 'Unnaturally consistent zero crossing rate'
            }
        
        return anomalies
    
    def _analyze_temporal_features(self, y: np.ndarray, sr: int) -> Dict[str, Any]:
        """Analyze temporal features for anomalies."""
        self._log("Analyzing temporal features...")
        
        anomalies = {}
        
        # RMS energy
        rms = librosa.feature.rms(y=y)[0]
        rms_mean = np.mean(rms)
        rms_std = np.std(rms)
        
        # Check for unnatural energy patterns
        if rms_std / (rms_mean + 1e-6) < 0.1:
            anomalies['energy_anomaly'] = {
                'detected': True,
                'mean': float(rms_mean),
                'std': float(rms_std),
                'reason': 'Unnaturally consistent energy levels'
            }
        
        # Onset detection
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        onsets = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr)
        
        # AI audio sometimes has very regular onset patterns
        if len(onsets) > 1:
            onset_intervals = np.diff(onsets)
            if len(onset_intervals) > 2 and np.std(onset_intervals) < 2:
                anomalies['onset_pattern_anomaly'] = {
                    'detected': True,
                    'onset_count': len(onsets),
                    'interval_std': float(np.std(onset_intervals)),
                    'reason': 'Suspiciously regular onset patterns'
                }
        
        return anomalies
    
    def _analyze_statistical_features(self, y: np.ndarray) -> Dict[str, Any]:
        """Analyze statistical properties for anomalies."""
        self._log("Analyzing statistical features...")
        
        anomalies = {}
        
        # Kurtosis - measure of tail heaviness
        kurtosis = scipy.stats.kurtosis(y)
        
        # Natural audio typically has kurtosis in certain ranges
        if abs(kurtosis) < 1.0:
            anomalies['kurtosis_anomaly'] = {
                'detected': True,
                'value': float(kurtosis),
                'reason': 'Abnormal distribution kurtosis'
            }
        
        # Skewness
        skewness = scipy.stats.skewness(y)
        
        # Check for unusual skewness
        if abs(skewness) > 2.0:
            anomalies['skewness_anomaly'] = {
                'detected': True,
                'value': float(skewness),
                'reason': 'Unusual distribution skewness'
            }
        
        return anomalies
    
    def _calculate_confidence(self, anomalies: Dict[str, Any]) -> float:
        """
        Calculate confidence score based on detected anomalies.
        
        Args:
            anomalies: Dictionary of detected anomalies
            
        Returns:
            Confidence score between 0 and 1
        """
        if not anomalies:
            return 0.0
        
        # Weight different types of anomalies
        weights = {
            'spectral_centroid_anomaly': 0.25,
            'spectral_rolloff_anomaly': 0.15,
            'zero_crossing_anomaly': 0.20,
            'energy_anomaly': 0.20,
            'onset_pattern_anomaly': 0.10,
            'kurtosis_anomaly': 0.05,
            'skewness_anomaly': 0.05,
        }
        
        total_weight = 0.0
        for anomaly_key in anomalies.keys():
            total_weight += weights.get(anomaly_key, 0.1)
        
        # Normalize to 0-1 range
        confidence = min(total_weight, 1.0)
        return confidence
