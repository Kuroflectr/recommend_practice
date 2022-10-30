import os
import csv
from pydantic import BaseModel
from pathlib import Path

DIR_PATH = Path(os.path.dirname(os.path.abspath(__file__)))


class Rating(BaseModel): 
    userId: int
    movieId: int 
    rating: float
    timestamp: int
    

class Ratings(BaseModel): 
    rating_list: list[Rating]

    @classmethod
    def from_csv(cls): 
        csv_file_path = DIR_PATH / "csv/ratings.csv"

        with open(csv_file_path, 'r') as f: 
            reader = csv.DictReader(f)
            rating_list = []
            for x in reader: 
                rating_list.append(Rating(
                    userId = x['userId'],
                    movieId = x['movieId'], 
                    rating = x['rating'], 
                    timestamp = x['timestamp'], 
                ))


        return cls(rating_list=rating_list)
    
    # def get_ratings(self, user_id):
    #     all_rating_list = self.rating_list  


    #     for rating in all_rating_list:
    #         if rating.userId == user_id:



    #     return rating_list