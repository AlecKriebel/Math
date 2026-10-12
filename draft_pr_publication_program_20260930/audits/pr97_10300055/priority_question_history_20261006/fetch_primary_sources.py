#!/usr/bin/env python3
"""Read-only HTTP retrieval into this audit only; no outside communication."""
import datetime, hashlib, json, os, pathlib, subprocess, sys, urllib.request, urllib.error
ROOT=pathlib.Path(__file__).resolve().parent
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
name,url,kind=sys.argv[1:4]
cache=ROOT/'new_primary_sources'; cache.mkdir(exist_ok=True)
dest=cache/(name+('.pdf' if kind=='pdf' else '.html' if kind=='html' else '.json'))
record={'name':name,'url':url,'kind':kind,'UTC_start':utc(),'operator_pid':os.getpid(),'read_only_retrieval':True,'destination':str(dest)}
try:
    req=urllib.request.Request(url,headers={'User-Agent':'Independent mathematics research source audit (read-only; no contact)'})
    with urllib.request.urlopen(req,timeout=30) as r:
        data=r.read(25000001)
        record.update(status=r.status,resolved_url=r.url,headers=dict(r.headers))
    if len(data)>25000000: raise ValueError('Source exceeds 25 MB bounded retrieval limit')
    if kind=='pdf' and not data.startswith(b'%PDF'): raise ValueError('Received non-PDF body for claimed PDF')
    if dest.exists(): raise ValueError('Refusing overwrite of previous retrieval')
    dest.write_bytes(data)
    record.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),retrieved=True)
    if kind=='pdf':
        txt=dest.with_suffix('.txt')
        cmd=['/opt/homebrew/bin/pdftotext','-layout',str(dest),str(txt)]
        cp=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        out,err=cp.communicate(timeout=30)
        dest.with_suffix('.pdftotext.stdout.bin').write_bytes(out)
        dest.with_suffix('.pdftotext.stderr.bin').write_bytes(err)
        record['text_extraction']={'argv':cmd,'pid':cp.pid,'exit':cp.returncode,'stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_sha256':hashlib.sha256(err).hexdigest()}
        if cp.returncode: raise ValueError('pdftotext failed')
        record['text_extraction'].update(text_path=str(txt),text_bytes=txt.stat().st_size,text_sha256=hashlib.sha256(txt.read_bytes()).hexdigest())
except Exception as e:
    record['error']=type(e).__name__+': '+str(e)
    if isinstance(e,urllib.error.HTTPError): record['HTTP_error_status']=e.code
record['UTC_end']=utc()
receipt=cache/(name+'.receipt.json')
receipt.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:record[k] for k in ['name','retrieved','status','bytes','sha256','error'] if k in record}))
sys.exit(0 if record.get('retrieved') and 'error' not in record else 1)
