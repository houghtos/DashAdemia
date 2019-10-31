#Objects to query list of pubmed article IDs for each author.
#First object 'PM_ID_key' runs custom query as specified from dictionary.
#Second object 'PM_ID_default' runs default query based on authors name.
#NOTE: Default query currently setup to search for authors apart of Memorial Sloan Kettering institution. 

import urllib.request 
import urllib.parse 
import re
import xml.etree.ElementTree as ET 


class PM_ID_key:
    
    def __init__(self, key):
        self.key = key
        self.obj_id_list = obj_id_list = []


    def id_key_generator(self):
     
        #Creates object of a url request with author name and then a new object that reads the first
        #Maximum number of IDs returned is 1,000
        id_list = []
        author_request = urllib.request.urlopen('http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&cmd=search&term={key}&retmax=1000'.format(key=self.key))
        author = author_request.read() 
        root = ET.fromstring(author)
        for author in root.iter('Id'):
            id_list.append(author.text)
        return (id_list)


class PM_ID_default:
    
    def __init__(self, first, last, mid):
        self.first = first.replace(" ","+")
        self.last = last.replace(" ","+")
        self.mid = mid
        self.fi = first[0]


    def id_def_generator1(self):
     
        #Creates object of a url request with author name and then a new object that reads the first
        #Maximum number of IDs returned is 1,000
        id_list = []
        author_request = urllib.request.urlopen('http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&cmd=search&term=(kettering[ad]+AND+{last}+{fi}[au])&retmax=1000'.format(last=self.last,fi=self.fi))
        author = author_request.read() 
        root = ET.fromstring(author)
        for author in root.iter('Id'):
            id_list.append(author.text)
        return (id_list)

    def id_def_generator2(self):
     
        #Creates object of a url request with author name and then a new object that reads the first
        #Maximum number of IDs returned is 1,000
        id_list = []
        author_request = urllib.request.urlopen('http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&cmd=search&term=((kettering[ad]+AND+{last}+{fi}[au])+OR+(kettering[AD]+AND+{last}+{fi}{mid}[au]))&retmax=1000'.format(last=self.last,fi=self.fi,mid=self.mid))
        author = author_request.read() 
        root = ET.fromstring(author)
        for author in root.iter('Id'):
            id_list.append(author.text)
        return (id_list)


