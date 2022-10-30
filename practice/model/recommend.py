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
    
    def equation_1(self, user_id ):
        
        user_ratings = self.ratings.get_ratings(user_id)
        it = len(user_ratings)
        movie_ids =  [ user_rating.movieId for user_rating in user_ratings ]
        rt = { }
        for movie_id in movie_ids: 
            tags = self.genome_scores.get_tags_by_movieid(movie_id)

            for tag_id in tags:
                if tag_id not in rt:
                    rt[tag_id] = []
                rt[tag_id].append(self.ratings.get_ratings_by_movies(movie_id, user_id))
            
        
        for tag_id in rt.keys(): 
            rt[tag_id] = sum(rt[tag_id])/it


        return rt
    
    def  equation2(self, user_id): 

        rt = self.equation_1(user_id)
        user_ratings = self.ratings.get_ratings(user_id)
        user_ratings_ratings = [rating.rating for rating in user_ratings]
        r_mu = sum(user_ratings_ratings)/len(user_ratings_ratings)
        
        wt = rt -  r_mu
        return wt 