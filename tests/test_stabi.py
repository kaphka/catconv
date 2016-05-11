import catconv.stabi as sb
import os
import os.path as op
import pytest
from catfixtures import *

def test_to_change_path():
    conv = {'cat': 'SD_png', 'ext': '.png', 'remove_type': True}
    png = sb.change_path('../SD/SD002/TIF/00000643.tif',**conv)
    target = 'SD_png/SD002/00000643.png'.split(os.sep)
    assert png.split(os.sep)[-3:] == target

    remove_ext = {'rel_path': '../'}
    png =  '../SD_png/SD002/00000643.png'
    page = sb.change_path(png, **remove_ext)
    assert page ==  'SD_png/SD002/00000643'

    page_bin = 'Cat/Batch/Page.bin.png' 
    assert page_bin == sb.change_path('Cat/Batch/Page.png',ext='.bin.png')
    assert page_bin == sb.change_path('Cat/Batch/Page',ext='.bin.png')
    assert 'Cat/Batch/Page' == sb.change_path(page_bin)

def test_page_dir(page):
    assert sb.page_dir(page['path']) == 'SD_png/SD001/00000001'
    assert sb.page_dir('SD_png/SD012/00000420.pseg.png') == 'SD_png/SD012/00000420'
    assert sb.page_dir('SD_png/SD012/00000420') == 'SD_png/SD012/00000420'


def test_read_text(page):
    sb.read_text(page)

def test_read_catalog(unconv_catalog_dir):
    assert sb.batches(unconv_catalog_dir) == ['SD001', 'SD002']


