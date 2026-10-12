import datetime,hashlib,json,lzma,os,pathlib,sys
R=pathlib.Path(__file__).resolve().parent
def pin(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'mode':oct(p.stat().st_mode&0o777)}
record={'actual_pid':os.getpid(),'argv':sys.argv,'cwd':os.getcwd(),'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'semantics':'All primary PDFs kept complete and byte-lossless. Reproducible rendered scan derivatives retired after current/native-input authentication; whole original scanned PDF, all OCR texts, and the visually inspected Prop5.5 PNG kept.','pdf_archives':[],'retired_render_derivatives':[]}
for p in sorted((R/'private_sources').glob('*.pdf')):
 if p.name in ['hansen1993.pdf','luce1999_attempt.pdf']:continue
 b=p.read_bytes(); c=lzma.compress(b,preset=6)
 if len(b)-len(c)>20000:
  before=pin(p);q=p.with_suffix('.pdf.xz');q.write_bytes(c)
  assert lzma.decompress(q.read_bytes())==b
  record['pdf_archives'].append({'original':before,'archive':pin(q),'decompression_verified':True,'encoding':'xz; original PDF bytes preserved exactly'})
  p.unlink()
receipts=[json.loads(p.read_text()) for p in (R/'process_evidence').glob('ocr_hs-*/execution.json')]
for p in sorted((R/'private_sources').glob('hs-*.png')):
 if p.name=='hs-28.png':continue
 before=pin(p);matches=[v for e in receipts for v in e['argument_file_pins'] if v['path']==str(p)]
 assert len(matches)==1 and matches[0]['sha256']==before['sha256']
 record['retired_render_derivatives'].append({'original':before,'actual_ocr_input_pin':matches[0],'reason':'reproducible pdftoppm -gray -r105 -png derivative from retained complete primary hansen1993.pdf; original primary/OCR text retained','producer':'process_evidence/render_hansen1993/execution.json'})
 p.unlink()
record['ended_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
(R/'SOURCE_COMPACTION.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'pdf_archives':len(record['pdf_archives']),'retired_png_count':len(record['retired_render_derivatives']),'saved_pdf_bytes':sum(x['original']['bytes']-x['archive']['bytes'] for x in record['pdf_archives']),'retired_derivative_bytes':sum(x['original']['bytes'] for x in record['retired_render_derivatives']),'logical_stored_bytes':sum(q.stat().st_size for q in R.rglob('*') if q.is_file())}))
