#!/usr/bin/env python3
"""Fetch only public primary sources into the ignored private source directory."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from urllib.request import Request, urlopen
import json

SOURCES = [
 ('bkr_publisher_html','https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/on-odd-powers-of-nonnegative-polynomials-that-are-not-sums-of-squares/7C4BAF1C7EBA17DE741C36DB40691412','bkr_publisher.html'),
 ('bkr_published_pdf','https://www.cambridge.org/core/services/aop-cambridge-core/content/view/7C4BAF1C7EBA17DE741C36DB40691412/S2050509426102217a.pdf/div-class-title-on-odd-powers-of-nonnegative-polynomials-that-are-not-sums-of-squares-div.pdf','bkr_published.pdf'),
 ('bkr_arxiv_v1_abstract','https://arxiv.org/abs/2407.21779v1','bkr_arxiv_v1_abstract.html'),
 ('bkr_arxiv_v1_pdf','https://arxiv.org/pdf/2407.21779v1','bkr_arxiv_v1.pdf'),
 ('owr_original_pdf','https://ems.press/content/serial-article-files/47007','owr_2023_14.pdf'),
 ('pinelis_mathoverflow','https://mathoverflow.net/questions/444079/are-truncated-even-degree-binomial-polynomials-psd','pinelis_mathoverflow.html'),
]

def fetch(item):
 key,url,filename=item
 rec={'key':key,'requested_url':url,'started_utc':datetime.now(timezone.utc).isoformat()}
 try:
  req=Request(url,headers={'User-Agent':'Independent mathematical source verification (read-only)'})
  with urlopen(req, timeout=35) as resp:
   raw=resp.read(); final=resp.url
   rec.update(status=resp.status, final_url=final, content_type=resp.headers.get('Content-Type'), bytes=len(raw),sha256=sha256(raw).hexdigest())
  (Path('sources/private')/filename).write_bytes(raw)
  rec['stored_path']='sources/private/'+filename
 except Exception as exc:
  rec['error']=type(exc).__name__+': '+str(exc)
 rec['finished_utc']=datetime.now(timezone.utc).isoformat()
 return rec

if __name__=='__main__':
 records=list(ThreadPoolExecutor(max_workers=5).map(fetch,SOURCES))
 Path('FETCH_LEDGER.json').write_text(json.dumps({'description':'Fresh public primary-source retrieval; copied bodies remain ignored/private.','records':records},indent=2)+'\n')
 print(json.dumps(records,indent=2))
