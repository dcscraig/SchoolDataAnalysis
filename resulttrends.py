import numpy
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
# matplotlib.style.use('ggplot')

def getMarks(level,subject,data,years,combine=True):
    
    marks = {}
    for year in years:
        temp = data.readTotalMarks(year,level,subject,remove_incomplete=True) 

#       data for courses available in different languages are assigned the same grade boundaries and are grouped as a single course for reporting purposes.
#       These courses are as follows:
#       
#       Mandarin (Traditional), Mandarin (Simplified) and Cantonese are reported as Chinese Languages for each level.
#       Mathematics and Matamataig are reported as Mathematics for each level.
#       Applications of Mathematics and Gniomhachas Matamataigs are reported as Applications of Mathematics.
#       Geography and Cruinn-eolas are reported as Geography for each level.
#       History and Eachdraidh are reported as History for each level.
#       Modern Studies and Nuadh-Eolas are reported as Modern Studies for each level.

#       !!!!!!! the sqa are not consistent with the use of gaelic spelling and this may not work! modern studies is known work
#       I have no data to check the chinese languages 
        if combine:
            if subject in ["Modern Studies","History", "Geography","Applications of Mathematics","Mathematics", "Mandarin (Traditional)", "Mandarin (Simplified)","Cantonese"]:
                if subject =="Modern Studies":
                    other_lang = data.readTotalMarks(year,level,"Nuadh-Eolas (Modern Studies)",remove_incomplete=True)
                    if(len(other_lang)!=0):
                        temp = numpy.concatenate((temp,other_lang))
                elif subject =="Mathematics":
                    other_lang = data.readTotalMarks(year,level,"Matamataig",remove_incomplete=True)
                    if(len(other_lang)!=0):
                        temp = numpy.concatenate((temp,other_lang))
                elif subject =="Applications of Mathematics":
                    other_lang = data.readTotalMarks(year,level,"Gniomhachas Matamataigs",remove_incomplete=True)
                    if(len(other_lang)!=0):
                        temp = numpy.concatenate((temp,other_lang))
                elif subject =="Geography":
                    other_lang = data.readTotalMarks(year,level,"Cruinn-eolas",remove_incomplete=True)
                    if(len(other_lang)!=0):
                        temp = numpy.concatenate((temp,other_lang))
                elif subject =="History":
                    other_lang = data.readTotalMarks(year,level,"Eachdraidh",remove_incomplete=True)
                    if(len(other_lang)!=0):
                        temp = numpy.concatenate((temp,other_lang))
        marks[year] = temp
    return marks

def createSubjectMarkTrends(years,data,level,data_store,title):
    pdf = PdfPages(title)
    cols = []
    for grade in ["Max","A","B","C","D"]:
        for year in years:
            cols.append(grade+" "+str(year))
    ind = data["Subject"]
    data = data[cols]
    data.index = ind

    for index, row in data.iterrows():
        print(index)
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
        # get the marks for the level, subject and years 
        # combine will cobine english medium and non-english medium subjects 
        # likely to be buggy but know to know for modern studies
        marks = getMarks(level,index,data_store,years,combine=True)
        count = 0
        for year in years:
            if (len(marks[year])!=0):
                percentages =100*(marks[year]/max_val[count]) 
                ax.boxplot(percentages, positions= [count]) 
                ax.text(count+0.1, numpy.median(percentages), len(percentages),style='normal', size= 12)       
            count +=1
        ax.set_xticks([0,1,2,3])
        ax.set_xticklabels(years)
        plt.legend()
        pdf.savefig()
        plt.close()
    pdf.close()

from dataimport import DataStore
data_store = DataStore()

# will need a results file for each of the years in the array 
# contact your sqa coordinator
# deliberately ignored 2020 and 2021!!
# may have an issue with grade boundaries for 2017 if not using 
# my edited sqa spreadsheets
# 
years = [2017,2018,2019,2022]
for level in [75,76]:
    subjects = data_store.readSchoolSubjects(2022,level)
    grade_boundaries = data_store.readGradeBoundariesAllYears(level=level,subjects=subjects)
    title = " Marks Trend.pdf"
    if level==75:
        title = "N5"+title
    else:
        title = "Higher"+title
    createSubjectMarkTrends(years,grade_boundaries,level,data_store,title)
        



# some quick and dirty profiling
# import cProfile
# prof = cProfile.Profile()

# prof.enable()
# test()
# prof.disable()

# prof.dump_stats("profile.prof")


# import pstats
# p = pstats.Stats("profile.prof")

# print(p.sort_stats("cumtime").print_stats(10))





# # for year in years:
# #     data_import.readGradeBoundaries(year,level=75,subjects=subjects)


# # print(subjects)

