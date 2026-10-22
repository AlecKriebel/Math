from pathlib import Path
import concurrent.futures,datetime,hashlib,json,subprocess,urllib.request
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr789_30001478/tmp");W=T/"scratch_primary";W.mkdir(exist_ok=True);M=T/"root-receipts"
sources=[("OWR2010_22","https://ems.press/content/serial-article-files/46279",[42,43,44]),("RS2012_VOR","https://www.cambridge.org/core/services/aop-cambridge-core/content/view/A716CDDA53B187EB87C28202DBCBBD94/S0010437X12000188a.pdf/div-class-title-some-projective-surfaces-of-gk-dimension-4-div.pdf",[1,5,8,9])]
def fetch(row):
 name,url,pages=row;out={"name":name,"requested_url":url,"utc":datetime.datetime.now(datetime.timezone.utc).isoformat()}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Independent-Math-Source-Verification/1.0"}),timeout=90)as response:b=response.read(12000001);out.update(status=response.status,final_url=response.url)
  assert b.startswith(b"%PDF")and len(b)<12000001;p=W/(name+".pdf");assert not p.exists();p.write_bytes(b)
  text=W/(name+".txt");r=subprocess.run(["pdftotext","-layout",str(p),str(text)],capture_output=True,text=True);assert r.returncode==0
  out.update(result="FETCHED_PDF",bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),text_sha256=hashlib.sha256(text.read_bytes()).hexdigest(),rendered=[])
  for page in pages:
   pref=W/(name+"_page"+str(page));r=subprocess.run(["pdftoppm","-f",str(page),"-l",str(page),"-singlefile","-scale-to","1800","-png",str(p),str(pref)],capture_output=True,text=True);assert r.returncode==0;out["rendered"].append({"page_one_based":page,"path":pref.name+".png","sha256":hashlib.sha256(pref.with_suffix(".png").read_bytes()).hexdigest()})
 except Exception as e:out.update(result="FETCH_OR_RENDER_FAILED",error_type=type(e).__name__,error=str(e))
 return out
with concurrent.futures.ThreadPoolExecutor(max_workers=2)as ex:rows=list(ex.map(fetch,sources))
(M/"ROOT_PRIMARY_RETRIEVAL.json").write_text(json.dumps({"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"scope":"Primary bodies/text/renders remain excluded scratch; this receipt records source custody, not a completed visual inspection","sources":rows},indent=2)+"\n")
print(json.dumps({"sources":rows}))
