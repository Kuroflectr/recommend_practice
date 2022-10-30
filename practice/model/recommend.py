from practice.data.ratings import Ratings
from practice.data.genome_score import GenomeScores 


class Recommend:
    def __init__(self):
        self.ratings = Ratings.from_csv()
        self.genome_scores = GenomeScores.from_csv()


    def train(self): 
        ...

    def recommend(self, user_id): 
        ...
    
    def equation_1(self, user_id, ):
        
        user_ratings = self.ratings.get_ratings(user_id)
        it = len(user_ratings)
        movie_ids =  [ user_rating.movieId for user_rating in user_ratings ]
        rt = { }
        for movie_id in movie_ids: 
            tag = self.genome_scores.get_tags_by_movieid(movie_id)
            rt[tag] = self.ratings.get_ratings_by_movies(movie_id, user_id)


        return 