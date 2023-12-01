import math
import pandas as pd

def get_nearest(type, lat, long):
    if type=="Law and Order":
        police_db = pd.read_csv("hyd_police_stn_jurisdictions.csv")
        nearest=[]
        count=0
        for index, entry in police_db.iterrows():
            distance = 3959 * math.acos( math.cos( math.radians(lat) ) * math.cos( math.radians( float(entry["Y"]) ) ) * 
math.cos( math.radians( long ) - math.radians(float(entry["X"])) ) + math.sin( float(math.radians(entry["Y"] )) ) * 
math.sin( math.radians( lat ) ) )
            if distance < 15:
                nearest.append([entry, distance])
                count +=1
            if count==3:
                break
        return sorted(nearest, key=lambda x: x[1])
    if type=="Fire":
        fire_db = pd.read_csv("hyderabad fire stations.csv")
        nearest=[]
        count=0
        for index, entry in fire_db.iterrows():
            distance = 3959 * math.acos( math.cos( math.radians(lat) ) * math.cos( math.radians( float(entry["Y"]) ) ) * 
math.cos( math.radians( long ) - math.radians(float(entry["X"])) ) + math.sin( float(math.radians(entry["Y"] )) ) * 
math.sin( math.radians( lat ) ) )
            if distance < 15:
                nearest.append([list(entry), distance])
                count +=1
            if count==3:
                break
        
        
        return sorted(nearest, key=lambda x: x[1])

print(get_nearest("Fire",17.4553,78.6665)[0][0])