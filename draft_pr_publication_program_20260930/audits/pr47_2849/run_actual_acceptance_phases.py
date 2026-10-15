"""UNEXECUTED PR47 ROOT phase operator SOURCE. ROOT reads and copies unchanged adjacent to A47 before use.
Restricted authority: exact current native13/owned mutable logs0644, child-process umask0022.
No general arbitrary-mode preservation claim; permission checks are read-only.
"""
from pathlib import Path,PurePosixPath
import argparse,datetime as dt,hashlib,json,math,os,re,stat,subprocess,sys,traceback
A=Path(__file__).absolute().parent;R=A.parents[2];H=A/'acceptance_preparation_family';P46=A.parent/'pr46_30004438'
PREP_SHA='1a10442d9962db99c608412f53fef754870bfadf24fd76e7e899112fc38ebef1'
SEALER_OPERATOR_SHA='43717798bf50352960238bdb66ef553f4249ee28e231b2188c112e890e42dba8'
NATIVE13=['draft_pr_publication_program_20260930/inventory.json',*[('unsolved_math_prioritization/'+n) for n in ['QUEUE.md','state.json','history.jsonl','catalog.json','assessments.json','queue.py','policy.json','manifest.json','cache/problems.json','cache/research_results.json','cache/catalog.sqlite','review_v2/related_target_groups.json']]]
OWNED_LOGS=['draft_pr_publication_program_20260930/RESEARCH_LOG.md','draft_pr_publication_program_20260930/audits/pr47_2849/ROOT_RESEARCH_LOG.md']
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
def eq(a,b):return type(a) is type(b) and (a.keys()==b.keys() and all(eq(a[k],b[k]) for k in a) if type(a) is dict else len(a)==len(b) and all(eq(x,y) for x,y in zip(a,b)) if type(a) is list else a==b)
def safe(n):
    need(type(n) is str and n and n!='.' and '\\' not in n and '\0' not in n,'Literal canonical path');p=PurePosixPath(n);need(p.as_posix()==n and not p.is_absolute() and not {'.','..','.git','__pycache__'}.intersection(p.parts),'Canonical relative member');return n
def ref(p):b=raw(p);return dict(path=safe(p.relative_to(R).as_posix()),bytes=len(b),sha256=sha(b))
def member(base,z):
    need(type(z) is dict and set(z)=={'path','bytes','sha256'} and type(z['bytes']) is int and z['bytes']>=0 and type(z['sha256']) is str and re.fullmatch('[0-9a-f]{64}',z['sha256']),'Strict typed member3');b=raw(base/safe(z['path']));need(len(b)==z['bytes'] and sha(b)==z['sha256'],'Entire exact member body');return b
def clock(s):need(type(s) is str and s and s==s.strip(),'Literal UTC');v=dt.datetime.fromisoformat(s[:-1]+'+00:00' if s.endswith('Z') else s);need(v.tzinfo is not None and v.utcoffset()==dt.timedelta(0),'Aware UTC required');return v
def stamp():return dt.datetime.now(dt.timezone.utc).isoformat()
def put(p,b):
    need(not p.is_symlink() and all(not x.is_symlink() for x in p.parents),'Regular output ancestors')
    with p.open('xb') as h:h.write(b);h.flush();os.fsync(h.fileno())
    need(stat.S_IMODE(p.stat().st_mode)==0o644,'New operational capture member full0644 under0022')
def permissions(fresh):
    need(type(fresh['files']) is list and len(fresh['files'])==13 and len({z['path'] for z in fresh['files']})==13 and {z['path'] for z in fresh['files']}==set(NATIVE13),'Exactly fresh native13 literal identities')
    native=[];logs=[]
    for z in sorted(fresh['files'],key=lambda z:z['path']):
        p=R/safe(z['path']);need(set(z)=={'path','bytes','sha256','worktree_mode'} and type(z['worktree_mode']) is int and z['worktree_mode']==0o644,'Fresh native13 exact full0644 authority');v=ref(p);mode=stat.S_IMODE(p.stat().st_mode);native.append(dict(v,worktree_mode=mode))
    for n in OWNED_LOGS:
        p=R/n
        if p.exists() or p.is_symlink():v=ref(p);mode=stat.S_IMODE(p.stat().st_mode);logs.append(dict(v,worktree_mode=mode))
    return native,logs
def scope_ok(native,logs):return len(native)==13 and all(type(z['worktree_mode']) is int and z['worktree_mode']==0o644 for z in native+logs)
def main():
    need(__debug__ and sys.flags.optimize==0 and os.environ.get('PYTHONOPTIMIZE','') in ('','0'),'No optimized guards')
    need(A.name=='pr47_2849' and H.is_dir() and not H.is_symlink() and raw(Path(__file__))==raw(A/'root_acceptance_author_preparation/run_actual_acceptance_phases.py'),'ROOT copies exact reviewed SOURCE adjacent to A47; preparation path has no executable authority')
    old_umask=os.umask(0o022)
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['preflight','overlay','prepush','finalize','mirror','post']);p.add_argument('--merge-queue-preimage-sha256');a=p.parse_args();need((a.merge_queue_preimage_sha256 is None) if a.phase!='overlay' else (type(a.merge_queue_preimage_sha256) is str and re.fullmatch('[0-9a-f]{64}',a.merge_queue_preimage_sha256)),'Only overlay requires exact actual merge-queue SHA')
    b=raw(H/'PREPARATION_MANIFEST.json');need(sha(b)==PREP_SHA and stat.S_IMODE((H/'PREPARATION_MANIFEST.json').stat().st_mode)==0o444,'Exact actually closed47 source manifest');prep=parse(b);need(prep['schema']=='pr47-acceptance-source-closure/v1' and prep['status']=='CLOSED_SOURCE_ONLY' and prep['source_only'] is True and prep['self_excluded']==['PREPARATION_MANIFEST.json'] and type(prep['files_count']) is int and prep['files_count']==len(prep['files'])==126,'Actual126 source-only payloads');pins={z['path']:z for z in prep['files']};need(len(pins)==126,'Unique closed source rows')
    cdir=A/'root_final_reconciliation_actual_capture';need({x.name for x in cdir.iterdir()}=={'CAPTURE.json','PRELAUNCH_SOURCE.py','PRELAUNCH_OPERATOR.py','stdout.bin','stderr.bin'},'Complete genuine final-sealer CAP5');c=load(cdir/'CAPTURE.json')
    need(c['schema']=='ROOT_actual_audit_administrative_capture_v1' and c['actual_execution'] is True and c['completed'] is True and type(c['exit_code']) is int and c['exit_code']==0 and c['status']=='PASS' and type(c['pid']) is int and c['pid']>0 and c['stdin_supplied'] is False and c['cwd']==str(A),'Literal inspected completed sealer capture/PID')
    need(eq(c['native13_before'],c['native13_after']) and c['main_head_before']==c['main_head_after'],'Sealer preserved native13/main within its own epoch');need(c['source_unchanged'] is True and sha(raw(cdir/'PRELAUNCH_SOURCE.py'))==sha(member(H,pins['seal_final_evidence.py']))==c['source_sha256'],'Entire exact closed sealer source');need(type(c['argv']) is list and len(c['argv'])==16 and c['argv'][:3]==['/usr/bin/python3','-B',str(H/'seal_final_evidence.py')] and c['argv'].count('--execute')==1,'Literal complete actual sealer argv')
    for flag,value in [('--root-bindings',ref(A/'ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS.json')['path']),('--root-bindings-sha256',sha(raw(A/'ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS.json'))),('--plan',ref(A/'ROOT_FINAL_PLAN.json')['path']),('--plan-sha256',sha(raw(A/'ROOT_FINAL_PLAN.json'))),('--preparation-manifest-sha256',PREP_SHA),('--output','final_review')]:need(c['argv'].count(flag)==1 and c['argv'][c['argv'].index(flag)+1]==value,'Every complete actual sealer argv flag/pin exact')
    need(sha(raw(cdir/'PRELAUNCH_OPERATOR.py'))==sha(raw(A/'capture_root_final_operation.py'))==sha(member(H,pins['capture_root_final_operation.py']))==SEALER_OPERATOR_SHA,'Actual copied ROOT sealer operator equals reviewed closed47 body')
    for k in ['stdout','stderr']:need(c[k]['path']==k+'.bin','Literal final stream names');member(cdir,c[k])
    need(raw(cdir/'stderr.bin')==b'','Whole successful final-sealer stderr');plan=load(A/'ROOT_FINAL_PLAN.json');final=A/'final_review';receipt=load(final/'ROOT_FINAL_RECONCILIATION.json');mf=load(final/'FINAL_MANIFEST.json')
    need(eq(plan,receipt['entire_scope']) and eq(plan,load(final/'ROOT_REVIEWED_SCOPE.json')) and eq(receipt['bindings_before'],receipt['bindings_after']),'Complete final plan/scope/evidence identity');need(receipt['schema']=='pr47-actual-final-reconciliation/v1' and receipt['status']=='PASS' and type(receipt['pr']) is int and receipt['pr']==47 and type(receipt['problem_id']) is int and receipt['problem_id']==2849 and receipt['preparation_manifest_sha256']==PREP_SHA and receipt['actual_root_reconciliation'] is True and receipt['science_helpers_executed'] is False and receipt['shared_mutations'] is False,'Actual exact47 final receipt');need(clock(c['started_utc'])<=clock(receipt['utc'])<=clock(c['finished_utc'])<=dt.datetime.now(dt.timezone.utc),'Actual completed sealer aware UTC')
    need(mf['schema']=='pr47-final-root-two-member-closure/v1' and mf['self_excluded']==['FINAL_MANIFEST.json'] and type(mf['files_count']) is int and mf['files_count']==len(mf['files'])==2 and {z['path'] for z in mf['files']}=={'ROOT_FINAL_RECONCILIATION.json','ROOT_REVIEWED_SCOPE.json'} and {x.name for x in final.iterdir()}=={'ROOT_FINAL_RECONCILIATION.json','ROOT_REVIEWED_SCOPE.json','FINAL_MANIFEST.json'},'Exact final2+self topology')
    for z in mf['files']:member(final,z);need(stat.S_IMODE((final/z['path']).stat().st_mode)==0o444,'Full frozen final member mode')
    need(stat.S_IMODE((final/'FINAL_MANIFEST.json').stat().st_mode)==0o444,'Full frozen literal final self');stdout=load(cdir/'stdout.bin');need(stdout['status']=='PASS' and stdout['science_helpers_executed'] is False and stdout['shared_mutations'] is False and stdout['final_receipt_sha256']==sha(raw(final/'ROOT_FINAL_RECONCILIATION.json')) and stdout['final_manifest_sha256']==sha(raw(final/'FINAL_MANIFEST.json')),'Entire completed sealer stdout receipt pins')
    name={'mirror':'state_mirror_reconciliation.py','post':'verify_post_acceptance.py'}.get(a.phase,'integrate_reviewed_partial.py');script=H/name;body=member(H,pins[name]);need(stat.S_IMODE(script.stat().st_mode)==0o444,'Frozen reviewed selected phase source')
    bindings=load(A/'ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS.json');need(bindings['status']=='ROOT_APPROVED_CLOSED_WHOLE_SOURCE_AND_ACTUAL_PR46_EVIDENCE' and bindings['root_actual_PR46_predecessor_read_completed'] is True and clock(bindings['created_utc'])<=clock(c['started_utc']),'Genuine ROOT approval completed before final sealer');need(plan['root_bindings']==ref(A/'ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS.json')['path'] and plan['root_bindings_sha256']==sha(raw(A/'ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS.json')),'Whole final plan pins genuine ROOT bindings')
    previous={n:bindings[n] for n in ['previous_mirror','previous_post']}
    for n,file in [('previous_mirror','state_mirror_bindings.json'),('previous_post','post_acceptance_verification.json')]:need(eq(previous[n],ref(P46/file)),'Exact actual46 previous full reference, never pending SOURCE metadata')
    refs={'final-plan':A/'ROOT_FINAL_PLAN.json','final-receipt':final/'ROOT_FINAL_RECONCILIATION.json','final-manifest':final/'FINAL_MANIFEST.json','reconciliation-capture':cdir/'CAPTURE.json','previous-mirror':P46/'state_mirror_bindings.json','previous-post':P46/'post_acceptance_verification.json','fresh-preimage':A/'ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES.json','root-bindings':A/'ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS.json'};literal_refs={k:ref(q) for k,q in refs.items()};fresh=load(refs['fresh-preimage']);need(fresh['schema']=='pr47-root-fresh-acceptance-input-preimages/v1' and fresh['approved_by_root'] is True and clock(fresh['created_utc'])<=dt.datetime.now(dt.timezone.utc),'Genuine later fresh native authority');before,logs_before=permissions(fresh);need(scope_ok(before,logs_before),'Entire current13 and existing owned logs full0644 before child')
    argv=['/usr/bin/python3','-B',str(script),'--execute','--preparation-manifest-sha256',PREP_SHA]
    for flag,z in literal_refs.items():argv.extend(['--'+flag,z['path'],'--'+flag+'-sha256',z['sha256']])
    if a.phase not in ['mirror','post']:argv.append(a.phase)
    if a.phase=='overlay':argv.extend(['--merge-queue-preimage-sha256',a.merge_queue_preimage_sha256])
    dest=A/('root_'+a.phase+'_actual_capture');need(not dest.is_symlink() and not dest.exists(),'Exclusive actual phase capture');dest.mkdir(exist_ok=False);need(stat.S_IMODE(dest.stat().st_mode)==0o755,'Operational capture directory0755 under0022');operator=raw(Path(__file__));put(dest/'PRELAUNCH_SOURCE.py',body);put(dest/'PRELAUNCH_OPERATOR.py',operator)
    pre=dict(schema='ROOT_reviewed_acceptance_phase_prelaunch_v1',phase=a.phase,argv=argv,cwd=str(R),operator_pid=os.getpid(),operator_sha256=sha(operator),source_sha256=sha(body),prepared_utc=stamp(),stdin_supplied=False,preparation_manifest_sha256=PREP_SHA,complete_literal_final_references=literal_refs,native13_before=before,owned_mutable_logs_before=logs_before,permissions_scope=dict(native13_and_existing_owned_mutable_logs_full_mode=0o644,operator_previous_umask=old_umask,operator_child_umask=0o022,read_only_permission_checks=True,arbitrary_mode_writer_correctness_accepted=False,authorized_phase_body_changes_are_allowed=True));put(dest/'PRELAUNCH.json',(json.dumps(pre,indent=2)+'\n').encode())
    rec=dict(pre,schema='ROOT_actual_reviewed_acceptance_phase_capture_v1',started_utc=stamp(),actual_execution=False,completed=False,pid=None,exit_code=None);out=err=b'';child=None
    try:
        child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE);rec.update(actual_execution=True,pid=child.pid);out,err=child.communicate();rec.update(completed=True,exit_code=child.returncode)
    except BaseException:
        rec['operator_error']=traceback.format_exc()
        if child is not None:
            try:out,err=child.communicate();rec.update(completed=True,exit_code=child.returncode)
            except BaseException:rec['operator_reap_error']=traceback.format_exc()
    try:after,logs_after=permissions(fresh);rec.update(native13_after=after,owned_mutable_logs_after=logs_after);need(scope_ok(after,logs_after),'Entire current13 and existing owned logs full0644 after child');rec['before_after_permission_scope_checked']=True
    except BaseException:rec.update(before_after_permission_scope_checked=False,permission_check_after_error=traceback.format_exc())
    try:rec.update(source_unchanged=raw(script)==body,operator_unchanged=raw(Path(__file__))==operator)
    except BaseException:rec.update(source_unchanged=False,operator_unchanged=False,source_readback_error=traceback.format_exc())
    try:rec['complete_literal_final_references_after']={k:ref(q) for k,q in refs.items()};need(eq(rec['complete_literal_final_references_after'],literal_refs),'All eight actual final/reference bodies preserved across child');rec['complete_final_references_unchanged']=True
    except BaseException:rec.update(complete_final_references_unchanged=False,final_reference_readback_error=traceback.format_exc())
    rec['finished_utc']=stamp()
    for k,b in [('stdout',out),('stderr',err)]:put(dest/(k+'.bin'),b);rec[k]={'path':k+'.bin','bytes':len(b),'sha256':sha(b)}
    rec['status']='PASS' if rec['actual_execution'] is True and rec['completed'] is True and type(rec['pid']) is int and rec['pid']>0 and type(rec['exit_code']) is int and rec['exit_code']==0 and rec['source_unchanged'] is True and rec['operator_unchanged'] is True and rec['before_after_permission_scope_checked'] is True and rec['complete_final_references_unchanged'] is True and err==b'' and 'operator_error' not in rec else 'FAIL';put(dest/'CAPTURE.json',(json.dumps(rec,indent=2)+'\n').encode());print(json.dumps(rec,indent=2));return 0 if rec['status']=='PASS' else 1
if __name__=='__main__':sys.exit(main())
