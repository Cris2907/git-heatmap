# Git Heatmap

This project visualizes personal Git commit activity over the days of the week and hours of the day.

The goal is to analyze work patterns, concentration peaks, and behavioral rhythms by mapping commits into a day-hour heatmap.

## Features

- Parses Git commit history and extracts timestamps via Git API
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

1. Generate a personal token and give it access to your commits and repositories
2. Create a folder to store the script and environment variables
3. Create a .venv file containing the following:
```
TOKEN = 'your_git_token'
USERNAME = 'your_git_username'
```
3. Download heatmap.py, save it into your folder and run it:
```
python3 heatmap.py
```

## Example Output

The heatmap shows days on the Y-axis, hours (in 12-hour format) on the X-axis, and commit counts as intensity.
You can annotate, adjust styles, or filter ranges as needed.

## License

MIT License
