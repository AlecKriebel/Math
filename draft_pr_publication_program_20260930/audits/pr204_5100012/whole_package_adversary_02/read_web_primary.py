#!/usr/bin/env python3
import sys
sys.dont_write_bytecode=True
import urllib.request,subprocess,hashlib,json,datetime
from pathlib import Path
H=Path(__file__).resolve().parent
urls=[
('centered','https://zenodo.org/api/records/23085904/files/main.pdf/content'),
('general','https://zenodo.org/api/records/23400541/files/main.pdf/content')]
receipts=[]
for label,url in urls:
 try:
  with urllib.request.urlopen(url,timeout=45) as r: data=r.read();headers=dict(r.headers)
  result=subprocess.run(['/opt/homebrew/bin/pdftotext','-layout','-','-'],input=data,capture_output=True,check=True)
  print('\n=== '+label+' PRIMARY TEXT ===\n'+result.stdout.decode())
  receipts.append(dict(label=label,url=url,UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),headers=headers,text_bytes=len(result.stdout)))
 except Exception as e:
  receipts.append(dict(label=label,url=url,error=repr(e)))
(H/'web_primary_receipt.json').write_text(json.dumps(receipts,indent=2)+'\n')

