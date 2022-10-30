import os
import csv
from pydantic import BaseModel
from pathlib import Path

DIR_PATH = Path(os.path.dirname(os.path.abspath(__file__)))



class Movie(BaseModel): 
    movieId: int
    title: str
    genres: str



class Movies(BaseModel): 
    movie_list: list[Movie]

    @classmethod
    def from_csv(cls): 
        csv_file_path = DIR_PATH / 'data/csv/movies.csv'
        
        with open(csv_file_path, 'r') as f: 
            reader = csv.DictReader(f)
            movie_list = []
            for x in reader: 
                movie_list.append(Movie(
                    movieId = x["movieId"], 
                    title = x['title'], 
                    genres = x['genres'],
                ))

        return cls(movie_list = movie_list )