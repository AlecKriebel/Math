import pathlib, urllib.request, hashlib, json, datetime, subprocess
assert __debug__
r=pathlib.Path(__file__).resolve().parent
sources=[('AIM_workshop','https://aimath.org/pastworkshops/kirbylistrep.pdf','pdf'),('FRY19','https://arxiv.org/pdf/1905.07664','pdf'),('dataset_readme','https://huggingface.co/datasets/ulamai/UnsolvedMath/raw/37e53eabe540fb458758e198be61634bd02ee008/README.md','md')]
rows=[]
for name,url,fmt in sources:
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  with urllib.request.urlopen(url,timeout=60) as p: data=p.read();status=p.status;final=p.url
  dest=r/'tmp'/'pdfs'/f'{name}.{fmt}';dest.write_bytes(data)
  if fmt=='pdf':
   assert data.startswith(b'%PDF')
   pp=subprocess.run(['/opt/homebrew/bin/pdftotext','-layout',str(dest),str(dest.with_suffix('.txt'))],capture_output=True);assert pp.returncode==0,pp.stderr
   info=subprocess.run(['/opt/homebrew/bin/pdfinfo',str(dest)],capture_output=True);assert info.returncode==0
   pages=int(next(v for v in info.stdout.decode().splitlines() if v.startswith('Pages:')).split(':')[1])
   row={'pages':pages}
  else:row={'license_yaml_cc_by_4_0':b'license: cc-by-4.0' in data,'utf8_bytes':len(data.decode().encode())}
  row.update({'label':name,'url':url,'final_url':final,'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':status,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'retrieved':True})
 except Exception as e:row={'label':name,'url':url,'started_utc':start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'retrieved':False,'exception_type':type(e).__name__,'exception':str(e)}
 rows.append(row);print(json.dumps(row),flush=True)
(r/'ADDITIONAL_PRIMARY_SOURCE_BINDINGS.json').write_text(json.dumps({'schema':'pr48-smooth-geometry-additional-primary-source-bindings/v1','sources':rows,'foreign_bodies_transient_only':True},indent=2)+'\n')
assert all(x['retrieved'] for x in rows)
