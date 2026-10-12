"""Authenticate the closed conditional family and independently replay its finite controls.
Only writes ROOT-owned evidence under this PR293 effort. No Git or service writes.
"""
from pathlib import Path
import datetime, gzip, hashlib, json, os, signal, subprocess

B = Path(__file__).resolve().parent
F = B / 'algebra_adversary_01'
W = B / 'root_algebra01_reproduction'
W.mkdir(exist_ok=False)
checks = []
def ck(ok, label):
    if not ok: raise RuntimeError(label)
    checks.append(label)
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def pin(p):
    b = p.read_bytes()
    return dict(path=str(p), bytes=len(b), sha256=sha(b), mode=p.stat().st_mode & 0o777)
def put(p, x): p.write_text(json.dumps(x, indent=2, sort_keys=True) + '\n')
def authenticate(z, exact_mode=True):
    p=Path(z['path']); b=p.read_bytes()
    ck(len(b)==z['bytes'] and sha(b)==z['sha256'], 'body:'+str(p))
    if exact_mode: ck((p.stat().st_mode & 0o777)==z['mode'], 'mode:'+str(p))
    return b

manifest_body=(F/'MANIFEST.json').read_bytes()
ck(sha(manifest_body)=='59d4bc3b793dbd39d6694ff07c5a81a95901080c11f796a37eba024fcb50dec4','closed manifest pin')
seal_body=(F/'FINAL_SEAL.json').read_bytes()
ck(sha(seal_body)=='1f37605f4cb48a4846f8cdb83e7fbc352116514eb7a4064c1f9027bc104ff685','closed seal pin')
m=json.loads(manifest_body); seal=json.loads(seal_body)
seen=set()
for z in m['files']:
    p=Path(z['path']); rel=str(p.relative_to(F))
    ck(rel==z['relative'] and rel not in seen and not p.is_symlink(),'manifest unique owned path:'+rel)
    seen.add(rel); authenticate(z)
files={str(p.relative_to(F)) for p in F.rglob('*') if p.is_file()}
ck(files==seen|{'MANIFEST.json','FINAL_SEAL.json'},'exact closed file domain')
ck(len(files)==59 and sum(p.stat().st_size for p in F.rglob('*') if p.is_file())==338485,'exact closed files and bytes')
ck(all(not p.is_symlink() for p in F.rglob('*')),'no closed symlinks')
ck(all((p.stat().st_mode & 0o777)==0o444 for p in F.rglob('*') if p.is_file()),'all closed files read-only')
ck(all((p.stat().st_mode & 0o777)==0o555 for p in [F,*[x for x in F.rglob('*') if x.is_dir()]]),'all closed directories read-only')
for role in ('manifest','report','derivations','read_scope','verdict'): authenticate(seal[role])
scope=json.loads((F/'READ_SCOPE.json').read_bytes()); verdict=json.loads((F/'VERDICT.json').read_bytes())
ck(verdict['status']=='PASS_CONDITIONAL_ALGEBRA_REDUCTION' and not verdict['unconditional_original_problem_resolution_cleared'] and not verdict['inherited_surface_adjoint_verified_by_this_family'],'conditional verdict only')
ck(not verdict['priority_audit_done'] and not verdict['publication_authority'] and not verdict['human_peer_review'],'no broader clearance')
ck(sha((F/'DERIVATIONS_PREAUTHOR.md').read_bytes())=='72bbbe129e9dd0a829d42a11ca3fd7ee995ede643b4a9d87c76f36123b0b31db','pre-author independent derivation pin')
native=[]
for C in sorted((F/'native').iterdir()):
    r=json.loads((C/'request.json').read_bytes()); s=json.loads((C/'started.json').read_bytes()); e=json.loads((C/'execution.json').read_bytes())
    ck(e['exit_code']==0 and e['error'] is None and e['parent_reaped'],'actual native completion:'+C.name)
    ck(e['actual_child_PID']==s['actual_child_PID'] and e['actual_recorder_PID']==s['actual_recorder_PID']==r['actual_recorder_PID'],'actual native identities:'+C.name)
    ck(r['UTC']<=s['UTC']<=e['UTC_end'],'actual native time order:'+C.name)
    streams={}
    for k in ('stdout','stderr'):
        v=gzip.decompress((C/(k+'.gz')).read_bytes()); streams[k]=v
        ck(len(v)==e[k]['bytes'] and sha(v)==e[k]['sha256'],'whole native stream:'+C.name+':'+k)
    ck(streams['stderr']==b'','native stderr empty:'+C.name)
    for k,z in r['sources'].items():
        v=authenticate(z,exact_mode=False)
        ck(v==gzip.decompress((C/(k+'_PRELAUNCH.gz')).read_bytes()),'exact pre-launch source:'+C.name+':'+k)
    if C.name!='primary_pdf_text': json.loads(streams['stdout'])
    native.append(dict(name=C.name, request=pin(C/'request.json'), execution=pin(C/'execution.json'), PID=e['actual_child_PID']))
ck(len(native)==6,'six genuine complete native captures')
expected=json.loads(gzip.decompress((F/'native/independent_GF2/stdout.gz').read_bytes()))
ck(expected==scope['independent_controls'],'whole independent JSON read-scope match')
ck(expected['explicit_checks']==60182 and expected['union_count']==7175 and expected['plane_multiset_count']==15488,'bounded independent domain')
source=F/'independent_GF2.py'; body=source.read_bytes()
ck(sha(body)=='765b6ea2f903f2bad14d75851a8f1d1d6e3d602d3a20b3caca03cc1ee4d9c41f','safe fully-read independent source')
argv=['/opt/homebrew/bin/python3','-E','-B',str(source)]
for n,p in [('program',source),('ROOT_verifier',Path(__file__).resolve()),('expected',F/'native/independent_GF2/stdout.gz')]:
    (W/(n+'_PRELAUNCH.gz')).write_bytes(gzip.compress(p.read_bytes(),mtime=0))
request=dict(UTC=utc(),actual_recorder_PID=os.getpid(),argv=argv,cwd=str(B),stdin_hex='',timeout_seconds=60,source=pin(source),optimized_python=False)
put(W/'request.json',request)
child=None; out=b''; err=b''; failure=None; reaped=False
try:
    child=subprocess.Popen(argv,cwd=B,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
    put(W/'started.json',dict(UTC=utc(),actual_recorder_PID=os.getpid(),actual_child_PID=child.pid))
    out,err=child.communicate(b'',timeout=60); reaped=child.poll() is not None
except BaseException as exc:
    failure=repr(exc)
    if child is not None:
        if child.poll() is None:
            try: os.killpg(child.pid,signal.SIGKILL)
            except ProcessLookupError: pass
        out,err=child.communicate(timeout=10); reaped=child.poll() is not None
finally:
    for n,v in [('stdout',out),('stderr',err)]: (W/(n+'.gz')).write_bytes(gzip.compress(v,mtime=0))
    execution=dict(UTC_end=utc(),actual_recorder_PID=os.getpid(),actual_child_PID=child.pid if child else None,exit_code=child.returncode if child else None,error=failure,parent_reaped=reaped,stdout=dict(bytes=len(out),sha256=sha(out)),stderr=dict(bytes=len(err),sha256=sha(err)))
    put(W/'execution.json',execution)
ck(failure is None and reaped and child.returncode==0 and err==b'','ROOT actual independent control completion')
actual=json.loads(out)
ck(actual['actual_PID']==child.pid,'ROOT JSON genuine child PID')
exp_sem={k:v for k,v in expected.items() if k not in ('actual_PID','UTC')}
act_sem={k:v for k,v in actual.items() if k not in ('actual_PID','UTC')}
ck(exp_sem==act_sem,'whole semantic bounded control JSON exactly reproduced')
for p in W.rglob('*'):
    if p.is_file(): p.chmod(0o444)
W.chmod(0o555)
result=dict(status='ROOT_ACCEPTS_CONDITIONAL_PR293_ALGEBRA_FAMILY',UTC=utc(),actual_ROOT_PID=os.getpid(),review_files=59,review_bytes=338485,checks=checks,native_captures=native,manifest=pin(F/'MANIFEST.json'),seal=pin(F/'FINAL_SEAL.json'),ROOT_replay=execution,complete_semantic_JSON_reproduced=True,explicit_checks=60182,qualification='C1-C4 independently checked and finite controls reproduced; conditional on Lemma B. No universal geometric certification from finite computation, novelty clearance, human peer review, or publication authority.',mathematical_read='ROOT fully read REPORT.md, DERIVATIONS.md, independent_GF2.py and recorder/reproduction source; manifest/native binding checks cover complete read-scope records.',inherited_surface_obligation_open_for_this_family=True)
put(B/'ROOT_ALGEBRA_FAMILY01_ACCEPTANCE.json',result)
(B/'ROOT_ALGEBRA_FAMILY01_ACCEPTANCE.json').chmod(0o444)
print(json.dumps(dict(status=result['status'],root_PID=os.getpid(),child_PID=child.pid,checks=len(checks),acceptance=pin(B/'ROOT_ALGEBRA_FAMILY01_ACCEPTANCE.json'))))
