# CVPR Conference Top Contributors

## Overview

This project is a Python-based web scraper that extracts information about the top contributors to the CVPR conference over the last three years (2022, 2023, and 2024). The script scrapes paper author data from the official CVPR Open Access website, processes the collected data, and stores the top three contributors along with their publication counts in an Excel spreadsheet.

### Features

Web scraping of CVPR conference paper authorship data.

Extraction and aggregation of author contribution counts over three years.

Logging of execution details and error handling.

Output results stored in an Excel spreadsheet.

### Dependencies

The project requires the following Python libraries:

- `requests`

- `beautifulsoup4`

- `pandas`

- `re`

- `collections`

- `time`

- `logging`

- `pathlib`

- `datetime`

You can install the required dependencies using:

```
pip install requests beautifulsoup4 pandas
```

### File Structure

```
project-folder/
│── cvpr_analysis.py  # Main Python script
│── README.md
│── docs/
│   │── logs/   # Logs directory
│── cvpr_top_contributors.xlsx  # Output file (generated after execution)
```

## Function Prototypes and Descriptions

| Function | Prototype | Description |
| -------------------- | ------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| logger | `def logger() -> Path:` | Configures logging for the application. |
| fetch_page | `def fetch_page(url: str) -> str:` | Fetches HTML content from a given URL. |
| extract_data | `def extract_data(html_content: str, year: int) -> list:` | Extracts paper titles and authors from the given HTML content. |
| process_data | `def process_data(year: int) -> dict:` | Processes extracted data and counts author contributions for a given year. |
| get_top_contributors | `def get_top_contributors(years=[2022, 2023, 2024], top_n=3) -> list:` | Identifies the top 3 contributors over the specified years. |
| save_to_excel | `def save_to_excel(data: list, filename="cvpr_top_contributors.xlsx") -> bool:` | Saves extracted contributor data to an Excel spreadsheet. |
| main | `def main(output_dir=None) -> None:` | Main execution function to run the script. |

## Running the Script

To execute the program, simply run:

```
python project2.py
```

The script will:

1. Scrape the CVPR website for author data from 2022 to 2024.

1. Process the data and count author contributions.

1. Identify the top three contributors.

1. Save the results in cvpr_top_contributors.xlsx.

## Example output

An example output stored in `cvpr_top_contributors.xlsx`:

| Author | 2022 | 2023 | 2024 | Total |
| -------- | ---- | ---- | ---- | ----- |
| Person 1 | 10 | 9 | 8 | 27 |
| Person 2 | 9 | 8 | 7 | 24 |
| Person 3 | 8 | 7 | 6 | 21 |

## Logging

Execution logs are saved in docs/logs/ with timestamps.

## Challenges Faced

- Handling website request timeouts and errors.

- Ensuring robust data extraction despite HTML structure variations.

- Managing rate limits and delays to avoid blocking.
