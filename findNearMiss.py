import numpy
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as lines
import seaborn as sns
import textwrap
# matplotlib.style.use('ggplot')
from dataimport import DataStore

data_store = DataStore()


def findNearMiss(year,level,filename):
    scn_to_name = data_store.readSCNtoName(year)
    subjects = data_store.readSchoolSubjects(year,level)
    grade_boundaries = data_store.readGradeBoundaries(level=level,year=year,subjects=subjects,marks=True)
    subject_names = subjects["Course Title"]
    subject_codes = subjects["Course"]
    national_attainment = data_store.readSqaAttainment(year,level)

    data = data_store.readMarks(year,level,names=True)
    #only process entries that have a band below the next grade up
    # 3 High B -> Low A
    sel = data["Band"].isin([3,5,7,8])
    data = data[sel]

    temp = data.groupby(["SCN","Course Title","Band","Forename","Surname"])["Mark"].sum()
    data = temp.reset_index()

    grade_boundaries[2] = grade_boundaries["A"]
    grade_boundaries[4] = grade_boundaries["B"]
    grade_boundaries[6] = grade_boundaries["C"]
    grade_boundaries[7] = grade_boundaries["D"]

    data["ABand"] = (data["Band"]-1).astype('int32')
    near_miss = []
    for subject in subject_names:
        print (subject)
        # this needs to be worked on
        # any subject that can be taken in another language needs to be brought in
        if (subject=="Nuadh-Eolas (Modern Studies)"):
            subject = "Modern Studies"
        subject_bounds = grade_boundaries[grade_boundaries["Subject"]==subject]

        replace_dict = {}
        for i in [2,4,6,7]:
            replace_dict[i] = subject_bounds[i].iloc[0]

        entries = data[data["Course Title"]==subject].copy(deep=True)

        entries["AMark"] = entries["ABand"].replace(replace_dict)
        entries["Diff"] = entries["AMark"]-entries["Mark"]
        

        temp = entries[entries["Diff"]<=2]
        
        if len(temp)!=0:
            near_miss.append(temp)
        

    data = pd.DataFrame(near_miss[0])
    for i in range(1,len(near_miss)):
        data = pd.concat([data,near_miss[i]])

    data.sort_values(by=["Diff","Course Title"],inplace=True)
    data["Marks Needed"] = data["Diff"]

    data = data[["SCN","Forename","Surname","Course Title","Band","Marks Needed"]]
    data.to_excel(filename)  


findNearMiss(2022,75,"National5_nearmiss.xlsx")
findNearMiss(2022,76,"Higher_nearmiss.xlsx")

exit()


