import os
import csv
from pydantic import BaseModel
from pathlib import Path


DIR_PATH = Path(os.path.dirname(os.path.abspath(__file__)))

class GenomeScore(BaseModel): 
    movieId: int
    tagId: int
    relevance: float



class GenomeScores(BaseModel): 
    genomescore_list: list[GenomeScore]
    tags_by_movieid: dict[int, list[int]] = {}
    movieid_by_tags: dict[int, list[int]] = {}

 
    @classmethod
    def from_csv(cls): 
        csv_file_path = DIR_PATH / 'csv/genome-scores.csv'
        # csv_file_path = DIR_PATH / 'csv/test_genome-scores.csv'

        
        with open(csv_file_path, 'r') as f: 
            reader = csv.DictReader(f)
            genomescore_list = []
            for x in reader: 
                genomescore_list.append(GenomeScore(
                    movieId = x["movieId"], 
                    tagId = x['tagId'], 
                    relevance = x['relevance'],
                ))

        return cls(genomescore_list = genomescore_list )

    def set_tags_by_movieid(self, ):
        if len(self.tags_by_movieid) == 0: 
            for genomescore_list_item in self.genomescore_list: 
                if genomescore_list_item.movieId not in self.tags_by_movieid: 
                    self.tags_by_movieid[genomescore_list_item.movieId] = []
                if genomescore_list_item.relevance >= 0.5: 
                    # only collect the tag with relevance >= 0.5 
                    self.tags_by_movieid[genomescore_list_item.movieId].append(genomescore_list_item.tagId) 
    
        # all_genomescore_list = self.genomescore_list
        # tags = [ genomescore.tagId for genomescore in all_genomescore_list if genomescore.movieId == movie_id ]
        # return tags

    def get_tags_by_movieid(self, movie_id ) -> list: 
        self.set_tags_by_movieid()
        return self.tags_by_movieid.get(movie_id, []) 

    def set_movieid_by_tags(self): 
        if len(self.movieid_by_tags) == 0: 
            for genomescore_list_item in self.genomescore_list: 
                if genomescore_list_item.tagId not in self.movieid_by_tags: 
                    self.movieid_by_tags[genomescore_list_item.tagId] = []
                if genomescore_list_item.relevance >= 0.5: 
                    # only collect the tag with relevance >= 0.5 
                    self.movieid_by_tags[genomescore_list_item.tagId].append(genomescore_list_item.movieId)             

    
    def get_movieid_by_tagid(self, tag_id ) -> list: 
        self.set_movieid_by_tags()

        return self.movieid_by_tags[tag_id]

    
