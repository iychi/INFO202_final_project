from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import json

def fetch_top250_movies():
    url = "https://www.imdb.com/chart/top/"
    driver = webdriver.Chrome() 
    driver.get(url)

    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'ipc-title'))
        WebDriverWait(driver, 5).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page loading")
        driver.quit()
        return []

    html = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html, 'html.parser')

    movie_blocks = soup.find_all('div', {'class': 'ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon ipc-title--on-textPrimary sc-a69a4297-2 bqNXEn cli-title with-margin'})
    print(f"Found {len(movie_blocks)} movie blocks.") # make sure to find 250 movies

    rating_blocks = soup.find_all('span', {'class': 'ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating'})
    print(f"Found {len(rating_blocks)} rating blocks.")  # make sure to find 250 ratings

    # user ratings
    imdb_ratings = []
    for rating_block in rating_blocks:
        aria_label = rating_block.get('aria-label', '')
        if "IMDb rating:" in aria_label:
            rating = float(aria_label.split("IMDb rating:")[-1].strip())
            imdb_ratings.append(rating)
    print(f"Extracted {len(imdb_ratings)} ratings.")  # make sure user rating's number

    # movie title, year, runtime, rating
    movie_data = []
    for i, movie_block in enumerate(movie_blocks):
        # title
        title_tag = movie_block.find('a')
        raw_title = title_tag.h3.text.strip()
        title = raw_title.split('. ', 1)[1]
      
        # year, runtime, content_rating
        metadata_block = movie_block.find_next_sibling('div', {'class': 'sc-300a8231-6 dBUjvq cli-title-metadata'})
        if metadata_block:
            spans = metadata_block.find_all('span')
            year = spans[0].text.strip() if len(spans) > 0 else None
            runtime = spans[1].text.strip() if len(spans) > 1 else None
            content_rating = spans[2].text.strip() if len(spans) > 2 else None
        else:
            year, runtime, content_rating = None, None, None

        
        imdb_rating = imdb_ratings[i] if i < len(imdb_ratings) else None

        if title:
            movie = {
                'title': title,
                'year': int(year) if year else None,
                'runtime': runtime,
                'content_rating': content_rating,
                'imdb_rating': imdb_rating
            }
            movie_data.append(movie)

    return movie_data

# save to json
def save_to_json(data, filename='imdb_top_250.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {filename}")

def main():
    print("Fetching IMDB Top 250 movies...")
    movies = fetch_top250_movies() 
    if movies:
        save_to_json(movies)
   

if __name__ == '__main__':
    main()
