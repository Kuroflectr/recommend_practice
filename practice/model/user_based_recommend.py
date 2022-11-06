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


    def recommend_rating(self, user_id, ratings_matrix, predict_movie_id_list): 

        # extract the necessary cosine similiarty column 
        sim_user = self.sim_user
        ind_user = np.where(self.ratings.user_list == user_id)[0]
        sim_user_user_id = sim_user[ind_user, :] # be aware that the first item is itself

        recommend_rating_list = np.zeros(len(predict_movie_id_list))
        for i, movieid in enumerate(predict_movie_id_list): 
            # extract the necessary movie rating column from rating matrix
            ind_movie = np.where(self.ratings.movieid_list == movieid)[0]
            ratings_matrix_user_id = ratings_matrix[:, ind_movie]

            raging_multiple = np.dot(sim_user_user_id, ratings_matrix_user_id)
            recommend_rating_list[i] = (raging_multiple/np.sum(sim_user_user_id))[0]


        return recommend_rating_list

    def recommend(self, user_id): 
        # extract the necessary movie rating column from rating matrix
        ratings_matrix = self.ratings.get_ratings_matrix()

        # find the movie-id that was not rated by any user; we will predict these values: 
        self.ratings.set_unrated_movie_id() 
        # fetch the ids of the unrated movie by the specified user id
        unrated_movieid_list_user = np.array(self.ratings.unrated_movieid_list[user_id])

        # predict the ratings corresponding to the movied id included in "unrated_movieid_list_user" 
        recommend_rating_list = self.recommend_rating(user_id, ratings_matrix, unrated_movieid_list_user)

        return unrated_movieid_list_user[recommend_rating_list.argmax()]

    def cosine_similarity(self, vec1, vec2): 
        cosine = np.dot(vec1,vec2)/(norm(vec1)*norm(vec2))

        return cosine

    def evaluate(self): 
        # evaluated value: 0.8916
        user_list = self.ratings.user_list
        evaluate_value_list = [None] * len(user_list)
        for i, user_id in enumerate(user_list): 
            evaluate_value_by_user = self.evaluate_by_user(user_id)
            evaluate_value_list[i] = evaluate_value_by_user

        return np.array(evaluate_value_list).mean()

    def evaluate_by_user(self, user_id):
        self.ratings.set_rating_by_user()

        # extract the necessary movie rating column from rating matrix
        ratings_matrix = self.ratings.get_ratings_matrix()

        # fetch the ids of the rated movie by the specified user id
        rated_movieid_list_user = np.array([x.movieId for x in self.ratings.rating_by_user[user_id]])

        # predict the ratings corresponding to the movied id included in "unrated_movieid_list_user" 
        recommend_rating_list = self.recommend_rating(user_id, ratings_matrix, rated_movieid_list_user)

        # find the rank of the recommendation: 
        ranks_predict = self.find_order(recommend_rating_list)


        # calculate the DCG_ture by the specified user
        rated_ratings_list_user = np.array([x.rating for x in self.ratings.rating_by_user[user_id]])

        # calculate the DCG_predic by the specified user
        DCG_predict = self.DCG(ranks_predict, rated_ratings_list_user)

        ranks_true = self.find_order(rated_ratings_list_user)
        DCG_true = self.DCG(ranks_true, rated_ratings_list_user )

        DCG_value_byuser = DCG_predict.sum()/DCG_true.sum()

        return DCG_value_byuser

    def find_order(self, array: np.array): 
        temp = np.argsort(-array)
        ranks = np.empty_like(temp)
        ranks[temp] = np.arange(len(array))
            
        return ranks+1

    
    def DCG(self, order: np.array, rating: np.array) -> np.array:
        
        return (2**(rating)-1)/(np.log2(order+1)) 
    