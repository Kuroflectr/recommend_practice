from statistics import variance
from practice.data.ratings import Ratings
from practice.data.genome_scores import GenomeScores 
from practice.data.genome_tags import GenomeTags 
from practice.data.movies import Movies 
from practice.model.recommend import Recommend
import numpy as np 
from numpy.linalg import norm
import time 


class PreferenceRecommend( Recommend ): 
    
    def __init__(self):
        super().__init__()
    
        self.genome_scores = GenomeScores.from_csv() 
        self.genome_tags =  GenomeTags.from_csv()
        
    def train(self): 
        time1 = time.time()
        if len(self.genome_tags.tagId_list) == 0: 
            self.genome_tags.set_tagId_list()
        
        time2 = time.time()
        print('stamp1', time2-time1)
        if len(self.ratings.user_list) == 0: 
            self.ratings.set_list()

        time3 = time.time()
        print('stamp2', time3-time2)
        tagId_list = self.genome_tags.tagId_list
        userId_list = self.ratings.user_list

        time4 = time.time()
        print('stamp3', time4-time3)
        self.U_by_user_tag_matrix = np.zeros([len(tagId_list),len(userId_list)])
        # for i, tag_id in enumerate(tagId_list): 
        #     for j, user_id in enumerate(userId_list): 
        #         U_user_tag = self.equation4(user_id, tag_id)
        #         self.U_by_user_tag_matrix[i, j] = U_user_tag

        self.U_by_user_tag_matrix = self.equation4(
                np.array(tagId_list), 
                np.array(userId_list))

        time5 = time.time()
        print('stamp4', time5-time4)


    def recommend(self, user_id, tag_k=5, movie_k=5) -> list:
        # extract the necessary U matrix which is derived via .train() 
        # U_by_user_tag_matrix = self.U_by_user_tag_matrix

        # find the top-k recommended tags list
        rank_k_tags_list = self.equation18_recommend(user_id, tag_k)

        # derive the score for recommendation (log(O)): 
        unrated_movieid_list_user = np.array(self.ratings.unrated_movieid_list[user_id])

        movieId_score_dict = {}
        for movie_id in unrated_movieid_list_user: 
            movieId_score_dict[movie_id] = self.equation22(user_id, movie_id, rank_k_tags_list)

        sorted_movieId_score_dict  = sorted(movieId_score_dict.items(), key=lambda item: -item[1])
        # sorted_dict: [(2, 9), (3, 4), (4, 2), (1, 1)]
        return  [v[0] for v in sorted_movieId_score_dict[:movie_k]]

    def evaluate(self, tag_k=5, movie_k=5 ): 

        user_list = self.ratings.user_list
        evaluate_value_list = [None] * len(user_list)
        for i, user_id in enumerate(user_list): 
            evaluate_value_by_user = self.evaluate_by_user(user_id, 
                                        tag_k=tag_k, movie_k=movie_k )
            evaluate_value_list[i] = evaluate_value_by_user

        return np.array(evaluate_value_list).mean()



    def evaluate_by_user(self, user_id, tag_k=5, movie_k=5 ): 

        rated_ratings_list_user = np.array([x.rating for x in self.ratings.rating_by_user[user_id]])

        # calculate DCG true 
        ranks_true = self.find_order(rated_ratings_list_user)
        DCG_true = self.DCG(ranks_true, rated_ratings_list_user )

        # calculate DCG predict
        # find the top-k recommended tags list
        rank_k_tags_list = self.equation18_recommend(user_id, tag_k)
        rated_movieid_list_byuser = np.array([x.movieId for x in self.ratings.rating_by_user[user_id]])
        movieId_score_dict = {}
        for movie_id in rated_movieid_list_byuser: 
            movieId_score_dict[movie_id] = self.equation22(user_id, movie_id, rank_k_tags_list)

        sorted_movieId_score_dict  = sorted(movieId_score_dict.items(), key=lambda item: -item[1])
        sorted_movieId_score = [v[1] for v in sorted_movieId_score_dict[:movie_k]]
        ranks_predict = self.find_order(sorted_movieId_score)
        DCG_predict = self.DCG(ranks_predict, rated_ratings_list_user)

        DCG_value_byuser = DCG_predict.sum()/DCG_true.sum()
        
        return DCG_value_byuser


    def DCG(self, order: np.array, rating: np.array) -> np.array:
        return (2**(rating)-1)/(np.log2(order+1)) 

    def find_order(self, array: np.array): 
        temp = np.argsort(-array)
        ranks = np.empty_like(temp)
        ranks[temp] = np.arange(len(array))
        return ranks+1

    def i_rated(self, user_ids) -> int:
        for user_id in user_ids: 
            user_ratings = self.ratings.get_ratings(user_id)
        return len(user_ratings)
        
    def it_rated(self, user_id, tag_id) -> int: 
        user_ratings = self.ratings.get_ratings(user_id)
        movie_id_list = [ x.movieId for x in user_ratings if tag_id in self.genome_scores.get_tags_by_movieid(x.movieId) ]

        return len(movie_id_list)

    def i(self, ) -> int:  
        return len(Movies.from_csv(csv_file_name='csv/movies.csv').movie_list)

    def it(self,tag_id ) -> int: 
        self.genome_scores.set_movieid_by_tags()
        movieid_by_tags_list = self.genome_scores.get_movieid_by_tagid(tag_id)
        return len(movieid_by_tags_list)

    def wit(self, movie_id, tag_id) -> int: 
        self.genome_scores.set_movieid_by_tags()
        movieid_by_tags_list = self.genome_scores.get_movieid_by_tagid(tag_id)
        if movie_id in movieid_by_tags_list: 
            return 1
        return 0


    def rt_vec(self, user_id) -> dict[int, list[float]]: 
        user_ratings = self.ratings.get_ratings(user_id)
        movie_ids = [ user_rating.movieId for user_rating in user_ratings ]
        rt = { }
        for movie_id in movie_ids: 
            tags = self.genome_scores.get_tags_by_movieid(movie_id)
            for tag_id in tags:
                if tag_id not in rt:
                    rt[tag_id] = []
                rt[tag_id].append(self.ratings.get_ratings_by_movies(movie_id, user_id))
        return rt


    def ni_plus(self, movie_id) -> float: 
        rating_by_movieid = self.ratings.get_ratings_by_movieid(movie_id)
    
        return len([ 1  for rating_item in  rating_by_movieid if rating_item.rating > 3  ]) 

    def ni_minus(self, movie_id) -> float: 
        rating_by_movieid = self.ratings.get_ratings_by_movieid(movie_id)
    
        return len([ 1  for rating_item in  rating_by_movieid if rating_item.rating <= 3  ]) 

    def equation1(self, user_id ) -> dict:
        # OK 
        rt_vec = self.rt_vec(user_id)
        rt = {}
        for tag_id in rt_vec.keys(): 
            it = self.it_rated(user_id, tag_id)
            rt[tag_id] = sum(rt_vec[tag_id])/it

        return rt
    
    def equation2(self, user_id) -> dict[int, float]: 
        # ok 
        rt = self.equation1(user_id)
        user_ratings = self.ratings.get_ratings(user_id)
        user_ratings_ratings = [rating.rating for rating in user_ratings]
        r_mu = sum(user_ratings_ratings)/len(user_ratings_ratings)
        
        wt = {}
        for tag_id in rt.keys(): 
            wt[tag_id] = rt[tag_id] -  r_mu

        return wt 
    
    def equation4(self, user_ids: np.array, tag_ids: np.array) -> np.array: 
        #  U = cov * sig * |wt|
        # importance of the tags
        # OK
        # time_eq4_1= time.time()
        cov = self.equation5(user_ids, tag_ids)
        sig = self.equation6(user_ids, tag_ids)
        wt_abs = abs(self.equation2(user_ids).get(tag_ids, 0) ) 
        # time_eq4_2 = time.time()
        # print('eq4:',time_eq4_2-time_eq4_1)
        return cov*sig*wt_abs

    
    def equation5(self, user_ids: np.array, tag_ids: np.array) -> np.array: 
        # OK
        i   = self.i_rated(user_ids)
        it  = self.it_rated( user_ids, tag_ids)
        
        return min([  it/i , (i-it)/ i  ])
        
    
    def equation6(self, user_id, tag_id) -> float:
        
        wt_abs = abs(self.equation2(user_id).get(tag_id, 0)) 
        
        Rt = self.rt_vec(user_id).get(tag_id, [])
        sigma_t = self.variance(Rt)
        it = self.it_rated( user_id, tag_id)

        if sigma_t == 0 or it ==0: 
            return 0
        return min(  [2, wt_abs/(sigma_t/np.sqrt(it))] )


    def variance(self, data, ddof=0) -> float:
        if len(data) == 0: 
            return 99999
        n = len(data)
        mean = sum(data) / n
        return sum((x - mean) ** 2 for x in data) / (n - ddof)


    def equation9(self, user_id ) -> int:
        self.genome_tags.set_tagId_list()
        tagId_list = self.genome_tags.tagId_list
        s_list = [ self.equation4(user_id, tagId) for tagId in tagId_list ]

        return np.argmax(s_list)

    def equation17(self, movie_id, tag_id, mu=1): 
        wit = self.wit(movie_id, tag_id, )
        it = self.it(tag_id)
        i = self.i()

        return ( wit + mu*it/ i ) / ( mu + i/it)

    def equation18(self, user_id, k=5) -> list:
        tagId_list = self.genome_tags.tagId_list
        U_list = [ self.equation4(user_id, tagId) for tagId in tagId_list] 
        
        tagId_u_dict = {}
        for u, tagId in zip(U_list, tagId): 
            tagId_u_dict[u] = tagId    
        sorted_dict = sorted(tagId_u_dict.items(), key=lambda item: -item[1])
    
        return [v[0] for v in sorted_dict[:k]]
    
    def equation18_recommend(self, user_id, k=5 ) -> list:

        user_id_ind = np.where(user_id == self.ratings.user_list)[0]
        U_list = self.U_by_user_tag_matrix[:, user_id_ind]
        
        tagId_u_dict = {}
        for u, tagId in zip(U_list, tagId): 
            tagId_u_dict[u] = tagId    
        sorted_dict = sorted(tagId_u_dict.items(), key=lambda item: -item[1])
    
        return [v[0] for v in sorted_dict[:k]]

    def equation19(self, user_id, tag_id) -> float: 
        # calculate wtu p
        T_list = self.equation18(user_id, k=5)
        if tag_id in T_list: 
            return self.equation2(user_id)[tag_id]
        return 0

    def equation22(self, user_id, movie_id, tagId_list ) -> float:  
        # return the score that would be used in ranking of recommendation
        ni_plus = self.ni_plus(movie_id)
        ni_minus = self.ni_minus(movie_id)
        # top_k_pref_tag = self.equation18(self, user_id)
        lin_list = [  self.equation19(user_id, tag_id)* np.log(self.equation17(movie_id, tag_id)) for tag_id in tagId_list]
        user_num = len(self.ratings.user_list)

        rank = np.log(ni_plus+1) - np.log(user_num + 1 - ni_minus)  + sum(lin_list)

        return rank