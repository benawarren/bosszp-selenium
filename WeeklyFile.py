import pandas as pd
import os
import datetime

#Files are stored in this directory
directory = '/Users/benwarren/Documents/GitHub/bosszp-selenium/output_data/WeeklyScrape'

#Get file names from the dir
file_names = os.listdir(directory)

#Consolidate files into a master file
dfs = []
for name in file_names:
    file_path = directory + "/" + name
    dfs.append(pd.read_csv(file_path))

master_file = pd.concat(dfs)

#drop duplicates
master_file.drop_duplicates(inplace=True)

#reset index
master_file = master_file.reset_index(drop=True)

#write to a new file
curr_date = datetime.datetime.today().strftime('%Y-%m-%d')
master_file_name = "/Users/benwarren/Documents/GitHub/bosszp-selenium/output_data/master_file_updated_" + curr_date + ".csv"
master_file.to_csv(master_file_name, index=True)