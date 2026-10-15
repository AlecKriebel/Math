from pathlib import Path
import urllib.request,json,hashlib,datetime,subprocess
A=Path(__file__).resolve().parent/"root_ftt_priority";D=A/"private_sources";D.mkdir(parents=True,exist_ok=True)
items=[]
for name,url in [("ftt_abs.html","https://arxiv.org/abs/2608.20620"),("ftt_v1.pdf","https://arxiv.org/pdf/2608.20620v1")]:
    p=D/name
    if p.exists():raise RuntimeError("Inspect existing retrieval before retry")
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"MathematicalResearchAudit/1.0"}),timeout=45) as r:
        b=r.read(); status=r.status; final=r.url; ct=r.headers.get("Content-Type")
    p.write_bytes(b)
    items.append({"name":name,"url":url,"retrieval_UTC":start,"status":status,"final_url":final,"content_type":ct,"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()})
subprocess.run(["/opt/homebrew/bin/pdftotext","-layout",str(D/"ftt_v1.pdf"),str(D/"ftt_v1.txt")],check=True)
b=(D/"ftt_v1.txt").read_bytes()
items.append({"name":"ftt_v1.txt","type":"private_text_derivative","bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()})
(A/"SOURCE_RETRIEVAL.json").write_text(json.dumps({"UTC":datetime.datetime.now(datetime.timezone.utc).isoformat(),"lead":"MSTY reference21 via current-primary family after its independent first seal; ROOT additional full-body screening","records":items,"source_bodies_private":True},indent=2)+"\n")
print(json.dumps(items,indent=2))

