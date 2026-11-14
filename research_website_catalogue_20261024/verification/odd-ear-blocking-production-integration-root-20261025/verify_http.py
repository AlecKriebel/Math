"""Thirteen ordinary GETs against the exact installed outputs; no cache bypass."""
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor
import datetime,hashlib,json,sys
O=Path(__file__).resolve().parent;W=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
mode=sys.argv[1]
if mode not in ('local','live'):raise ValueError(mode)
base='http://127.0.0.1:8765/' if mode=='local' else 'https://aleckriebel.com/'
installation=json.loads((O/'installation.json').read_text())
paths=[Path(r['destination']).relative_to(W) for r in installation['copies'] if Path(r['destination']).is_relative_to(W)]
paths += [Path('research/research.css'),Path('robots.txt'),Path('favicon.ico')]
def get(p):
    rel=str(p);route=rel[:-len('index.html')] if rel.endswith('/index.html') else rel
    requested=base+quote(route)
    with urlopen(requested,timeout=25) as r:
        data=r.read();digest=hashlib.sha256(data).hexdigest()
        if r.status!=200 or digest!=hashlib.sha256((W/p).read_bytes()).hexdigest():raise RuntimeError(requested)
        return {'requested_url':requested,'actual_final_url':r.url,'status':r.status,'bytes':len(data),'sha256':digest,'ordinary_GET':True,'cache_bypass':False,'response_headers':list(r.headers.items()),'exact_installed_bytes':True}
rows=list(ThreadPoolExecutor(max_workers=4).map(get,paths))
qa=json.loads((O/'final-content-check.json').read_text())
if qa['status']!='PASS' or len(rows)!=13 or not all(all(p['checks'].values()) for p in qa['papers'].values()):raise RuntimeError('target/file checks')
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','mode':mode,'ordinary_GETs':rows,'actual_exact_files':13,'target_checks':sum(len(p['checks']) for p in qa['papers'].values()),'renderer_reexecuted':False,'browser_download_native_gates_pending':True,'AA':None,'all203_complete':False}
with (O/(mode+'-http.json')).open('x') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps({'mode':mode,'ordinary_exact_GETs':13,'target_checks':result['target_checks'],'status':'PASS'}))
