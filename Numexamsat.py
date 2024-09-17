import pandas as pd
import numpy
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def findExcellenceAwards(attainment):
    excellence_awards = attainment[attainment["Band"]==1]
    excellence_awards = excellence_awards.sort_values(["Level","Surname"])
    excellence_awards.to_csv("Output/Excellenceawards.csv",index=False)


filename = "Data/SchoolResults/2024.xlsx"
temp = pd.read_excel(filename,header=9,thousands=",")
# only care about the band so just take the first component
temp = temp[temp["Component"]==1]


attainment = temp[["SCN","Forename", "Surname","Band","Level","Course Title"]]
# findExcellenceAwards(attainment)

attainment["Rank"] = 0
attainment["Points"] = 0

attFilename = "Data/tariffpoints.csv"
attVals = pd.read_csv(attFilename,header=0)

for level in [75,76,77]:
    levelVals = attVals[attVals["Level"]==level]
    for band in [1,2,3,4,5,6,7]:
        update = (attainment["Band"]==band) & (attainment["Level"]==level) 
        attainment.loc[update,"Points"] = levelVals[levelVals["Band"]==band]["Points"].values[0]
        attainment.loc[update,"Rank"] = levelVals[levelVals["Band"]==band]["Rank"].values[0]



def NumberExamSatBySubjectAndPupil(filename,attainment,level):
    filename = "N5 "+filename
  
    # delete those pupils who failed?
    # attainment = attainment[attainment["Band"] <=7] 
    pdf = PdfPages("Output/"+filename+".pdf")
    fig, ax =plt.subplots(1,1,figsize=(11.69,8.27))


    levelattainment = attainment[attainment["Level"]==76]
    level_pupils = levelattainment["SCN"].unique()
    level_mask = ~attainment["SCN"].isin(level_pupils)
    attainment = attainment[level_mask]



    subjects = attainment[attainment["Level"]==level]
    subjects = pd.unique(subjects["Course Title"])
    data_n5sat = {}
    subject_numexams = []
    for subject in subjects:
        pupils = attainment[(attainment["Course Title"]==subject) & (attainment["Level"]==level)]["SCN"].values
        test = attainment[attainment["SCN"].isin(pupils)]
        test["SCN"] = test["SCN"].astype(str)
        test = test.sort_values(["SCN","Points"],ascending=False)
        comparison = test[test["Course Title"]!=subject]
        subject_attain = test[test["Course Title"]==subject]
        num_n5sat = test.groupby("SCN").count()["Points"]
        data_n5sat[subject] = num_n5sat
        subject_numexams.append([subject,num_n5sat.median()])

    subject_numexams = pd.DataFrame(subject_numexams,columns=["Course Title","Num Exams"]).sort_values("Num Exams",ascending=False)

    subject_numexams = subject_numexams["Course Title"].values

    data_n5sat = pd.DataFrame.from_dict(data_n5sat)

    data_n5sat = data_n5sat[subject_numexams] 

    labels = data_n5sat.columns.values

    for i in range(len(labels)):
        labels[i] = labels[i].replace(" ","\n")

    data_n5sat.columns = labels

    sns.boxplot(data=data_n5sat,medianprops={"color": "k", "linewidth": 2,'linestyle': '--'},ax=ax)
    # plot.set_xticks(labels,)
    ax.set_title("Number of N5 Exams passed by pupils who achieved by each subject")

    ax.set_xticklabels(labels, rotation=90)

    count = 0
    for i in data_n5sat.columns.values:
        ax.text(count-0.2, data_n5sat[i].quantile(0.75) -(0.5*(data_n5sat[i].quantile(0.75) -data_n5sat[i].quantile(0.25))),data_n5sat[i].count(),color="black",size=12)
        count +=1
    
    pdf.savefig()
    pdf.close()
    plt.close()


def subjectAttainmentandNumexams(filename,attainment,level):
    filename = "N5 "+filename
  
    # delete those pupils who failed?
    # attainment = attainment[attainment["Band"] <=7] 
    pdf = PdfPages("Output/"+filename+".pdf")
    fig, ax =plt.subplots(1,1,figsize=(11.69,8.27))
    fig.tight_layout()

    # removes pupils who sat 1 or more higher
    # exams
    levelattainment = attainment[attainment["Level"]==76]
    level_pupils = levelattainment["SCN"].unique()
    level_mask = ~attainment["SCN"].isin(level_pupils)
    attainment = attainment[level_mask]

    subjects = attainment[attainment["Level"]==level]
    subjects = pd.unique(subjects["Course Title"])
    data_n5sat = {}
    subject_numexams = []
    new_data = {"Band":[0]}
    new_data["Band"] = []
    new_data["NumExams"] = []
    new_data["Course Title"] = []
    
    new_data = pd.DataFrame(new_data)
    subjects = ["Physics","Computing Science","Graphic Communication","Practical Woodworking","Practical Cookery","French"]
    for subject in subjects:
        pupils = attainment[(attainment["Course Title"]==subject) & (attainment["Level"]==level)]["SCN"].values
        test = attainment[attainment["SCN"].isin(pupils)]
        test["SCN"] = test["SCN"].astype(str)
        test = test.sort_values(["SCN","Band"],ascending=True)

        test['NumExams'] = test.groupby('SCN', sort=False)['Band'].transform('count')
        comparison = test[test["Course Title"]!=subject]
        subject_attain = test[test["Course Title"]==subject]
        subject_attain = subject_attain.sort_values("Band")
        new_data = pd.concat([new_data, subject_attain[["Band","NumExams","Course Title"]]], sort=False)


    new_data = new_data.replace("Computing Science", "Compsci")
    new_data = new_data.replace("Graphic Communication", "Graphcomm")
    new_data = new_data.replace("Practical Woodworking", "Woodwork")
    new_data = new_data.replace("Practical Cookery", "Cookery")
    
    

        
    # sns.stripplot(data=new_data, x="Band", y="NumExams",hue="Course Title")
    # sns.jointplot(data=new_data,x="Band", y="NumExams", kind="hex", color="#4CB391")
    # sns.lmplot(data=new_data,x="Band", y="NumExams", hue="Course Title",height=5)
    sns.pairplot(new_data, hue="Course Title")
    pdf.savefig()
    pdf.close()
    plt.close()





  
# will only work with n5 
filename = " ExamsSat"

NumberExamSatBySubjectAndPupil(filename,attainment,75)

filename = " BandExamsSat Experimental"
subjectAttainmentandNumexams(filename,attainment,75)
exit()

