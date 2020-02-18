from multiprocessing import Pool
import multiprocessing
import urllib.request
from pathlib import Path
import os
import tqdm
import pandas as pd
import argparse
from sys import exit

parser = argparse.ArgumentParser()

parser.add_argument('-c', '--count', default=5, type=int, help='how many files to download (default: 5)')
parser.add_argument('--all', action='store_const', const=True, help='download all (millions!)')
 
args = parser.parse_args()

base_path = os.path.dirname(os.path.realpath(__file__))

files_path = "%s/files" % base_path
url_df = pd.read_csv("files-urls.csv")

if (args.all):
  count = len(url_df.file_key)
  print("Downloading all %s files" % count)
else:
  count = args.count
  print("Downloading %s files" % count)

file_set = url_df.file_key[:count]

def url_for_file_key(file_key):
    file_key = file_key.replace("\"","")
    url = "https://files.sl.nsw.gov.au/fotoweb/thumbnails/150_150/%s" % file_key
    return url

def download_file(file_key):
    file_key = file_key.replace("\"","")
    url = url_for_file_key(file_key)
    file_path = "%s/%s" % (files_path, file_key[:file_key.find("/")])
    file_name = "%s/%s" % (files_path, file_key)
    Path(file_path).mkdir(exist_ok=True, parents=True)
    if (Path(file_name).exists() == False):
        urllib.request.urlretrieve(url, file_name)

pool = multiprocessing.Pool(multiprocessing.cpu_count())

for result in tqdm.tqdm(pool.imap(download_file, file_set), total=count):
    pass

exit(0)