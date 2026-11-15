"""Bounded primary-body GET acquisition. Never edits supplied originals."""
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib, json, subprocess

HERE = Path(__file__).resolve().parent / 'primary'
URLS = {
 'BDH-v1': 'https://arxiv.org/pdf/2410.10235v1',
 'Ducoffe-v1': 'https://arxiv.org/pdf/2607.04287v1',
 'CCDDV-v1': 'https://arxiv.org/pdf/2503.15011v1',
 'Median-v2': 'https://arxiv.org/pdf/1907.10398v2',
 'OWR-2026-08': 'https://publications.mfo.de/bitstream/handle/mfo/4442/OWR_2026_08.pdf?isAllowed=y&sequence=1',
 'ESA-2026-133': 'https://drops.dagstuhl.de/storage/00lipics/lipics-vol388-esa2026/LIPIcs.ESA.2026.133/LIPIcs.ESA.2026.133.pdf',
 'MFCS-2021-43': 'https://drops.dagstuhl.de/storage/00lipics/lipics-vol202-mfcs2021/LIPIcs.MFCS.2021.43/LIPIcs.MFCS.2021.43.pdf',
 'SODA-final-attempt': 'https://epubs.siam.org/doi/pdf/10.1137/1.9781611978322.52',
}
def fetch(item):
    name,url=item
    receipt=HERE/(name+'.receipt.json')
    if receipt.exists():
        return {'name':name,'status':'existing, not overwritten'}
    r={'requested_UTC':datetime.now(timezone.utc).isoformat(),'requested_URL':url}
    try:
        with urlopen(Request(url, headers={'User-Agent':'Mozilla/5.0'}), timeout=45) as h:
            body=h.read();r.update(status=h.status, final_URL=h.url,headers_ordered=list(h.headers.raw_items()))
    except HTTPError as h:
        body=h.read();r.update(status=h.code,final_URL=h.url,headers_ordered=list(h.headers.raw_items()))
    except Exception as e:
        r['error']=repr(e);body=b''
    suffix='.pdf' if body.startswith(b'%PDF-') else '.response'
    path=HERE/(name+suffix)
    path.write_bytes(body)
    r.update(path=str(path),bytes=len(body),SHA256=hashlib.sha256(body).hexdigest(),actual_PDF=body.startswith(b'%PDF-'))
    receipt.write_text(json.dumps(r,indent=2)+'\n')
    if r['actual_PDF']:
        subprocess.run(['pdftotext','-layout',str(path),str(HERE/(name+'.txt'))],check=True)
    return {'name':name,**{k:r.get(k) for k in ('status','bytes','SHA256','actual_PDF','error')}}
if __name__=='__main__':
    HERE.mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=6) as pool:
        for r in pool.map(fetch,URLS.items()): print(json.dumps(r))
