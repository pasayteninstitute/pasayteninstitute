import datetime as dt
from astropy.time import Time
from astropy import coordinates as c
        
def getTime( dateTimeString , utcDelta = 7 ):
    formatString = "%Y-%m-%d %H:%M"
    time = dt.datetime.strptime( dateTimeString , formatString ) + dt.timedelta(hours = utcDelta )
    return(Time(time.strftime(formatString)))
    
def observationPoint( lat , lon , ele ):
    return(c.earth.EarthLocation.from_geodetic(lon,lat,ele))
    
def getWinthrop():
    return( observationPoint( 48.4779 , -120.1862 , 542 ) )    
    
def getPlanets( timeString , location = "" ):
    
    time = getTime( timeString )
    
    if location == "":
        location = getWinthrop()
    
    planets = {}
    with c.solar_system_ephemeris.set("builtin"):
        for body in c.solar_system_ephemeris.bodies:
            planets[body] = c.get_body( body , time , location )
    
    observations = {}
    constellations = {}
    
    aaFormat = c.AltAz( location = location , obstime = time )
    for planet in planets:
        observations[planet] = planets[planet].transform_to(aaFormat)
        constellations[planet] = planets[planet].get_constellation()
        
    return({ "planets" : planets , "observations" : observations , "constellations" : constellations })



if __name__ == "__main__":

    ps = getPlanets("2022-10-25 20:00")
    print(ps["observations"])
