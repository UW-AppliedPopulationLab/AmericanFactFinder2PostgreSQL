#preps the metadata for import to DB
#it adds the table name to end of the code to match the db
from tempfile import NamedTemporaryFile
import shutil
import csv
import string

##This script reads a csv header, replaces and periods or dashes in header titles
##with nothing, and then re-writes the whole file out with the updated header.

##It reads the file, writes a temporary file with the data, and then replaces
##the original file with the edited temporary file

def prep_data(filename):
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
                header[index] = header[index] + "_" + table_name.split(".")[0]

        ##write updated header.
        writer.writerow(header)

        ##rewrite all other rows... Since we did next, it won't grab the header.
        for row in reader:
            writer.writerow(row)

    shutil.move(tempfile.name, filename)

#############################################################
#############################################################

def data_loop(dir_name, filenames):
    for name in filenames:
        if "meta" not in name:
            # call function to open csv file and read in rows
            prep_data(name)

    print "Data prepared!"
