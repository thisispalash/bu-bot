import os, json

''' Constants '''
FILE_EXT = '.json'
ROOT_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(ROOT_DIR,'data')

STUD_FILE = os.path.join(DATA_DIR,'students'+FILE_EXT)
CONFIG_FILE = os.path.join(DATA_DIR,'config'+FILE_EXT)
LOG_FILE = os.path.join(DATA_DIR,'event.log')

''' Exists? '''
if not os.path.isdir(DATA_DIR): 
  os.mkdir(DATA_DIR)
if not os.path.isfile(STUD_FILE):
  with open(STUD_FILE,'w') as f: json.dump([],f)
if not os.path.isfile(CONFIG_FILE):
  with open(CONFIG_FILE,'w') as f: json.dump({},f)
if not os.path.isfile(LOG_FILE):
  with open(LOG_FILE,'w') as f: f.write('')