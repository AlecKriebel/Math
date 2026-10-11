from pathlib import Path
import hashlib,json,urllib.request,subprocess,datetime
A=Path(__file__).resolve().parent;D=A/'raw_sources';D.mkdir(exist_ok=True)
(A/'.gitignore').write_text('raw_sources/\ntmp/\n')
P=A/'snapshot/unsolved_math_prioritization/attempts/30002200'
rows=[]
for e in json.loads((P/'SOURCE_MANIFEST.json').read_text())['sources']:
 req=urllib.request.Request(e['url'],headers={'User-Agent':'Mozilla/5.0 independent mathematical audit'})
 with urllib.request.urlopen(req,timeout=60) as r:b=r.read();final=r.url
 assert b.startswith(b'%PDF-');dest=D/e['file'];dest.write_bytes(b)
 assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],e['file']
 subprocess.run(['pdftotext','-layout',str(dest),str(dest.with_suffix('.txt'))],check=True)
 rows.append({'file':e['file'],'url':e['url'],'final_url':final,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'exact_historical_PDF_match':True})
(A/'root_primary_source_receipt.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sources':rows,'full_four_PDF_matches':True,'raw_source_files_local_ignored':True,'primary_passages_read_pending':True},indent=2)+'\n')
print(json.dumps(rows,indent=2))
