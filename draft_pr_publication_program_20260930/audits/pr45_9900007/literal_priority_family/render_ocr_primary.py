#!/usr/bin/env python3
"""Local rendering/OCR only. Foreign primary artifacts stay excluded from publication."""
import hashlib
import json
import pathlib
import subprocess
import datetime

root=pathlib.Path(__file__).resolve().parent
foreign=root/"foreign_primary"
pdf=foreign/"asmussen_pdf.pdf"
records=[]
def run(argv):
 p=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 begin=datetime.datetime.now(datetime.timezone.utc).isoformat()
 out,err=p.communicate()
 records.append({"argv":argv,"pid":p.pid,"launch_utc":begin,"end_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"exit_code":p.returncode,"stdout":out.decode(errors="replace"),"stderr":err.decode(errors="replace")})
 if p.returncode:raise RuntimeError(records[-1])
run(["pdftoppm","-r","125","-png",str(pdf),str(foreign/"asmussen_page")])
pages=sorted(foreign.glob("asmussen_page-*.png"))
for page in pages:
 run(["tesseract",str(page),str(page.with_suffix("")),"-l","eng","--psm","6"])
alltext="".join("\n=== PAGE "+str(i+1)+" ===\n"+p.with_suffix(".txt").read_text() for i,p in enumerate(pages))
(foreign/"asmussen_full_ocr.txt").write_text(alltext)
(foreign/"OCR_OPERATIONS.json").write_text(json.dumps({"publication_allowed":False,"operations":records},indent=2)+"\n")
print(json.dumps({"status":"PASS","pages":len(pages),"ocr_bytes":len(alltext.encode()),"ocr_sha256":hashlib.sha256(alltext.encode()).hexdigest(),"publication_allowed":False}))
