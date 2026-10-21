"""Root PR206 buffer-authenticated native lifecycle; MAIN CAS is external."""
import sys
if not (sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path and not sys.flags.optimize):
    raise RuntimeError("Ordinary Python -E -S -B -P required before dependency imports")
from pathlib import Path
import argparse,hashlib,importlib.util,json,os,stat,types
D=Path(__file__).absolute().parent
A=D.parent
AUDITS=A.parent
P=AUDITS.parent
ROOT=P.parent
OWN='publication_lifecycle_preparation_02'
ADOPTION='ROOT_LIFECYCLE_SOURCE_ADOPTION_01.json'
BACKENDS=frozenset([
'draft_pr_publication_program_20260930/audits/pr152_5000006/prepare_scoped_merge.py',
'draft_pr_publication_program_20260930/audits/pr177_10400049/prepare_final_scoped_merge.py',
'draft_pr_publication_program_20260930/audits/pr177_10400049/prepare_progress_checkpoint_01.py',
'draft_pr_publication_program_20260930/audits/pr179_10800007/prepare_final_scoped_merge.py',
'draft_pr_publication_program_20260930/audits/pr179_10800007/prepare_progress_checkpoint_03.py',
'draft_pr_publication_program_20260930/audits/pr190_5000007/campaign_aliases.py',
'draft_pr_publication_program_20260930/audits/pr190_5000007/prepare_final_scoped_merge.py',
'draft_pr_publication_program_20260930/audits/pr191_5000005/lifecycle_common.py',
'draft_pr_publication_program_20260930/audits/pr204_5100012/immutable_tree_transport_01/tree_transport.py'])
def need(ok,msg):
    if type(ok) is not bool or not ok: raise RuntimeError(msg)
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def checked(path,wanted,readonly=True):
    need(path.is_absolute() and path.is_relative_to(ROOT) and path.resolve(strict=True)==path,'Noncanonical/outside input')
    for q in (path,*path.parents):
        if q==ROOT.parent:break
        need(not q.is_symlink(),'Symlink input')
    before=path.lstat();need(stat.S_ISREG(before.st_mode) and before.st_size<=2000000 and (not readonly or stat.S_IMODE(before.st_mode)==0o444),'Regular bounded input before open')
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC|os.O_NONBLOCK)
    try:
        s=os.fstat(fd)
        need(stat.S_ISREG(s.st_mode) and s.st_size<=2000000 and (not readonly or stat.S_IMODE(s.st_mode)==0o444),'Regular bounded input')
        with os.fdopen(fd,'rb',closefd=False) as f:raw=f.read(2000001)
    finally:os.close(fd)
    need(pin(raw)==wanted,'Exact externally adopted input')
    return raw
def execution_buffer(path,raw):
    if path==AUDITS/'pr179_10800007/prepare_final_scoped_merge.py':
        edits=[
        (b"if TREE_CACHE_PATH.exists():\n for key,rows in json.loads(TREE_CACHE_PATH.read_text())['trees'].items():\n  verify_tree_object(key,rows);native_tree_cache[key]={n:tuple(x) for n,x in rows.items()}\n",b"# Root: legacy disk-cache read disabled in this execution buffer.\n"),
        (b"atexit.register(persist_authenticated_tree_cache)\n",b"# Root: legacy exit writer registration disabled in this execution buffer.\n")]
        for old,new in edits:
            need(raw.count(old)==1,'Exact accepted backend execution edit')
            raw=raw.replace(old,new,1)
    return raw
class BufferLoader:
    def __init__(self,path,raw):self.path,self.raw=path,raw
    def create_module(self,spec):return None
    def exec_module(self,module):exec(compile(self.raw,str(self.path),'exec'),module.__dict__)
class SafeParser(argparse.ArgumentParser):
    def error(self,message):raise RuntimeError('Invalid command arguments')
def main():
    ap=SafeParser()
    ap.add_argument('--adoption',required=True)
    ap.add_argument('--adoption-bytes',required=True,type=int)
    ap.add_argument('--adoption-sha256',required=True)
    ap.add_argument('phase',choices=['ready','merge','factual','completion'])
    ap.add_argument('action',choices=['preflight','bind','prepare','verify','accept','sync','pointer'])
    ap.add_argument('generation')
    ap.add_argument('--ack-path')
    ap.add_argument('--ack-bytes',type=int)
    ap.add_argument('--ack-sha256')
    args=ap.parse_args()
    need(args.adoption==ADOPTION,'Exact canonical Root adoption basename')
    wanted={'bytes':args.adoption_bytes,'sha256':args.adoption_sha256}
    adopt=json.loads(checked(A/ADOPTION,wanted))
    checked(Path(__file__).absolute(),adopt['dispatcher_pin'])
    need(adopt.get('schema')=='pr206-root-lifecycle-source-adoption-v1' and adopt.get('evidence_scope')=='ACTUAL_ROOT_RECEIPT' and adopt.get('accepted_preparation_only') is True and adopt.get('PR')==206 and adopt.get('original_head')=='488e8f575a6c9bcc0bd097d2852c9a7fa19bf8a7','Exact Root lifecycle adoption')
    need(adopt.get('external_dispatcher_owns_authenticated_direct8_adapter_and_all_alias_cache_cleanup') is True,'Explicit backend/cleanup ownership')
    expected={OWN+'/'+n for n in ['support206.py','ready206.py','lifecycle206.py','make_native206.py']}
    need(set(adopt['sources'])==expected and set(adopt['loader_sources'])==BACKENDS,'Exact four modules and direct9 source graph')
    buffers={A/n:checked(A/n,e) for n,e in adopt['sources'].items()}
    backend={}
    for n,e in adopt['loader_sources'].items():
        path=ROOT/n;raw=checked(path,e['original'],e['readonly']);body=execution_buffer(path,raw)
        need(pin(body)==e['execution'],'Exact accepted backend execution buffer');backend[path]=body
    gref=adopt['expected_publication_gate']
    need(set(gref)=={'path','bytes','sha256'} and gref['path']=='ROOT_PUBLICATION_GATE_01.json','Exact gate envelope')
    gpin={k:gref[k] for k in ('bytes','sha256')}
    checked(A/gref['path'],gpin)
    aliases=['Root_support206','Root_ready206','Root_native206','Root_lifecycle206']
    present={n:n in sys.modules for n in aliases}
    prior={n:sys.modules.get(n) for n in aliases}
    original_spec=importlib.util.spec_from_file_location
    cache=None;mods=[];original_api=None;loaded=[]
    def direct(name,path):
        v=types.ModuleType(name);v.__file__=str(path);v.__package__='';sys.modules[name]=v
        exec(compile(buffers[path],str(path),'exec'),v.__dict__);return v
    def guarded_spec(name,path,*aa,**kw):
        q=Path(path)
        need(q.is_absolute() and q in backend and not aa and not kw,'Unapproved backend import')
        spec=original_spec(name,q);need(spec is not None,'Backend module spec')
        spec.loader=BufferLoader(q,backend[q]);loaded.append(str(q.relative_to(ROOT)));return spec
    def native(name,path):
        spec=guarded_spec(name,path);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v);return v
    try:
        S=direct(aliases[0],A/OWN/'support206.py');S.configure_authority(wanted)
        N=direct(aliases[2],A/OWN/'make_native206.py');R=direct(aliases[1],A/OWN/'ready206.py')
        L=direct(aliases[3],A/OWN/'lifecycle206.py');N.configure(S);R.configure(S);L.configure(S,R,N)
        need(S.writer_protocol()==adopt['program_view_writer_protocol'],'Exact shared cooperating-writer protocol')
        S.gate(gpin);S.baseline_custody();S.originals();S.queue_rows();S.generation(args.generation)
        ack=None
        if args.phase=='ready':
            need(args.ack_path is None and args.ack_bytes is None and args.ack_sha256 is None,'No metadata acknowledgement at ready90')
        else:
            need(args.ack_path=='ROOT_PR_METADATA_ACKNOWLEDGEMENT_01.json' and args.ack_bytes is not None and args.ack_sha256 is not None,'Explicit canonical actual metadata acknowledgement')
            ack={'path':args.ack_path,'bytes':args.ack_bytes,'sha256':args.ack_sha256}
        if args.action=='preflight':
            need(args.phase=='ready','Pure local preflight is limited to ready; nonready prerequisites require native validation')
            R.inputs(gpin)
            print(json.dumps({'PR':206,'phase':'ready','preflight':True,'authenticated_sources':len(buffers)+len(backend),'backend_import_API_cache_or_phase':False,'program_lock_read_or_acquired':False},sort_keys=True))
            return
        if args.action=='bind' and args.phase=='ready':
            result=R.bind(args.generation,gpin);print(json.dumps(result,sort_keys=True,allow_nan=False));return
        importlib.util.spec_from_file_location=guarded_spec
        c=native('Root_direct_c191_206',AUDITS/'pr191_5000005/lifecycle_common.py')
        h=native('Root_direct_h190_206',AUDITS/'pr190_5000007/prepare_final_scoped_merge.py')
        adapter=native('Root_tree_adapter206',AUDITS/'pr204_5100012/immutable_tree_transport_01/tree_transport.py')
        mods=[h,h.m,h.m.m,h.m.m.h,h.m.m.h.m,h.m.m.h.m.m];original_api=h.api
        need(len({id(v) for v in mods})==6 and all(v.api is original_api for v in mods),'Six distinct identical API aliases')
        need(h.m.native_tree_cache is h.lookup.__globals__['TREE_CACHE'] and not h.m.native_tree_cache,'No inherited disk cache')
        S.configure_backend(c,h)
        original_init=adapter.TreeCache.__init__
        def capture_init(instance,*aa,**kw):
            nonlocal cache
            cache=instance;instance.fd=None
            return original_init(instance,*aa,**kw)
        adapter.TreeCache.__init__=capture_init
        try:cache,_restore=adapter.install_loaded(c,h)
        finally:adapter.TreeCache.__init__=original_init
        if args.action=='bind':result=L.bind(args.phase,args.generation,ack)
        else:result=getattr(R,args.action)(args.generation) if args.phase=='ready' else getattr(L,args.action)(args.phase,args.generation)
        print(json.dumps(result,sort_keys=True,allow_nan=False))
    finally:
        errors=[];restore_attempts=0
        if mods:
            for obj in mods:
                try:
                    if obj.api is not cache and obj.api is not original_api:errors.append('Unexpected API alias before restoration')
                except BaseException as exc:errors.append('Alias read: '+type(exc).__name__)
                try:
                    restore_attempts+=1;obj.api=original_api
                except BaseException as exc:errors.append('Alias restore: '+type(exc).__name__)
        if cache is not None:
            try:cache.close()
            except BaseException as exc:errors.append('Cache close: '+type(exc).__name__)
        importlib.util.spec_from_file_location=original_spec
        for n in aliases:
            try:
                if present[n]:sys.modules[n]=prior[n]
                else:sys.modules.pop(n,None)
            except BaseException as exc:errors.append('Module restore: '+type(exc).__name__)
        if cache is not None:
            print(json.dumps({'transport_stats':getattr(cache,'stats',{}),'all_six_API_restore_attempted':restore_attempts==6,'API_restore_attempt_count':restore_attempts,'cleanup_errors':errors},sort_keys=True))
        if errors:raise RuntimeError('Lifecycle dispatcher cleanup failed: '+repr(errors))
def entry():
    try:main()
    except BaseException as error:
        if isinstance(error,SystemExit) and (error.code is None or (type(error.code) is int and error.code==0)):return
        sys.stderr.write('Root PR206 lifecycle failed: '+type(error).__name__+'\n')
        raise SystemExit(1) from None
if __name__=='__main__':entry()

