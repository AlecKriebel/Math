import json,pathlib,hashlib,urllib.request,datetime,subprocess
HERE=pathlib.Path(__file__).resolve().parent
CAND=HERE.parent/'snapshot/problems/30004320_laurent_descent'
RAW=HERE/'private_sources';RAW.mkdir(exist_ok=True)
rows=[]
def walk(v):
 if isinstance(v,dict):
  if all(k in v for k in ('name','url','bytes','sha256')): rows.append({k:v[k] for k in ('name','url','bytes','sha256')})
  for x in v.values():walk(x)
 elif isinstance(v,list):
  for x in v:walk(x)
for n in ['SOURCE_MANIFEST.json','SOURCE_ADDITION_T1.json','SOURCE_ADDITION_T4.json','SOURCE_ADDITION_T5.json']:walk(json.loads((CAND/n).read_text()))
receipt=[]
for row in rows:
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 req=urllib.request.Request(row['url'],headers={'User-Agent':'Independent mathematical source audit'})
 with urllib.request.urlopen(req,timeout=90) as f: data=f.read();final=f.url
 p=RAW/row['name'];p.write_bytes(data)
 actual={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
 if any(actual[k]!=row[k] for k in actual):raise RuntimeError({'source':row,'actual':actual})
 subprocess.run(['pdftotext','-layout',str(p),str(p.with_suffix('.txt'))],check=True)
 text=p.with_suffix('.txt').read_bytes()
 receipt.append(dict(row,download_start_utc=start,download_end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),resolved_url=final,text_bytes=len(text),text_sha256=hashlib.sha256(text).hexdigest()))
 print(row['name'],actual,flush=True)
(HERE/'SOURCE_DOWNLOAD_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
