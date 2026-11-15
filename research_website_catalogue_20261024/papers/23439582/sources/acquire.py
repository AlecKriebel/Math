"""Source custody only: ordinary public HTTPS, immutable originals, no code execution.
Scientific manuscript/code/results bodies are not displayed or interpreted.
"""
from pathlib import Path
from urllib.request import Request,urlopen,build_opener,HTTPRedirectHandler
from urllib.error import HTTPError
from datetime import datetime,timezone
import json,hashlib,sys

S=Path(__file__).resolve().parent
ATT=S/'attempts/20261115T035031Z'
def now():return datetime.now(timezone.utc).isoformat()
class Redirects(HTTPRedirectHandler):
 def __init__(self):super().__init__();self.receipts=[]
 def redirect_request(self,req,fp,code,msg,headers,newurl):
  self.receipts.append({'request_URL':req.full_url,'HTTP_status':code,'response_headers_in_order':list(headers.raw_items()),'next_URL':newurl})
  return super().redirect_request(req,fp,code,msg,headers,newurl)
def get(url,label,path):
 if path.exists():raise RuntimeError('refuse overwrite '+str(path))
 path.parent.mkdir(parents=True,exist_ok=True);handler=Redirects()
 req=Request(url,headers={'User-Agent':'Mozilla/5.0'},method='GET')
 r={'UTC_started':now(),'role':label,'request_URL':url,'request_method':'GET','request_headers_in_order':list(req.header_items())}
 try:
  with build_opener(handler).open(req,timeout=60) as h:
   body=h.read();r.update(HTTP_status=h.status,final_URL=h.url,response_headers_in_order=list(h.headers.raw_items()),error_type=None)
 except HTTPError as h:
  body=h.read();r.update(HTTP_status=h.code,final_URL=h.url,response_headers_in_order=list(h.headers.raw_items()),error_type='HTTPError')
 except Exception as e:
  body=b'';r.update(HTTP_status=None,final_URL=url,response_headers_in_order=[],error_type=repr(e))
 path.write_bytes(body);r.update(UTC_completed=now(),redirect_receipts=handler.receipts,body_path=str(path),bytes=len(body),SHA256=hashlib.sha256(body).hexdigest())
 (path.with_name(path.name+'.receipt.json')).write_text(json.dumps(r,indent=2)+'\n')
 return r
if __name__=='__main__':
 if sys.argv[1]=='record':
  ATT.mkdir(parents=True,exist_ok=True)
  r=get('https://zenodo.org/api/records/23439582','record.attempt-001',ATT/'record.attempt-001.raw')
  print({k:r[k] for k in ('HTTP_status','bytes','SHA256')})
  if r['HTTP_status']==200:
   d=json.loads(Path(r['body_path']).read_text())
   print(json.dumps({'id':d['id'],'title':d['metadata']['title'],'version_field_present':'version' in d['metadata'],'version':d['metadata'].get('version'),'publication_date':d['metadata'].get('publication_date'),'created':d.get('created'),'updated':d.get('updated'),'links':d.get('links'),'files':d['files']},indent=2))
