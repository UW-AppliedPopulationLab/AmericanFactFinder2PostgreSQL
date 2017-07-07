import csv
import sys
import os

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
    fn = array[-1].split("\\")[1]
    file_basename = fn.split("_meta")[0]
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

                with open("C:/Users/caitlinmckown/Desktop/github_clones/AmericanFactFinder2PostgreSQL/build/meta_lookup.js","a+") as lookupfile:
                    #create the json object string
                    string = '{  \n \t code: "'  + str(code)  + '", \n ' \
                            '\t description: "'  + str(description) + '", \n ' \
                            '\t unit: "'  + unit + '", \n ' \
                            '\t data:"'  + source_info + '", \n ' \
                            '\t table: "'  + table + '", \n ' \
                            '\t shortDescription: "'  + description + '" \n }, \n '
                    #write it and close
                    lookupfile.write(string)

def lookup_loop(dir_name, filenames):
    for name in filenames:
        if "metadata" in name:
            # call function to open csv file and read in rows
            source_text = dir_name+"/"+getTable(name)+".txt"
            source_text = getSource(source_text)
            readRows(name, source_text)

    print "build/meta_lookup.js made!"
