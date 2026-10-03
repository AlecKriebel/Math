#!/usr/bin/env python3
"""Retrieve official/author source bodies; every body is a foreign exclusion.
This is an access record, not certification of a retrieved source's theorems.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, subprocess, urllib.request
root=Path(__file__).resolve().parent
cache=root/'foreign_primary'
cache.mkdir()
items=[('lomonaco1981','https://userpages.cs.umbc.edu/lomonaco/5knots/Lomonaco-Pacific-Journal-Math.pdf'),
       ('hillman_v3','https://arxiv.org/pdf/math/0212142v3')]
receipts=[]
for name,url in items:
    before=datetime.now(timezone.utc).isoformat()
    with urllib.request.urlopen(url,timeout=45) as response:
        body=response.read(); final=response.geturl(); status=response.status
        kind=response.headers.get('Content-Type')
    after=datetime.now(timezone.utc).isoformat()
    pdf=cache/(name+'.pdf'); pdf.write_bytes(body)
    receipt={'url':url,'final_url':final,'before_utc':before,'after_utc':after,
             'http_status':status,'content_type':kind,'body_path':str(pdf.relative_to(root)),
             'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest()}
    if body[:5]!=b'%PDF-':
        receipts.append(receipt)
        (root/'PRIMARY_ACCESS.json').write_text(json.dumps(receipts,indent=2)+'\n')
        raise RuntimeError('Retrieved body is not a PDF; retained without claiming full-paper access')
    textfile=cache/(name+'.txt')
    argv=['/opt/homebrew/bin/pdftotext','-layout',str(pdf),str(textfile)]
    proc=subprocess.Popen(argv,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout,stderr=proc.communicate()
    receipt['text_extraction']={'argv':argv,'pid':proc.pid,'exit_code':proc.returncode,
                                'stdout_bytes':len(stdout),'stderr_text':stderr.decode(errors='replace')}
    receipts.append(receipt)
    (root/'PRIMARY_ACCESS.json').write_text(json.dumps(receipts,indent=2)+'\n')
    if proc.returncode: raise RuntimeError('PDF extraction failed; retained access receipt')
print(json.dumps(receipts,indent=2))
