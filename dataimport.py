import pandas as pd
from datacache import *
import numpy

# utility class that gets the required data from 
# 1. school attainment (sqa coordinator can get this as an excel document)
# 2. SQA grade boundaries 
# 3. SQA national Attainment 
# 4. SQA component summary statistics 

class DataStore:

    def __init__(self):
        self.valid_years = [2018,2019,2022,2023]
        self.valid_levels = [75,76]
        self.valid_grades = ["A","B","C","D"]
        self.results_cache = {}

        results_filename = "Data/SchoolResults/?.xlsx"
        self.results = ResultCache(results_filename)
        boundary_filename = "Data/GradeBoundaries/2017-2023.xlsx"
        self.boundaries = BoundaryCache(boundary_filename)
        sqa_filename = "Data/sqaAttainment/2019-2023.xlsx"  
        self.sqa_attainment = NationalAttainmentCache(sqa_filename)
        comp_filename = "Data/ComponentMarks/2023.xlsx"  
        self.components = ComponentCache(comp_filename)
        
    def checkYears(self,year):
        if not year in self.valid_years:
            raise Exception("year not valid. "+str(self.valid_years)+" only")
    
    def checkLevel(self,level):
        if not level in self.valid_levels:
            raise Exception("level("+str(level)+") not valid. "+str(self.valid_levels)+" only")


    # this works for 2022 but will not work for previous years as the sqa changed 
    # the formatting
    def readComponentsSqa(self,year,level):
        filename = "Data/ComponentMarks/"+str(year)+".xlsx"
        data = self.components.getData(year,level)
        return data
        

    def readSqaAttainment(self,year,level):
        self.checkYears(year)
        self.checkLevel(level)
        data = self.sqa_attainment.getData(year,level)
        return data

    def readSCNtoName(self,year):
        self.checkYears(year)
        data = self.results.getData(year)
        data = data[["SCN","Forename","Surname"]]
        return data
    
    def readMarks(self,year,level,names=False):
        self.checkYears(year)
        self.checkLevel(level)
        
        data = self.results.getData(year)
        if not names:
            data = data.drop(labels=["Forename","Surname"],axis=1)
        data = data[data['Mark']!=999]
        data = data[data["Level"]==level]
        return data

    def readTotalMarks(self,year,level,course,remove_incomplete=True):
        
        data = self.readMarks(year,level)
        data = data[data["Course Title"]==course]
        #need to consider if thie is what i want to do here
        # remove any student with incomplete components
        num_comp = data["Component"].max()

        if(remove_incomplete):
            temp = data.groupby(["SCN"])["SCN"]
            if ((temp.count()!=num_comp).sum()!=0):
                complete = temp.count()==num_comp
                totals = data.groupby("SCN")["Mark"].sum()
                temp = pd.merge(totals, complete, right_index = True,left_index = True)
                temp = temp[temp["SCN"]]
                totals = (temp["Mark"].values.flatten())
                return totals
           
        totals = data.groupby("SCN")["Mark"].sum().values.flatten()
        return totals 

    def readRawMarks(self,year,level,course,remove_incomplete=True):
        data = self.readMarks(year,level)
        data = data[data["Course Title"]==course]
        if(remove_incomplete):
            temp = data.groupby(["SCN"])["SCN"]
            num_comp = data["Component"].max()
            complete = temp.count()==num_comp
            if (complete.sum()-len(complete)!=0):
                print("Raw marks: Removed ",str(len(complete)-complete.sum()), "Incomplete results from ",course)
            complete = pd.DataFrame(complete.values,index= complete.index,columns=["Complete"])

            data = data.merge(complete, left_on='SCN', right_on='SCN')
            data = data[data["Complete"]==True]
            
        return data
    
    #find the subjects that pupils sat in the school in the year provided
    # returns a dict of course codes and Course titles
    def readSchoolSubjects(self,year,level):
        data = self.readMarks(year,level)
        temp = {}
        temp["Course"] = data["Course"].unique()
        temp["Course Title"] = data["Course Title"].unique()
        return temp
  
    
    def readGrandBoundaryFile(self,filename,level):
        data = self.boundaries.getData(level)
        return data

    def readGradeBoundariesAllYears(self,level,subjects=None):
        self.checkLevel(level)

        data = self.boundaries.getData(level)
        
        if subjects != None:
            data = data[data["Subject"].isin(subjects["Course Title"])]
        
        rep_dict = {}
        for year in self.valid_years:
            for grade in self.valid_grades:
                col_name = grade+ " Boundary "+str(year)
                rep_dict[col_name] = grade+" "+str(year)
            rep_dict["Maximum Mark "+str(year)] = "Max "+str(year)
        data.rename(columns= rep_dict,inplace=True) 
        return data

    def readGradeBoundaries(self,year,level=75,subjects=None,marks=False):
        self.checkYears(year)
        self.checkLevel(level)
        
        data = self.boundaries.getData(level)
        if subjects != None:
            data = data[data["Subject"].isin(subjects["Course Title"])]
        cols = []
        rep_dict = {}
        for grade in self.valid_grades:
            col_name = grade +" Boundary " +str(year)
            cols.append(col_name)
            #replace dictionary for col names
            rep_dict[col_name] = grade
        
        rep_dict["Maximum Mark "+str(year)] = "Maxiumum Mark"

        data = data[["Subject","Maximum Mark "+str(year)]+cols]
        if not marks:
            data[cols] = data[cols].div(data["Maximum Mark "+str(year)],axis = 0)
            data[cols] = data[cols]*100
            
        data.index = data["Subject"]
        data.rename(columns= rep_dict,inplace=True) 
        return data