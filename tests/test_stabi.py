import catconv.stabi as sb
import os
import os.path as op
import pytest
from catfixtures import *

def test_to_change_path():
    conv = {'cat': 'SD_png', 'ext': '.png', 'remove_type': True}
    png = sb.change_path('../SD/SD002/TIF/00000643.tif', **conv)
    target = '../SD_png/SD_png002/00000643.png'.split(os.sep)
    result = png.split(os.sep)
    assert result == target

    remove_ext = {'rel_path': '../'}
    png =  '../SD_png/SD002/00000643.png'
    page = sb.change_path(png, **remove_ext)
    assert page ==  'SD_png/SD002/00000643'

    page_bin = 'Cat/Batch/Page.bin.png' 
    assert page_bin == sb.change_path('Cat/Batch/Page.png',ext='.bin.png')
    assert page_bin == sb.change_path('Cat/Batch/Page',ext='.bin.png')
    assert 'Cat/Batch/Page' == sb.change_path(page_bin)

    page_bin = 'SN/SN001/Page.bin.png' 
    assert page_bin == sb.change_path('SN/SN001/Page.png',ext='.bin.png',cat="SN")

def test_page_dir(page):
    assert sb.page_dir(page['path']) == 'SD_png/SD001/00000001'
    assert sb.page_dir('SD_png/SD012/00000420.pseg.png') == 'SD_png/SD012/00000420'
    assert sb.page_dir('SD_png/SD012/00000420') == 'SD_png/SD012/00000420'


def test_read_text(page):
    sb.read_text(page)

def test_read_catalog(unconv_catalog_dir):
    assert sb.batches(unconv_catalog_dir) == ['SD001', 'SD002']

def test_load_catalog(conv_catalog_dir):
    cat_structure = { 'path': conv_catalog_dir,
                      'name': 'SN',
                      'pages':[
                          {'path': 'SN001/00000001'
                        },
                          {'path': 'SN001/00000002'
                            }
                          ,
                          {'path': 'SN002/00000002'
                            }
            ,
        {'path': 'SN002/00000003'
    }
                          ]
                      }
    catalog = sb.load_catalog(conv_catalog_dir)
    sb.change_paths(catalog, {'rel_path': conv_catalog_dir})
    assert cat_structure == catalog
