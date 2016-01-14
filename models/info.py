# -*- coding: utf-8 -*-
import json, os
# import sys

# from pprint import pprint

# info is saved in a file looks like
# {
#	"key": "value"
# }

# print 'sys.argv[0] =', sys.argv[0]
 #pathname = os.path.dirname(sys.argv[0])
# print 'path =', pathname
# print 'full path =', os.path.abspath(pathname)
pathname = str(os.path.abspath(os.getcwd()))
# print len(pathname)
# print 'file path = ', os.path.abspath(pathname[:23]+"data.json")
pathname = os.path.abspath(pathname[:23]+"data.json")
with open(pathname) as data_file:
    data = json.load(data_file)
data_file.close()

def get_database_url():
	return data['database_url']

def get_email_mailer():
	return data['email_mailer']

def get_passw_mailer():
	return data['passw_mailer']

def get_database_url2():
	return data['database_url2']

def get_database_psycopg():
	return data['database_psycopg']