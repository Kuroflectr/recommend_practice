from distutils.msvccompiler import MSVCCompiler
import os
import csv
from pydantic import BaseModel
from pathlib import Path
import numpy as np 
import time



DIR_PATH = Path(os.path.dirname(os.path.abspath(__file__)))


class Rating(BaseModel): 
    userId: int
    movieId: int 
    rating: float
    timestamp: int
    

class Ratings(BaseModel): 
    rating_list: list[Rating]
    rating_by_user: dict[int, list[Rating]] = {}
    user_list: list[int] = []
    movieid_list: list[int] = []
    rating_by_movieid: dict[int, list[Rating]] = {}

    # user_id: [unrated movie id list]
    unrated_movieid_list: dict[int, list[int]] = {}

    @classmethod
    def from_csv(cls, csv_file_name="ratings_s.csv"): 
        csv_file_path = DIR_PATH / f"csv/{csv_file_name}"
        # csv_file_path = DIR_PATH / "csv/test_ratings.csv"


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
        
    def set_rating_by_movie(self,):
        if len(self.rating_by_movieid) == 0:
            all_rating_list = self.rating_list  
            for rating_item in all_rating_list: 
                if rating_item.movieId not in self.rating_by_movieid: 
                    self.rating_by_movieid[rating_item.movieId] =  []
                self.rating_by_movieid[rating_item.movieId].append(rating_item)
    
    def get_ratings_by_movieid(self, movie_id):
        self.set_rating_by_movie() 

        return self.rating_by_movieid.get(movie_id) 

    def set_rating_by_user(self,):
        if len(self.rating_by_user) == 0:
            all_rating_list = self.rating_list  
            for rating_item in all_rating_list: 
                if rating_item.userId not in self.rating_by_user: 
                    self.rating_by_user[rating_item.userId] =  []
                self.rating_by_user[rating_item.userId].append(rating_item)


    def get_ratings(self, user_id):
        self.set_rating_by_user() 

        return self.rating_by_user[user_id]

        # all_rating_list = self.rating_list  
        # rating_list = [ rating for rating in all_rating_list if rating.userId ==  user_id ]

        # return rating_list
    

    def get_ratings_by_movies(self, movie_id, user_id): 
        user_ratings = self.get_ratings(user_id) 
        ratings_dict = {rating_line.movieId: rating_line.rating for rating_line in user_ratings}

        return ratings_dict[movie_id]

        # all_rating_list = self.rating_list  
        # ratings_by_movies = [ rating for rating in all_rating_list if (rating.userId ==  user_id) & (rating.movieId ==  movie_id) ]
        # return ratings_by_movies 


    def set_list(self):
        if self.movieid_list == [] or self.user_list == []: 
            # find how many users, movies are included
            # time1 = time.perf_counter()
            user_list = np.unique( [rating_list_item.userId for rating_list_item in self.rating_list] ) 
            # time2 = time.perf_counter()
            
            # print('user_list: {}'.format(time2-time1))
            
            
            movieid_list = np.unique( [rating_list_item.movieId for rating_list_item in self.rating_list] ) 
            # time3 = time.perf_counter()

            # print('movie_list: {}'.format(time3-time2))

            # user_list = np.unique()
            # movieid_list = []
            # for rating_list_item in self.rating_list: 
            #     if rating_list_item.userId not in user_list: 
            #         user_list.append(rating_list_item.userId)
            #     if rating_list_item.movieId not in movieid_list: 
            #         movieid_list.append(rating_list_item.movieId)
            self.user_list = np.array(user_list)
            self.movieid_list = np.array(movieid_list)

                
        
    def get_ratings_matrix(self):  
        self.set_list()        

        user_num = len(self.user_list)
        movie_num = len(self.movieid_list)

        # create a null rating matrix
        ratings_matrix = np.zeros([user_num, movie_num])

        # fill in the values 
        for rating_list_item in self.rating_list: 
            ind_user = np.where(self.user_list == rating_list_item.userId)[0]
            ind_movie = np.where(self.movieid_list == rating_list_item.movieId)[0]
            ratings_matrix[ind_user, ind_movie]  = rating_list_item.rating

        return ratings_matrix

    def set_unrated_movie_id(self): 
        ratings_matrix = self.get_ratings_matrix()

        # if self.unrated_movieid_list == {}: 
        #     for rating_list_item in self.rating_list :
        #         ratings_matrix_byuser = ratings_matrix[i, :]
        #         self.unrated_movieid_list[rating_list_item.userId] = ratings_matrix_byuser[ratings_matrix_byuser == 0]
        
        if self.unrated_movieid_list == {}: 
            for i, user_id in enumerate(self.user_list): 
                ratings_matrix_byuser = ratings_matrix[i, :]
                self.unrated_movieid_list[user_id] = np.array(self.movieid_list)[ratings_matrix_byuser == 0]
                
