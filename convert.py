import argparse
import catconv.operations as co
import catconv.stabi as sb
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("source")
parser.add_argument("target")
parser.add_argument("-u", "--update", help="overwrite previous results",
                    action="store_true")
args = parser.parse_args()

source = sb.op.normpath(args.source)
target = sb.op.normpath(args.target)
data_dir, target_cat_name = sb.op.split(target)
pages = map(sb.page_from_path, sb.catalog_pages(source,ext=".tif"))

print("Source catalog:")
print("path:", source)
print("pages:", len(pages))

conversion = {"ext": ".png", "remove_type": True, "to_cat": data_dir}
from_to = [(tif, sb.convert_path(tif, conversion)) for tif in pages]
amount = 100
step_size = len(from_to) / amount
for ft in tqdm(from_to[:amount * step_size:step_size]):
    co.convert_to_png(*ft)

