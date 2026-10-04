"""UNEXECUTED SOURCE. ROOT alone authors one fresh current epoch before one role."""
from pathlib import Path
import argparse,hashlib,json,os,stat,sys
sys.dont_write_bytecode=True
A=Path(__file__).absolute().parent;R=A.parents[2];P=A/'post_push_foreign_epoch_preparation_v5'

def bootstrap(ready):
    if not __debug__ or sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE','') not in ('','0'):raise ValueError('Nonoptimized SOURCE only')
    os.environ['GIT_OPTIONAL_LOCKS']='0';os.environ['GIT_LITERAL_PATHSPECS']='1'
    for k in ['GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE','GIT_OBJECT_DIRECTORY','GIT_ALTERNATE_OBJECT_DIRECTORIES']:os.environ.pop(k,None)
    def body(p,expected):
        if type(expected) is not int or p.is_symlink() or any(q.is_symlink() for q in p.parents) or not p.is_file():raise ValueError('Regular typed source mode')
        before=p.stat()
        if stat.S_IMODE(before.st_mode)!=expected:raise ValueError('Exact full07777 source mode at read')
        with p.open('rb') as stream:b=stream.read()
        after=p.stat()
        if (before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns,before.st_ctime_ns,before.st_mode)!=(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns,after.st_mode):raise ValueError('Source body/fullmode changed during read')
        return b
    source=body(Path(__file__),0o644)
    if A.name!='pr48_2961' or source!=body(P/Path(__file__).name,0o444):raise ValueError('ROOT exact adjacent copy only')
    b=body(P/'SOURCE_READY.json',0o444)
    if hashlib.sha256(b).hexdigest()!=ready:raise ValueError('ROOT literal readiness hash')
    rows=json.loads(b)['source_files'];z=next(z for z in rows if Path(z['path']).name=='epoch_common.py');cb=body(R/z['path'],0o444)
    if len(cb)!=z['bytes'] or hashlib.sha256(cb).hexdigest()!=z['sha256']:raise ValueError('Actual cached common bytes')
    import types
    if stat.S_IMODE(P.stat().st_mode)!=0o755 or body(R/z['path'],0o444)!=cb:raise ValueError('Prepared directory/common fullmode before cached compile')
    c=types.ModuleType('epoch_common');c.__file__=str(P/'epoch_common.py');sys.modules['epoch_common']=c;exec(compile(cb,c.__file__,'exec'),c.__dict__);c.source_read(Path(__file__),0o644);c.source_read(P/'epoch_common.py',0o444)
    return c,source

def main():
    p=argparse.ArgumentParser();p.add_argument('--execute',action='store_true');p.add_argument('--personally-read-complete-source',action='store_true');p.add_argument('--source-ready-sha256',required=True);p.add_argument('--source-manifest-sha256',required=True);p.add_argument('--phase',choices=['finalize','mirror','post'],required=True);p.add_argument('--independent-source-verdict',required=True);p.add_argument('--independent-source-verdict-sha256',required=True);p.add_argument('--output',required=True);p.add_argument('--root-commit-capture',required=True);p.add_argument('--root-push-capture',required=True);p.add_argument('--outer-capture-directory',required=True);a=p.parse_args();c,source=bootstrap(a.source_ready_sha256);c.need(a.execute and a.personally_read_complete_source,'ROOT explicit actual source read required');os.umask(0o022)
    _,new=c.closed_packet(a.source_ready_sha256,a.source_manifest_sha256);original=c.original_sources();values=c.pins();prefix,last=c.validated_prefix(a.phase,a.source_ready_sha256,a.source_manifest_sha256);review=c.ref(R/c.safe(a.independent_source_verdict));c.need(review['sha256']==a.independent_source_verdict_sha256,'Actual independent verdict hash');c.source_review(review,a.source_ready_sha256)
    c.safe(a.output);c.need('/' not in a.output and a.output=='ROOT_POST_PUSH_V5_'+a.phase.upper()+'_FOREIGN_EPOCH.json','Literal distinct own epoch name');out=A/a.output;c.need(not out.exists() and not out.is_symlink(),'New actual epoch only');c.absent_outputs(a.phase)
    commit=R/c.safe(a.root_commit_capture);push=R/c.safe(a.root_push_capture);cc=c.cap4(commit);pc=c.cap4(push);c.need(cc['argv'][:2]==['git','commit'] and pc['argv']==['git','push','origin','main'] and c.clock(cc['finished_utc'])<=c.clock(pc['started_utc'])<=c.clock(pc['finished_utc'])<=c.clock(c.stamp()),'Real original commit then actual push')
    d=A/('root_'+a.phase+'_foreign_epoch_v5_readonly');d.mkdir(exist_ok=False);c.put(d/'PRELAUNCH_SOURCE.py',source);outer=R/c.safe(a.outer_capture_directory);mode_before=c.author_source_modes(outer,d);reads=c.Readonly(source,lambda:c.author_source_modes(outer,d));g=c.module('pr48_guards',original['pr48_guards.py'],c.H/'pr48_guards.py');g.git_bytes=reads.git
    try:
        frozen,pins=g.gates(argparse.Namespace(execute=True,**values));c.need(c.eq(pins,values),'Original17 gates retained');g.canonical(frozen,a.phase!='finalize');head=g.git('rev-parse','HEAD');reads.git('merge-base','--is-ancestor',c.MERGE,head);index=c.git_index(g);c.need(g.git('branch','--show-current')=='main','Actual main required')
        prefixpath=g.K.relative_to(R).as_posix()+'/'
        oldtree=reads.git('ls-tree','-r','-z',c.MERGE,'--',prefixpath);newtree=reads.git('ls-tree','-r','-z',head,'--',prefixpath);c.need(oldtree==newtree,'Whole original1955 canonical Git topology/body object identity remains exact in descendant')
        fresh=c.load(A/'ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES.json')
        for z in fresh['files']:
            n=z['path']
            if n==g.Q.relative_to(R).as_posix() or n in g.IGNORED_CACHE3:continue
            c.need(reads.git('ls-tree','-z',c.MERGE,'--',n)==reads.git('ls-tree','-z',head,'--',n),'All twelve other native Git identities remain historical accepted authority; additional drift requires separate review')
        native,logs=c.native_and_logs(g,a.phase);foreign=c.tracked_foreign(g);queue=c.mode_ref(g.Q)
        # Before post, the mirror's complete queue binding must remain genuine.
        if a.phase=='post':c.need(c.eq({k:queue[k] for k in ['path','sha256']},c.load(A/'state_mirror_bindings.json')['queue']),'No unreviewed post-mirror queue drift')
        e=dict(schema='pr48-ROOT-post-push-per-phase-foreign-epoch/v5',phase=a.phase,status='ROOT_APPROVED_CURRENT_FOREIGN_EPOCH_ONLY',approved_by_ROOT=True,utc=c.stamp(),actual_ROOT_author_pid=os.getpid(),science_or_original_approval_changed=False,original_dated_foreign_live_equality_asserted=False,source_ready=c.ref(P/'SOURCE_READY.json'),source_manifest=c.ref(P/'SOURCE_MANIFEST.json'),independent_SOURCE_review=review,original_preflight=c.ref(A/'integration_preflight.json'),original_preparation_manifest_sha256=c.PREP,merge_commit=c.MERGE,current_head=head,whole_index=index,dated_original_foreign_rows=c.load(A/'integration_preflight.json')['foreign_logs'],protected_foreign_tracked_paths=[z['path'] for z in foreign],current_foreign_rows=foreign,current_queue=queue,native13_before=native,owned_logs_before=logs,original17_pins=values,genuine_push_capture=c.ref(push),genuine_commit_capture=c.ref(commit),original_successful_prefix=prefix,readonly_ledger=None,declared_delegations=c.DELEGATIONS,mode_contract=c.MODE_CONTRACT,source_modes_before=mode_before,source_modes_after=None,source_custody_modes=None)
        # Target and absent alias predicates use original accepted science; no queue write.
        integration=c.module('integrate_reviewed_partial',new['integrate_reviewed_partial_epoch_v5.py'],P/'integrate_reviewed_partial_epoch_v5.py');after,row=integration.queue_after(c.raw(A/'integration_queue_before.md'));c.queue_check(g,e,after)
        c.need(c.eq(c.tracked_foreign(g),foreign) and g.git('rev-parse','HEAD')==head and c.eq(c.git_index(g),index),'Current full foreign domain/body/mode and HEAD/index unchanged during actual author')
        c.need(c.eq(list(c.native_and_logs(g,a.phase)), [native,logs]),'All13 native full bodies/modes and both owned log prefixes unchanged during actual author')
        c.need(c.clock(last)<=c.clock(e['utc']) and c.clock(pc['finished_utc'])<=c.clock(e['utc']),'New per-role actual authority follows prior successful role and real push')
        c.need(c.raw(Path(__file__))==source and c.raw(P/'author_post_push_foreign_epoch_v5.py')==source,'Actual author source unchanged');c.closed_packet(a.source_ready_sha256,a.source_manifest_sha256);e['source_modes_after']=c.author_source_modes(outer,d);c.need(c.eq(e['source_modes_before'],e['source_modes_after']),'Actual source/operator/prelaunch fullmode unchanged through ROOT epoch author')
        c.put(d/'READONLY_LEDGER.json',c.encode(reads.records));e['readonly_ledger']=c.ref(d/'READONLY_LEDGER.json');e['source_custody_modes']=dict(readonly_ledger=c.source_binding(d/'READONLY_LEDGER.json',0o644),epoch=dict(path=c.safe(out.relative_to(R).as_posix()),full_mode=0o644));c.need(set(e)==c.EPOCH_KEYS,'Exact epoch keyset');c.put(out,c.encode(e));c.need(c.artifact_modes(A,[out.name])==[e['source_custody_modes']['epoch']],'Actual new epoch fullmode after exclusive creation');c.need(c.eq(c.author_source_modes(outer,d),mode_before),'Source fullmodes remain exact after epoch output');print(json.dumps(dict(status='PASS_ACTUAL_ROOT_FOREIGN_EPOCH_ONLY',epoch=c.ref(out),actual_pid=os.getpid())))
    finally:
        if not (d/'READONLY_LEDGER.json').exists():c.put(d/'READONLY_LEDGER.json',c.encode(reads.records))
if __name__=='__main__':main()
