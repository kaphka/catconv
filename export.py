import argparse
import logging
from logging.config import fileConfig

from tqdm import tqdm

import catconv.operations as co
import catconv.stabi as sb


parser = argparse.ArgumentParser()
parser.add_argument("source")
parser.add_argument("target")
parser.add_argument("-u", "--update", help="overwrite previous results",
                    action="store_true")
parser.add_argument("-e", "--ext", help="file-extesion", required=False)
args = parser.parse_args()

source = sb.op.normpath(args.source)
target = sb.op.normpath(args.target)
data_dir, target_cat_name = sb.op.split(target)

catalog = sb.load_catalog(source, {'ext': args.ext}, text_box=True, text=True)
pages = catalog['pages']
conv = {'rel_path': source}
catalog['pages'] = map(lambda page: sb.convert_page_path(page, conv), catalog['pages'])


fileConfig('logging_config.ini')
logger = logging.getLogger()
logger.info('Processing {}'.format(catalog['name']))
logger.info("Number of pages {}".format( len(pages)))

with open(target, 'wb') as jfile:
    sb.ujson.dump(catalog, jfile, ensure_ascii=False,indent=2, escape_forward_slashes=False)
# for ft in tqdm(from_to[:amount * step_size:step_size]):
#    co.convert_to_png(*ft)
