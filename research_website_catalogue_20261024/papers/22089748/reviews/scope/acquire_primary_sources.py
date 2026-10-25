from pathlib import Path
import hashlib,json,subprocess,datetime
r=Path(__file__).resolve().parent
p=r/'primary-sources';p.mkdir(exist_ok=True)
items=[
('tkadlec2020.html','https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1007494'),
('tkadlec2020.pdf','https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1007494&type=printable'),
('tkadlec2020-s1.pdf','https://journals.plos.org/ploscompbiol/article/file?id=10.1371/journal.pcbi.1007494.s001&type=supplementary'),
('svoboda2024.html','https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1012008')]
rows=[]
for name,url in items:
 q=p/name
 if not q.exists():
  proc=subprocess.run(['curl','--fail','--location','--silent','--show-error','--max-time','60','--output',str(q),url],capture_output=True,text=True)
  if proc.returncode:
   rows.append({'name':name,'url':url,'status':'download_failed','error':proc.stderr});continue
 data=q.read_bytes()
 if q.suffix=='.pdf':
  assert data.startswith(b'%PDF-'),name
  subprocess.run(['pdftotext','-layout',str(q),str(q.with_suffix('.txt'))],check=True)
 rows.append({'name':name,'url':url,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'fetched_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'success'})
(r/'primary-source-receipts.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,indent=2))
