# This module reads author information data uploads it to the authr MySQL database table.
# The data table is named "SH_AUTHOR" and contains attributes for:
#   Author ID (this is primary key that links author with publications)
#   Last name, first name, middle initial, department author belongs to, service author belongs to,
#   Binary indicatory (0 or 1) whether to look for aliases for the author
#   Binary indicatory whether to use custom pubmed query for author
#   Author title (e.g. Assistant Professor)
#   A second optional department code.
##############

# Import author data 
from aut_info import aut_info
from aut_aliases import aut_aliases
from PM_Keys import python_keys

#Set Database connection to existing database.
import pymysql

dbServerName = "database.server.name"
dbUser = "userName"
dbPassword = "password"
dbName = "databaseName"
charSet = "utf8mb4"
cusrorType = pymysql.cursors.DictCursor
connectionObject = pymysql.connect(host= dbServerName, user= dbUser, password= dbPassword, db= dbName, charset=charSet,cursorclass=cusrorType)
cursorObject = connectionObject.cursor()

#Loop through author data source and upload to data table.
for aut in aut_info:
	last = aut[0]
	first = aut[1]
	middle = aut[2]
	author_id = aut[3]
	department = aut[4]
	service = aut[5]
	service = service.replace(" ", "-")
	alias = aut[6]
	custom_query = aut[7]
	title = aut[8] 
	dep = aut[9]
	cursorObject.execute("""INSERT INTO SH_AUTHOR (`AU_ID`, `AU_LAST`, `AU_FIRST`, `AU_MID`, `AU_DEPT`, `AU_SERV`, `AU_ALIAS`, `AU_QUERY`, `AU_TITLE`, `AU_SRC`) VALUES (\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")""" % (author_id,last,first,middle,department,service,alias,custom_query,title,dep))
	connectionObject.commit()

connectionObject.close()

