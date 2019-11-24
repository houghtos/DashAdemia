# Uses pymsql library to create or drop MySQL Author and Pubmed data tables.
# Requires prior setup of MySQL database.

import pymysql

class manageDB:

  #Configure MySQL database connection 
	def __init__(self):
		self.dbServerName = "database.server.address"
		self.dbUser = "USERNAME"
		self.dbPassword = "PASSWORD"
		self.dbName = "DATABASE_NAME"
		self.charSet = "utf8mb4"
		self.cusrorType = pymysql.cursors.DictCursor
		self.connectionObject = pymysql.connect(host= self.dbServerName, user= self.dbUser, password= self.dbPassword, db= self.dbName, charset=self.charSet,cursorclass=self.cusrorType)

  #Create author table
	def createAUtable(self):
		cursorObject = self.connectionObject.cursor()
		sqlQuery = "CREATE TABLE SH_AUTHOR(AU_ID varchar(12), AU_LAST varchar(40), AU_FIRST varchar(32), AU_MID varchar(4), AU_DEPT varchar(20), AU_SERV varchar(20), AU_ALIAS int (1), AU_QUERY int (1), AU_TITLE varchar(20), AU_SRC varchar(10))"
		cursorObject.execute(sqlQuery)
		self.connectionObject.close()
		return(print("SH_AUTHOR TABLE HAS BEEN CREATED"))
  
  #Drop author table
	def dropAUtable(self):
		cursorObject = self.connectionObject.cursor()
		sqlQuery = "DROP TABLE SH_AUTHOR"
		cursorObject.execute(sqlQuery)
		self.connectionObject.close()
		return(print("SH_AUTHOR TABLE HAS BEEN DROPPED (DELETED)"))
  
  #Create pubmed/publication table
	def createPMtable(self):
		cursorObject = self.connectionObject.cursor()
		sqlQuery = "CREATE TABLE SH_PUBMED(PM_ID varchar(12), PM_ART_ID varchar(20), PM_DATE date, PM_EDATE date, PM_ISSN varchar(20), PM_TYPE varchar(100), PM_SOURCE varchar(100), PM_JOURN varchar(150), PM_TITLE varchar(300), PM_AP_CD int(4), PM_AP_DESC varchar(10))"
		cursorObject.execute(sqlQuery)
		self.connectionObject.close()
		return(print("SH_PUBMED TABLE HAS BEEN CREATED"))
  
  #Drop pubmed/publication table
	def dropPMtable(self):
		cursorObject = self.connectionObject.cursor()
		sqlQuery = "DROP TABLE SH_PUBMED"
		cursorObject.execute(sqlQuery)
		self.connectionObject.close()
		return(print("SH_PUBMED TABLE HAS BEEN DROPPED (DELETED)"))

if __name__ == "__main__":

	# Currently set switch manually before running here!!
  # switch = 0 CREATES author and pubmed table.
  # switch = 1 DROPS author and pubmed table.
	switch = 1


	if switch == 0:
		for i in range(0,2):
			if i == 0:
				init = manageDB()
				init.createAUtable()
			elif i == 1:
				init = manageDB()
				init.createPMtable()
			else:
				break

	elif switch == 1:
		for i in range(0,2):
			if i == 0:
				init = manageDB()
				init.dropAUtable()
			elif i == 1:
				init = manageDB()
				init.dropPMtable()
			else:
				break
	else:
		print("Switch variable can only be equal to integers 1 or 0")
		print("Current switch variable is equal to: " + str(switch))
