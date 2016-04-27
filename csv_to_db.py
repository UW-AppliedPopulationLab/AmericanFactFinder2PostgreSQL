#ogr2ogr test
from osgeo import ogr
from subprocess import call
import csv
import os
from os import path
from os import listdir
import fileinput
import string
#   get the config infomation for the database connection
#   it will import a config.py if the file is not made one
#   will need to be made.  see example_config.py for format.

import sys
import getopt

dir_path = os.path.dirname(os.path.realpath(__file__))

geog = None
dir_name = None

options, remainder = getopt.getopt(sys.argv[1:], 'g:v', ['geog='])

for opt, arg in options:
    if opt in ('-geog'):
        geog = arg
        print geog

if geog:
    print 'Geog   :', geog

if geog == 's':
    dir_name =  dir_path + "/src/state"
elif geog == 'c':
    dir_name =  dir_path + "/src/county"
elif geog == 'cs':
    dir_name =  dir_path + "/src/county_subdivision"
elif geog == 'ct':
    dir_name =  dir_path + "/src/census_tract"
elif geog == 'bg':
    dir_name =  dir_path + "/src/block_group"
elif geog == 'p':
    dir_name =  dir_path + "/src/places"
else:
    print "please specify which type of geography you would like to run \n" \
    "Use -g then the geogtype as an option \n\n" \
    "s  : runs state\n" \
    "c  : runs county\n"\
    "cs  : runs county subdivison\n"\
    "ct  : runs census tract\n"\
    "bg  : runs census block group\n\n"\
    "p  : runs places\n\n"\
    "EXAMPLE:\n"\
    "python make_meta_lookup.py -g s\n"
    sys.exit(0)

print dir_name
#CHANGE THESE AS NEEDED
#path to the folder
#dir_path = os.path.dirname(os.path.realpath(__file__))
#dir_name =  dir_path + "/src/state"
#dir_name =  dir_path + "/src/county"
#dir_name =  dir_path + "/src/county_subdivision"
#dir_name =  dir_path + "/src/census_tract"



import config # configuration file named config.py see example_config.py for format
host  = config.DataBaseInfo['host']
user = config.DataBaseInfo['user']
db = config.DataBaseInfo['db']
password = config.DataBaseInfo['password']



#function that finds all csv files in the given filename and  returns it
def find_csv_filenames( path_to_dir, suffix=".csv" ):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]


filenames = find_csv_filenames(dir_name)


def ogr2ogr_to_Db(filename):

    db_name = filename.split("/")[-1]
    db_name = db_name.split(".")[0] + "_" + filename.split("/")[-2]
    db_name = db_name.replace("_with_ann","")
    print db_name

    call(['ogr2ogr','-f',
        'PostgreSQL','PG:host=' + host + ' user=' + user + ' dbname=' + db + ' password='+password+'',
        filename,
        "-nln",
        db_name
        ])

    print db_name + " added to the database"

    #print filename.split("/")[-1] + " Done"


for name in filenames:
    # call function to open csv file and read in rows
    full_path_csv = dir_name +"/"+ name
    ogr2ogr_to_Db(full_path_csv)


##replace original file with temp file

#filename = 'test/census_county_test/ACS_14_5YR_S1601_metadata.csv'

#shutil.move(tempfile.name, filename)
print "Done running ogr_to_db!"
