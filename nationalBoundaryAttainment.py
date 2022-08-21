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

year = 2022
for level in [75,76]:

    
    filename = " NationalAttainmentBoundary"
    if level==75:
        filename = "National 5 "+filename
    else:
        filename = "Higher "+filename
    
    pdf = PdfPages(filename+".pdf")
    fig, ax =plt.subplots(1,1,figsize=(11.69,8.27))
    

    subjects = data_store.readSchoolSubjects(year,level)
    grade_boundaries = data_store.readGradeBoundaries(level=level,year=year,subjects=subjects,marks=True)

    print(subjects)
    subject_names = subjects["Course Title"]
    subject_codes = subjects["Course"]
    national_attainment = data_store.readSqaAttainment(year,level)

    # seperate attainment stats are not available for 
    
    

    national_components = data_store.readComponentsSqa(year,level)
  
  
    a_pass = 100*national_attainment["A"]/national_attainment["Total"]
    a_pass = a_pass.round(2)

    national_results = pd.DataFrame({"Course":national_attainment["Course"],"A Pass":a_pass})

    temp = national_results["Course"].isin(subject_names)
    national_results = national_results[temp]


    boundaries = grade_boundaries[grade_boundaries["Subject"].isin(subject_names)]

    boundaries["A Boundary"] = (100*boundaries["A"]/boundaries["Maxiumum Mark"]).round(2)
    a_bound = boundaries["A Boundary"]



    temp = national_results.set_index('Course').join(boundaries.set_index('Subject'))

    data = temp[["A Pass","A Boundary"]]
    data["Course"] = data.index
    names = data.index
    fig, ax =plt.subplots(1,1,figsize=(11.69,8.27))

    ax.scatter(data["A Pass"],data["A Boundary"])

    for index in range(len(data)):
        subject = data.iloc[index].to_dict()
        
        
        if len(subject["Course"].split(" "))>1:
            temp = ""
            for sub in subject["Course"].split(" "):
                temp+= sub[0:4]+" "
            ax.annotate(temp, (subject["A Pass"], subject["A Boundary"]))
        elif len(subject["Course"])>20:
            ax.annotate(subject["Course"][0:10], (subject["A Pass"], subject["A Boundary"]))
        else:
            ax.annotate(subject["Course"], (subject["A Pass"], subject["A Boundary"]))
            
   
    ax.set_xlabel("National A Pass %")
    ax.set_ylabel("National A Boundary %")
    if (level==75):
        ax.set_title("National 5 National A vs A Boundary")
    else:
        ax.set_title("Higher National A vs A Boundary")
    
    ax.set_xlim(a_pass.min()*0.9, a_pass.max()*1.1)
    ax.set_ylim(a_bound.min()*0.9, a_bound.max()*1.1)
    
    pdf.savefig()
    plt.close()
    pdf.close()



