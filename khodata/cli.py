"""Command-line interface for khodata."""

import sys
import json
import argparse
from khodata.pilot import DataAnalyzer


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Khodata - Data Intelligence Pilot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  khodata --example          Show example usage with sample data
  khodata --file data.json   Analyze data from a JSON file
        """
    )
    
    parser.add_argument(
        "--example",
        action="store_true",
        help="Run with example data"
    )
    
    parser.add_argument(
        "--file",
        type=str,
        help="Path to JSON data file to analyze"
    )
    
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Show data summary"
    )
    
    parser.add_argument(
        "--quality",
        action="store_true",
        help="Show data quality metrics"
    )
    
    parser.add_argument(
        "--insights",
        action="store_true",
        help="Show data insights"
    )
    
    args = parser.parse_args()
    
    # Show help if no arguments provided
    if len(sys.argv) == 1:
        parser.print_help()
        return 0
    
    analyzer = DataAnalyzer()
    
    # Load data
    if args.example:
        # Example data
        sample_data = [
            {"name": "Alice", "age": 30, "score": 85.5},
            {"name": "Bob", "age": 25, "score": 92.0},
            {"name": "Charlie", "age": 35, "score": 78.5},
            {"name": "Diana", "age": 28, "score": 88.0},
            {"name": "Eve", "age": 32, "score": 95.5},
        ]
        analyzer.load_data(sample_data)
        print("Loaded example data")
        print("=" * 50)
    elif args.file:
        try:
            with open(args.file, 'r') as f:
                data = json.load(f)
            analyzer.load_data(data)
            print(f"Loaded data from {args.file}")
            print("=" * 50)
        except FileNotFoundError:
            print(f"Error: File '{args.file}' not found")
            return 1
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in file '{args.file}'")
            return 1
    else:
        print("Error: Please specify --example or --file")
        return 1
    
    # Show requested information
    show_all = not (args.summary or args.quality or args.insights)
    
    if args.summary or show_all:
        print("\nData Summary:")
        print("-" * 50)
        summary = analyzer.get_summary()
        print(json.dumps(summary, indent=2, default=str))
    
    if args.quality or show_all:
        print("\nData Quality:")
        print("-" * 50)
        quality = analyzer.check_quality()
        print(json.dumps(quality, indent=2))
    
    if args.insights or show_all:
        print("\nData Insights:")
        print("-" * 50)
        insights = analyzer.get_insights()
        for i, insight in enumerate(insights, 1):
            print(f"{i}. {insight}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
