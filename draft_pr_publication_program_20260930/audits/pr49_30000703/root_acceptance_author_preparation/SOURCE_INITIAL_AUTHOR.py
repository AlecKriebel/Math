"""UNEXECUTED SOURCE. ROOT reads and copies this body unchanged adjacent to A49.
No production/helper import or scientific execution. The explicit ROOT argument
attests only complete new SOURCE/control/fresh review readings; existing precise
ROOT ledgers retain their own scope. Automatic hashing is not personal reading.
At RUN the author requires genuinely completed48, six distinct ordered phases,
whole ROOT22/post, fresh13/main/foreign/log preimages and a strict clean index.
Only allowlisted readonly Git children and absent-only adjacent admin outputs.
"""
from pathlib import Path,PurePosixPath
import datetime as dt,hashlib,json,math,os,re,stat,subprocess,sys
A=Path(__file__).absolute().parent;R=A.parents[2]
H=A/'acceptance_preparation_family_v2';F=A/'acceptance_source_adversary_family_v2_fresh'
W=A/'current_whole_adversary_family';C=A/'reviewed_candidate'
PROGRAM=R/'draft_pr_publication_program_20260930';B=A.parent/'pr45_9900007'
P48=A.parent/'pr48_2961';H48=P48/'acceptance_preparation_family_v3'
PREP='52795f5940b255fb25eb1dfc958de37dcc570dc21a411e83c40eba3dd71bc27c'
PREP48='9c525f7b540068af07477e8f794e21596d93e69e49e8dbc52972d3196eb9fda4'
CURRENT='8ca8820e1e1493391224ea8f93dde859bd9b3f6316c41763e86433dc85a1fa47'
WHOLE='b3d91982e7a2cfbda0ffce7fe0e45141dabafcb374aecd52078ad3d66a1e9736'
ROOTWHOLE='debae5972fe2e74816b4af75f7dca38cc92544cb39b0ae2188a86d85df20a160'
OPERATOR='0231fd55622f5571c083ce1082c87d009653d653c3d080a2487dfe74b0469985'
FM='1c9ec221a2679f490431c41cd653fe35748cc52cd80df427886f57a4fa0233a0'
SOURCE_REPORT='684315814ef3ace4f5264814f5a571a1ce57903a988bf32a8e4c78bc11de326c'
SOURCE_FILES=54
ROOT_CAPS=[('root_pr49_source_v2_closure_actual_capture','23b08b04c5538fed59449543dda47251328e233922f37f0f35658e3f3a77ca9f',10927),('root_pr49_source_v2_closed_readback_actual_capture','7d184e6bc218abdbe25b98fa4e07b24e91e756501f1d3d97b1df52fc8ffb55b4',11183),('root_pr49_source_v2_fresh_review_closure_actual_capture','ad90b5b60397cab0628b314c2b3561106c764ccf5862721d4cd0be47b5a8ff14',26941),('root_pr49_source_v2_fresh_review_closed_readback_actual_capture','b566009df72244579e6779a5bdc947e5054698286ecfbc7a2b5807083b69370a',27548)]
NATIVE13=['draft_pr_publication_program_20260930/inventory.json',*[('unsolved_math_prioritization/'+n) for n in ['QUEUE.md','state.json','history.jsonl','catalog.json','assessments.json','queue.py','policy.json','manifest.json','cache/problems.json','cache/research_results.json','cache/catalog.sqlite','review_v2/related_target_groups.json']]]
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

def captured(p,expected=0,cwd=None,shape='ROOT'):
    c=load(p);d=p.parent;need(type(c['exit_code']) is int and c['exit_code']==expected and clock(c['started_utc'])<=clock(c['finished_utc'])<=clock(now()),'Actual typed exit/UTC')
    need(c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']>0 and c['operator_unchanged'] is True,'Actual complete child and operator')
    if shape!='ROOT':need(c['source_unchanged'] is True,'Real child source unchanged')
    members={x.name for x in d.iterdir()};need(all(not x.is_symlink() and (x.is_file() or (shape=='PREPARER' and x.is_dir())) for x in d.iterdir()),'Complete regular capture members')
    if shape=='ROOT':
        need(members=={'CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin'} and c['schema']=='root-explicit-command-capture/v1' and c['stdin_supplied'] is False and c['cwd']==str(R) and sha(raw(d/'prelaunch_operator.py'))==c['operator_sha256'],'Genuine ROOT CAP4')
    elif shape=='PHASE':
        need(members=={'CAPTURE.json','PRELAUNCH.json','PRELAUNCH_SOURCE.py','PRELAUNCH_OPERATOR.py','stdout.bin','stderr.bin'} and c['schema']=='ROOT_actual_reviewed_acceptance_phase_capture_v1' and c['cwd']==str(R) and c['stdin_supplied'] is False,'Exact actual phase CAP6')
        pre=load(d/'PRELAUNCH.json');need(all(eq(c[k],v) for k,v in pre.items() if k!='schema'),'Entire original phase prelaunch')
        need(sha(raw(d/'PRELAUNCH_SOURCE.py'))==c['source_sha256'] and sha(raw(d/'PRELAUNCH_OPERATOR.py'))==c['operator_sha256'],'Whole phase sources/operators')
    elif shape=='PREPARER':
        pre=c['prelaunch'];need(c['schema']=='pr49-v2-private-actual-capture/v1' and pre['cwd']==str(H) and pre['stdin_supplied'] is False and pre['argv'][1]=='-B' and Path(pre['argv'][2]).parent==H and eq(load(d/'PRELAUNCH.json'),pre),'Own captured source-author/control argv/prelaunch')
        expectedmembers={'CAPTURE.json','PRELAUNCH.json','PRELAUNCH_SOURCE.py','PRELAUNCH_OPERATOR.py','stdout.bin','stderr.bin'}
        if pre['proposed_sources_read_as_text_only']:expectedmembers.add('PRELAUNCH_PROPOSED_SOURCES')
        if 'own_common' in pre:expectedmembers.add(pre['own_common']['path'])
        need(members==expectedmembers,'Entire literal preparer capture topology')
        need(sha(raw(d/'PRELAUNCH_SOURCE.py'))==pre['source_sha256'] and sha(raw(d/'PRELAUNCH_OPERATOR.py'))==pre['operator_sha256'] and clock(pre['created_utc'])<=clock(c['started_utc']),'Full preparer source/operator/chronology')
        for z in pre['proposed_sources_read_as_text_only']:
            b=raw(d/'PRELAUNCH_PROPOSED_SOURCES'/safe(z['path']));need(len(b)==z['bytes'] and sha(b)==z['sha256'],'Full proposed body captured as text')
        if 'own_common' in pre:
            z=pre['own_common'];b=raw(d/z['path']);need(b==raw(H/'source_package_checks.py') and len(b)==z['bytes'] and sha(b)==z['sha256'],'Full own readback dependency')
    elif shape=='REVIEW':
        pre=c['prelaunch'];need(members=={'CAPTURE.json','PRELAUNCH.json','PRELAUNCH_SOURCE.py','PRELAUNCH_OPERATOR.py','stdout.bin','stderr.bin'} and c['schema']=='pr49-independent-private-actual-capture/v1' and c['cwd']==str(F) and c['stdin_supplied'] is False and eq(load(d/'PRELAUNCH.json'),pre) and eq(c['argv'],pre['argv']) and pre['cwd']==str(F),'Different independent review actual CAP6')
        need(c['argv'][:2]==['/usr/bin/python3','-B'] and Path(c['argv'][2]).parent==F and Path(c['argv'][2]).name in {'private_controls.py','check_custody.py'} and sha(raw(d/'PRELAUNCH_SOURCE.py'))==c['source_sha256']==pre['source_sha256'] and sha(raw(d/'PRELAUNCH_OPERATOR.py'))==c['operator_sha256']==pre['operator_sha256'] and clock(pre['created_utc'])<=clock(c['started_utc']),'Independent whole prelaunch source/operator/argv')
    else:raise ValueError('Unknown explicit capture shape')
    for key in ['stdout','stderr']:
        z=c[key];need(set(z)=={'path','bytes','sha256'} and z['path']==key+'.bin' and type(z['bytes']) is int and z['bytes']>=0,'Typed literal entire stream');b=raw(d/z['path']);need(len(b)==z['bytes'] and sha(b)==z['sha256'],'Whole actual split stream')
    need(raw(d/'stderr.bin')==b'' if expected==0 else bool(raw(d/'stderr.bin')),'Retained success/failure stream')
    return dict(capture=ref(p,True),complete_capture=c,complete_members=[ref(x,True) for x in sorted(d.rglob('*')) if x.is_file()])

PINNAMES=['preparation_manifest_sha256','final_plan','final_plan_sha256','final_receipt','final_receipt_sha256','final_manifest','final_manifest_sha256','reconciliation_capture','reconciliation_capture_sha256','previous_mirror','previous_mirror_sha256','previous_post','previous_post_sha256','fresh_preimage','fresh_preimage_sha256','root_bindings','root_bindings_sha256']
def predecessor():
    # These actual bodies/PIDs/hashes cannot exist in this preparation's authority.
    # Read the completed evidence only during genuine ROOT RUN; missing evidence fails closed.
    m=load(P48/'state_mirror_bindings.json');post=load(P48/'post_acceptance_verification.json');rp=load(P48/'ROOT_ACTUAL_POST_INSPECTION.json');contract=load(H48/'ROOT_POST_CONTRACT.json');pm,_=closure(H48,'PREPARATION_MANIFEST.json',PREP48,53)
    need(pm['schema']=='pr48-acceptance-source-closure/v3' and sha(raw(H48/'ROOT_POST_CONTRACT.json'))=='26f89f5ebf8444f96394ca5050c503920de1b9adb7417489241fcbe04885b410','Exact repaired48V3 source and unchanged literal contract')
    need(contract['schema']=='pr48-future-ROOT-whole-post-contract/v1' and contract['source_only'] is True and contract['future_ROOT_post_completed'] is False and len(contract['future48_required_ROOT_complete_keyset'])==22 and set(rp)==set(contract['future48_required_ROOT_complete_keyset']),'Whole actual48 ROOT22; SOURCE contract stays false')
    need(rp['schema']==contract['future48_required_ROOT_schema'] and all(eq(rp[k],v) for k,v in contract['future48_required_completed_values'].items()) and eq(rp['entire_post'],post),'Every typed complete actual48 ROOT value and entire post')
    expected={**contract['future48_required_entire_post_values'],**{k:post[k] for k in PINNAMES},'utc':post['utc'],'merge_commit':post['merge_commit'],'merge_tree':post['merge_tree'],'actual_remote_state':'MERGED'}
    need(eq(post,expected) and post['preparation_manifest_sha256']==PREP48 and clock(post['utc'])<=clock(rp['utc'])<=clock(now()),'Entire exact actual48 post/chronology, never pending SOURCE')
    for n in ['final_plan','final_receipt','final_manifest','reconciliation_capture','previous_mirror','previous_post','fresh_preimage','root_bindings']:safe(post[n]);need(type(post[n+'_sha256']) is str and re.fullmatch('[0-9a-f]{64}',post[n+'_sha256']) and sha(raw(R/post[n]))==post[n+'_sha256'],'Every actual48 final-reference body')
    need(type(m['entries']) is list and len(m['entries'])==38 and all(type(z['pr']) is int for z in m['entries']) and sorted(z['pr'] for z in m['entries'])==m['required_completed_prs'] and len(set(m['required_completed_prs']))==38 and all(n in m['required_completed_prs'] for n in [46,47,48]) and 49 not in m['required_completed_prs'] and type(m['duplicate_mirrors']) is list and len(m['duplicate_mirrors'])==1,'Actual38 primaries and existing duplicate, ascending48 predecessor')
    phases=['preflight','overlay','prepush','finalize','mirror','post'];need(type(rp['all_six_real_phase_captures']) is list and len(rp['all_six_real_phase_captures'])==6,'Exactly six different ordered real phases')
    flags=['final-plan','final-receipt','final-manifest','reconciliation-capture','previous-mirror','previous-post','fresh-preimage','root-bindings'];caps=[];end=None;pids=set()
    for phase,z in zip(phases,rp['all_six_real_phase_captures']):
        check(z,'full_mode' in z);p=P48/('root_'+phase+'_actual_capture')/'CAPTURE.json';need(z['path']==p.relative_to(R).as_posix(),'Exact distinct actual48 phase path');row=captured(p,shape='PHASE');c=row['complete_capture'];name={'mirror':'state_mirror_reconciliation.py','post':'verify_post_acceptance.py'}.get(phase,'integrate_reviewed_partial.py')
        need(c['phase']==phase and c['pid'] not in pids and c['source_sha256']==sha(raw(H48/name)) and c['operator_sha256']==sha(raw(P48/'run_actual_acceptance_phases.py')),'Exact actual phase/source/operator and distinct child');pids.add(c['pid'])
        argv=['/usr/bin/python3','-B',str(H48/name),'--execute','--preparation-manifest-sha256',PREP48]
        for flag in flags:n=flag.replace('-','_');argv.extend(['--'+flag,post[n],'--'+flag+'-sha256',post[n+'_sha256']])
        if phase not in ['mirror','post']:argv.append(phase)
        if phase=='overlay':argv.extend(['--merge-queue-preimage-sha256',sha(raw(P48/'integration_merge_queue_before.md'))])
        need(eq(c['argv'],argv),'Entire ordered actual48 argv; all17 pins, role and overlay preimage')
        need((end is None or end<=clock(c['started_utc'])) and clock(c['finished_utc'])<=clock(rp['utc']),'Actual phase order and postexit ROOT read');end=clock(c['finished_utc']);caps.append(row)
    rpfile=P48/'root_complete_actual_post_inspection_capture/CAPTURE.json';rootcap=captured(rpfile);cc=rootcap['complete_capture']
    need(cc['argv'][:3]==['/usr/bin/python3','-B',str(P48/'inspect_complete_actual_post.py')] and clock(cc['started_utc'])<=clock(rp['utc'])<=clock(cc['finished_utc']) and end<=clock(cc['started_utc']),'Whole actual48 ROOT post genuinely authored within real child after all phase exits')
    output=load(rpfile.parent/'stdout.bin');need(output['status']=='PASS_COMPLETE_ACTUAL_ROOT_POST_INSPECTION' and eq(output['inspection'],ref(P48/'ROOT_ACTUAL_POST_INSPECTION.json')),'Actual ROOT post stdout entire record identity')
    need(type(rp['current13']) is list and len(rp['current13'])==13 and {z['path'] for z in rp['current13']}==set(NATIVE13),'Exact historical13 identity domain')
    for z in rp['current13']:
        need(set(z)=={'path','bytes','sha256','worktree_mode'} and type(z['worktree_mode']) is int and 0<=z['worktree_mode']<=0o7777 and type(z['bytes']) is int and z['bytes']>=0,'Typed actual48 historical native row');safe(z['path'])
        if z['path'] not in MUTABLE4:check(dict(triple(z),full_mode=z['worktree_mode']),True)
    plan=load(P48/'state_mirror_plan.json');intent=load(P48/'state_mirror_intent.json');current=load(R/'unsolved_math_prioritization/state.json')
    need(eq(current,plan['state_after']) and len(current)==39 and all(type(v['turns_used']) is int for v in current.values()) and sum(v['turns_used'] for v in current.values())==47 and raw(R/'unsolved_math_prioritization/history.jsonl')==(intent['before_history_bytes']+plan['history_append_bytes']).encode(),'Whole completed48 native39targets47turns38primary baseline')
    inv=load(PROGRAM/'inventory.json');need(type(inv['completed_count']) is int and inv['completed_count']==38 and len(inv['items'])==180 and sum(z.get('stage')=='complete' for z in inv['items'])==38 and inv['current_pr']==49,'Actual38-of180 inventory predecessor, next49')
    return m,post,rp,caps,rootcap

def encode(o):return (json.dumps(o,indent=2,sort_keys=True,ensure_ascii=False,allow_nan=False)+'\n').encode()
def exclusive(p,b):
    need(not p.exists() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents),'Absent regular ROOT administrative output')
    with p.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
    need(stat.S_IMODE(p.stat().st_mode)==0o644,'Exact new full0644 under explicit0022 umask')
def put(p,b):need(p.parent==A,'Adjacent ROOT record only');exclusive(p,b)

def fresh_runtime(inputs):
    native=sorted(NATIVE13);need(len(native)==13 and len(set(native))==13,'Exactly13 native paths');native_before=[dict(triple(ref(R/n)),worktree_mode=ref(R/n,True)['full_mode']) for n in native]
    queue=raw(R/'unsolved_math_prioritization/QUEUE.md').decode().splitlines();header=['Rank','ID / code','Problem','EV','Impact (/10)','Difficulty','Proposed','Status','Turns','Chat','Findings','DOI'];heads=[s for s in queue if s.startswith('| Rank | ID / code |')];need(len(heads)==1 and [x.strip() for x in heads[0].split('|')[1:-1]]==header,'Exact fresh twelve-column QUEUE header')
    rows=[s.split('|')[1:-1] for s in queue if len(s.split('|'))==14];selected=[z for z in rows if z[1].strip()=='30000703 / OWR-1460-009'];need(len(selected)==1 and selected[0][7].strip()=='queued' and selected[0][8].strip()=='0/5','Fresh selected49 queued0/5; entire unrelated rows retained')
    root=A/'root_acceptance_author_readonly_inputs';need(not root.exists() and not root.is_symlink(),'Exclusive runtime readonly capture family');root.mkdir();exclusive(root/'PRELAUNCH_OPERATOR.py',raw(Path(__file__)));queries=[]
    def git(*args):
        allowed=[('branch','--show-current'),('rev-parse','HEAD'),('diff','--no-ext-diff','--no-textconv','--cached','--name-only','-z'),('diff','--no-ext-diff','--no-textconv','--name-only','-z')]
        dynamic=(len(args)==5 and args[:4] in [('ls-tree','-z','HEAD','--'),('ls-files','--stage','-z','--')]) or (len(args)==3 and args[:2]==('show','--no-textconv') and (args[2].startswith('HEAD:') or args[2].startswith(':')))
        need(args in allowed or dynamic,'Readonly Git argv whitelist')
        if dynamic:safe(args[-1].split(':',1)[1] if args[0]=='show' else args[-1])
        argv=['git',*args];started=now();d=root/('%03d'%len(queries));d.mkdir();pre=dict(schema='pr49-root-author-readonly-Git-prelaunch/v1',argv=argv,cwd=str(R),started_utc=started,actual_operator_pid=os.getpid(),source=None,stdin_supplied=False);exclusive(d/'PRELAUNCH.json',encode(pre))
        child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        try:out,err=child.communicate(timeout=60)
        except BaseException:child.kill();out,err=child.communicate();exclusive(d/'stdout.bin',out);exclusive(d/'stderr.bin',err);raise
        exclusive(d/'stdout.bin',out);exclusive(d/'stderr.bin',err);cap=dict(pre,schema='pr49-root-author-readonly-Git-capture/v1',actual_execution=True,pid=child.pid,completed=True,exit_code=child.returncode,finished_utc=now(),source_unchanged=None,operator_sha256=sha(raw(Path(__file__))),operator_unchanged=raw(Path(__file__))==raw(root/'PRELAUNCH_OPERATOR.py'),stdout=ref(d/'stdout.bin'),stderr=ref(d/'stderr.bin'))
        exclusive(d/'CAPTURE.json',encode(cap));queries.append(dict(capture=ref(d/'CAPTURE.json'),complete_capture=cap,complete_members=[ref(p,True) for p in sorted(d.iterdir())]));need(child.returncode==0 and err==b'' and cap['operator_unchanged'] is True,'Complete successful readonly Git child');return out
    def owned(n):safe(n);return n in native or n==(PROGRAM/'RESEARCH_LOG.md').relative_to(R).as_posix() or n.startswith('unsolved_math_prioritization/attempts/30000703/') or n.startswith(A.relative_to(R).as_posix()+'/')
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
    freshclock=now();fresh=dict(schema='pr49-root-fresh-acceptance-input-preimages/v1',approved_by_root=True,created_utc=freshclock,reason_date_utc=clock(freshclock).date().isoformat(),reason='ROOT reconciles genuine completed PR48 and closed PR49 V2 source against the actual current main and all thirteen native bodies and full modes; historical native observations do not authorize this fresh epoch.',current_head=head,files=native_before,protected_foreign_tracked_paths=paths)
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
    need(__debug__ and sys.flags.optimize==0 and sys.argv==[sys.argv[0],'--personally-read-complete-source'],'Explicit ROOT complete new source/control/fresh-review attestation')
    need(A.name=='pr49_30000703' and raw(Path(__file__))==raw(A/'root_acceptance_author_preparation/author_ROOT_acceptance.py'),'Copy exact personally reviewed SOURCE adjacent; do not run preparation')
    outputs=['capture_root_final_operation.py','ROOT_SOURCE_ACCEPTANCE_REVIEW.json','ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS.json','ROOT_FINAL_PLAN.json','ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES.json'];need(all(not (A/n).exists() and not (A/n).is_symlink() for n in outputs),'All ROOT approvals and actualfresh outputs absent-only')
    prep,prepared=closure(H,'PREPARATION_MANIFEST.json',PREP,129);fm,owned=closure(F,'SELF_MANIFEST.json',FM,54)
    need(set(prep)=={'schema','status','utc','self_excluded','files_count','files','source_only','proposed_helpers_imported_compiled_executed','future_acceptance_or_ROOT_approval_claimed'} and prep['schema']=='pr49-acceptance-source-closure/v2' and prep['status']=='CLOSED_SOURCE_ONLY' and prep['source_only'] is True and prep['proposed_helpers_imported_compiled_executed'] is False and prep['future_acceptance_or_ROOT_approval_claimed'] is False,'Exact actual129-payload V2 source-only closure')
    need(fm['schema']=='pr49-fresh-acceptance-source-adversary-closure/v1' and set(fm)=={'schema','utc','self_excluded','files_count','files','directories','source_only','production_imported_compiled_executed','future_acceptance_approved'} and fm['source_only'] is True and fm['production_imported_compiled_executed'] is False and fm['future_acceptance_approved'] is False,'Exact fresh independent54-payload source-only closure')
    need(sha(raw(F/'REPORT.md'))==SOURCE_REPORT,'Exact fully read fresh report');v=load(F/'VERDICT.json');need(v['schema']=='pr49-acceptance-source-adversary-verdict/v1' and v['verdict']=='PASS_SOURCE_ONLY_SCOPED' and v['preparation_manifest_sha256']==PREP and v['mandatory_corrections']==[] and v['production_imported_compiled_executed'] is False and v['future_acceptance_approved'] is False and v['original_source_response_field_absent'] is True and v['project_solved'] is False,'Complete clean exact new independent verdict, credited-known scope')
    external=load(F/'EXTERNAL_BINDINGS.json');need(external['schema']=='pr49-fresh-source-individual-inputs/v1' and type(external['files']) is list and len(external['files'])==375 and len({z['path'] for z in external['files']})==375 and external['nested_fixed_table_count']==3229,'Exact375 direct and3229 nested input rows')
    rootwhole=load(A/'ROOT_WHOLE_CURRENT_REVIEW.json');need(sha(raw(A/'ROOT_WHOLE_CURRENT_REVIEW.json'))==ROOTWHOLE and eq(ref(A/'ROOT_WHOLE_CURRENT_REVIEW.json',True),external['nested_fixed_table']),'Genuine complete ROOT WHOLE body/mode')
    rr=[];tables=[external['files'],rootwhole['normalized_complete_fixed_bindings'],load(H/external['nested_old_source_table'])['files'],load(H/external['nested_closed48_history_table'])['closed_history_fixed_bindings']];need([len(z) for z in tables]==[375,3229,154,148],'Complete direct/nested/old/history counts')
    unique={}
    for table in tables:
        for z in table:check(z,True);need(z['path'] not in unique or eq(unique[z['path']],z),'Conflicting full fixed body/mode observations');unique[z['path']]=z
    rr=sorted(unique.values(),key=lambda z:z['path']);need(rootwhole['approved_by_root'] is True and rootwhole['future_acceptance_approved'] is False and rootwhole['current_native_acceptance_approved'] is False and len(rootwhole['dated_native4'])==4,'WHOLE-only approval and four dated native witnesses')
    for z in rootwhole['dated_native4']:check(z['whole_historical_snapshot'],True);need(z['future_fresh13_ROOT_required'] is True and z['live_unchanged_required_by_review_closure'] is False and z['whole_historical_snapshot']['sha256']==z['original_observed_row']['sha256'] and z['whole_historical_snapshot']['bytes']==z['original_observed_row']['bytes'],'Wholebody dated native witness, no live immutable equality')
    inputs=load(H/'INPUT_BINDINGS.json');need(inputs['whole_binding_completed'] is True and inputs['actual_predecessor_PR48_completed'] is False,'Closed SOURCE has no future48 native approval; actual RUN must supply it')
    current,_=closure(C,'MANIFEST.json',CURRENT,1544);whole,_=closure(W,'SELF_MANIFEST.json',WHOLE,127)
    ledger=load(A/'ROOT_PRIMARY_READ_LEDGER.json');card=load(A/'ROOT_SCIENCE_CARD.json');need(sha(raw(A/'ROOT_PRIMARY_READ_LEDGER.json'))=='21ea16820a7e3b5230c1894ae18405803302f52d6f1364d587130e043bce6e04' and sha(raw(A/'ROOT_SCIENCE_CARD.json'))=='fa7fc79442d88b97aa41ee5a218b036ae39b7c988fc615915fd8fbf4a2fe497c' and ledger['approved_by_root'] is True and ledger['reading_completed'] is True and len(ledger['root_flags'])==8 and all(z is True for z in ledger['root_flags'].values()) and card['approved_by_root'] is True and card['status']=='already_solved' and card['full_2007_journal_proof_independently_certified'] is False,'Exact earlier ROOT scientific/read ledgers, no newly invented reproving')
    science=load(H/'SCIENTIFIC_SCOPE.json');plan=load(H/'DRAFT_FINAL_PLAN.json');need(eq(plan['scientific_scope'],science) and science['literal_target_status']=='already_solved' and science['problem_id']==30000703 and type(science['problem_id']) is int and science['full_problem_solved'] is True and science['full_problem_solved_by_project'] is False and science['full_2007_journal_proof_independently_certified'] is False and science['original_substantive_attempts']==science['new_substantive_attempts']==science['audit_turns']==0 and science['original_source_response_count'] is None and science['original_response_field_absent'] is True and science['partial_valid'] is True and science['novelty_claimed'] is False and science['paper_or_new_doi_or_tracker'] is False,'Exact qualified known-result0/5 scope; no new discovery/paper/response count')
    names={'AUTHORING_ACTUAL_CAPTURE':1,'REPAIR_AUTHOR_ACTUAL_CAPTURE':0,'AUTHORING_V2_ACTUAL_CAPTURE':0,'PRIVATE_CONTROLS_ACTUAL_CAPTURE':0,'FINAL_PRIVATE_CONTROLS_ACTUAL_CAPTURE':0,'PREDECESSOR_DESIGN_BINDING_ACTUAL_CAPTURE':0,'FINAL_SOURCE_READINESS_ACTUAL_CAPTURE':0};own=[captured(H/n/'CAPTURE.json',code,shape='PREPARER') for n,code in names.items()]
    reviewnames={'independent_controls_actual':1,'independent_controls_v2_actual':1,'independent_controls_v3_actual':0,'fixed_source_custody_actual':0};review=[captured(F/n/'CAPTURE.json',code,shape='REVIEW') for n,code in reviewnames.items()]
    rootcaps=[]
    for n,pin,pid in ROOT_CAPS:p=B/n/'CAPTURE.json';need(sha(raw(p))==pin,'True actual ROOT closure/readback hash');row=captured(p);need(row['complete_capture']['pid']==pid,'Exact genuine ROOT child identity');rootcaps.append(row)
    for first,last,m,closer,verifier,report,pin in [(rootcaps[0],rootcaps[1],prep,H/'close_source_ROOT_ONLY.py',H/'verify_closed_source_ROOT_ONLY.py',sha(raw(H/'REPORT.md')),PREP),(rootcaps[2],rootcaps[3],fm,F/'close_for_ROOT.py',F/'verify_closed_readonly.py',SOURCE_REPORT,FM)]:
        c,d=first['complete_capture'],last['complete_capture'];need(c['argv']==['/usr/bin/python3','-B',str(closer),'--expected-report-sha256',report] and d['argv']==['/usr/bin/python3','-B',str(verifier),'--expected-manifest-sha256',pin] and clock(c['started_utc'])<=clock(m['utc'])<=clock(c['finished_utc'])<clock(d['started_utc']),'Entire literal true ROOT close then separate postexit readback')
    previous,post,rp,previouscaps,root48cap=predecessor()
    operator_body=raw(H/'capture_root_final_operation.py');need(sha(operator_body)==OPERATOR,'Exact reviewed49V2 final operator body')
    old_umask=os.umask(0o022);fresh,foreign,ownedlogs,queries,current_check,runtimefolder=fresh_runtime(inputs)
    inspection=dict(schema='pr49-root-complete-acceptance-source-inspection/v1',status='PASS_ROOT_COMPLETE_ACCEPTANCE_SOURCE_INSPECTION',utc=now(),all_prepared_source_and_controls_fully_read=True,exact_preparation_closure_and_full_modes_checked=True,all_individual_source_adversary_inputs_checked=True,all_complete_actual_captures_checked=True,complete_VERDICT_object=v,preparation_manifest_sha256=PREP,acceptance_source_manifest=ref(F/'SELF_MANIFEST.json'),acceptance_source_verdict=ref(F/'VERDICT.json'),mandatory_corrections=[],future_execution_approved=False,complete_prepared_bindings=prepared,complete_closed_adversary_bindings=owned,normalized_complete_external_input_bindings=rr,complete_actual_closing_and_postclosing_readback_captures=rootcaps[2:4],all_complete_source_captures=own+review+rootcaps,entire_actual_PR48_post=post,entire_actual_PR48_ROOT_post=rp,complete_actual_PR48_distinct_ordered_phase_captures=previouscaps,complete_actual_PR48_ROOT_post_capture=root48cap,actual_PR48_native13_epoch_qualification=dict(historical_current13=rp['current13'],mutable_native4_dated_not_future_authority=True,current_stable9_checked=True,complete_current48_state_history_baseline_checked=True,fresh13_QUEUE_inventory_main_collected_at_RUN=True,author_current13_before_after_guarantee_is_own_epoch_only=True),existing_precise_ROOT_scientific_read_ledger=ref(A/'ROOT_PRIMARY_READ_LEDGER.json'),existing_precise_ROOT_science_card=ref(A/'ROOT_SCIENCE_CARD.json'),existing_complete_ROOT_WHOLE_record=ref(A/'ROOT_WHOLE_CURRENT_REVIEW.json'),fresh_native13_before_authoring=fresh['files'],current_main_head_at_authoring=fresh['current_head'],complete_foreign_tracked_dirt_preimages=foreign,exact_owned_operational_log_preimages=ownedlogs,actual_author_previous_umask=old_umask,actual_author_umask=0o022,actual_bytes_changed_columns=['Status','Findings'],allowed_named_queue_columns=['Status','Turns','Findings'],Turns_bytes_unchanged_literal='0/5',automatic_hash_checks_are_not_personal_reading_claims=True,ROOT_personal_reading='The explicit argument attests complete new prepared SOURCE/control/report/contract, this author source and final independent SOURCE report/verdict personal reading. Existing precise ROOT science/reading/WHOLE ledgers retain their own earlier scope. Runtime reconciles every fixed byte/mode and genuinely completed48 phases/argv/streams/post; it does not assert fresh personal reading of every corpus body or reprove the imported2007 journal proof. Known prior result only, original0/new0/audit0; no discovery/paper/DOI/tracker.')
    operator=A/'capture_root_final_operation.py';inspection_body=encode(inspection);bindings=load(H/'DRAFT_ROOT_IMMUTABLE_BINDINGS.json');bindings.update(status='ROOT_APPROVED_CLOSED_WHOLE_SOURCE_AND_ACTUAL_PR48_EVIDENCE',created_utc=now(),root_full_current_read_completed=True,root_full_whole_read_completed=True,root_acceptance_source_review_completed=True,independent_whole_current_pass=True,root_actual_PR48_predecessor_read_completed=True)
    paths=dict(whole_manifest=W/'SELF_MANIFEST.json',root_whole_inspection=A/'ROOT_WHOLE_CURRENT_REVIEW.json',previous_mirror=P48/'state_mirror_bindings.json',previous_post=P48/'post_acceptance_verification.json',previous_root_post=P48/'ROOT_ACTUAL_POST_INSPECTION.json',previous_post_contract=H48/'ROOT_POST_CONTRACT.json',previous_preparation_manifest=H48/'PREPARATION_MANIFEST.json',acceptance_source_manifest=F/'SELF_MANIFEST.json',acceptance_source_verdict=F/'VERDICT.json')
    for k,p in paths.items():bindings[k]=ref(p)
    bindings['root_capture_operator']=dict(path=operator.relative_to(R).as_posix(),bytes=len(operator_body),sha256=sha(operator_body));bindings['root_source_inspection']=dict(path=(A/'ROOT_SOURCE_ACCEPTANCE_REVIEW.json').relative_to(R).as_posix(),bytes=len(inspection_body),sha256=sha(inspection_body));bindings_body=encode(bindings);binding_ref=dict(path=(A/'ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS.json').relative_to(R).as_posix(),bytes=len(bindings_body),sha256=sha(bindings_body))
    refs=[triple(inputs['pins'][n]) for n in sorted(inputs['pins'])]+[triple(z) for z in rootwhole['normalized_complete_fixed_bindings']]+[ref(C/'MANIFEST.json'),ref(C/'CURRENT_DEPENDENCIES.json'),ref(W/'SELF_MANIFEST.json'),ref(W/'REPORT.md'),ref(W/'VERDICT.json'),ref(A/'ROOT_WHOLE_CURRENT_REVIEW.json'),binding_ref]+[bindings[k] for k in ['previous_mirror','previous_post','previous_root_post','previous_post_contract','previous_preparation_manifest','acceptance_source_manifest','acceptance_source_verdict','root_source_inspection','root_capture_operator']];dedup={}
    for z in refs:need(z['path'] not in dedup or eq(dedup[z['path']],z),'Exact immutable plan identity');dedup[z['path']]=z
    plan.update(plan_status='ROOT_REVIEWED_FOR_ACTUAL_RECONCILIATION',partial_valid=True,preparation_manifest_sha256=PREP,root_bindings=binding_ref['path'],root_bindings_sha256=binding_ref['sha256'],whole_manifest_sha256=bindings['whole_manifest']['sha256'],root_full_current_read_completed=True,root_full_whole_read_completed=True,root_acceptance_source_review_completed=True,independent_whole_current_pass=True,root_actual_PR48_predecessor_read_completed=True,immutable_evidence_references=sorted(dedup.values(),key=lambda z:z['path']))
    current_check()
    for p,b in [(operator,operator_body),(A/'ROOT_SOURCE_ACCEPTANCE_REVIEW.json',inspection_body),(A/'ROOT_IMMUTABLE_ACCEPTANCE_BINDINGS.json',bindings_body),(A/'ROOT_FINAL_PLAN.json',encode(plan)),(A/'ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES.json',encode(fresh))]:put(p,b)
    for z in refs:check(z)
    current_check();need(raw(Path(__file__))==raw(runtimefolder/'PRELAUNCH_OPERATOR.py'),'Entire actual author unchanged');runtime=dict(schema='pr49-root-author-complete-readonly-runtime-input-inspection/v1',utc=now(),actual_author_pid=os.getpid(),entire_fresh_native_authority=fresh,all_complete_readonly_Git_captures=queries,protected_foreign_tracked_full_preimages=foreign,exact_owned_operational_log_preimages=ownedlogs,native13_before_after_equal=True,HEAD_index_foreign_body_fullmode_unchanged=True,author_source=ref(Path(__file__)),source_preparation_executed_this_author=False,future_acceptance_completed=False)
    exclusive(runtimefolder/'READONLY_INPUT_INSPECTION.json',encode(runtime));print(json.dumps(dict(status='PASS_ROOT_COMPLETE_SOURCE_AND_GENUINE_ACTUAL48_FRESH_BINDINGS',actual_pid=os.getpid(),prepared=129,adversary=54,individual_external=len(rr),complete_source_captures=len(own)+len(review)+len(rootcaps),actual48_distinct_ordered_phase_captures=6,actual_readonly_Git_children=len(queries),fresh_current_main=fresh['current_head'],protected_foreign_paths=fresh['protected_foreign_tracked_paths'],plan_references=len(dedup),fresh_authority=ref(A/'ROOT_FRESH_ACCEPTANCE_INPUT_PREIMAGES.json'),runtime=ref(runtimefolder/'READONLY_INPUT_INSPECTION.json'),future_execution_approved=False)))
if __name__=='__main__':main()
