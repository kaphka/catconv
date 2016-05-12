import argparse
import catconv.operations as co
import catconv.stabi as sb
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("source")
parser.add_argument("-u", "--update", help="overwrite previous results",
                    action="store_true")
parser.add_argument("-b", "--binarize", help="create binary images",
                    action="store_true")
parser.add_argument("-s", "--segment", help="extract text lines",
                    action="store_true")
parser.add_argument("-p", "--predict", help="predict text", required=False)
args = parser.parse_args()

source = sb.op.normpath(args.source)
data_dir, cat_name = sb.op.split(source)
pages = map(sb.page_from_path, sb.catalog_pages(source))

print("Source catalog:")
print("path:", source)
print("pages:", len(pages))

# limit the amount of pages for testing
amount = 100
step_size = len(pages) // amount

for page in tqdm(pages[:amount * step_size:step_size]):
    png = page["path"]
    bin_png = sb.change_path(png, ext=".bin.png")
    bin_job = co.binarize(png)
    seg_job = co.segment(bin_png)

    if args.binarize:
        co.execute_job(bin_job)
    if args.segment:
        co.execute_job(seg_job)

if args.predict:
    lines = sb.op.join(args.source, "*", "????????", "??????.bin.png")
    pred_job = co.predict(lines, args.predict, 7)
    co.execute_job(pred_job)
