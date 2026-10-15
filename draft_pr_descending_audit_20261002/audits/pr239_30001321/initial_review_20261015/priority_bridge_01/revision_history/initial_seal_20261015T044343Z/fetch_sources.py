import urllib.request,hashlib,json,datetime,pathlib,subprocess
base=pathlib.Path(__file__).resolve().parent
sources=[('bcr_v1_2014','https://arxiv.org/pdf/1405.6819v1'),('bcr_v2_2016','https://arxiv.org/pdf/1405.6819v2'),('bbds23_v3','https://arxiv.org/pdf/2105.09030v3'),('bcd16_v3','https://arxiv.org/pdf/1505.02791v3'),('bbds_v1_2024','https://arxiv.org/pdf/2410.14302v1'),('bbds_v2_2026','https://arxiv.org/pdf/2410.14302v2')]
out=[]
for name,url in sources:
 rec={'name':name,'url':url,'start_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(url,timeout=60) as r: data=r.read(); rec['final_url']=r.url
  p=base/'private_reading'/f'{name}.pdf';p.write_bytes(data)
  rec.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),status='retrieved')
  subprocess.run(['pdftotext','-layout',str(p),str(p.with_suffix('.txt'))],check=True)
 except Exception as e:rec.update(status='failure',error=repr(e))
 rec['finish_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();out.append(rec)
 print(name,rec['status'],rec.get('sha256',''),flush=True)
(base/'SOURCE_RETRIEVAL.json').write_text(json.dumps({'sources':out,'whole_reading_objects_private':True},indent=2)+'\n')
