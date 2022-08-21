# School Data Analysis
Individual Scottish school data analysis for SQA results. 

# Background

Insight (https://insight-guides.scotxed.net/stepbystep.htm) provides Scottish schools a variety of metrics to judge attainment. The release schedule for Insight is often several months after results day. It would be useful to have an overview of results as soon as they are released and for more in depth anaylsis of those results to be conducted.

# Requirements

All education establishments that use SQA courses will have a coordinator that can access results for the entire establishment. Most of the analysis included here will need those results in an Excel spreadsheet.

Grade boundaries, Component marks and national attainment is provided by the SQA Statistics and information (https://www.sqa.org.uk/sqa/78673.html). I have included the files that I have used with minor alterations. 

![Image of sqa results](https://github.com/dcscraig/SchoolDataAnalysis/blob/98967ce96621ded16fcef691e2c189f857f7350d/emptyresulta.png)

# Description

These are a group of scripts that provides result analysis. 

## Result Trends

Produces mark trends for all subjects in your school over the last few years exluding 2020 and 2021.

![Image of subject trend](https://github.com/dcscraig/SchoolDataAnalysis/blob/main/trends.png)

## Gradeboundaries

Produces comparison graphs of the grade boundaries for all sqa subjects in your school.

![Image of grade boundaries](https://github.com/dcscraig/SchoolDataAnalysis/blob/main/gradeboundaries.png)

## Overview

Provides a page for each subject with an estimated mark distribution, grade percentage comparison with national and component mark comparisons. The estimated mark distribution is experimental and should be treated with caution. I would recommend comparing the overall shape of the school mark and national distributions , ie is the peak shifted to the right (better average performance) or to the right (worse average performance). TODO more description.

![Image of subject overview](https://github.com/dcscraig/SchoolDataAnalysis/blob/main/subject_overview.png)


## Find Near Miss

This script will produce a list of students and their courses for which they missed out in getting the next grade by 1 or 2 marks. 

I haven included an exmple of obvious data protection issues.

# Technical

I have tried to comment the code to help understanding but the current documentation level leaves a lot to be desired. Data access is handled through DataStore and makes use of a DataCache to reduce repeated file access. Not entirely convinced that this approach is conceptually that great but it works.

## Incomplete data

Any student who does not have a complete record, say they did not have a mark for a component of their assessment, has been removed from the data.
This includes students who still passed! All access to the data is through a DataStore class. There are options to remove said students for the following functions (readTotalMarks and readRawMarks [remove_incomplete=True])



## Gaelic Medium Subjects

There are a variety of courses that are offered in Gaelic. 



## Authors

* **Craig Stewart** - *Initial work* - (https://github.com/dcscraig)

## License

<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons Licence" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">GoggleClips</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="https://github.com/dcscraig/GoggleClips" property="cc:attributionName" rel="cc:attributionURL">Craig Stewart</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.<br />Based on a work at <a xmlns:dct="http://purl.org/dc/terms/" href="https://github.com/dcscraig/SchoolDataAnalysis" rel="dct:source">https://github.com/dcscraig/SchoolDataAnalysis</a>.
