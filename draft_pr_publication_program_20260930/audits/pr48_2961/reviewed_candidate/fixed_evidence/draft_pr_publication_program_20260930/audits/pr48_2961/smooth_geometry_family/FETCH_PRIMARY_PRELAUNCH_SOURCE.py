import pathlib, urllib.request, hashlib, json, datetime, subprocess
assert __debug__
r=pathlib.Path(__file__).resolve().parent
sources=[('K3','https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf'),('W20','https://ems.press/content/serial-article-files/46844'),('BIP','https://arxiv.org/pdf/0710.1412'),('T12','https://ems.press/content/serial-article-files/43279?nt=1'),('BHW','https://www.math.lmu.de/~hensel/papers/dagger_arxiv.pdf')]
rows=[]
for name,url in sources:
 t=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Independent mathematics source verification'}),timeout=60) as p: data=p.read(); status=p.status; final=p.url
  assert data.startswith(b'%PDF'), (name,len(data),data[:20])
  dest=r/'tmp'/'pdfs'/f'{name}.pdf';dest.write_bytes(data)
  pp=subprocess.run(['/opt/homebrew/bin/pdftotext','-layout',str(dest),str(dest.with_suffix('.txt'))],capture_output=True)
  assert pp.returncode==0,(name,pp.stderr)
  row={'label':name,'url':url,'final_url':final,'started_utc':t,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':status,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'text_bytes':dest.with_suffix('.txt').stat().st_size,'text_sha256':hashlib.sha256(dest.with_suffix('.txt').read_bytes()).hexdigest(),'retrieved':True}
 except Exception as e:
  row={'label':name,'url':url,'started_utc':t,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'retrieved':False,'exception_type':type(e).__name__,'exception':str(e)}
 rows.append(row)
 print(json.dumps(row),flush=True)
(r/'FRESH_PRIMARY_SOURCE_BINDINGS.json').write_text(json.dumps({'schema':'pr48-smooth-geometry-fresh-primary-source-bindings/v1','sources':rows,'foreign_bodies_transient_only':True},indent=2)+'\n')
assert all(x['retrieved'] for x in rows), 'Failed sources retained; retry separately.'
