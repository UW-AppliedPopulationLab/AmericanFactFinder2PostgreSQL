##master script
import sys
import os
import glob

import bulk_prep_metadata as stepOne
import bulk_prep_data as stepTwo
import make_meta_lookup as stepThree
import csv_to_db as stepFour

##Can also run from a hard-coded location if desired. This must be run from command line or it's cranky.
location = os.path.dirname(os.path.realpath(__file__))
source_loc = location+"src"

##Get list of subfolders in src.
dirs = [d for d in os.listdir(source_loc) if os.path.isdir(os.path.join(source_loc, d))]
##Default option: run process for all folders (minus block group).
dir_opts = ['census_tract', 'county', 'county_subdivision', 'places', 'state']

meta_count = 0

##Loop through folders!
for d in dirs:
    if d in dir_opts:
        dir_name = source_loc+"/"+d
        filenames = glob.glob(dir_name+'/*.csv')
        
        if len(filenames) > 0: ##if any CSV files exist in directory
            print "Now starting: "+str(d)
            
            if meta_count == 0:
                ##only run metadata and lookup for first directory!
                ##this breaks down if you have more than one table in your directory, however
                stepOne.metadata_loop(dir_name, filenames)
                stepThree.lookup_loop(dir_name, filenames)
              
            stepTwo.data_loop(dir_name, filenames)
            stepFour.dbify_loop(dir_name, filenames, meta_count)
            meta_count += 1
            
            print "Done with "+str(d)+"!\n\n"
    
print "All done!"
