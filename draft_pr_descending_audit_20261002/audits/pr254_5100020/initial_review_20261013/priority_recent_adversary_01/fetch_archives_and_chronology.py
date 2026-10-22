from pathlib import Path
import urllib.request, hashlib, json, datetime, zipfile, io, subprocess
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).resolve().parent; S=ROOT/'sources'; R=ROOT/'receipts'
def fetch(pair):
    url,name=pair; item={'url':url,'name':name,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Independent mathematical source verification'}),timeout=45) as res:
            data=res.read(); item.update(status=res.status, final_url=res.url, headers=dict(res.headers))
        path=S/name; path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(data)
        item.update(bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
        if name.endswith('.zip'):
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                for entry in z.infolist():
                    parts=Path(entry.filename).parts
                    if '..' in parts or Path(entry.filename).is_absolute(): raise ValueError('unsafe archive path')
                    if entry.filename.endswith('.tex'):
                        out=S/'current_tex'/Path(name).stem/entry.filename; out.parent.mkdir(parents=True,exist_ok=True); out.write_bytes(z.read(entry))
    except Exception as e: item.update(error=repr(e))
    return item
tasks=[]
for p in sorted((S/'metadata').glob('*.json')):
    d=json.loads(p.read_text()); tasks.append((f'https://eulersolve.org/papers/{p.stem}/source.zip',f'current_zip/{p.stem}.zip'))
with ThreadPoolExecutor(max_workers=8) as pool: records=list(pool.map(fetch,tasks))
(R/'FETCH_CURRENT_ARCHIVES.json').write_text(json.dumps(records,indent=2)+'\n')
gh='/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
for n in (204,254):
    for suffix,name in [('',f'pr{n}.json'),('/commits',f'pr{n}_commits.json')]:
        res=subprocess.run([gh,'api',f'repos/AlecKriebel/Math/pulls/{n}{suffix}'],capture_output=True,text=True)
        (R/name).write_text(res.stdout); (R/(name+'.stderr')).write_text(res.stderr)
        if res.returncode: raise RuntimeError(name)
print(json.dumps({'archives_success':sum('sha256'in x for x in records),'archive_failures':[x for x in records if 'error'in x],'chronology_files':['pr204.json','pr204_commits.json','pr254.json','pr254_commits.json']},indent=2))
