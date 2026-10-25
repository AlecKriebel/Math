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
SOURCES={
 'flo-numdam':'https://numdam.org/item/10.1007/s10240-012-0040-z.pdf',
 'jpss-columbia':'https://www.math.columbia.edu/~hj/Rankin%20Selberg%20convolutions.pdf',
 'lm16-v3':'https://arxiv.org/pdf/1411.6310v3',
 'owr2011-ems':'https://ems.press/content/serial-article-files/46327',
 'luo-zha-springer':'https://link.springer.com/article/10.1007/s11464-025-0256-0',
 'luo-zha-hep':'https://journal.hep.com.cn/fm/EN/10.1007/s11464-025-0256-0',
 'hku2025-program':'https://hkumath.hku.hk/MathWWW/event/2025/Workshop_Program.pdf'
}
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
with (PAPER/'sources/primary-acquisition-receipt.json').open('x') as f:f.write(json.dumps({'record_id':'23430326','utc':now(),'sources':receipts},ensure_ascii=False,indent=2)+'\n')
