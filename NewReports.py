from copy import deepcopy
import numpy
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as lines
import matplotlib as mpl
import seaborn as sns
import seaborn.objects as so
import textwrap
import concurrent.futures
import time
import itertools
from ReportWriter import ReportWriter


# first version 


combine_courses = {}

to_english ={}
to_english["Nuadh-Eolas (Modern Studies)"] = "Modern Studies"
to_english["Nuadh-eòlas (Modern Studies)"] = "Modern Studies"

to_english["Matamataig"] = "Mathematics"
to_english["Matamataig (Mathematics)"] ="Mathematics"
to_english["Gniomhachas Matamataigs"] = "Applications of Mathematics"
to_english["Cruinn-eolas"] = "Geography"
to_english["Eachdraidh"] = "History"

to_alt ={}
for i in to_english.keys():
    to_alt[to_english[i]] = i
combine_courses["english"] = to_english
combine_courses["alt"] = to_alt

from dataimport import DataStore
data_store = DataStore()


def createGraph(subject,level,nationalgrades,allGrades,national_components,allMarks,selected_year):
    sns.set_style("darkgrid")

    fig, ax =plt.subplots(1,1,figsize=(11.69,8.27))
    ax.set(ylabel='Percentage')
    temp = nationalgrades[(nationalgrades["Subject"]==subject)&(nationalgrades["Year"]==selected_year)]
    temp = temp.assign(Type = "National")
    temp1 = allGrades[(allGrades["Subject"]==subject)&(allGrades["Year"]==selected_year)]
    temp1 = temp1.assign(Type = "School")
    
    temp = pd.concat([temp1,temp])

    temp = temp.assign(Percentage=temp["Percentage"].round())
    
    sns.set(font_scale=2)
    p = sns.histplot(data=temp, x='Type', hue='Grade', weights='Percentage', discrete=True, multiple='stack', shrink=0.8,hue_order= ["A","B","C","D","NA"],ax=ax)
    # ax = sns.lineplot(data=allGrades[allGrades["Subject"]=="English"], x='Year', hue='Grade', y='Percentage', hue_order= ["A","B","C","D","NA"],markers=True)
    # ax = sns.lineplot(data=allGrades[nationalgrades["Subject"]=="English"], x='Year', hue='Grade', y='Percentage', hue_order= ["A","B","C","D","NA"],linestyle='dotted')

    for c in ax.containers:
        labels = [round(v.get_height(),2) if v.get_height() > 0 else '' for v in c]
        ax.bar_label(c, labels=labels, label_type='center')
    p.set_xlabel("")
    p.set_ylabel("Percentage",fontdict={"size":20})
    p.set_xticks(["School","National"])
    p.set_xticklabels(["School","National"],fontdict={"size":20})
    
    p.set_yticks([0,20,40,60,80,100])
    p.set_yticklabels([0,20,40,60,80,100],fontdict={"size":20})
    
    sns.move_legend(ax, "lower center",ncol=5, bbox_to_anchor=(0.5, 1))
    # temp = temp[(temp["Type"]=="School")]
    # axes[1].table(cellText=temp[["Num"]].values,
    #             colLabels=["School Count"],
    #             rowLabels=["A","B","C","D","NA"])
    #         #   bbox=(0.7, .2, 0.5, 0.5))
    plt.tight_layout()
    plt.savefig("Output/reportgraphs/comp/"+subject+"_"+str(level)+".png")
    plt.close()


def drawHistoricGraph(data,xlabels,fname):
    sns.set_style("darkgrid")
    fig, ax =plt.subplots(1,1,figsize=(11.69,6.27))
    ax.set(ylabel='Percentage')
    sns.set(font_scale=2)
    p = sns.histplot(data=data, x='Year', hue='Grade', weights='Percentage', discrete=True, multiple='stack', shrink=0.8,hue_order= ["A","B","C","D","NA"],ax=ax)
    
    for c in ax.containers:
        labels = [round(v.get_height(),2) if v.get_height() > 0 else '' for v in c]
        ax.bar_label(c, labels=labels, label_type='center')
    
    p.set_xlabel("")
    p.set_ylabel("Percentage",fontdict={"size":20})
    p.set_xticks(xlabels)
    p.set_xticklabels(xlabels,fontdict={"size":20})
    
    p.invert_xaxis()
    sns.move_legend(ax, "upper left",ncol=1, bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.savefig(fname)
    plt.close()
    

    

def createHistoricalGraph(subject,level,nationalgrades,allGrades,national_components,allMarks,years):
    
    national = nationalgrades[nationalgrades["Subject"]==subject]
    national = national.assign(Type = "National")
    school = allGrades[(allGrades["Subject"]==subject)]
    school = school.assign(Type = "School")
    
    national = national.assign(Percentage=national["Percentage"].round())
    school = school.assign(Percentage=school["Percentage"].round())

    
    # temp = pd.concat([temp1,temp])
   
    fname = "Output/reportgraphs/historic/"+subject+"_"+str(level)+"_school.png"
    drawHistoricGraph(school,years,fname)
    fname = "Output/reportgraphs/historic/"+subject+"_"+str(level)+"_national.png"
    drawHistoricGraph(national,years,fname)



def createReport(selected_year,level,name):
    # filename = " Overview"
    # title = name+"\n "
    # if level==75:
    #     filename = "National 5 "+filename
    #     title += "National 5\n"
    # else:
    #     filename = "Higher "+filename
    #     title += "Higher\n"
    # title += str(year-1)+"-"+str(year)
    
    # pdf = PdfPages("Output/"+filename+".pdf")
    # fig, ax =plt.subplots(1,1,figsize=(11.69,8.27))
    # makeFrontPage(title,ax)
    # pdf.savefig()
    # plt.close()

    courses = data_store.readSchoolSubjects(selected_year,level)

    num_years = 3
    temp_year = selected_year - num_years+1
    years = []
    for i in range(num_years):
        years.append(temp_year)
        temp_year += 1
    years= years[::-1]


    allgradeboundaries = {}
    allnational_attainment = {}
    allnational_components ={}

    subjects = courses["Course Title"]


    allGrades = []
    nationalgrades = []
    national_components = {}
    allMarks = {}
        
    for year in years:
        # allgradeboundaries[year] = data_store.readGradeBoundaries(level=level,year=year,subjects=subjects,marks=False)

        temp_components = data_store.readComponentsSqa(year,level)
        temp_components = temp_components[temp_components["Subject"].isin(subjects)]
        temp_components["Year"] = year

        
        national_components[year] = temp_components
        
        temp =  data_store.readSqaAttainment(year,level)
        
        temp = temp[["Course","A","B","C","D","NA","Total"]]
        totalgrades = temp[temp["Course"].isin(subjects)]
        for ind in totalgrades.index:
             for grade in ["A","B","C","D","NA"]:  
                temp = []
                temp.append(totalgrades['Course'][ind])
                temp.append(level)
                temp.append(year)
                temp.append(grade)
                temp.append(totalgrades[grade][ind])
                temp.append(totalgrades["Total"][ind])
                temp.append(100*(totalgrades[grade][ind]/totalgrades["Total"][ind]))
                nationalgrades.append(temp) 
             
        
        # allnational_components[year] = data_store.readComponentsSqa(year,level)
        for subject in subjects:
            school_attainment = data_store.readRawMarks(year,level,subject,remove_incomplete=True)
            
            temp = school_attainment.groupby("Component")["Mark"].agg(["min","max","mean","median"])
            temp = temp.round(1)
            temp["Title"] = school_attainment["Title"].unique()
            
            # temp = temp.reset_index()
            year_data = temp.to_dict()
            temp = allMarks.get(subject,{})
            temp[year] = year_data
            allMarks[subject] = temp
            
            school_grades = school_attainment.drop_duplicates(subset=["SCN"]).copy(deep=True)
            
            # reduce bands to grades
            bands = [1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0]
            grades = ["A","A","B","B","C","C","D","NA","NA"]
            temp = school_grades["Band"]
            temp = temp.replace(bands,grades)
            
            school_grades = temp.value_counts().to_dict()
            grades = ["A","B","C","D","NA"]
            total = 0
            for grade in grades:
                if not grade in school_grades.keys():
                    school_grades[grade] = 0
                else:
                    total += school_grades[grade]
            
            school_grades["Total"] = total
            grades = ["A","B","C","D","NA"]
            for grade in grades:
                if (total==0):
                    allGrades.append([subject,level,year,grade,total,school_grades[grade],0])
                else:
                    allGrades.append([subject,level,year,grade,total,school_grades[grade],(school_grades[grade]/total)*100])

    
    temp = []
    for i in national_components:
        temp.append(national_components[i])
    
    national_components = pd.concat(temp)

    
    cols = national_components.columns.values
    national_components = national_components.melt(id_vars=["Subject","Year"], value_vars=cols)
    national_components = national_components[national_components["value"]!="[c]"]
    national_components = national_components[national_components["value"]!="[z]"]
    compnum = national_components["variable"].str.extract('(\\d)')
    national_components = national_components.assign(CompNum=compnum)
    


    cols = ["Subject","Level","Year","Grade","Total","Num","Percentage"]
    nationalgrades = pd.DataFrame(nationalgrades,columns=cols)
    
    cols = ["Subject","Level","Year","Grade","Total","Num","Percentage"]
    allGrades = pd.DataFrame(allGrades,columns=cols)

    # allGrades["Year"] = allGrades["Year"].astype(str) 
    allGrades["Num"] = allGrades["Num"].astype(int) 
    allGrades["Percentage"] = allGrades["Percentage"].round(1) 
    

    # with concurrent.futures.ProcessPoolExecutor(12) as executor:
    #     start_time = time.perf_counter()
    #     selected_year = 2024
    #     result = list(executor.map(createGraph, subjects,itertools.repeat(level),itertools.repeat(nationalgrades),itertools.repeat(allGrades),itertools.repeat(national_components),itertools.repeat(allMarks),itertools.repeat(selected_year)))
    #     finish_time = time.perf_counter()
    # print(f"Program finished in {finish_time-start_time} seconds")
    for subject in subjects:
        createGraph(subject,level,nationalgrades,allGrades,national_components,allMarks,selected_year)
        createHistoricalGraph(subject,level,nationalgrades,allGrades,national_components,allMarks,years)
    
    for subject in subjects:
        subject_nat_comp = national_components[(national_components["Subject"]==subject)]
        output = {}
        for temp_year in national_components["Year"].unique():
            res = {}
            for measure in ["Maximum","Mean"]:
                temp = subject_nat_comp[subject_nat_comp["Year"]==temp_year]
                temp = temp[temp['variable'].str.contains(measure,na=False)][["CompNum","value"]]
                temp = temp.dropna()
                
                temp["CompNum"] = temp["CompNum"].astype(int) 
                temp = temp.set_index("CompNum")
                
                temp = temp["value"].astype(float).to_dict()
                
                res[measure.lower()] = temp
            output[temp_year] = res
        
        subject_nat_comp = output
        
        subject_grades = allGrades[allGrades["Subject"]==subject]
        
        ReportWriter(subject,level,selected_year,years,subject_grades,allMarks[subject],subject_nat_comp)



if __name__=='__main__':
    test = False
    institution = "Portree High School"
    year = 2024
    createReport(year,75,institution)
    createReport(year,76,institution)
    
    exit()
