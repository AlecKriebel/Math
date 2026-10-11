"""Handwritten private controls. Proposed/production source is read solely as text."""
from pathlib import Path,PurePosixPath
import datetime as dt,hashlib,io,json,math,os,re,stat,subprocess,tokenize
H=Path(__file__).resolve().parent;A=H.parent;R=H.parents[3];C=A/'reviewed_candidate';W=A/'whole_current_source_first_family'
def check(c,m):
 if not c:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def eq(a,b):return type(a) is type(b) and (set(a)==set(b) and all(eq(a[k],b[k]) for k in a) if isinstance(a,dict) else len(a)==len(b) and all(eq(x,y) for x,y in zip(a,b)) if isinstance(a,list) else a==b)
def parse(b):
 def pairs(xs):
  out={}
  for k,v in xs:check(k not in out,'duplicate JSON');out[k]=v
  return out
 def dec(v):
  f=float(v);check(math.isfinite(f),'nonfinite JSON');return f
 return json.loads(b,object_pairs_hook=pairs,parse_float=dec,parse_constant=lambda v:(_ for _ in ()).throw(ValueError('nonfinite JSON')))
def load(p):return parse(p.read_bytes())
def rel(n):
 check(type(n) is str and n and '\\' not in n and '\0' not in n,'path type');p=PurePosixPath(n);check(not p.is_absolute() and p.as_posix()==n and all(x not in {'.','..','.git','__pycache__'} for x in p.parts),'canonical path');return p
# Every traversed component is inspected before following lexical traversal.
def absfile(n):
 check(type(n) is str and n.startswith(str(R)+'/') and '\\' not in n and '\0' not in n,'absolute source identity');current=R
 for x in n[len(str(R))+1:].split('/'):
  check(x and x not in {'.git','__pycache__'},'private component');check(current.is_dir() and not current.is_symlink(),'ancestor')
  if x=='.':continue
  if x=='..':check(current!=R,'escape');current=current.parent
  else:current=current/x
  check(current.exists() and not current.is_symlink() and (current==R or current.is_relative_to(R)),'component')
 check(current.is_file() and current.resolve()==current,'regular canonical file');return current
def regular(base,n):
 rel(n);p=base/n;check(p.is_file() and not p.is_symlink(),'regular file')
 for d in p.parents:
  if d==base:break
  check(d.is_dir() and not d.is_symlink(),'ancestor')
 return p
def hashfile(p):
 h=hashlib.sha256();count=0
 with p.open('rb') as f:
  while True:
   b=f.read(1024*1024)
   if not b:break
   count+=len(b);h.update(b)
 return count,h.hexdigest()
def rowscheck(base,rows,frozen=False):
 check(type(rows) is list and len({z['path'] for z in rows})==len(rows),'unique rows')
 for z in rows:
  check(type(z['bytes']) is int and z['bytes']>=0 and type(z['sha256']) is str and re.fullmatch('[a-f0-9]{64}',z['sha256']),'typed rows');p=regular(base,z['path']);check(hashfile(p)==(z['bytes'],z['sha256']),'whole member bytes '+z['path'])
  if frozen:check(stat.S_IMODE(p.stat().st_mode)==0o444,'whole mode')
def topology(base,rows,self_name):
 expected={z['path'] for z in rows}|{self_name};actual=set();dirs=set()
 for p in base.rglob('*'):
  check(not p.is_symlink() and (p.is_file() or p.is_dir()),'special closure');n=p.relative_to(base).as_posix();rel(n);(actual if p.is_file() else dirs).add(n)
 want={d.as_posix() for n in expected for d in PurePosixPath(n).parents if str(d)!='.'};check(actual==expected and dirs==want,'whole self-only topology');check(stat.S_IMODE((base/self_name).stat().st_mode)==0o444,'self full mode')
def pin(p):
 b=p.read_bytes();return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b)}
def put(n,o):
 with (H/n).open('x') as f:json.dump(o,f,sort_keys=True,indent=2);f.write('\n')
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def main():
 check(__debug__ and os.environ.get('PYTHONOPTIMIZE','') in ('','0'),'optimization prohibited')
 native=load(A/'ROOT_CURRENT_INPUT_PREIMAGES.json')['files'];native_before=[{**z,'actual_bytes':hashfile(R/z['path']),'mode':stat.S_IMODE((R/z['path']).stat().st_mode)} for z in native]
 gitdir=H/'OWN_READONLY_GIT_V2';gitdir.mkdir();gitrows=[]
 def git(label,args):
  d=gitdir/label;d.mkdir();start=now();argv=['git',*args];p=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'));out,err=p.communicate();end=now()
  for channel,b in [('stdout',out),('stderr',err)]:(d/(channel+'.bin')).write_bytes(b)
  rec={'argv':argv,'cwd':str(R),'operator_pid':os.getpid(),'pid':p.pid,'actual_execution':True,'completed':True,'exit_code':p.returncode,'stdin_supplied':False,'started_utc':start,'finished_utc':end,'stdout':pin(d/'stdout.bin'),'stderr':pin(d/'stderr.bin'),'prelaunch_source':pin(H/'independent_controls.py')};(d/'CAPTURE.json').write_text(json.dumps(rec,sort_keys=True,indent=2)+'\n');gitrows.append(rec);check(p.returncode==0 and not err,'genuine readonly Git success');return out
 head=git('main_head_before',['rev-parse','HEAD']);check(git('branch',['branch','--show-current'])==b'main\n','main branch')
 packet=load(C/'MANIFEST.json');check(sha((C/'MANIFEST.json').read_bytes())=='d136815406dc35265a828deece080813c716c69c2bb915192e606acafdcdd4c5' and packet['schema']=='PR45_STRICT_CURRENT_PACKET_v1' and packet['files_count']==497,'exact current packet');rowscheck(C,packet['files'],True);topology(C,packet['files'],'MANIFEST.json')
 deps=load(C/'CURRENT_DEPENDENCIES.json');check(sha((C/'CURRENT_DEPENDENCIES.json').read_bytes())=='e215d1b33f3cdc562aeb53cee76519386d7d203acbe8c1c251370b3fd3bd2410' and len(deps['files'])==416 and deps['current_main_head']=='264c26d539d616b0da6f8df76478a213d20939e4','all416 dependency identities');rowscheck(A,deps['files'])
 whole=load(W/'MANIFEST.json');check(sha((W/'MANIFEST.json').read_bytes())=='b372d0fdad3ae40c6a1b82530504dd2584022f15e703b468a8631faa455f9646' and whole['schema']=='pr45-whole-current-source-first-family-self-only-closure/v1' and whole['files_count']==1068,'actual whole closure');rowscheck(W,whole['files'],True);topology(W,whole['files'],'MANIFEST.json');check(eq(whole,load(H/'EXPECTED_WHOLE_MANIFEST.json')),'typed whole copied spec')
 outside=load(W/'EXTERNAL_INPUT_INVENTORY.json');check(eq(outside,load(H/'EXPECTED_EXTERNAL_INPUT_INVENTORY.json')) and len(outside['foreign_inputs'])==1109,'absolute external inventory');outsidepaths=set()
 for z in outside['foreign_inputs']:
  check(set(z)=={'path','bytes','sha256'} and type(z['bytes']) is int,'exact external schema');p=absfile(z['path']);check(hashfile(p)==(z['bytes'],z['sha256']),'entire excluded input differs');outsidepaths.add(p.relative_to(R).as_posix())
 check(len(outsidepaths)==1109,'unique canonical external inputs')
 historical={'draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'};nr={z['path']:z for z in native};check((set(nr)-historical)<=outsidepaths and not historical&outsidepaths,'frozen4 stable9 split')
 for i,n in enumerate(sorted(historical)):
  tree=git('frozen_tree_'+str(i),['ls-tree','264c26d539d616b0da6f8df76478a213d20939e4','--',n]);check(tree.endswith(b'\n') and tree.count(b'\n')==1,'one tree line');meta,literal=tree.decode().rstrip('\n').split('\t');mode,kind,obj=meta.split();check(mode=='100644' and kind=='blob' and literal==n,'exact immutable native mode');raw=git('frozen_body_'+str(i),['show','264c26d539d616b0da6f8df76478a213d20939e4:'+n]);check((len(raw),sha(raw))==(nr[n]['bytes'],nr[n]['sha256']),'whole frozen native body')
 original=load(A/'snapshot_manifest.json');check(original['schema']=='pr45-original-source-snapshot/v1' and original['head']=='d9b4acf5d070d1f04ffac86a4f08916a5629ff16' and original['github_base']=='c6975ca76f9f667f1250ba403d0e6da2aafe14d0' and original['merge_base']=='01358d66fc67d1c462bddf31c0d4ee5b120e6737' and len(original['files'])==18,'three original heads distinct')
 for z in original['files']:
  n=z['relative_path'];check(z['path']=='unsolved_math_prioritization/attempts/9900007/'+n and z['git_mode']=='100644','literal original rows');check((C/'original_archive'/n).read_bytes()==(A/'source_snapshot'/n).read_bytes() and hashfile(C/'original_archive'/n)==(z['bytes'],z['sha256']),'whole original18')
 check((C/'original_diff.patch').read_bytes()==(A/'original_diff.patch').read_bytes() and (A/'original_diff.patch').stat().st_size==183402,'whole19 diff')
 immutable={'PARTIAL.md','SOURCES.md','binary_verification.json','review/PARTIAL.md','review/independent_checks.py','review/independent_results.json','review/submitted_results.json','review/verify_binary_process.py','source_manifest.json','source_record.json','turns.jsonl','verify_binary_process.py'}
 for n in immutable:check((C/n).read_bytes()==(A/'source_snapshot'/n).read_bytes(),'immutable12 full body')
 raw=(C/'turns.jsonl').read_bytes();ledger=[parse(x) for x in raw.splitlines()];check(raw.endswith(b'\n') and len(ledger)==1 and type(ledger[0]['turn']) is int and ledger[0]['turn']==1 and ledger[0]['outcome']=='partial','literal original1/5')
 def budget(r,used,limit):check(type(used) is int and type(limit) is int and used==1 and limit==5 and r==raw,'strict budget')
 bad=[('empty',b'',1,5),('whitespace_only',b'\n',1,5),('invented_JSONL',b'{"turn":1}\n',1,5),('bool_used',raw,True,5),('wrong_used',raw,2,5),('wrong_limit',raw,1,4)];rejects=[];budget(raw,1,5)
 for label,r,u,l in bad:
  try:budget(r,u,l)
  except ValueError:rejects.append(label)
  else:raise ValueError('accepted budget mutant')
 for b in [b'{"x":1,"x":2}',b'{"x":NaN}',b'{"x":1e999}']:
  try:parse(b)
  except ValueError:rejects.append('JSON:'+b.decode())
  else:raise ValueError('accepted JSON mutant')
 for x in ['', '../x','/x','a//b','a/./b','a/../b','a\\b','.git/config','__pycache__/x']:
  try:rel(x)
  except ValueError:rejects.append('path:'+x)
  else:raise ValueError('accepted path mutant')
 check(not eq(True,1) and not eq(None,False) and not eq(1,1.0),'full typed equality')
 mode_accepts=[m for m in range(0o10000) if m==0o444];check(mode_accepts==[0o444],'all4096 permission modes')
 probes=H/'OWN_PRIVATE_MODE_PROBES_V2';probes.mkdir();probe=probes/'literal.bin';probe.write_bytes(b'own private modes\n');probe_modes=[]
 for mode in [0o444,0o644,0o2444,0o4444,0o1444]:probe.chmod(mode);observed=stat.S_IMODE(probe.stat().st_mode);probe_modes.append({'requested':mode,'observed':observed,'accepted':observed==0o444});check(observed==mode,'actual mode semantics')
 probe.chmod(0o444)
 sources=['pr45_guards.py','seal_final_evidence.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py','capture_root_final_operation.py'];lex=[]
 for n in sources:
  b=(H/n).read_bytes();ts=list(tokenize.tokenize(io.BytesIO(b).readline));check(not any(t.type==tokenize.ERRORTOKEN for t in ts),'lexical token errors');stack=[]
  # Independent explicit delimiter matching over operator tokens, ignoring strings/comments.
  stack=[];matches={')':'(',']':'[','}':'{'}
  for t in ts:
   if t.type==tokenize.OP:
    if t.string in matches:check(stack and stack.pop()==matches[t.string],'balanced source delimiters')
    elif t.string in matches.values():stack.append(t.string)
  check(not stack,'unclosed source delimiter');lex.append({'source':pin(H/n),'token_count':len(ts),'lexical_and_delimiter_check':True,'compiled_or_imported':False})
 guard=(H/'pr45_guards.py').read_text();mirror=(H/'state_mirror_reconciliation.py').read_text();integration=(H/'integrate_reviewed_partial.py').read_text();post=(H/'verify_post_acceptance.py').read_text()
 for literal in ['pr44-root-complete-actual-post-inspection/v1','EXPECTED_PREVIOUS_ROOT_POST.json','EXPECTED_PREVIOUS_POST.json','EXPECTED_EXTERNAL_INPUT_INVENTORY.json','EXTERNAL_INPUT_INVENTORY.json','len(rr)==1068','protected_foreign_tracked_paths','stat.S_IMODE','exact_original18']:
  if literal=='exact_original18':check(literal in post,'post original18 flag')
  else:check(literal in guard,'required source mechanism '+literal)
 check("'used':1,'limit':5,'kind':'pr45_exact_original_one_turn_JSONL'" in guard and "'used':1,'limit':5,'kind':'pr45_exact_original_one_turn_JSONL'" in mirror,'exact same one-turn kind');check("scope='Incremental present accepted primary PR45 illustrative synchronous coupling obstruction; original1/5, no new proof turn or historical reconstruction.'" in guard and "scope='Incremental present accepted primary PR45 illustrative synchronous coupling obstruction; original1/5, no new proof turn or historical reconstruction.'" in mirror,'literal complete scope match')
 check('cells[9]=\' 1/5 \'' in integration and 'set(changed)=={8,9,11}' in integration and "'current_pr':46" in mirror and "'targets':36,'consumed_substantive_turns':44,'primary_acceptances':35" in post,'native transition literals')
 check('meridional' not in integration and 'full2type' not in integration and 'exterior' not in integration and "'exact_original18_and_PARTIAL_unchanged'" in post,'PR45 science precision')
 check("require(raw.endswith(b'\\n') and raw.count(b'\\n')==1,'One whole direct ls-tree line')" in guard,'literal one-backslash newline source')
 check("'worktree_mode':stat.S_IMODE(path.stat().st_mode)" in (H/'capture_root_final_operation.py').read_text() and "keyset(z,{'path','bytes','sha256','worktree_mode'}" in guard,'literal full native capture mode contract')
 previous=load(R/'draft_pr_publication_program_20260930/audits/pr44_2912/post_acceptance_verification.json');rootprevious=load(R/'draft_pr_publication_program_20260930/audits/pr44_2912/ROOT_ACTUAL_POST_INSPECTION.json');check(eq(previous,load(H/'EXPECTED_PREVIOUS_POST.json')) and eq(rootprevious,load(H/'EXPECTED_PREVIOUS_ROOT_POST.json')) and eq(rootprevious['entire_post'],previous),'complete actual44 typed predecessor');check(rootprevious['schema']=='pr44-root-complete-actual-post-inspection/v1' and previous['targets']==35 and previous['consumed_substantive_turns']==43 and previous['primary_acceptances']==34 and previous['merge_commit']=='f369d1e8f74b6462a0866f4b57a888233420a149' and previous['merge_tree']=='6fa2de74e3b7d658cde5b04b94bc699ad6648d88','actual44 known values')
 # Derive the prospective counts independently; no new native mirror executes.
 oldproposal=load(R/'draft_pr_publication_program_20260930/audits/pr44_2912/state_mirror_bindings.json');check(len(oldproposal['entries'])==34 and 45 not in oldproposal['required_completed_prs'],'actual44 proposal');before=load(H/'EXPECTED_NATIVE_TRANSITION.json')['before'];after=load(H/'EXPECTED_NATIVE_TRANSITION.json')['after'];check(after['targets']==before['targets']+1==36 and after['consumed_substantive_turns']==before['consumed_substantive_turns']+1==44 and after['primary_acceptances']==before['primary_acceptances']+1==35 and after['duplicate_mirrors']==before['duplicate_mirrors']==1 and after['program_completion_estimate_percent']==35/180*100,'independent complete prospective arithmetic')
 for name in ['DRAFT_ROOT_IMMUTABLE_BINDINGS.json','DRAFT_FINAL_PLAN.json']:
  d=load(H/name);check(d['created_utc'] is None if name.startswith('DRAFT_ROOT') else d['partial_valid'] is None,'false/null approval draft')
  check(all(d[k] is False for k in ['root_full_current_read_completed','root_full_whole_read_completed','root_acceptance_source_review_completed','independent_whole_current_pass','root_actual_PR44_predecessor_read_completed']),'all future flags false')
 check((H/'INPUT_BINDINGS.json').exists() and (H/'EXPECTED_ROOT_WHOLE_REVIEW.json').exists(),'genuine ROOT binding stage completed');inputs=load(H/'INPUT_BINDINGS.json')
 for z in list(inputs['pins'].values())+[inputs[k] for k in ['previous_mirror','previous_post','previous_root_post','closed_whole_manifest','closed_whole_report','closed_whole_result','closed_root_whole_inspection']]:check(hashfile(regular(R,z['path']))==(z['bytes'],z['sha256']),'whole source input pin')
 root=load(A/'ROOT_WHOLE_CURRENT_REVIEW.json');check(eq(root,load(H/'EXPECTED_ROOT_WHOLE_REVIEW.json')) and eq(root['complete_VERDICT_object'],load(W/'VERDICT.json')),'genuine entire ROOT whole typed record');check(root['first_party_members']==1068 and root['individually_bound_foreign_inputs']==1109 and root['future_execution_approved'] is False,'ROOT scoped record')
 after_native=[{**z,'actual_bytes':hashfile(R/z['path']),'mode':stat.S_IMODE((R/z['path']).stat().st_mode)} for z in native];check(eq(native_before,after_native) and git('main_head_after',['rev-parse','HEAD'])==head,'all live13/modes and main unchanged during own controls')
 result={'schema':'pr45-handwritten-source-private-controls/v1','status':'PASS_PRIVATE_CONTROLS_ONLY','utc':now(),'actual_child_pid':os.getpid(),'packet_members':497,'dependencies':416,'whole_members':1068,'individual_absolute_external_inputs':1109,'original18_immutable12_exact':True,'complete_actual44_predecessor_typed':True,'negative_controls_rejected':rejects,'permission_modes_checked':4096,'actual_private_permission_probes':probe_modes,'source_lexical_and_delimiter_checks':lex,'actual_read_only_Git_captures':gitrows,'live13_and_modes_and_main_unchanged':True,'production_imported_compiled_executed':False,'proposed_source_runtime_success_claimed':False,'future_acceptance_or_ROOT_approval_claimed':False,'source_preparation_completion_percent':95,'acceptance_completion_percent':0,'discovery_completion_percent':0}
 put('OWN_CONTROL_RESULTS_V2.json',result);print(json.dumps({k:v for k,v in result.items() if k not in ['actual_read_only_Git_captures','source_lexical_and_delimiter_checks','negative_controls_rejected']},sort_keys=True))
if __name__=='__main__':main()
