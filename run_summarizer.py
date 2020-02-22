import time
import pandas as pd
import subprocess

"""
  Assumes:
  - a summarizer server running at: http://localhost:4567/ via Docker for Mac
  - an image server running at: http://host.docker.internal:8000/ 
    (the way Docker for Mac does same host networking)
  - the existence of a image list in ../data/files-urls.csv
  - the existence of an output folder in ../data/colors_output
"""

count=0
starttime = time.time()

url_df = pd.read_csv("../data/files-urls.csv", index_col='access_pid')

def summarize_row(access_pid, row):
  file_key = row['file_key'].replace("\"","")
  access_pid = access_pid.replace("\"","")
  subprocess.run(["python", "summarizer.py", "-w", file_key, "../data/colors_output/%s.json" % access_pid])

for access_pid, row in url_df.iterrows():
  summarize_row(access_pid, row)

print('Processed %s files in {} seconds'.format(time.time() - starttime) % count)