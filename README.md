# Git Heatmap

This project visualizes personal Git commit activity over the days of the week and hours of the day.

The goal is to analyze work patterns, concentration peaks, and behavioral rhythms by mapping commits into a day-hour heatmap.

## Features

- Parses Git commit history and extracts timestamps
- Aggregates commits by weekday and hour
- Renders a customizable heatmap using Seaborn
- Supports hourly granularity and zero-fill for missing times
- Produces exportable, high-quality images

## Motivation

This tool was built to reflect on productivity and time management through actual development activity.
It helps identify when deep work happens, when context-switching is likely, and whether a schedule aligns with natural focus windows.

## Requirements

- Python 3.8+
- pandas
- matplotlib
- seaborn

You can install the dependencies using:

```
pip install -r requirements.txt
```

## Usage

1. Export commit timestamps using:

```
git log --pretty=format:"%ad" --date=iso > commits_by_date.txt
```

2. Load the file and process it into a DataFrame.
3. Use the Jupyter notebook or script to generate the heatmap.

## Example Output

The heatmap shows days on the Y-axis, hours (in 12-hour format) on the X-axis, and commit counts as intensity.
You can annotate, adjust styles, or filter ranges as needed.

## License

MIT License
