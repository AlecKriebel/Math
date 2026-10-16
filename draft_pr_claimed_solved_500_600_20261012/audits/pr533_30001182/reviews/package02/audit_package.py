#!/usr/bin/env python3
"""Independent sealed inventory, replay and failure-injection audit."""
import datetime,hashlib,json,os,shutil,subprocess,sys,zipfile
from pathlib import Path,PurePosixPath
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent.parent
PUB=AUDIT/'publication'
SCRATCH=HERE/'scratch'
def digest(data):return hashlib.sha256(data).hexdigest()
def inventory(base):
    return {p.relative_to(base).as_posix():{'bytes':p.stat().st_size,'sha256':digest(p.read_bytes())} for p in base.rglob('*') if p.is_file()}
def write(name,obj):
    (HERE/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
original_publication=inventory(PUB)
z=zipfile.ZipFile(PUB/'verification_package.zip');names=z.namelist()
assert len(names)==60 and len(set(names))==60
prefix='ambient_independence_verification/'
assert all(n.startswith(prefix) and not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts for n in names)
assert all(n.endswith(('.md','.json','.py','.txt','.tex')) or n.endswith('/.gitignore') for n in names)
sealed={n[len(prefix):]:z.read(n) for n in names};manifest=json.loads(sealed['MANIFEST.json'])
assert len(manifest['files'])==59 and set(manifest['files'])|{'MANIFEST.json'}==set(sealed)
for n,item in manifest['files'].items():assert item=={'bytes':len(sealed[n]),'sha256':digest(sealed[n])}
assert json.loads((PUB/'PACKAGE_MANIFEST.json').read_text())==manifest
assert json.loads(sealed['metadata.json'])==json.loads((PUB/'zenodo-deposit.json').read_text())
for name in ['README.md','requirements.txt','run_all.py','CORRECTIONS.md','BUILD.json','PDF_QA.json','ambient_independence.tex']:assert sealed[name]==(PUB/name).read_bytes()
for n,data in sealed.items():
    if n.startswith('original/'):
        src=AUDIT/'original/unsolved_math_prioritization/attempts/30001182'/n[len('original/'):]
    elif n.startswith(('reviews/','root_reproduction/')):src=AUDIT/n
    elif n=='SOURCE_DOWNLOADS.json':src=AUDIT/'root_sources/SOURCES.json'
    else:continue
    assert data==src.read_bytes(),n
nested=[]
for seal in ['original/public/FROZEN_MANIFEST.json','original/audit/AUDIT_MANIFEST.json']+[f'reviews/{f}/MANIFEST.json' for f in ['operator01','extension01','source01']]:
    records=json.loads(sealed[seal])['files'];base=PurePosixPath(seal).parent
    for r in records:
        p=PurePosixPath(r['path']);assert not p.is_absolute() and '..' not in p.parts
        n=(base/p).as_posix();assert n in sealed
        assert len(sealed[n])==r.get('bytes',r.get('size')) and digest(sealed[n])==r['sha256']
        nested.append({'seal':seal,'path':n})
assert len(nested)==35
write('CONCORDANCE.json',{'status':'PASS','zip_members':60,'outer_payloads':59,'nested_records':35,'all_repository_payloads_byte_equal':True,'metadata_exact':True,'nested_checks':nested,'public_package_builder':json.loads((PUB/'PACKAGE_BUILD.json').read_text())})

env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONOPTIMIZE',None)
env.update(HTTP_PROXY='http://127.0.0.1:9',HTTPS_PROXY='http://127.0.0.1:9',ALL_PROXY='http://127.0.0.1:9',NO_PROXY='')
def run(base,args=(),extra=None):
    e=dict(env);e.update(extra or {})
    return subprocess.run([sys.executable,*args,str(base/'run_all.py')],cwd=base,env=e,capture_output=True,text=True)
replays=[]
for tag in ['recorded_replay01','recorded_replay02']:
    container=SCRATCH/tag
    if container.exists():shutil.rmtree(container)
    z.extractall(container);base=container/'ambient_independence_verification';before=inventory(base)
    p=run(base);after=inventory(base);assert p.returncode==0 and before==after
    lines=[json.loads(l) for l in p.stdout.splitlines()];assert lines[-1]['manifest_files_verified']==59 and lines[-1]['nested_manifest_files_verified']==35
    (HERE/(tag+'.stdout.jsonl')).write_text(p.stdout)
    replays.append({'run':tag,'returncode':p.returncode,'stderr':p.stderr,'before':before,'after_equals_before':after==before,'stdout_sha256':digest(p.stdout.encode()),'jobs':lines})
assert replays[0]['stdout_sha256']==replays[1]['stdout_sha256']
write('REPLAY_RECEIPT.json',{'status':'PASS','repeated_pristine_outputs_equal':True,'blocked_proxy_environment':True,'network_enforcement_limit':'Proxy blackhole and static standard-library code audit; no OS-level network namespace was available or claimed. Runner uses no network code.','runs':replays})

mutations=[]
def case(tag,mutate,args=(),extra=None,expected=''):
    container=SCRATCH/'mutations'/tag
    if container.exists():shutil.rmtree(container)
    z.extractall(container);base=container/'ambient_independence_verification';mutate(base)
    p=run(base,args,extra);assert p.returncode!=0 and expected in p.stderr,(tag,p.returncode,p.stderr)
    mutations.append({'case':tag,'returncode':p.returncode,'expected_error':expected,'stderr':p.stderr,'stdout':p.stdout,'rejected':True})
def refresh(base,name):
    p=base/name;data=p.read_bytes();m=json.loads((base/'MANIFEST.json').read_text());m['files'][name]={'bytes':len(data),'sha256':digest(data)};(base/'MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
def update_json(base,name,fn,refresh_outer=False):
    p=base/name;o=json.loads(p.read_text());fn(o);p.write_text(json.dumps(o,indent=2)+'\n')
    if refresh_outer:refresh(base,name)
case('missing_payload',lambda b:(b/'ambient_independence.tex').unlink(),expected='Inventory mismatch')
case('changed_payload',lambda b:(b/'ambient_independence.tex').write_bytes((b/'ambient_independence.tex').read_bytes()+b'\n% altered\n'),expected='Integrity mismatch')
case('extra_payload',lambda b:(b/'unsealed_note.md').write_text('extra'),expected='Inventory mismatch')
case('missing_dotignore',lambda b:(b/'reviews/source01/.gitignore').unlink(),expected='Inventory mismatch')
case('optimized_flag',lambda b:None,args=('-O',),expected='Run without Python optimization')
case('optimized_environment',lambda b:None,extra={'PYTHONOPTIMIZE':'1'},expected='Run without Python optimization')
case('outer_parent_path',lambda b:update_json(b,'MANIFEST.json',lambda m:m['files'].__setitem__('../outside',{'bytes':0,'sha256':'0'*64})),expected='Invalid manifest path')
case('outer_absolute_path',lambda b:update_json(b,'MANIFEST.json',lambda m:m['files'].__setitem__('/outside',{'bytes':0,'sha256':'0'*64})),expected='Invalid manifest path')
case('nested_inconsistent_hash',lambda b:update_json(b,'reviews/source01/MANIFEST.json',lambda m:m['files'][0].__setitem__('sha256','0'*64),True),expected='Nested manifest mismatch')
case('nested_parent_path',lambda b:update_json(b,'reviews/source01/MANIFEST.json',lambda m:m['files'][0].__setitem__('path','../outside'),True),expected='Invalid nested path')
case('nested_absolute_path',lambda b:update_json(b,'reviews/source01/MANIFEST.json',lambda m:m['files'][0].__setitem__('path','/outside'),True),expected='Invalid nested path')
case('replay_mismatch_after_outer_reseal',lambda b:update_json(b,'root_reproduction/weighted_family_results.json',lambda m:m.__setitem__('status','MUTATED'),True),expected='Replay mismatch')
case('symlink',lambda b:(b/'extra_link').symlink_to(b/'README.md'),expected='Unexpected symlink')
write('MUTATION_RESULTS.json',{'status':'PASS','rejected_cases':len(mutations),'cases':mutations,'limits':'Integrity/replay attacks in isolated copies; manifest consistency is not authenticity.'})

producer=SCRATCH/'producer'
if producer.exists():shutil.rmtree(producer)
producer.mkdir()
shutil.copytree(PUB,producer/'publication')
shutil.copytree(AUDIT/'original',producer/'original')
for family in ['operator01','extension01','source01']:
    source=AUDIT/'reviews'/family;target=producer/'reviews'/family;target.mkdir(parents=True)
    for p in source.iterdir():
        if p.is_file():shutil.copy2(p,target/p.name)
shutil.copytree(AUDIT/'root_reproduction',producer/'root_reproduction')
(producer/'root_sources').mkdir();shutil.copy2(AUDIT/'root_sources/SOURCES.json',producer/'root_sources/SOURCES.json')
p=subprocess.run([sys.executable,str(producer/'publication/make_package.py')],cwd=producer/'publication',capture_output=True,text=True)
assert p.returncode==0,p.stderr
new=(producer/'publication/verification_package.zip').read_bytes();assert new==(PUB/'verification_package.zip').read_bytes()
checks=[]
for tag,alter in [('omitted_sealed_dotignore',lambda b:(b/'reviews/source01/.gitignore').unlink()),('inconsistent_sealed_certificate',lambda b:(b/'reviews/source01/CERTIFICATES.md').write_text('changed'))]:
    branch=SCRATCH/'producer_mutations'/tag
    if branch.exists():shutil.rmtree(branch)
    shutil.copytree(producer,branch);alter(branch)
    x=subprocess.run([sys.executable,str(branch/'publication/make_package.py')],cwd=branch/'publication',capture_output=True,text=True)
    assert x.returncode!=0 and 'Nested sealed payload' in x.stderr
    checks.append({'case':tag,'returncode':x.returncode,'stderr':x.stderr,'rejected':True})
write('PRODUCER_RECEIPT.json',{'status':'PASS','byte_identical_zip':True,'rebuilt_zip_sha256':digest(new),'stdout':p.stdout,'stderr':p.stderr,'failure_controls':checks})
assert inventory(PUB)==original_publication
write('PUBLICATION_UNCHANGED.json',{'status':'PASS','checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'publication_before':original_publication,'publication_after_equals_before':True})
print(json.dumps({'status':'PASS','outer_payloads':59,'nested_entries':35,'pristine_replays':2,'runner_failures_rejected':len(mutations),'producer_failures_rejected':len(checks),'byte_identical_producer':True,'publication_unchanged':True},indent=2))
