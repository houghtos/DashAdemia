## Generates structured pubmed data.

#Import modules to generate pubmed IDs for author and structure data
from PM_Scraper import PM_Scraper
from PM_ID_gen import PM_ID_key, PM_ID_default

#Import author information, aliases, and custom querys
from aut_info import aut_info
from aut_aliases import aut_aliases
from PM_Keys import python_keys

import pymysql
import time

# Function to perform default query using author name. 
def defaultQuery(aut):
	last = aut[0]
	first = aut[1]
	middle = aut[2]
	if middle == '':
		print("No middle")
		id_gen = PM_ID_default(first, last, middle)
		id_list = id_gen.id_def_generator1()
	else:
		print("Yes middle")
		id_gen = PM_ID_default(first, last, middle)
		id_list = id_gen.id_def_generator2()
	return(id_list)

# Custom pubmed query.
def customQuery(aut):
	aut_id = aut[3]
	try:
		query_string = python_keys[aut_id]
		id_gen = PM_ID_key(query_string)
		id_list = id_gen.id_key_generator()
	except KeyError:
		print("KEY ERROR FOR CUSTOM PM SEARCH FOR ", aut_id)
		id_list = []
	return(id_list)


def PM_Scrape_Default(first,mid,last,pm_id):
	scrape_init = PM_Scraper(first,mid,last,pm_id)
	art_date = scrape_init.pms_date()
	art_e_date = scrape_init.pms_edate()	
	ISSN = scrape_init.pms_ISSN()
	pubtype = scrape_init.pms_pubtype()
	source = scrape_init.pms_source()
	jname = scrape_init.pms_jname()
	title = scrape_init.pms_title()
	pmf = scrape_init.pms_pmf()
	autp = scrape_init.pms_autp()
	return(art_date, art_e_date, ISSN, pubtype, source, jname, title, pmf, autp)

def PM_Scrape_Alias(first,mid,last,pm_id, alias):
	scrape_init = PM_Scraper(first,mid,last,pm_id, alias)
	art_date = scrape_init.pms_date()
	art_e_date = scrape_init.pms_edate()
	ISSN = scrape_init.pms_ISSN()
	pubtype = scrape_init.pms_pubtype()
	source= scrape_init.pms_source()
	jname = scrape_init.pms_jname()
	title = scrape_init.pms_title()
	pmf = scrape_init.pms_pmf()
	autp = scrape_init.pms_aliases()
	return(art_date, art_e_date, ISSN, pubtype, source, jname, title, pmf, autp)


def uploadFunction(pm_id, art_id, date, edate, issn, ptype, source, journ, title, ap):
	cursorObject.execute("""INSERT INTO SH_PUBMED (`PM_ID`, `PM_ART_ID`, `PM_DATE`, `PM_EDATE`, `PM_ISSN`, `PM_TYPE`, `PM_SOURCE`, `PM_JOURN`, `PM_TITLE`, `PM_AP_CD`) VALUES (\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")""" % (pm_id, art_id, date, edate, issn, ptype, source, journ, title, ap))
	connectionObject.commit()
	return(print("Upload function complete"))

if __name__ == "__main__":
	# Iterate over author list and parse list elements into individual variable.

	dbServerName = "database.server.address"
	dbUser = "username"
	dbPassword = "password"
	dbName = "databaseName"
	charSet = "utf8mb4"
	cusrorType = pymysql.cursors.DictCursor
	connectionObject = pymysql.connect(host= dbServerName, user= dbUser, password= dbPassword, db= dbName, charset=charSet,cursorclass=cusrorType)
	cursorObject = connectionObject.cursor()


	for aut in aut_info:
		print(aut)
		last = aut[0]
		first = aut[1]
		middle = aut[2]
		aut_id = aut[3]
		department = aut[4]
		service = aut[5]
		alias = aut[6]
		custom_query = aut[7]
		title = aut[8]
		dep = aut[9]

		#Generate Pubmed IDs
		if custom_query == 0:
			pm_ids = defaultQuery(aut)
		else:
			pm_ids = customQuery(aut)
			

		for j in pm_ids:
			print(j)
			if alias == 0:
				try:
					scrape_return = PM_Scrape_Default(first, middle, last, j)
					uploadFunction(aut_id, j, scrape_return[0], scrape_return[1], scrape_return[2], scrape_return[3], scrape_return[4], scrape_return[5], scrape_return[6].replace('"',"'"), scrape_return[-1])
				except:
					print("Call failed... trying again.")
					scrape_return = PM_Scrape_Default(first, middle, last, j)
					uploadFunction(aut_id, j, scrape_return[0], scrape_return[1], scrape_return[2], scrape_return[3], scrape_return[4], scrape_return[5], scrape_return[6].replace('"',"'"), scrape_return[-1])
			else:
				try:
					author_alias = python_keys[aut_id]
					scrape_return = PM_Scrape_Alias(first, middle, last, j, author_alias)
					uploadFunction(aut_id, j, scrape_return[0], scrape_return[1], scrape_return[2], scrape_return[3], scrape_return[4], scrape_return[5], scrape_return[6].replace('"',"'"), scrape_return[-1])
				except:
					print("Call failed... trying again.")
					author_alias = python_keys[aut_id]
					scrape_return = PM_Scrape_Alias(first, middle, last, j, author_alias)
					uploadFunction(aut_id, j, scrape_return[0], scrape_return[1], scrape_return[2], scrape_return[3], scrape_return[4], scrape_return[5], scrape_return[6].replace('"',"'"), scrape_return[-1])
	connectionObject.close()
