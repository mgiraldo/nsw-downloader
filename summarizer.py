import time
import urllib.request
from pathlib import Path
import multiprocessing
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('image', type=str, help='image URL (if WITH_IMAGE_SERVER is present then relative path in IMAGE_SERVER)')
parser.add_argument('filename', default="summary.json", type=str, help='destination filename (default: summary.json)')
parser.add_argument('-ss', '--summarizer_server', default="http://localhost:4567", type=str, help='summarizer server endpoint that conforms to the https://github.com/mgiraldo/color-summarizer-docker charactoeristics (default: http://localhost:4567)')
parser.add_argument('-is', '--image_server', default="http://host.docker.internal:8000/", type=str, help='image server endpoint (default: http://host.docker.internal:8000/)')
parser.add_argument('-w', '--with_image_server', action='store_const', const=True, help='use the image server providing path in image server')
parser.add_argument('-v', '--verbose', action='store_const', const=True, help='print messages for images processed or not found')

args = parser.parse_args()

summarizer_server = args.summarizer_server
image_server = args.image_server
with_image_server = args.with_image_server
verbose = args.verbose
image = args.image
filename = args.filename

def summarize_file():
    if (with_image_server):
      image_url = "%s%s" % (image_server, image)
    else:
      image_url = image
    url = "%s/?url=%s" % (summarizer_server, image_url)
    if (Path(filename).exists() == False):
        try:
            if (verbose):
                print(url)
            urllib.request.urlretrieve(url, filename)
            return True
        except BaseException as e:
            if (verbose):
                print("Could not retrieve: %s " % url)
                print("  Error: %s " % e)
            return False
    else:
        if (verbose):
            print("File exists: %s" % filename)
        return False

if __name__ == '__main__':
    starttime = time.time()
    processed = summarize_file()
    if (processed and verbose):
        print('Processed in {} seconds'.format(time.time() - starttime))