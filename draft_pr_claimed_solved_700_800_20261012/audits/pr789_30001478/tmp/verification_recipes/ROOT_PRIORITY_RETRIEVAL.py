from pathlib import Path
import concurrent.futures,datetime,hashlib,json,subprocess,urllib.request
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr789_30001478/tmp");W=T/"scratch_priority_root";W.mkdir(exist_ok=True);M=T/"root-receipts"
items=[("NS1206_v2","https://arxiv.org/pdf/1206.0760v2","pdf"),("Campbell2016","https://era.ed.ac.uk/bitstreams/ca9b4e97-4142-4f02-b516-c99c7584481c/download","pdf"),("RS2012_Crossref","https://api.crossref.org/works/10.1112/S0010437X12000188","json"),("NS2015_VOR","https://link.springer.com/content/pdf/10.1007/s00209-015-1470-3.pdf","pdf")]
def fetch(item):
 name,url,kind=item;out={"name":name,"requested_url":url,"utc":datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Math-independent-source-audit/1.0"}),timeout=90)as response:b=response.read(12000001);out.update(HTTP_status=response.status,final_url=response.url)
  assert len(b)<12000001
  p=W/(name+"."+kind);assert not p.exists()
  if kind=="pdf":
   assert b.startswith(b"%PDF");p.write_bytes(b);txt=W/(name+".txt");r=subprocess.run(["pdftotext","-layout",str(p),str(txt)],capture_output=True,text=True);assert r.returncode==0;out.update(text_sha256=hashlib.sha256(txt.read_bytes()).hexdigest())
  else:
   data=json.loads(b);p.write_bytes(b);msg=data["message"];out["normalized_metadata"]={k:msg.get(k)for k in["DOI","title","publisher","published","published-online","published-print","relation","update-to","updated-by","link","version","assertion"]}
  out.update(result="FETCHED",bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
 except Exception as e:out.update(result="UNREAD_FETCH_FAILED",error_type=type(e).__name__,error=str(e))
 return out
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as ex:rows=list(ex.map(fetch,items))
out={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"scope":"Root follow-up retrievals, source bodies/metadata stay excluded scratch; no full-body or priority reading yet claimed","sources":rows};(M/"ROOT_PRIORITY_RETRIEVALS.json").write_text(json.dumps(out,indent=2)+"\n");print(json.dumps(out))
