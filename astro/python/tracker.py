import pandas as pd
import datetime as dt
from astropy.time import Time
from astropy import coordinates as c

class DateTimeIntevral( object ):
    '''A base class that includes specific datetime range objects.'''
    def __init__( self , date ):
        self.date = date
        self.formatString = "%Y-%m-%d %H:%M"
        
        self.night = date + " 20:0"
        self.midnight = date + " 0:0"
        self.morning = date + " 4:0" 
        
        self.oneWeekNight = self.dayRange( self.night , 7)
        self.oneWeekMidnight = self.dayRange( self.midnight , 7)        
        self.oneWeekMorning = self.dayRange( self.morning , 7)   
                
        self.oneNight = self.hourRange( self.night , 8)
        
        self.specificTime = lambda time : self.date + time
        
    def dayRange( self , session , days):
        
        startDateTime = dt.datetime.strptime( session , self.formatString )
        datetime = startDateTime
        times = [datetime]
        
        for i in range(days + 1):
            datetime = datetime + dt.timedelta(days=1)
            times.append(datetime)
        return(times)

    def hourRange( self , session , hours):
        
        startDateTime = dt.datetime.strptime( session , self.formatString )
        datetime = startDateTime
        times = [datetime]
        
        for i in range(hours + 1):
            datetime = datetime + dt.timedelta(hours=1)
            times.append(datetime)
        return(times)

    
class PlanetTrack( DateTimeIntevral ):
    '''A generic planet tracker for any point on Earth.'''
    def __init__( self , planet , date , lat , lon , ele , utcDelta ):
        DateTimeIntevral.__init__( self , date )
        self.planet = planet
        self.date = date
        self.location = c.earth.EarthLocation.from_geodetic(lon,lat,ele)
        self.utcDelta = utcDelta
        self.formatString = "%Y-%m-%d %H:%M"
        
    def getTime( self , dateTimeString ):
        
        time = dt.datetime.strptime( dateTimeString , self.formatString ) + dt.timedelta(hours = self.utcDelta )
        return(Time(time.strftime(self.formatString)))
    
    def getCV( self , datetime , source = "builtin"):
        
        time = self.getTime(datetime.strftime(self.formatString))
        aaFormat = c.AltAz( location = self.location , obstime = time )
        with c.solar_system_ephemeris.set(source):
            point = c.get_body( self.planet , time , self.location )
        point = point.transform_to(aaFormat) 
        pointData = {}
        pointData["timestamp"] = datetime.strftime(self.formatString)
        pointData["planet"] = self.planet
        pointData["az"] = point.az.value
        pointData["alt"] = point.alt.value        
        pointData["constellation"] = point.get_constellation()
        return(pointData)


    def getOneNightTrack( self ):
        output = [ self.getCV(datetime) for datetime in self.oneNight ]
        return(pd.DataFrame(output))
    
    def getOneWeekNightTrack( self ):
        output = [ self.getCV(datetime) for datetime in self.oneWeekNight ]
        return(pd.DataFrame(output))
    
    def getOneWeekMidnightTrack( self ):
        output = [ self.getCV(datetime) for datetime in self.oneWeekMidnight ]
        return(pd.DataFrame(output))   
    
    def getOneWeekMorningTrack( self ):
        output = [ self.getCV(datetime) for datetime in self.oneWeekMorning ]
        return(pd.DataFrame(output))       


class WinthropTrack( PlanetTrack ):
    '''A winthrop-specific planet tracker'''
    def __init__(self , planet , date ):
        PlanetTrack.__init__( self , planet , date , 48.4779 , -120.1862 , 542 , 7 )
        self.date = date
        self.planet = planet

class SeattleTrack( PlanetTrack ):
    '''A seattle-specific planet tracker'''
    def __init__(self , planet , date ):
        PlanetTrack.__init__( self , planet , date , 47.6124 , -122.3226 , 0 , 7 )
        self.date = date
        self.planet = planet
        
class KailuaTrack( PlanetTrack ):
    '''A seattle-specific planet tracker'''
    def __init__(self , planet , date ):
        PlanetTrack.__init__( self , planet , date , 21.3984 , -157.7275 , 0 , 7 )
        self.date = date
        self.planet = planet        
        
class TrackCollections( object ):
    '''The collectino of all winthrop specific tracks'''
    def __init__( self , PlanetTrackClass , date = ""):
        
        self.date = date
        if date == "":
            self.date = dt.datetime.now().strftime("%Y-%m-%d")

        self.planets = {}
        for planet in c.solar_system_ephemeris.bodies:
            self.planets[planet] = PlanetTrackClass( planet , self.date )
            
    def getNight( self ):
        return(pd.concat([self.planets[p].getOneNightTrack() for p in self.planets]))
    
    def getWeekNight( self ):
        return(pd.concat([self.planets[p].getOneWeekNightTrack() for p in self.planets]))
    
    def getOneWeekMidnight( self ):
        return(pd.concat([self.planets[p].getOneWeekMidnightTrack() for p in self.planets]))
    
    def getOneWeekMorning( self ):
        return(pd.concat([self.planets[p].getOneWeekMorningTrack() for p in self.planets]))
    
    
    def write( self , filePath ):
        print("compiling the night...")
        self.getNight().to_csv(filePath + self.date + "_night.csv")
        print("compiling evening values...")
        self.getNight().to_csv(filePath + self.date + "_evening.csv")
        print("compiling midnight values...")
        self.getNight().to_csv(filePath + self.date + "_midnight.csv")
        print("compiling early morning values...")
        self.getNight().to_csv(filePath + self.date + "_earlyMorning.csv")        
        

Winthrop = lambda date : TrackCollections( WinthropTrack , date )
Seattle  = lambda date : TrackCollections( SeattleTrack  , date )
Kailua   = lambda date : TrackCollections( KailuaTrack   , date )

