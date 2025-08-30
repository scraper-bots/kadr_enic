# Kadr ENIC Web Scraper

This script scrapes candidate data from https://kadr.enic.edu.az/ across all 150 pages using async HTTP requests.

## Features

- Async scraping with aiohttp for fast performance
- Extracts all candidate details including popup data
- Saves data to CSV format
- Rate limiting to avoid overwhelming the server
- Retry logic for failed requests
- Progress tracking

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python scraper.py
```

The script will create a `kadr_enic_candidates.csv` file with all candidate data.

## Output CSV Columns

- page_number: Source page number
- name: Full name from list
- surname: Last name from popup
- first_name: First name from popup  
- country: Country from list
- country_detailed: Detailed country from popup
- specialization: Specialization from list
- specialization_detailed: Detailed specialization from popup
- university: University name
- education_level: Education level (Bakalavriat/Magistratura)
- birth_date: Birth date
- photo_url: Photo URL from list
- photo_url_detailed: Detailed photo URL from popup
- certificate_url: Certificate document URL