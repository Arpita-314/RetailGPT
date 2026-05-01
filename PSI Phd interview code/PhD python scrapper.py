import requests
from bs4 import BeautifulSoup
import pandas as pd

class PhDPositionScraper:
    def __init__(self, keywords="silicon photonics"):
        self.keywords = keywords
        self.results = []

    def scrape_findaphd(self, pages=2):
        base_url = "https://www.findaphd.com/phds/?Keywords="
        for page in range(1, pages+1):
            url = f"{base_url}{self.keywords.replace(' ', '+')}&PG={page}"
            resp = requests.get(url)
            soup = BeautifulSoup(resp.text, "html.parser")
            for item in soup.select(".ProjectSummary"):
                title = item.select_one(".ProjectTitle").get_text(strip=True)
                link = "https://www.findaphd.com" + item.select_one("a")["href"]
                location = item.select_one(".Institution").get_text(strip=True)
                summary = item.select_one(".ProjectDescription").get_text(strip=True)
                self.results.append({
                    "Title": title,
                    "Location": location,
                    "Summary": summary,
                    "Link": link,
                    "Source": "FindAPhD"
                })

    def scrape_academicpositions(self, pages=2):
        base_url = "https://academicpositions.com/find-jobs/?q=silicon+photonics&positions=phd"
        for page in range(1, pages+1):
            url = f"{base_url}&page={page}"
            resp = requests.get(url)
            soup = BeautifulSoup(resp.text, "html.parser")
            for item in soup.select(".job-list-item"):
                title = item.select_one(".job-title").get_text(strip=True)
                link = "https://academicpositions.com" + item.select_one("a")["href"]
                location = item.select_one(".job-location").get_text(strip=True)
                summary = item.select_one(".job-intro").get_text(strip=True) if item.select_one(".job-intro") else ""
                self.results.append({
                    "Title": title,
                    "Location": location,
                    "Summary": summary,
                    "Link": link,
                    "Source": "AcademicPositions"
                })

    def to_excel(self, filename="phd_positions.xlsx"):
        df = pd.DataFrame(self.results)
        df.to_excel(filename, index=False)

if __name__ == "__main__":
    scraper = PhDPositionScraper()
    scraper.scrape_findaphd()
    scraper.scrape_academicpositions()
    scraper.to_excel()
    print("Scraping complete. Results saved to phd_positions.xlsx.")