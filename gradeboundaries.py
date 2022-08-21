import numpy
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
# matplotlib.style.use('ggplot')
from dataimport import DataStore


def createYearGradeBoundaryPlot(data,subplot,title):
    subplot.set_xlim(0,100)
    subplot.invert_xaxis()
    labels = data.index
    labels = list(labels)
    # labels = ['\n'.join(wrap(l,15)) for l in labels]
    a = data["A"]
    b = data["B"]
    c = data["C"]
    d = data["D"]

    tol = numpy.ones(d.shape)*100
    
    subplot.barh(labels,tol-a,left=a, label="A")
    subplot.barh(labels,a-b,left=b, label="B")
    subplot.barh(labels,b-c,left=c, label="C")
    subplot.barh(labels,c-d,left=d, label="D")

    
    subplot.axvline(x = 70, color = 'black', label = 'Notional A')
    subplot.axvline(x = 60, color = 'dimgrey', label = 'Notional B')
    subplot.axvline(x = 50, color = 'darkgrey', label = 'Notional C')
    subplot.axvline(x = 40, color = 'lightgrey', label = 'Notional D')
    subplot.set_title(title)

    subplot.legend()

def createGradeBoundariesYearLevel(data,year,level,ax):
    #find the school subjects for that year and level
    subjects = data.readSchoolSubjects(year,level)
    #find the grade boundaries for that combination
    grade_bound = data.readGradeBoundaries(year,level,subjects)
    grade_bound.sort_values(by=["A"], inplace=True)
        
    title = str(year)
    if level==75:
        title += " N5 "
    else:
        title += " Higher "
    title += "Grade Boundaries"
    #plot the data
    createYearGradeBoundaryPlot(grade_bound,ax,title)

data_import = DataStore()
year = 2022
pdf = PdfPages(str(year)+" Grade Boundaries.pdf")
fig, ax = plt.subplots(constrained_layout=True,figsize=(11.69,8.27))
createGradeBoundariesYearLevel(data_import,year,75,ax)
pdf.savefig() 
fig, ax = plt.subplots(constrained_layout=True,figsize=(11.69,8.27))
createGradeBoundariesYearLevel(data_import,year,76,ax)
pdf.savefig() 

pdf.close()
