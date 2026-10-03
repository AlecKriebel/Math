"""Actually close only this adverse SOURCE audit; ROOT captures this child outside F."""
from pathlib import Path, PurePosixPath
import datetime as dt, hashlib, json, os, stat, sys
F=Path(__file__).absolute().parent; A=F.parent; R=A.parents[2]
def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def dump(v): return (json.dumps(v,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
def require(v,msg):
    if v is not True: raise ValueError(msg)
def regular(q):
    require(not q.is_symlink() and all(not p.is_symlink() for p in q.parents) and stat.S_ISREG(q.stat().st_mode),'regular nonsymlink required')
    return q.read_bytes()
def main():
    require(not sys.flags.optimize and os.environ.get('PYTHONOPTIMIZE','') in ('','0'),'no optimized closure')
    require(F.name=='current_source_adversary_family' and A.name=='pr46_30004438' and R==Path('/Users/alec/Documents/Math'),'exact own root')
    require(not (F/'SELF_MANIFEST.json').exists(),'never overwrite a closed own manifest')
    closer=regular(Path(__file__).absolute()); result=json.loads(regular(F/'PRIVATE_AUDIT_RESULTS.json')); verdict=json.loads(regular(F/'verdict.json'))
    require(result['status']=='PASS_SCOPED_PRIVATE_SOURCE_AUDIT' and result['assertions']==5396 and result['production_import_compile_or_execution'] is False,'genuine private control result')
    require(verdict['verdict']=='REQUIRES_SOURCE_CORRECTION' and verdict['closed_clean'] is False and len(verdict['mandatory_corrections'])==1,'adverse verdict remains adverse')
    captures=sorted(F.glob('PRIVATE_AUDIT_ACTUAL_*/CAPTURE.json')); require(len(captures)==4,'all four own launches retained')
    successful=[]
    for q in captures:
        cap=json.loads(regular(q)); folder=q.parent
        require({p.name for p in folder.iterdir()}=={'PRELAUNCH_SOURCE.py','PRELAUNCH_OPERATOR.py','PRELAUNCH.json','CAPTURE.json','stdout.bin','stderr.bin'},'six capture members exact')
        require(cap['actual_execution'] is True and cap['completed'] is True and type(cap['pid']) is int and cap['pid']>0 and type(cap['exit_code']) is int and cap['exit_code'] in (0,1),'genuine child termination')
        require(cap['source_unchanged'] is True and cap['operator_unchanged'] is True and cap['production_import_compile_or_execution'] is False,'only own unchanged source operated')
        require(sha(regular(folder/'PRELAUNCH_SOURCE.py'))==cap['source_sha256'] and sha(regular(folder/'PRELAUNCH_OPERATOR.py'))==cap['operator_sha256'],'prelaunch sources full exact')
        require(regular(folder/'PRELAUNCH_OPERATOR.py')==regular(F/'capture_private_audit.py'),'own current operator unchanged')
        for channel in ['stdout','stderr']:
            b=regular(folder/cap[channel]['path']); require(len(b)==cap[channel]['bytes'] and sha(b)==cap[channel]['sha256'],'full streams retained')
        if cap['exit_code']==0:
            require(regular(folder/'PRELAUNCH_SOURCE.py')==regular(F/'private_source_audit.py'),'successful current source exact'); successful.append(cap)
    require(len(successful)==1 and successful[0]['pid']==89631,'one real successful audit child')
    require(sha(regular(A/'current_preparation_family/PREPARATION_MANIFEST.json'))==verdict['preparation_manifest_sha256'],'audited source remains pinned')
    require(sha(regular(A/'current_preparation_family/prepare_current_packet.py'))==verdict['builder_sha256'],'audited builder remains pinned')
    require(sha(regular(A/'current_preparation_family/capture_root_builder_operation.py'))==verdict['operator_sha256'],'audited operator remains pinned')
    stamp=now(); verdict.update(own_source_closure=True,own_closure_pid=os.getpid(),own_closure_started_utc=stamp,separate_outer_closure_capture_completed_only_after_this_child_exit=True)
    (F/'verdict.json').write_bytes(dump(verdict))
    (F/'CLOSURE_PRELAUNCH_SOURCE.py').write_bytes(closer)
    with (F/'RESEARCH_LOG.md').open('a') as out:
        out.write('\n'+stamp+' — Actual own self-only closure child PID '+str(os.getpid())+'. Scoped source adversary100%; clean SOURCE approval0%; actual current freeze/whole-current/final acceptance unverified; discovery credit0%. Verdict remains REQUIRES_SOURCE_CORRECTION with mandatory C1 and nonblocking Q1. Separate outer capture must be written by ROOT only after this child terminates.\n')
        out.flush(); os.fsync(out.fileno())
    paths=list(F.rglob('*')); require(all(not p.is_symlink() for p in paths),'no own symlink')
    files=[p for p in paths if stat.S_ISREG(p.stat().st_mode)]; dirs=[p for p in paths if stat.S_ISDIR(p.stat().st_mode)]
    require(len(files)+len(dirs)==len(paths),'no own special member')
    names={p.relative_to(F).as_posix() for p in files}; directories={p.relative_to(F).as_posix() for p in dirs}
    implied={p.as_posix() for name in names for p in PurePosixPath(name).parents if p.as_posix()!='.'}
    require(directories==implied,'own exact recursive directory topology')
    rows=[]
    for q in sorted(files):
        b=regular(q); q.chmod(0o444); require(stat.S_IMODE(q.stat().st_mode)==0o444,'own full0444')
        rows.append({'path':q.relative_to(F).as_posix(),'bytes':len(b),'sha256':sha(b),'full_mode':'0444'})
    manifest={'schema':'PR46_CURRENT_SOURCE_ADVERSARY_SELF_ONLY_CLOSURE_v1','self_excluded':['SELF_MANIFEST.json'],'files_count':len(rows),'files':rows,'directories':sorted(directories),'directory_full_modes':{n:stat.S_IMODE((F/n).stat().st_mode) for n in sorted(directories)},'all_full_mode0444':True,'utc':stamp,'actual_closure_pid':os.getpid(),'parent_pid':os.getppid(),'source_audit_verdict':'REQUIRES_SOURCE_CORRECTION','closed_clean':False,'mandatory_corrections':['C1_FALSE_INNER_GIT_LOG_POSTEXIT_WRITE_CLAIM'],'production_import_compile_or_execution':False,'native_or_Git_writes':False,'separate_actual_outer_capture_required_after_child_exit':True,'clean_SOURCE_approval_or_current_freeze_or_whole_acceptance_granted':False}
    with (F/'SELF_MANIFEST.json').open('xb') as out: out.write(dump(manifest)); out.flush(); os.fsync(out.fileno())
    (F/'SELF_MANIFEST.json').chmod(0o444)
    for row in rows:
        q=F/row['path']; b=regular(q); require(len(b)==row['bytes'] and sha(b)==row['sha256'] and stat.S_IMODE(q.stat().st_mode)==0o444,'own closed row exact')
    require(regular(Path(__file__).absolute())==closer,'own closer unchanged')
    require({p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_file()}==names|{'SELF_MANIFEST.json'},'self alone excluded')
    print(json.dumps({'status':'ACTUAL_ADVERSE_SOURCE_AUDIT_SELF_CLOSED','files_count':len(rows),'manifest_sha256':sha(regular(F/'SELF_MANIFEST.json')),'verdict':'REQUIRES_SOURCE_CORRECTION','closed_clean':False,'production_executed':False},sort_keys=True))
if __name__=='__main__': main()
