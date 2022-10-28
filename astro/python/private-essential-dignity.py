import pandas as pd

def dignityMatrix():

    c1 = ["sun","moon","mercury","venus","mars","jupiter","saturn"]
    c2 = [["Leo"],["Cancer"],["Gemini","Virgo"],["Libra","Taurus"],["Aries","Scorpius"],["Sagittarius","Pisces"],["Capricornus","Aquarius"]]
    c3 = [["Aquarius"],["Capricornus"],["Sagittarius","Pisces"],["Aries","Scorpius"],["Libra","Taurus"],["Gemini","Virgo"],["Cancer","Leo"]]
    c4 = ["Aries","Taurus","Virgo","Pisces","Capricornus","Cancer","Libra"]
    c5 = ["Libra","Scorpius","Pisces","Virgo","Cancer","Capricornus","Aries"]

    dMatrix = pd.DataFrame()
    dMatrix["dignity"] = c2
    dMatrix["detriment"] = c3
    dMatrix["exaltation"] = pd.Series( c4 ).apply( lambda x : [x] )
    dMatrix["fall"] = pd.Series( c5 ).apply( lambda x : [x] )
    dMatrix.index = c1
    return( dMatrix )


def houseMatrix():

    sign = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo","Libra","Scorpius","Sagittarius","Capricornus","Aquarius","Pisces"]
    ruler = ["mars","venus","mercury","moon","sun","mercury","venus","pluto","jupiter","saturn","uranus","neptune"]
    data = pd.DataFrame()
    data["ruler"] = ruler
    data.index = sign

    data["order"] = range(len(sign))
    data["polarity"] = data["order"].apply(lambda x : x % 2 )
    data["modality"] = data["order"].apply(lambda x : x % 3 )
    data["triplicity"] = data["order"].apply(lambda x : x % 4 )
    data["hexality"] = data["order"].apply(lambda x : x%6)

    polarity = {0:1 ,1 : -1}
    modality = { 0 : "cardinal" , 1: "fixed" , 2: "mutable"}
    triplicity = { 0 : "fire" , 1: "earth", 2: "air" , 3: "water"}

    data["polarity"] = data["polarity"].apply(lambda x : polarity.get(x))
    data["modality"] = data["modality"].apply(lambda x : modality.get(x))
    data["triplicity"] = data["triplicity"].apply(lambda x : triplicity.get(x))
    return(data)

def loadAstroData( filePath ):
    data = pd.read_csv(filePath,index_col=0)
    dm = dignityMatrix()
    together = pd.merge(data,dm,how="outer",left_on="planet",right_index=True)

    for column in dm.columns:
        together[column] = together.fillna("").apply(lambda x : x["constellation"] in x[column] , axis = 1)
    return(together)
