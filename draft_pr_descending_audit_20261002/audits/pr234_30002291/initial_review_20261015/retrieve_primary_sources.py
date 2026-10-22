"""Ordinary primary-source reads; full reading copies stay private."""
from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import subprocess
import urllib.request

D=Path(__file__).resolve().parent
R=D/'private_reading';R.mkdir(exist_ok=True)
S=D/'submitted/unsolved_math_prioritization/attempts/30002291'
sources=json.loads((S/'source_manifest.json').read_text())['sources']


def retrieve(row):
    name=Path(row['file']).stem
    result=dict(name=name,url=row['url'],utc=datetime.now(timezone.utc).isoformat(),expected_sha256=row['sha256'])
    try:
        with urllib.request.urlopen(row['url'],timeout=25) as response:raw=response.read(30_000_000)
        assert raw.startswith(b'%PDF-')
        pdf=R/(name+'.pdf');pdf.write_bytes(raw)
        text=R/(name+'.txt')
        out=subprocess.run(['pdftotext','-layout',str(pdf),str(text)],capture_output=True,timeout=30)
        assert out.returncode==0
        result.update(status='retrieved',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),
                      matches_author_source_pin=hashlib.sha256(raw).hexdigest()==row['sha256'],
                      text_bytes=text.stat().st_size,text_sha256=hashlib.sha256(text.read_bytes()).hexdigest())
    except Exception as error:result.update(status='failed',error=type(error).__name__+': '+str(error))
    return result


with ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(retrieve,sources))
(D/'ROOT_PRIMARY_RETRIEVAL.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
