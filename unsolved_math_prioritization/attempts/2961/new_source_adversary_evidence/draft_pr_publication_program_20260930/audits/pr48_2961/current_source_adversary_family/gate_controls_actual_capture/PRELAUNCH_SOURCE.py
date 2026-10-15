"""Private synthetic gate/queue controls and complete existing actual-capture readback.
No production/helper import, compile or execution; synthetic records grant no approval.
"""
import copy,datetime as dt,hashlib,json,math,os,re,stat
from pathlib import Path,PurePosixPath
F=Path(__file__).absolute().parent;A=F.parent;S=A/'current_preparation_family';R=A.parents[2];labels=[];bindings={}
def need(v,n):
 if not v:raise ValueError(n)
def check(v,n):need(v,n);labels.append(n)
def reject(f,n):
 try:f()
 except (ValueError,TypeError,KeyError,OSError):labels.append('Reject '+n);return
 raise ValueError('Accepted malformed '+n)
def sha(b):return hashlib.sha256(b).hexdigest()
def body(p):
 need(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'Regular nonsymlink');b=p.read_bytes();r={'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b),'full_mode':stat.S_IMODE(p.stat().st_mode)};need(r['path'] not in bindings or bindings[r['path']]==r,'Repeated unchanged body');bindings[r['path']]=r;return b
def load(b):
 def pairs(items):
  d={}
  for k,v in items:need(k not in d,'No duplicate JSON');d[k]=v
  return d
 def constant(n):raise ValueError('Nonfinite')
 return json.loads(b,object_pairs_hook=pairs,parse_constant=constant)
def clock(v):
 need(type(v) is str,'Typed UTC');t=dt.datetime.fromisoformat(v.replace('Z','+00:00'));need(t.tzinfo is not None and t.utcoffset()==dt.timedelta(0),'Aware UTC');return t
def safe(n):
 need(type(n) is str and n and '\\' not in n and '\0' not in n,'Text path');p=PurePosixPath(n);need(not p.is_absolute() and str(p)==n and not set(p.parts)&{'.','..','.git','__pycache__'},'Canonical path');return n
def row(r):
 need(type(r) is dict and set(r)=={'path','bytes','sha256','full_mode'},'Exact mode row');safe(r['path']);need(type(r['bytes']) is int and r['bytes']>=0 and type(r['sha256']) is str and re.fullmatch('[0-9a-f]{64}',r['sha256']) and type(r['full_mode']) is int and 0<=r['full_mode']<4096,'Typed row scalars')
def rows(rr):
 need(type(rr) is list,'Typed rows list');ns=set()
 for r in rr:row(r);need(r['path'] not in ns,'No duplicate rows');ns.add(r['path'])
 return ns
HEAD='e2e5c8c3e5ad218f867fa753c465bb96b3687bda';BASE='c6975ca76f9f667f1250ba403d0e6da2aafe14d0';MERGE='60292bed09f59236aa192cb17aa138f7b4750e1a'
NATIVE={'unsolved_math_prioritization/'+n for n in ['QUEUE.md','state.json','history.jsonl','catalog.json','assessments.json','queue.py','policy.json','manifest.json','cache/problems.json','cache/research_results.json','cache/catalog.sqlite','review_v2/related_target_groups.json']}|{'draft_pr_publication_program_20260930/inventory.json'}
HEADER=['Rank','ID / code','Problem','EV','Impact (/10)','Difficulty','Proposed','Status','Turns','Chat','Findings','DOI']
FLAGS=['original17_complete18_path_diff_helpers_results_metadata_fully_read','complete_partial_compression_support_stabilization_scope_checked','raw_all15458_SQL_both_report_keys_ABSENT_literal_empty_fallback_fully_read','actual_ROOT38_Git_and_four_literal_historical_final_replays_fully_read','both_closed_independent_mathematical_family_reports_fully_read','duplicate_exact_target_shared2of5_budget_accepted','operative_provenance_review_and_historical_receipt_qualifications_fully_read','new_source_adversary_closed_clean_complete_report_personally_read']
m=load(body(S/'PREPARATION_MANIFEST.json'));mf=sha(body(S/'PREPARATION_MANIFEST.json'));qual=sha(body(S/'SOURCE_PRECISION_QUALIFICATIONS.md'));start=clock(m['created_utc']);stamp=dt.datetime.now(dt.timezone.utc).isoformat()
def common(o,schema):
 need(o['schema']==schema and o['approved_by_root'] is True and o['operative_preparation_directory']=='current_preparation_family' and start<=clock(o['created_utc'])<=dt.datetime.now(dt.timezone.utc) and o['preparation_manifest_sha256']==mf and o['source_qualification_sha256']==qual,'ROOT common')
def science(o):
 common(o,'pr48-root-science-card/v1');need(o['status']=='unsolved' and o['full_problem_solved'] is False and o['project_solved'] is False and o['novelty_claimed'] is False and o['duplicate_id']==30004403 and o['duplicate_shared_budget'] is True,'Exact partial')
 for k,v in [('original_substantive_attempts',2),('turn_limit',5),('new_substantive_attempts',0),('audit_turns',0)]:need(type(o[k]) is int and o[k]==v,'Typed shared budget')
 for k in ['paper_created','new_DOI_created','tracker_row_created']:need(o[k] is False,'No paper DOI tracker')
 for k in ['current_model','current_reasoning_effort','current_deadline_utc','current_verdict']:need(o[k] is None,'No fabricated runtime')
 need(o['new_whole_current_gate']=='PENDING','Future gate pending')
def reading(o):
 common(o,'pr48-root-primary-read-ledger/v1');need(o['reading_completed'] is True and json.dumps(o['root_flags'],sort_keys=True)==json.dumps({n:True for n in FLAGS},sort_keys=True) and type(o['reading_notes']) is str and len(o['reading_notes'].strip())>=40,'Personal full reading flags')
def fresh(o):
 need(type(o) is dict and set(o)=={'schema','approved_by_root','created_utc','reason','current_head','files','operative_preparation_directory'} and o['schema']=='pr48-root-fresh13-input-preimages/v1' and o['approved_by_root'] is True and o['operative_preparation_directory']=='current_preparation_family' and start<=clock(o['created_utc'])<=dt.datetime.now(dt.timezone.utc) and type(o['reason']) is str and len(o['reason'].strip())>=40 and type(o['current_head']) is str and re.fullmatch('[0-9a-f]{40}',o['current_head']) and rows(o['files'])==NATIVE and len(o['files'])==13,'Fresh13 exact synthetic authority')
def scope(s):
 need(type(s) is str and s.splitlines()[0]=='# ROOT PR48 exact unresolved partial acceptance' and s.splitlines().count('ROOT_SCOPE_ACCEPTED_EXACT_UNSOLVED_PARTIAL_ONLY')==1 and 'DRAFT' not in s,'Scope sentinel')
 for x in [HEAD,BASE,MERGE,'Status: unsolved','Original shared turns: 2/5; new: 0; audit: 0','Full target resolved: false','Novelty: false','Duplicate: 30004403 / OWR-17471-009','NEW whole-current review: PENDING','Paper/new DOI/tracker: false']:need(x in s,'Scope literal')
def queue(b):
 ls=b.splitlines(keepends=True);ix={n:HEADER.index(n)+1 for n in HEADER};need(sum(l.startswith(b'|') and [v.strip() for v in l.decode().split('|')[1:-1]]==HEADER for l in ls)==1,'Unique queue header');repl={};absent=[]
 for label in ['2961 / KP-4.85','30004403 / OWR-17471-009']:
  hits=[(l,l.decode().split('|')) for l in ls if l.startswith(b'|') and len(l.decode().split('|'))==len(HEADER)+2 and l.decode().split('|')[ix['ID / code']].strip()==label]
  if label.startswith('30004403') and not hits:absent.append(label);continue
  need(len(hits)==1,'Unique target row');old,ff=hits[0];need(ff[ix['Status']].strip()=='queued' and ff[ix['Turns']].strip()=='0/5','Exact queued preimage');new=list(ff)
  for k,v in [('Status','unsolved'),('Turns','2/5'),('Findings','PRIVATE synthetic UNSOLVED partial shared2/5 new0 audit0')]:new[ix[k]]=' '+v+' '
  check(all(x==y for i,(x,y) in enumerate(zip(ff,new)) if i not in {ix['Status'],ix['Turns'],ix['Findings']}),'Preserve every other queue field');repl[old]='|'.join(new).encode()
 return b''.join(repl.get(l,l) for l in ls),absent
base={'schema':'pr48-root-science-card/v1','approved_by_root':True,'operative_preparation_directory':'current_preparation_family','created_utc':stamp,'preparation_manifest_sha256':mf,'source_qualification_sha256':qual,'status':'unsolved','full_problem_solved':False,'project_solved':False,'novelty_claimed':False,'duplicate_id':30004403,'duplicate_shared_budget':True,'original_substantive_attempts':2,'turn_limit':5,'new_substantive_attempts':0,'audit_turns':0,'paper_created':False,'new_DOI_created':False,'tracker_row_created':False,'current_model':None,'current_reasoning_effort':None,'current_deadline_utc':None,'current_verdict':None,'new_whole_current_gate':'PENDING'}
science(base);check(True,'Private synthetic science positive; never actual ROOT approval')
for k,vv in {'approved_by_root':[False,1,None],'created_utc':[None,'2026-10-03T01:00:00+00:00','2099-01-01T00:00:00+00:00','2026-10-03T06:00:00'],'preparation_manifest_sha256':['0'*64,None],'source_qualification_sha256':['0'*64,None],'full_problem_solved':[1,True,None],'project_solved':[1,True,None],'novelty_claimed':[1,True,None],'duplicate_shared_budget':[1,False,None],'new_whole_current_gate':['PASS',None],'current_verdict':['PASS',False],'current_model':['gpt-6',False],'paper_created':[True,0,None]}.items():
 for v in vv:b=copy.deepcopy(base);b[k]=v;reject(lambda b=b:science(b),'science '+k+' '+repr(v))
for k in ['original_substantive_attempts','turn_limit','new_substantive_attempts','audit_turns']:
 for v in [True,False,float(base[k]),str(base[k]),None,base[k]+1]:b=copy.deepcopy(base);b[k]=v;reject(lambda b=b:science(b),'integer budget '+k+' '+repr(v))
rd=dict(base,schema='pr48-root-primary-read-ledger/v1',reading_completed=True,root_flags={n:True for n in FLAGS},reading_notes='PRIVATE synthetic predicate test, not an actual ROOT record or reading approval.')
reading(rd);check(True,'Private exact8 reading flags positive')
for n in FLAGS:
 for v in [1,False,None,'true']:b=copy.deepcopy(rd);b['root_flags'][n]=v;reject(lambda b=b:reading(b),'reading flag '+n+' '+repr(v))
ff={'schema':'pr48-root-fresh13-input-preimages/v1','approved_by_root':True,'created_utc':stamp,'reason':'PRIVATE synthetic fixture only; never records or reads native inputs.','current_head':'a'*40,'files':[{'path':n,'bytes':0,'sha256':'0'*64,'full_mode':420} for n in sorted(NATIVE)],'operative_preparation_directory':'current_preparation_family'}
fresh(ff);check(True,'Private13 path list positive without reading native bodies')
for i in range(13):
 for k,v in [('path','../escape'),('bytes',True),('bytes',-1),('sha256','A'*64),('full_mode',True),('full_mode',4096),('extra',0)]:b=copy.deepcopy(ff);b['files'][i][k]=v;reject(lambda b=b:fresh(b),'fresh13 row'+str(i)+' '+k)
for mutate in ['duplicate','missing','extra_key','wrong_head','wrong_schema']:
 b=copy.deepcopy(ff)
 if mutate=='duplicate':b['files'][1]=copy.deepcopy(b['files'][0])
 elif mutate=='missing':b['files'].pop()
 elif mutate=='extra_key':b['extra']=True
 elif mutate=='wrong_head':b['current_head']='a'*39
 else:b['schema']='historical'
 reject(lambda b=b:fresh(b),'fresh13 '+mutate)
ss='\n'.join(['# ROOT PR48 exact unresolved partial acceptance','ROOT_SCOPE_ACCEPTED_EXACT_UNSOLVED_PARTIAL_ONLY',HEAD,BASE,MERGE,'Status: unsolved','Original shared turns: 2/5; new: 0; audit: 0','Full target resolved: false','Novelty: false','Duplicate: 30004403 / OWR-17471-009','NEW whole-current review: PENDING','Paper/new DOI/tracker: false'])
scope(ss);check(True,'Private scope sentinel positive')
for bad in [ss+'\nDRAFT',ss+'\nROOT_SCOPE_ACCEPTED_EXACT_UNSOLVED_PARTIAL_ONLY',ss.replace(MERGE,HEAD),ss.replace('PENDING','PASS'),ss.replace('Status: unsolved','Status: claimed_solved')]:reject(lambda bad=bad:scope(bad),'private scope alteration')
header='| '+' | '.join(HEADER)+' |\r\n';original=body(A/'original_queue_in_head.md');q,a=queue(original);check(a==['30004403 / OWR-17471-009'] and q.count(b'30004403 / OWR-17471-009')==0 and q!=original,'Actual ORIGINAL queue duplicate absent, private proposal does not invent a row')
qrows=[l for l in original.splitlines(keepends=True) if l.startswith(b'|') and b'2961 / KP-4.85' in l];need(len(qrows)==1,'Original target once')
for bad in [original+qrows[0],original.replace(qrows[0],b''),original+header,original.replace(b'| 2961 / KP-4.85',b'| 2961 / KP-4.85').replace(qrows[0],qrows[0].replace(b'queued',b'unsolved'))]:reject(lambda bad=bad:queue(bad),'queue malformed preimage')
# All private and ROOT actual capture bodies/streams are read in full AFTER their child exits.
external=[]
for dirname,expected_pid in [('root_pr48_current_source_closure_actual_capture',50088),('root_pr48_current_source_closed_readback_actual_capture',50493)]:
 d=A.parent/'pr45_9900007'/dirname;need({p.name for p in d.iterdir()}=={'CAPTURE.json','stdout.bin','stderr.bin','prelaunch_operator.py'},'Actual external four-member inventory');c=load(body(d/'CAPTURE.json'));need(c['schema']=='root-explicit-command-capture/v1' and type(c['pid']) is int and c['pid']==expected_pid and type(c['exit_code']) is int and c['exit_code']==0 and c['actual_execution'] is True and c['completed'] is True and c['stdin_supplied'] is False and c['operator_unchanged'] is True and c['status']=='PASS' and clock(c['started_utc'])<=clock(c['finished_utc'])<=dt.datetime.now(dt.timezone.utc),'True ROOT completed external capture')
 need(sha(body(d/'prelaunch_operator.py'))==c['operator_sha256'],'External actual preserved operator')
 for k in ['stdout','stderr']:b=body(d/(k+'.bin'));need(len(b)==c[k]['bytes'] and sha(b)==c[k]['sha256'] and c[k]['path']==k+'.bin','Entire external stream')
 need(c['stderr']['bytes']==0,'ROOT source closure stderr empty');external.append(c);check(True,'Complete ROOT source actual '+str(expected_pid))
need(clock(external[0]['finished_utc'])<clock(external[1]['started_utc']) and sha(body(A/'ROOT_CURRENT_SOURCE_CLOSURE_PRELAUNCH_SOURCE.py'))==sha(body(S/'close_source_preparation.py')),'Separate postexit readback and true closer prelaunch')
private=[]
for dirname,code,pid in [('controls_actual_capture',1,58409),('controls_actual_capture_v2',1,61867),('controls_actual_capture_v3',0,62526)]:
 d=F/dirname;c=load(body(d/'CAPTURE.json'));pre=load(body(d/'PRELAUNCH.json'));need({p.name for p in d.iterdir()}=={'CAPTURE.json','PRELAUNCH.json','PRELAUNCH_SOURCE.py','PRELAUNCH_OPERATOR.py','stdout.bin','stderr.bin'},'Private actual six-member topology');need(c['pid']==pid and type(c['pid']) is int and c['exit_code']==code and type(c['exit_code']) is int and c['actual_execution'] is True and c['completed'] is True and c['source_unchanged'] is True and c['operator_unchanged'] is True and c['stdin_supplied'] is False and c['production_import_compile_or_execution'] is False and clock(c['started_utc'])<=clock(c['finished_utc'])<=dt.datetime.now(dt.timezone.utc),'Complete retained private actual exit');need(pre['argv']==c['argv'] and pre['source_sha256']==sha(body(d/'PRELAUNCH_SOURCE.py'))==c['source_sha256'] and pre['operator_sha256']==sha(body(d/'PRELAUNCH_OPERATOR.py'))==c['operator_sha256'],'Exact private prelaunch binding')
 for k in ['stdout','stderr']:b=body(d/(k+'.bin'));need(len(b)==c[k]['bytes'] and sha(b)==c[k]['sha256'],'Entire private stream retained')
 private.append(c);check(True,'Complete private actual '+str(pid)+' exit'+str(code))
# Explicit representation/substitution negatives separate from production execution.
for c in load(body(A/'root_original_actual_reproduction_v2/ROOT_REPRODUCTION_RESULT.json'))['complete_actual_Git_captures']:
 need(c['source'] is None and c['source_unchanged'] is None,'Every38 genuine Git null positive')
 for bad in [dict(c,source={}),dict(c,source=False),dict(c,source_unchanged=True),dict(c,source_unchanged=False)]:reject(lambda bad=bad:need(bad['source'] is None and bad['source_unchanged'] is None,'Null Git convention'),'Git/helper substitution '+str(c['pid']))
for n in ['DRAFT_ROOT_PRIMARY_READ_LEDGER.json','DRAFT_ROOT_SCIENCE_CARD.json','DRAFT_ROOT_EVIDENCE_BINDINGS.json','DRAFT_ROOT_CURRENT_INPUT_PREIMAGES.json']:
 o=load(body(S/n));need(o['approved_by_root'] is False and o['created_utc'] is None and o['current_verdict'] is None,'Actual null draft');reject(lambda o=o:science(o),'Unapproved actual draft '+n)
need(not (A/'reviewed_candidate').exists(),'No freeze');check(True,'No current packet exists')
o={'schema':'pr48-independent-source-gate-control-results/v1','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),'assertions':len(labels),'labels':labels,'complete_existing_private_captures':private,'complete_source_closure_external_captures':external,'whole_fixed_rows':list(bindings.values()),'whole_read_bytes':sum(r['bytes'] for r in bindings.values()),'synthetic_ROOT_records_are_private_predicate_fixtures_only':True,'native_bodies_read_or_written':False,'production_or_helpers_imported_compiled_executed':False,'future_acceptance_approved':False,'shared_original_attempts':'2/5','new_attempts':0,'audit_turns':0,'SOURCE_review_completion_percent':95,'target_discovery_completion_percent':0}
with (F/'GATE_CONTROL_RESULTS.json').open('x') as h:json.dump(o,h,indent=2,allow_nan=False);h.write('\n');h.flush();os.fsync(h.fileno())
print(json.dumps({'status':'PASS_PRIVATE_GATES_AND_EXISTING_ACTUAL_CAPTURE_READBACK','assertions':len(labels),'complete_body_count':len(bindings),'whole_read_bytes':o['whole_read_bytes'],'native_read_write':False,'future_acceptance':False}))
