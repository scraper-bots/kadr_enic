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

## 📊 Data Analysis & Visualization

Comprehensive data analysis with interactive charts and insights is available in the `/charts` directory.

### Quick Stats
- **Total Candidates**: 1,746 (from 1,892 records)
- **Countries**: 44 countries represented
- **Universities**: 605 different institutions
- **Specializations**: 406 unique fields of study
- **Average Age**: 30.8 years

### 📈 Available Charts

| Chart | Insights |
|-------|----------|
| **Country Distribution** | Turkey (46%), Russia (18.4%), Ukraine (12.5%) dominate |
| **Education Levels** | Bachelor's 56.9%, Master's 36.7%, Medical 5.3% |
| **Top Specializations** | Economics (8.1%), Law (6.8%), Business (4.0%) lead |
| **Age Demographics** | Peak age: 22-35 years, Mean: 30.8 years |
| **Universities** | 605 institutions with wide international coverage |
| **Birth Year Trends** | Increasing young applicants (born 1990-2005) |
| **Country-Education Matrix** | Country-specific education patterns revealed |
| **Specialization Categories** | Business & Economics dominate at 500+ candidates |

### 🎯 Key Insights

**Geographic Focus:**
- Top 3 countries (Turkey, Russia, Ukraine) represent 76.9% of all candidates
- 46% of all candidates come from Turkey alone
- Opportunity for targeted language support and partnerships

**Education Trends:**
- 93.6% are Bachelor's or Master's degree holders
- Strong concentration in Business, Economics, and Law fields
- Medical credentials represent a specialized 5.3% segment

**Demographics:**
- Young professional demographic (avg age 30.8)
- Digital-native generation requiring modern application processes
- Peak birth years: 1990-2000 (Millennials and early Gen Z)

### 📁 View Full Analysis

**[→ See complete analysis with charts and actionable recommendations](charts/README.md)**

The charts directory contains:
- 8 high-resolution visualization charts (300 DPI)
- Comprehensive statistical analysis
- Strategic recommendations for operations
- Actionable insights for market expansion
- Data quality assessment

### Generate Updated Charts

To regenerate charts with updated data:

```bash
python3 generate_charts.py
```

This will create/update all charts in the `/charts` directory with the latest data from `kadr_enic_candidates.csv`.