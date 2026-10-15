"""Read-only public original-source retrieval; full sources remain private."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import urllib.request

D=Path(__file__).resolve().parent
P=D/'private_reading'
P.mkdir(exist_ok=True)
sources=[
 ('bhp2016_history.html','https://arxiv.org/abs/1604.02307',False),
 ('blp2015_history.html','https://arxiv.org/abs/1506.06679',False),
 ('bhp2018_history.html','https://arxiv.org/abs/1806.10352',False),
 ('bhp2018_functionals.pdf','https://arxiv.org/pdf/1806.10352',True),
]
rows=[]
for name,url,pdf in sources:
    req=urllib.request.Request(url,headers={'User-Agent':'Independent scholarly source verification'})
    with urllib.request.urlopen(req,timeout=35) as response:
        raw=response.read();final=response.url
    assert (raw.startswith(b'%PDF') if pdf else b'<html' in raw.lower()),name
    q=P/name;q.write_bytes(raw)
    row=dict(url=url,final_url=final,path='private_reading/'+name,bytes=len(raw),
             sha256=hashlib.sha256(raw).hexdigest(),retrieved_utc=datetime.now(timezone.utc).isoformat())
    if pdf:
        subprocess.run(['pdftotext','-layout',str(q),str(q.with_suffix('.txt'))],check=True,timeout=30)
        txt=q.with_suffix('.txt').read_bytes()
        row.update(text_sha256=hashlib.sha256(txt).hexdigest(),text_bytes=len(txt))
    rows.append(row)
out=dict(utc=datetime.now(timezone.utc).isoformat(),sources=rows,
         whole_source_texts_private=True,source_retrieval_not_mathematical_or_novelty_certification=True)
(D/'PRIMARY_HISTORY_RETRIEVAL.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
