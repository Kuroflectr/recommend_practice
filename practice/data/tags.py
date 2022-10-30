import os
import csv
from pydantic import BaseModel
from pathlib import Path


DIR_PATH = Path(os.path.dirname(os.path.abspath(__file__)))


class Tag(BaseModel): 
    userId: int
    movieId: int
    tag: str
    timestamp: int



class Tags(BaseModel): 
    tag_list: list[Tag]

    @classmethod
    def from_csv(cls):
        csv_file_path = DIR_PATH / "csv/tags.csv"

        with open(csv_file_path, "r") as f:
            reader = csv.DictReader(f)
            tag_list = []
            for x in reader:
                tag_list.append(Tag(
                    userId=x["userId"],
                    movieId=x["movieId"],
                    tag=x["tag"],
                    timestamp=x["timestamp"], 
                )) 

        return cls(tag_list=tag_list)