#!/usr/bin/env python3
"""Reproduce private primary-source retrieval; no Git/provider mutation."""
from pathlib import Path
from urllib.request import urlopen, Request
import hashlib,subprocess,json,datetime
ROOT=Path(__file__).resolve().parent
SOURCES=[
 ('DL_finalJEMS','https://ems.press/content/serial-article-files/51451?nt=1','03b84a6c19a8a9b25ad4c8991157f55247fe75e3297bad310aac7bcc85013a8b'),
 ('DGZZ_finalInvent','https://webusers.imj-prg.fr/~anton.zorich/Papers/Large_Genus_Asymptotic_Geometry_2022_Inventiones_published.pdf','372586949b85e272a60b7a0dae2dc1c616cbfb94d0e661f40e5ba3bc8c621239'),
]
def main():
 private=ROOT/'private_reading'; private.mkdir(exist_ok=True)
 transport=ROOT/'private_transport'; transport.mkdir(exist_ok=True)
 for name,url,expected in SOURCES:
  with urlopen(Request(url,headers={'User-Agent':'Independent mathematical source audit'})) as response:
   data=response.read()
   (transport/(name+'_headers.json')).write_text(json.dumps({'url':url,'retrieved_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'headers':dict(response.headers)},indent=2)+'\n')
  actual=hashlib.sha256(data).hexdigest()
  if actual!=expected:
   (private/(name+'_CHANGED.pdf')).write_bytes(data)
   raise RuntimeError(f'{name}: source changed; expected {expected}, got {actual}. Changed payload retained privately.')
  pdf=private/(name+'.pdf'); pdf.write_bytes(data)
  subprocess.run(['pdftotext','-layout',str(pdf),str(private/(name+'.txt'))],check=True)
  print(name,actual)
if __name__=='__main__': main()
