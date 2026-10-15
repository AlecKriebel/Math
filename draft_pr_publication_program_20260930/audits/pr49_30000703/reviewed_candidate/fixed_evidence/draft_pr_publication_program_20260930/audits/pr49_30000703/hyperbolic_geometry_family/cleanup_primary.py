#!/usr/bin/python3
import datetime,hashlib,json,pathlib,shutil
own=pathlib.Path(__file__).parent
meta=json.loads((own/'PRIMARY_IDENTITIES.json').read_text())
temp=pathlib.Path(meta['temporary_directory'])
assert temp.name.startswith('pr49_hyperbolic_primary_')
files=[]
for p in sorted(temp.iterdir()):
    assert p.is_file() and p.suffix in ['.pdf','.png']
    b=p.read_bytes();files.append({'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
shutil.rmtree(str(temp))
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'removed_files':files,'removed_file_count':len(files),'directory_absent_after':not temp.exists(),'foreign_bodies_retained_in_family':False,'raw_pdf_text_ocr_html_http_cache_sql_or_pixels_copied_for_publication':False}
(own/'PRIMARY_DELETION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'removed_file_count':len(files),'directory_absent_after':not temp.exists()}))
