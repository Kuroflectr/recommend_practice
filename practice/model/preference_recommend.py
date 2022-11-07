from practice.data.ratings import Ratings
from practice.data.genome_scores import GenomeScores 
from practice.model.recommend import Recommend
import numpy as np 
from numpy.linalg import norm
import time 


class UserBasedRecommend( Recommend ): 
    
    def __init__(self):
        super().__init__()
    
        self.genome_scores = GenomeScores.from_csv() # user-based doesnt use
    

    def i_rated(self, user_id):
        user_ratings = self.ratings.get_ratings(user_id)
        return len(user_ratings)
        
    def it_rated(self, user_id, tag_id): 
        user_ratings = self.ratings.get_ratings(user_id)
        movie_id_list = [ x.movieId for x in user_ratings if tag_id in self.genome_scores.get_tags_by_movieid(x.movieId) ]

        return len(movie_id_list)



    def equation_1(self, user_id ):
        
        it = self.it_rated(user_id)

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
    
    def equation4(self, uer_id, tag_id): 
        ...

    
    def equation5(self, user_id, tag_id): 

        i = self.i_rated(user_id)
        it = self.it_rated( user_id, tag_id)
        
        return min([  it/i  ,   (i-it)/ i    ])
        
    
    def equation6(self):
        ...
     