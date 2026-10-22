#!/usr/bin/env python3
"""Fetch primary bodies into memory and retain identity/inspection-request metadata only."""
import argparse, datetime, hashlib, json, os, re, subprocess, urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parent

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--id",required=True);p.add_argument("--url",required=True)
    p.add_argument("--pages",default="");p.add_argument("--scan",default="")
    p.add_argument("--find",default="")
    a=p.parse_args()
    receipt={"id":a.id,"requested_url":a.url,"retrieved_utc":datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        with urllib.request.urlopen(urllib.request.Request(a.url,headers={"User-Agent":"IndependentPriorityAudit/1.0"}),timeout=35) as r:
            b=r.read(20_000_001)
            if len(b)>20_000_000:raise ValueError("memory cap")
            receipt.update(status=r.status,resolved_url=r.url,content_type=r.headers.get("Content-Type"),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
        if b.startswith(b"%PDF"):
            t=subprocess.run(["pdftotext","-layout","-","-"],input=b,capture_output=True,check=True).stdout
            pages=t.decode().split("\f")
            if not pages[-1].strip():pages.pop()
            receipt.update(pages=len(pages),text_sha256=hashlib.sha256(t).hexdigest(),physical_pages_requested=a.pages)
            if a.scan:receipt["scan_page_hits"]={x:[i for i,z in enumerate(pages,1) if re.search(x,z,re.I)] for x in a.scan.split(";")}
            selected=set()
            if a.pages:
                for group in a.pages.split(","):
                    if "-" in group:
                        x,y=map(int,group.split("-"));selected.update(range(x,y+1))
                    else:selected.add(int(group))
            if a.find:
                receipt["find_regex"]=a.find
                selected.update(i for i,z in enumerate(pages,1) if re.search(a.find,z,re.I))
            for i in sorted(selected):print("\nPHYSICAL PAGE",i,"\n",pages[i-1])
        else:receipt["body_boundary"]="Non-PDF response; not treated as actual paper body."
    except Exception as e:receipt.update(error_type=type(e).__name__,error=str(e))
    f=ROOT/"SOURCE_FETCH_RECEIPTS.json";rows=json.loads(f.read_text()) if f.exists() else []
    rows.append(receipt);tmp=f.with_name(f.name+".tmp-own");tmp.write_text(json.dumps(rows,indent=2)+"\n");os.replace(tmp,f)
    print("\nRECEIPT",json.dumps(receipt,sort_keys=True))

if __name__=="__main__":main()
