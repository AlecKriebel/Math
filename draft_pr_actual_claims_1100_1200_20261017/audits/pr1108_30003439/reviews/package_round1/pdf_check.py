#!/usr/bin/env python3
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
from PIL import Image,ImageChops
from pypdf import PdfReader
import json,re
OUT=Path(__file__).resolve().parent
TMP=OUT/'tmp'
a=TMP/'unpacked/output/pdf/negative-curvature-cone.pdf';b=TMP/'compiled/main.pdf'
ra=PdfReader(a);rb=PdfReader(b)
if len(ra.pages)!=5 or len(rb.pages)!=5:raise RuntimeError('Not five pages')
txt=(OUT/'distributed_extracted.txt').read_bytes();newtxt=(OUT/'rebuilt_extracted.txt').read_bytes()
if txt!=newtxt:raise RuntimeError('Extracted text differs')
if b'??'in txt:raise RuntimeError('Unresolved reference marker')
log=(TMP/'compiled/main.log').read_text()
if re.search(r'Overfull|undefined references|undefined citations|LaTeX Error',log,re.I):raise RuntimeError('Compilation diagnostics require attention')
results=[]
for n in range(1,6):
    p=TMP/f'rendered-distributed/page-{n}.png';q=TMP/f'rendered-rebuilt/page-{n}.png'
    x=Image.open(p).convert('RGB');y=Image.open(q).convert('RGB')
    if x.size!=y.size or ImageChops.difference(x,y).getbbox() is not None:raise RuntimeError('Page pixels differ '+str(n))
    results.append({'page':n,'dimensions':list(x.size),'pixels_equal':True,'distributed_render_sha256':sha256(p.read_bytes()).hexdigest(),'rebuilt_render_sha256':sha256(q.read_bytes()).hexdigest()})
r={'status':'PASS','checked_at_utc':datetime.now(timezone.utc).isoformat(),'pages':5,'extracted_text_exact':True,'extracted_text_sha256':sha256(txt).hexdigest(),'compiled_log_clean':True,'pixel_comparison_dpi':110,'page_results':results,'original_pdf_sha256':sha256(a.read_bytes()).hexdigest(),'rebuilt_pdf_sha256':sha256(b.read_bytes()).hexdigest(),'original_pdf_metadata':dict(ra.metadata),'rebuilt_pdf_metadata':dict(rb.metadata),'byte_equality_required':False}
(OUT/'pdf_results.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
