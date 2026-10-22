"""Public read-only primary API check; retain selected bibliographic fields only."""
from urllib.request import Request,urlopen
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
from pathlib import Path
import json,hashlib
urls=['https://zenodo.org/api/records/23087221','https://zenodo.org/api/records/23088516','https://api.datacite.org/dois/10.5281/zenodo.23087221','https://api.datacite.org/dois/10.5281/zenodo.23088516','https://api.github.com/repos/AlecKriebel/Math/pulls/201']
def get(url):
    d={'url':url,'access_UTC':datetime.now(timezone.utc).isoformat()}
    try:
        with urlopen(Request(url,headers={'User-Agent':'Independent-mathematics-package-review','Accept':'application/json'}),timeout=25) as r:b=r.read();d['http_status']=r.status
        j=json.loads(b);d['response_bytes']=len(b);d['response_sha256']=hashlib.sha256(b).hexdigest()
        if 'api.github' in url:d['selected']={'number':j.get('number'),'created_at':j.get('created_at'),'head_sha':j.get('head',{}).get('sha'),'state':j.get('state'),'title':j.get('title')}
        elif 'datacite' in url:
            a=j.get('data',{}).get('attributes',{});d['selected']={k:a.get(k) for k in ('doi','created','registered','published','publicationYear','titles','dates','url')}
        else:d['selected']={k:j.get(k) for k in ('id','created','modified','doi','publication_date')};d['selected']['metadata']={k:j.get('metadata',{}).get(k) for k in ('title','publication_date','version')}
    except Exception as e:d['error']=type(e).__name__+': '+str(e)
    return d
with ThreadPoolExecutor(max_workers=5) as pool:rows=list(pool.map(get,urls))
print(json.dumps({'UTC':datetime.now(timezone.utc).isoformat(),'note':'Only selected public metadata retained; no raw API response copied. API fields do not establish first visibility or derivational independence.','records':rows},indent=2))
