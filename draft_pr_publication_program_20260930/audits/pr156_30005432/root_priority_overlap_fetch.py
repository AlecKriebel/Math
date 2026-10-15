from pathlib import Path
import json, hashlib, datetime, urllib.request, urllib.parse, re, subprocess
A=Path("/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr156_30005432")
D=A/"root_priority_overlap"; P=D/"private_sources"
P.mkdir(parents=True,exist_ok=True)
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def get(url, name):
    before=now()
    req=urllib.request.Request(url,headers={"User-Agent":"Math-public-priority-audit/1.0"})
    with urllib.request.urlopen(req,timeout=35) as r:
        body=r.read(); final=r.url; status=r.status; headers=dict(r.headers)
    path=P/name; path.write_bytes(body)
    return {"url":url,"resolved_url":final,"started_UTC":before,"retrieved_UTC":now(),"status":status,"path":str(path.relative_to(D)),"bytes":len(body),"sha256":hashlib.sha256(body).hexdigest(),"headers":headers}
assessment={"UTC":now(),"status":"ROOT_FIRST_OVERLAP_ASSESSMENT_BEFORE_FULL_LATER_PAPER_READ","original_HEAD":"aec31742f3f26c5b1e533404da57539d17dc94a1","original_commit_UTC":"2026-09-30T12:28:42Z","observations":["Primary EulerSolve page announces October11 2026 exact same Z x Z4 counterexample and property(s) set.","Primary arXiv records confirm March/July/September2026 precursor characterizations and standard constructions; full earlier result comparison by independent families is ongoing.","Existing GitHub commit author/committer dates alone do not certify actual public disclosure; fresh provider PR creation time and original-head file authenticity will be recorded."],"exact_prior_negative_resolution_located":False,"independence_or_mutual_awareness_certified":False,"novelty_or_publication_clearance":False,"mathematics_gate":"ROOT_ACCEPTED_EXACT_SOURCE_INFINITE_BRACE_COUNTEREXAMPLE","context":"Independent agent first assessments were sealed before root supplied cross-family leads; this root chronology family has received status messages, so does not claim isolation from them."}
(D/"FIRST_ASSESSMENT.json").write_text(json.dumps(assessment,indent=2)+"\n")
records=[]
for url,name in [
("https://eulersolve.org/papers/owr-12697693-003/","eulersolve_page.html"),
("https://eulersolve.org/papers/owr-12697693-003/paper.pdf?v=19895b9d96a5","eulersolve_v1_1.pdf"),
("https://eulersolve.org/papers/owr-12697693-003/metadata.json?v=a2a77a90a32e","eulersolve_metadata.json")]:
    records.append(get(url,name))
html=(P/"eulersolve_page.html").read_text()
dois=sorted(set(re.findall(r'https://doi.org/(10\.5281/zenodo\.\d+)',html)))
for doi in dois:
    number=doi.rsplit(".",1)[1]
    try: records.append(get("https://zenodo.org/api/records/"+number,"zenodo_"+number+".json"))
    except Exception as e: records.append({"url":"https://zenodo.org/api/records/"+number,"error":type(e).__name__+": "+str(e)})
run=subprocess.run(["/opt/homebrew/Cellar/gh/2.85.0/bin/gh","api","repos/AlecKriebel/Math/pulls/156"],capture_output=True,text=True,check=True)
raw=run.stdout.encode(); (P/"github_PR156_readback.json").write_bytes(raw)
pr=json.loads(raw); records.append({"source":"GitHub REST authenticated read only","retrieved_UTC":now(),"path":"private_sources/github_PR156_readback.json","bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest()})
receipt={"UTC":now(),"records":records,"original_PR_created_at":pr["created_at"],"current_HEAD":pr["head"]["sha"],"original_HEAD_matches":pr["head"]["sha"]==assessment["original_HEAD"],"PR_state":pr["state"],"draft":pr["draft"],"GitHub_PR_URL":pr["html_url"],"EulerSolve_DOIs_from_page":dois,"provider_writes":False}
(D/"SOURCE_FETCH_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n")
subprocess.run(["/opt/homebrew/bin/pdftotext","-layout",str(P/"eulersolve_v1_1.pdf"),str(P/"eulersolve_v1_1.txt")],check=True)
print(json.dumps({k:v for k,v in receipt.items() if k!="records"},indent=2))
print("Fetched source records:",len(records))

