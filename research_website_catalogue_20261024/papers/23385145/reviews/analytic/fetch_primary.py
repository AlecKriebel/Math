"""Capture selected actual primary bodies after the initial seal; no source replay."""
from pathlib import Path
from datetime import datetime,timezone
from hashlib import sha256
from concurrent.futures import ThreadPoolExecutor
import json
import urllib.request
import urllib.error

P=Path(__file__).resolve().parent


def fetch(spec):
    name,url=spec;target=P/'private-primary'/name
    if target.exists():raise FileExistsError(str(target))
    rec={'requested_url':url,'started_UTC':datetime.now(timezone.utc).isoformat()}
    req=urllib.request.Request(url,headers={'User-Agent':'curl/8.7.1','Accept':'*/*'})
    try:resp=urllib.request.urlopen(req,timeout=45)
    except urllib.error.HTTPError as err:resp=err
    with resp:
        body=resp.read();rec.update(HTTP_status=resp.status,final_url=resp.geturl(),
           headers_in_received_order=list(resp.headers.raw_items()))
    with target.open('xb') as out:out.write(body)
    rec.update(completed_UTC=datetime.now(timezone.utc).isoformat(),path=str(target),
       bytes=len(body),SHA256=sha256(body).hexdigest(),PDF_magic=body.startswith(b'%PDF-'))
    return rec


if __name__=='__main__':
    specs=[('bdh-v1.pdf','https://arxiv.org/pdf/2410.10235v1'),
           ('ducoffe-v1.pdf','https://arxiv.org/pdf/2607.04287v1'),
           ('ccddv-v1.pdf','https://arxiv.org/pdf/2503.15011v1'),
           ('median-arxiv-abstract','https://arxiv.org/abs/1907.10398'),
           ('owr2026-publisher-response','https://ems.press/doi/10.4171/OWR/2026/8'),
           ('soda-publisher-response','https://doi.org/10.1137/1.9781611978322.52')]
    target=P/'PRIMARY_FETCH_01.json'
    if target.exists():raise FileExistsError(str(target))
    with ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(fetch,specs))
    target.write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps([{k:r[k] for k in ('requested_url','HTTP_status','bytes','SHA256','PDF_magic')}
                      for r in results],indent=2))
