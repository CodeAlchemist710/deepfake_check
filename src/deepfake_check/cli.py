"""
Command-line interface for deepfake detection.
"""

import argparse
import sys
import json
from pathlib import Path
from typing import List

from .analyzer import DeepfakeAnalyzer
from .base import AnalysisResult


def print_result(result: AnalysisResult, verbose: bool = False):
    """Print analysis result in a human-readable format."""
    print("\n" + "="*70)
    print(f"Analysis Report for: {result.file_path}")
    print("="*70)
    print(f"\nFile Type: {result.file_type.upper()}")
    print(f"\nAI-Generated Content: {'YES' if result.is_likely_ai_generated else 'NO'}")
    print(f"Confidence Score: {result.confidence_score:.2%}")
    
    if result.anomalies_detected:
        print(f"\nAnomalies Detected: {len(result.anomalies_detected)}")
        if verbose:
            print("\nDetailed Anomalies:")
            for anomaly_name, anomaly_data in result.anomalies_detected.items():
                print(f"\n  - {anomaly_name}:")
                if isinstance(anomaly_data, dict):
                    for key, value in anomaly_data.items():
                        if key != 'detected':
                            print(f"      {key}: {value}")
    else:
        print("\nNo anomalies detected.")
    
    print("\n" + "="*70 + "\n")


def analyze_file(file_path: str, verbose: bool = False, 
                output_json: str = None) -> int:
    """
    Analyze a single file.
    
    Args:
        file_path: Path to file to analyze
        verbose: Enable verbose output
        output_json: Optional path to save JSON report
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        analyzer = DeepfakeAnalyzer(verbose=verbose)
        result = analyzer.analyze(file_path)
        
        print_result(result, verbose=verbose)
        
        if output_json:
            analyzer.save_report(result, output_json)
            print(f"Report saved to: {output_json}")
        
        return 0
        
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error analyzing file: {e}", file=sys.stderr)
        if verbose:
            import traceback
            traceback.print_exc()
        return 1


def analyze_batch(file_paths: List[str], verbose: bool = False,
                 output_dir: str = None) -> int:
    """
    Analyze multiple files.
    
    Args:
        file_paths: List of file paths to analyze
        verbose: Enable verbose output
        output_dir: Optional directory to save JSON reports
        
    Returns:
        Exit code (0 for all success, 1 if any errors)
    """
    analyzer = DeepfakeAnalyzer(verbose=verbose)
    
    results = []
    errors = 0
    
    for file_path in file_paths:
        try:
            print(f"\nAnalyzing: {file_path}")
            result = analyzer.analyze(file_path)
            results.append(result)
            
            print_result(result, verbose=verbose)
            
            if output_dir:
                output_path = Path(output_dir)
                output_path.mkdir(parents=True, exist_ok=True)
                
                file_name = Path(file_path).stem
                json_path = output_path / f"{file_name}_report.json"
                analyzer.save_report(result, str(json_path))
                print(f"Report saved to: {json_path}")
            
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}", file=sys.stderr)
            errors += 1
            if verbose:
                import traceback
                traceback.print_exc()
    
    # Print summary
    print("\n" + "="*70)
    print("BATCH ANALYSIS SUMMARY")
    print("="*70)
    print(f"Total files analyzed: {len(file_paths)}")
    print(f"Successful: {len(results)}")
    print(f"Errors: {errors}")
    
    if results:
        ai_generated = sum(1 for r in results if r.is_likely_ai_generated)
        print(f"Likely AI-generated: {ai_generated}")
        print(f"Likely authentic: {len(results) - ai_generated}")
        
        avg_confidence = sum(r.confidence_score for r in results) / len(results)
        print(f"Average confidence: {avg_confidence:.2%}")
    
    print("="*70 + "\n")
    
    return 0 if errors == 0 else 1


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Deepfake Check - Audio & Video analyzer to detect AI generated content",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a single audio file
  deepfake-check audio.mp3
  
  # Analyze a video file with verbose output
  deepfake-check video.mp4 --verbose
  
  # Analyze multiple files
  deepfake-check file1.mp3 file2.mp4 file3.wav
  
  # Save report to JSON
  deepfake-check audio.mp3 --output report.json
  
  # Batch analysis with reports saved to directory
  deepfake-check *.mp4 --output-dir reports/
        """
    )
    
    parser.add_argument(
        'files',
        nargs='+',
        help='File(s) to analyze'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Save report to JSON file (single file mode only)'
    )
    
    parser.add_argument(
        '-d', '--output-dir',
        help='Save reports to directory (batch mode)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 0.1.0'
    )
    
    args = parser.parse_args()
    
    # Single file mode
    if len(args.files) == 1 and not args.output_dir:
        exit_code = analyze_file(
            args.files[0],
            verbose=args.verbose,
            output_json=args.output
        )
    # Batch mode
    else:
        if args.output:
            print("Warning: --output ignored in batch mode. Use --output-dir instead.",
                  file=sys.stderr)
        exit_code = analyze_batch(
            args.files,
            verbose=args.verbose,
            output_dir=args.output_dir
        )
    
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
