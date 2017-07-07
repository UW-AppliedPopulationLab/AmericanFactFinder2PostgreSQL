#preps the metadata for import to DB
#it adds the table name to end of the code to match the db
from tempfile import NamedTemporaryFile
import shutil
import csv

##This script reads a csv header, replaces and periods or dashes in header titles
##with nothing, and then re-writes the whole file out with the updated header.

##It reads the file, writes a temporary file with the data, and then replaces
##the original file with the edited temporary file

def prep_metadata(filename):
    tempfile = NamedTemporaryFile(delete=False)

    with open(filename, 'rb') as origFile, tempfile:
        reader = csv.reader(origFile)
        writer = csv.writer(tempfile)
        header = next(reader)

        #key, prop
        for index, name in enumerate(header):
            header = ["key", "prop"]

        ##write updated header.
        writer.writerow(header)

        ##rewrite all other rows... Since we did next, it won't grab the header.
        for row in reader:
            table_name = filename.split("_meta")[0]
            table_name = table_name.split("_")[-1]
            if "GEO" in row[0]:
                row[0] = row[0].replace(".","_")
                row[0] = row[0].replace(".","_")

            else:
                row[0] = row[0] + "_" + table_name

            writer.writerow([row[0],row[1]])

    shutil.move(tempfile.name, filename)

#############################################################
#############################################################

def metadata_loop(dir_name, filenames):
    for name in filenames:
        if "metadata" in name:
            # call function to open csv file and read in rows
            prep_metadata(name)

    print "Metadata prepared!"
