"""ROOT authenticates exact closed surface-family evidence; no reviewer mutation."""
from pathlib import Path
import datetime,gzip,hashlib,json,os
B=Path(__file__).resolve().parent; F=B/'surface_adversary_01'; checks=[]
def ck(x,m):
    if not x:raise RuntimeError(m)
    checks.append(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=sha(b),mode=p.stat().st_mode&0o777)
def auth(z,exact_mode=False):
    p=Path(z['path']);b=p.read_bytes()
    ck(len(b)==z['bytes'] and sha(b)==z['sha256'],'complete pinned body:'+str(p))
    if exact_mode:ck((p.stat().st_mode&0o777)==z['mode'],'final immutable mode:'+str(p))
    return b
mb=(F/'MANIFEST.json').read_bytes();sb=(F/'FINAL_SEAL.json').read_bytes()
ck(sha(mb)=='61bd797097236e01d3c62239995638b848d2114f335b12550cdf44dead29bb22','closed manifest pin')
ck(sha(sb)=='3f0660e5021b1b69ca87b70b3ff5810c8b097c7e44ea9a0af44d7196bcce187d','closed seal pin')
m=json.loads(mb);s=json.loads(sb);seen=set()
for z in m['files']:
    p=Path(z['path']);rel=str(p.relative_to(F))
    ck(rel==z['relative_path'] and rel not in seen and not p.is_symlink(),'unique closed owned file:'+rel);seen.add(rel);auth(z,True)
domain={str(p.relative_to(F)) for p in F.rglob('*') if p.is_file()}
ck(domain==seen|{'MANIFEST.json','FINAL_SEAL.json'} and len(seen)==290 and len(domain)==292,'exact290+2 closure')
ck(sum(z['bytes'] for z in m['files'])==7126729,'exact complete payload byte total')
ck(all((p.stat().st_mode&0o777)==0o444 for p in F.rglob('*') if p.is_file()),'all292 final files444')
ck(all((p.stat().st_mode&0o777)==0o555 for p in [F,*[q for q in F.rglob('*') if q.is_dir()]]),'all final directories555')
for role in ('manifest','source','report','derivations','verdict','input_source_custody','read_scope'):auth(s[role],True)
scope=json.loads(auth(s['read_scope']));custody=json.loads(auth(s['input_source_custody']));verdict=json.loads(auth(s['verdict']))
ck(not s['priority_assessed'] and not s['human_peer_review'] and not s['full_line_theorem_certified'] and not s['Git_PR_service_mutations'],'exact scoped exclusions')
ck(sha((F/'INDEPENDENT_INITIAL_DERIVATION.md').read_bytes())=='1f649f16509b8fd963f3d3525f47ffc85148bf336694ddbbe8f02b0c0220c224','independent pre-author derivation')
ck(scope['initial_record']['precedes_author_proof'] and scope['initial_record']['precedes_prior_review'] and not scope['prior_reviewer_proof_semantically_read'],'independent early derivation and no prior proof convergence')
recursive_pins=0
def walk(z):
    global recursive_pins
    if isinstance(z,dict):
        if all(k in z for k in ('path','bytes','sha256')) and isinstance(z['path'],str) and z['path'].startswith('/'):
            auth(z);recursive_pins+=1
        for v in z.values():walk(v)
    elif isinstance(z,list):
        for v in z:walk(v)
walk(scope);walk(custody)
ck(len(custody['all_19_original_bodies_authenticated'])==19,'all19 submitted bodies source-bound')
for z in custody['all_19_original_bodies_authenticated']:
    b=auth(z['pin']);ck(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==z['computed_git_blob'],'full original Git blob:'+z['repository_path'])
native=[]
for C in sorted((F/'native').iterdir()):
    r=json.loads((C/'request.json').read_bytes());a=json.loads((C/'started.json').read_bytes());e=json.loads((C/'execution.json').read_bytes())
    ck(r['actual_recorder_PID']==a['actual_recorder_PID']==e['actual_recorder_PID'] and a['actual_child_PID']==e['actual_child_PID'],'native actual identities:'+C.name)
    ck(r['UTC']<=a['UTC']<=e['end_UTC'] and e['parent_reaped_child'] and not e['timed_out'] and e['exception'] is None,'native complete actual envelope:'+C.name)
    expected=23 if int(C.name.split('_')[0])<=8 else 0
    ck(e['exit_code']==expected,'original failed/successful execution preserved:'+C.name)
    for name in ('stdout','stderr'):auth(e[name])
    body=auth(r['recorder_source']);ck(body==gzip.decompress((C/'recorder_prelaunch.py.gz').read_bytes()),'exact recorder prelaunch:'+C.name)
    for row in r.get('child_sources',[]):
        body=auth(row['source']);ck(body==gzip.decompress(auth(row['prelaunch'])),'exact child prelaunch:'+C.name)
    native.append(dict(name=C.name,actual_child_PID=e['actual_child_PID'],actual_recorder_PID=e['actual_recorder_PID'],exit_code=e['exit_code'],execution=pin(C/'execution.json')))
ck(len(native)==33 and sum(z['exit_code']!=0 for z in native)==8,'all33 complete envelopes/eight preserved download failures')
result=dict(status='ROOT_ACCEPTS_PR293_SURFACE_FAMILY01_EXACT_LEMMAS_A_B',UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual_ROOT_PID=os.getpid(),manifest=pin(F/'MANIFEST.json'),seal=pin(F/'FINAL_SEAL.json'),report=pin(F/'REPORT.md'),derivations=pin(F/'DERIVATIONS.md'),checks=checks,recursive_custody_pins=recursive_pins,native_captures=native,mathematical_scope='Smooth-surface adjoint nonvanishing and integral-hypersurface conductor adjoint in every algebraically closed characteristic.',ROOT_semantic_read='Full final REPORT and DERIVATIONS; pg-conditioned Picard smoothness, positive-square Hodge/genus argument, integral Cartier pullback, resolution canonical inclusion, finite CM duality and singular-curve conductor vanishing independently checked.',qualification='Standard algebraic theorem dependencies are explicit. Full source byte custody does not assert semantic reading of every source PDF page; no finite computation establishes the universal lemmas. This family alone does not certify C1-C4, novelty, formal proof, human peer review or a preprint.',priority_clearance=False,publication_authority=False)
path=B/'ROOT_SURFACE_FAMILY01_ACCEPTANCE.json'
with path.open('x') as f:json.dump(result,f,indent=2,sort_keys=True);f.write('\n')
path.chmod(0o444)
print(json.dumps(dict(status=result['status'],ROOT_PID=os.getpid(),checks=len(checks),acceptance=pin(path))))
