from pathlib import Path
import urllib.request, urllib.error, hashlib, json, datetime, re
from concurrent.futures import ThreadPoolExecutor

ROOT=Path(__file__).resolve().parent
S=ROOT/'sources'; R=ROOT/'receipts'
S.mkdir(exist_ok=True); R.mkdir(exist_ok=True)
def fetch(url, name):
    item={'url':url,'name':name,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Independent mathematical source verification'})
        with urllib.request.urlopen(req,timeout=45) as res:
            data=res.read(); item.update(status=res.status, final_url=res.url, headers=dict(res.headers))
        (S/name).parent.mkdir(parents=True,exist_ok=True)
        (S/name).write_bytes(data)
        item.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
    except Exception as e:
        item.update(error=repr(e))
    return item

catalogue=fetch('https://eulersolve.org/papers/','eulersolve_papers.html')
html=(S/'eulersolve_papers.html').read_text()
codes=sorted(set(re.findall(r'/papers/(amr-050-\d+)/',html)))
tasks=[(f'https://eulersolve.org/papers/{code}/metadata.json',f'metadata/{code}.json') for code in codes]
with ThreadPoolExecutor(max_workers=8) as pool:
    records=[catalogue]+list(pool.map(lambda pair:fetch(*pair),tasks))
(R/'FETCH_CATALOGUE.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps({'codes':codes,'success':sum('sha256'in x for x in records),'failures':[x for x in records if 'error'in x]},indent=2))
