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



levels = [75,76,77]
output = []


for level in levels:
    subjects = data_store.readSchoolSubjects(2024,level)
    for i in range(len(subjects["Course"])):
        code = subjects["Course"][i]
        code = "C"+code[1:]
        output.append([level,code,subjects["Course Title"][i]])

subjects = pd.DataFrame(output,columns= ["Level","Code","Course Title"])

subjects.to_csv("Output/SchoolSubjects.csv",index=False)

exit()


