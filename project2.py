import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from collections import Counter, defaultdict
import time
from pathlib import Path
from datetime import datetime
import logging


def logger():
    """Logging setup and logic"""
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = log_dir / f"cvpr_scraper_{timestamp}.log"

    logging.basicConfig{
        level = logging.INFO,
        format = '%{asctime}s - %{levelname}s - %{message}s',
        handlers = [
            logging.FileHandler(log_filename)
            logging.StreamHandler()
        ]
    }

    logging.info(f"Logging initialized. Log File: {log_filename}")
    return log_filename


def fetch_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.118 Safari/537.36'
    }

    try:
        logging.info(f"fetching url: {url}")
        response = requests.get(url, headers=headers, timeout=30)

        if response.status_code != 200:
            logging.error(f"Failed to fetch url: {
                          url} with status code: {response.status_code}")
            return None
        else:
            logging.info(f"Successfully retrieved url: {url}")
            return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Requeest exception for url: {url}: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error fetching url: {url}: {str(e)}")
        return None


def extract_data(html_content, years):
    if not html_content:
        logging.error(f"Error: No html content to parse for years: {years}")
        return []

    try:
        soup = BeautifulSoup(html_content, 'html_parser')
        papers_data = []

        entries = soup.find_all('dt', class_='ptitle')
        logging.info(f"found {len(entries)} paper entries for years {years} ")

        for i in enumerate(entries):
