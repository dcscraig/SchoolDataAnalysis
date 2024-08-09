import pandas as pd
import numpy


def findExcellenceAwards(attainment):
    excellence_awards = attainment[attainment["Band"]==1]
    excellence_awards = excellence_awards.sort_values(["Level","Surname"])
    excellence_awards.to_csv("Excellenceawards.csv",index=False)


filename = "Data/SchoolResults/2024.xlsx"
temp = pd.read_excel(filename,header=9,thousands=",")
# only care about the band so just take the first component
# temp = temp[temp["Component"]==1]

print(temp[temp["SCN"]==120046004][["Course Title","Band","Mark"]])


exit()

attainment = temp[["SCN","Forename", "Surname","Band","Level","Course Title"]]
findExcellenceAwards(attainment)


attainment["Rank"] = 0
attainment["Points"] = 0


attFilename = "Data/tariffpoints.csv"
attVals = pd.read_csv(attFilename,header=0)


for level in [75,76,77]:
    levelVals = attVals[attVals["Level"]==level]
    for band in [1,2,3,4,5,6,7]:
        # attainment[(attainment["Band"]==band) & (attainment["Level"]==level)]["Points"] = levelVals[levelVals["Band"]==band]["Points"].values[0]
        # attainment[(attainment["Band"]==band) & (attainment["Level"]==level)]["Rank"] = levelVals[levelVals["Band"]==band]["Rank"].values[0]
        update = (attainment["Band"]==band) & (attainment["Level"]==level) 

        attainment.loc[update,"Points"] = levelVals[levelVals["Band"]==band]["Points"].values[0]
        attainment.loc[update,"Rank"] = levelVals[levelVals["Band"]==band]["Rank"].values[0]
        
        
        # = levelVals[levelVals["Band"]==band]["Rank"].values[0]
        
        # exit()
        
attainment.to_csv("TEST.csv")
print(attainment)        

print(attainment.groupby("SCN").sum("Points"))
exit()
print(attVals)





subject = "Graphic Communication"
level = 76
subject_attainment = attainment[(attainment["Course Title"]==subject) & (attainment["Level"]==level)].sort_values("Band")




print(subject)
print(subject_attainment)

for pupil in subject_attainment["SCN"]:
    temp = attainment[attainment["SCN"]==pupil].sort_values("Band")
    temp = temp[temp["Course Title"]!=subject]


    print(temp)


