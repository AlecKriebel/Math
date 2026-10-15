from pathlib import Path
import datetime,hashlib,json,zipfile
HERE=Path(__file__).resolve().parent
PRE=HERE.parent
INITIAL=PRE.parent/'initial_review_20261013'
REPO=Path('/Users/alec/Documents/Math')
keys=['path','relative_path','name','absolute_path','external_readonly_path','reading_filename','filename','native_path','relative_original_path','current_reading_name','file','key']
def digest(data):return hashlib.sha256(data).hexdigest()
def walk(x):
    if isinstance(x,dict):
        yield x
        for v in x.values():yield from walk(v)
    elif isinstance(x,list):
        for v in x:yield from walk(v)
with zipfile.ZipFile(PRE/'output/critical_wave_verification.zip') as z:
    contents={n:z.read(n) for n in z.namelist()}
archive_hashes={digest(data):(n,len(data)) for n,data in contents.items()}
disk_files=[p for p in INITIAL.rglob('*') if p.is_file()]
cache={}
results=[]
unresolved=[]
for member,data in contents.items():
    if not member.endswith('.json') or member=='FILE_MANIFEST.json':continue
    for obj in walk(json.loads(data)):
        sha=obj.get('sha256')
        if not isinstance(sha,str) or len(sha)!=64:continue
        name=next((obj[k] for k in keys if isinstance(obj.get(k),str)),None)
        match=None
        if isinstance(name,str) and Path(name).is_absolute() and Path(name).is_file():
            original=Path(name).read_bytes()
            if digest(original)==sha and ('bytes' not in obj or len(original)==obj['bytes']):match=name
        if sha in archive_hashes:
            n,size=archive_hashes[sha]
            if 'bytes' not in obj or obj['bytes']==size:match='ZIP:'+n
        if not match:
            for p in disk_files:
                if 'bytes' in obj and p.stat().st_size!=obj['bytes']:continue
                if p not in cache:cache[p]=digest(p.read_bytes())
                if cache[p]==sha:
                    match=str(p);break
        if not match:
            unresolved.append({'manifest':member,'name_or_path':name,'bytes':obj.get('bytes'),'sha256':sha})
            continue
        results.append({'manifest':member,'name_or_path':name,'bytes':obj.get('bytes'),'sha256':sha,'verified_against':match})
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS' if not unresolved else 'HISTORICAL_INPUT_RECONCILIATION_PENDING','archive_sha256':digest((PRE/'output/critical_wave_verification.zip').read_bytes()),'nested_sha256_objects_checked':len(results),'path_schemas':keys,'all_exact_byte_bindings_valid':not unresolved,'unresolved_historical_objects':unresolved,'results':results,'scope':'Every nested sha256 object, including alternate source-path keys and digest-only receipts. Exact preserved historical files may be renamed. Reading copies are checked locally and not redistributed.'}
(HERE/'ALL_NESTED_PIN_REPRODUCTION.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','nested_sha256_objects_checked','all_exact_byte_bindings_valid']},indent=2))
print(json.dumps(unresolved,indent=2))
