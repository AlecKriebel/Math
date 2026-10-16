from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, subprocess, urllib.request
A=Path(__file__).resolve().parents[1]
p=A/'root_priority/private';p.mkdir(parents=True,exist_ok=True)
url='https://d-nb.info/107268702X/34'
req=urllib.request.Request(url,headers={'User-Agent':'Math research priority audit'})
with urllib.request.urlopen(req,timeout=45) as response:
 b=response.read();meta=dict(url=url,final_url=response.geturl(),headers=dict(response.headers),UTC=datetime.now(timezone.utc).isoformat(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
if not b.startswith(b'%PDF'):raise RuntimeError('Not a full primary PDF')
(p/'leckey2015_thesis.pdf').write_bytes(b)
subprocess.run(['/opt/homebrew/bin/pdftotext','-layout',str(p/'leckey2015_thesis.pdf'),str(p/'leckey2015_thesis.txt')],check=True,timeout=45)
meta['text_sha256']=hashlib.sha256((p/'leckey2015_thesis.txt').read_bytes()).hexdigest()
(p/'THESIS_ACQUISITION.json').write_text(json.dumps(meta,indent=2)+'\n')
pages=(p/'leckey2015_thesis.txt').read_text().split('\f')
for i in [106,107,108,120,121]:
 print('PDF PAGE '+str(i+1));print(pages[i])
print(json.dumps(meta,indent=2))

