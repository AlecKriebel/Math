#!/usr/bin/env python3
"""Independent first-party source acquisition; no candidate imports."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess, urllib.request
ROOT=Path(__file__).resolve().parent
SOURCES=[
 ('aldous2012_long','https://www.stat.berkeley.edu/~aldous/206-SNET/Papers/aldous_SIRSN_long.pdf'),
 ('aldous2014_published','https://www.maths.tcd.ie/EMIS/journals/EJP-ECP/article/download/2920/2920-16115-1-PB.pdf'),
 ('kahn2015_v3','https://arxiv.org/pdf/1503.03976v3'),
 ('blanc_curien_kahn2024_v1','https://arxiv.org/pdf/2407.07887v1'),
]
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def digest(p):
 b=p.read_bytes(); return {'path':p.relative_to(ROOT).as_posix(),'size':len(b),'sha256':hashlib.sha256(b).hexdigest()}
receipts={'purpose':'Full first-party source-only reconstruction before candidate exposure','started_utc':now(),'author_process_pid':os.getpid(),'download_receipts':[],'text_extraction_receipts':[]}
for name,url in SOURCES:
 p=ROOT/'sources'/f'{name}.pdf'; begin=now()
 with urllib.request.urlopen(url,timeout=90) as response:
  data=response.read(); effective_url=response.url; headers=dict(response.headers)
 p.write_bytes(data)
 receipts['download_receipts'].append({'url':url,'effective_url':effective_url,'started_utc':begin,'completed_utc':now(),'pid':os.getpid(),'headers':headers,**digest(p)})
 txt=p.with_suffix('.txt'); stdout=ROOT/'streams'/f'{name}_pdftotext.stdout'; stderr=ROOT/'streams'/f'{name}_pdftotext.stderr'; begin=now()
 with stdout.open('wb') as out, stderr.open('wb') as err:
  proc=subprocess.Popen(['/opt/homebrew/bin/pdftotext','-layout',str(p),str(txt)],stdout=out,stderr=err)
  pid=proc.pid; rc=proc.wait(timeout=90)
 receipts['text_extraction_receipts'].append({'command':['/opt/homebrew/bin/pdftotext','-layout',str(p),str(txt)],'pid':pid,'started_utc':begin,'completed_utc':now(),'returncode':rc,'stdout':digest(stdout),'stderr':digest(stderr),'output':digest(txt) if txt.exists() else None})
 if rc: raise RuntimeError(f'pdftotext failed for {name}')
receipts['completed_utc']=now()
(ROOT/'source_acquisition_receipts.json').write_text(json.dumps(receipts,indent=2)+'\n')
print(json.dumps({'source_count':len(SOURCES),'receipt':'source_acquisition_receipts.json','completed_utc':receipts['completed_utc']},indent=2))
