"""
Video analysis module for detecting AI-generated or manipulated video.
"""

import numpy as np
from pathlib import Path
from typing import Dict, Any, List, Optional
import warnings

warnings.filterwarnings('ignore')

try:
    import cv2
    VIDEO_LIBS_AVAILABLE = True
except ImportError:
    VIDEO_LIBS_AVAILABLE = False

from ..base import BaseAnalyzer, AnalysisResult


class VideoAnalyzer(BaseAnalyzer):
    """Analyzer for detecting AI-generated or manipulated video."""
    
    # Supported video file formats for analysis
    SUPPORTED_FORMATS = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm'}
    
    def __init__(self, verbose: bool = False, sample_frames: int = 30):
        """
        Initialize the video analyzer.
        
        Args:
            verbose: Enable verbose logging
            sample_frames: Number of frames to sample for analysis
        """
        super().__init__(verbose)
        if not VIDEO_LIBS_AVAILABLE:
            raise ImportError(
                "Video analysis requires opencv-python. "
                "Install it with: pip install opencv-python"
            )
        self.sample_frames = sample_frames
    
    def supports_file(self, file_path: str) -> bool:
        """Check if this analyzer supports the given video file."""
        path = Path(file_path)
        return path.suffix.lower() in self.SUPPORTED_FORMATS
    
    def analyze(self, file_path: str) -> AnalysisResult:
        """
        Analyze a video file for AI generation/manipulation.
        
        Args:
            file_path: Path to the video file
            
        Returns:
            AnalysisResult with analysis findings
        """
        self._log(f"Analyzing video file: {file_path}")
        
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Video file not found: {file_path}")
        
        if not self.supports_file(file_path):
            raise ValueError(f"Unsupported video format: {path.suffix}")
        
        # Open video file
        cap = cv2.VideoCapture(file_path)
        if not cap.isOpened():
            raise RuntimeError(f"Failed to open video file: {file_path}")
        
        try:
            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            duration = frame_count / fps if fps > 0 else 0
            
            self._log(f"Video properties: {width}x{height}, {fps:.2f} fps, "
                     f"{frame_count} frames, {duration:.2f}s duration")
            
            # Sample frames for analysis
            frames = self._sample_frames(cap, frame_count)
            self._log(f"Sampled {len(frames)} frames for analysis")
            
            # Analyze frames
            anomalies = {}
            analysis_details = {}
            
            # 1. Frame quality analysis
            quality_anomalies = self._analyze_frame_quality(frames)
            anomalies.update(quality_anomalies)
            analysis_details['quality'] = quality_anomalies
            
            # 2. Temporal consistency analysis
            temporal_anomalies = self._analyze_temporal_consistency(frames)
            anomalies.update(temporal_anomalies)
            analysis_details['temporal'] = temporal_anomalies
            
            # 3. Color distribution analysis
            color_anomalies = self._analyze_color_distribution(frames)
            anomalies.update(color_anomalies)
            analysis_details['color'] = color_anomalies
            
            # 4. Edge detection analysis
            edge_anomalies = self._analyze_edges(frames)
            anomalies.update(edge_anomalies)
            analysis_details['edges'] = edge_anomalies
            
            # Calculate confidence score
            confidence_score = self._calculate_confidence(anomalies)
            is_likely_ai = confidence_score > 0.5
            
            self._log(f"Analysis complete. Confidence: {confidence_score:.2f}")
            
            return AnalysisResult(
                file_path=str(path),
                file_type="video",
                is_likely_ai_generated=is_likely_ai,
                confidence_score=confidence_score,
                anomalies_detected=anomalies,
                analysis_details=analysis_details
            )
        
        finally:
            cap.release()
    
    def _sample_frames(self, cap: cv2.VideoCapture, 
                      frame_count: int) -> List[np.ndarray]:
        """Sample frames evenly from the video."""
        frames = []
        
        if frame_count <= self.sample_frames:
            # Sample all frames
            indices = range(frame_count)
        else:
            # Sample evenly distributed frames
            indices = np.linspace(0, frame_count - 1, self.sample_frames, dtype=int)
        
        for idx in indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            if ret:
                frames.append(frame)
        
        return frames
    
    def _analyze_frame_quality(self, frames: List[np.ndarray]) -> Dict[str, Any]:
        """Analyze frame quality for anomalies."""
        self._log("Analyzing frame quality...")
        
        anomalies = {}
        
        # Calculate sharpness (Laplacian variance)
        sharpness_scores = []
        for frame in frames:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            sharpness = laplacian.var()
            sharpness_scores.append(sharpness)
        
        mean_sharpness = np.mean(sharpness_scores)
        std_sharpness = np.std(sharpness_scores)
        
        # AI-generated video often has very consistent sharpness
        if std_sharpness < 10 and mean_sharpness > 50:
            anomalies['sharpness_anomaly'] = {
                'detected': True,
                'mean': float(mean_sharpness),
                'std': float(std_sharpness),
                'reason': 'Unnaturally consistent sharpness across frames'
            }
        
        # Very low sharpness can indicate AI generation
        if mean_sharpness < 30:
            anomalies['low_sharpness_anomaly'] = {
                'detected': True,
                'mean': float(mean_sharpness),
                'reason': 'Unusually low overall sharpness'
            }
        
        return anomalies
    
    def _analyze_temporal_consistency(self, 
                                     frames: List[np.ndarray]) -> Dict[str, Any]:
        """Analyze temporal consistency between frames."""
        self._log("Analyzing temporal consistency...")
        
        anomalies = {}
        
        if len(frames) < 2:
            return anomalies
        
        # Calculate frame differences
        frame_diffs = []
        for i in range(len(frames) - 1):
            gray1 = cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(frames[i + 1], cv2.COLOR_BGR2GRAY)
            diff = cv2.absdiff(gray1, gray2)
            frame_diffs.append(np.mean(diff))
        
        mean_diff = np.mean(frame_diffs)
        std_diff = np.std(frame_diffs)
        
        # AI video sometimes has very consistent frame-to-frame changes
        if std_diff < 1.0 and mean_diff > 5:
            anomalies['temporal_consistency_anomaly'] = {
                'detected': True,
                'mean_diff': float(mean_diff),
                'std_diff': float(std_diff),
                'reason': 'Suspiciously consistent temporal changes'
            }
        
        # Check for sudden jumps (possible GAN artifacts)
        max_diff = np.max(frame_diffs)
        if max_diff > mean_diff * 5:
            anomalies['temporal_jump_anomaly'] = {
                'detected': True,
                'max_diff': float(max_diff),
                'mean_diff': float(mean_diff),
                'reason': 'Unusual temporal discontinuities detected'
            }
        
        return anomalies
    
    def _analyze_color_distribution(self, 
                                   frames: List[np.ndarray]) -> Dict[str, Any]:
        """Analyze color distribution for anomalies."""
        self._log("Analyzing color distribution...")
        
        anomalies = {}
        
        # Analyze color histograms
        color_means = []
        color_stds = []
        
        for frame in frames:
            for channel in range(3):  # B, G, R channels
                channel_data = frame[:, :, channel]
                color_means.append(np.mean(channel_data))
                color_stds.append(np.std(channel_data))
        
        overall_mean = np.mean(color_means)
        overall_std = np.mean(color_stds)
        
        # AI video sometimes has unusual color distributions
        if overall_std < 20:
            anomalies['color_distribution_anomaly'] = {
                'detected': True,
                'mean': float(overall_mean),
                'std': float(overall_std),
                'reason': 'Unnaturally low color variation'
            }
        
        # Check color balance
        color_channel_means = [[] for _ in range(3)]
        for frame in frames:
            for channel in range(3):
                color_channel_means[channel].append(np.mean(frame[:, :, channel]))
        
        channel_avgs = [np.mean(ch) for ch in color_channel_means]
        channel_imbalance = np.std(channel_avgs)
        
        # Significant color imbalance can indicate manipulation
        if channel_imbalance > 30:
            anomalies['color_balance_anomaly'] = {
                'detected': True,
                'channel_means': [float(m) for m in channel_avgs],
                'imbalance': float(channel_imbalance),
                'reason': 'Unusual color channel imbalance'
            }
        
        return anomalies
    
    def _analyze_edges(self, frames: List[np.ndarray]) -> Dict[str, Any]:
        """Analyze edge characteristics for anomalies."""
        self._log("Analyzing edge characteristics...")
        
        anomalies = {}
        
        edge_densities = []
        for frame in frames:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges > 0) / edges.size
            edge_densities.append(edge_density)
        
        mean_density = np.mean(edge_densities)
        std_density = np.std(edge_densities)
        
        # AI-generated video may have unusual edge patterns
        if std_density < 0.001:
            anomalies['edge_consistency_anomaly'] = {
                'detected': True,
                'mean_density': float(mean_density),
                'std_density': float(std_density),
                'reason': 'Suspiciously consistent edge patterns'
            }
        
        # Very low edge density can indicate AI generation
        if mean_density < 0.02:
            anomalies['low_edge_density_anomaly'] = {
                'detected': True,
                'mean_density': float(mean_density),
                'reason': 'Unusually low edge density'
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
            'sharpness_anomaly': 0.15,
            'low_sharpness_anomaly': 0.10,
            'temporal_consistency_anomaly': 0.25,
            'temporal_jump_anomaly': 0.15,
            'color_distribution_anomaly': 0.15,
            'color_balance_anomaly': 0.10,
            'edge_consistency_anomaly': 0.05,
            'low_edge_density_anomaly': 0.05,
        }
        
        total_weight = 0.0
        for anomaly_key in anomalies.keys():
            total_weight += weights.get(anomaly_key, 0.1)
        
        # Normalize to 0-1 range
        confidence = min(total_weight, 1.0)
        return confidence
