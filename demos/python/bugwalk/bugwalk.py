import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Bug(object):
    stepsize = 0.01
    def __init__(self,xi,yi):
        self.x = 0
        self.y = 0
        self.track = []
        self.distance = 0
        self.updatePosition(xi,yi)
    
    def updatePosition(self,dx,dy):
        self.x += dx
        self.y += dy
        self.track.append((self.x,self.y))
        
        
    def trackStep(self,pair):
        x,y = pair
        dx = (x - self.x)*Bug.stepsize
        dy = (y - self.y)*Bug.stepsize
        self.updatePosition(dx,dy)
        self.distance += np.sqrt(dx*dx + dy*dy)

    def getLocation(self):
        return((self.x,self.y))
    
    def updateFromBug(self,bug):
        self.trackStep(bug.getLocation())
        
    def getTrack(self):
        x = pd.Series([j[0] for j in self.track])
        y = pd.Series([j[1] for j in self.track])
        return(pd.DataFrame({"x":x,"y":y}))
        
        
class BugWalk( object ):
    '''Implementation of Martin Gardners 4-bug problem for arbitrary bugs and starting positions.'''
    def __init__(self , bugPoints ):
        self.startCoordinates = bugPoints
        self.bugs = [Bug(*coordinate) for coordinate in self.startCoordinates]
        self.bugCount = len(self.bugs)
        
    def walk( self , J = 10000 ):
        for j in range(J):
            for k in range(self.bugCount):
                otherBug = (k+1) % self.bugCount
                self.bugs[k].updateFromBug( self.bugs[otherBug] )

                
        self.theDance = pd.concat([x.getTrack() for x in self.bugs])
                
    def plot( self ):
        ax = self.theDance.plot.scatter(x="x",y="y")
        ax.set_aspect(1)
        plt.xlim([-1, 1])
        plt.ylim([-1, 1])
        plt.title(str(len(self.bugs)) + " bug dance")
        plt.show()
        
class RegularBugWalk( BugWalk ):
    '''Bug walk with starting points as vertices on a regular polygon.'''
    def __init__( self , corners , resolution = 3):

        if corners < 3:
            corners = 3
            print("Regular polygons need at least 3 vertices. Argument set to 3.")

        self.degree = corners
        self.length = self.getPolygonLength(self.degree)
        self.points = self.makePoints(self.degree,resolution)
        BugWalk.__init__( self , self.points )
        self.fullWalk()
        self.bugLength = np.mean([bug.distance for bug in self.bugs])
        
    def makePoints( self , corners , resolution ):
        angle = (2*np.pi) / corners
        points = [(round(np.cos(angle*i),resolution),round(np.sin(angle*i),resolution)) for i in range(corners)]
        return(points)
    
    def getPolygonLength(self,corners):
        points = self.makePoints(corners,10)
        distances = []
        for i in range(corners):
            dx = points[i][0] - points[(i+1)%corners][0]
            dy = points[i][1] - points[(i+1)%corners][1]
            distances.append(np.sqrt(dx*dx + dy*dy))
        return(np.mean(distances))
    
    def fullWalk( self ):
        self.steps = 0
        ratio = 0
        
        # the bugs will walk for a distance proportional to the length of the polygon.
        # this condition essentially cuts the bug walk off when they all reach the middle.
        while ratio < 2:
            for k in range(self.bugCount):
                self.steps += 1
                otherBug = (k+1) % self.bugCount
                self.bugs[k].updateFromBug( self.bugs[otherBug] )

            ratio = np.mean([bug.distance for bug in self.bugs]) * self.length
        self.theDance = pd.concat([x.getTrack() for x in self.bugs])
