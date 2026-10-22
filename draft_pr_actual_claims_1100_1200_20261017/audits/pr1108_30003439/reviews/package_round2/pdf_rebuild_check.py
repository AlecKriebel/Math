#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime,timezone
from hashlib import sha256
import json,subprocess,shutil
from pypdf import PdfReader
from PIL import Image,ImageChops
ROOT=Path(__file__).resolve().parent;TMP=ROOT/'tmp';PUB=ROOT.parents[1]/'publication'
old=PUB/'output/pdf/negative-curvature-cone.pdf';new=TMP/'compiled/main.pdf'
a,b=PdfReader(old),PdfReader(new)
checks=[]
def check(truth,label):
 if not truth:raise RuntimeError(label)
 checks.append(label)
check(len(a.pages)==len(b.pages)==5,'both have exactly 5 pages')
check((TMP/'original.txt').read_bytes()==(TMP/'rebuilt.txt').read_bytes(),'layout-extracted text byte-identical')
check(a.metadata.title==b.metadata.title=='A negative-curvature normal barrier on an algebraic cone that is not a hyperbolicity cone','PDF title metadata')
check(a.metadata.author==b.metadata.author=='Alec Kriebel','PDF author metadata')
pages=[]
for i,(x,y)in enumerate(zip(a.pages,b.pages),1):
 check(list(x.mediabox)==list(y.mediabox),'page dimensions '+str(i))
 check(x.extract_text()==y.extract_text(),'page text exact '+str(i))
 check(x.get_contents().get_data()==y.get_contents().get_data(),'page drawing streams exact '+str(i))
 im=Image.open(TMP/f'rendered_original/page-{i}.png').convert('RGB');jm=Image.open(TMP/f'rendered_rebuilt/page-{i}.png').convert('RGB')
 check(im.size==jm.size,'render dimensions '+str(i));diff=ImageChops.difference(im,jm)
 box=diff.getbbox();check(box is None,'zero pixel differences '+str(i))
 pages.append({'page':i,'size_pixels':im.size,'different_pixels':0,'drawing_stream_bytes':len(x.get_contents().get_data()),'text_characters':len(x.extract_text())})
 for annot in x.get('/Annots',[]):
  ann=annot.get_object();rect=list(ann.get('/Rect',[]))
  if rect:check(float(rect[0])>=0 and float(rect[1])>=0 and float(rect[2])<=float(x.mediabox.right) and float(rect[3])<=float(x.mediabox.top),'link rectangle in page '+str(i))
log=(TMP/'compiled/main.log').read_text()
check('undefined references' not in log and 'Overfull' not in log and 'Underfull' not in log,'no overflow/undefined-reference warnings')
version=subprocess.check_output(['tectonic','--version'],text=True).strip()
meta_diffs={str(k):{'original':str(a.metadata.get(k)),'rebuilt':str(b.metadata.get(k))}for k in set(a.metadata)|set(b.metadata)if a.metadata.get(k)!=b.metadata.get(k)}
# Only remove the explicitly named cache created for this review; not shared cache.
cache=TMP/'TectonicCache'
if cache.exists():
 check(cache.parent.resolve()==TMP.resolve() and cache.name=='TectonicCache' and not cache.is_symlink(),'isolated review cache cleanup path')
 shutil.rmtree(cache)
result={'status':'PASS','timestamp_utc':datetime.now(timezone.utc).isoformat(),'compiler':version,'compile_command':'TECTONIC_CACHE_DIR=review/tmp/TectonicCache tectonic -C --untrusted --keep-logs --outdir review/tmp/compiled review/tmp/unpacked/main.tex','network_downloads':'disabled (-C)','checks':len(checks),'original_sha256':sha256(old.read_bytes()).hexdigest(),'rebuilt_sha256':sha256(new.read_bytes()).hexdigest(),'metadata_differences':meta_diffs,'page_results':pages,'visual_inspection':'pending, record after viewing all five pages','cache_cleanup':'only own APFS-cloned isolated cache removed'}
(ROOT/'pdf_rebuild_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
