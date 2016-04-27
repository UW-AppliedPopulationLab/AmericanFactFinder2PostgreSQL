import csv
import os
from os import path
from os import listdir
import fileinput
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
    "EXAMPLE:\n"\
    "python make_meta_lookup.py -g s\n"
    sys.exit(0)

print dir_name


#CHANGE THESE

#path to the folder
#dir_name =  dir_path + "/src/state"
#dir_name =  dir_path + "/src/county"
#dir_name =  dir_path + "/src/county_subdivision"
#dir_name =  dir_path + "/src/census_tract"



#function that finds all csv files in the given filename and  returns it
def find_csv_filenames( path_to_dir, suffix=".csv" ):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]


#Make an Array of all the file names
filenames = find_csv_filenames(dir_name)

def getSource(path_to_file):
    with open(path_to_file, 'rU') as f:
        read_data = f.read()
        source = str(read_data)
        source = source.split("Source: ")[-1]
        source = source.split('\n')[0]
        return source.strip()
    f.closed

#find unit
def unitType(prop):
    if "%" in prop:
        return "percent"
    elif "Percent" in prop:
        return "percent"
    elif "population" in prop:
        return "people"
    elif "Total" in prop:
        return "total"
    elif "age" in prop:
        return "years old"
    elif "housing units" in prop:
        return "housing units"
    else:
        return ""

#get table name
def getTable(filename):
    array = filename.split("/")
    file = array[len(array) -1]
    file_basename = file.split("_meta")[0]
    return file_basename

#Opens the csv and reads the rows out
def readRows(csv_file_name, source_info):
    with open(csv_file_name, 'rU') as csvfile:
        reader = csv.DictReader(csvfile)
        # add table name to append to code
        tablename_col = csv_file_name.split("_meta")[0]
        tablename_col = tablename_col.split("_")[-1]
        for row in reader:
            newDict = {};

            #print row
            key = row['key']
            prop = row['prop']
            if "GEO" not in key:
                #set variables for json object
                code = key
                description = str(prop)
                unit = unitType(prop)
                shortDescription = prop
                table = getTable(csv_file_name)
                # source_info = dir_name +"/"+table+".txt"
                # source_info =  getSource(source_info)

                f = open("build/meta_lookup.js","a+")
                #create the json object string
                string = '{  \n \t code: "'  + str(code)  + '", \n ' \
                        '\t description: "'  + str(description) + '", \n ' \
                        '\t unit: "'  + unit + '", \n ' \
                        '\t data:"'  + source_info + '", \n ' \
                        '\t table: "'  + table + '", \n ' \
                        '\t shortDescription: "'  + description + '" \n }, \n '
                #write it and close
                f.write(string)
                f.close();


#for all th files
for name in filenames:
    if "metadata" in name:
        # call function to open csv file and read in rows
        #print dir_name +"/"+ name
        full_path_csv = dir_name +"/"+ name
        source_text = dir_name +"/"+getTable(name)+".txt"
        source_text = getSource(source_text)
        readRows(full_path_csv, source_text)

print "build/meta_lookup.js made"
