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

def loadAstroData( filePath ):
    data = pd.read_csv(filePath,index_col=0)
    dm = dignityMatrix()
    together = pd.merge(data,dm,how="outer",left_on="planet",right_index=True)

    for column in dm.columns:
        together[column] = together.fillna("").apply(lambda x : x["constellation"] in x[column] , axis = 1)
    return(together)
