import time
import pandas as pd
import subprocess
import multiprocessing
import tqdm
import argparse
import os
from pathlib import Path

"""
  Assumes:
  - a summarizer server running at: http://localhost:4567/ via Docker for Mac
  - an image server running at: http://host.docker.internal:8000/ 
    (the way Docker for Mac does same host networking)
  - the existence of a image list in ../data/files-urls.csv
  - the existence of an output folder in ../data/colors_output
"""

parser = argparse.ArgumentParser()

parser.add_argument('-o', '--output_folder', default="./files/colors_output", type=str, help='output folder (created if not provided)')
parser.add_argument('-p', '--processes', default=None, type=int, help='how many processes (default: None which lets Python decide)')

args = parser.parse_args()

cpu = args.processes
output_folder = args.output_folder

count=0
starttime = time.time()

file_path = output_folder
# Create the output folder
if (output_folder is None):
  print("no folder provided, creating default")
  base_path = os.path.dirname(os.path.realpath(__file__))
  files_path = "%s/files" % base_path
  file_path = "%s/%s" % (files_path, "colors_output")
  Path(file_path).mkdir(exist_ok=True, parents=True)
else:
  Path(file_path).mkdir(exist_ok=True, parents=True)

url_df = pd.read_csv("../data/files-urls.csv", index_col='access_pid')

count = len(url_df.file_key)

print("Summarizing %s files with %s processes" % (count, (multiprocessing.cpu_count() if cpu == None else cpu)))

def summarize_row(access_pid, row):
  file_key = row['file_key'].replace("\"","")
  access_pid = access_pid.replace("\"","")
  subprocess.run(["python", "summarizer.py", "-w", file_key, "%s/%s.json" % (file_path, access_pid)])

with multiprocessing.Pool(processes=cpu) as pool:
  for access_pid, row in tqdm.tqdm(url_df.iterrows(), total=count):
    pool.apply(summarize_row, args=(access_pid, row))
  pool.close()
  pool.join()

print('Processed %s files in {} seconds'.format(time.time() - starttime) % count)