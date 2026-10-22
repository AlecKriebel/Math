"""Root authenticated-buffer dispatcher for PR206 publication and tracking."""
import sys
if not (sys.flags.ignore_environment==1 and sys.flags.no_site==1 and sys.dont_write_bytecode and sys.flags.safe_path and not sys.flags.optimize):
    raise RuntimeError('Python -E -S -B -P without -O required before dependency imports')
from pathlib import Path
import argparse,hashlib,json,os,stat,types
D=Path(__file__).resolve().parent
A=D.parent
OWN='publication_operations_preparation_02'
ADOPTION='ROOT_PUBLICATION_OPERATIONS_ADOPTION_01.json'
KIT='/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py'
PINS={
'ops_common206.py':(26399,'daeb8fb3d153de25ffec8521aaf913120ee2ffa8571019b4e7395dd541e7855a'),
'publisher206.py':(12158,'51809038d0811aba4d35584777a476f362ed032b51760059802c215ba6b7da3e'),
'tracker206.py':(12926,'10975c5abf2b5cc87927bfd791395af76da9216f3e8f9a471d50b36baaf45e33'),
'offline_guards.py':(49615,'3907aa894454038ddaa532fee0494156f4e8f09662efefd08223bafa00c4e473'),
'run_offline.py':(4735,'f468f54f541ec39be9601292657d9a260cc1494935b602db5c5803db5f5a7d41')}
def need(ok,message):
    if type(ok) is not bool or not ok: raise RuntimeError(message)
def pin(raw): return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def checked(path,wanted):
    resolved=path.resolve(strict=True)
    need(path.is_absolute() and resolved==path and resolved.is_relative_to(A),'Normalized path inside PR206 required')
    for q in (path,*path.parents):
        if q==A.parent: break
        need(not q.is_symlink(),'Symlinked source/input')
    before=path.lstat();need(stat.S_ISREG(before.st_mode) and stat.S_IMODE(before.st_mode)==0o444 and before.st_size<=2000000,'Regular readonly input before open')
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC|os.O_NONBLOCK)
    try:
        s=os.fstat(fd)
        need(stat.S_ISREG(s.st_mode) and stat.S_IMODE(s.st_mode)==0o444 and s.st_size<=2000000,'Regular readonly bounded input')
        with os.fdopen(fd,'rb',closefd=False) as f: raw=f.read(2000001)
    finally:
        os.close(fd)
    need(pin(raw)==wanted,'Exact input pin: '+path.name)
    return raw
def load_module(name,path,raw):
    module=types.ModuleType(name)
    module.__file__=str(path)
    module.__package__=''
    sys.modules[name]=module
    exec(compile(raw,str(path),'exec'),module.__dict__)
    return module
class SafeParser(argparse.ArgumentParser):
    def error(self,message):raise RuntimeError('Invalid command arguments')
def main():
    ap=SafeParser()
    ap.add_argument('--adoption',required=True)
    ap.add_argument('--adoption-bytes',required=True,type=int)
    ap.add_argument('--adoption-sha256',required=True)
    ap.add_argument('action',choices=['preflight','stage','inspect','publish','inspect-doi','finalize','append','recover'])
    ap.add_argument('--confirm-id',type=int)
    args=ap.parse_args()
    need(args.adoption==ADOPTION,'Fixed Root operations adoption basename required')
    wanted={'bytes':args.adoption_bytes,'sha256':args.adoption_sha256}
    adoption=json.loads(checked(A/ADOPTION,wanted))
    need(adoption.get('schema')=='pr206-root-publication-operations-adoption-v1' and adoption.get('evidence_scope')=='ACTUAL_ROOT_RECEIPT' and adoption.get('accepted_preparation_only') is True and adoption.get('PR')==206 and adoption.get('original_head')=='488e8f575a6c9bcc0bd097d2852c9a7fa19bf8a7','Root adoption identity')
    expected={OWN+'/'+n:{'bytes':v[0],'sha256':v[1]} for n,v in PINS.items()}
    need(adoption['sources']==expected,'Exact approved five-source set')
    checked(Path(__file__),adoption['dispatcher_pin'])
    checked(A/'ROOT_PUBLICATION_GATE_01.json',adoption['approved_publication_gate_pin'])
    checked(A/'ROOT_ACTUAL_READY_CHECKPOINT.json',adoption['approved_actual_ready_pointer_pin'])
    checked(A/'ROOT_ACTUAL_READY_VERIFICATION_01.json',adoption['approved_actual_ready_verification_pin'])
    checked(A/'ROOT_PUBLICATION_OPERATIONS_CONTRACT_ADDENDUM_01.json',adoption['approved_operations_contract_addendum_pin'])
    buffers={n:checked(A/OWN/n,expected[OWN+'/'+n]) for n in PINS}
    aliases=('ops_common206','Root_pr206_publisher','Root_pr206_tracker')
    prior={name:sys.modules.get(name) for name in aliases}
    present={name:name in sys.modules for name in aliases}
    oldargv=list(sys.argv)
    try:
        common=load_module(aliases[0],A/OWN/'ops_common206.py',buffers['ops_common206.py'])
        common.configure_authority(ADOPTION,wanted)
        if args.action=='preflight':
            context=common.load_context(A)
            print(json.dumps({'preflight':True,'PR':206,'context':common.context_pin(context),'compiled_sources':['ops_common206.py'],'checked_sources':len(buffers),'process_or_HTTP_or_Git_calls':False},sort_keys=True))
            return
        tracker=args.action in ('append','recover')
        name='tracker206.py' if tracker else 'publisher206.py'
        module=load_module(aliases[2] if tracker else aliases[1],A/OWN/name,buffers[name])
        sys.argv=[str(A/OWN/name),args.action,'--base',str(A),'--adoption',ADOPTION,'--adoption-bytes',str(args.adoption_bytes),'--adoption-sha256',args.adoption_sha256]
        if not tracker: sys.argv+=['--kit',KIT]
        if args.confirm_id is not None:
            need(not tracker and args.action in ('inspect','publish','inspect-doi'),'Known ID only for an explicit Zenodo phase')
            sys.argv+=['--confirm-id',str(args.confirm_id)]
        module.main()
    finally:
        sys.argv=oldargv
        for name in aliases:
            if present[name]: sys.modules[name]=prior[name]
            else: sys.modules.pop(name,None)
def entry():
    try:main()
    except BaseException as error:
        if isinstance(error,SystemExit) and (error.code is None or (type(error.code) is int and error.code==0)):return
        sys.stderr.write('Root PR206 operations failed: '+type(error).__name__+'\n')
        raise SystemExit(1) from None
if __name__=='__main__':entry()
