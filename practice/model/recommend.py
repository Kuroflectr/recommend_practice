from practice.data.ratings import Ratings
from practice.data.genome_scores import GenomeScores 
import time 

class Recommend:
    def __init__(self):
        self.ratings = Ratings.from_csv()
        # self.genome_scores = GenomeScores.from_csv() # user-based doesnt use


    def train(self): 
        ...

    def recommend(self, user_id): 
        ...
    