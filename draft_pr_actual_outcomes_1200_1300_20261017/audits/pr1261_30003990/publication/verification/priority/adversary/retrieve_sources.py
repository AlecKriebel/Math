"""Read-only public-primary retrieval; no source-author programs are executed."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import hashlib, json, subprocess, urllib.request

ROOT = Path(__file__).resolve().parent
SOURCES = {
 'totik_varga_2012': 'https://www.math.u-szeged.hu/pot/5fdp.pdf',
 'totik_survey_2013': 'https://publicatio.bibl.u-szeged.hu/3241/1/TotikMadrid.pdf',
 'slot_laurent_1905_v2': 'https://arxiv.org/pdf/1905.08142v2',
 'slot_laurent_2001_v2': 'https://arxiv.org/pdf/2001.11289v2',
 'deklerk_hess_laurent_1603_v2': 'https://arxiv.org/pdf/1603.03329v2',
 'gribling_deklerk_vera_2605_v1': 'https://arxiv.org/pdf/2605.31496v1',
 'laurent_slot_2026_overview': 'https://ir.cwi.nl/pub/36052/36052.pdf',
 'owr_2018': 'https://ems.press/content/serial-article-files/46772?nt=1',
}

def get(item):
    key, url = item
    stamp=datetime.now(timezone.utc).isoformat()
    try:
        req=urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0 (independent mathematical literature audit)'})
        with urllib.request.urlopen(req, timeout=60) as response:
            data=response.read(); final_url=response.url; content_type=response.headers.get('Content-Type')
        dest=ROOT/'_local'/'primary'/(key+'.pdf')
        dest.write_bytes(data)
        if not data.startswith(b'%PDF'):
            raise ValueError('Response is not a PDF')
        proc=subprocess.run(['pdftotext','-layout',str(dest),str(dest.with_suffix('.txt'))],capture_output=True,text=True)
        return {'id':key,'requested_url':url,'final_url':final_url,'retrieved_utc':stamp,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'content_type':content_type,'pdf_path':str(dest.relative_to(ROOT)),'text_path':str(dest.with_suffix('.txt').relative_to(ROOT)),'extraction_exit':proc.returncode,'error':proc.stderr or None}
    except Exception as exc:
        return {'id':key,'requested_url':url,'retrieved_utc':stamp,'error':str(exc)}

if __name__=='__main__':
    with ThreadPoolExecutor(max_workers=8) as pool:
        records=list(pool.map(get,SOURCES.items()))
    (ROOT/'RETRIEVAL_RECEIPT.json').write_text(json.dumps(records,indent=2)+'\n')
    print(json.dumps(records,indent=2))
