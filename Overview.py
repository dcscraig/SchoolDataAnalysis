from copy import deepcopy
import numpy
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as lines
import seaborn as sns
import textwrap
# matplotlib.style.use('ggplot')


combine_courses = {}

to_english ={}
to_english["Nuadh-Eolas (Modern Studies)"] = "Modern Studies"
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


def getMarks(level,subject,data,combine=True):
    years = [2017,2018,2019,2022]
    marks = {}
    for year in years:
        temp = data.readTotalMarks(year,level,subject)
        # need to combine a few subjects as the sqa 

#       data for courses available in different languages are assigned the same grade boundaries and are grouped as a single course for reporting purposes.
#       These courses are as follows:
#       
#       Mandarin (Traditional), Mandarin (Simplified) and Cantonese are reported as Chinese Languages for each level.
#       Mathematics and Matamataig are reported as Mathematics for each level.
#       Applications of Mathematics and Gniomhachas Matamataigs are reported as Applications of Mathematics.
#       Geography and Cruinn-eolas are reported as Geography for each level.
#       History and Eachdraidh are reported as History for each level.
#       Modern Studies and Nuadh-Eolas are reported as Modern Studies for each level.

#       !!!!!!! the sqa are not consistent with the use of gaelic spelling this may not work! modern studies is know to work
#       I have no data to check the chinese languages 
        if combine:
            if subject in ["Modern Studies","History", "Geography","Applications of Mathematics","Mathematics", "Mandarin (Traditional)", "Mandarin (Simplified)","Cantonese"]:
                if subject =="Modern Studies":
                    other_lang = data.readTotalMarks(year,level,"Nuadh-Eolas (Modern Studies)")
                    if(len(other_lang)!=0):
                        temp = numpy.concatenate((temp,other_lang))
                elif subject =="Mathematics":
                    other_lang = data.readTotalMarks(year,level,"Matamataig")
                    if(len(other_lang)!=0):
                        temp = numpy.concatenate((temp,other_lang))
                elif subject =="Applications of Mathematics":
                    other_lang = data.readTotalMarks(year,level,"Gniomhachas Matamataigs")
                    if(len(other_lang)!=0):
                        temp = numpy.concatenate((temp,other_lang))
                elif subject =="Geography":
                    other_lang = data.readTotalMarks(year,level,"Cruinn-eolas")
                    if(len(other_lang)!=0):
                        temp = numpy.concatenate((temp,other_lang))
                elif subject =="History":
                    other_lang = data.readTotalMarks(year,level,"Eachdraidh")
                    if(len(other_lang)!=0):
                        temp = numpy.concatenate((temp,other_lang))
        marks[year] = temp
    return marks

def createSubjectMarkTrends(data,level,data_store,title):
    pdf = PdfPages(title)
    cols = []
    for grade in ["Max","A","B","C","D"]:
        for year in [2017,2018,2019,2022]:
            cols.append(grade+" "+str(year))
    ind = data["Subject"]
    data = data[cols]
    data.index = ind

    for index, row in data.iterrows():
        fig, ax = plt.subplots(constrained_layout=True,figsize=(11.69,8.27))
        ax.set_title(index)
        #max
        max_val = row[0:4].values
        # ax.plot(100*(row[0:4].values/max_val),ls='--',label="Max")
        ax.plot(100*(row[4:8].values/max_val),ls='--',marker='*',label="A")
        ax.plot(100*(row[8:12].values/max_val),ls='--',marker='*',label="B")
        ax.plot(100*(row[12:16].values/max_val),ls='--',marker='*',label="C")
        ax.plot(100*(row[16:].values/max_val),ls='--',marker='*',label="D")
        ax.set_ylim([0,100])
        ax.set_xlabel("Years")
        ax.set_ylabel("%")
        
        marks = getMarks(level,index,data_store,combine=True)
        count = 0
        for year in [2017,2018,2019,2022]:
            if (len(marks[year])!=0):
                percentages =100*(marks[year]/max_val[count]) 
                ax.boxplot(percentages, positions= [count]) 
                ax.text(count+0.1, numpy.median(percentages), len(percentages),style='normal', size= 12)       
            count +=1
        ax.set_xticks([0,1,2,3])
        ax.set_xticklabels([2017,2018,2019,2021])
        plt.legend()
        pdf.savefig()
        plt.close()
    pdf.close()

def makeFrontPage(title, plot):
	plot.text(0.5, 0.5, title, wrap=True, horizontalalignment='center', fontsize=36)
	plot.axis('off')


def estimateMarkDistribution(entries, boundaries):
    percent = {}
    for j in ["A","B","C","D","NA"]:
        temp = round(100*(entries[j]/entries["Total"]))
        percent[j] = temp
    
    top_est = (boundaries['Maxiumum Mark']-boundaries["A"])/2.0 
    top_est += boundaries["A"]
    
    a_marks = numpy.random.randint(boundaries["A"],top_est,size=percent["A"])
    b_marks = numpy.random.randint(boundaries["B"],boundaries["A"],size=percent["B"])
    c_marks = numpy.random.randint(boundaries["C"],boundaries["B"],size=percent["C"])
    d_marks = numpy.random.randint(boundaries["D"],boundaries["C"],size=percent["D"])
    f_marks = numpy.random.randint(boundaries["D"]/2.0,boundaries["D"],size=percent["B"])
    
    marks = []
    marks.append(a_marks)
    marks.append(b_marks)
    marks.append(c_marks)
    marks.append(d_marks)
    marks.append(f_marks)
    res = []
    for j in marks:
        for k in j:
            res.append(k)
    return res

def makeGradeTable(national,school,plot):
    # plot.title.set_text('Grades')
    plot.text(0.5,0.9,'Grades',horizontalalignment='center', fontsize=12)

    

    column_labels = ["School % (number of entries)","National Performance %"]
    row_labels = ["A","B","C","D","NA"]

    temp = []
    total = 0

    for i in row_labels:
        temp.append([str(round(100*(school[i]/school["Total"]),0))+"("+str(school[i])+")",round(100*float(national[i])/national["Total"],0)])
        total += school[i]
    table = plot.table(cellText=temp,colLabels=column_labels,rowLabels = row_labels,loc='center')
    table.set_fontsize(12)
    table.scale(1, 1.5)
    plot.axis('off')

    plot.text(0.5, 0.01, "Number of Entries: "+ str(total) , wrap=True, horizontalalignment='center', fontsize=12)
	


def makeGradesGraph(national_data,school_data,boundaries,plot):
    diverging_colors = sns.color_palette("hls", 5)[::-1]
    plot.title.set_text('School vs National Grades')
    school_per = []
    national_per = []
    
    grades = ["A","B","C","D","NA"]
    count = 4

    for grade in grades:
        school_per = school_data[grade]/school_data["Total"]
        national_per = national_data[grade]/national_data["Total"]
        plot.scatter(national_per*100,school_per*100,label= grade,color= diverging_colors[4-count])
        count -= 1
    plot.axline((0, 0),[70,70], color="black",linestyle="--")
    plot.legend()
    
    plot.set_xlabel("National %")
    plot.set_ylabel("School %")
        


    # plot.set_xlim(0,100)
    # plot.set_ylim(0,100)
    
def makeComponentTable(school,national,plot):
    # plot.title.set_text('Component Marks',pad=10)
    plot.text(0.5,0.9,'Component Marks',horizontalalignment='center', fontsize=12)

    num_comp = (len(school))
    temp = {}
    for i in range(num_comp):
        temp["National Mean"] = []
        temp["National Max"] = []
  
    national = national.iloc[0].to_dict()
    row_labels = []
    comp_names = []
    for i in range(num_comp):
        temp["National Mean"].append(national["Component "+str(i+1)+" Mean Mark"]) 
        temp["National Max"].append(national["Component "+str(i+1)+" Maximum Mark"])
        row_labels.append("C"+str(i+1))
        comp_names.append(national["Component "+str(i+1) +" Name"])
        
    data = school.copy(deep=True)
    data["National Mean"] = temp["National Mean"]
    data["National Max"] = temp["National Max"]
    data["Diff"] = data["School Mean"] - data["National Mean"].astype(float)
    data["Diff"] = data["Diff"].round(2)
    data["Diff %"] = (100*(data["Diff"]/data["National Max"])).round(0)
        
    data["School Mean"] = data["School Mean"].round(2)
    
   
    # for i in range(num_comp):
    #     temp["National Mean"] = temp["National Mean"].append
    #     temp["National Maxiumum Mark"] = []
        
    #     "Component "+str(i)+" Mean Mark"
    #     "Component "+str(i)+" Maximum Mark"
    
    cols = ["School Mean","National Mean","Diff","Diff %", "School Max","National Max"]
    data = data[cols]
    
    table = plot.table(cellText=data.values, colLabels=data.columns,rowLabels = row_labels, loc='center',fontsize=16)
    table.set_fontsize(18)
    if len(data)<4:
        table.scale(1, 3)
    else:
        table.scale(1, 1.5)
    
    caption = ""
    count = 1
    for name in comp_names:
        caption += "C"+str(count)+" : "+name+"\n "
        count +=1
    plot.text(0.5, -0.15, caption, horizontalalignment='center', fontsize=12)
    plot.axis('off')
	


def makeMarksGraph(national_data,school_data,boundaries,plot):
    diverging_colors = sns.color_palette("hls", 5)
    plot.title.set_text('Mark Distribution')
    # cutoffs = school_data[1]
    plot.axvspan(boundaries["Maxiumum Mark"],boundaries["A"], alpha=0.5, color=diverging_colors[4],label="A")
    plot.axvspan(boundaries["A"],boundaries["B"], alpha=0.5, color=diverging_colors[3],label="B")
    plot.axvspan(boundaries["B"],boundaries["C"], alpha=0.5, color=diverging_colors[2],label="C")
    plot.axvspan(boundaries["C"],boundaries["D"], alpha=0.5, color=diverging_colors[1],label="D")
    plot.axvspan(boundaries["D"],0, alpha=0.5, color=diverging_colors[0],label="NA")
    


    temp_school = pd.DataFrame(["School"]*len(school_data))
    temp_school["Marks"] = school_data
    temp_national = pd.DataFrame(["National"]*len(national_data))
    temp_national["Marks"] = national_data

    data = pd.concat([temp_school,temp_national])
    data = data.rename(columns = {0:"Institution"})



    # school = sns.kdeplot(school_data,color="k",ax=plot,bw_adjust=.6)
    # national = sns.kdeplot(national_data,color="k",ax=plot, linestyle="--")
    
    test = sns.kdeplot(x=data["Marks"],hue=data["Institution"],common_norm=False,ax=plot,bw_adjust=.8,legend=True)

    handles = plot.legend_.legendHandles
    for h, t in zip(handles, plot.legend_.texts):
        h.set_label(t.get_text())  # assign the legend labels to the handles
    
    sns.rugplot(school_data,color="k",ax=plot)
	

    temp = []
    temp.append(mpatches.Patch(color=diverging_colors[0], label='NA'))
    temp.append(mpatches.Patch(color=diverging_colors[1], label='D'))
    temp.append(mpatches.Patch(color=diverging_colors[2], label='C'))
    temp.append(mpatches.Patch(color=diverging_colors[3], label='B'))
    temp.append(mpatches.Patch(color=diverging_colors[4], label='A'))

    temp.append(handles[0])
    temp.append(handles[1])

    # # # temp.append(Line2D([0], [0], color='b', linestyle="--", label='National'))
    # plot.set

    plot.legend(handles=temp,ncol=2,loc='upper left')
    # plot.legend(ncol=2,loc='upper left')

    plot.get_yaxis().set_visible(False)
    

    plot.set_xlim(0,boundaries["Maxiumum Mark"])



def createOverview(year,level,name):
    filename = " Overview"
    title = name+"\n "
    if level==75:
        filename = "National 5 "+filename
        title += "National 5\n"
    else:
        filename = "Higher "+filename
        title += "Higher\n"
    title += str(year-1)+"-"+str(year)
    
    pdf = PdfPages(filename+".pdf")
    fig, ax =plt.subplots(1,1,figsize=(11.69,8.27))
    makeFrontPage(title,ax)
    pdf.savefig()
    plt.close()


    subjects = data_store.readSchoolSubjects(year,level)
    grade_boundaries = data_store.readGradeBoundaries(level=level,year=year,subjects=subjects,marks=True)

    
    subject_names = subjects["Course Title"]
    subject_codes = subjects["Course"]
    # seperate attainment stats are not available for courses in alternative languages 
    national_attainment = data_store.readSqaAttainment(year,level)

    # though they are for components!
    national_components = data_store.readComponentsSqa(year,level)



    for i in range(len(subject_names)):
        
        subject_name = subject_names[i]
        alt_subject = False
        alt_subject_name = ""
        
        if subject_name in combine_courses["english"].keys():
            print("Found subject in other language")
            print(subject_name)
            alt_subject_name = combine_courses["english"][subject_name]
            print("English equiv: ",alt_subject_name)
            alt_subject = True

            boundaries = grade_boundaries[grade_boundaries["Subject"]==alt_subject_name]
            national_grades = (national_attainment[national_attainment["Course"]==subject_name])
            #COMPONENTS STATS ARE AVAILABLE FROM SQA FOR NOT ENGLISH SUBJECTS 
            national_comp = national_components[national_components["Subject"]==subject_name]
        else:
            boundaries = grade_boundaries[grade_boundaries["Subject"]==subject_name]
            national_grades = (national_attainment[national_attainment["Course"]==subject_name])
            national_comp = national_components[national_components["Subject"]==subject_name]
        
        # print(subject_name)
        # print(boundaries)
        # get the grade boundaries as a dict
        boundaries = boundaries.iloc[0].to_dict()
        # get marks from the data store. Remove_incomplete will remove pupils who have 
        # incomplete evidence, such as those pupils who did an assignment but not the exam, 
        # or pupils who did one paper but not the others
        school_attainment = data_store.readRawMarks(year,level,subject_name,remove_incomplete=True)

        #get the total marks
        school_marks = school_attainment.groupby("SCN")["Mark"].sum().values
        # some subjects have multiple components and each mark
        # for each candidate is listed, remove the duplicate lines
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
        # data_store.readComponentsSqa(year,level)



        national_grades = national_grades.iloc[0].to_dict()
        
        fig, axes =plt.subplots(2,2,figsize=(11.69,8.27))
        # axes[0][1].axis('off')
        national_marks = estimateMarkDistribution(national_grades,boundaries)
        raw_marks = data_store.readTotalMarks(year,level,subject_name,remove_incomplete=True)
        makeMarksGraph(national_marks,raw_marks,boundaries,axes[0][0])
        makeGradesGraph(national_grades,school_grades,boundaries,axes[0][1])
        makeGradeTable(national_grades,school_grades,axes[1][1])

        temp = school_attainment.groupby("Component")["Mark"]
        school_comp = pd.DataFrame({"School Mean":temp.mean(),"School Std":temp.std(),"School Max":temp.max()})
        national_comp = national_comp.dropna(axis=1, how='all')
        
        makeComponentTable(school_comp, national_comp,axes[1][0])


        plt.figtext(0.95, 0.95, subject_name, wrap=True, horizontalalignment='right', fontsize=24)

        # plt.show()
        pdf.savefig()
        plt.close()
    pdf.close()



def specialMaths(year,level,name):
    filename = "Maths Overview"
    title = name+"\n "
    if level==75:
        filename = "National 5 "+filename
        title += "National 5\n"
    else:
        filename = "Higher "+filename
        title += "Higher\n"
    title += str(year-1)+"-"+str(year)
    
    pdf = PdfPages(filename+".pdf")
    fig, ax =plt.subplots(1,1,figsize=(11.69,8.27))
    makeFrontPage(title,ax)
    pdf.savefig()
    plt.close()


    subjects = data_store.readSchoolSubjects(year,level)
    
    only_maths = []
    only_maths.append("Mathematics")
    only_maths.append("Matamataig (Mathematics)")
    only_maths.append("Applications of Mathematics")
    only_maths.append("Applications of Mathematics")
    


    grade_boundaries = data_store.readGradeBoundaries(level=level,year=year,subjects=subjects,marks=True)

    
    subject_names = subjects["Course Title"]
    subject_codes = subjects["Course"]
    # seperate attainment stats are not available for courses in alternative languages 
    national_attainment = data_store.readSqaAttainment(year,level)

    # though they are for components!
    national_components = data_store.readComponentsSqa(year,level)


    first_apps = False
    for i in range(len(subject_names)):
        
        subject_name = subject_names[i]
        
        alt_subject = False
        alt_subject_name = ""

        if not (subject_name in only_maths):
            pass
        else:

            if subject_name in combine_courses["english"].keys():
                print("Found subject in other language")
                print(subject_name)
                alt_subject_name = combine_courses["english"][subject_name]
                print("English equiv: ",alt_subject_name)
                alt_subject = True

                boundaries = grade_boundaries[grade_boundaries["Subject"]==alt_subject_name]
                national_grades = (national_attainment[national_attainment["Course"]==subject_name])
                #COMPONENTS STATS ARE AVAILABLE FROM SQA FOR NOT ENGLISH SUBJECTS 
                national_comp = national_components[national_components["Subject"]==subject_name]
            else:
                boundaries = grade_boundaries[grade_boundaries["Subject"]==subject_name]
                national_grades = (national_attainment[national_attainment["Course"]==subject_name])
                national_comp = national_components[national_components["Subject"]==subject_name]
            
            # get the grade boundaries as a dict
            boundaries = boundaries.iloc[0].to_dict()
            national_grades = national_grades.iloc[0].to_dict()
                    
            if (subject_name== "Applications of Mathematics"):
                for i in range(2):
                    # get marks from the data store. Remove_incomplete will remove pupils who have 
                    # incomplete evidence, such as those pupils who did an assignment but not the exam, 
                    # or pupils who did one paper but not the others
                    school_attainment = data_store.readRawMarks(year,level,subject_name,remove_incomplete=True)
                    print(subject_name)
                    

                    if (i==1):
                        maths = data_store.readRawMarks(year,level,"Mathematics",remove_incomplete=True)["SCN"].unique()
                        gmaths = data_store.readRawMarks(year,level,"Matamataig (Mathematics)",remove_incomplete=True)["SCN"].unique()
                        school_attainment = school_attainment[~school_attainment["SCN"].isin(maths) & ~school_attainment["SCN"].isin(gmaths)]
                        
                    
                    #get the total marks
                    school_marks = school_attainment.groupby("SCN")["Mark"].sum().values
                    # some subjects have multiple components and each mark
                    # for each candidate is listed, remove the duplicate lines
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
                    # data_store.readComponentsSqa(year,level)



                    
                    
                    fig, axes =plt.subplots(2,2,figsize=(11.69,8.27))
                    # axes[0][1].axis('off')
                    national_marks = estimateMarkDistribution(national_grades,boundaries)
                    raw_marks = data_store.readTotalMarks(year,level,subject_name,remove_incomplete=True)
                    makeMarksGraph(national_marks,school_marks,boundaries,axes[0][0])
                    makeGradesGraph(national_grades,school_grades,boundaries,axes[0][1])
                    makeGradeTable(national_grades,school_grades,axes[1][1])

                    temp = school_attainment.groupby("Component")["Mark"]
                    school_comp = pd.DataFrame({"School Mean":temp.mean(),"School Std":temp.std(),"School Max":temp.max()})
                    national_comp = national_comp.dropna(axis=1, how='all')
                    
                    makeComponentTable(school_comp, national_comp,axes[1][0])
                    if (i==1):
                        subject_name = "Apps Maths (excluding pupils sitting Maths or Matamataig)"
                    
                    plt.figtext(0.95, 0.95, subject_name, wrap=True, horizontalalignment='right', fontsize=24)

                    # plt.show()
                    pdf.savefig()
                    plt.close()
            else:
                # get marks from the data store. Remove_incomplete will remove pupils who have 
                    # incomplete evidence, such as those pupils who did an assignment but not the exam, 
                    # or pupils who did one paper but not the others
                    school_attainment = data_store.readRawMarks(year,level,subject_name,remove_incomplete=True)
                    print(subject_name)
                    

                    if (i==1):
                        maths = data_store.readRawMarks(year,level,"Mathematics",remove_incomplete=True)["SCN"].unique()
                        gmaths = data_store.readRawMarks(year,level,"Matamataig (Mathematics)",remove_incomplete=True)["SCN"].unique()
                        school_attainment = school_attainment[~school_attainment["SCN"].isin(maths) & ~school_attainment["SCN"].isin(gmaths)]
                        
                    
                    #get the total marks
                    school_marks = school_attainment.groupby("SCN")["Mark"].sum().values
                    # some subjects have multiple components and each mark
                    # for each candidate is listed, remove the duplicate lines
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
                    # data_store.readComponentsSqa(year,level)



                    
                    
                    fig, axes =plt.subplots(2,2,figsize=(11.69,8.27))
                    # axes[0][1].axis('off')
                    national_marks = estimateMarkDistribution(national_grades,boundaries)
                    raw_marks = data_store.readTotalMarks(year,level,subject_name,remove_incomplete=True)
                    makeMarksGraph(national_marks,school_marks,boundaries,axes[0][0])
                    makeGradesGraph(national_grades,school_grades,boundaries,axes[0][1])
                    makeGradeTable(national_grades,school_grades,axes[1][1])

                    temp = school_attainment.groupby("Component")["Mark"]
                    school_comp = pd.DataFrame({"School Mean":temp.mean(),"School Std":temp.std(),"School Max":temp.max()})
                    national_comp = national_comp.dropna(axis=1, how='all')
                    
                    makeComponentTable(school_comp, national_comp,axes[1][0])
                    if (i==1):
                        subject_name = "Apps Maths (excluding pupils sitting Maths or Matamataig)"
                    
                    plt.figtext(0.95, 0.95, subject_name, wrap=True, horizontalalignment='right', fontsize=24)

                    # plt.show()
                    pdf.savefig()
                    plt.close()
    pdf.close()



test = False
institution = "Portree High School"
year = 2023

if test:
    import cProfile
    prof = cProfile.Profile()
    prof.enable()
    createOverview(year,75,institution)

    prof.disable()
    prof.dump_stats("profile.prof")
    import pstats
    p = pstats.Stats("profile.prof")
    print(p.sort_stats("cumtime").print_stats(10))
else:
    # specialMaths(year,75,institution)
    createOverview(year,75,institution)


createOverview(year,75,institution)
createOverview(year,76,institution)
