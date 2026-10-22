"""Root single-invocation capture; no retries, no ref movement, no receipt promotion."""
import sys
if not (sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.safe_path and not sys.flags.optimize):
    raise RuntimeError('Ordinary Python -E -S -B -P required')
from pathlib import Path
import argparse,datetime,hashlib,json,os,re,stat,subprocess
D=Path(__file__).absolute().parent
A=D.parent
PY='/opt/homebrew/opt/python@3.14/bin/python3.14'
RUNNERS={
'lifecycle':('root_lifecycle_runner_01/run_lifecycle206_v3.py',11168,'8d0aed332228ce340d09105ff9e85126d4f26f42da8cc620ed8e19f409053ecc'),
'installer':('root_program_lock_installation_01/install_program_lock206_v4.py',5869,'0efd81e6b8e55335cdacefca4c44167a030806cf8013dbff040bc15dd359fe98'),
'operations':('root_publication_ops_runner_01/run_operations206_v5.py',5969,'7487d0c1c4ef8851fc6b35430aec197b90b4dfb1ad167547d2ac974254c5052b')}
def need(ok,msg):
    if type(ok) is not bool or not ok:raise RuntimeError(msg)
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def read(path,wanted):
    need(path.resolve(strict=True)==path and path.is_relative_to(A),'Canonical case input')
    s=path.lstat();need(stat.S_ISREG(s.st_mode) and stat.S_IMODE(s.st_mode)==0o444 and s.st_size<=2000000,'Bounded readonly regular case input')
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK|os.O_CLOEXEC)
    try:
        st=os.fstat(fd);need(stat.S_ISREG(st.st_mode) and st.st_size<=2000000,'Regular bounded opened input')
        with os.fdopen(fd,'rb',closefd=False) as f:raw=f.read(2000001)
    finally:os.close(fd)
    need(pin(raw)==wanted,'Exact capture source/authority input');return raw
def put(path,raw):
    fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o444)
    try:
        with os.fdopen(fd,'wb',closefd=False) as f:need(f.write(raw)==len(raw),'Short capture write');f.flush();os.fsync(fd)
    finally:os.close(fd)
    fd=os.open(path.parent,os.O_RDONLY)
    try:os.fsync(fd)
    finally:os.close(fd)
def enc(value):return (json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
class SafeParser(argparse.ArgumentParser):
    def error(self,message):raise RuntimeError('Invalid capture arguments')
def main():
    ap=SafeParser()
    ap.add_argument('mode',choices=RUNNERS)
    ap.add_argument('action')
    ap.add_argument('tag')
    ap.add_argument('--adoption-bytes',required=True,type=int)
    ap.add_argument('--adoption-sha256',required=True)
    ap.add_argument('--phase',choices=['ready','merge','factual','completion'])
    ap.add_argument('--generation')
    ap.add_argument('--ack-bytes',type=int)
    ap.add_argument('--ack-sha256')
    ap.add_argument('--confirm-id',type=int)
    args=ap.parse_args()
    need(re.fullmatch('[A-Za-z0-9_]{1,80}',args.tag) is not None,'Bounded capture tag')
    rel,size,sha=RUNNERS[args.mode];runner=A/rel;runner_pin={'bytes':size,'sha256':sha};read(runner,runner_pin)
    adoption_name='ROOT_PUBLICATION_OPERATIONS_ADOPTION_01.json' if args.mode=='operations' else 'ROOT_LIFECYCLE_SOURCE_ADOPTION_01.json'
    wanted={'bytes':args.adoption_bytes,'sha256':args.adoption_sha256};adopt=json.loads(read(A/adoption_name,wanted))
    need(adopt.get('evidence_scope')=='ACTUAL_ROOT_RECEIPT' and adopt.get('accepted_preparation_only') is True and adopt.get('PR')==206,'Actual Root capture authority')
    need(adopt['program_lock_installer_pin' if args.mode=='installer' else 'dispatcher_pin']==runner_pin,'Exact delegated reviewed source')
    read(Path(__file__).absolute(),adopt['capture_manager_pin'])
    argv=[PY,'-E','-S','-B','-P',str(runner)]
    if args.mode!='installer':argv+=['--adoption',adoption_name]
    argv+=['--adoption-bytes',str(args.adoption_bytes),'--adoption-sha256',args.adoption_sha256]
    if args.mode=='lifecycle':
        need(args.phase is not None and args.generation is not None and re.fullmatch('[A-Za-z0-9_]{1,80}',args.generation) is not None,'Explicit lifecycle phase/generation')
        need(args.action in ('preflight','bind','prepare','verify','accept','sync','pointer') and args.confirm_id is None,'Exact lifecycle action')
        argv += [args.phase,args.action,args.generation]
        if args.phase!='ready':
            need(args.ack_bytes is not None and args.ack_sha256 is not None,'Explicit actual metadata acknowledgement pin')
            argv+=['--ack-path','ROOT_PR_METADATA_ACKNOWLEDGEMENT_01.json','--ack-bytes',str(args.ack_bytes),'--ack-sha256',args.ack_sha256]
        else:need(args.ack_bytes is None and args.ack_sha256 is None,'No metadata acknowledgement at ready')
    elif args.mode=='operations':
        need(args.phase is None and args.generation is None and args.ack_bytes is None and args.ack_sha256 is None,'No lifecycle controls in operations')
        need(args.action in ('preflight','stage','inspect','publish','inspect-doi','finalize','append','recover'),'Exact operations action')
        argv += [args.action]
        if args.confirm_id is not None:
            need(args.action in ('inspect','publish','inspect-doi') and args.confirm_id>0,'Explicit known-ID phase only')
            argv += ['--confirm-id',str(args.confirm_id)]
    else:
        need(args.action=='install' and args.phase is None and args.generation is None and args.ack_bytes is None and args.ack_sha256 is None and args.confirm_id is None,'Exact installer action')
    records=D/'execution_records';records.mkdir(exist_ok=True)
    need(records.resolve(strict=True)==records and records.is_dir() and not records.is_symlink(),'Owned capture directory')
    base=records/(args.mode+'_'+args.tag)
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    put(Path(str(base)+'.INFLIGHT.json'),enc({'UTC':started,'argv':argv,'runner_pin':runner_pin,'adoption_pin':wanted,'scope':'One explicit child invocation, no automatic retries or ref movement; existence is not success.'}))
    try:
        r=subprocess.run(argv,cwd=A,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=600)
        stdout,stderr,code,outcome=r.stdout,r.stderr,r.returncode,'completed'
    except subprocess.TimeoutExpired as error:
        stdout,stderr,code,outcome=error.stdout or b'',error.stderr or b'',124,'timeout; inspect state, do not repeat mutation'
    put(Path(str(base)+'.stdout'),stdout);put(Path(str(base)+'.stderr'),stderr)
    result={'started_UTC':started,'ended_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'argv':argv,'exit_code':code,'outcome':outcome,'stdout':pin(stdout),'stderr':pin(stderr),'runner_pin':runner_pin,'adoption_pin':wanted,'capture_manager_pin':pin(Path(__file__).read_bytes()),'actual_phase_acceptance_or_publication_not_inferred_by_manager':True}
    put(Path(str(base)+'.RESULT.json'),enc(result))
    print(json.dumps(result,sort_keys=True))
    if code==0 and stdout:sys.stdout.write(stdout.decode('utf-8'))
    raise SystemExit(code)
def entry():
    try:main()
    except BaseException as error:
        if isinstance(error,SystemExit):
            if error.code is None:return
            if type(error.code) is int:raise SystemExit(error.code) from None
        sys.stderr.write('Root PR206 capture failed: '+type(error).__name__+'\n')
        raise SystemExit(1) from None
if __name__=='__main__':entry()

