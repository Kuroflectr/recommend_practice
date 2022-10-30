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

    @classmethod
    def from_csv(cls): 
        csv_file_path = DIR_PATH / 'data/csv/genome-scores.csv'
        
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