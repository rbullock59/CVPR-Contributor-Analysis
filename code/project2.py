import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from collections import Counter, defaultdict
import time
import logging
from pathlib import Path
from datetime import datetime

# Set up logging


def logger():
    """Configure logging to file and console using pathlib."""
    # Create logs directory if it doesn't exist
    log_dir = Path("docs/logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    # Set up logging with timestamp in filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = log_dir / f"cvpr_scraper_{timestamp}.log"

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )

    logging.info(f"Logging initialized. Log file: {log_filename}")
    return log_filename


def fetch_page(url):
    """Fetch the HTML content of a webpage with error logging."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        logging.info(f"Fetching URL: {url}")
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code == 200:
            logging.info(f"Successfully fetched {url}")
            return response.text
        else:
            logging.error(f"Failed to fetch {url}, status code: {
                          response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Request exception for {url}: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error fetching {url}: {str(e)}")
        return None


def extract_data(html_content, year):
    """Extract paper titles and authors from the HTML content with error logging."""
    if not html_content:
        logging.error(f"No HTML content to parse for year {year}")
        return []

    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        papers_data = []

        # Find all paper entries
        paper_entries = soup.find_all('dt', class_='ptitle')
        logging.info(f"Found {len(paper_entries)
                              } paper entries for year {year}")

        for i, paper in enumerate(paper_entries):
            try:
                # Get the paper title
                title = paper.text.strip()

                # Find the authors in the next dd element
                authors_element = paper.find_next('dd')
                if authors_element:
                    authors_text = authors_element.text.strip()
                    # Extract authors (they're usually comma-separated)
                    authors = [author.strip()
                               for author in authors_text.split(',')]
                    papers_data.append({'title': title, 'authors': authors})
                else:
                    logging.warning(f"No authors found for paper: {title}")
            except Exception as e:
                logging.error(f"Error processing paper {
                              i} for year {year}: {str(e)}")

        logging.info(f"Successfully extracted data for {
                     len(papers_data)} papers for year {year}")
        return papers_data
    except Exception as e:
        logging.error(f"Error parsing HTML for year {year}: {str(e)}")
        return []


def process_data(year):
    """Process data for a specific conference year with error logging."""
    logging.info(f"Processing CVPR {year} data...")
    url = f"https://openaccess.thecvf.com/CVPR{year}?day=all"

    try:
        html_content = fetch_page(url)

        if html_content:
            papers_data = extract_data(html_content, year)

            # Count contributions per author
            author_counts = defaultdict(int)
            for paper in papers_data:
                for author in paper['authors']:
                    author_counts[author] += 1

            logging.info(f"Found {len(author_counts)
                                  } unique authors for CVPR {year}")
            return author_counts
        else:
            logging.error(f"Failed to get HTML content for CVPR {year}")
    except Exception as e:
        logging.error(f"Error processing conference data for year {
                      year}: {str(e)}")

    return {}


def get_top_contributors(years=[2022, 2023, 2024], top_n=3):
    """Get the top N contributors across specified years with error logging."""
    logging.info(f"Getting top {top_n} contributors for years {years}")

    # Dictionary to store author contributions by year
    author_contributions = defaultdict(lambda: defaultdict(int))

    # Process each year
    for year in years:
        try:
            logging.info(f"Processing CVPR {year}...")
            year_data = process_data(year)

            # Store contributions for this year
            for author, count in year_data.items():
                author_contributions[author][year] = count

            # Add a small delay to avoid overwhelming the server
            time.sleep(2)
        except Exception as e:
            logging.error(f"Error processing year {year}: {str(e)}")

    try:
        # Calculate total contributions for each author
        author_totals = {}
        for author, year_counts in author_contributions.items():
            total = sum(year_counts.values())
            author_totals[author] = total

        # Get top N contributors
        top_contributors = sorted(
            author_totals.items(), key=lambda x: x[1], reverse=True)[:top_n]

        # Prepare results for Excel
        results = []
        for author, total in top_contributors:
            row = {
                'Author': author,
                '2022': author_contributions[author][2022],
                '2023': author_contributions[author][2023],
                '2024': author_contributions[author][2024],
                'Total': total
            }
            results.append(row)

        logging.info(f"Successfully identified top {
                     len(results)} contributors")
        return results
    except Exception as e:
        logging.error(f"Error calculating top contributors: {str(e)}")
        return []


def save_to_excel(data, filename="cvpr_top_contributors.xlsx"):
    """Save the results to an Excel spreadsheet with error logging using pathlib."""
    try:
        if not data:
            logging.error("No data to save to Excel")
            return False

        # Use pathlib for file path handling
        output_path = Path(filename)

        # Create parent directories if they don't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)

        df = pd.DataFrame(data)
        # Ensure correct column order
        df = df[['Author', '2022', '2023', '2024', 'Total']]
        df.to_excel(output_path, index=False)
        logging.info(f"Results successfully saved to {output_path.absolute()}")
        return True
    except Exception as e:
        logging.error(f"Error saving to Excel: {str(e)}")
        return False


def main(output_dir=None):
    """Main function to run the program with error handling."""
    try:
        # Set up logging
        log_file = logger()

        logging.info("Starting CVPR Conference contributor analysis...")
        top_contributors = get_top_contributors()

        # Use pathlib to handle output directory and file
        if output_dir:
            output_path = Path(output_dir) / "cvpr_top_contributors.xlsx"
        else:
            output_path = Path("cvpr_top_contributors.xlsx")

        if top_contributors:
            success = save_to_excel(top_contributors, str(output_path))
            if success:
                logging.info("Analysis complete!")
                logging.info(f"Results saved to: {output_path.absolute()}")
                logging.info(f"Log file saved to: {log_file}")
            else:
                logging.error("Failed to save results to Excel")
        else:
            logging.error("No top contributors found. Analysis failed.")
    except Exception as e:
        logging.critical(f"Critical error in main function: {str(e)}")


if __name__ == "__main__":
    main()
