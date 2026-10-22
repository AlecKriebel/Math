from pathlib import Path
import urllib.request,hashlib,json,datetime,subprocess
D=Path(__file__).resolve().parent
rows=[]
for name,url in [('gross_sullivant_v3','https://arxiv.org/pdf/1404.6989v3'),('homs_kuznetsova_stolz_v1','https://arxiv.org/pdf/2609.02382v1')]:
 p=D/'private_reading'/(name+'.pdf')
 if p.exists():
  print('Existing payload preserved:',name);continue
 req=urllib.request.Request(url,headers={'User-Agent':'Independent mathematical literature verification/1.0'})
 with urllib.request.urlopen(req,timeout=60) as r:b=r.read();final=r.url
 assert b.startswith(b'%PDF'),name
 p.write_bytes(b)
 subprocess.run(['pdftotext','-layout',str(p),str(p.with_suffix('.txt'))],check=True)
 rows.append({'url':url,'final_url':final,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'local_private_pdf':str(p),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
(D/'PRIORITY_PRIMARY_RETRIEVAL.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(rows,indent=2))
