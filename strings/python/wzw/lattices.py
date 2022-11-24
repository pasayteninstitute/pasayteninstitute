import pandas as pd

class WessZuminoWitten( object ):
    '''Object that includes Lie Algebra lattice data and central charges for the associated WZW Models.'''
    def __init__( self ):
        
        # first build the database of lattice data
        self.latticeData = self.initializeLatticeData()
        
        # next build the central charges
        self.centralCharges = self.getCentralCharges(self.latticeData)
    
    def getCentralCharges( self , latticeData ,  minLevel = 1 , maxLevel = 32 ):
        
        # create a function to extract lattice data at a specified level
        addLevel = lambda level : latticeData.apply(lambda x : (level * x["dimAdjoint"]) / (x["dualCoexter"] + level) , axis = 1)
        
        # now build the dataframe
        levels = range(minLevel,maxLevel+1)
        
        centralCharges = pd.DataFrame([addLevel(i) for i in levels])
        
        # reindex for clarity
        centralCharges.index = range(minLevel,maxLevel+1)
        centralCharges.index.name = "level"
        return(centralCharges)
    
    def initializeLatticeData( self ):
        
        # We are actually defining these globally here. We've organized it this way to keep the code together.
        # Also to keep the clutter down
        
        self.A = lambda n : {"name" : "A"+(str(n)),"dualCoexter" : (n+1), "dimAdjoint" : n*n + 2*n }
        self.B = lambda n : {"name" : "B"+(str(n)),"dualCoexter" : (2*n-1), "dimAdjoint" : 2*n*n + n }
        self.C = lambda n : {"name" : "C"+(str(n)),"dualCoexter" : (n+1), "dimAdjoint" : 2*n*n + n }
        self.D = lambda n : {"name" : "D"+(str(n)),"dualCoexter" : (2*n-2), "dimAdjoint" : 2*n*n - n }
        
        # we also include exceptional group data using the same pattern although there is no index n.
        self.G2 = lambda n : {"name" : "G2","dualCoexter" : 4, "dimAdjoint" :14 }
        self.F4 = lambda n : {"name" : "F4","dualCoexter" : 9, "dimAdjoint" :52 }
        self.E6 = lambda n : {"name" : "E6","dualCoexter" : 12, "dimAdjoint" :78 }
        self.E7 = lambda n : {"name" : "E7","dualCoexter" : 18, "dimAdjoint" :133 }
        self.E8 = lambda n : {"name" : "E8","dualCoexter" : 30, "dimAdjoint" :248 }
        
        # we also include E8xE8 because its important for Heterotic Strings
        self.E8xE8 = lambda n : {"name" : "E8xE8","dualCoexter" : 60, "dimAdjoint" :496 }
        
        exceptionals = [self.G2,self.F4, self.E6,self.E7,self.E8,self.E8xE8]
        
        
        ## now we build the data table.
        
        # first the exceptionals
        algebraData = pd.DataFrame([g(1) for g in exceptionals])
        
        # next the series
        algebraData = pd.concat([algebraData,pd.DataFrame([self.A(n) for n in range(1,17)])])
        algebraData = pd.concat([algebraData,pd.DataFrame([self.B(n) for n in range(1,17)])])
        algebraData = pd.concat([algebraData,pd.DataFrame([self.C(n) for n in range(1,17)])])
        algebraData = pd.concat([algebraData,pd.DataFrame([self.D(n) for n in range(1,17)])])        
        
        # now reindex for clarity
        algebraData.index = algebraData["name"]
        algebraData = algebraData[[c for c in algebraData.columns if c!="name"]]
        
        return(algebraData)
