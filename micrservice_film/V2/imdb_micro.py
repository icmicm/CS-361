from requests import get
from bs4 import BeautifulSoup as Soup
import pandas as pd

"""
https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=250&start=0&ref_=adv_nxt
https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start=201&ref_=adv_nxt
url = get("https://www.imdb.com/search/title/?count=1000&groups=top_1000&sort=user_rating")
"""

Title = []
Year = []
Rating = []
Actors = []


def scraper(url):
    request = url.text
    soup_data = Soup(request, "html.parser")
    movies = soup_data.findAll("div", {"class": "lister-item mode-advanced"})

    for movie in movies:
        Title.append(movie.h3.a.text)
        Year.append(movie.find("span", {"class": "lister-item-year text-muted unbold"}).text[1:5])
        Rating.append(movie.find("div", {"class": "inline-block ratings-imdb-rating"})["data-value"])
        stars = movie.find('p', class_="").text
        stars = stars.split("Stars:")
        stars = stars[1].split(",")
        movie_actors = []
        for star in stars:
            movie_actors.append(star.replace(" \n", "").replace("\n", ""))
        Actors.append(movie_actors)


for segment in ["0", "251", "501", "751"]:
    scraper(get("https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,"
                "desc&count=250&start=" + segment + "&ref_=adv_nxt"))
data = list(zip(Title, Year, Rating, Actors))

df = pd.DataFrame(data, columns=["Title", "Year", "Rating", "Actors"])

print(df)
