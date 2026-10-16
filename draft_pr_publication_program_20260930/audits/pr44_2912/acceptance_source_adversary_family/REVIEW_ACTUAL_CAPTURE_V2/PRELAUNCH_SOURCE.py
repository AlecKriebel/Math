"""Independent source-only acceptance adversary. Never imports/compiles/runs proposed code."""
from pathlib import Path, PurePosixPath
import copy
import datetime as dt
import difflib
import hashlib
import io
import json
import math
import os
import re
import stat
import subprocess
import tokenize

H=Path(__file__).resolve().parent
A=H.parent
R=H.parents[3]
P=A/'acceptance_preparation_family'
C=A/'reviewed_candidate'
W=A/'whole_current_source_first_family'
PREP='413ae6bab4142da7b611d910f801cf8ab92d7d085fad4ceed7203074538442de'
EPOCH='2b9d0234b1396fa84c4b34055b5e8e14c873588b'
HEAD='c772dc5b851ec91da9d46d534577609e5d3ca389'
BASE='01358d66fc67d1c462bddf31c0d4ee5b120e6737'
refs={};checks=[];queries=[];hostile=[]
def utc():return dt.datetime.now(dt.timezone.utc).isoformat()
def check(ok,label):
    if not ok:raise ValueError(label)
    checks.append(label)
def sha(b):return hashlib.sha256(b).hexdigest()
def parse(b):
    def pairs(rr):
        o={}
        for k,v in rr:
            if k in o:raise ValueError('Duplicate JSON key')
            o[k]=v
        return o
    def floating(s):
        v=float(s)
        if not math.isfinite(v):raise ValueError('Nonfinite JSON float')
        return v
    return json.loads(b,object_pairs_hook=pairs,parse_float=floating,parse_constant=lambda s:(_ for _ in ()).throw(ValueError('Nonfinite JSON constant')))
def load(p):return parse(p.read_bytes())
def typed_eq(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return set(a)==set(b) and all(typed_eq(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(typed_eq(x,y) for x,y in zip(a,b))
    return a==b
def safe(n):
    if type(n) is not str or not n or '\\' in n or '\0' in n:raise ValueError('Unsafe name')
    p=PurePosixPath(n)
    if p.is_absolute() or p.as_posix()!=n or set(p.parts)&{'.','..','.git','__pycache__'}:raise ValueError('Unsafe canonical path')
    return n
def regular(base,n):
    safe(n);p=base/n
    if base.is_symlink() or not base.is_dir() or p.is_symlink() or not p.is_file():raise ValueError('Not regular')
    for q in p.parents:
        if q==base:break
        if q.is_symlink():raise ValueError('Symlink ancestor')
    if not p.resolve().is_relative_to(base.resolve()):raise ValueError('Escaping file')
    return p
def pin(p):
    p=regular(R,p.relative_to(R).as_posix());h=hashlib.sha256();n=0
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):n+=len(b);h.update(b)
    z={'path':p.relative_to(R).as_posix(),'bytes':n,'sha256':h.hexdigest()}
    if z['path'] in refs and refs[z['path']]!=z:raise ValueError('Changed input during review')
    refs[z['path']]=z
    return z
def bound(base,z):
    safe(z['path']);n=z.get('bytes',z.get('size'))
    check(type(n) is int and n>=0 and type(z['sha256']) is str and re.fullmatch('[0-9a-f]{64}',z['sha256']) is not None,'Typed individual identity '+z['path'])
    got=pin(regular(base,z['path']))
    check(got['bytes']==n and got['sha256']==z['sha256'],'Entire hash-only identity '+got['path'])
def topology(base,expected):
    actual=set();dirs=set()
    for p in base.rglob('*'):
        n=p.relative_to(base).as_posix();safe(n)
        if p.is_symlink() or not(p.is_file() or p.is_dir()):raise ValueError('Special member')
        (actual if p.is_file() else dirs).add(n)
    required_dirs={q.as_posix() for n in expected for q in PurePosixPath(n).parents if q.as_posix()!='.'}
    if actual!=set(expected) or dirs!=required_dirs:raise ValueError('Exact recursive closure differs')
    return dirs
def closure(base,name,pinned,count):
    z=pin(base/name);check(z['sha256']==pinned,'Literal closure hash '+str(base));o=load(base/name)
    check(o['self_excluded']==[name] and type(o['files_count']) is int and o['files_count']==count and len(o['files'])==count,'Self-only closure/count '+str(base))
    names=[z['path'] for z in o['files']]
    check(len(set(names))==count and name not in names,'Unique nonself rows '+str(base))
    for z in o['files']:bound(base,z)
    dirs=topology(base,set(names)|{name})
    for n in set(names)|{name}:check(stat.S_IMODE(regular(base,n).stat().st_mode)==0o444,'Literal full0444 '+str(base/n))
    return o,dirs
def git(*tail):
    allowed=tail in [('branch','--show-current'),('rev-parse','HEAD')] or (tail[:2]==('ls-tree','-z') and tail[2]==EPOCH) or (tail[:1]==('show',) and tail[1].startswith(EPOCH+':'))
    check(allowed,'Read-only Git argv allowlist')
    d=H/'ACTUAL_GIT'/str(os.getpid())/str(len(queries));d.mkdir(parents=True,exist_ok=False)
    pre={'argv':['git',*tail],'cwd':str(R),'utc':utc(),'operator_pid':os.getpid(),'source_sha256':sha(Path(__file__).read_bytes()),'stdin_supplied':False}
    (d/'PRELAUNCH.json').write_text(json.dumps(pre,sort_keys=True,indent=2)+'\n')
    proc=subprocess.Popen(pre['argv'],cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
    out,err=proc.communicate()
    rec={**pre,'pid':proc.pid,'actual_execution':True,'completed':True,'exit_code':proc.returncode,'finished_utc':utc()}
    for k,b in [('stdout',out),('stderr',err)]:(d/(k+'.bin')).write_bytes(b);rec[k]={'path':(d/(k+'.bin')).relative_to(H).as_posix(),'bytes':len(b),'sha256':sha(b)}
    (d/'CAPTURE.json').write_text(json.dumps(rec,sort_keys=True,indent=2)+'\n');queries.append(rec)
    check(proc.returncode==0 and not err,'Actual read-only query result')
    return out
def native():
    return [{**pin(R/z['path']),'worktree_mode':stat.S_IMODE((R/z['path']).stat().st_mode)} for z in load(A/'ROOT_CURRENT_INPUT_PREIMAGES.json')['files']]
def rejection(label,fn):
    try:fn()
    except (ValueError,KeyError,TypeError):hostile.append(label)
    else:raise ValueError('Hostile control accepted: '+label)
def capture(folder,source_name):
    o=load(folder/'CAPTURE.json');pre=load(folder/'PRELAUNCH.json')
    check(typed_eq(pre,o['prelaunch']),'Complete actual prelaunch copy '+folder.name)
    check(o['actual_execution'] is True and o['completed'] is True and type(o['pid']) is int and o['pid']>0 and type(o['operator_pid']) is int and o['operator_pid']>0 and type(o['exit_code']) is int and o['exit_code']==0 and o['status']=='PASS','Genuine process '+folder.name)
    check(pre['source']==source_name and pre['argv']==['/usr/bin/python3','-B',str(P/source_name)] and pre['cwd']==str(P) and pre['stdin_supplied'] is False and pre['production_operations_authorized'] is False,'Exact actual launch '+folder.name)
    check((folder/'PRELAUNCH_SOURCE.py').read_bytes()==(P/source_name).read_bytes() and sha((folder/'PRELAUNCH_SOURCE.py').read_bytes())==pre['source_sha256'],'Full prelaunch source '+folder.name)
    # Historical operators are bound to their genuine prelaunch identity. Later
    # operator evolution does not rewrite the earlier actual launch source.
    check(sha((folder/'PRELAUNCH_OPERATOR.py').read_bytes())==pre['operator_sha256'],'Full historical prelaunch operator '+folder.name)
    if folder.name=='CLOSURE_ACTUAL_CAPTURE':check((folder/'PRELAUNCH_OPERATOR.py').read_bytes()==(P/'capture_owned_operation.py').read_bytes(),'Actual final closure operator equals current source')
    check(o['source_unchanged'] is True and o['operator_unchanged'] is True,'Unchanged actual launch source '+folder.name)
    check(dt.datetime.fromisoformat(pre['utc'])<=dt.datetime.fromisoformat(o['started_utc'])<=dt.datetime.fromisoformat(o['finished_utc'])<=dt.datetime.now(dt.timezone.utc),'Real capture UTC order '+folder.name)
    for k in ['stdout','stderr']:bound(folder,o[k])
    check((folder/'stderr.bin').read_bytes()==b'','Complete zero stderr '+folder.name)
    check(topology(folder,{'PRELAUNCH.json','PRELAUNCH_SOURCE.py','PRELAUNCH_OPERATOR.py','CAPTURE.json','stdout.bin','stderr.bin'}) is not None,'Exact6 actual capture '+folder.name)
    return {'path':folder.relative_to(R).as_posix(),'pid':o['pid'],'operator_pid':o['operator_pid'],'capture':pin(folder/'CAPTURE.json'),'prelaunch':pin(folder/'PRELAUNCH.json'),'source':pin(folder/'PRELAUNCH_SOURCE.py'),'operator':pin(folder/'PRELAUNCH_OPERATOR.py'),'stdout':pin(folder/'stdout.bin'),'stderr':pin(folder/'stderr.bin')}

def main():
    check(git('branch','--show-current')==b'main\n','Stay main');initial_head=git('rev-parse','HEAD');before=native()
    prep,pdirs=closure(P,'PREPARATION_MANIFEST.json',PREP,99);check(len(pdirs)==18 and pin(P/'PREPARATION_MANIFEST.json')['bytes']==16825,'Exact preparation100files/18dirs/16825bytes')
    cur,cdirs=closure(C,'MANIFEST.json','169f2825a8f730735627bdc33a43366c05e317fdf7ec4df4cd96a31e37329eb0',430)
    whole,wdirs=closure(W,'SELF_MANIFEST.json','ea6416b54945bf80d0a706cf878c8de707464ddcdaea66ae0e812868ff547c9f',96)
    deps=load(C/'CURRENT_DEPENDENCIES.json');check(len(deps['files'])==369 and pin(C/'CURRENT_DEPENDENCIES.json')['sha256']=='2c8d2ef1cd1846a0b82dce49b8c8891f6821ca129bd42ec20cf4fc45ae258c18','369 exact dependencies')
    for z in deps['files']:bound(A,z)
    inp=load(P/'INPUT_BINDINGS.json')
    for z in list(inp['pins'].values())+[inp[k] for k in ['closed_whole_manifest','closed_whole_report','closed_whole_result','closed_root_whole_inspection','previous_mirror','previous_post','previous_root_post']]:bound(R,z)
    foreign=load(W/'INDIVIDUAL_INPUTS.json')['files'];check(len(foreign)==964 and len({z['path'] for z in foreign})==964,'964 literal foreign identities')
    historic={'draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'}
    dated=load(A/'ROOT_CURRENT_INPUT_PREIMAGES.json');datedrows={z['path']:z for z in dated['files']};check(dated['current_head']==EPOCH,'Immutable epoch stays fixed')
    check(not historic&{z['path'] for z in foreign} and set(datedrows)-historic<={z['path'] for z in foreign},'964 has stable9 and excludes changing frozen4')
    for z in foreign:check(z['excluded_from_family_authorship'] is True,'Foreign explicitly excluded '+z['path']);bound(R,z)
    for n in sorted(historic):
        entry=git('ls-tree','-z',EPOCH,'--',n);fields,path=entry.decode().rstrip('\0').split('\t');mode,kind,blob=fields.split()
        check(entry.count(b'\0')==1 and path==n and mode=='100644' and kind=='blob','Immutable native Git path/mode '+n)
        body=git('show',EPOCH+':'+n);check(len(body)==datedrows[n]['bytes'] and sha(body)==datedrows[n]['sha256'],'Entire actual immutable native4 '+n)
    sources={n:(P/n).read_text() for n in ['pr44_guards.py','seal_final_evidence.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py','capture_root_final_operation.py']}
    lexical=[]
    for n,s in sources.items():
        ts=list(tokenize.tokenize(io.BytesIO(s.encode()).readline));stack=[]
        check(not [t for t in ts if t.type==tokenize.ERRORTOKEN and t.string.strip()],'Source lexical only '+n)
        for t in ts:
            if t.type==tokenize.OP and t.string in '([{':stack.append(t.string)
            elif t.type==tokenize.OP and t.string in ')]}':check(bool(stack) and {'(':')','[':']','{':'}'}[stack.pop()]==t.string,'Source delimiter only '+n)
        check(not stack,'Source delimiters close '+n);lexical.append({'source':n,'tokens':len(ts),'compiled':False,'imported':False,'executed':False})
    g,i,m,v,se,op=(sources[n] for n in ['pr44_guards.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py','seal_final_evidence.py','capture_root_final_operation.py'])
    scope='Incremental present accepted primary PR44 standard partial; original2/5, no new proof turn or historical reconstruction.'
    check('scope='+repr(scope) in g and 'scope='+repr(scope) in m,'M2 exact entire scope punctuation in writer and guard')
    check("snapshot_manifest_v2.json" in g and "snapshot_manifest_v2.json" in i and "snapshot_manifest.json" not in g+i,'M1 actual original snapshot filename')
    check("'prior_publication_doi':None" in v and "'full_target_resolved_in_prior_published_literature':False" in v and '10.4064' not in v,'44 no shifted43 scientific DOI residue')
    source_requirements=[('complete ROOT source verdict',"'complete_VERDICT_object':verdict"),('distinct adversary closure',"sm.parent not in {C,HERE}"),('actual prior post',"equal(rootpost['entire_post'],post)"),('immutable independent4',"historical_checked==historical"),('stable9 foreign',"(NATIVE-historical)<=names and not historical.intersection(names)"),('capture real source',"regular(cb,'PRELAUNCH_OPERATOR.py').read_bytes()==bound(root_authority['root_capture_operator'])"),('reviewed exact future operator',"bound(o['root_capture_operator'])==expected_operator"),('original noff parents',"[pre['main_before'],HEAD]"),('no unrelated real merge paths',"changed<="),('exact inventory derivation',"derive_inventory(parse(before),remote,record['utc'])"),('strict frozen special bits',"stat.S_IMODE(regular(base,n).stat().st_mode)==0o444"),('self-only exact topology',"d == expected"),('full saved plan rebuild',"equal(plan,rebuild_saved_mirror_plan(proposal,plan['created_at_utc'],before_state,before_history))"),('full prior typed proposal',"equal(proposal,expected)"),('full accepted typed receipt',"equal(o,expected)"),('actual sealer return binding',"'final_receipt_sha256':a.final_receipt_sha256"),('actual open ready remote',"'isDraft':False,'headRefOid':HEAD"),('no hidden compile',"def mirror_module(proposal)")]
    for label,literal in source_requirements:check(literal in g,'Source mechanism '+label)
    for label,literal in [('queued0/5 before',"cells[8].strip()=='queued' and cells[9].strip()=='0/5'"),('only selected3 queuecells',"set(changed)=={8,9,11}"),('automatic actual index',"show',':'+qpath"),('actual conflicted stage2',"show',':2:'+qpath"),('actual conflicted stage3',"show',':3:'+qpath"),('owned exact438',"g.canonical_names(frozen)"),('accepted lowercase after merged',"'state':'MERGED'"),('whole180 inventory',"g.derive_inventory(before_inv,observation,now)")]:check(literal in i,'Integration mechanism '+label)
    for label,literal in [('history before state',"g.write(history,old_history+plan['history_append_bytes'].encode())"),('all34 oldstates',"all(g.equal(plan['state_after'][k],v) for k,v in prior.items())"),('cooperative lock',"fcntl.LOCK_EX|fcntl.LOCK_NB"),('new only1',"len(plan['history_append'])==1"),('exact original2 ledger',"'used':2,'limit':5,'kind':'pr44_exact_original_two_turn_JSONL'"),('six ledgerhostiles',"('empty',b'',2,5)")]:check(literal in m,'Mirror mechanism '+label)
    for label,literal in [('whole history bytes',"history==old_history+plan['history_append_bytes'].encode()"),('entire typed state',"g.equal(current,plan['state_after'])"),('membership',"set(current)==set(old)|{g.ID}"),('fresh replay byte noop',"replay['state_after_bytes'].encode()==state"),('typed entire finalinventory',"g.equal(inventory,g.derive_inventory")]:check(literal in v,'Post mechanism '+label)
    check('renamex_np' in se and 'os.fsencode(target),4' in se and "output.parent==g.A and not output.exists()" in se,'Sealer absent-only macOS exact adjacent publication')
    names={z['path'] for z in cur['files']};overlay=names|{'reviewed_pending_administration/'+n for n in ['status.json','readiness.json','review/verdict.json']}|{'reviewed_pending_administration/MANIFEST.json','ACCEPTED_QUEUE_PATCH.json','CURRENT_ACCEPTANCE_SCOPE.md','CURRENT_CONTEXT_PRESENT.md','CURRENT_AUDIT_SCOPE_PRESENT.md'}
    check(len(overlay)==438 and len(overlay|{'acceptance.json','ACCEPTANCE.md'})==440,'Independent prospective438/440 count')
    snapshots=load(A/'snapshot_manifest_v2.json');check(snapshots['head']==HEAD and snapshots['base']==BASE and len(snapshots['files'])==18 and len(snapshots['changed_paths'])==19 and all('size' in z and 'bytes' not in z for z in snapshots['files']),'Actual original18 rows use size')
    for z in snapshots['files']:bound(A/'source_snapshot',z);bound(C/'original_archive',z)
    # Review all original sources as text/data only. No scientific runtime claim.
    for n in ['OBSTRUCTION.md','CURRENT_OBSTRUCTION_CONTEXT.md','SOURCE_PRECISION_QUALIFICATIONS.md']:(C/n).read_text()
    science=load(P/'SCIENTIFIC_SCOPE.json');check(science['original_substantive_attempts']==2 and type(science['original_substantive_attempts']) is int and science['turn_limit']==5 and science['new_substantive_attempts']==0 and science['audit_turns']==0 and len(science['exact_remaining_gaps'])==2 and science['full_problem_solved'] is False and science['novelty_claimed'] is False and science['prior_publication_doi'] is None,'Globally scoped UNSOLVED original2/5,new0,audit0 with both gaps')
    check(sha((C/'SOURCE_PRECISION_QUALIFICATIONS.md').read_bytes())==science['global_qualification_sha256'],'Exact global source/category/integral/history qualification')
    draft=load(P/'DRAFT_ROOT_IMMUTABLE_BINDINGS.json');plan=load(P/'DRAFT_FINAL_PLAN.json')
    flags=['root_full_current_read_completed','root_full_whole_read_completed','root_acceptance_source_review_completed','root_actual_PR43_predecessor_read_completed','independent_whole_current_pass']
    keys=['whole_manifest','root_whole_inspection','root_capture_operator','previous_mirror','previous_post','previous_root_post','acceptance_source_manifest','acceptance_source_verdict','root_source_inspection']
    check(draft['created_utc'] is None and all(draft[k] is None for k in keys) and all(draft[k] is False and plan[k] is False for k in flags) and plan['partial_valid'] is None and plan['immutable_evidence_references']==[],'Actual drafts reject future approval/no fabricated reference/clock')
    def approval_contract(o):
        if set(o)!=set(draft):raise ValueError('Unknown/missing keys')
        if o['status']!='ROOT_APPROVED_CLOSED_WHOLE_SOURCE_AND_ACTUAL_PR43_EVIDENCE':raise ValueError('Status')
        if any(o[k] is not True for k in flags):raise ValueError('Typed read flags')
        for k in keys:
            q=o[k]
            if type(q) is not dict or set(q)!={'path','bytes','sha256'} or type(q['bytes']) is not int or q['bytes']<0 or type(q['sha256']) is not str or not re.fullmatch('[0-9a-f]{64}',q['sha256']):raise ValueError('Exact reference')
            safe(q['path'])
        if type(o['created_utc']) is not str:raise ValueError('Actual UTC')
        d=dt.datetime.fromisoformat(o['created_utc'])
        if d.tzinfo is None or d.utcoffset()!=dt.timedelta(0) or d>dt.datetime.now(dt.timezone.utc):raise ValueError('Real UTC clock')
        for k in ['original_substantive_attempts','new_substantive_attempts','audit_turns']:
            if type(o[k]) is not int or o[k]!=draft[k]:raise ValueError('Exact typed scope')
        if o['mandatory_corrections']!=[]:raise ValueError('Mandatory correction')
    rejection('actual false/null draft',lambda:approval_contract(draft))
    # An in-memory hypothetical shape is explicitly not an authored ROOT record.
    shape=copy.deepcopy(draft);shape['status']='ROOT_APPROVED_CLOSED_WHOLE_SOURCE_AND_ACTUAL_PR43_EVIDENCE';shape['created_utc']=utc()
    for k in flags:shape[k]=True
    for k in keys:shape[k]={'path':'hypothetical/'+k+'.json','bytes':1,'sha256':'a'*64}
    approval_contract(shape)
    for k in flags:
        for bad in [False,None,1,'true']:
            q=copy.deepcopy(shape);q[k]=bad;rejection('approval '+k+'='+repr(bad),lambda q=q:approval_contract(q))
    for k in keys:
        for bad in [None,True,'yes',{}, {'path':'../escape','bytes':1,'sha256':'a'*64},{'path':'x','bytes':True,'sha256':'a'*64}]:
            q=copy.deepcopy(shape);q[k]=bad;rejection('reference '+k+'='+repr(bad),lambda q=q:approval_contract(q))
    for raw in [b'{"x":1,"x":2}',b'{"x":NaN}',b'{"x":Infinity}',b'{"x":1e999}']:rejection('strict JSON '+raw.decode(),lambda raw=raw:parse(raw))
    for bad in ['../escape','/absolute','a/../b','a//b','a/./b','a\\b','.git/x','__pycache__/x']:rejection('path '+bad,lambda bad=bad:safe(bad))
    ledger=(C/'turns.jsonl').read_bytes();original_turns=[parse(z) for z in ledger.splitlines()];check(len(original_turns)==2 and [z['turn'] for z in original_turns]==[1,2] and all(z['outcome']=='stalled' for z in original_turns),'Independent original two-turn ledger typed read')
    def ledger_contract(raw,used,limit):
        if type(raw) is not bytes or raw!=ledger or type(used) is not int or type(limit) is not int or used!=2 or limit!=5:raise ValueError('Exact2/5')
    for label,raw,u,l in [('empty',b'',2,5),('whitespace',b'\n',2,5),('invented',b'{"turn":1}\n',2,5),('bool used',ledger,True,5),('wrong used',ledger,1,5),('wrong limit',ledger,2,4)]:rejection('ledger '+label,lambda raw=raw,u=u,l=l:ledger_contract(raw,u,l))
    check(not typed_eq(True,1) and not typed_eq(1,1.0) and not typed_eq({'x':1},{'x':True}),'Typed equal defeats boolean/numeric aliases')
    for mode in range(0o10000):check((stat.S_IMODE(mode)==0o444)==(mode==0o444),'All4096 full mode predicates')
    probes=H/'PRIVATE_TOPOLOGY'/str(os.getpid());probes.mkdir(parents=True)
    (probes/'a').write_bytes(b'Private owned probe\n');topology(probes,{'a'})
    (probes/'empty').mkdir();rejection('unlisted empty directory',lambda:topology(probes,{'a'}));(probes/'empty').rmdir()
    (probes/'alias').symlink_to('a');rejection('symlink alias',lambda:topology(probes,{'a','alias'}));(probes/'alias').unlink()
    os.mkfifo(probes/'special');rejection('special file',lambda:topology(probes,{'a','special'}));(probes/'special').unlink()
    (probes/'a').chmod(0o2444);check(stat.S_IMODE((probes/'a').stat().st_mode)==0o2444 and stat.S_IMODE((probes/'a').stat().st_mode)!=0o444,'Actual private special-mode rejection');(probes/'a').chmod(0o444)
    old43=load(R/inp['previous_post']['path']);root43=load(R/inp['previous_root_post']['path']);mirror43=load(R/inp['previous_mirror']['path'])
    check(typed_eq(root43['entire_post'],old43) and root43['schema']=='pr43-root-complete-actual-post-inspection/v1' and root43['completed_primary_prs']==33 and root43['original_attempts']==0 and root43['program_completion_percent']==33/180*100,'Entire genuine43 ROOT record includes real schema/attempts/percentage')
    check(old43['targets']==34 and old43['consumed_substantive_turns']==41 and old43['primary_acceptances']==33 and old43['merge_commit']=='c60255489a342fae02c0acf3d1026255b47be3d1' and old43['merge_tree']=='fdc2bb213905051a430d24e13afb20e54fa9106a','Actual43 counters/head/tree')
    check(len(mirror43['entries'])==33 and len(mirror43['duplicate_mirrors'])==1 and mirror43['required_completed_prs']==sorted(z['pr'] for z in mirror43['entries']),'Entire prior33 primary/one oldduplicate')
    check(len(root43['all_six_real_phase_captures'])==6 and len(root43['current13'])==13 and all(root43[k] is True for k in ['all33_prior_states_and_full_history_prefix_preserved','current13_match_exact_allowed_acceptance_changes','canonical357_plus_manifest_fullbytes_modes','merge355_overlay_plus_queue_Git_bodies_and_parents','entire_current_inventory_reconstructed']),'All actual priorROOT mandatory fields inspected')
    for z in root43['all_six_real_phase_captures']:
        bound(R,z);p=R/z['path'];capt=load(p);check(capt['actual_execution'] is True and capt['completed'] is True and capt['status']=='PASS' and type(capt['pid']) is int and capt['pid']>0 and capt['exit_code']==0,'Prior phase genuine metadata '+p.parent.name)
        for stream in ['stdout','stderr']:bound(p.parent,capt[stream])
        check(sha((p.parent/'PRELAUNCH_SOURCE.py').read_bytes())==capt['source_sha256'],'Prior complete prelaunch source');pin(p.parent/'PRELAUNCH_SOURCE.py');pin(p.parent/'PRELAUNCH_OPERATOR.py')
    root44=load(A/'ROOT_WHOLE_CURRENT_REVIEW.json');check(typed_eq(root44,load(P/'EXPECTED_ROOT_WHOLE_REVIEW.json')) and pin(A/'ROOT_WHOLE_CURRENT_REVIEW.json')['sha256']=='54c0944b7e6892ed0e04cab2a58432feb2afbf3694a04073f036fbeda466d1dc','Exact corrected ROOT record')
    check(root44['actual_direct_four_operator_pid']==1084 and root44['direct_four_independent_ROOT_Git_checks_completed'] is True and len(root44['complete_dated_git_captures'])==8,'Direct actual ROOT1084 native4 eight captures')
    for z in root44['complete_dated_git_captures']:
        for k in ['stdout','stderr']:bound(R,z[k])
        check(z['actual_execution'] is True and z['completed'] is True and type(z['pid']) is int and z['pid']>0 and z['operator_pid']==1084 and z['exit_code']==0,'ROOT direct actual metadata')
    check(typed_eq(root44['complete_VERDICT_object'],load(W/'VERDICT.json')),'Whole verdict exact typed identity, without transfer')
    state=load(R/'unsolved_math_prioritization/state.json');inv=load(R/'draft_pr_publication_program_20260930/inventory.json')
    check(len(state)==34 and '2912' not in state and sum(z['turns_used'] for z in state.values())==41 and len(inv['items'])==180 and inv['completed_count']==33 and inv['current_pr']==44,'Actual fresh before34/41/33 and full inventory180')
    transition=load(P/'EXPECTED_NATIVE_TRANSITION.json');check(transition['after']=={'completed':34,'consumed_substantive_turns':43,'current_pr':45,'duplicate_mirrors':1,'primary_acceptances':34,'program_completion_estimate_percent':34/180*100,'targets':35},'Prospective exact counters35/43/34/next45')
    captures=[capture(P/f,n) for f,n in [('AUTHORING_ACTUAL_CAPTURE','author_sources.py'),('SOURCE_REPAIR_ACTUAL_CAPTURE','author_repair.py'),('CONTROLS_ACTUAL_CAPTURE','independent_controls.py'),('CLOSURE_ACTUAL_CAPTURE','close_source.py')]]
    check([z['pid'] for z in captures]==[99306,3789,8465,13133],'Exact four genuine source-authoring/control/closure child PIDs')
    delta=[]
    for n in ['pr44_guards.py','seal_final_evidence.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py','EXPECTED_ROOT_WHOLE_REVIEW.json','INPUT_BINDINGS.json']:delta.extend(difflib.unified_diff((P/'INITIAL_GENERATED_SOURCE'/n).read_text().splitlines(keepends=True),(P/n).read_text().splitlines(keepends=True),fromfile='INITIAL_GENERATED_SOURCE/'+n,tofile=n))
    check(''.join(delta)==(P/'SOURCE_REPAIR_DELTA.patch').read_text(),'Entire seven-file repair delta independently recomputed')
    check(git('rev-parse','HEAD')==initial_head and typed_eq(native(),before),'Native13 fullbytes/modes and actual main HEAD preserved')
    ref_list=sorted(refs.values(),key=lambda z:z['path'])
    (H/'INDIVIDUAL_INPUTS.json').write_text(json.dumps({'schema':'pr44-acceptance-source-adversary-individual-inputs/v1','resolution':'repository_root / files.path','files_count':len(ref_list),'files':ref_list,'foreign_raw_primary_private_bodies_copied':False,'all_foreign_inputs_hash_checked_in_place':True,'own_actual_native4_Git_stdout_is_first_party_procedural_evidence':True},ensure_ascii=False,sort_keys=True,indent=2)+'\n')
    result={'schema':'pr44-independent-acceptance-source-controls/v1','status':'PASS_HANDWRITTEN_SOURCE_CONTRACT_CONTROLS_ONLY','utc':utc(),'actual_operator_pid':os.getpid(),'preparation_manifest_sha256':PREP,'checks':len(checks),'hostile_rejections':len(hostile),'rejected_hostile_cases':hostile,'counts':{'preparation_members':99,'preparation_directories':18,'current_members':430,'current_dependencies':369,'whole_members':96,'foreign_individual_inputs':964,'prospective_overlay':438,'prospective_accepted_members':440,'prior_targets':34,'prior_turns':41,'prior_primaries':33,'future_targets':35,'future_turns':43,'future_primaries':34,'inventory_rows':180},'lexical_source_observations':lexical,'actual_preparation_captures':captures,'complete_actual_readonly_Git_queries':queries,'all_individual_inputs':len(ref_list),'main_HEAD_before':initial_head.decode().strip(),'main_HEAD_unchanged':True,'native13_fullbytes_and_modes_unchanged':True,'production_imported_compiled_executed':False,'future_acceptance_approved':False,'production_runtime_success_claimed':False,'whole_math_PASS_transferred':False,'root_personal_reading_claimed':False,'source_review_completion_percent':100,'acceptance_completion_percent':0,'discovery_completion_percent':0}
    (H/'CONTROL_RESULTS.json').write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
    with (H/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+utc()+' — Independent control checkpoint. Completion100% source review/0% acceptance/0% discovery. '+str(len(checks))+' handwritten/static/hash controls; '+str(len(hostile))+' hostile rejections; production imported/compiled/executed false. Complete actual process and readonly Git evidence retained.\n')
    print(json.dumps({'status':result['status'],'checks':len(checks),'hostile_rejections':len(hostile),'individual_inputs':len(ref_list),'actual_operator_pid':os.getpid(),'production_imported_compiled_executed':False,'future_acceptance_approved':False},sort_keys=True))
if __name__=='__main__':main()
