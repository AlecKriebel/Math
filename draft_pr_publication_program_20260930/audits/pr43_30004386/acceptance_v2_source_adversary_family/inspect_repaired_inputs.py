"""Fresh independent full-byte reader. No proposed source execution or import."""
from pathlib import Path, PurePosixPath
import ast, datetime as dt, hashlib, json, math, os, stat, subprocess

D=Path(__file__).resolve().parent;A=D.parent;R=A.parents[2]
V=A/'acceptance_preparation_family_v2';O=A/'acceptance_preparation_family'
W=A/'whole_current_source_first_family';C=A/'reviewed_candidate'
count=0;reads=[];gits=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def need(ok,message):
    global count
    count+=1
    if not ok:raise ValueError(message)
def parse(raw):
    def pairs(z):
        out={}
        for k,v in z:need(k not in out,'Duplicate JSON key '+k);out[k]=v
        return out
    def floating(x):
        v=float(x);need(math.isfinite(v),'Nonfinite float');return v
    return json.loads(raw,object_pairs_hook=pairs,parse_float=floating,
                      parse_constant=lambda x:(_ for _ in ()).throw(ValueError('Nonfinite '+x)))
def equal(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return a.keys()==b.keys() and all(equal(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
    return a==b
def read(p):
    p=Path(p);need(p.is_file() and not p.is_symlink(),'Regular file '+str(p))
    for ancestor in p.parents:need(not ancestor.is_symlink(),'Symlink ancestor')
    raw=p.read_bytes();reads.append({'path':str(p),'bytes':len(raw),'sha256':sha(raw),
      'classification':'foreign individually read, not copied','individual_exclusion':True})
    if p.name.endswith('.json'):parse(raw)
    if p.name.endswith('.jsonl'):
        need(not raw or raw.endswith(b'\n'),'Incomplete JSONL')
        for line in raw.splitlines():parse(line)
    return raw
def bound(base,row):
    n=row['path'];p=PurePosixPath(n)
    need(type(n) is str and not p.is_absolute() and p.as_posix()==n and not set(p.parts)&{'.','..','.git','__pycache__'},'Literal canonical member')
    size=row['bytes'] if 'bytes' in row else row['size']
    need(type(size) is int and size>=0,'Typed size')
    raw=read(base/n);need(len(raw)==size and sha(raw)==row['sha256'],'Entire bound body '+n);return raw
def closure(base,name,pin,members):
    raw=read(base/name);need(sha(raw)==pin,'Manifest pin '+name);obj=parse(raw)
    rows=obj['files'];need(type(rows) is list and len(rows)==members,'Member count')
    need(obj['self_excluded']==[name] and obj['files_count']==members and type(obj['files_count']) is int,'Literal self/count')
    names={z['path'] for z in rows};need(len(names)==members and name not in names,'Distinct member identities')
    for row in rows:bound(base,row)
    files=set();dirs=set()
    for p in base.rglob('*'):
        need(not p.is_symlink() and (p.is_file() or p.is_dir()),'Exact topology regular node')
        n=p.relative_to(base).as_posix();(files if p.is_file() else dirs).add(n)
        if p.is_file():need(stat.S_IMODE(p.stat().st_mode)==0o444,'Entire frozen mode0444 '+n)
    expected={q.as_posix() for n in names|{name} for q in PurePosixPath(n).parents if q.as_posix()!='.'}
    need(files==names|{name} and dirs==expected,'Entire recursive files/directories')
    return obj
def git(*tail):
    dest=D/('git_query_'+str(len(gits)+1));dest.mkdir();argv=['git',*tail]
    start=dt.datetime.now(dt.timezone.utc).isoformat()
    p=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
    out,err=p.communicate();end=dt.datetime.now(dt.timezone.utc).isoformat()
    rec={'argv':argv,'cwd':str(R),'pid':p.pid,'actual_execution':True,'completed':True,
      'started_utc':start,'finished_utc':end,'exit_code':p.returncode}
    for channel,raw in [('stdout',out),('stderr',err)]:
        (dest/(channel+'.bin')).write_bytes(raw);rec[channel]={'path':str(dest/(channel+'.bin')),'bytes':len(raw),'sha256':sha(raw)}
    (dest/'CAPTURE.json').write_text(json.dumps(rec,indent=2)+'\n');gits.append(rec);need(p.returncode==0,'Read-only Git query');return out
start_head=git('rev-parse','HEAD').decode().strip();need(git('branch','--show-current')==b'main\n','Main branch')
v=closure(V,'PREPARATION_MANIFEST.json','11f39e9d890bc1a65efb4fe64bd8bd1612774c746c42c3cafa9883629fe58e91',45)
old=closure(O,'PREPARATION_MANIFEST.json','4161032794d175f8e0cfc3b62b3d1567f172ca93abe590f43ef81576d6cd20f9',108)
ad=closure(A/'acceptance_source_adversary_family','SELF_MANIFEST.json','7c200634012ac198fbd643143e145a374837318a493d5d94e2e815faa3e096f2',119)
changes={
 'integrate_reviewed_partial.py':(b"g.A/'snapshot_manifest_v2.json'",b"g.A/'snapshot_manifest.json'"),
 'state_mirror_reconciliation.py':(b'primary PR43; source-status correction;',b'primary PR43 source-status correction;')}
production=['pr43_guards.py','seal_final_evidence.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py']
for n in production:
    before=read(O/n);after=read(V/n)
    if n in changes:
        x,y=changes[n];need(before.count(x)==1 and before.replace(x,y,1)==after,'Only exact one token repair '+n)
    else:need(before==after,'Unchanged production '+n)
    ast.parse(after,filename=n)
for n in ['DRAFT_ROOT_IMMUTABLE_BINDINGS.json','DRAFT_FINAL_PLAN.json','SCIENTIFIC_SCOPE.json','EXPECTED_CURRENT_ADMIN.json','EXPECTED_ROOT_WHOLE_REVIEW.json','EXPECTED_WHOLE_VERDICT.json']:
    need(read(O/n)==read(V/n),'Unchanged science/draft '+n)
native=read(R/'draft_pr_publication_program_20260930/infrastructure/accepted_state_sync/revision2/accepted_state_sync_v2.py')
need(sha(native)=='ca7576ece5bc37a6e569a62764541de773243d38bffa811f4d1174f25635667f','Native source anchor');ast.parse(native)
oldop=read(A/'capture_root_final_operation.py');newop=read(A/'capture_root_final_operation_v2.py')
need(oldop.count(b"A / 'acceptance_preparation_family'")==1 and oldop.replace(b"A / 'acceptance_preparation_family'",b"A / 'acceptance_preparation_family_v2'",1)==newop,'Only operator family replacement')
ast.parse(newop)
inp=parse(read(V/'INPUT_BINDINGS.json'));beforeinp=parse(read(O/'INPUT_BINDINGS.json'))
oldname='capture_root_final_operation.py';newname='capture_root_final_operation_v2.py'
expected=json.loads(json.dumps(beforeinp));expected['pins'].pop(oldname)
expected['pins'][newname]=inp['pins'][newname];expected['root_capture_operator']=inp['root_capture_operator']
need(equal(expected,inp),'Only two input operator references changed')
for ref in inp['pins'].values():bound(R,ref)
for name in ['closed_whole_manifest','closed_whole_result','closed_whole_report','closed_root_whole_inspection','root_capture_operator']:bound(R,inp[name])
need(equal(inp['required_future_PR42_predecessor'],{'previous_mirror':None,'previous_post':None,'previous_root_post':None}),'Future predecessor refsNULL')
candidate=closure(C,'MANIFEST.json','4849e6037a5db3dce546a656dcd57063ae83d782c19e24d4e3dff97ebbcdec14',347)
depsraw=read(C/'CURRENT_DEPENDENCIES.json');need(sha(depsraw)=='4cec33dfaee001419ccf07dc2483d3c8bdf67f0308e5601cbefb4e620c45337e','Dependencies anchor')
deps=parse(depsraw);need(len(deps['files'])==274,'All274 dependencies')
for ref in deps['files']:bound(A,ref)
snapshot=parse(read(A/'snapshot_manifest.json'));need(len(snapshot['files'])==16,'All16 original')
for ref in snapshot['files']:
    raw=bound(A/'source_snapshot',ref);need(raw==read(C/'original_archive'/ref['path']),'Full original archive')
need(read(C/'turns.jsonl')==b'','Original zero bytes');need(equal(parse(read(A/'pinned_prior_report.json')),{}),'Fallback{}')
whole=closure(W,'SELF_MANIFEST.json','af80fc4d9ce1bb3b282b193f8dbe3dfdd873184f7ffb1143c6b027419f6a0c2d',30)
hist={'draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'}
dated=parse(read(A/'ROOT_CURRENT_INPUT_PREIMAGES.json'));datedrows={x['path']:x for x in dated['files']}
seen=set();canonical=set();dateddone=set();foreign=whole['external_individually_excluded_inputs']
need(len(foreign)==756,'All756 foreign identities')
for ref in foreign:
    name=ref['path'];need(name not in seen,'Foreign literal unique');seen.add(name)
    need(type(name) is str and name.startswith(str(R)+'/') and '\\' not in name and '\0' not in name,'Absolute repository foreign')
    parts=name[len(str(R))+1:].split('/');need(all(p and p not in {'.git','__pycache__'} for p in parts),'Foreign components')
    current=R
    for i,part in enumerate(parts):
        need(current.is_dir() and not current.is_symlink(),'Real traversed parent')
        if part=='.':continue
        if part=='..':need(current!=R,'No escape prefix');current=current.parent
        else:current=current/part
        need(current.exists() and not current.is_symlink(),'Exists without symlink hop')
        need(current==R or R in current.parents,'Every prefix inside repository')
        if i<len(parts)-1:need(current.is_dir(),'Intermediate directory')
    need(current.is_file() and current.resolve()==current,'Canonical final regular');n=current.relative_to(R).as_posix();canonical.add(n)
    if n in hist:
        need(ref['bytes']==datedrows[n]['bytes'] and ref['sha256']==datedrows[n]['sha256'],'Actual dated freeze pin')
        tree=git('ls-tree','-z',dated['current_head'],'--',n).decode();field,literal=tree[:-1].split('\t');need(tree.endswith('\0') and literal==n and field.split()[:2]==['100644','blob'],'Exact immutable Git regular body')
        raw=git('show',dated['current_head']+':'+n);dateddone.add(n)
        reads.append({**ref,'classification':'foreign dated original project Git body; own actual query stream, not present authority'})
    else:raw=read(current)
    need(type(ref['bytes']) is int and len(raw)==ref['bytes'] and sha(raw)==ref['sha256'],'Complete foreign full body')
need(len(seen)==756 and dateddone==hist,'Exactly four historical inputs')
root=parse(read(A/'ROOT_WHOLE_CURRENT_REVIEW.json'));verdict=parse(read(W/'VERDICT.json'))
need(equal(root,parse(read(V/'EXPECTED_ROOT_WHOLE_REVIEW.json'))) and equal(root['complete_VERDICT_object'],verdict),'Complete ROOT whole verdict equality')
need(root['future_execution_approved'] is False and verdict['mandatory_defects']==[],'No future approval from priorwhole')
for name in ['AUTHORING_ACTUAL_CAPTURE','CONTROLS_ACTUAL_CAPTURE','CLOSURE_ACTUAL_CAPTURE']:
    cap=parse(read(V/name/'CAPTURE.json'));need(cap['actual_execution'] is True and cap['completed'] is True and cap['exit_code']==0,'Actual V2 own successful capture')
    need(type(cap['pid']) is int and cap['pid']>0,'Actual child PID')
    for channel in ['stdout','stderr']:bound(V/name,cap[channel])
    need(sha(read(V/name/'PRELAUNCH_SOURCE.py'))==cap['source_sha256'],'Actual prelaunch source')
finish_head=git('rev-parse','HEAD').decode().strip()
result={'schema':'PR43_V2_SOURCE_ADVERSARY_COMPLETE_INPUT_READING_v1','actual_pid':os.getpid(),
 'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'predicates':count,'complete_reads':len(reads),
 'cumulative_read_bytes':sum(x['bytes'] for x in reads),'all_individual_inputs':reads,
 'historical_Git_captures':gits,'preparation_members':45,'preserved_V1_members':108,
 'preserved_V1_adversary_members':119,'current_members':347,'dependencies':274,'original_files':16,
 'whole_members':30,'foreign_identities':756,'historical_native_bodies':4,
 'production_changes_exact_two_tokens':True,'unchanged_science_and_drafts':True,
 'old_main_head':start_head,'new_main_head':finish_head,'main_change_observation_only':start_head!=finish_head,
 'production_import_compile_execution':False,'future_predecessor_or_ROOT_approval_certified':False}
(D/'INPUT_READING_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['all_individual_inputs','historical_Git_captures']},indent=2))
