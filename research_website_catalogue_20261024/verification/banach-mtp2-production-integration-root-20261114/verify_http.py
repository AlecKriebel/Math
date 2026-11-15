"""Ordinary HTTP retrievals bound to the exact installed public files."""
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import quote
import argparse,datetime,hashlib,json
O=Path(__file__).resolve().parent
PUB=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
ap=argparse.ArgumentParser();ap.add_argument('--base-url',required=True);ap.add_argument('--receipt',required=True);args=ap.parse_args()
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
dest=O/args.receipt
need(dest.parent==O and not dest.exists(),'new local receipt name')
installation=json.loads((O/'installation.json').read_text())
files=[Path(r['destination']) for r in installation['copies'] if Path(r['destination']).is_relative_to(PUB)]
files += [PUB/'research/research.css',PUB/'robots.txt',PUB/'favicon.ico']
rows=[]
for f in files:
    rel=str(f.relative_to(PUB));urlpath=rel[:-10] if rel.endswith('index.html') else rel
    u=args.base_url.rstrip('/')+'/'+quote(urlpath)
    with urlopen(u,timeout=30) as r:
        body=r.read();row={'url':u,'final_url':r.url,'status':r.status,'ordered_response_headers':list(r.headers.raw_items()),'bytes':len(body),'sha256':hashlib.sha256(body).hexdigest(),'local_path':str(f),'ordinary_GET_no_cache_bypass':True}
    need(row['status']==200 and body==f.read_bytes(),'status or exact bytes '+u)
    rows.append(row)
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_13_ORDINARY_GETS_EXACT','requests':rows,'live_browser_download_and_tracker_separate':True}
dest.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'status':receipt['status'],'base_url':args.base_url,'requests':len(rows)}))
