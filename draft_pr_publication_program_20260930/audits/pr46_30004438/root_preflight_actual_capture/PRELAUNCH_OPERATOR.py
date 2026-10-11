"""ROOT-only PR46 V2 phase operator. Prepared source only; ROOT must read and copy unchanged adjacent to A46 before actual use."""
from pathlib import Path,PurePosixPath
import argparse,datetime as dt,hashlib,json,math,os,re,stat,subprocess,sys,traceback
A=Path(__file__).resolve().parent;R=A.parents[2];H=A/'acceptance_preparation_family_v2'
PREP_SHA='f44ccf65fa4397736305881de926eafcf211c33ef9e6fec5e5596c99d252ef40'
SEALER_OPERATOR_SHA='ded1b43627fb695cf5ca2f279647a4b0bbafec79d4bf5aa91b363ed5029d291e'
def need(v,m):
    if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def raw(p):need(p.is_file() and not p.is_symlink() and all(not x.is_symlink() for x in p.parents),'Regular nonsymlink source');return p.read_bytes()
def parse(b):
    def pairs(items):
        o={}
        for k,v in items:need(k not in o,'Duplicate JSON key');o[k]=v
        return o
    def fl(s):v=float(s);need(math.isfinite(v),'Nonfinite JSON');return v
    return json.loads(b,object_pairs_hook=pairs,parse_float=fl,parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)))
def load(p):return parse(raw(p))
def ref(p):b=raw(p);return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b)}
def eq(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return a.keys()==b.keys() and all(eq(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(eq(x,y) for x,y in zip(a,b))
    return a==b
def clock(s):
    need(type(s) is str and s and s==s.strip(),'Literal aware UTC');v=dt.datetime.fromisoformat(s[:-1]+'+00:00' if s.endswith('Z') else s);need(v.tzinfo is not None and v.utcoffset()==dt.timedelta(0),'Aware UTC required');return v
def stamp():return dt.datetime.now(dt.timezone.utc).isoformat()
def put(p,b):
    need(not p.is_symlink() and all(not x.is_symlink() for x in p.parents),'Regular output ancestors')
    with p.open('xb') as h:h.write(b);h.flush();os.fsync(h.fileno())
def member(base,z):
    need(type(z) is dict and set(z)=={'path','bytes','sha256'} and type(z['path']) is str,'Exact member row');n=z['path'];p=PurePosixPath(n);need(n and p.as_posix()==n and not p.is_absolute() and n!='.' and not {'.','..','.git','__pycache__'}.intersection(p.parts) and '\\' not in n and '\0' not in n,'Canonical literal member');b=raw(base/n);need(type(z['bytes']) is int and z['bytes']>=0 and len(b)==z['bytes'] and type(z['sha256']) is str and re.fullmatch('[0-9a-f]{64}',z['sha256']) and sha(b)==z['sha256'],'Complete exact member body');return b
def main():
    need(__debug__ and os.environ.get('PYTHONOPTIMIZE','') in ('','0'),'No optimized guards')
    need(A.name=='pr46_30004438' and H.is_dir() and not H.is_symlink(),'ROOT must copy exact reviewed wrapper adjacent to A46; preparation path is not executable authority')
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['preflight','overlay','prepush','finalize','mirror','post']);p.add_argument('--merge-queue-preimage-sha256');a=p.parse_args()
    need((a.merge_queue_preimage_sha256 is None) if a.phase!='overlay' else (type(a.merge_queue_preimage_sha256) is str and re.fullmatch('[0-9a-f]{64}',a.merge_queue_preimage_sha256)),'Only overlay requires the exact actual merge-queue SHA')
    b=raw(H/'PREPARATION_MANIFEST.json');need(sha(b)==PREP_SHA and stat.S_IMODE((H/'PREPARATION_MANIFEST.json').stat().st_mode)==0o444,'Exact actually closed46V2 source manifest');prep=parse(b);need(prep['schema']=='pr46-acceptance-source-closure/v1' and prep['status']=='CLOSED_SOURCE_ONLY' and prep['source_only'] is True and prep['self_excluded']==['PREPARATION_MANIFEST.json'] and type(prep['files_count']) is int and prep['files_count']==len(prep['files'])==109,'Actual closed46V2 source, not rejectedV1')
    pins={z['path']:z for z in prep['files']};need(len(pins)==109,'Unique closed source rows')
    cdir=A/'root_final_reconciliation_actual_capture';need({x.name for x in cdir.iterdir()}=={'CAPTURE.json','PRELAUNCH_SOURCE.py','PRELAUNCH_OPERATOR.py','stdout.bin','stderr.bin'},'Complete genuine final-sealer capture');c=load(cdir/'CAPTURE.json')
    need(c['schema']=='ROOT_actual_audit_administrative_capture_v1' and c['actual_execution'] is True and c['completed'] is True and type(c['exit_code']) is int and c['exit_code']==0 and c['status']=='PASS' and type(c['pid']) is int and c['pid']>0 and c['stdin_supplied'] is False and c['cwd']==str(A),'Literal inspected completed sealer capture/PID, no hardcoded invented PID')
    need(eq(c['native13_before'],c['native13_after']) and c['main_head_before']==c['main_head_after'],'Sealer native13/main preserved')
    need(c['source_unchanged'] is True and sha(raw(cdir/'PRELAUNCH_SOURCE.py'))==sha(member(H,pins['seal_final_evidence.py']))==c['source_sha256'],'Entire exact closed sealer source')
    need(type(c['argv']) is list and c['argv'][:3]==['/usr/bin/python3','-B',str(H/'seal_final_evidence.py')],'Literal actual sealer argv')
    need(sha(raw(cdir/'PRELAUNCH_OPERATOR.py'))==sha(raw(A/'capture_root_final_operation.py'))==sha(member(H,pins['capture_root_final_operation.py']))==SEALER_OPERATOR_SHA,'Actual copied ROOT sealer operator equals reviewed closed46V2 body')
    for k in ['stdout','stderr']:need(c[k]['path']==k+'.bin','Literal final stream names');member(cdir,c[k])
    need(raw(cdir/'stderr.bin')==b'','Whole successful final-sealer stderr')
    plan=load(A/'ROOT_FINAL_PLAN.json');final=A/'final_review';receipt=load(final/'ROOT_FINAL_RECONCILIATION.json');mf=load(final/'FINAL_MANIFEST.json')
    need(eq(plan,receipt['entire_scope']) and eq(plan,load(final/'ROOT_REVIEWED_SCOPE.json')) and eq(receipt['bindings_before'],receipt['bindings_after']),'Complete final plan/scope/evidence identity')
    need(receipt['schema']=='pr46-actual-final-reconciliation/v1' and receipt['status']=='PASS' and type(receipt['pr']) is int and receipt['pr']==46 and type(receipt['problem_id']) is int and receipt['problem_id']==30004438 and receipt['preparation_manifest_sha256']==PREP_SHA and receipt['actual_root_reconciliation'] is True and receipt['science_helpers_executed'] is False and receipt['shared_mutations'] is False,'Actual exact46 final receipt')
    need(clock(c['started_utc'])<=clock(receipt['utc'])<=clock(c['finished_utc'])<=dt.datetime.now(dt.timezone.utc),'Actual completed sealer aware UTC')
    need(mf['schema']=='pr46-final-root-two-member-closure/v1' and mf['self_excluded']==['FINAL_MANIFEST.json'] and type(mf['files_count']) is int and mf['files_count']==len(mf['files'])==2 and {z['path'] for z in mf['files']}=={'ROOT_FINAL_RECONCILIATION.json','ROOT_REVIEWED_SCOPE.json'} and {x.name for x in final.iterdir()}=={'ROOT_FINAL_RECONCILIATION.json','ROOT_REVIEWED_SCOPE.json','FINAL_MANIFEST.json'},'Exact final2+self topology')
    for z in mf['files']:member(final,z);need(stat.S_IMODE((final/z['path']).stat().st_mode)==0o444,'Full frozen final member mode')
    need(stat.S_IMODE((final/'FINAL_MANIFEST.json').stat().st_mode)==0o444,'Full frozen literal final self')
    stdout=load(cdir/'stdout.bin');need(stdout['status']=='PASS' and stdout['science_helpers_executed'] is False and stdout['shared_mutations'] is False and stdout['final_receipt_sha256']==sha(raw(final/'ROOT_FINAL_RECONCILIATION.json')) and stdout['final_manifest_sha256']==sha(raw(final/'FINAL_MANIFEST.json')),'Entire completed sealer stdout receipt pins')
    name={'mirror':'state_mirror_reconciliation.py','post':'verify_post_acceptance.py'}.get(a.phase,'integrate_reviewed_partial.py');script=H/name;body=member(H,pins[name]);need(stat.S_IMODE(script.stat().st_mode)==0o444,'Frozen reviewed selected phase source')
    previous=parse(member(H,pins['INPUT_BINDINGS.json']))
    refs={'final-plan':A/'ROOT_FINAL_PLAN.json','final-receipt':final/'ROOT_FINAL_RECONCILIATION.json','final-manifest':final/'FINAL_MANIFEST.json','reconciliation-capture':cdir/'CAPTURE.json','previous-mirror':R/previous['previous_mirror']['path'],'previous-post':R/previous['previous_post']['path'],'fresh-preimage':A/'ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES.json','root-bindings':A/'ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS.json'}
    for k,n in [('previous-mirror','previous_mirror'),('previous-post','previous_post')]:need(eq(ref(refs[k]),previous[n]),'Exact actual previous45 full reference')
    argv=['/usr/bin/python3','-B',str(script),'--execute','--preparation-manifest-sha256',PREP_SHA]
    for flag,q in refs.items():z=ref(q);argv.extend(['--'+flag,z['path'],'--'+flag+'-sha256',z['sha256']])
    if a.phase not in ['mirror','post']:argv.append(a.phase)
    if a.phase=='overlay':argv.extend(['--merge-queue-preimage-sha256',a.merge_queue_preimage_sha256])
    dest=A/('root_'+a.phase+'_actual_capture');dest.mkdir(exist_ok=False)
    operator=raw(Path(__file__));put(dest/'PRELAUNCH_SOURCE.py',body);put(dest/'PRELAUNCH_OPERATOR.py',operator)
    pre={'schema':'ROOT_reviewed_acceptance_phase_prelaunch_v1','phase':a.phase,'argv':argv,'cwd':str(R),'operator_pid':os.getpid(),'operator_sha256':sha(operator),'source_sha256':sha(body),'prepared_utc':stamp(),'stdin_supplied':False};put(dest/'PRELAUNCH.json',(json.dumps(pre,indent=2)+'\n').encode())
    rec={**pre,'schema':'ROOT_actual_reviewed_acceptance_phase_capture_v1','started_utc':stamp(),'actual_execution':False,'completed':False,'pid':None,'exit_code':None};out=err=b''
    try:
        child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE);rec.update(actual_execution=True,pid=child.pid);out,err=child.communicate();rec.update(completed=True,exit_code=child.returncode)
    except BaseException:rec['operator_error']=traceback.format_exc()
    rec.update(finished_utc=stamp(),source_unchanged=raw(script)==body,operator_unchanged=raw(Path(__file__))==operator)
    for k,b in [('stdout',out),('stderr',err)]:put(dest/(k+'.bin'),b);rec[k]={'path':k+'.bin','bytes':len(b),'sha256':sha(b)}
    rec['status']='PASS' if rec['completed'] is True and type(rec['exit_code']) is int and rec['exit_code']==0 and rec['source_unchanged'] is True and rec['operator_unchanged'] is True and err==b'' and 'operator_error' not in rec else 'FAIL';put(dest/'CAPTURE.json',(json.dumps(rec,indent=2)+'\n').encode());print(json.dumps(rec,indent=2));return 0 if rec['status']=='PASS' else 1
if __name__=='__main__':sys.exit(main())
