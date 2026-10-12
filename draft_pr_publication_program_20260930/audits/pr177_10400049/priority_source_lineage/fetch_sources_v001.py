from pathlib import Path
from datetime import datetime, timezone
import urllib.request, urllib.error, hashlib, json, sys
from concurrent.futures import ThreadPoolExecutor
BASE=Path(__file__).resolve().parent
PRIVATE=BASE/'private_sources'
PRIVATE.mkdir(exist_ok=True)
def fetch(item):
    name,url=item
    start=datetime.now(timezone.utc).isoformat()
    record={'name':name,'requested_url':url,'start_utc':start}
    req=urllib.request.Request(url,headers={'User-Agent':'Independent mathematical source audit; no redistribution'})
    try:
        with urllib.request.urlopen(req,timeout=35) as response:
            body=response.read()
            record.update({'final_url':response.geturl(),'status':response.status,'headers':dict(response.headers),'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest(),'content_type':response.headers.get('Content-Type')})
        dest=PRIVATE/name
        with dest.open('xb') as f:f.write(body)
        dest.chmod(0o444)
        record['retained']=str(dest)
    except Exception as err:
        record.update({'outcome':'unavailable','error_type':type(err).__name__,'error':str(err)})
    record['end_utc']=datetime.now(timezone.utc).isoformat()
    dest=PRIVATE/(name+'.access.json')
    with dest.open('x') as f:json.dump(record,f,indent=2);f.write('\n')
    dest.chmod(0o444)
    print(json.dumps({k:v for k,v in record.items() if k!='headers'}),flush=True)
    return record
if __name__=='__main__':
    items=json.loads(sys.argv[1])
    with ThreadPoolExecutor(max_workers=6) as pool:list(pool.map(fetch,items))
