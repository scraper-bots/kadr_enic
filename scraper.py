#!/usr/bin/env python3
"""
Async web scraper for kadr.enic.edu.az
Scrapes all candidate data from 150 pages and saves to CSV
"""

import asyncio
import aiohttp
import csv
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import logging
from typing import List, Dict, Optional
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class KadrEnicScraper:
    def __init__(self):
        self.base_url = "https://kadr.enic.edu.az/"
        self.max_pages = 150
        self.semaphore = asyncio.Semaphore(10)  # Limit concurrent requests
        self.session = None
        
    async def __aenter__(self):
        timeout = aiohttp.ClientTimeout(total=30)
        connector = aiohttp.TCPConnector(limit=100)
        self.session = aiohttp.ClientSession(
            timeout=timeout,
            connector=connector,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def fetch_page(self, url: str) -> Optional[str]:
        """Fetch a single page with retry logic"""
        async with self.semaphore:
            for attempt in range(3):
                try:
                    async with self.session.get(url) as response:
                        if response.status == 200:
                            return await response.text()
                        else:
                            logger.warning(f"HTTP {response.status} for {url}")
                            
                except asyncio.TimeoutError:
                    logger.warning(f"Timeout for {url} (attempt {attempt + 1})")
                except Exception as e:
                    logger.error(f"Error fetching {url}: {e}")
                    
                if attempt < 2:
                    await asyncio.sleep(1 * (attempt + 1))  # Exponential backoff
                    
        return None

    def parse_candidate_from_item(self, item) -> Dict[str, str]:
        """Parse candidate data from a list item"""
        candidate = {}
        
        # Extract name
        name_elem = item.find('span', class_='top')
        candidate['name'] = name_elem.get_text(strip=True) if name_elem else ''
        
        # Extract country and specialization
        pos_elem = item.find('div', class_='pos')
        if pos_elem:
            # Get text content and split by <br> tags or newlines
            pos_text = pos_elem.get_text(separator='\n', strip=True)
            lines = [line.strip() for line in pos_text.split('\n') if line.strip()]
            
            if len(lines) >= 2:
                candidate['country'] = lines[0]
                candidate['specialization'] = lines[1]
            elif len(lines) == 1:
                # Text might be concatenated, try to separate by known patterns
                text = lines[0]
                # Common country endings that help identify separation
                country_patterns = [
                    r'(.*?Respublikası)(.*)',
                    r'(.*?Krallığı)(.*)',
                    r'(.*?Dövləti)(.*)', 
                    r'(.*?Federasiyası)(.*)',
                    r'(.*?İttifaqı)(.*)',
                    r'(.*?Birliyi)(.*)',
                    r'(.*?Konfederasiyası)(.*)',
                    r'(.*?Sultanlığı)(.*)',
                    r'(.*?Knyazlığı)(.*)',
                    r'(.*?Xalq Respublikası)(.*)',
                    r'(.*?Ştatları)(.*)'
                ]
                
                found = False
                for pattern in country_patterns:
                    match = re.match(pattern, text)
                    if match:
                        candidate['country'] = match.group(1)
                        candidate['specialization'] = match.group(2)
                        found = True
                        break
                
                if not found:
                    # Fallback: use the detailed data if available
                    candidate['country'] = text
                    candidate['specialization'] = ''
            else:
                candidate['country'] = ''
                candidate['specialization'] = ''
        
        # Extract photo URL
        img_elem = item.find('img')
        candidate['photo_url'] = urljoin(self.base_url, img_elem['src']) if img_elem else ''
        
        # Extract popup details from onclick attribute
        onclick_elem = item.find('a', {'onclick': True})
        if onclick_elem:
            onclick = onclick_elem.get('onclick', '')
            # Parse OpenPop function parameters - handle both single and double quotes
            match = re.search(r"OpenPop\('([^']*)','([^']*)','([^']*)','([^']*)','([^']*)','([^']*)','([^']*)','([^']*)','([^']*)'\)", onclick)
            if match:
                candidate['surname'] = match.group(1)
                candidate['first_name'] = match.group(2)
                candidate['specialization_detailed'] = match.group(3)
                # URLs already have the domain, don't add it again
                photo_url = match.group(4)
                candidate['photo_url_detailed'] = urljoin(self.base_url, photo_url) if photo_url and not photo_url.startswith('http') else photo_url
                cert_url = match.group(5)
                candidate['certificate_url'] = urljoin(self.base_url, cert_url) if cert_url and not cert_url.startswith('http') else cert_url
                candidate['birth_date'] = match.group(6)
                candidate['country_detailed'] = match.group(7)
                candidate['university'] = match.group(8)
                candidate['education_level'] = match.group(9)
        
        return candidate

    async def scrape_page(self, page_num: int) -> List[Dict[str, str]]:
        """Scrape candidates from a single page"""
        url = f"{self.base_url}?page={page_num}"
        logger.info(f"Scraping page {page_num}")
        
        html = await self.fetch_page(url)
        if not html:
            logger.error(f"Failed to fetch page {page_num}")
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        candidates = []
        
        # Find all candidate items
        list_items = soup.find_all('div', class_='list-item')
        
        for item in list_items:
            try:
                candidate = self.parse_candidate_from_item(item)
                if candidate.get('name'):  # Only add if we have a name
                    candidate['page_number'] = page_num
                    candidates.append(candidate)
            except Exception as e:
                logger.error(f"Error parsing candidate on page {page_num}: {e}")
        
        logger.info(f"Found {len(candidates)} candidates on page {page_num}")
        return candidates

    async def scrape_all_pages(self) -> List[Dict[str, str]]:
        """Scrape all pages concurrently"""
        logger.info(f"Starting to scrape {self.max_pages} pages")
        
        # Create tasks for all pages
        tasks = []
        for page_num in range(1, self.max_pages + 1):
            task = asyncio.create_task(self.scrape_page(page_num))
            tasks.append(task)
        
        # Execute all tasks with progress tracking
        all_candidates = []
        completed = 0
        
        for coro in asyncio.as_completed(tasks):
            try:
                candidates = await coro
                all_candidates.extend(candidates)
                completed += 1
                logger.info(f"Progress: {completed}/{self.max_pages} pages completed")
            except Exception as e:
                logger.error(f"Task failed: {e}")
        
        logger.info(f"Scraping completed. Total candidates: {len(all_candidates)}")
        return all_candidates

    def save_to_csv(self, candidates: List[Dict[str, str]], filename: str = 'kadr_enic_candidates.csv'):
        """Save candidates data to CSV file"""
        if not candidates:
            logger.warning("No candidates to save")
            return
            
        # Define CSV headers
        headers = [
            'page_number', 'name', 'surname', 'first_name', 
            'country', 'country_detailed', 'specialization', 'specialization_detailed',
            'university', 'education_level', 'birth_date',
            'photo_url', 'photo_url_detailed', 'certificate_url'
        ]
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                
                for candidate in candidates:
                    # Ensure all headers are present
                    row = {header: candidate.get(header, '') for header in headers}
                    writer.writerow(row)
                    
            logger.info(f"Successfully saved {len(candidates)} candidates to {filename}")
            
        except Exception as e:
            logger.error(f"Error saving to CSV: {e}")

async def main():
    """Main function to run the scraper"""
    start_time = time.time()
    
    async with KadrEnicScraper() as scraper:
        candidates = await scraper.scrape_all_pages()
        scraper.save_to_csv(candidates)
    
    end_time = time.time()
    logger.info(f"Total execution time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())