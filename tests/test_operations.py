from catfixtures import *
import catconv.operations as co
import catconv.stabi as sb

def test_convert_to_png(tmpdir, unconv_catalog_dir):
    data_dir, cat_name = sb.op.split(unconv_catalog_dir)
    to_path = sb.op.join(str(tmpdir), cat_name)
    pages = map(sb.page_from_path, sb.catalog_pages(unconv_catalog_dir, ext=".tif"))
    assert len(pages) == 4
    conversion = {"ext": ".png", "remove_type": True, "to_cat":str(tmpdir)}
    from_to = [(page, sb.convert_page_path(page, conversion)) for page in pages]

    jobs = [co.convert_to_png(*ft) for ft in from_to]
    
    converted =  sb.catalog_pages(to_path)
    print [str(job['output']) for job in jobs] 
    assert len(converted) == 4

