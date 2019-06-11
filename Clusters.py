import json
import time
from tqdm import tqdm 

class Clusters():

    threshold = 0.5

    # Constructor gets objects and features
    def __init__(self, objects, features):
        self._objects_ = objects
        self._features_ = features

    
    # Calculate distance between objects
    def __distance__(self, features_a, features_b):
        ans = len(set.intersection(features_a, features_b))
        return ans/((len(features_a)+len(features_b))/2)  

    
    # returns clusters list(index 0 - cluster, index 1 - cluster features) 
    def getClusters(self): 
        data = [[[ob], ft] for (ob, ft) in zip(self._objects_, self._features_)]

        # remove objects without features
        for [ob_d, ft_d] in data:
            if len(ft_d) == 0:
                data.remove([ob_d, ft_d])

        connect = True
        while  connect: 
            connect = False
            for p1 in tqdm(data): 
                for p2 in  data: 
                    if p1 == p2:
                        continue 
                    if self.__distance__(p1[1], p2[1]) >= self.threshold:
                        p1[0] = p1[0] + p2[0]
                        p1[1] = set.union(p1[1], p2[1])
                        data.remove(p2)
                        connect = True
        return data            
 