import concurrent.futures,datetime,hashlib,io,json,pathlib,shutil,tarfile,urllib.request
ROOT=pathlib.Path(__file__).resolve().parent
PINNED=pathlib.Path('/Users/alec/Documents/Math/openai_followon_bosonic_capacity/notes/formal_scope/pinned_build/.lake/packages/mathlib')
packages=json.loads((PINNED/'lake-manifest.json').read_text())['packages']
MAX_DOWNLOAD=16*1024*1024
MAX_TOTAL_SOURCE=64*1024*1024
FLOOR=1024*1024*1024
source_total=0
records=[]
for p in packages:
    if shutil.disk_usage(ROOT).free < FLOOR+64*1024*1024:
        raise RuntimeError('Stopped: insufficient reserve for metadata-only source assessment')
    repo=p['url'].removesuffix('.git').split('github.com/')[1]
    url=f"https://codeload.github.com/{repo}/tar.gz/{p['rev']}"
    with urllib.request.urlopen(url,timeout=25) as resp:
        data=resp.read(MAX_DOWNLOAD+1)
    if len(data)>MAX_DOWNLOAD:raise RuntimeError('snapshot exceeded16MiB cap')
    dest=ROOT/'dependency_sources'/p['name']
    dest.mkdir(parents=True,exist_ok=True)
    entries=[]
    with tarfile.open(fileobj=io.BytesIO(data),mode='r:gz') as tf:
        for m in tf.getmembers():
            if not m.isfile() or not m.name.endswith('.lean'):continue
            path=pathlib.PurePosixPath(m.name)
            relative=pathlib.PurePosixPath(*path.parts[1:])
            if '..' in relative.parts or relative.is_absolute():raise RuntimeError('unsafe tar path')
            b=tf.extractfile(m).read()
            source_total+=len(b)
            if source_total>MAX_TOTAL_SOURCE:raise RuntimeError('source assessment exceeded64MiB cap')
            out=dest.joinpath(*relative.parts);out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(b)
            entries.append({'path':str(relative),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)})
    r={'name':p['name'],'revision':p['rev'],'url':url,'tar_sha256':hashlib.sha256(data).hexdigest(),'compressed_bytes':len(data),'lean_source_bytes':sum(e['bytes'] for e in entries),'sources':entries}
    records.append(r)
    print(p['name'],len(data),r['lean_source_bytes'],flush=True)
(ROOT/'receipts/dependency_sources.json').write_text(json.dumps({'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_total_bytes':source_total,'packages':records},indent=2)+'\n')
