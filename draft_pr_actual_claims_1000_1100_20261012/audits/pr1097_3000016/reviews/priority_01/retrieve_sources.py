#!/usr/bin/env python3
"""Bounded read-only public retrieval; no authentication, outreach or services."""
from pathlib import Path
import subprocess, json, hashlib, datetime, concurrent.futures
ROOT = Path(__file__).resolve().parent
SOURCES = [
    ('FL_v3', 'https://arxiv.org/pdf/1502.04690v3'),
    ('HKT_v4', 'https://arxiv.org/pdf/1507.03209v4'),
    ('T_v2', 'https://arxiv.org/pdf/2102.11970v2'),
    ('BL_author', 'https://www.cs.elte.hu/~lovasz/morepapers/abacus.pdf'),
    ('BL_journal', 'https://www.emis.de/journals/JACO/Volume1_4/l31v67681vv718ll.fulltext.pdf'),
    ('T_thesis', 'https://tmlilla.web.elte.hu/tezis.pdf'),
    ('Hoang_thesis', 'https://www.research-collection.ethz.ch/bitstreams/5fa373e7-1715-4fa8-9643-915d2bdf9696/download'),
    ('ACE_journal', 'https://www.combinatorics.org/ojs/index.php/eljc/article/download/v33i2p5/pdf/'),
    ('ACE_latest', 'https://arxiv.org/pdf/2411.18364'),
    ('MD_latest', 'https://arxiv.org/pdf/2604.13949'),
    ('CL_latest', 'https://arxiv.org/pdf/1804.03322'),
    ('KT_latest', 'https://arxiv.org/pdf/1407.6958'),
    ('HT_latest', 'https://arxiv.org/pdf/1511.03568'),
    ('HLM_latest', 'https://arxiv.org/pdf/0801.3306'),
    ('Klivans_book', 'https://www.dam.brown.edu/people/cklivans/Chip-Firing.pdf'),
]

def retrieve(item):
    key, url = item
    raw = ROOT / 'sources/raw' / (key + '.pdf')
    raw.parent.mkdir(parents=True, exist_ok=True)
    before = datetime.datetime.now(datetime.timezone.utc).isoformat()
    p = subprocess.run(['curl','-L','--max-time','45','--connect-timeout','12','-sS','-w','%{http_code}', '-o',str(raw),url],capture_output=True,text=True)
    row = {'id':key,'url':url,'utc':before,'curl_exit':p.returncode,'http_code':p.stdout.strip(),'stderr':p.stderr.strip()}
    if raw.is_file():
        b=raw.read_bytes(); row.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),is_pdf=b.startswith(b'%PDF'))
        if row['is_pdf']:
            text_path=ROOT/'sources/extracted'/(key+'.txt'); text_path.parent.mkdir(parents=True,exist_ok=True)
            e=subprocess.run(['pdftotext','-layout',str(raw),str(text_path)],capture_output=True,text=True)
            row.update(extract_exit=e.returncode,extract_stderr=e.stderr.strip())
            if text_path.is_file():
                t=text_path.read_bytes(); row.update(text_bytes=len(t),text_sha256=hashlib.sha256(t).hexdigest(),pdf_pages=text_path.read_text().count('\f'))
        else:
            raw.unlink()
    return row

if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        rows=list(pool.map(retrieve,SOURCES))
    out=ROOT/'SOURCE_RETRIEVAL.json'
    out.write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'records':rows},indent=2)+'\n')
    print(json.dumps([{k:v for k,v in r.items() if k in ('id','http_code','curl_exit','bytes','is_pdf','pdf_pages')} for r in rows]))
