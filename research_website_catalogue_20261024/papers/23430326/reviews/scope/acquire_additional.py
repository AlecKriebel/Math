#!/usr/bin/env python3
"""Acquire named public primary sources; preserve successes and ordinary errors."""
from pathlib import Path
import concurrent.futures
import datetime
import hashlib
import json
import shutil
import subprocess
import urllib.error
import urllib.request

PAPER=Path(__file__).resolve().parents[2]
OUT=PAPER/'sources/primary-cache'
OUT.mkdir(exist_ok=True)
SOURCES={'lm14-author': 'https://idus.us.es/bitstreams/9d339eb9-03bf-4cac-bcc9-3ca8f34cf3a6/download', 'gmm-v1': 'https://arxiv.org/pdf/1609.03155v1', 'mos-publisher': 'https://ems.press/content/serial-article-files/26354', 'bp-v2': 'https://arxiv.org/pdf/2008.05036v2', 'lu-matringe-v2': 'https://arxiv.org/pdf/2503.11988v2', 'matringe-offen-v2': 'https://arxiv.org/pdf/2102.00480v2', 'matringe-offen-yang-v2': 'https://arxiv.org/pdf/2303.03663v2', 'sharma-v1': 'https://arxiv.org/pdf/2609.21384v1'}
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def get(item):
    name,url=item;rec={'name':name,'url':url,'started_utc':now()}
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (independent scholarly source verification)'})
        with urllib.request.urlopen(req,timeout=35) as r:
            data=r.read();rec.update({'final_url':r.url,'http_status':r.status,'headers':dict(r.headers)})
    except urllib.error.HTTPError as e:
        data=e.read();rec.update({'final_url':e.url,'http_status':e.code,'headers':dict(e.headers),'error':str(e)})
    except Exception as e:
        data=b'';rec.update({'error':repr(e),'http_status':None})
    rec.update({'retrieved_utc':now(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
    kind='pdf' if data.startswith(b'%PDF-') else 'html' if b'<html' in data[:5000].lower() else 'download'
    raw=OUT/(name+'.'+kind)
    with raw.open('xb') as f:f.write(data)
    rec['raw_path']=str(raw.relative_to(PAPER));rec['is_pdf']=kind=='pdf'
    if kind=='pdf':
        info=subprocess.run([shutil.which('pdfinfo'),str(raw)],capture_output=True,text=True)
        rec['pdfinfo']=info.stdout;rec['pdfinfo_returncode']=info.returncode
        text=subprocess.run([shutil.which('pdftotext'),'-layout',str(raw),'-'],capture_output=True)
        target=OUT/(name+'.txt')
        with target.open('xb') as f:f.write(text.stdout)
        rec.update({'text_path':str(target.relative_to(PAPER)),'text_bytes':len(text.stdout),'text_sha256':hashlib.sha256(text.stdout).hexdigest(),'text_returncode':text.returncode})
    return rec
receipts=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    for rec in pool.map(get,SOURCES.items()):
        receipts.append(rec);print(json.dumps({k:rec.get(k) for k in ['name','http_status','bytes','is_pdf','error']}),flush=True)
with (PAPER/'sources/primary-additional-acquisition-receipt.json').open('x') as f:f.write(json.dumps({'record_id':'23430326','utc':now(),'sources':receipts},ensure_ascii=False,indent=2)+'\n')
