import argparse
import logging
from logging.config import fileConfig
import tinydb
from tinydb import Query
from tqdm import tqdm
import catconv.stabi as st
import os.path as op
import os


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
    batch, page, line_id = line['id'].split('/')
    cat_name = st.get_cat_name(batch)
    page_path = op.join( cat_name, batch, page)
    target_dir = op.join(args.catalog_source_dir, page_path)
    print(target_dir)