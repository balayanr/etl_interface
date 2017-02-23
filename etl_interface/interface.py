import record
import os
import re
import sys
import numpy as np
from definitions import *
from kanji_and_radicals import *


class ETL_Interface:
    def __init__(self, location = None):
        self.data = {}
        self.location = location
        
        
        
        
    def set_database_location(self, location):
        self.location = location
        
    def get_dataset_location(self):
        return self.location
        
    # Returns a dictionary of databases specified
    def get_data(self, databases = "all"):
        if databases == "all":
            databases = self.data.keys()
        return {db:self.data[db] for db in databases}
            
    # Returns all records containing the requested character
    def get_character(self, char, databases = "all"):
        if databases == "all":
            databases = self.data.keys()
        return {db:self.data[db][char] for db in databases}
    
    def load_dataset(self, dataset, verbouse = True, save_sample = True):
        data = {}
        db_dir = self.location + dataset + "/"
        for item in os.listdir(db_dir):
            if verbouse: print(item)
            if not re.findall(dataset, item)\
                or re.findall("ETL.*INFO", item)\
                or re.findall("jpg", item):
                if verbouse: print(item + " skipped!")
                continue
            elif os.path.isfile(db_dir+item):
                records = load_file(db_dir+item)
                for record in records:
                    if record.get_character() in data:
                        data[record.get_character()].append(record)
                    else:
                        data[record.get_character()] = [record]
                        if verbouse: print("Added " + record.get_character())
                        try:record.save_img("%s%s_(%s)_sample.jpg" % 
                                        (db_dir,item,record.get_character()))
                        except:
                            print("Couldn't save a sample of %s" % 
                                                        record.get_character())
                if verbouse:
                    print(item+ " loaded!")
                    print("Dataset contents: " + ", ".join(data.keys()))
                    print("Dataset dize: " + str(sys.getsizeof(data)))
        self.data[dataset] = data
        
    
# Extract the formatting from the filename
def filename_to_format(filename, return_db = False):
    for db in data_formats.keys():
        if re.findall(db, filename):
            if return_db:
                return data_formats[db]["File format"], db
            else:
                return data_formats[db]["File format"]
    raise Exception("Unknown format for %s" % filename)


def load_file(filename, load_n = 0):
    file_format, database = filename_to_format(filename, return_db = True)
    format_class = record.format_to_class[file_format]
    block_size = format_length[file_format]
    num_records = load_n if load_n else os.path.getsize(filename)//block_size
    records = [None] * num_records
    raw_records = np.fromfile(filename, dtype=np.uint8) 
    for i in range(num_records):
        records[i] = format_class(raw_records[block_size*i:block_size*(i+1)], database)
    return records


