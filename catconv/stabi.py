import glob as g
# import ujson
import os
import os.path as op
import ocrolib
import re

def change_path(path, cat=None, ext=None, remove_type=False, rel_path=None):
    """change catalog paths to a simpler folder structure"""
    norm = os.path.normpath(path)
    path_sep = norm.split(os.sep)
    filename = op.splitext(path_sep[-1])[0]
    # splitext may not remove the extension from names like page1.pseg.bin
    filename = re.sub('\.pseg|\.bin', '', filename)
    # Throw away Filetype dir and filename
    if remove_type:
        path_sep = path_sep[:-2]
    else:
        del path_sep[-1]
    if cat:
        path_sep[-2] = cat
    if ext:
        path_sep.append(filename + ext)
    else:
        path_sep.append(filename)
    path = op.sep.join(path_sep)
    if rel_path:
        path = op.relpath(path, rel_path)
    return path

def convert_path(page, conversion):
    return {'path': change_path(page['path'], **conversion)}

def page_dir(page_path):
    """directory named like the image"""
    pagename = op.basename(change_path(page_path))
    return op.join(op.split(page_path)[0], pagename)

def catalog_pages(cat_path, batch='*', ext='.png', amount=None):
    pattern = op.join(cat_path, '{}/????????{}'.format(batch, ext))
    return g.glob(pattern)

def batches(cat_path):
    pattern = op.join(cat_path, '*')
    batches = sorted(map(op.basename,g.glob(pattern)))
    return batches

def line_index_to_name(idx):
    return '0'+hex((0x010000+(idx)))[2:]

def read_line_boxes(page):
    """read the dimensions of each text line"""
    path = change_path(page['path'], ext='.pseg.png')
    path = path.encode()
    try:
        pseg = ocrolib.read_page_segmentation(path)
    except IOError:
        return []
    regions = ocrolib.RegionExtractor()
    regions.setPageLines(pseg)
    lines = []
    for i in range(1, regions.length()):
        y0, x0, y1, x1 = regions.bboxMath(i)
        lines.append({'name': line_index_to_name(i),
                      'position': [x0, y0, x1, y1]})
    return lines

def load_box_positions(page):
    segments = read_line_boxes(page)
    page['lines'] = segments
    return page

def pages_from_paths(path):
    return {'path': path}

def read_text(page):
    if not 'lines' in page:
        return page
    text_dir = page_dir(page['path'])
    for line in page['lines']:
        path = op.join(text_dir, line['name']) + '.txt'
        text = ""
        if op.isfile(path):
            with open(path, 'rb') as sfile:
                text = sfile.read()
        line['text'] = text


