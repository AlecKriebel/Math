"""UNEXECUTED SOURCE. Transparent adapter child; own actual source/argv are retained."""
from pathlib import Path
import argparse,hashlib,json,os,stat,sys,types
sys.dont_write_bytecode=True
A=Path(__file__).absolute().parent;R=A.parents[2];P=A/'post_push_foreign_epoch_preparation_v5'
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
    if len(cb)!=z['bytes'] or hashlib.sha256(cb).hexdigest()!=z['sha256']:raise ValueError('Cached exact common source')
    if stat.S_IMODE(P.stat().st_mode)!=0o755 or raw(R/z['path'],0o444)!=cb:raise ValueError('Prepared directory/common fullmode before cached compile')
    c=types.ModuleType('epoch_common');c.__file__=str(P/'epoch_common.py');sys.modules['epoch_common']=c;exec(compile(cb,c.__file__,'exec'),c.__dict__);c.source_read(Path(__file__),0o644);c.source_read(P/'epoch_common.py',0o444);return c

def main():
    p=argparse.ArgumentParser();p.add_argument('--source-ready-sha256',required=True);p.add_argument('--source-manifest-sha256',required=True);p.add_argument('--phase',choices=['finalize','mirror','post'],required=True);p.add_argument('--foreign-epoch',required=True);p.add_argument('--foreign-epoch-sha256',required=True);p.add_argument('--epoch-author-capture',required=True);a=p.parse_args();c=bootstrap(a.source_ready_sha256);os.umask(0o022);_,new=c.closed_packet(a.source_ready_sha256,a.source_manifest_sha256);old=c.original_sources();c.validated_prefix(a.phase,a.source_ready_sha256,a.source_manifest_sha256);ep=R/c.safe(a.foreign_epoch);e=c.validated_epoch(ep,a.foreign_epoch_sha256,a.phase,R/c.safe(a.epoch_author_capture),a.source_ready_sha256,a.source_manifest_sha256);e['_actual_path']=c.safe(a.foreign_epoch);mode_before=c.current_runtime_source_modes();c.need(c.eq(mode_before,e['source_modes_before']['runtime']),'Exact actual adjacent/prepared/original source fullmodes before adapter compile/actions');g=c.activate(e,a.phase,old,new);c.absent_outputs(a.phase)
    c.need(c.eq(list(c.native_and_logs(g,a.phase,e['current_queue'])),[e['native13_before'],e['owned_logs_before']]),'Exact fresh per-role native and owned-log envelope before action')
    # Documentary original argv is never represented as this child's actual argv.
    delegated=c.literal_helper_argv(a.phase,c.pins());sys.argv=delegated[2:]
    target={'finalize':'integrate_reviewed_partial','mirror':'state_mirror_reconciliation','post':'verify_post_acceptance'}[a.phase];c.need(c.eq(c.current_runtime_source_modes(),mode_before),'Source fullmodes immediately before delegated action');sys.modules[target].main();c.need(c.eq(c.current_runtime_source_modes(),mode_before),'Source fullmodes immediately after delegated action')
    g.foreign_check(c.load(A/'integration_preflight.json'));c.native_and_logs(g,{'finalize':'mirror','mirror':'post','post':'post'}[a.phase],e['current_queue']);c.closed_packet(a.source_ready_sha256,a.source_manifest_sha256)
if __name__=='__main__':main()
