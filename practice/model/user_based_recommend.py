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
        self.sim_user = np.array(user_num, user_num)
        
        
        ratings_matrix = self.ratings.get_ratings_matrix()
        # extract the vec which represents user1 and user2
        for i in range(user_num): 
            user1_vec = ratings_matrix[i, :]
            for j in range(user_num): 
                if i != j: 
                    user2_vec = ratings_matrix[j, :]
                    self.sim_user[i,j] = self.cosine_similarity(user1_vec,user2_vec) 


    def recommend(self, user_id): 
        ...

    def cosine_similarity(self, vec1, vec2): 
        cosine = np.dot(vec1,vec2)/(norm(vec1)*norm(vec2))

        return cosine

    