import argparse
import catconv.operations as co
import catconv.stabi as sb
from tqdm import tqdm
import logging
from logging.config import fileConfig

parser = argparse.ArgumentParser()
parser.add_argument("source")
parser.add_argument("-u", "--update", help="overwrite previous results",
                    action="store_true")
parser.add_argument("-b", "--binarize", help="create binary images",
                    action="store_true")
parser.add_argument("-s", "--segment", help="extract text lines",
                    action="store_true")
parser.add_argument("-p", "--predict", help="predict text", required=False)
parser.add_argument("-e", "--ext", help="file-extesion", required=False)
args = parser.parse_args()

fileConfig('logging_config.ini')
logger = logging.getLogger()

source = sb.op.normpath(args.source)
data_dir, cat_name = sb.op.split(source)
catalog = sb.load_catalog(source, {'ext': args.ext}, text_box=True, text=True)
pages = catalog['pages']
# pages = map(sb.page_from_path, sb.catalog_pages(source))

logger.info('Processing {}'.format(catalog['name']))
logger.info("Number of pages {}".format( len(pages)))

# limit the amount of pages for testing
amount = min(len(pages),100)
step_size = len(pages) // amount

for page in tqdm(pages):
    png = page["path"]
    bin_png = sb.change_path(png, ext=".bin.png")
    seg_png = sb.change_path(png, ext=".pseg.png")
    bin_job = co.binarize(png)
    seg_job = co.segment(bin_png)

    if args.binarize and not sb.op.exists(bin_png):
        co.execute_job(bin_job)
    if args.segment and not sb.op.exists(seg_png):
        co.execute_job(seg_job)

if args.predict:
    print("Predicting text lines")
    lines = sb.op.join(args.source, "*", "????????", "??????.bin.png")
    pred_job = co.predict(lines, args.predict, 7)
    co.execute_job(pred_job)
