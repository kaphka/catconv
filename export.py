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

catalog = sb.load_catalog(source, {}, text_box=True, text=True)
conv = {'rel_path': source}
catalog['pages'] = map(lambda page: sb.convert_page_path(page, conv), catalog['pages'])


print("Source catalog:")
print("path:", source)
print("pages:", len(catalog['pages']))

with open(target, 'wb') as jfile:
    sb.ujson.dump(catalog, jfile, ensure_ascii=False,indent=2, escape_forward_slashes=False)
# for ft in tqdm(from_to[:amount * step_size:step_size]):
#    co.convert_to_png(*ft)

