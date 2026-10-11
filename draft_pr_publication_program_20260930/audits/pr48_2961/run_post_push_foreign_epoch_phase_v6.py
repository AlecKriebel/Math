"""UNEXECUTED SOURCE. ROOT caller retains actual adapter argv and both dependency classes."""
from pathlib import Path
import argparse,hashlib,json,os,stat,subprocess,sys,traceback,types
sys.dont_write_bytecode=True
A=Path(__file__).absolute().parent;R=A.parents[2];P=A/'post_push_foreign_epoch_preparation_v6'
def bootstrap(ready):
    if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','') not in ('','0'):raise ValueError('Nonoptimized exact source')
    os.environ['GIT_OPTIONAL_LOCKS']='0';os.environ['GIT_LITERAL_PATHSPECS']='1'
    for k in ['GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE','GIT_OBJECT_DIRECTORY','GIT_ALTERNATE_OBJECT_DIRECTORIES']:os.environ.pop(k,None)
    def raw(p,expected):
        if type(expected) is not int or p.is_symlink() or any(q.is_symlink() for q in p.parents) or not p.is_file():raise ValueError('Regular typed source mode')
        before=p.stat()
        if stat.S_IMODE(before.st_mode)!=expected:raise ValueError('Exact full07777 source mode at read')
        with p.open('rb') as stream:b=stream.read()
        after=p.stat()
        if (before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns,before.st_ctime_ns,before.st_mode)!=(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns,after.st_mode):raise ValueError('Source body/fullmode changed during read')
        return b
    source=raw(Path(__file__),0o644)
    if A.name!='pr48_2961' or source!=raw(P/Path(__file__).name,0o444):raise ValueError('Exact ROOT adjacent copy')
    b=raw(P/'SOURCE_READY.json',0o444)
    if hashlib.sha256(b).hexdigest()!=ready:raise ValueError('ROOT readiness hash')
    z=next(z for z in json.loads(b)['source_files'] if Path(z['path']).name=='epoch_common.py');cb=raw(R/z['path'],0o444)
    if len(cb)!=z['bytes'] or hashlib.sha256(cb).hexdigest()!=z['sha256']:raise ValueError('Cached verified common source')
    if stat.S_IMODE(P.stat().st_mode)!=0o755 or raw(R/z['path'],0o444)!=cb:raise ValueError('Prepared directory/common fullmode before cached compile')
    c=types.ModuleType('epoch_common');c.__file__=str(P/'epoch_common.py');sys.modules['epoch_common']=c;exec(compile(cb,c.__file__,'exec'),c.__dict__);c.source_read(Path(__file__),0o644);c.source_read(P/'epoch_common.py',0o444);return c,source

def main():
    p=argparse.ArgumentParser();p.add_argument('--source-ready-sha256',required=True);p.add_argument('--source-manifest-sha256',required=True);p.add_argument('--phase',choices=['finalize','mirror','post'],required=True);p.add_argument('--foreign-epoch',required=True);p.add_argument('--foreign-epoch-sha256',required=True);p.add_argument('--epoch-author-capture',required=True);p.add_argument('--outer-capture-directory',required=True);a=p.parse_args();c,operator=bootstrap(a.source_ready_sha256);os.umask(0o022);_,new=c.closed_packet(a.source_ready_sha256,a.source_manifest_sha256);old=c.original_sources();prior,last=c.validated_prefix(a.phase,a.source_ready_sha256,a.source_manifest_sha256);ep=R/c.safe(a.foreign_epoch);author=R/c.safe(a.epoch_author_capture);e=c.validated_epoch(ep,a.foreign_epoch_sha256,a.phase,author,a.source_ready_sha256,a.source_manifest_sha256);c.need(last<=c.clock(e['utc']),'Fresh role authority follows genuine previous child');effective=dict(e,_actual_path=a.foreign_epoch);g=c.activate(effective,a.phase,old,new);c.absent_outputs(a.phase);native,logs=c.native_and_logs(g,a.phase,e['current_queue']);c.need(c.eq(native,e['native13_before']) and c.eq(logs,e['owned_logs_before']),'Exact actual epoch native/owned-log preimages')
    script=A/'execute_post_push_foreign_epoch_phase_v6.py';source=c.raw(script);c.need(source==new['execute_post_push_foreign_epoch_phase_v6.py'],'Actual adapter exact prepared source');d=A/('root_'+a.phase+'_actual_capture');d.mkdir(exist_ok=False);c.put(d/'PRELAUNCH_SOURCE.py',source);c.put(d/'PRELAUNCH_OPERATOR.py',operator);outer=R/c.safe(a.outer_capture_directory)
    deps=[];ndeps=[]
    for directory,names,bodies,rows in [('ORIGINAL_DEPENDENCIES',c.dependency_names(a.phase),old,deps),('NEW_DEPENDENCIES',['epoch_common.py','integrate_reviewed_partial_epoch_v6.py','state_mirror_reconciliation_epoch_v6.py'],new,ndeps)]:
        sub=d/directory;sub.mkdir()
        for n in names:c.put(sub/n,bodies[n]);rows.append(c.ref(sub/n))
    refs={k:c.ref(R/c.pins()[k]) for k in ['final_plan','final_receipt','final_manifest','reconciliation_capture','previous_mirror','previous_post','fresh_preimage','root_bindings']};argv=c.adapter_argv(a.phase,a.source_ready_sha256,a.source_manifest_sha256,c.ref(ep),author.relative_to(R).as_posix());foreign=[{k:z[k] for k in ['path','bytes','sha256','worktree_mode']} for z in e['current_foreign_rows']]
    mode_before=c.caller_source_modes(outer,d,a.phase);c.need(c.eq(mode_before['runtime'],e['source_modes_before']['runtime']),'Actual mode-bound source versions match genuine epoch')
    pre=dict(schema='ROOT_explicit_post_push_epoch_phase_prelaunch_v6',phase=a.phase,prepared_utc=c.stamp(),argv=argv,cwd=str(R),operator_pid=os.getpid(),stdin_supplied=False,source_sha256=c.sha(source),operator_sha256=c.sha(operator),source_ready_sha256=a.source_ready_sha256,source_manifest_sha256=a.source_manifest_sha256,foreign_epoch=c.ref(ep),epoch_author_capture=c.ref(author),original17_pins=c.pins(),delegated_original_helper_argv=c.literal_helper_argv(a.phase,c.pins()),original_dependency_refs=deps,new_dependency_refs=ndeps,complete_literal_final_references=refs,native13_before=native,owned_mutable_logs_before=logs,protected_foreign_before=foreign,HEAD_before=e['current_head'],whole_index_before=e['whole_index'],original_dated_foreign_live_equality_asserted=False,declared_delegations=c.DELEGATIONS,mode_contract=c.MODE_CONTRACT,source_modes_before=mode_before,outer_capture_directory=a.outer_capture_directory)
    c.put(d/'PRELAUNCH.json',c.encode(pre));cap=dict(pre,schema='ROOT_actual_explicit_post_push_epoch_phase_capture_v6',started_utc=c.stamp(),actual_execution=False,completed=False,pid=None,exit_code=None);out=err=b'';child=None
    try:
        env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONOPTIMIZE='0',GIT_OPTIONAL_LOCKS='0')
        for k in ['GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE','GIT_OBJECT_DIRECTORY','GIT_ALTERNATE_OBJECT_DIRECTORIES']:env.pop(k,None)
        c.need(c.eq(c.caller_source_modes(outer,d,a.phase),mode_before),'Actual source/operator/prelaunch/dependency fullmodes immediately before real child');child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env);cap.update(actual_execution=True,pid=child.pid);out,err=child.communicate();cap.update(completed=True,exit_code=child.returncode)
        cap['source_modes_after']=c.caller_source_modes(outer,d,a.phase);c.need(c.eq(cap['source_modes_after'],mode_before),'Actual source/operator/prelaunch/dependency fullmodes immediately after real child');c.need(child.returncode==0,'Actual adapter failed; partial writes must be inspected, never blind-rerun');g.foreign_check(c.load(A/'integration_preflight.json'));afterphase={'finalize':'mirror','mirror':'post','post':'post'}[a.phase];after_native,after_logs=c.native_and_logs(g,afterphase,e['current_queue']);cap.update(native13_after=after_native,owned_mutable_logs_after=after_logs,protected_foreign_after=[{k:z[k] for k in ['path','bytes','sha256','worktree_mode']} for z in c.tracked_foreign(g)],HEAD_after=g.git('rev-parse','HEAD'),whole_index_after=c.git_index(g));c.closed_packet(a.source_ready_sha256,a.source_manifest_sha256)
        cap.update(source_unchanged=c.raw(script)==source==c.raw(d/'PRELAUNCH_SOURCE.py'),operator_unchanged=c.source_read(Path(__file__),0o644)[0]==operator==c.raw(d/'PRELAUNCH_OPERATOR.py'),original_dependencies_unchanged=all(c.check(z)==old[Path(z['path']).name] for z in deps),new_dependencies_unchanged=all(c.check(z)==new[Path(z['path']).name] for z in ndeps),complete_final_references_unchanged=c.eq(refs,{k:c.ref(R/c.pins()[k]) for k in refs}),protected_foreign_unchanged_during_this_phase=c.eq(cap['protected_foreign_after'],foreign),native_modes_and_owned_logs_scope_checked=True,source_fullmodes_unchanged=c.eq(cap['source_modes_after'],cap['source_modes_before']))
        c.need(all(cap[k] is True for k in ['source_unchanged','operator_unchanged','original_dependencies_unchanged','new_dependencies_unchanged','complete_final_references_unchanged','protected_foreign_unchanged_during_this_phase','native_modes_and_owned_logs_scope_checked','source_fullmodes_unchanged']) and c.eq(cap['HEAD_after'],cap['HEAD_before']) and c.eq(cap['whole_index_after'],cap['whole_index_before']) and err==b'','Actual role complete source/body/mode preservation')
        cap['status']='PASS'
    except BaseException:
        cap.update(status='FAIL',operator_error=traceback.format_exc())
        if child is not None and cap['completed'] is False:
            try:out,err=child.communicate();cap.update(completed=True,exit_code=child.returncode)
            except BaseException:cap['reap_error']=traceback.format_exc()
    for k,b in [('stdout',out),('stderr',err)]:c.put(d/(k+'.bin'),b);cap[k]=dict(path=k+'.bin',bytes=len(b),sha256=c.sha(b))
    cap['finished_utc']=c.stamp();cap['artifact_mode_bindings']=[dict(path=c.safe((d/n).relative_to(R).as_posix()),full_mode=0o644) for n in ['PRELAUNCH.json','PRELAUNCH_SOURCE.py','PRELAUNCH_OPERATOR.py','stdout.bin','stderr.bin','CAPTURE.json']];c.put(d/'CAPTURE.json',c.encode(cap));c.need(c.eq(cap['artifact_mode_bindings'],c.artifact_modes(d,['PRELAUNCH.json','PRELAUNCH_SOURCE.py','PRELAUNCH_OPERATOR.py','stdout.bin','stderr.bin','CAPTURE.json'])),'Actual complete new capture fullmodes after creation');print(json.dumps(dict(status=cap['status'],capture=c.ref(d/'CAPTURE.json'),actual_pid=cap['pid'],actual_exit_code=cap['exit_code'])));c.need(cap['status']=='PASS','Actual failed role retained; ROOT must inspect recovery')
if __name__=='__main__':main()
