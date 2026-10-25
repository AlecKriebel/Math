import urllib.request,urllib.error,hashlib,json,gzip,datetime,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def fetch(name,url):
 r={"name":name,"request_url":url,"start_utc":now()}
 try:
  req=urllib.request.Request(url,headers={"User-Agent":"Independent mathematical literature audit (no contact)"})
  with urllib.request.urlopen(req,timeout=40) as q:
   b=q.read();r.update(status=q.status,resolved_url=q.geturl(),content_type=q.headers.get("Content-Type"),last_modified=q.headers.get("Last-Modified"))
 except urllib.error.HTTPError as e:
  b=e.read();r.update(status=e.code,error=str(e))
 except Exception as e:
  b=b"";r.update(status=None,error=str(e))
 r.update(end_utc=now(),raw_bytes=len(b),raw_sha256=hashlib.sha256(b).hexdigest())
 raw=ROOT/"private_tmp"/(name+".raw.gz");
 try:raw.write_bytes(gzip.compress(b,mtime=0));r["private_body"]=str(raw.relative_to(ROOT))
 except OSError as e:r["persistence_error"]=str(e)
 if b.startswith(b"%PDF"):
  z=subprocess.run(["pdftotext","-layout","-","-"],input=b,capture_output=True);t=z.stdout;r.update(pdftotext_exit=z.returncode,text_bytes=len(t),text_sha256=hashlib.sha256(t).hexdigest());(ROOT/"private_tmp"/(name+".txt.gz")).write_bytes(gzip.compress(t,mtime=0))
 
 with (ROOT/"FETCH_LEDGER.jsonl").open("a") as f:f.write(json.dumps(r,ensure_ascii=False)+"\n")
 print(json.dumps(r,ensure_ascii=False))
 return r
if __name__=="__main__":fetch(sys.argv[1],sys.argv[2])
