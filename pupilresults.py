import pandas as pd
import numpy
import seaborn as sns
import matplotlib.pyplot as plt

def findExcellenceAwards(attainment):
    excellence_awards = attainment[attainment["Band"]==1]
    excellence_awards = excellence_awards.sort_values(["Level","Surname"])
    excellence_awards.to_csv("Output/Excellenceawards.csv",index=False)


filename = "Data/SchoolResults/2024.xlsx"
temp = pd.read_excel(filename,header=9,thousands=",")
# only care about the band so just take the first component
temp = temp[temp["Component"]==1]


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
        
attainment.to_csv("Output/TEST.csv")
print(attainment)        

# find all the pupils for a give course and level
subject = "Chemistry"
level = 75

pupils = attainment[(attainment["Course Title"]==subject) & (attainment["Level"]==level)]["SCN"].values

# print(pupils)

# print(attainment)

test = attainment[attainment["SCN"].isin(pupils)]
test["SCN"] = test["SCN"].astype(str)
test = test.sort_values(["SCN","Points"],ascending=False)

# sns.boxplot(data=test,x="SCN",y="Points")
# plt.show()
# test.sort_values(["Points"])
comparison = test[test["Course Title"]!=subject]
subject_attain = test[test["Course Title"]==subject]
# sns.boxplot(data=comparison, x="SCN", y="Points")
# sns.swarmplot(data=subject_attain, x="SCN", y="Points")


sns.boxplot(data=comparison, x="SCN", y="Points")
sns.scatterplot(data=subject_attain,marker="*",s=100 , x="SCN", y="Points", hue="Course Title")
sns.lineplot(data=subject_attain, x="SCN", y="Points")

# print(subject_attain)
plt.show()


exit()


temp = attainment.groupby("SCN").sum("Points")
temp = temp.sort_values("Points")
print(temp)
attainment = attainment[attainment["Level"]==75]
sns.swarmplot(data=attainment, x="Points", y="Points", hue="Course Title")

plt.show()

exit()


subject = "Graphic Communication"
level = 76
subject_attainment = attainment[(attainment["Course Title"]==subject) & (attainment["Level"]==level)].sort_values("Band")




print(subject)
print(subject_attainment)

for pupil in subject_attainment["SCN"]:
    temp = attainment[attainment["SCN"]==pupil].sort_values("Band")
    temp = temp[temp["Course Title"]!=subject]


    print(temp)


