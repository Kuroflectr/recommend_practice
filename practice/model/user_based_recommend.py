from practice.data.ratings import Ratings
from practice.data.genome_scores import GenomeScores 
from practice.model.recommend import Recommend
import numpy as np 
from numpy.linalg import norm
import time 


class UserBasedRecommend( Recommend ): 

    def train(self): 
        
        self.ratings.set_list()
        user_num = len(self.ratings.user_list) 
        self.sim_user = np.zeros([user_num, user_num])
        
        # breakpoint()

        ratings_matrix = self.ratings.get_ratings_matrix()
        # extract the vec which represents user1 and user2
        for i in range(user_num): 
            user1_vec = ratings_matrix[i, :]
            for j in range(user_num): 
                if i != j: 
                    user2_vec = ratings_matrix[j, :]
                    self.sim_user[i,j] = self.cosine_similarity(user1_vec,user2_vec) 


    def recommend(self, user_id): 
        # find the movie-id that was not rated by any user; we will predict these values: 
        self.ratings.set_unrated_movie_id() 

        # extract the necessary cosine similiarty column 
        sim_user = self.sim_user
        ind_user = np.where(self.ratings.user_list == user_id)
        sim_user_user_id = sim_user[ind_user, :] # be aware that the first item is itself

        # extract the necessary movie rating column from rating matrix
        ratings_matrix = self.ratings.get_ratings_matrix()

        unrated_movieid_list_user = np.array(self.ratings.unrated_movieid_list[user_id])
        recommend_rating_list = np.zeros(len(unrated_movieid_list_user))
        for i, movieid in enumerate(unrated_movieid_list_user): 
            # extract the necessary movie rating column from rating matrix
            ind_movie = np.where(self.ratings.movieid_list == movieid)
            ratings_matrix_user_id = ratings_matrix[:, ind_movie]

            raging_multiple = np.dot(sim_user_user_id, ratings_matrix_user_id)
            recommend_rating_list[i] = raging_multiple/np.sum(sim_user_user_id)
        
        return unrated_movieid_list_user[recommend_rating_list.argmax()]

    def cosine_similarity(self, vec1, vec2): 
        cosine = np.dot(vec1,vec2)/(norm(vec1)*norm(vec2))

        return cosine

    