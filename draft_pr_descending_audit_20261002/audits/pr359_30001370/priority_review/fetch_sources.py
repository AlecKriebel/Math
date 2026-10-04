#!/usr/bin/env python3
"""Fetch complete native payloads with self-contained process receipts. No installs."""
import argparse,datetime,hashlib,json,subprocess
from pathlib import Path

def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def identity(p):
    b=p.read_bytes()
    return {'path':str(p.relative_to(ROOT)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

ROOT=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('name');ap.add_argument('url');args=ap.parse_args()
out=ROOT/'private/payloads'/args.name
headers=ROOT/'private/payloads'/(args.name+'.headers')
stdout=ROOT/'private/payloads'/(args.name+'.stdout')
stderr=ROOT/'private/payloads'/(args.name+'.stderr')
argv=['curl','--location','--max-time','45','--retry','0','--silent','--show-error','--dump-header',str(headers),'--output',str(out),'--write-out','%{json}',args.url]
start=utc();p=subprocess.run(argv,capture_output=True);end=utc()
stdout.write_bytes(p.stdout);stderr.write_bytes(p.stderr)
for q in [out,headers]:
    if not q.exists():q.write_bytes(b'')
r={'name':args.name,'request_url':args.url,'started_utc':start,'finished_utc':end,'argv':argv,'exit_code':p.returncode,'native_payload':identity(out),'headers':identity(headers),'full_stdout':identity(stdout),'full_stderr':identity(stderr),'stderr_utf8':p.stderr.decode('utf-8',errors='replace')}
try:r['curl_metadata']=json.loads(p.stdout)
except Exception:r['curl_metadata']=None
if out.read_bytes().startswith(b'%PDF'):
    txt=out.with_suffix('.txt');ea=['pdftotext','-layout',str(out),str(txt)];es=utc();e=subprocess.run(ea,capture_output=True)
    eo=ROOT/'private/payloads'/(args.name+'.extraction.stdout');ee=ROOT/'private/payloads'/(args.name+'.extraction.stderr');eo.write_bytes(e.stdout);ee.write_bytes(e.stderr)
    r['extraction']={'argv':ea,'started_utc':es,'finished_utc':utc(),'exit_code':e.returncode,'full_stdout':identity(eo),'full_stderr':identity(ee),'stderr_utf8':e.stderr.decode('utf-8',errors='replace'),'text':identity(txt) if txt.exists() else None}
(ROOT/'private/receipts'/(args.name+'.json')).write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({'name':args.name,'exit_code':p.returncode,'bytes':out.stat().st_size,'http_code':r.get('curl_metadata',{}).get('http_code') if r.get('curl_metadata') else None,'pdf':out.read_bytes().startswith(b'%PDF')}))
