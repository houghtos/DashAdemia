#Generates publication information in relation to author as author.
#Takes as argument author's first name, middle initial, last name, article pubmed ID and (optionally) other aliases.
#Aliases are taken from the author alias dictionary in seperate file. Author must have alias column set to "1" to use aliases.
#Returns structured data from the publication as well as the author's priority (E.g. first author, last author, etc.)


import urllib.request 
import urllib.parse 
import re 
import xml.etree.ElementTree as ET 
from urllib import request
import itertools
from collections import Counter
import datetime

class PM_Scraper:

	#Initialize variables for object
    def __init__(self,first,mid,last,pm_id, aliases = None):
        self.first = first
        self.mid = mid
        self.last =last
        self.pm_id = pm_id
        self.aliases = aliases
        self.id_request = urllib.request.urlopen('http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={pm_id}'.format(pm_id=self.pm_id))
        self.id_pubmed = self.id_request.read()
        self.root = ET.fromstring(self.id_pubmed)


    #Scrape publication date
    def pms_date(self):
        for author in self.root.iter('Item'):
            if author.attrib['Name'] == 'PubDate': 
                date = author.text

        try:
            tokens = date.split(' ')
            if len(tokens) == 1 and date != "None":
                dt_return = datetime.datetime.strptime(date, '%Y')
                dt_return = dt_return.date().isoformat()
            elif len(tokens) == 2 and '-' in tokens[1]:
                date = date.split('-')[0]
                dt_return = datetime.datetime.strptime(date, '%Y %b')
                dt_return = dt_return.date().isoformat()
            elif len(tokens) == 3:
                dt_return = datetime.datetime.strptime(date, '%Y %b %d')
                dt_return = dt_return.date().isoformat()
            elif date == "None":
                dt_return = None
            else:
                seasons = {
                    'spring':'Apr',
                    'winter':'Jan',
                    'summer':'Jul',
                    'fall':'Oct'
                }
                if tokens[1].lower() in seasons.keys():
                    date = '{} {}'.format(tokens[0], seasons[tokens[1].lower()])
                dt_return = datetime.datetime.strptime(date, '%Y %b')
                dt_return = dt_return.date().isoformat()
        except ValueError:
            date_year = date[0:4]
            dt_return = datetime.datetime.strptime(date_year, '%Y')
            dt_return = dt_return.date().isoformat()
        #except UnboundLocalError:
        return(dt_return)

    #Scrape ePub date if applicable
    def pms_edate(self):
        for author in self.root.iter('Item'): 
            if author.attrib['Name'] == 'EPubDate': 
                date = author.text
        if date is not None:
            tokens = date.split(' ')
            if len(tokens) == 1 and date != "None":
                dt_return = datetime.datetime.strptime(date, '%Y')
                dt_return = dt_return.date().isoformat()
            elif len(tokens) == 2 and '-' in tokens[1]:
                date = date.split('-')[0]
                dt_return = datetime.datetime.strptime(date, '%Y %b')
                dt_return = dt_return.date().isoformat()
            elif len(tokens) == 3:
                dt_return = datetime.datetime.strptime(date, '%Y %b %d')
                dt_return = dt_return.date().isoformat()
            else:
                seasons = {
                    'spring':'Apr',
                    'winter':'Jan',
                    'summer':'Jul',
                    'fall':'Oct'
                }
                if tokens[1].lower() in seasons.keys():
                    date = '{} {}'.format(tokens[0], seasons[tokens[1].lower()])
                dt_return = datetime.datetime.strptime(date, '%Y %b')
                dt_return = dt_return.date().isoformat()
        else:
            dt_return = None
        return(dt_return)


    #Scrape publication ISSN number
    def pms_ISSN(self):
        for author in self.root.iter('Item'): 
            if author.attrib['Name'] == 'ISSN': 
                issn_return = author.text                
        return(issn_return)

    #Scrape publication type
    def pms_pubtype(self):
        for author in self.root.iter('Item'): 
            if author.attrib['Name'] == 'PubType': 
                pubtype_return = author.text
        try:
            pubtype_return
        except NameError:
            pubtype_return = None
        return(pubtype_return)

    #Scrape publication source
    def pms_source(self):
        for author in self.root.iter('Item'): 
            if author.attrib['Name'] == 'Source': 
                source_return = author.text                
        return(source_return)

    #Scrape journal publication is from
    def pms_jname(self):
        for author in self.root.iter('Item'): 
            if author.attrib['Name'] == 'FullJournalName': 
                jname_return = author.text                
        return(jname_return)
    
    #Scrape publication title
    def pms_title(self):
        for author in self.root.iter('Item'): 
            if author.attrib['Name'] == 'Title': 
                title_return = author.text                
        return(title_return)

    #Scrape PM Ref Count
    def pms_pmf(self):
        for author in self.root.iter('Item'): 
            if author.attrib['Name'] == 'PmcRefCount': 
                pmf_return = author.text                
        return(pmf_return)

    #Process author priority based on author name inputs
    def pms_autp(self):
        author_list = []
        name = self.last.lower() +" "+self.first[0].lower()
        for author in self.root.iter('Item'): 
            if author.attrib['Name'] == 'Author': 
                author_list.append(author.text)

        author_list = [x.lower() for x in author_list]
        try:
            if len(author_list) == 1:
                ap_final = 1
            elif name in author_list[0]:
                ap_final = 1
            elif len(author_list)>2 and (name in author_list[1]):
                ap_final = 2
            elif len(author_list)>3 and (name in author_list[2]):
                ap_final = 3
            elif name in author_list[-1]:
                ap_final = 0
            else:
                ap_final = 4
        except IndexError:
            ap_final = -1
        return(ap_final) 

    #Process author priority based on aliases.
    def pms_aliases(self):
        author_list = []
        for author in self.root.iter('Item'): 
            if author.attrib['Name'] == 'Author': 
                author_list.append(author.text)
        try:
            if len(author_list) == 1:
                ap_final = 1
            elif author_list[0] in self.aliases:
                ap_final = 1
            elif len(author_list)>2 and (author_list[1] in self.aliases):
                ap_final = 2
            elif len(author_list)>3 and (author_list[2] in self.aliases):
                ap_final = 3
            elif author_list[-1] in self.aliases:
                ap_final = 0
            else:
                ap_final = 4  
        except IndexError:
            ap_final = -1
        return(ap_final)    
