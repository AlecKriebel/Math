#!/usr/bin/env python3
"""Close only this family. A postchild ROOT readback must be captured separately."""
from pathlib import Path, PurePosixPath
import argparse, datetime as dt, hashlib, json, os, stat, sys
F=Path(__file__).absolute().parent; A=F.parent
def req(v,n):
    if not v: raise ValueError(n)
def sha(b): return hashlib.sha256(b).hexdigest()
def dump(v): return (json.dumps(v,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
def read(p):
    req(not p.is_symlink() and not any(q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'Regular nonsymlink source required'); return p.read_bytes()
def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--execute',action='store_true'); a=p.parse_args()
    req(a.execute and not sys.flags.optimize,'Explicit unoptimized private closure required')
    req(F.name=='current_source_adversary_family_v2' and A.name=='pr46_30004438' and A.parents[2]==Path('/Users/alec/Documents/Math'),'Exact private scope required')
    req(not (F/'MANIFEST.json').exists() and not (F/'MANIFEST.json').is_symlink(),'Never overwrite closure')
    req(not (A/'reviewed_candidate').exists() and not (A/'reviewed_candidate').is_symlink(),'SOURCE audit precedes current packet')
    for n,s in [('PREPARATION_MANIFEST.json','5ba87a43d1e5da841c8d6f47b6c398c5de55047a447468e1576d2b0cbbd7439e'),('prepare_current_packet.py','e6df8cf9b54132d0ec9aee6d4a010e4f8ae95797dbbdd4abd23eb03f86856215'),('capture_root_builder_operation.py','02a5a169bfc87cb83595d796e375ece467f4073e63ac91f4171af6403606ae8a')]: req(sha(read(A/'current_preparation_family_v2'/n))==s,'Operative SOURCE pin changed')
    b=json.loads(read(F/'PRIVATE_CONTROL_RESULTS.json')); e=json.loads(read(F/'EXTENDED_CONTROL_RESULTS.json')); v=json.loads(read(F/'verdict.json'))
    req(b['assertions_passed']==len(b['assertion_labels'])==13179 and e['assertions_passed']==len(e['assertion_labels'])==15916 and b['failed']==e['failed']==0,'Final complete assertion receipts')
    req(b['fixed_full_body_reads_unique']==len(b['complete_fixed_member_reads'])==627 and sum(r['bytes'] for r in b['complete_fixed_member_reads'])==56626784,'Exact full body reads')
    req(v['mandatory_corrections']==[] and v['future_acceptance_approved'] is False and v['private_final_suite_assertions']==29095,'Scoped verdict only')
    for rr in b['complete_fixed_member_reads']:
        raw=read(A/rr['path']); req(len(raw)==rr['bytes'] and sha(raw)==rr['sha256'],'Fixed dependency changed before closing')
    captures=[]
    for d in sorted(F.glob('actual_private_capture_*')):
        cap=json.loads(read(d/'CAPTURE.json')); pre=json.loads(read(d/'PRELAUNCH.json'))
        req(cap['actual_execution'] is True and cap['completed'] is True and type(cap['pid']) is int and cap['pid']>0 and type(cap['exit_code']) is int and cap['exit_code'] in [0,1],'Real captured completion')
        req(cap['source_unchanged'] is True and cap['operator_unchanged'] is True and cap['native13_unchanged'] is True and cap['native13_before']==cap['native13_after'],'Actual source/operator/native beforeafter unchanged')
        req(sha(read(d/'PRELAUNCH_SOURCE.py'))==cap['source_sha256'] and sha(read(d/'PRELAUNCH_OPERATOR.py'))==cap['operator_sha256'],'Preserved prelaunch sources')
        for k in ['stdout','stderr']:
            rr=cap[k]; body=read(d/rr['path']); req(len(body)==rr['bytes'] and sha(body)==rr['sha256'],'Complete streams')
        req(pre['actual_execution'] is False and pre['pid'] is None and pre['completed'] is False,'No fabricated prelaunch completion')
        captures.append({'directory':d.name,'pid':cap['pid'],'exit_code':cap['exit_code'],'capture_sha256':sha(read(d/'CAPTURE.json'))})
    req(len(captures)==4 and [c['exit_code'] for c in captures]==[1,0,0,0],'One genuine failure and all three successful private runs preserved')
    source=read(Path(__file__).absolute()); (F/'CLOSING_CHILD_SOURCE_SNAPSHOT.py').write_bytes(source)
    now=dt.datetime.now(dt.timezone.utc).isoformat()
    (F/'CLOSING_CHILD_INVOCATION.json').write_bytes(dump({'schema':'PR46_PRIVATE_SELF_CLOSING_CHILD_INVOCATION_v1','pid':os.getpid(),'parent_pid':os.getppid(),'argv':sys.argv,'cwd':str(Path.cwd()),'started_inside_child_utc':now,'source_sha256':sha(source),'is_prelaunch_capture':False,'completed_outer_capture':None,'ROOT_postchild_readback_pending':True}))
    with (F/'RESEARCH_LOG.md').open('a') as log:
        log.write('\n'+now+' — Self-only closing child'+str(os.getpid())+'. Estimated bounded SOURCE audit completion100%; production execution/current-freeze validation0%; new-discovery credit0%. All own files are being frozenfull0444 with sole MANIFEST exclusion. No postchild completion capture is claimed inside this self closure. ROOT must independently read back the closed family AFTER this child exits and preserve that actual separate capture outside this family. The optional lexical/unknown-field limits remain in the full report.\n')
        log.flush(); os.fsync(log.fileno())
    files=[]; dirs=set()
    for pth in sorted(F.rglob('*')):
        req(not pth.is_symlink(),'No symlink member')
        if pth.is_dir(): dirs.add(pth.relative_to(F).as_posix()); continue
        raw=read(pth); pth.chmod(0o444); req(stat.S_IMODE(pth.stat().st_mode)==0o444,'Full mode exact444')
        files.append({'path':pth.relative_to(F).as_posix(),'bytes':len(raw),'sha256':sha(raw)})
    names={r['path'] for r in files}; req(dirs=={str(p) for n in names for p in PurePosixPath(n).parents if str(p)!='.'},'No extra/empty directory')
    result={'schema':'PR46_INDEPENDENT_V2_SOURCE_ADVERSARY_SELF_ONLY_CLOSURE_v1','status':'CLOSED_SOURCE_ONLY_INDEPENDENT_V2_ADVERSARY','closed_utc':now,'closing_child_pid':os.getpid(),'self_excluded':['MANIFEST.json'],'files_count':len(files),'files':files,'directories':sorted(dirs),'directory_modes':{n:stat.S_IMODE((F/n).stat().st_mode) for n in sorted(dirs)},'all_member_full_modes':'0444','verdict':v['verdict'],'mandatory_corrections':[],'private_final_suite_assertions':29095,'fixed_unique_full_body_reads':627,'production_import_compile_execute':False,'ROOT_runtime_or_future_merge_certified':False,'future_acceptance_approved':False,'new_discovery_credit_percent':0,'original_substantive_attempts':0,'original_source_verification_responses':1,'new_substantive_attempts':0,'audit_turns':0,'complete_own_private_actual_captures':captures,'postchild_ROOT_separate_external_readback':None,'ROOT_separate_postchild_readback_pending':True,'report':'AUDIT.md','operative_preparation_directory':'current_preparation_family_v2','preparation_manifest_sha256':v['preparation_manifest_sha256'],'builder_sha256':v['builder_sha256'],'operator_sha256':v['operator_sha256'],'source_audit_completion_estimate_percent':100,'production_runtime_validation_completion_estimate_percent':0,'foreign_body_copy':False}
    with (F/'MANIFEST.json').open('xb') as out: out.write(dump(result)); out.flush(); os.fsync(out.fileno())
    (F/'MANIFEST.json').chmod(0o444)
    for rr in files:
        raw=read(F/rr['path']); req(len(raw)==rr['bytes'] and sha(raw)==rr['sha256'] and stat.S_IMODE((F/rr['path']).stat().st_mode)==0o444,'Frozen member readback')
    req(read(Path(__file__).absolute())==source,'Closing source unchanged')
    print(json.dumps({'status':result['status'],'files_count':len(files),'manifest_sha256':sha(read(F/'MANIFEST.json')),'closing_child_pid':os.getpid(),'private_final_suite_assertions':29095,'source_audit_completion_estimate_percent':100,'ROOT_postchild_readback_pending':True,'future_acceptance_approved':False},sort_keys=True))
if __name__=='__main__': main()
