"""UNEXECUTED SOURCE preparation: ROOT reads, copies unchanged adjacent to A48, then runs.
No proposed helper imports or scientific execution. Only allowlisted readonly Git
children and absent-only adjacent ROOT administrative outputs run under ROOT.
The explicit reading argument attests only the specified complete source/control
and final SOURCE-review readings; earlier mathematical readings use their precise
existing ROOT ledgers. Automatically hashed external bodies are not personal reads.
"""
from pathlib import Path, PurePosixPath
import datetime as dt, hashlib, json, math, os, re, stat, subprocess, sys
A=Path(__file__).absolute().parent;R=A.parents[2]
H=A/'acceptance_preparation_family_v3';F=A/'acceptance_source_adversary_family_v3_fresh'
W=A/'current_whole_adversary_family';C=A/'reviewed_candidate'
PROGRAM=R/'draft_pr_publication_program_20260930'
B=A.parent/'pr45_9900007';P47=A.parent/'pr47_2849';H47=P47/'acceptance_preparation_family'
PREP='9c525f7b540068af07477e8f794e21596d93e69e49e8dbc52972d3196eb9fda4'
PREP47='1a10442d9962db99c608412f53fef754870bfadf24fd76e7e899112fc38ebef1'
CURRENT='3f8d6b38fcd0268df5a32fc006c5a759b2dd61f225f2fa2fa959861a9bcb115f'
WHOLE='060aac8a645879155b1f3ae0a8026a201c0e63303ca24b6bd7b1374046ac30c8'
OPERATOR='bf58fa04ca027d240e8362cd77bf6024e6d4894c6e43b8f11f5a7f331e4efb65'
ROOT47='89924d5de705c8465ab75f872201b1b8a004c4ebc3c092f3c95bfc17f97777ab'
# Genuine ROOT fresh V3 adversary closure7036 and separate readonly7597.
FM='b9ee93f62a8e1219c9f045a69819bf14244d0cf7e428cdc449128222aa1b5c68';SOURCE_FILES=48
SOURCE_REPORT='9c595a8c7c918cb645c22a4070ee787a1aa4a3f4356c94a89c33a70e2a87d782'
SOURCE_VERDICT='de4f397ce5489fe0ef8b33c6dbd12fd0bbcce521c07b68aea32e13a507145687'
ROOT_CAPS=[
 ('root_pr48_source_v3_closure_actual_capture','7b4533c58b2b23ec7b2320f825e66a1a2810899b423ea79de3b585bac6749090',0),
 ('root_pr48_source_v3_closed_readback_actual_capture','c86821a0c49f270c12d8a012b40ccfb9bb1f0f7b5e9fade56312baa53e82c1e9',0),
 ('root_pr48_source_v3_fresh_review_closure_actual_capture','7ebf48485fc33e4ecad69bef21635facf0bfdb6097af2e0f2f3f15ec939f7f7d',0),
 ('root_pr48_source_v3_fresh_review_closed_readback_actual_capture','3bdb66c375693ec2fb743c19f3d2a04270346e88be7e23475239dc64b911f50e',0)]
MUTABLE4={'draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'}
def need(v,s):
    if not v:raise ValueError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def raw(p):need(p.is_file() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents),'Regular nonsymlink file');return p.read_bytes()
def load(p):
    def pairs(items):
        d={}
        for k,v in items:need(k not in d,'Duplicate JSON key');d[k]=v
        return d
    def floating(s):v=float(s);need(math.isfinite(v),'Nonfinite JSON');return v
    return json.loads(raw(p),object_pairs_hook=pairs,parse_float=floating,parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)))
def eq(a,b):return type(a) is type(b) and (a.keys()==b.keys() and all(eq(a[k],b[k]) for k in a) if type(a) is dict else len(a)==len(b) and all(eq(x,y) for x,y in zip(a,b)) if type(a) is list else a==b)
def safe(n):
    need(type(n) is str and n and n!='.' and '\\' not in n and '\0' not in n,'Literal path');p=PurePosixPath(n);need(not p.is_absolute() and p.as_posix()==n and not {'.','..','.git','__pycache__'}&set(p.parts),'Canonical repository member');return n
def ref(p,mode=False):
    b=raw(p);o=dict(path=safe(p.relative_to(R).as_posix()),bytes=len(b),sha256=sha(b))
    if mode:o['full_mode']=stat.S_IMODE(p.stat().st_mode)
    return o
def check(z,mode=False):
    need(type(z) is dict and set(z)==({'path','bytes','sha256','full_mode'} if mode else {'path','bytes','sha256'}),'Strict reference keyset');safe(z['path']);need(type(z['bytes']) is int and z['bytes']>=0 and type(z['sha256']) is str and re.fullmatch('[0-9a-f]{64}',z['sha256']),'Typed length/SHA')
    if mode:need(type(z['full_mode']) is int and 0<=z['full_mode']<=0o7777,'Full mode integer')
    need(eq(ref(R/z['path'],mode),z),'Entire bound body/full mode changed');return z
def triple(z):return {k:z[k] for k in ('path','bytes','sha256')}
def clock(s):need(type(s) is str and s==s.strip(),'UTC string');v=dt.datetime.fromisoformat(s[:-1]+'+00:00' if s.endswith('Z') else s);need(v.utcoffset()==dt.timedelta(0),'Aware UTC');return v
def closure(d,n,pin,count):
    need(sha(raw(d/n))==pin,'Exact closed manifest pin');m=load(d/n);need(m['self_excluded']==[n] and type(m['files_count']) is int and m['files_count']==len(m['files'])==count,'Exact self-only count');names=set();out=[]
    for z in m['files']:
        need((set(z)=={'path','bytes','sha256'} or (set(z)=={'path','bytes','sha256','full_mode'} and z['full_mode']=='0444')) and z['path'] not in names,'Unique exact member, preserving WHOLE string0444');safe(z['path']);names.add(z['path']);check(dict(triple(z),path=d.relative_to(R).as_posix()+'/'+z['path']));out.append(ref(d/z['path'],True))
    files=set();dirs=set()
    for p in d.rglob('*'):
        need(not p.is_symlink(),'No symlink');x=safe(p.relative_to(d).as_posix())
        if p.is_file():files.add(x);need(stat.S_IMODE(p.stat().st_mode)==0o444,'Full0444 including special bits')
        else:need(p.is_dir(),'No special member');dirs.add(x)
    need(files==names|{n} and dirs=={p.as_posix() for x in files for p in PurePosixPath(x).parents if p.as_posix()!='.'},'Entire recursive topology')
    if 'directories' in m:need(type(m['directories']) is list and len(m['directories'])==len(dirs) and set(m['directories'])==dirs,'Entire declared directories')
    return m,out

def captured(p,expected=0):
    c=load(p);d=p.parent;need(type(c['exit_code']) is int and c['exit_code']==expected and clock(c['started_utc'])<=clock(c['finished_utc'])<=clock(now()),'Actual typed exit and aware clocks')
    need(c['actual_execution'] is True and c['completed'] is True and c['stdin_supplied'] is False and type(c['pid']) is int and c['pid']>0 and c['operator_unchanged'] is True,'Actual completed child, not proposed execution')
    need(type(c['argv']) is list and c['argv'] and all(type(x) is str for x in c['argv']) and c['cwd']==str(R),'Literal argv and repository cwd');members={x.name for x in d.iterdir()};need(all(x.is_file() and not x.is_symlink() for x in d.iterdir()),'Only regular capture members')
    for k in ['stdout','stderr']:
        z=c[k];need(set(z)=={'path','bytes','sha256'} and z['path']==k+'.bin' and type(z['bytes']) is int and z['bytes']>=0 and type(z['sha256']) is str and re.fullmatch('[0-9a-f]{64}',z['sha256']),'Typed entire channel');b=raw(d/z['path']);need(len(b)==z['bytes'] and sha(b)==z['sha256'],'Whole stdout/stderr')
    if 'PRELAUNCH_SOURCE.py' in members:
        need(type(c['operator_pid']) is int and c['operator_pid']>0 and c['source_unchanged'] is True and sha(raw(d/'PRELAUNCH_SOURCE.py'))==c['source_sha256'] and sha(raw(d/'PRELAUNCH_OPERATOR.py'))==c['operator_sha256'],'Whole real source/operator')
        if 'PRELAUNCH.json' in members:
            need(members=={'CAPTURE.json','PRELAUNCH.json','PRELAUNCH_SOURCE.py','PRELAUNCH_OPERATOR.py','stdout.bin','stderr.bin'},'Exact CAP6');pre=load(d/'PRELAUNCH.json');need(all(eq(c[k],v) for k,v in pre.items() if k!='schema'),'Entire original prelaunch')
        else:need(members=={'CAPTURE.json','PRELAUNCH_SOURCE.py','PRELAUNCH_OPERATOR.py','stdout.bin','stderr.bin'} and c['schema']=='pr48-v3-fresh-adversary-actual-private-capture/v1','Exact independent SOURCE private CAP5')
    else:need(members=={'CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin'} and c['schema']=='root-explicit-command-capture/v1' and sha(raw(d/'prelaunch_operator.py'))==c['operator_sha256'],'Exact ROOT CAP4')
    if expected==0:need(raw(d/'stderr.bin')==b'','Whole successful stderr')
    return dict(capture=ref(p),complete_capture=c,complete_members=[ref(x,True) for x in sorted(d.iterdir())])

PINNAMES=['preparation_manifest_sha256','final_plan','final_plan_sha256','final_receipt','final_receipt_sha256','final_manifest','final_manifest_sha256','reconciliation_capture','reconciliation_capture_sha256','previous_mirror','previous_mirror_sha256','previous_post','previous_post_sha256','fresh_preimage','fresh_preimage_sha256','root_bindings','root_bindings_sha256']
def predecessor(inputs):
    m=load(P47/'state_mirror_bindings.json');post=load(P47/'post_acceptance_verification.json');rp=load(P47/'ROOT_ACTUAL_POST_INSPECTION.json');contract=load(H47/'ROOT_POST_CONTRACT.json');closure(H47,'PREPARATION_MANIFEST.json',PREP47,126)
    need(sha(raw(P47/'ROOT_ACTUAL_POST_INSPECTION.json'))==ROOT47,'Actual completed ROOT47 post pin')
    need(contract['schema']=='pr47-future-ROOT-whole-post-contract/v1' and contract['source_only'] is True and contract['future_ROOT_post_completed'] is False and len(contract['future47_required_ROOT_complete_keyset'])==22 and set(rp)==set(contract['future47_required_ROOT_complete_keyset']),'Closed contract remains SOURCE; actual entire22 required')
    need(rp['schema']==contract['future47_required_ROOT_schema'] and all(eq(rp[k],v) for k,v in contract['future47_required_completed_values'].items()) and eq(rp['entire_post'],post),'Every typed completed ROOT47 value and entire actual post')
    expected={**contract['future47_required_entire_post_values'],**{k:post[k] for k in PINNAMES},'utc':post['utc'],'merge_commit':post['merge_commit'],'merge_tree':post['merge_tree'],'actual_remote_state':'MERGED'}
    need(eq(post,expected) and post['preparation_manifest_sha256']==PREP47 and clock(post['utc'])<=clock(rp['utc'])<=clock(now()),'Entire typed actual47 post and completed chronology')
    for n in ['final_plan','final_receipt','final_manifest','reconciliation_capture','previous_mirror','previous_post','fresh_preimage','root_bindings']:safe(post[n]);need(type(post[n+'_sha256']) is str and re.fullmatch('[0-9a-f]{64}',post[n+'_sha256']) and sha(raw(R/post[n]))==post[n+'_sha256'],'Every original actual47 final pin')
    for n,p in [('previous_mirror',P47/'state_mirror_bindings.json'),('previous_post',P47/'post_acceptance_verification.json'),('previous_root_post',P47/'ROOT_ACTUAL_POST_INSPECTION.json')]:check(inputs[n],True);need(eq(triple(inputs[n]),ref(p)),'SOURCE exact genuine actual47 predecessor identity')
    need(type(m['entries']) is list and len(m['entries'])==37 and all(type(z['pr']) is int for z in m['entries']) and sorted(z['pr'] for z in m['entries'])==m['required_completed_prs'] and len(set(m['required_completed_prs']))==37 and 46 in m['required_completed_prs'] and 47 in m['required_completed_prs'] and 48 not in m['required_completed_prs'] and type(m['duplicate_mirrors']) is list and len(m['duplicate_mirrors'])==1,'Actual ordered46 then47,37 primaries and existing one duplicate')
    phases=['preflight','overlay','prepush','finalize','mirror','post'];need(type(rp['all_six_real_phase_captures']) is list and len(rp['all_six_real_phase_captures'])==6,'Exactly six genuine phase captures');caps=[];end=None
    for phase,z in zip(phases,rp['all_six_real_phase_captures']):
        check(z);p=P47/('root_'+phase+'_actual_capture')/'CAPTURE.json';need(z['path']==p.relative_to(R).as_posix(),'Exact phase identity');row=captured(p);c=row['complete_capture'];name={'mirror':'state_mirror_reconciliation.py','post':'verify_post_acceptance.py'}.get(phase,'integrate_reviewed_partial.py')
        need(c['schema']=='ROOT_actual_reviewed_acceptance_phase_capture_v1' and c['phase']==phase and c['argv'][:3]==['/usr/bin/python3','-B',str(H47/name)] and c['source_sha256']==sha(raw(H47/name)) and c['operator_sha256']==sha(raw(P47/'run_actual_acceptance_phases.py')),'Literal actual47 phase source/operator/argv')
        need((end is None or end<=clock(c['started_utc'])) and clock(c['finished_utc'])<=clock(rp['utc']),'Phase order and post-exit ROOT read')
        for n in PINNAMES:flag='--'+n.replace('_','-');need(c['argv'].count(flag)==1 and c['argv'][c['argv'].index(flag)+1]==post[n],'Every actual47 phase argv pin')
        end=clock(c['finished_utc']);caps.append(row)
    frozen=load(H/'ACTUAL47_PREDECESSOR_BINDINGS.json');need(eq(frozen['entire_ROOT22_post'],rp),'SOURCE binds entire genuine ROOT47 post')
    p=P47/'root_complete_actual_post_inspection_capture/CAPTURE.json';need(sha(raw(p))=='8df3d6fcf7cc57697096cefca0cd5b838501c69f527cf2f5e539baa63f0c7143','Literal ROOT74925 complete-post capture');rootcap=captured(p);cc=rootcap['complete_capture'];need(cc['pid']==74925 and clock(cc['started_utc'])<=clock(rp['utc'])<=clock(cc['finished_utc']),'ROOT post authoring during real child, never readiness transfer')
    need(eq(rootcap,frozen['complete_actual_ROOT_post_capture']),'Entire actual ROOT47 CAP4 and all members match frozen SOURCE')
    check(frozen['original47_post_operator_source'],True)
    need(type(rp['current13']) is list and len(rp['current13'])==13 and {z['path'] for z in rp['current13']}=={z['path'] for z in inputs['dated_native13']},'Historical exact13 identity domain')
    for z in rp['current13']:
        need(set(z)=={'path','bytes','sha256','worktree_mode'} and type(z['worktree_mode']) is int and 0<=z['worktree_mode']<=0o7777 and type(z['bytes']) is int and z['bytes']>=0,'Typed historical native13 row');safe(z['path'])
        if z['path'] not in MUTABLE4:check(dict(triple(z),full_mode=z['worktree_mode']),True)
    plan=load(P47/'state_mirror_plan.json');intent=load(P47/'state_mirror_intent.json');current=load(R/'unsolved_math_prioritization/state.json')
    need(eq(current,plan['state_after']) and len(current)==38 and all(type(v['turns_used']) is int for v in current.values()) and sum(v['turns_used'] for v in current.values())==45 and raw(R/'unsolved_math_prioritization/history.jsonl')==(intent['before_history_bytes']+plan['history_append_bytes']).encode(),'Whole actual47 state/history baseline38targets45turns37primary')
    return m,post,rp,caps,rootcap

def encode(o):return (json.dumps(o,indent=2,sort_keys=True,ensure_ascii=False,allow_nan=False)+'\n').encode()
def exclusive(p,b):
    need(not p.exists() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents),'Absent regular ROOT administrative output')
    with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
    need(stat.S_IMODE(p.stat().st_mode)==0o644,'Exact new full0644 under explicit0022 umask')
def put(p,b):need(p.parent==A,'Adjacent ROOT record only');exclusive(p,b)

def fresh_runtime(inputs):
    native=sorted(z['path'] for z in inputs['dated_native13']);need(len(native)==13 and len(set(native))==13,'Exactly13 native paths');native_before=[dict(triple(ref(R/n)),worktree_mode=ref(R/n,True)['full_mode']) for n in native]
    queue=raw(R/'unsolved_math_prioritization/QUEUE.md').decode().splitlines();header=['Rank','ID / code','Problem','EV','Impact (/10)','Difficulty','Proposed','Status','Turns','Chat','Findings','DOI'];heads=[s for s in queue if s.startswith('| Rank | ID / code |')];need(len(heads)==1 and [x.strip() for x in heads[0].split('|')[1:-1]]==header,'Exact fresh twelve-column QUEUE header')
    rows=[s.split('|')[1:-1] for s in queue if len(s.split('|'))==14];selected=[z for z in rows if z[1].strip()=='2961 / KP-4.85'];need(len(selected)==1 and selected[0][7].strip()=='queued' and selected[0][8].strip()=='0/5' and not any(z[1].strip().startswith('30004403 / ') for z in rows),'Fresh primary queued0/5 and related alias absent; unrelated current rows retained')
    root=A/'root_acceptance_author_readonly_inputs';need(not root.exists() and not root.is_symlink(),'Exclusive runtime readonly capture family');root.mkdir();exclusive(root/'PRELAUNCH_OPERATOR.py',raw(Path(__file__)));queries=[]
    def git(*args):
        allowed=[('branch','--show-current'),('rev-parse','HEAD'),('diff','--no-ext-diff','--no-textconv','--cached','--name-only','-z'),('diff','--no-ext-diff','--no-textconv','--name-only','-z')]
        dynamic=(len(args)==5 and args[:4] in [('ls-tree','-z','HEAD','--'),('ls-files','--stage','-z','--')]) or (len(args)==3 and args[:2]==('show','--no-textconv') and (args[2].startswith('HEAD:') or args[2].startswith(':')))
        need(args in allowed or dynamic,'Readonly Git argv whitelist')
        if dynamic:safe(args[-1].split(':',1)[1] if args[0]=='show' else args[-1])
        argv=['git',*args];started=now();d=root/('%03d'%len(queries));d.mkdir();pre=dict(schema='pr48-root-author-readonly-Git-prelaunch/v1',argv=argv,cwd=str(R),started_utc=started,actual_operator_pid=os.getpid(),source=None,stdin_supplied=False);exclusive(d/'PRELAUNCH.json',encode(pre))
        child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        try:out,err=child.communicate(timeout=60)
        except BaseException:child.kill();out,err=child.communicate();exclusive(d/'stdout.bin',out);exclusive(d/'stderr.bin',err);raise
        exclusive(d/'stdout.bin',out);exclusive(d/'stderr.bin',err);cap=dict(pre,schema='pr48-root-author-readonly-Git-capture/v1',actual_execution=True,pid=child.pid,completed=True,exit_code=child.returncode,finished_utc=now(),source_unchanged=None,operator_sha256=sha(raw(Path(__file__))),operator_unchanged=raw(Path(__file__))==raw(root/'PRELAUNCH_OPERATOR.py'),stdout=ref(d/'stdout.bin'),stderr=ref(d/'stderr.bin'))
        exclusive(d/'CAPTURE.json',encode(cap));queries.append(dict(capture=ref(d/'CAPTURE.json'),complete_capture=cap,complete_members=[ref(p,True) for p in sorted(d.iterdir())]));need(child.returncode==0 and err==b'' and cap['operator_unchanged'] is True,'Complete successful readonly Git child');return out
    def owned(n):safe(n);return n in native or n==(PROGRAM/'RESEARCH_LOG.md').relative_to(R).as_posix() or n.startswith('unsolved_math_prioritization/attempts/2961/') or n.startswith(A.relative_to(R).as_posix()+'/')
    def names(b):need(not b or b.endswith(b'\0'),'Complete NUL-delimited Git paths');return [safe(x.decode()) for x in b.split(b'\0') if x]
    need(git('branch','--show-current')==b'main\n','Current main only');head=git('rev-parse','HEAD').decode().strip();need(re.fullmatch('[0-9a-f]{40}',head),'Actual current main SHA');need(git('diff','--no-ext-diff','--no-textconv','--cached','--name-only','-z')==b'','Strict clean index before approval')
    paths=sorted(names(git('diff','--no-ext-diff','--no-textconv','--name-only','-z')));need(len(paths)==len(set(paths)) and not any(owned(n) for n in paths),'Every dirty owned path must be checkpointed before fresh foreign capture; no broad exemption')
    foreign=[]
    for n in paths:
        headentry=git('ls-tree','-z','HEAD','--',n);indexentry=git('ls-files','--stage','-z','--',n);need(headentry.endswith(b'\0') and headentry.count(b'\0')==1 and indexentry.endswith(b'\0') and indexentry.count(b'\0')==1,'One exact regular HEAD/index entry');fields,literal=headentry[:-1].decode().split('\t');mode,kind,blob=fields.split();need(literal==n and kind=='blob' and mode in {'100644','100755'} and indexentry[:-1].decode()==mode+' '+blob+' 0\t'+n,'No stage, HEAD/index mode/object change')
        hb=git('show','--no-textconv','HEAD:'+n);ib=git('show','--no-textconv',':'+n);need(hb==ib,'Entire protected HEAD/index body equality');row=dict(triple(ref(R/n)),worktree_mode=ref(R/n,True)['full_mode'],head_sha256=sha(hb),head_entry=headentry[:-1].decode(),index_entry=indexentry[:-1].decode());foreign.append(row)
    ownedlogs=[]
    for p in [A/'ROOT_RESEARCH_LOG.md',PROGRAM/'RESEARCH_LOG.md']:
        need(not p.is_symlink() and all(not q.is_symlink() for q in p.parents),'Exact regular owned log path');ownedlogs.append(dict(path=p.relative_to(R).as_posix(),present=p.exists(),preimage=ref(p,True) if p.exists() else None))
    freshclock=now();fresh=dict(schema='pr48-root-fresh-acceptance-input-preimages/v1',approved_by_root=True,created_utc=freshclock,reason_date_utc=clock(freshclock).date().isoformat(),reason='ROOT reconciles genuine completed PR46 then PR47 and closed PR48 V3 source against the actual current main and all thirteen native bodies and full modes; historical native observations do not authorize this fresh epoch.',current_head=head,files=native_before,protected_foreign_tracked_paths=paths)
    def check_current():
        need(git('branch','--show-current')==b'main\n' and git('rev-parse','HEAD').decode().strip()==head and git('diff','--no-ext-diff','--no-textconv','--cached','--name-only','-z')==b'' and sorted(names(git('diff','--no-ext-diff','--no-textconv','--name-only','-z')))==paths,'Fresh main/index/all tracked dirty identities preserved')
        need(eq(native_before,[dict(triple(ref(R/n)),worktree_mode=ref(R/n,True)['full_mode']) for n in native]),'All13 full bodies and permission bits preserved')
        for z in foreign:
            check(dict(triple(z),full_mode=z['worktree_mode']),True);n=z['path'];need(git('ls-tree','-z','HEAD','--',n).decode().rstrip('\0')==z['head_entry'] and git('ls-files','--stage','-z','--',n).decode().rstrip('\0')==z['index_entry'] and sha(git('show','--no-textconv','HEAD:'+n))==sha(git('show','--no-textconv',':'+n))==z['head_sha256'],'Every entire foreign HEAD/index/body/full mode remains exact')
        for z in ownedlogs:
            p=R/z['path'];need(p.exists() is z['present'] and not p.is_symlink(),'Owned log exact presence preserved')
            if z['present']:check(z['preimage'],True)
    check_current();return fresh,foreign,ownedlogs,queries,check_current,root

def main():
    need(__debug__ and sys.flags.optimize==0 and sys.argv==[sys.argv[0],'--personally-read-complete-source'],'Explicit ROOT scoped source/control and final SOURCE report attestation required')
    need(A.name=='pr48_2961' and raw(Path(__file__))==raw(A/'root_acceptance_author_preparation/author_ROOT_acceptance.py'),'ROOT must copy exact prepared SOURCE adjacent; preparation path is not executable authority')
    outputs=['capture_root_final_operation.py','ROOT_SOURCE_ACCEPTANCE_REVIEW.json','ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS.json','ROOT_FINAL_PLAN.json','ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES.json'];need(all(not (A/n).exists() and not (A/n).is_symlink() for n in outputs),'Never replace any existing ROOT approval/fresh record')
    prep,prepared=closure(H,'PREPARATION_MANIFEST.json',PREP,53);fm,owned=closure(F,'SELF_MANIFEST.json',FM,SOURCE_FILES)
    need(set(prep)=={'schema','status','utc','self_excluded','files_count','files','source_only','proposed_helpers_imported_compiled_executed','future_acceptance_or_ROOT_approval_claimed'} and prep['schema']=='pr48-acceptance-source-closure/v3' and prep['status']=='CLOSED_SOURCE_ONLY' and prep['source_only'] is True and prep['proposed_helpers_imported_compiled_executed'] is False and prep['future_acceptance_or_ROOT_approval_claimed'] is False,'Exact closed V3 nine-key SOURCE schema')
    need(set(fm)=={'schema','status','utc','self_excluded','files_count','files','production_imported_compiled_executed','future_acceptance_approved'} and fm['schema']=='pr48-fresh-V3-SOURCE-adversary-self-closure/v1' and fm['status']=='CLOSED_SOURCE_ONLY' and fm['production_imported_compiled_executed'] is False and fm['future_acceptance_approved'] is False,'Exact different fresh V3 SOURCE closure')
    need(sha(raw(F/'REPORT.md'))==SOURCE_REPORT and sha(raw(F/'VERDICT.json'))==SOURCE_VERDICT,'Whole exact fresh clean report/verdict pins');v=load(F/'VERDICT.json')
    need(v['schema']=='pr48-acceptance-source-adversary-verdict/v1' and v['verdict']=='PASS_SOURCE_ONLY_SCOPED' and v['preparation_manifest_sha256']==PREP and v['mandatory_corrections']==[] and v['production_imported_compiled_executed'] is False and v['future_acceptance_approved'] is False and v['previous_PASS_transferred'] is False and v['reviewer_prepared_this_acceptance_SOURCE'] is False,'Fresh independent SOURCE verdict only')
    external=load(F/'INPUT_BINDINGS.json');rr=external['normalized_complete_external_input_bindings'];need(external['schema']=='pr48-v3-fresh-source-complete-input-bindings/v1' and external['preparation_manifest_sha256']==PREP and external['dated_native13_and_four_historical_rows_not_live_pins'] is True and external['production_imported_compiled_executed'] is False and external['future_acceptance_approved'] is False and type(rr) is list and len(rr)==4386 and len({z['path'] for z in rr})==4386,'Complete unique fixed SOURCE union and explicit dated native qualifications')
    for z in rr:check(z,True)
    inputs=load(H/'INPUT_BINDINGS.json');need(inputs['actual_predecessor_PR47_completed'] is True and inputs['whole_binding_completed'] is True and inputs['future_native13_and_main_required'] is True and inputs['actual_predecessor_PR47_native4_dated_not_future_authority'] is True and len(inputs['external_input_rows'])==inputs['external_input_count']==3912,'Bound actual47, fixed3912 and fresh-authority distinction')
    for z in inputs['external_input_rows']:check(z,True)
    previous,post,rp,previouscaps,root47cap=predecessor(inputs);current,_=closure(C,'MANIFEST.json',CURRENT,1946);whole,_=closure(W,'MANIFEST.json',WHOLE,162)
    for p,n in [(C/'CURRENT_DEPENDENCIES.json','EXPECTED_CURRENT_DEPENDENCIES.json'),(W/'MANIFEST.json','EXPECTED_WHOLE_MANIFEST.json'),(W/'VERDICT.json','EXPECTED_WHOLE_VERDICT.json'),(A/'ROOT_WHOLE_CURRENT_REVIEW.json','EXPECTED_ROOT_WHOLE_REVIEW.json'),(A/'ROOT_PRIMARY_READ_LEDGER.json','EXPECTED_PRIMARY_READ_LEDGER.json'),(A/'ROOT_SCIENCE_CARD.json','EXPECTED_SCIENCE_CARD.json'),(A/'root_original_actual_reproduction_v2/ROOT_REPRODUCTION_RESULT.json','EXPECTED_ORIGINAL_CAPTURE_RESULT.json')]:need(eq(load(p),load(H/n)),'Whole fixed typed current/WHOLE/actual ROOT/source record differs')
    ledger=load(A/'ROOT_PRIMARY_READ_LEDGER.json');card=load(A/'ROOT_SCIENCE_CARD.json');rootwhole=load(A/'ROOT_WHOLE_CURRENT_REVIEW.json');need(ledger['reading_completed'] is True and ledger['approved_by_root'] is True and len(ledger['root_flags'])==8 and all(v is True for v in ledger['root_flags'].values()) and card['approved_by_root'] is True and rootwhole['personal_report_and_verdict_fully_read'] is True and rootwhole['actual_readback_pid']==30858 and rootwhole['future_acceptance_approved'] is False,'Precise existing ROOT scientific/read ledgers support their recorded scope, no new reproving claim')
    science=load(H/'SCIENTIFIC_SCOPE.json');plan=load(H/'DRAFT_FINAL_PLAN.json');need(eq(plan['scientific_scope'],science) and science['literal_target_status']=='unsolved' and type(science['problem_id']) is int and science['problem_id']==2961 and type(science['related_problem_id']) is int and science['related_problem_id']==30004403 and science['duplicate_shared_budget'] is True and science['original_substantive_attempts']==2 and science['turn_limit']==5 and science['new_substantive_attempts']==science['audit_turns']==0 and science['partial_valid'] is True and science['included_subgroup_only'] is True and science['all_powers_on_included_subgroup'] is True and science['signed_averaging_finite_integrability_required'] is True and science['arbitrary_ambient_bound_claimed'] is False and science['full_problem_solved'] is False and science['novelty_claimed'] is False and science['related_alias_QUEUE_row_absent_preserved'] is True and science['related_alias_native_entry_added'] is False and science['paper_or_new_doi_or_tracker'] is False,'Entire UNSOLVED shared original2/5 science and primary-only alias representation')
    own=[captured(p) for p in sorted(H.rglob('CAPTURE.json'))];need(len(own)==2,'Exactly two V3 preparer private captures');review=[captured(p,1 if p.parent.name=='fixed_custody_actual_capture' else 0) for p in sorted(F.rglob('CAPTURE.json'))];need(len(review)==4 and sum(z['complete_capture']['exit_code']==1 for z in review)==1,'Complete independent SOURCE private captures including retained failed584')
    rootcaps=[]
    for n,pin,exit_code in ROOT_CAPS:p=B/n/'CAPTURE.json';need(sha(raw(p))==pin,'Pinned actual ROOT SOURCE operation');rootcaps.append(captured(p,exit_code))
    for first,last,m,closer,verifier,report,pin in [(rootcaps[0],rootcaps[1],prep,H/'close_source.py',H/'verify_closed_source.py',sha(raw(H/'REPORT.md')),PREP),(rootcaps[2],rootcaps[3],fm,F/'close_source.py',F/'verify_closed_source.py',SOURCE_REPORT,FM)]:
        c,d=first['complete_capture'],last['complete_capture'];need(c['argv']==['/usr/bin/python3','-B',str(closer),'--expected-report-sha256',report] and d['argv']==['/usr/bin/python3','-B',str(verifier),'--expected-manifest-sha256',pin] and clock(c['started_utc'])<=clock(m['utc'])<=clock(c['finished_utc'])<clock(d['started_utc']),'Literal ROOT close then separate post-exit readonly with genuine pins')
    operator_body=raw(H/'capture_root_final_operation.py');need(sha(operator_body)==OPERATOR,'Exact V3 final operator body, author is distinct from sealer/capture operator')
    old_umask=os.umask(0o022);fresh,foreign,ownedlogs,queries,current_check,runtimefolder=fresh_runtime(inputs)
    inspection=dict(schema='pr48-root-complete-acceptance-source-inspection/v1',status='PASS_ROOT_COMPLETE_ACCEPTANCE_SOURCE_INSPECTION',utc=now(),all_prepared_source_and_controls_fully_read=True,exact_preparation_closure_and_full_modes_checked=True,all_individual_source_adversary_inputs_checked=True,all_complete_actual_captures_checked=True,complete_VERDICT_object=v,preparation_manifest_sha256=PREP,acceptance_source_manifest=ref(F/'SELF_MANIFEST.json'),acceptance_source_verdict=ref(F/'VERDICT.json'),mandatory_corrections=[],future_execution_approved=False,complete_prepared_bindings=prepared,complete_closed_adversary_bindings=owned,normalized_complete_external_input_bindings=rr,complete_actual_closing_and_postclosing_readback_captures=rootcaps[2:4],all_complete_source_captures=own+review+rootcaps,entire_actual_PR47_post=post,entire_actual_PR47_ROOT_post=rp,complete_actual_PR47_phase_captures=previouscaps,complete_actual_PR47_ROOT_post_capture=root47cap,actual_PR47_native13_epoch_qualification=dict(historical_current13=rp['current13'],mutable_native4_are_dated_observations_not_future_live_authority=True,current_stable9_body_and_fullmode_checked=True,complete_current47_state_history_baseline_checked=True,fresh_current_QUEUE_inventory_main_authority_collected_at_actual_RUN=True,author_current13_before_after_guarantee_is_own_epoch_only=True),existing_precise_ROOT_scientific_read_ledger=ref(A/'ROOT_PRIMARY_READ_LEDGER.json'),existing_precise_ROOT_science_card=ref(A/'ROOT_SCIENCE_CARD.json'),existing_precise_ROOT_closed_WHOLE_record=ref(A/'ROOT_WHOLE_CURRENT_REVIEW.json'),fresh_native13_before_authoring=fresh['files'],current_main_head_at_authoring=fresh['current_head'],complete_foreign_tracked_dirt_preimages=foreign,exact_owned_operational_log_preimages=ownedlogs,actual_author_previous_umask=old_umask,actual_author_umask=0o022,V3_source_accepts_existing_full_modes_and_checks_all13=True,automatic_external_hash_checks_are_not_personal_reading_claims=True,ROOT_personal_reading='By the explicit argument ROOT attests the complete prepared V3 sources/controls/report/contract, this author source, and the final independently closed fresh SOURCE report/verdict were personally read. Existing exact primary-reading, science and WHOLE records provide their own precise earlier assertions. Runtime reconciliation checks whole fixed bodies/types/full modes and all completed47 role/argv/stream evidence; it does not invent personal reading of every external payload or new independent mathematical reproving. Approval is for the inherited UNSOLVED partial only, with no new proof turn, fullgroup solution, paper or DOI.')
    operator=A/'capture_root_final_operation.py';inspection_body=encode(inspection);bindings=load(H/'DRAFT_ROOT_IMMUTABLE_BINDINGS.json');bindings.update(status='ROOT_APPROVED_CLOSED_WHOLE_SOURCE_AND_ACTUAL_PR47_EVIDENCE',created_utc=now(),root_full_current_read_completed=True,root_full_whole_read_completed=True,root_acceptance_source_review_completed=True,independent_whole_current_pass=True,root_actual_PR47_predecessor_read_completed=True)
    paths=dict(whole_manifest=W/'MANIFEST.json',root_whole_inspection=A/'ROOT_WHOLE_CURRENT_REVIEW.json',previous_mirror=P47/'state_mirror_bindings.json',previous_post=P47/'post_acceptance_verification.json',previous_root_post=P47/'ROOT_ACTUAL_POST_INSPECTION.json',previous_post_contract=H47/'ROOT_POST_CONTRACT.json',acceptance_source_manifest=F/'SELF_MANIFEST.json',acceptance_source_verdict=F/'VERDICT.json')
    for k,p in paths.items():bindings[k]=ref(p)
    bindings['root_capture_operator']=dict(path=operator.relative_to(R).as_posix(),bytes=len(operator_body),sha256=sha(operator_body));bindings['root_source_inspection']=dict(path=(A/'ROOT_SOURCE_ACCEPTANCE_REVIEW.json').relative_to(R).as_posix(),bytes=len(inspection_body),sha256=sha(inspection_body));bindings_body=encode(bindings);binding_ref=dict(path=(A/'ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS.json').relative_to(R).as_posix(),bytes=len(bindings_body),sha256=sha(bindings_body))
    refs=[triple(inputs['pins'][n]) for n in sorted(inputs['pins'])]+[ref(C/'MANIFEST.json'),ref(C/'CURRENT_DEPENDENCIES.json'),ref(W/'MANIFEST.json'),ref(W/'AUDIT.md'),ref(W/'VERDICT.json'),ref(A/'ROOT_WHOLE_CURRENT_REVIEW.json'),binding_ref]+[bindings[k] for k in ['previous_mirror','previous_post','previous_root_post','previous_post_contract','acceptance_source_manifest','acceptance_source_verdict','root_source_inspection','root_capture_operator']];dedup={}
    for z in refs:need(z['path'] not in dedup or eq(dedup[z['path']],z),'Exact immutable plan identity');dedup[z['path']]=z
    plan.update(plan_status='ROOT_REVIEWED_FOR_ACTUAL_RECONCILIATION',partial_valid=True,preparation_manifest_sha256=PREP,root_bindings=binding_ref['path'],root_bindings_sha256=binding_ref['sha256'],whole_manifest_sha256=bindings['whole_manifest']['sha256'],root_full_current_read_completed=True,root_full_whole_read_completed=True,root_acceptance_source_review_completed=True,independent_whole_current_pass=True,root_actual_PR47_predecessor_read_completed=True,immutable_evidence_references=sorted(dedup.values(),key=lambda z:z['path']))
    current_check()
    for p,b in [(operator,operator_body),(A/'ROOT_SOURCE_ACCEPTANCE_REVIEW.json',inspection_body),(A/'ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS.json',bindings_body),(A/'ROOT_FINAL_PLAN.json',encode(plan)),(A/'ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES.json',encode(fresh))]:put(p,b)
    for z in refs:check(z)
    current_check();need(raw(Path(__file__))==raw(runtimefolder/'PRELAUNCH_OPERATOR.py'),'Author whole source unchanged');runtime=dict(schema='pr48-root-author-complete-readonly-runtime-input-inspection/v1',utc=now(),actual_author_pid=os.getpid(),entire_fresh_native_authority=fresh,all_complete_readonly_Git_captures=queries,protected_foreign_tracked_full_preimages=foreign,exact_owned_operational_log_preimages=ownedlogs,native13_before_after_equal=True,HEAD_index_foreign_body_fullmode_unchanged=True,author_source=ref(Path(__file__)),source_preparation_executed_this_author=False,future_acceptance_completed=False)
    exclusive(runtimefolder/'READONLY_INPUT_INSPECTION.json',encode(runtime))
    print(json.dumps(dict(status='PASS_ROOT_COMPLETE_SOURCE_AND_GENUINE_ACTUAL47_FRESH_BINDINGS',actual_pid=os.getpid(),prepared=53,adversary=SOURCE_FILES,individual_external=len(rr),complete_source_captures=len(own)+len(review)+len(rootcaps),actual47_phase_captures=6,actual_readonly_Git_children=len(queries),fresh_current_main=fresh['current_head'],protected_foreign_paths=fresh['protected_foreign_tracked_paths'],plan_references=len(dedup),fresh_authority=ref(A/'ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES.json'),runtime=ref(runtimefolder/'READONLY_INPUT_INSPECTION.json'),future_execution_approved=False)))
if __name__=='__main__':main()
