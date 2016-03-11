#American FactFinder to DB

To import metadata and data from American FactFinder tables into our database.  A script in this file will also produce a json lookup table with the column names, descriptions, units, table name and source.

###About
Files downloaded from American FactFinder are to be placed in src folder.  The sub folders in the src directory are for the types of geographies downloaded. For each table there should be a data.csv a metadata.csv and txt file with the name of the table. Their may also be a readme.txt file but that is not needed.  These files are produced by AFF when you download them.  It is important to uncheck the box for "Include descriptive data element names".  It would create a row that is unneeded and would break the script.

###Use

1. **Download** files from American FactFinder.

	2. Uncheck  **"Include descriptive data element names"** option
	
	3. Select **"Data and annotations in a single file"** option
	
	
	3. Download one geography at a time  
	
	
2. Place the downloaded files in the src folder in the correct geography sub-folders  

3. In the terminal cd to this directory 'FactFinder_to_DB'

4. **Prepare the meta_data**
	6. In an editor open  bulk_prep_metadata.py and change the dir_name to desired path. Example: `dir_name =  dir_path + "/src/county"`
	
	5. In the terminal type $ `python bulk_prep_metadata.py`
	
5. **Prepare the data**
	6. In an editor open  bulk_prep_data.py and change the dir_name to desired path. 
	
	6. In the terminal type $  `python bulk_prep_data.py`
	
5. **Create the code lookup**

	6. In an editor open  make_meta_lookup.py and change the dir_name to desired path.  
	
	6. In the terminal type $  `python make_meta_lookup.py`

5. **Upload the data and metadata to the database**

	6. In a editor open csv_to_db.py and change the dir_name to desired path /the geography you would like to run
	
	7. Hostname, username, DBname will all need to be updated to run
	
	7. In the terminal type $ `python csv_to_db.py`
	
8. copy out buld/meta_lookup.js to a permeant location

###Files

**bulk_prep_data.py**  
Removes "-" and "." from column names

**bulk_prep_metadata.py**  
Adds a header column of key and prop and Removes "-" and "." from keys.

**make_meta_lookup.py**  
Creates build/meta_lookup.js file.  An object for each column with its table, source, units, and description information. Useful for tooltip lookup in applications.

**csv_to_db.py**  
Finds all the csv files in the folder it is currently pointing at and uploads them to the database, appending the geography type to the table name to create the database name.

###Folders
**build**  
The lookup table is saved here from make_meta_lookup.py.

**src**  
Where all the files from American FactFinder are saved.  The python scrips look here to run.


###Todo:
- [ ] create a python script that runs all the python scripts in the correct order and runs through all the src folders not just one geography at a time.

