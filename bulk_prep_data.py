#preps the metadata for import to DB
#it adds the table name to end of the code to match the db

from tempfile import NamedTemporaryFile
import shutil
import csv
import os
from os import path
from os import listdir
import string

#CHANGE THESE

#path to the folder
dir_path = os.path.dirname(os.path.realpath(__file__))
dir_name =  dir_path + "/src/state"
#dir_name =  dir_path + "/src/county"
#dir_name =  dir_path + "/src/county_subdivision"
#dir_name =  dir_path + "/src/census_tract"


#function that finds all csv files in the given filename and  returns it
def find_csv_filenames( path_to_dir, suffix=".csv" ):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]


filenames = find_csv_filenames(dir_name)

#translate_tbl = string.maketrans('', '',)

##This script reads a csv header, replaces and periods or dashes in header titles
##with nothing, and then re-writes the whole file out with the updated header.

##It reads the file, writes a temporary file with the data, and then replaces
##the original file with the edited temporary file

def prep_meatadata(filename):
    translate_tbl = string.maketrans('.-', '__',)
    tempfile = NamedTemporaryFile(delete=False)

    with open(filename, 'rb') as origFile, tempfile:
        reader = csv.reader(origFile)
        writer = csv.writer(tempfile)
        header = next(reader)

        ##get name and also index. Use index to overwrite header name.
        for index, name in enumerate(header):
            name = name.translate(translate_tbl)
            header[index] = name

            #if column is not geo id then append the tables name to the column name
            if "GEO" not in header[index]:
                table_name = filename.split("_with")[0]
                table_name = table_name.split("_")[-1]
                header[index] = header[index] + "_" + table_name

        ##write updated header.
        writer.writerow(header)

        ##rewrite all other rows... Since we did next, it won't grab the header.
        for row in reader:
            writer.writerow(row)

    shutil.move(tempfile.name, filename)
    print filename.split("/")[-1] + " Done"


for name in filenames:
    if "ann" in name:
        # call function to open csv file and read in rows
        tempfile = NamedTemporaryFile(delete=False)
        full_path_csv = dir_name +"/"+ name
        prep_meatadata(full_path_csv)


##replace original file with temp file

#filename = 'test/census_county_test/ACS_14_5YR_S1601_metadata.csv'

#shutil.move(tempfile.name, filename)
print "Done and Over!"
