import json
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np


# convert runtime to minutes
def convert_runtime_to_minutes(runtime_str):
    if 'h' in runtime_str:
        hours, minutes = 0, 0
        if 'm' in runtime_str:
            hm_parts = runtime_str.split('h')
            hours = int(hm_parts[0].strip())
            minutes = int(hm_parts[1].replace('m', '').strip())
        else:
            hours = int(runtime_str.replace('h', '').strip())
        return hours * 60 + minutes
    return int(runtime_str.replace('m', '').strip())


with open('imdb_top_250.json', 'r', encoding='utf-8') as f:
    movies = json.load(f)

for movie in movies:
    movie['runtime'] = convert_runtime_to_minutes(movie['runtime'])
    if not movie['content_rating']: 
        movie['content_rating'] = "Not Rated"


# movies by content ratings
def visualize_content_ratings(movies):
    content_ratings = [movie['content_rating'] for movie in movies]
    rating_counts = Counter(content_ratings)

    plt.bar(rating_counts.keys(), rating_counts.values())
    plt.xlabel('Content Rating')
    plt.ylabel('Number of Movies')
    plt.title('Content Rating Distribution')
    plt.xticks(rotation=45)

# Add counts on bars
    for index, value in enumerate(rating_counts.values()):
        plt.text(index, value + 0.5, str(value), ha='center', fontsize=10)
    plt.tight_layout()
    plt.show()


# movies by runtimes
def visualize_runtimes(movies):
    runtimes = [movie['runtime'] for movie in movies]

    plt.boxplot(runtimes, vert=False)
    plt.xlabel('Runtime (minutes)')
    plt.title('Movie Runtime Distribution')
    plt.show()


# movies by decades
def visualize_decades(movies):
    decades = [(movie['year'] // 10) * 10 for movie in movies]
    decade_counts = Counter(decades)

    plt.bar(decade_counts.keys(), decade_counts.values(), width=8)
    plt.xlabel('Decade')
    plt.ylabel('Number of Movies')
    plt.title('Movies by Decade')
    plt.xticks(range(min(decade_counts.keys()), max(decade_counts.keys()) + 10, 10))
    for index, (decade, count) in enumerate(decade_counts.items()):
        plt.text(decade, count + 0.5, str(count), ha='center', fontsize=10)
    plt.tight_layout()
    plt.show()


# movies by ratings
def visualize_ratings(movies):
    ratings = [movie['imdb_rating'] for movie in movies]
    rating_counts = Counter(ratings)

# Sort the ratings and counts
    sorted_ratings = sorted(rating_counts.keys())
    sorted_counts = [rating_counts[rating] for rating in sorted_ratings]

    min_rating = min(sorted_ratings)
    max_rating = max(sorted_ratings)
    x_ele = np.arange(min_rating, max_rating + 0.1, 0.1)

    plt.bar(sorted_ratings, sorted_counts, width=0.05, edgecolor='black')
    plt.xlabel('IMDB Rating')
    plt.ylabel('Number of Movies')
    plt.title('IMDB Rating Distribution')

    for x, y in zip(sorted_ratings, sorted_counts):
        plt.text(x, y + 0.5, str(y), ha='center', fontsize=9)
    plt.xticks(x_ele, fontsize=9)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Visualize data
    visualize_content_ratings(movies)
    visualize_runtimes(movies)
    visualize_decades(movies)
    visualize_ratings(movies)


