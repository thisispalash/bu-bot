import os, json

''' Constants '''
FILE_EXT = '.json'
ROOT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(ROOT_DIR,'data')

STUD_FILE = os.path.join(DATA_DIR,'students'+FILE_EXT)
SERVER_INFO = os.path.join(DATA_DIR,'server'+FILE_EXT)

''' Exists? '''
if not os.path.isdir(DATA_DIR): 
  os.mkdir(DATA_DIR)
if not os.path.isfile(STUD_FILE):
  with open(STUD_FILE,'w') as f: json.dump({},f)
if not os.path.isfile(SERVER_INFO):
  with open(STUD_FILE,'w') as f: json.dump({},f)