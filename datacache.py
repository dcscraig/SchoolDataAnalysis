import pandas as pd
import numpy

# Data Caches, will returna clean copy of the data requested (if requested before)
# and will read the file required to get the data if not.
class DataCache:
    def __init__(self,data_clean=None,header=0):
        self.data = {}
        self.data_clean = data_clean
        self.header = header

    def __genKey(self,filename,option):
        key = filename
        if(option!=None):
            key= filename+option
        return key


    def add(self,filename,option=None):
        if option!=None:
            temp = pd.read_excel(filename,sheet_name = option,header=self.header)
        else:
            temp = pd.read_excel(filename,header=self.header)
            
        if self.data_clean !=None:
            temp = self.data_clean(temp)
        self.data[self.__genKey(filename,option)] = temp

    def remove(self,filename,option=None):
        del self.data[self.__genKey(filename,option)]

    def contains(self,filename,option=None):
        return self.__genKey(filename,option) in self.data.keys()
    
    def keys(self):
        return self.data.keys()

    def get(self,filename,option=None):
        return self.data[self.__genKey(filename,option)].copy(deep=True)


class ComponentCache:

    def __init__(self,filename,header=1):
        self.filename = filename
        self.cache = DataCache(self.__cleanData,header)
        self.sheet_names = {}
        self.sheet_names[75] = "National_5"
        self.sheet_names[76] = "Higher"
        
    def __cleanData(self,data):
        if("Gaidhlig" in data['Subject'].unique()):
            data['Subject'] = data['Subject'].replace(['Gaidhlig'], 'Gàidhlig')
        return data

    def getData(self,year,level):
        temp = self.filename.replace("?",str(year))
        if not self.cache.contains(temp,self.sheet_names[level]):
            self.cache.add(temp,self.sheet_names[level])
        return self.cache.get(temp,self.sheet_names[level])


class BoundaryCache:

    def __init__(self,filename,header=2):
        self.filename = filename
        self.cache = DataCache(self.__cleanData,header)
        self.sheet_names = {}
        self.sheet_names[75] = "National_5"
        self.sheet_names[76] = "Higher"
        
    def __cleanData(self,data):
        data = data.replace("[z]",numpy.nan)
        return data

    def getData(self,level=None):
        if not self.cache.contains(self.filename,self.sheet_names[level]):
            self.cache.add(self.filename,self.sheet_names[level])
        return self.cache.get(self.filename,self.sheet_names[level])

class ResultCache:

    def __init__(self,filename,header=9):
        self.filename = filename
        self.cache = DataCache(self.__cleanData,header)
        
    def __cleanData(self,data):
        if("Gaidhlig" in data['Course Title'].unique()):
            data['Course Title'] = data['Course Title'].replace(['Gaidhlig'], 'Gàidhlig')
        return data

    def getData(self,year):
        temp = self.filename.replace("?",str(year))
        if not self.cache.contains(temp):
            self.cache.add(temp)
        return self.cache.get(temp)
        
class NationalAttainmentCache:

    def __init__(self,filename,header=2):
        self.filename = filename
        self.cache = DataCache(self.__cleanData,header)
        self.sheet_names = {}
        self.sheet_names[75] = "National_5"
        self.sheet_names[76] = "Higher"
        
        
    def __cleanData(self,data):
        if("Gaidhlig" in data['Subject'].unique()):
            data['Subject'] = data['Subject'].replace(['Gaidhlig'], 'Gàidhlig')
        return data

    def reformat(self,data,year):
        temp = ["Subject","Grade A Count"]
        for i in ["A-B","A-C","A-D"]:
            temp.append("Grades "+i+" Count")
        temp.append("No Award Count")
        temp.append("Entries")
        for i in range(1,len(temp)):
            temp[i] = temp[i]+" "+str(year)
        
        col_dict = {}

        for i in temp:
            if i[0:2]=="No":
                col_dict[i] = "NA"
            elif i[0:2]=="En":
                col_dict[i] = "Total"
            elif i[0:2]=="Su":
                col_dict[i] = "Course"
            else:
                col_dict[i] = (i.split(" ")[1])

        data = data[temp]
        data = data.rename(columns=col_dict)
        data["B"] = data["A-B"] - data["A"]
        data["C"] = data["A-C"] - data["A-B"]
        data["D"] = data["A-D"] - data["A-C"]
        # SQA try to hide the number of no awards
        # but provide all the information required to 
        # calculate it..
        data["NA"] = data["Total"] - data["A-D"]
        return (data)

    def getData(self,year,level=None):
        if not self.cache.contains(self.filename,self.sheet_names[level]):
            self.cache.add(self.filename,self.sheet_names[level])
        data = self.cache.get(self.filename,self.sheet_names[level])
        data = self.reformat(data,year)
        return data
        






if __name__=="__main__":
    level = 75
    filename = "Data/GradeBoundaries/2017-2022.xlsx"
    cache = BoundaryCache(filename)
    data = cache.getData(level)
    print(data)
    
    year = 2022
    filename = "Data/PortreeResults/?.xlsx"

    results = ResultCache(filename)
    data = results.getData(year)
    data = results.getData(year)
    data = results.getData(year)

    filename = "Data/sqaAttainment/2018-2022.xls"  
    national = NationalAttainmentCache(filename)
    data = national.getData(2022,76)
    print (data)

    filename = "Data/ComponentMarks/?.xlsx"
    component = ComponentCache(filename)
    data = component.getData(2022,76)
    print (data)

        


    