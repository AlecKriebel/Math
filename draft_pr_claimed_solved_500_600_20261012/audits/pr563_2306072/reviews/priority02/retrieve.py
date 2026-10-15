import datetime,hashlib,json,pathlib,urllib.request,urllib.error,sys
BASE=pathlib.Path(__file__).resolve().parent
CACHE=BASE/'.cache';CACHE.mkdir(exist_ok=True)
def get(name,url):
 rec={'id':name,'requested_url':url,'retrieved_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'ordinary public URL, no credentials'}
 try:
  with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=35) as r:
   b=r.read();rec.update(status=r.status,resolved_url=r.url,content_type=r.headers.get('Content-Type'),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),pdf_signature=b[:5]==b'%PDF-')
   p=CACHE/(name+('.pdf' if b[:5]==b'%PDF-' else '.bin'));p.write_bytes(b);rec['cache_path']=str(p.relative_to(BASE))
 except Exception as e:rec['error']=repr(e)
 with (BASE/'RETRIEVALS.jsonl').open('a') as f:f.write(json.dumps(rec)+'\n')
 print(json.dumps(rec))
if __name__=='__main__':get(sys.argv[1],sys.argv[2])
