#!/usr/bin/env python3
from pathlib import Path
import concurrent.futures,datetime,hashlib,json,urllib.request
BASE=Path(__file__).resolve().parent
PRIVATE=BASE.parents[3]/'private/pr0280_package2'
SOURCES=json.loads((BASE/'archive/birational-cycle-verification/SOURCE_REFERENCES.json').read_text())['sources']
def fetch(e):
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        req=urllib.request.Request(e['url'],headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(req,timeout=40) as r:data=r.read();url=r.url
        if not data.startswith(b'%PDF'):raise ValueError('Response is not a PDF')
        p=PRIVATE/(e['id']+'.pdf');p.write_bytes(data)
        sha=hashlib.sha256(data).hexdigest()
        return {'id':e['id'],'url':e['url'],'resolved_url':url,'retrieved_utc':now,
            'bytes':len(data),'sha256':sha,'matches_package_reference':len(data)==e['bytes'] and sha==e['sha256'],
            'private_basename':p.name,'status':'downloaded'}
    except Exception as ex:return {'id':e['id'],'url':e['url'],'attempted_utc':now,'status':'failed','error':str(ex)}
if __name__=='__main__':
    PRIVATE.mkdir(parents=True,exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=7) as pool:r=list(pool.map(fetch,SOURCES))
    print(json.dumps(r,indent=2,sort_keys=True))
