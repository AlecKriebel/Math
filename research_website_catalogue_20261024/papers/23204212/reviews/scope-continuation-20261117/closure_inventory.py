"""Passive final identity inventory of already retrieved data; no network, source execution or Git."""
import datetime, hashlib, json, stat
from pathlib import Path, PurePosixPath

P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN=P/'papers/23204212/reviews/scope-continuation-20261117'
SRC=P/'papers/23204212/sources'
def read_json(p):
    return json.loads(p.read_bytes())
def pin(p):
    a=p.lstat();assert stat.S_ISREG(a.st_mode) and not p.is_symlink()
    raw=p.read_bytes();b=p.lstat()
    fields=lambda s:(s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
    assert fields(a)==fields(b) and len(raw)==a.st_size
    return {'bytes':len(raw),'SHA256':hashlib.sha256(raw).hexdigest(),'mode':oct(stat.S_IMODE(a.st_mode))}
def safe(name):
    p=PurePosixPath(name)
    assert name and not p.is_absolute() and p.as_posix()==name and all(s not in ('.','..') for s in p.parts)
    return name
records=read_json(OWN/'PRIMARY_RETRIEVAL.json')['results']
records += [dict(r,path='classical/'+r['name']) for r in read_json(OWN/'CLASSICAL_SUPPLEMENT_RETRIEVAL.json')['records']]
records += [dict(read_json(OWN/'BCR_ADDENDUM_RETRIEVAL.json'),path='classical/BCR-addendum-1301.0616v1.pdf')]
assert len(records)==99 and len({r['path'] for r in records})==99
inventory=[]
for r in records:
    name=safe(r['path']);actual=pin(OWN/'primary'/name)
    assert actual['bytes']==r['bytes'] and actual['SHA256']==r['SHA256']
    item={'path':'primary/'+name,'identity':actual,'URL':r['URL'],'effective_URL':r['effective_URL'],'retrieval_status':r['status'],'status_code':r['status_code']}
    for k in ('edition','PDF_signature','error_type','error','started_UTC','finished_UTC'):
        if k in r:item[k]=r[k]
    inventory.append(item)
failed=[r for r in inventory if r['retrieval_status'].startswith('FAILED')]
assert len(failed)==1 and failed[0]['path']=='primary/classical/CFP-published-1996.pdf' and failed[0]['PDF_signature'] is False
upstream=read_json(SRC/'archives/01-thompson-cstar-verification.zip.extracted/sources/SOURCE_MANIFEST.json')
assert upstream['upstream_commit']=='adc7f1241b42e322a6451854ab7e4b4c146bf78a' and len(upstream['files'])==88
assert len({r['path'] for r in upstream['files']})==88
for r in upstream['files']:
    actual=pin(OWN/'primary/upstream'/safe(r['path']))
    assert actual['bytes']==r['bytes'] and actual['SHA256']==r['sha256']
before=read_json(OWN/'CUSTODY_BEFORE.json');after=read_json(OWN/'CUSTODY_AFTER.json')
assert all(before[k]==after[k] for k in ('sources','INITIAL'))
native=read_json(OWN/'NATIVE_RUN.json');assert native['attempt']==1 and native['exit_code']==0
assert pin(OWN/'NATIVE.stdout.txt')['bytes']==274 and pin(OWN/'NATIVE.stderr.txt')['bytes']==0
original=SRC/'archives/01-thompson-cstar-verification.zip.extracted/upstream_finite_checks.py'
copy=OWN/'native-run/upstream_finite_checks.py'
assert pin(original)==pin(copy)=={'bytes':7192,'SHA256':'63a71b64cb2104c8550bfe376d08f2930cbeea19722495fdee41d26d85e36f59','mode':'0o644'}
license_name='archives/01-thompson-cstar-verification.zip.extracted/LICENSE_CODE.txt'
assert pin(SRC/license_name)==pin(OWN/'native-run/LICENSE_CODE.txt')
result={'schema':'bounded-independent-primary-and-native-final-inventory-v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'upstream_commit':upstream['upstream_commit'],'primary_request_count':99,'identity_valid_primary_files':98,'upstream_files_exact':88,'valid_classical_PDFs':10,'literal_transport_failures':failed,'native_scientific_attempts':1,'native_scientific_failures':0,'native_run':native,'source_files_childdirs':[55,14],'INITIAL_files_childdirs':[37,1],'complete_source_INITIAL_bytes_modes_hidden_empty_before_after_exact':True,'retrieved_files':sorted(inventory,key=lambda r:r['path'])}
with (OWN/'PRIMARY_INVENTORY.json').open('x') as f:json.dump(result,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('retrieved_files','native_run','literal_transport_failures')}))
