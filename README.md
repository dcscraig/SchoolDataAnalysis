# School Data Analysis
Automated individual Scottish school data analysis for SQA results. 

# Requirements

Python3, Pandas, Numpy, Seaborne. Install Anaconda (https://www.anaconda.com/)

# Usage

You will need to add your own school results file from your sqa coordinator. Name it the year you are analysing ie Data/SchoolResults/2022.xlsx .

python Overview.py will produce the overview pdfs of all the N5 subjects and Higher Subjects.

python resulttrends.py will produce the result trends pdfs of all the N5 subjects and Higher Subjects.

# Background

Insight (https://insight-guides.scotxed.net/stepbystep.htm) provides Scottish schools a variety of metrics to judge attainment. The release schedule for Insight is often several months after results day. It would be useful to have an overview of results as soon as they are released and for more in depth analysis of those results to be conducted.

# Requirements

All education establishments that use SQA courses will have a coordinator that can access results for the entire establishment. Most of the analysis included here will need those results in an Excel spreadsheet.

Grade boundaries, Component marks and national attainment is provided by the SQA Statistics and information (https://www.sqa.org.uk/sqa/78673.html). I have included the files that I have used with minor alterations. 

![Image of sqa results](https://github.com/dcscraig/SchoolDataAnalysis/blob/98967ce96621ded16fcef691e2c189f857f7350d/emptyresulta.png)

# Scripts

## Result Trends (resulttrends.py)

Produces mark trends for all subjects in your school over the last few years exluding 2020 and 2021.

![Image of subject trend](https://github.com/dcscraig/SchoolDataAnalysis/blob/main/trends.png)

## Overview (Overview.py)

Provides a page for each subject with an estimated mark distribution, grade percentage comparison with national and component mark comparisons. The estimated mark distribution is experimental and should be treated with caution. I would recommend comparing the overall shape of the school mark and national distributions , ie is the peak shifted to the right (better average performance) or to the left (worse average performance). TODO more description.

![Image of subject overview](https://github.com/dcscraig/SchoolDataAnalysis/blob/main/subject_overview.png)


## Find Near Miss (findNearMiss.py)

This script will produce a list of students and their courses for which they missed out in getting the next grade by 1 or 2 marks. 

I have not included an example for obvious data protection issues.

## Grade Boundaries (gradeboundaries.py)

Produces comparison graphs of the grade boundaries for all sqa subjects in your school.

![Image of grade boundaries](https://github.com/dcscraig/SchoolDataAnalysis/blob/main/gradeboundaries.png)

## Grade Boundary vs Attainment (nationalBoundaryAttainment.py)

Looks at the relationship between a subject's A grade boundary and the % of pupils attaining an A. Some interesting grade boundary decisions...

![Image of grade boundaries](https://github.com/dcscraig/SchoolDataAnalysis/blob/main/boundvsattain.png)



# Technical

I have tried to comment the code to help understanding but the current documentation level leaves a lot to be desired. Data access is handled through DataStore and makes use of a DataCache to reduce repeated file access. Not entirely convinced that this approach is conceptually that great but it works.

## Incomplete data

Any student who does not have a complete record, say they did not have a mark for a component of their assessment, has been removed from the data.
This includes students who still passed! All access to the data is through a DataStore class. There are options to remove said students for the following functions (readTotalMarks and readRawMarks [remove_incomplete=True])



## Gaelic Medium Subjects

There are a variety of courses that are offered in Gaelic. They are treated as one subject by the SQA in the reporting of attainment statistics but seperately in component analysis. The overview script treats them as individual subjects while the trend script combines them. This feature is likely to be buggy. I would recommend cross validating.     



## Authors

* **Craig Stewart** - *Initial work* - (https://github.com/dcscraig)

## License

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons Licence" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">GoggleClips</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="https://github.com/dcscraig/GoggleClips" property="cc:attributionName" rel="cc:attributionURL">Craig Stewart</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.<br />Based on a work at <a xmlns:dct="http://purl.org/dc/terms/" href="https://github.com/dcscraig/SchoolDataAnalysis" rel="dct:source">https://github.com/dcscraig/SchoolDataAnalysis</a>.
