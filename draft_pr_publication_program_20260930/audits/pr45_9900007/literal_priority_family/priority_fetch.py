#!/usr/bin/env python3
"""Bounded independent Asmussen primary access; all response bytes retained locally."""
import hashlib
import json
import pathlib
import urllib.error
import urllib.request

root=pathlib.Path(__file__).resolve().parent
urls=(
 ("asmussen_full", "https://projecteuclid.org/journals/annals-of-applied-probability/volume-2/issue-3/On-Coupling-and-Weak-Convergence-to-Stationarity/10.1214/aoap/1177005657.full"),
 ("asmussen_pdf", "https://projecteuclid.org/journals/annals-of-applied-probability/volume-2/issue-3/On-Coupling-and-Weak-Convergence-to-Stationarity/10.1214/aoap/1177005657.pdf"),
 ("asmussen_institution", "https://pure.au.dk/portal/en/publications/on-coupling-and-weak-convergence-to-stationarity"),
)
records=[]
for key,url in urls:
 rec={"key":key,"url":url,"publication_allowed":False}
 try:
  req=urllib.request.Request(url,headers={"User-Agent":"Independent mathematical source audit"})
  with urllib.request.urlopen(req,timeout=18) as r:
   b=r.read();rec.update(status=r.status,effective_url=r.url,headers=dict(r.headers))
 except urllib.error.HTTPError as e:
  b=e.read();rec.update(status=e.code,effective_url=e.url,exception=repr(e))
 except Exception as e:
  b=b"";rec["exception"]=repr(e)
 p=root/"foreign_primary"/(key+(".pdf" if b.startswith(b"%PDF-") else ".bin"))
 p.write_bytes(b);rec.update(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),is_pdf=b.startswith(b"%PDF-"))
 records.append(rec);print(json.dumps(rec),flush=True)
(root/"foreign_primary"/"PRIORITY_FETCH_MANIFEST.json").write_text(json.dumps({"records":records,"publication_allowed":False},indent=2)+"\n")
