import pandas as pd
import re
import json 
import time 
from tqdm import tqdm 
from Clusters import Clusters
import os.path


def extract_features(ob):
    # check if argument type is not string, 
    # we force it to be string :)
    if (type(ob) != str):
        ob = str(ob)

    # we split string into words
    lst = re.findall(r"[\w']+", ob) 

    # elements that we dont want to be recognized as features   
    remove_list = ['по', 'на', 'в', 'с', 'и', 'к', 'у', 'я']

    # removing unwanted elements 
    for elm in lst:
        if (not (elm in remove_list) and ((len(elm) < 3) or (len(elm) > 15))):
            lst.remove(elm)

    # TODO implement some nice hash function so 
    # there can be some optimization
    # we want features to be small but 
    # precise 
    return set(map(lambda x: x, lst))


def get_Data(path, max_count=500, field_name='commentText'):
    with open(path, encoding='utf') as json_file:
        data=json.load(json_file)
        df=pd.DataFrame().from_dict(data)
    data_raw=list(df[field_name].values[0:max_count])
    return list((map(lambda x: x.lower(), data_raw)))


if __name__ == "__main__":
    
    processed_dir = 'processed_data'
    raw_dir       = 'raw_data'

    file_name  = 'data.json'    
    field_name = 'commentText'
    


    overallStartTime=time.time()

    # load
    data_raw=get_Data(os.path.join(raw_dir, file_name), field_name=field_name)

    objects = [[x] for x in data_raw]  
    
    # extracting features
    features = [extract_features(x) for x in data_raw]

    # building clusters
    clusters_builder = Clusters(objects, features)
    data = clusters_builder.getClusters()

    tm = (time.time() - overallStartTime) 
    avg_len = 0 
    for ob in data:
        avg_len+=len(ob[0])
    avg_len = avg_len / len(data)    

    #logging results
    result = {}
    result['File name']                   = file_name
    result['Time in minutes']             = tm / 60 
    result['Max elements in cluster']     = max([len(x[0]) for x in data])
    result['Average elements in cluster'] = avg_len
    result['Clusters count']              = len(data)
    result['Clusters']                    = [x[0] for x in data]
    result['Features']                    = [list(x[1]) for x in data]

    #saving result
    with open('processed_data\\processed_{0}'.format(file_name), mode = 'w+') as f:
        json.dump(result, f)
    
       
     