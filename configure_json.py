import json
import os, sys

#Function write snew config.json file if it does not exist and prompts user for relevant information.
def writeNewConfig(newpath):
	#Template for json configure file 
	jsonInput = {
	'rds_creds': {
				'server_name': '',
				'user': '',
				'password': '',
				'database_name': ''
				}
			}

	#Prompt user to enter configuration information.
	jsonInput['rds_creds']['server_name'] = input('Enter server name address: ')
	jsonInput['rds_creds']['user'] = input('Enter user name: ')
	jsonInput['rds_creds']['password'] = input('Enter password: ')
	jsonInput['rds_creds']['database_name'] = input('Enter database name: ')

	#Write config file in subdirectory "conf"
	with open(newpath,'w') as f:
		json.dump(jsonInput, f)
	return()

#Uses "Try" to ensure each json data variable exists. 
#If does not, returns false and prompts writeNewConfig function to run. 
def checkConfFormat(filepath):
	with open(filepath,'r') as f:
		json_format = r"{'rds_creds': {'server_name': '', 'user': '', 'password': '', 'database_name': ''}}"
		priorConfig = json.load(f)
		correct_format = True

		try:
			priorConfig['rds_creds']['server_name']
		except:
			print("server_name variable in json does not exist.")
			print("Ensure json conforms to following format:")
			print(json_format,'\n')
			if correct_format:
				correct_format = False

		try:
			priorConfig['rds_creds']['user']
		except:
			print("user variable in json does not exist.")
			print("Ensure json conforms to following format:")
			print(json_format,'\n')
			if correct_format:
				correct_format = False

		try:
			priorConfig['rds_creds']['password']
		except:
			print("password variable in json does not exist.")
			print("Ensure json conforms to following format:")
			print(json_format,'\n')
			if correct_format:
				correct_format = False

		try:
			priorConfig['rds_creds']['database_name']
		except:
			print("database_name variable in json does not exist.")
			print("Ensure json conforms to following format:")
			print(json_format,'\n')
			if correct_format:
				correct_format = False
	#Return true or false based on whether json is properly configured.			
	return(correct_format)


#Loads existing json config file.
#Will prompt user to enter config values which are already empty (blank space)
#User can use prior non-empty values by leaving input blank (e.g. aws configure) 
def editConfig(filepath):
	with open(filepath,'r+') as f:
		priorConfig = json.load(f)
		#Check server name config.
		if priorConfig['rds_creds']['server_name'].strip() == '':
			priorConfig['rds_creds']['server_name'] = input('Enter server name address: ')
		else:
			print("Current server name: " + priorConfig['rds_creds']['server_name'])
			temp_var = input('Enter new server name.  Leave blank to not change: ')
			if temp_var.strip() == '':
				pass
			else:
				priorConfig['rds_creds']['server_name'] = temp_var

		#Check username config.
		if priorConfig['rds_creds']['user'].strip() == '':
			priorConfig['rds_creds']['user'] = input('Enter server name address: ')
		else:
			print("Current server name: " + priorConfig['rds_creds']['user'])
			temp_var = input('Enter new username.  Leave blank to not change: ')
			if temp_var.strip() == '':
				pass
			else:
				priorConfig['rds_creds']['user'] = temp_var

		#Check password config.
		if priorConfig['rds_creds']['password'].strip() == '':
			priorConfig['rds_creds']['password'] = input('Enter server name address: ')
		else:
			print("Current server name: " + priorConfig['rds_creds']['password'])
			temp_var = input('Enter new password.  Leave blank to not change: ')
			if temp_var.strip() == '':
				pass
			else:
				priorConfig['rds_creds']['password'] = temp_var

		#Check database name config.
		if priorConfig['rds_creds']['database_name'].strip() == '':
			priorConfig['rds_creds']['database_name'] = input('Enter server name address: ')
		else:
			print("Current server name: " + priorConfig['rds_creds']['database_name'])
			temp_var = input('Enter new database name.  Leave blank to not change: ')
			if temp_var.strip() == '':
				pass
			else:
				priorConfig['rds_creds']['database_name'] = temp_var
	return()

if __name__ == "__main__":

	#Get path of current python scripts to check if "conf" directory exists yet.
	config_path = os.path.dirname(os.path.realpath(__file__)) + '/conf'

	#If the "conf" directory exists, pass.  Otherwise, create it.
	#Script will halt if unable to create "conf" directory and it does not exist.
	if os.path.exists(config_path):
		pass
	else:
		print("No conf directory found.  Attempting to create.")
		try:
			os.mkdir(config_path)
		except OSError:
			print("Creation of the directory {} failed".format(config_path))
			sys.exit("Halting configuration script due to failure to generate conf directory.")
		else:
			print ("Successfully created the directory {} ".format(config_path))

	#Get directory path of configure file to write or edit
	config_file = config_path + '/config.json'
	
	#If configure file exists, check to ensure it has correct json variables.
	#If it does not contain correct variables, write new configure file.
	#Otherwise, write new configure file.
	if os.path.exists(config_file):
		formatted = checkConfFormat(config_file)
		if formatted:
			editConfig(config_file)
		else:
			writeNewConfig(config_file)
	else:
		writeNewConfig(config_file)
