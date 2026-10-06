#!/usr/bin/env python3
import datetime, hashlib, json, os, pathlib, subprocess, urllib.request

D=pathlib.Path(__file__).resolve().parent
requests=[
('blanco_encinas_1405.3942v1.pdf','https://arxiv.org/pdf/1405.3942v1'),
('blanco_encinas_publisher.pdf','https://link.springer.com/content/pdf/10.1007/s00229-017-0929-4.pdf'),
('laclair_metadata.html','https://arxiv.org/abs/2304.13299'),
('blanco_metadata.html','https://arxiv.org/abs/1405.3942'),
('blanco_publisher_metadata.html','https://link.springer.com/article/10.1007/s00229-017-0929-4'),
]
receipt={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_PID':os.getpid(),'records':[]}
for filename,url in requests:
    rec={'filename':filename,'url':url}
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=20) as response:
            body=response.read(); rec.update(final_url=response.url,http_status=response.status,content_type=response.headers.get('Content-Type'))
        if filename.endswith('.pdf') and not body.startswith(b'%PDF-'): raise ValueError('Response is not a PDF')
        path=D/'private_sources'/filename
        if path.exists() and path.read_bytes()!=body: raise ValueError('Refusing different body overwrite')
        path.write_bytes(body)
        if filename.endswith('.pdf'):
            p=subprocess.run(['/opt/homebrew/bin/pdftotext','-layout',str(path),str(path.with_suffix('.txt'))],capture_output=True)
            if p.returncode!=0: raise ValueError('pdftotext failed')
            rec['extraction_actual_returncode']=p.returncode
        rec.update(bytes=len(body),sha256=hashlib.sha256(body).hexdigest(),status='retrieved')
    except Exception as e: rec.update(status='unavailable',exception_type=type(e).__name__,exception=str(e))
    receipt['records'].append(rec)
    (D/'ADDITIONAL_RETRIEVAL_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps(receipt,indent=2,sort_keys=True))
