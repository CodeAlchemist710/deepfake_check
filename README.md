# Deepfake Check

Audio & Video analyzer to detect AI generated content.

## Overview

Deepfake Check is a Python-based tool that analyzes audio and video files to detect potential AI-generated or manipulated content. It uses advanced signal processing techniques and statistical analysis to identify anomalies that are characteristic of AI-generated media.

## Features

- **Audio Analysis**: Detects AI-generated audio using:
  - Spectral analysis (centroid, rolloff, zero-crossing rate)
  - Temporal pattern analysis (energy levels, onset detection)
  - Statistical properties (kurtosis, skewness)

- **Video Analysis**: Detects AI-generated or manipulated video using:
  - Frame quality analysis (sharpness, blur detection)
  - Temporal consistency checking
  - Color distribution analysis
  - Edge pattern detection

- **Supported Formats**:
  - Audio: `.mp3`, `.wav`, `.m4a`, `.flac`, `.ogg`, `.aac`, `.wma`
  - Video: `.mp4`, `.avi`, `.mov`, `.mkv`, `.flv`, `.wmv`, `.webm`

- **Easy-to-use CLI**: Simple command-line interface for single file or batch processing
- **Detailed Reports**: JSON export for detailed analysis results

## Installation

### Prerequisites

- Python 3.8 or higher
- pip

### Install from source

```bash
# Clone the repository
git clone https://github.com/CodeAlchemist710/deepfake_check.git
cd deepfake_check

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Dependencies

The tool requires the following Python packages:
- `numpy` - Numerical computing
- `scipy` - Scientific computing
- `librosa` - Audio analysis
- `opencv-python` - Video processing
- `Pillow` - Image processing
- `tqdm` - Progress bars

## Usage

### Command Line Interface

#### Analyze a single file

```bash
deepfake-check audio.mp3
```

#### Analyze with verbose output

```bash
deepfake-check video.mp4 --verbose
```

#### Analyze multiple files

```bash
deepfake-check file1.mp3 file2.mp4 file3.wav
```

#### Save report to JSON

```bash
deepfake-check audio.mp3 --output report.json
```

#### Batch analysis with reports

```bash
deepfake-check *.mp4 --output-dir reports/
```

### Python API

```python
from deepfake_check import DeepfakeAnalyzer

# Initialize analyzer
analyzer = DeepfakeAnalyzer(verbose=True)

# Analyze a file (auto-detects type)
result = analyzer.analyze('suspicious_audio.mp3')

# Check if likely AI-generated
if result.is_likely_ai_generated:
    print(f"Warning: File is likely AI-generated (confidence: {result.confidence_score:.2%})")
    print(f"Anomalies detected: {len(result.anomalies_detected)}")
else:
    print("File appears to be authentic")

# Save detailed report
analyzer.save_report(result, 'report.json')

# Explicitly analyze audio or video
audio_result = analyzer.analyze_audio('audio.wav')
video_result = analyzer.analyze_video('video.mp4')
```

## How It Works

### Audio Analysis

The audio analyzer examines multiple aspects of the audio signal:

1. **Spectral Features**: Analyzes the frequency content using spectral centroid, rolloff, and zero-crossing rate to detect unnatural patterns
2. **Temporal Features**: Examines energy levels and onset patterns for consistency that's too perfect
3. **Statistical Analysis**: Uses kurtosis and skewness to identify unusual distribution patterns

### Video Analysis

The video analyzer performs frame-by-frame analysis:

1. **Quality Analysis**: Measures sharpness and blur to detect overly consistent or suspiciously uniform quality
2. **Temporal Consistency**: Checks frame-to-frame changes for unnatural patterns or sudden jumps
3. **Color Analysis**: Examines color distribution and balance for anomalies
4. **Edge Detection**: Analyzes edge patterns that may indicate synthetic generation

### Confidence Scoring

The tool calculates a confidence score (0-1) based on:
- Number of anomalies detected
- Weighted severity of each anomaly type
- Combined evidence from multiple analysis methods

A score above 0.5 indicates the file is likely AI-generated.

## Limitations

- **Not 100% Accurate**: This tool uses heuristics and may produce false positives or false negatives
- **Evolving Technology**: AI generation techniques are constantly improving
- **Requires Anomalies**: Detection works best when AI-generated content has detectable artifacts
- **Computational Cost**: Video analysis can be resource-intensive for large files

## Development

### Running Tests

```bash
pytest tests/
```

### Code Style

The project follows PEP 8 style guidelines. Format code with:

```bash
black src/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Disclaimer

This tool is provided for research and educational purposes. Results should be used as one factor among many when evaluating media authenticity. Always verify important content through multiple methods and trusted sources.
