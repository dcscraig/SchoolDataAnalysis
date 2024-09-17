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


def findNearMiss(year,level,filename,subject_names):
    scn_to_name = data_store.readSCNtoName(year)
    subjects = data_store.readSchoolSubjects(year,level)
    grade_boundaries = data_store.readGradeBoundaries(level=level,year=year,subjects=subjects,marks=True)
    
    # subject_names = subjects["Course Title"]
    # subject_codes = subjects["Course"]
    # national_attainment = data_store.readSqaAttainment(year,level)

    data = data_store.readMarks(year,level,names=True)
    Odata = data_store.readMarks(year,level,names=True)
    
    #only process entries that have a band below the next grade up
    # 3 High B -> Low A
    # sel = data["Band"].isin([3,5,7,8])
    # data = data[sel]

    temp = data.groupby(["SCN","Course Title","Band","Forename","Surname"])["Mark"].sum()
    data = temp.reset_index()

    grade_boundaries[2] = grade_boundaries["A"]
    grade_boundaries[4] = grade_boundaries["B"]
    grade_boundaries[6] = grade_boundaries["C"]
    grade_boundaries[7] = grade_boundaries["D"]

    data["Band"] = (data["Band"]).astype('int32')
    near_miss = []

    for subject in subject_names:
        print (subject)
        # this needs to be worked on
        # any subject that can be taken in another language needs to be brought in
        t_subject = subject
        if (subject=="Nuadh-Eolas (Modern Studies)"):
            t_subject = "Modern Studies"
        if (subject=="Matamataig (Mathematics)"):
            t_subject = "Mathematics"
            
        subject_bounds = grade_boundaries[grade_boundaries["Subject"]==t_subject]
        print(subject_bounds)
        
        replace_dict = {}
        for i in [2,4,6,7]:
            replace_dict[i] = subject_bounds[i].iloc[0]

        entries = data[data["Course Title"]==subject].copy(deep=True)

        entries["Percentage"] = (entries["Mark"]/subject_bounds["Maxiumum Mark"].values*100).round(0)

        for i in "ABCD":
            entries[i] = subject_bounds[i].values[0]
        entries = entries.sort_values(["Surname"])
        entries.index = entries["SCN"]
        # entries = entries.drop(["SCN"],axis=1)
        
        temp = Odata[(Odata["Course Title"]==subject)&(Odata["SCN"].isin(entries["SCN"]))]

        components = temp[["SCN","Component","Title","Mark"]]
        
        for i in components["Component"].unique():
            temp = components[components["Component"]==i]
            temp.index = temp["SCN"]    
            temp[temp.Title.unique()[0]] = temp["Mark"]
            temp = temp[[temp.Title.unique()[0]]]
            entries = entries.join(temp)
        entries.to_excel("Output/subject marks/"+subject+"_"+str(level)+".xlsx")
     



subject_names = ["Graphic Communication","Computing Science","Practical Woodworking","Practical Metalworking","Practical Cookery"]
subject_names = ["Graphic Communication","Computing Science","Practical Woodworking","Practical Metalworking","Practical Cookery"]


# subject_names = []
# subject_names.append("Mathematics")
# subject_names.append("Matamataig (Mathematics)")
# subject_names.append("Applications of Mathematics")

findNearMiss(2024,75,"Output/N5Pupillist.xlsx",subject_names)

findNearMiss(2024,76,"Output/HPupillist.xlsx",subject_names)

exit()


