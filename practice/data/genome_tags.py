import os
import csv
from pydantic import BaseModel
from pathlib import Path

DIR_PATH = Path(os.path.dirname(os.path.abspath(__file__)))



class GenomeTag(BaseModel):
    tagId: int
    tag: str
    

class GenomeTags(BaseModel): 
    genome_tag_list = list[GenomeTag]
    
    @classmethod
    def from_csv(cls): 
        csv_file_path = DIR_PATH / 'csv/genome-tags.csv' 
        
        with open(csv_file_path, 'r') as f: 
            reader = csv.DictReader(f)
            genome_tag_list = []
            for x in reader: 
                genome_tag_list.append(GenomeTag(
                    tagId = x['tagId'], 
                    tag = x['tag']
                ))

        return cls(genome_tag_list=genome_tag_list)
