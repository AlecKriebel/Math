"""Own handwritten whole source read; never imports any scientific/prepared helper."""
from pathlib import Path, PurePosixPath
import json, hashlib, stat, subprocess, datetime, os
H=Path(__file__).resolve().parent; A=H.parent; R=A.parents[2]; C=A/'reviewed_candidate'
sha=lambda b:hashlib.sha256(b).hexdigest()
stamp=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
reads=[]; commands=[]
def require(ok,msg):
    if not ok:raise ValueError(msg)
def read(p):
    require(p.is_file() and not p.is_symlink(),'Regular source file')
    raw=p.read_bytes();reads.append({'path':p.relative_to(R).as_posix(),'bytes':len(raw),'sha256':sha(raw),'worktree_mode':stat.S_IMODE(p.stat().st_mode)})
    return raw
def load(p):return json.loads(read(p))
def git(*tail):
    argv=['git',*tail]; start=stamp();proc=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
    out,err=proc.communicate();i=len(commands);d=H/'READ_ONLY_GIT_STREAMS';d.mkdir(exist_ok=True)
    (d/(str(i)+'.stdout')).write_bytes(out);(d/(str(i)+'.stderr')).write_bytes(err)
    commands.append({'argv':argv,'cwd':str(R),'pid':proc.pid,'started_utc':start,'finished_utc':stamp(),'exit_code':proc.returncode,'stdout':{'path':str(i)+'.stdout','bytes':len(out),'sha256':sha(out)},'stderr':{'path':str(i)+'.stderr','bytes':len(err),'sha256':sha(err)}})
    require(proc.returncode==0,'Read-only Git failed');return out
require(git('branch','--show-current').strip()==b'main','Staymain')
head=git('rev-parse','HEAD').decode().strip()
raw=read(C/'MANIFEST.json');require(sha(raw)=='4849e6037a5db3dce546a656dcd57063ae83d782c19e24d4e3dff97ebbcdec14','Current exact manifest')
mf=json.loads(raw);require(mf['files_count']==len(mf['files'])==347 and mf['self_excluded']==['MANIFEST.json'],'347+self')
for z in mf['files']:
    p=C/z['path'];raw=read(p);require(len(raw)==z['bytes'] and sha(raw)==z['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444,'Complete frozen current member')
require(stat.S_IMODE((C/'MANIFEST.json').stat().st_mode)==0o444,'Frozen literal self')
deps=load(C/'CURRENT_DEPENDENCIES.json');require(len(deps['files'])==274,'274 deps')
for z in deps['files']:
    raw=read(A/z['path']);require(len(raw)==z['bytes'] and sha(raw)==z['sha256'],'Entire dependency')
original=load(A/'snapshot_manifest.json');require(len(original['files'])==16 and len(original['changed_paths'])==17 and original['diff_bytes']==54344,'Original16/17 diff')
for z in original['files']:
    raw=read(A/'source_snapshot'/z['path']);require(len(raw)==z['size'] and sha(raw)==z['sha256'] and raw==read(C/'original_archive'/z['path']),'Whole original/archive')
require(read(C/'turns.jsonl')==b'','Literal zero-byte original ledger')
whole=load(A/'whole_current_source_first_family/SELF_MANIFEST.json');require(whole['files_count']==len(whole['files'])==30 and whole['self_excluded']==['SELF_MANIFEST.json'],'Whole30+self')
for z in whole['files']:
    p=A/'whole_current_source_first_family'/z['path'];raw=read(p);require(len(raw)==z['bytes'] and sha(raw)==z['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444,'Whole authored body')
foreign=whole['external_individually_excluded_inputs'];require(len(foreign)==756,'756 individual inputs')
dated={'draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'}
checked=set()
for z in foreign:
    p=Path(z['path']);require(p.is_absolute() and p.resolve().is_relative_to(R),'Repository foreign source')
    n=p.resolve().relative_to(R).as_posix()
    if n in dated:
        raw=git('show','c61dc0cb572de281b871264819c8b80d647d0373:'+n);checked.add(n)
    else:raw=read(p)
    require(type(z['bytes']) is int and len(raw)==z['bytes'] and sha(raw)==z['sha256'],'Entire individually foreign body')
require(checked==dated,'Exactly4 historical native identities')
for n in ['ROOT_CURRENT_PARTIAL_SCOPE_CERTIFICATE.md','ROOT_WHOLE_CURRENT_REVIEW.json','ROOT_PRIMARY_READ_LEDGER.json','ROOT_SCIENCE_CARD.json','capture_root_final_operation.py']:
    read(A/n)
require(git('rev-parse','HEAD').decode().strip()==head,'No head transition during own source read')
record={'schema':'pr43-source-only-whole-read/v1','created_utc':stamp(),'actual_child_pid':os.getpid(),'status':'PASS','files_read':reads,'read_only_git_commands':commands,'current_members':347,'current_dependencies':274,'original_files':16,'whole_owned_members':30,'individual_foreign_inputs':756,'dated_native4':sorted(dated),'native_source_head':'c61dc0cb572de281b871264819c8b80d647d0373','main_observed':head,'proposed_helpers_imported_compiled_executed':False,'ROOT_approval_authored':False,'future_PR42_predecessor_certified':False,'new_substantive_attempts':0,'audit_turns':0}
(H/'SOURCE_INPUT_READS.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:v for k,v in record.items() if k not in {'files_read','read_only_git_commands'}}))
