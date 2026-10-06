"""GET-only primary-source retrieval, private bodies and public metadata."""
from pathlib import Path
import urllib.request,hashlib,json,datetime,os,subprocess
A=Path(__file__).resolve().parent
D=A/"root_priority_audit_20261006"
D.mkdir(exist_ok=True)
(D/".gitignore").write_text("private_sources/\nprivate_renders/\n")
S=D/"private_sources"; S.mkdir(exist_ok=True)
receipts=[]
sources=[
("yuen_math_0608632v1.pdf","https://arxiv.org/pdf/math/0608632v1"),
("miller_singh_varbaro_2014_author.pdf","https://www.math.utah.edu/~singh/publications/miller_singh_varbaro.pdf"),
("teitler_software_2015_publisher.pdf","https://msp.org/jsag/2015/7-1/jsag-v7-n1-p01-p.pdf")]
for name,url in sources:
 p=S/name
 if p.exists():raise ValueError("Private source already exists; avoid replacing it")
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Independent mathematical source audit"}),timeout=40) as r:
  body=r.read(); final=r.url; ctype=r.headers.get("Content-Type")
 if not body.startswith(b"%PDF"):raise ValueError("Not PDF: "+url)
 p.write_bytes(body)
 child=subprocess.Popen(["/opt/homebrew/bin/pdftotext","-layout",str(p),str(p.with_suffix(".txt"))],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 stdout,stderr=child.communicate(timeout=40)
 if child.returncode or stderr:raise ValueError("Source extraction failed")
 receipts.append({"name":name,"requested_url":url,"final_url":final,"retrieval_start_UTC":start,"retrieval_end_UTC":datetime.datetime.now(datetime.timezone.utc).isoformat(),"bytes":len(body),"sha256":hashlib.sha256(body).hexdigest(),"content_type":ctype,"actual_pdftotext_PID":child.pid,"pdftotext_exit_code":child.returncode,"read_status":"retrieved; body not yet root-read","private_excluded":True})
 out={"schema":"pr117-root-priority-primary-retrieval/v1","actual_operator_PID":os.getpid(),"sources":receipts,"external_individual_contact":False,"service_mutations":False,"priority_clearance":False}
 (D/"PRIMARY_RETRIEVAL_RECEIPT.json").write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
print(json.dumps(out,indent=2,sort_keys=True))

