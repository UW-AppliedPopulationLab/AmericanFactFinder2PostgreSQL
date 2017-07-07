#ogr2ogr test
from subprocess import call
import csv
import sys
import os

#   get the config infomation for the database connection
#   it will import a config.py if the file is not made one
#   will need to be made.  see example_config.py for format.

import config # configuration file named config.py see example_config.py for format
host  = config.DataBaseInfo['host']
user = config.DataBaseInfo['user']
db = config.DataBaseInfo['db']
password = config.DataBaseInfo['password']

def ogr2ogr_To_Db(filename):
    db_name = filename.split("/")[-1].split("\\")[1]
    db_name = db_name.split(".")[0] + "_" + filename.split("/")[-1].split("\\")[0]
    db_name = db_name.replace("_with_ann","")
    print db_name

    call(['ogr2ogr','-f',
        'PostgreSQL','PG:host=' + host + ' user=' + user + ' dbname=' + db + ' password='+password+'',
        filename,
        "-nln",
        db_name
        ])

    print db_name + " added to the database"
    
#############################################################
#############################################################

def dbify_loop(dir_name, filenames, count):
    for name in filenames:
        # call function to open csv file and read in rows
        if "metadata" not in name or count == 0:
            ogr2ogr_To_Db(name)
        else:
            continue

    print "Done running ogr_to_db!"
