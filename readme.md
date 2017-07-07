# American FactFinder to DB

To import metadata and data from American FactFinder tables into our database.  A script in this file will also produce a json lookup table with the column names, descriptions, units, table name and source.

### About
Files downloaded from American FactFinder are to be placed in src folder.  The sub folders in the src directory are for the types of geographies downloaded. For each table there should be a data.csv a metadata.csv and txt file with the name of the table. Their may also be a readme.txt file but that is not needed.  These files are produced by AFF when you download them.  It is important to uncheck the box for "Include descriptive data element names".  It would create a row that is unneeded and would break the script.

### Use

1. **Download** files from American FactFinder.

	1. Uncheck  **"Include descriptive data element names"** option

	2. Select **"Data and annotations in a single file"** option

	3. Download one geography at a time  


2. Place the downloaded files in the src folder in the correct geography sub-folders  

3. **Config:** Create a "config.py" file with your database information. For an example, see example_config.py

4. **Edit Master Script:** By default, the system will look for files in the following folders: census_tract, county, county_subdivision, places, and state. You can change this by editing the "dir_opts" variable directly.

5. Run master_script.py from a shell

6. Copy out build/meta_lookup.js to a permenant location


### Files

**bulk_prep_data.py**  
Removes "-" and "." from column names

**bulk_prep_metadata.py**  
Adds a header column of key and prop and Removes "-" and "." from keys.

**make_meta_lookup.py**  
Creates build/meta_lookup.js file.  An object for each column with its table, source, units, and description information. Useful for tooltip lookup in applications.

**csv_to_db.py**  
Finds all the csv files in the folder it is currently pointing at and uploads them to the database, appending the geography type to the table name to create the database name.

**master_script.py**  
A grouping script that runs the other files for each folder specified.


### Folders
**build**  
The lookup table is saved here from make_meta_lookup.py.

**src**  
Where all the files from American FactFinder are saved.  The python scripts look here to run.