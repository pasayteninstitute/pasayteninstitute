import re
import random
import pandas as pd
from collections import Counter

class PartitionDataBase(object):
    initalCount = 20
    def __init__( self , filePath = ""):
        self.source = filePath
        self.data = self.loadData()

    def clean(self , x ):
        return(sorted(set(map(lambda y : tuple(sorted(y)),x)),reverse=True))
        
    def distributionMC( self , n , samples = 10000):
        
        sampleSet = []
        data = self.data.partitions.loc[n]
        for i in range(samples):
            sampleSet.append(random.choice(random.choice(data)))
            
        samples = pd.DataFrame()
        samples["raw"] = pd.Series(dict(Counter(sampleSet)))
        samples["percent"] = samples["raw"] / samples["raw"].sum() * 100
        return(samples.sort_index())
        
                
    def formalPartitions(self,n,oldoutput = {}):
        output = oldoutput
        for i in range(1,n+1):
            parts = [[i]]
        
            for j in range(i):
                p = i-j
                q = j
                if j >0:
                    for w in output.get(q):
                    
                        parts.append(w+[p])
                
            output[i] = parts
        return(output)
    
    
    def incrementPartition(self):
        output = dict(self.data.partitions)
        i = max(output) + 1
        
        parts = [[i]]
        
        for j in range(i):
            p = i-j
            q = j
            if j > 0:
                for w in output.get(q):
                    parts.append(list(w)+[p])
                    
        parts = self.clean(parts)
        output[i] = parts
            
        self.data.loc[i] = {"partitions":parts , "size": len(parts)}
        
        self.data.to_csv(self.source)
        
    def partitions(self,n):
        
        data = pd.DataFrame()
        data["partitions"] = pd.Series(self.formalPartitions(n)).apply(self.clean)
        data["size"] = data["partitions"].apply(len)
        return(data)
        

    def loadData( self ):
        data = pd.DataFrame()
        try:
            def readLine( line ):
                out = list(map(lambda y : tuple([int(i) for i in y]) , (map(lambda x : re.findall("[0-9]+",x) , re.findall("\([0-9, ]+\)",line)))))
                return(out)
            
            data = pd.read_csv(self.source,index_col=0)
            print("loaded Old Data")
            
            data.partitions = data.partitions.apply(readLine)
            print("converted Old Data")            
            
            data.to_csv(self.source + ".old")
        except:
            data = self.partitions(PartitionDataBase.initalCount)
        return(data)
    
    def saveData( self ):
        self.data.to_csv(self.source)

