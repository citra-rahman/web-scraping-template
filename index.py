import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape latest news articles from a given URL
def scrape_news(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print("Failed to retrieve content from {url}")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    articles = []
    for item in soup.find_all('div', class_='news-item'):
        title = item.find('h3').get_text(strip=True)
        link = item.find('a')['href']
        date = item.find('time').get_text(strip=True)
        summary = item.find('p').get_text(strip=True)
        articles.append({'Title': title, 'Link': link, 'Date': date, 'Summary': summary})
    
    return articles

# List of URLs to scrape news from
urls = [
    'https://www.fiercepharma.com/news',  # Example site for pharma news
    'https://www.pharmexec.com/latest-news',  # Example site for pharmaceutical executive news
]

# Scraping news from each site
all_articles = []
for url in urls:
    print("Scraping news from: {url}")
    articles = scrape_news(url)
    all_articles.extend(articles)

# Converting to DataFrame for better visualization
df = pd.DataFrame(all_articles)

# Save the results to a CSV file
df.to_csv("pharma_news.csv")
print("Scraping completed. The results have been saved to 'pharma_news.csv'.")

# Display the first few rows of the DataFrame
print(df.head())
