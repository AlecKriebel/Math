"""Bounded ordinary retrieval of two newly surfaced institutional PDFs."""
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import subprocess
import urllib.request
from urllib.parse import urlsplit, urlunsplit

HERE=Path(__file__).resolve().parent
PRIVATE=HERE/'private_reading'
PRIVATE.mkdir(exist_ok=True)
targets=[
 ('dipersio_summary','https://www.mat.uniroma3.it/scuola_orientamento/alumni/laureati/dipersio/sintesi.pdf'),
 ('barraquand_HDR','https://www.phys.ens.psl.eu/~barraquand/HDR-barraquand.pdf'),
]


def retrieve(target):
    name,url=target
    row=dict(name=name,url=url,utc=datetime.now(timezone.utc).isoformat(),original_target_source=False)
    try:
        with urllib.request.urlopen(url,timeout=20) as response:
            raw=response.read(40_000_000)
            parts=urlsplit(response.url)
            row.update(status=response.status,final_url=urlunsplit((parts.scheme,parts.netloc,parts.path,'','')),content_type=response.headers.get('Content-Type'))
        row.update(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),pdf_magic=raw.startswith(b'%PDF-'))
        if raw.startswith(b'%PDF-'):
            path=PRIVATE/(name+'.pdf');path.write_bytes(raw)
            text=PRIVATE/(name+'.txt')
            result=subprocess.run(['pdftotext','-layout',str(path),str(text)],capture_output=True,timeout=30)
            row['pdftotext_exit']=result.returncode
            if result.returncode==0:row.update(text_sha256=hashlib.sha256(text.read_bytes()).hexdigest(),text_bytes=text.stat().st_size)
        else:
            (PRIVATE/(name+'.response')).write_bytes(raw)
    except Exception as error:
        row.update(status='retrieval_failed',error_type=type(error).__name__,error=str(error))
    return row


with ThreadPoolExecutor(max_workers=2) as pool:rows=list(pool.map(retrieve,targets))
(HERE/'PRIMARY_LEAD_RETRIEVAL.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,indent=2))
