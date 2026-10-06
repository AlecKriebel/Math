"""ROOT-held source/characteristic family authentication and asserted finite replay."""
from pathlib import Path
import datetime,gzip,hashlib,json,os,signal,subprocess
B=Path(__file__).resolve().parent; F=B/'scope_characteristic_adversary_01'; W=B/'root_scope01_reproduction'
W.mkdir(exist_ok=False); checks=[]
def ck(x,m):
    if not x:raise RuntimeError(m)
    checks.append(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=sha(b),mode=p.stat().st_mode&0o777)
def put(p,z):p.write_text(json.dumps(z,indent=2,sort_keys=True)+'\n')
inventory=F/'HELD_INVENTORY.json'; ib=inventory.read_bytes()
ck(sha(ib)=='8a7ce38c00137c6b5b746c4c5c8cb4491591447671513a78f3985e1f09df07cf','pinned held inventory')
z=json.loads(ib); domain=set()
for row in z['entries']:
    p=F/row['path'];b=p.read_bytes()
    ck(not p.is_symlink() and row['path'] not in domain,'unique held file:'+row['path']);domain.add(row['path'])
    ck(len(b)==row['bytes'] and sha(b)==row['sha256'] and oct(p.stat().st_mode&0o777)==row['mode'],'whole held body/mode:'+row['path'])
allfiles=[p for p in F.rglob('*') if p.is_file()]; names={str(p.relative_to(F)) for p in allfiles}
ck(len(domain)==164 and len(names)==168 and names==domain|set(z['closing_exclusions']),'exact164+4 held domain')
ck(sha((F/'FAMILY_REPORT.md').read_bytes())=='67a3fb36c41d665edba805d447313163452f30b3c548b8e802ff6514f620e24c','exact full report pin')
early=json.loads((F/'SOURCE_ONLY_INVENTORY.json').read_bytes())
ck(sha((F/'SOURCE_ONLY_INVENTORY.json').read_bytes())=='2c1ecd8c64acc9c228bedb4cf82cc41b889e9d400d090a9aa5a7cbb2e552acd7','independent source-first inventory pin')
ck(len(early['entries'])==36,'36 early source-only entries')
for row in early['entries']:
    p=F/row['path'];b=p.read_bytes()
    if row['path']=='RESEARCH_LOG.md':b=b[:row['bytes']]
    ck(len(b)==row['bytes'] and sha(b)==row['sha256'] and oct(p.stat().st_mode&0o777)==row['mode'],'actual early body/log prefix preserved:'+row['path'])
freeze=json.loads((F/'receipts/freeze-source.json').read_bytes());acquire=json.loads((F/'receipts/acquire-author.json').read_bytes())
ck(freeze['end_utc']=='2026-10-05T15:48:02Z' and freeze['end_utc']<acquire['start_utc'],'actual source freeze predates candidate acquisition')
receipts=[]
for p in sorted((F/'receipts').glob('*.json')):
    r=json.loads(p.read_bytes());ck(r['kind']=='actual-native-execution' and r['start_utc']<=r['end_utc'],'actual native receipt:'+p.stem)
    for stream in ('stdout','stderr'):
        v=p.with_suffix('.'+stream).read_bytes()
        ck(len(v)==r[stream+'_bytes'] and sha(v)==r[stream+'_sha256'],'full original stream:'+p.stem+':'+stream)
    expected=56 if p.stem in ('retrieve-chiarli-ams','retrieve-chiarli-primary-mirror') else 0
    ck(r['exit_code']==expected,'preserved original exit:'+p.stem)
    receipts.append(dict(name=p.stem,receipt=pin(p),exit_code=r['exit_code'],start_utc=r['start_utc'],end_utc=r['end_utc']))
ck(len(receipts)==34,'all34 original receipt streams')
original=json.loads((F/'receipts/check-geometric-families-v02.stdout').read_bytes())
source=F/'derivations/check_geometric_families.py'; body=source.read_bytes()
put(W/'request.json',dict(UTC=utc(),actual_recorder_PID=os.getpid(),argv=['/opt/homebrew/bin/python3','-E','-B',str(source)],cwd=str(B),timeout_seconds=60,source=pin(source),optimized_python=False,stdin_hex=''))
for label,p in [('program',source),('ROOT_verifier',Path(__file__).resolve()),('expected',F/'receipts/check-geometric-families-v02.stdout')]:
    (W/(label+'_PRELAUNCH.gz')).write_bytes(gzip.compress(p.read_bytes(),mtime=0))
child=None;out=err=b'';failure=None;reaped=False
try:
    child=subprocess.Popen(['/opt/homebrew/bin/python3','-E','-B',str(source)],cwd=B,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
    put(W/'started.json',dict(UTC=utc(),actual_recorder_PID=os.getpid(),actual_child_PID=child.pid))
    out,err=child.communicate(b'',timeout=60);reaped=child.poll() is not None
except BaseException as exc:
    failure=repr(exc)
    if child is not None:
        if child.poll() is None:
            try:os.killpg(child.pid,signal.SIGKILL)
            except ProcessLookupError:pass
        out,err=child.communicate(timeout=10);reaped=child.poll() is not None
finally:
    for label,v in [('stdout',out),('stderr',err)]: (W/(label+'.gz')).write_bytes(gzip.compress(v,mtime=0))
    execution=dict(UTC_end=utc(),actual_recorder_PID=os.getpid(),actual_child_PID=child.pid if child else None,exit_code=child.returncode if child else None,error=failure,parent_reaped=reaped,stdout=dict(bytes=len(out),sha256=sha(out)),stderr=dict(bytes=len(err),sha256=sha(err)))
    put(W/'execution.json',execution)
ck(failure is None and child.returncode==0 and reaped and not err,'ROOT assert-enabled geometric controls complete')
ck(json.loads(out)==original,'whole current geometric control JSON reproduced')
hold=json.loads((F/'receipts/hold-final.stdout').read_bytes())
ck(hold['inventory_sha256']==sha(ib) and hold['files_in_inventory']==164,'four closing exclusions tied to actual hold result')
for p in allfiles:p.chmod(0o444)
for p in sorted([F,*[q for q in F.rglob('*') if q.is_dir()]],key=lambda x:len(x.parts),reverse=True):p.chmod(0o555)
for p in W.iterdir():p.chmod(0o444)
W.chmod(0o555)
closed=[pin(p) for p in sorted(allfiles)]
result=dict(status='ROOT_ACCEPTS_PR293_SCOPE_AND_CHARACTERISTIC_FAMILY01',UTC=utc(),actual_ROOT_PID=os.getpid(),checks=checks,closed_files=closed,original_held_inventory=pin(inventory),original_native_receipts=receipts,ROOT_current_geometric_replay=execution,original_source_first_preserved=True,mathematical_semantic_reads=['FAMILY_REPORT.md','EVIDENCE_LIMITS.md','derivations/CHARACTERISTIC_FREE_CHAIN.md','derivations/GEOMETRIC_EDGE_FAMILIES.md','derivations/check_geometric_families.py'],qualifications=['Original native receipts do not record child PIDs or contemporaneous program-body pins; no such identities are invented. ROOT replay newly binds actual PID and exact current body with asserts enabled.','The historical first control body is disclosed as a current reconstruction, not a contemporaneously sealed input.','After source-only freeze a manifest exposed a favorable inherited status snippet, explicitly unused.','Original primary source mathematical reads are limited to the selected chapters/pages listed by the reviewer; no full Chiarli-Greco article was obtained.','Finite controls test explicit examples only. No formal proof or human peer review.'],priority_clearance=False,preprint_clearance=False,publication_authority=False)
path=B/'ROOT_SCOPE_CHARACTERISTIC_FAMILY01_ACCEPTANCE.json'
put(path,result);path.chmod(0o444)
print(json.dumps(dict(status=result['status'],ROOT_PID=os.getpid(),child_PID=child.pid,checks=len(checks),files=len(allfiles),bytes=sum(p.stat().st_size for p in allfiles),acceptance=pin(path))))
