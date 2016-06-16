import argparse
import logging
from logging.config import fileConfig
import tinydb
from tinydb import Query
from tqdm import tqdm

fileConfig('logging_config.ini')
logger = logging.getLogger()

parser = argparse.ArgumentParser()
parser.add_argument("catalog_source_dir")
parser.add_argument("line_text_db_file")
parser.add_argument("line_dir")
args = parser.parse_args()

Line = Query()
db = tinydb.TinyDB(args.line_text_db_file)
lines = db.table('lines')

for line in lines.all():
    print(line)
