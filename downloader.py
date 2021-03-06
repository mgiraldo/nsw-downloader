import concurrent.futures
import multiprocessing
import urllib.request
from pathlib import Path
import os
import tqdm
import pandas as pd
import argparse
from urllib.error import HTTPError

parser = argparse.ArgumentParser()

parser.add_argument('-c', '--count', default=5, type=int, help='how many files to download (default: 5)')
parser.add_argument('-p', '--processes', default=None, type=int, help='how many processes (default: None which lets Python decide)')
parser.add_argument('--all', action='store_const', const=True, help='download all (millions!)')

args = parser.parse_args()

base_path = os.path.dirname(os.path.realpath(__file__))
base_url = "https://files02.sl.nsw.gov.au/fotoweb/thumbnails/150_150"
files_path = "%s/files" % base_path
url_df = pd.read_csv("files-urls.csv")

cpu = args.processes

if (args.all):
  count = len(url_df.file_key)
else:
  count = args.count

print("Downloading %s files with %s processes from %s" % (count, (multiprocessing.cpu_count() if cpu == None else cpu), base_url))

file_set = url_df.file_key[:count]

skipped = []

def url_for_file_key(file_key):
  file_key = file_key.replace("\"","")
  url = "%s/%s" % (base_url, file_key)
  return url

def download_file(file_key):
  file_key = file_key.replace("\"","")
  url = url_for_file_key(file_key)
  file_path = "%s/%s" % (files_path, file_key[:file_key.find("/")])
  file_name = "%s/%s" % (files_path, file_key)
  Path(file_path).mkdir(exist_ok=True, parents=True)
  if (Path(file_name).exists() == False):
    try:
      urllib.request.urlretrieve(url, file_name)
    except:
      skipped.append(file_key)
      pass

with multiprocessing.Pool(processes=cpu) as pool:
  for i in tqdm.tqdm(pool.imap_unordered(download_file, file_set), total=count):
    pass
  pool.close()
  pool.join()

if (len(skipped) > 0):
  print("\nSkipped %s files:" % len(skipped))
  print("%s" % skipped)