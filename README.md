# khodata
Data intelligence pilot application

## Overview
Khodata is a data intelligence tool that provides basic data analysis capabilities including statistical summaries, data quality checks, and automated insights.

## Installation

```bash
pip install -e .
```

Or install dependencies directly:

```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

Run with example data:
```bash
python -m khodata.cli --example
```

Analyze data from a JSON file:
```bash
python -m khodata.cli --file examples/sample_data.json
```

Show specific information:
```bash
python -m khodata.cli --example --summary
python -m khodata.cli --example --quality
python -m khodata.cli --example --insights
```

### Python API

```python
from khodata import DataAnalyzer

# Create analyzer instance
analyzer = DataAnalyzer()

# Load data
data = [
    {"name": "Alice", "age": 30, "score": 85.5},
    {"name": "Bob", "age": 25, "score": 92.0},
]
analyzer.load_data(data)

# Get summary
summary = analyzer.get_summary()
print(summary)

# Check data quality
quality = analyzer.check_quality()
print(quality)

# Get insights
insights = analyzer.get_insights()
for insight in insights:
    print(insight)
```

## Testing

Run the test suite:
```bash
python -m pytest tests/
```

Or using unittest:
```bash
python -m unittest discover tests
```

## Features

- **Data Loading**: Support for dictionaries, lists, and pandas DataFrames
- **Statistical Summary**: Get quick statistics about your data
- **Quality Checks**: Identify missing values, duplicates, and completeness
- **Automated Insights**: Generate human-readable insights from data

## License

Apache License 2.0
