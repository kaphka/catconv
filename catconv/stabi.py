"""This modules provides functions to process the music catalog provided by
the Staatsbibliothek Berlin"""
import copy
import os
import re

import ocrolib
import ujson

import glob as g
import os.path as op


# import ujson
TIF_PAGES_GLOB = "{name}{batch}/TIF/????????{ext}"
PAGES_GLOB = "{name}{batch}/????????{ext}"

class Catalog(object):
    """collection of catalog cards"""


    def __init__(self, path):
        self.name = op.basename(path)
        self.path = path

def split_path(path):
    """splits path into data_dir, cat_name, batch_name, page_name"""
    norm = os.path.normpath(path)
    # -> /catalogs/S/S001/00001.tif
    pages_dir, file_name = op.split(norm)
    # -> /catalogs/S/S001/TIF/ 00001.tif
    # -> /catalogs/S/S001 00001.tif
    # page file names may contain multiple dots
    page_name = re.sub(r"(\.\w+)+$", "", file_name)
    batch_dir, batch_name = op.split(pages_dir)
    # -> /catalogs/S/S001 TIF
    # -> /catalogs/S S001
    if batch_name == "TIF":
        batch_dir, batch_name = op.split(batch_dir)
    data_dir, cat_name = op.split(batch_dir)
    # -> /catalogs S
    return data_dir, cat_name, batch_name, page_name


def change_path(path, cat=None, ext="", remove_type=False, rel_path=None, to_cat=None):
    """change catalog paths to a simpler folder structure"""
    data_dir, cat_name, batch_name, page_name = split_path(path)
    if cat:
        cat_name = cat
        batch_name = cat_name + batch_name[-3:]
    if to_cat:
        data_dir = to_cat
    changed_path = op.join(data_dir, cat_name, batch_name, page_name + ext)
    if rel_path:
        return op.relpath(changed_path, op.normpath(rel_path))
    else:
        return changed_path

def convert_page_path(page, conversion):
    """create a copy of a page and changes the path"""
    new_path = change_path(page['path'], **conversion)
    new_page = copy.deepcopy(page)
    new_page['path'] = new_path
    return new_page

def page_dir(page_path):
    """directory named like the image"""
    pagename = op.basename(change_path(page_path))
    return op.join(op.split(page_path)[0], pagename)

def catalog_pages(cat_path, batch='*', ext='.png', amount=None):
    # pattern = op.join(cat_path, '{}/????????{}'.format(batch, ext))
    path, name = op.split(cat_path)
    if ext == ".tif":
        pattern = TIF_PAGES_GLOB
    else:
        pattern = PAGES_GLOB
    page_glob = op.join(path, name, pattern.format(name=name, batch=batch, ext=ext))
    return g.glob(page_glob)

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

def page_from_path(path):
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
        
def get_cat_name(batch_name):
    return re.match('([A-S]+)', batch_name).group(0)

def load_catalog(path, selection={}, text_box=False, text=False):
    name = op.basename(path)
    pages = sorted(map(page_from_path, catalog_pages(path, **selection)),key=lambda page: page['path'])
    for page in pages:
        if text_box:
            load_box_positions(page)
        if text:
            read_text(page)
    return {'name': name, 'path': path, 'pages': pages}

def change_paths(cat, conv):
    cat['pages'] = map(lambda page: convert_page_path(page,conv), cat['pages'])
