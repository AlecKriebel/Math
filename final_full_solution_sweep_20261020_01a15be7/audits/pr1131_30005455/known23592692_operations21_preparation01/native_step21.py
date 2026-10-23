"""Inactive native controller21: one explicit action, fixed OUT, raw before parse.
No automatic next action, authority installation, alternate CASE or create.
"""
import sys
if sys.flags.optimize or not __debug__ or not(sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode):raise RuntimeError('Use Python -I -S -B optimize0')
from pathlib import Path
import argparse,datetime,hashlib,json,os,re,subprocess
E=Path(__file__).resolve().parent;P=E.parent;ENTRY=E/'entry21.py'
OUT=P/'root_actual21_known23592692_actions01'
CONTRACT=P/'known23592692_operations21_authority01/ROOT_EXECUTION_ADOPTION21.json'
ACTIONS=['stage-known','publish','verify-public','ledger'];ID=23592692
def need(v,m):
    if not v:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def can(v):return json.dumps(v,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()
def strict(b):
    def pairs(xs):
        out={}
        for k,v in xs:need(k not in out,'duplicate JSON key');out[k]=v
        return out
    return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda x:need(False,'nonfinite JSON'))
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def plain(p):
    p=Path(p);need(p.is_absolute()and not any(x.is_symlink()for x in[p,*p.parents]),'absolute no-symlink path');return p
def readpin(pin):
    p=plain(pin['path']);b=p.read_bytes();need(type(pin['bytes'])is int and len(b)==pin['bytes']and sha(b)==pin['sha256'],'complete ROOT-pinned input changed');return b
def evidence(wanted):
    need(re.fullmatch('[a-f0-9]{64}',wanted or''),'caller-pinned ROOT21 execution contract required')
    raw=plain(CONTRACT).read_bytes();need(sha(raw)==wanted,'ROOT21 execution adoption changed');g=strict(raw)
    need(g['native_controller21_sha256']==sha(Path(__file__).resolve().read_bytes()),'exact separately adopted native controller21')
    need(g['schema']=='ROOT-known23592692-execution21-1'and g['id']==ID and type(g['id'])is int,'fixed known21 contract')
    for key in['approved_for_actions','new_whole21_review_adopted','full_original_known_create_and_six_history_accepted','old_source19_20_joint_science_reused_unchanged','known_create_only','future_create_allowance_zero']:need(g[key]is True,'future ROOT21 action adoption missing '+key)
    need(g['source21_sha256']==sha((E/'source21/SOURCE_MANIFEST21.json').read_bytes())and g['entry21_sha256']==sha(ENTRY.read_bytes()),'exact new source/entry adoption')
    for key in['whole21_manifest','whole21_ROOT_adoption','ROOT_preparation_input_adoption']:readpin(g[key])
    t=datetime.datetime.now(datetime.timezone.utc)
    def utc(v):
        d=datetime.datetime.fromisoformat(v.replace('Z','+00:00'));need(d.tzinfo is not None and d.utcoffset()==datetime.timedelta(0),'UTC adoption');return d
    start=utc(g['not_before']);end=utc(g['expires_at']);need(start<=t<end and end-start<=datetime.timedelta(hours=2),'short future ROOT21 execution validity')
    need(type(g['allowed_actions'])is list and set(g['allowed_actions'])<=set(ACTIONS)and len(g['allowed_actions'])==len(set(g['allowed_actions'])),'explicit separate action roles')
    return g
def parsed_entry(g):
    raw=ENTRY.read_bytes();need(sha(raw)==g['entry21_sha256'],'entry changed before capture');n={'__file__':str(ENTRY),'__name__':'checked_native21_entry'};exec(compile(raw,str(ENTRY),'exec',dont_inherit=True,optimize=0),n)
    return n,raw
def cross_authorities(g,n,policy):
    rootraw=plain(n['AUTHORITY']).read_bytes();compatraw=plain(n['COMPAT20']).read_bytes()
    need(sha(rootraw)==g['ROOT21_sha256']and sha(compatraw)==g['compatibility20_authority_sha256'],'exact same ROOT21/compatibility buffers before cross-document parse')
    root=strict(rootraw);compat=strict(compatraw);review=g['whole21_manifest']['sha256']
    need(root['whole21_review_sha256']==compat['whole20_review_sha256']==review,'execution/ROOT21/compatibility20 must bind SAME complete new whole21 review')
    need(root['whole21_ROOT_adoption_sha256']==g['whole21_ROOT_adoption']['sha256'],'ROOT21 and execution must bind same ROOT whole21 adoption')
    need(root['ROOT_preparation_input_adoption_sha256']==g['ROOT_preparation_input_adoption']['sha256']==policy.data['ROOT_preparation_input_adoption']['sha256'],'execution/ROOT21/source21 must bind same exact preparation input adoption')
    need(can(g['ROOT_preparation_input_adoption'])==can(policy.data['ROOT_preparation_input_adoption']),'complete preparation-adoption pin path/size/SHA')
    need(g['ROOT19_sha256']==policy.data['ROOT19_sha256']and root['source21_sha256']==g['source21_sha256']and root['entry21_sha256']==compat['entry20_sha256']==g['entry21_sha256'],'full cross-document source/entry/base authority consistency')
def saved(path,raw):
    plain(path);need(path.parent==OUT and OUT.is_dir(),'fixed native21 OUT only');v=os.statvfs(OUT);need(v.f_bavail*v.f_frsize>=120*1024**2+len(raw)+16384,'native transport reserve')
    fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(fd,'wb')as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())
    fd=os.open(OUT,os.O_RDONLY)
    try:os.fsync(fd)
    finally:os.close(fd)
def record(path,value):saved(path,(json.dumps(value,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode())
def action(which,wanted):
    g=evidence(wanted);need(which in g['allowed_actions'],'this separate action not adopted');n,entry=parsed_entry(g)
    for path,key in[(n['AUTHORITY'],'ROOT21_sha256'),(n['COMPAT20'],'compatibility20_authority_sha256')]:need(sha(plain(path).read_bytes())==g[key],'separate authority changed')
    argv=[which,'--expected-pr-head',n['HEAD'],'--deposit-id',str(ID),'--clearance-sha256',g['ROOT19_sha256'],'--root21-clearance-sha256',g['ROOT21_sha256'],'--compat20-clearance-sha256',g['compatibility20_authority_sha256']]
    m,actual,policy,guard=n['prepare'](argv);cross_authorities(g,n,policy);m.bind_runtime();m.bind_state();need(guard.known(ID)==ID,'full first tagged known proof before child');policy.check()
    if which=='stage-known':m.state_exact(ID,absent=True)
    else:m.state_exact(ID)
    # Output allocation is after all read-only source/known-state preflight.
    plain(OUT)
    if OUT.exists():need(OUT.is_dir(),'fixed OUT is not a directory')
    else:OUT.mkdir(mode=0o700)
    index=ACTIONS.index(which)
    if index:
        previous=ACTIONS[index-1];exit=strict((OUT/(previous+'.exit.json')).read_bytes());parsed=strict((OUT/(previous+'.parsed.json')).read_bytes())
        need(exit['returncode']==0 and exit['complete_native_return']is True and sha((OUT/(previous+'.stdout.bin')).read_bytes())==exit['stdout']['sha256'],'previous separate native success missing')
        need(parsed.get('id',parsed.get('record'))==ID,'previous exact known target differs')
    marker=OUT/(which+'.intent.json');need(not marker.exists(),'consumed known21 native action; GET-only, never retry/alternate OUT')
    program='from pathlib import Path;import hashlib;p=Path('+repr(str(ENTRY))+');b=p.read_bytes();\nif hashlib.sha256(b).hexdigest()!='+repr(g['entry21_sha256'])+':raise RuntimeError("entry21 changed")\nn={"__file__":str(p),"__name__":"checked_actual_known21"};exec(compile(b,str(p),"exec",dont_inherit=True,optimize=0),n);n["main"]('+repr(argv)+')'
    command=[sys.executable,'-I','-S','-B','-c',program];binary=Path(sys.executable).resolve(strict=True);b=binary.read_bytes();interpreter={'path':sys.executable,'resolved_path':str(binary),'bytes':len(b),'sha256':sha(b),'at':now()}
    record(marker,{'at':now(),'action':which,'known_id':ID,'source21_sha256':g['source21_sha256'],'entry21_sha256':g['entry21_sha256'],'ROOT_execution_sha256':wanted,'argv':argv,'native_command':command,'interpreter':interpreter,'attempt_limit':1,'future_create_allowance':0,'rule':'Any interruption/unknown outcome consumes this marker; preserve first known ID/intents; GET-only reconcile; no new record, retry, alternate OUT or automatic next action.'})
    out=OUT/(which+'.stdout.bin');err=OUT/(which+'.stderr.bin');fd1=os.open(out,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600);fd2=os.open(err,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600);start=now();code=None;error=None;complete=False
    with os.fdopen(fd1,'wb')as stdout,os.fdopen(fd2,'wb')as stderr:
        try:r=subprocess.run(command,stdin=subprocess.DEVNULL,stdout=stdout,stderr=stderr,check=False);code=r.returncode;complete=True
        except BaseException as exc:error={'type':type(exc).__name__,'message':str(exc)}
        finally:stdout.flush();os.fsync(stdout.fileno());stderr.flush();os.fsync(stderr.fileno())
    ob=out.read_bytes();eb=err.read_bytes()
    record(OUT/(which+'.exit.json'),{'started_at':start,'finished_at':now(),'action':which,'native_command':command,'interpreter':interpreter,'returncode':code,'error':error,'complete_native_return':complete,'stdout':{'bytes':len(ob),'sha256':sha(ob)},'stderr':{'bytes':len(eb),'sha256':sha(eb)},'binary_saved_before_parse':True,'rule':'Unknown is not certification and may have effects; preserve all bytes and reconcile by GET only.'})
    need(complete and code==0,'native21 failed/unknown; preserve all raw streams and never retry')
    result=strict(ob);need(type(result)is dict and type(result.get('id',result.get('record')))is int and result.get('id',result.get('record'))==ID,'only exact known21 result')
    record(OUT/(which+'.parsed.json'),result);print(json.dumps({'action':which,'transport':str(OUT),'native_returncode':code,'known_id':ID,'automatic_next_action':False}))
def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);mode=parser.add_mutually_exclusive_group(required=True);mode.add_argument('--describe',action='store_true');mode.add_argument('--check-evidence',action='store_true');mode.add_argument('--action',choices=ACTIONS);parser.add_argument('--root-contract-sha256');args=parser.parse_args(argv)
    if args.describe:return print(json.dumps({'preparation_only':True,'known_id':ID,'future_create_allowance':0,'actions':ACTIONS,'entry':str(ENTRY),'fixed_OUT':str(OUT),'actual_effects':0}))
    if args.check_evidence:evidence(args.root_contract_sha256);return print(json.dumps({'evidence_only':True,'authority_installed':False,'action_executed':False}))
    return action(args.action,args.root_contract_sha256)
if __name__=='__main__':main()
