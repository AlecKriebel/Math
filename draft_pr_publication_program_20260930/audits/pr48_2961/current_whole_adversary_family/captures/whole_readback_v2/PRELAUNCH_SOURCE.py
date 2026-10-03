"""Independent full-body/type/custody audit; no production import or execution."""
from pathlib import Path,PurePosixPath
import collections,datetime as dt,hashlib,json,math,os,sqlite3,stat,subprocess,sys
F=Path(__file__).absolute().parent;A=F.parent;C=A/'reviewed_candidate';R=A.parents[2]
sha=lambda b:hashlib.sha256(b).hexdigest();bindings=[]
def require(x):assert x

def parse(b):
 def pairs(a):
  o={}
  for k,v in a:require(k not in o);o[k]=v
  return o
 def fl(v):z=float(v);require(math.isfinite(z));return z
 return json.loads(b,object_pairs_hook=pairs,parse_float=fl,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def equal(a,b):
 if type(a)is not type(b):return False
 if type(a)is dict:return a.keys()==b.keys() and all(equal(a[k],b[k])for k in a)
 if type(a)is list:return len(a)==len(b) and all(equal(x,y)for x,y in zip(a,b))
 return a==b

def rel(n):
 require(type(n)is str and n and '\\'not in n and '\0'not in n);p=PurePosixPath(n)
 require(not p.is_absolute() and p.as_posix()==n and not set(p.parts)&{'.','..','.git','__pycache__'});return n

def read(p):
 require(not p.is_symlink() and all(not a.is_symlink()for a in p.parents) and stat.S_ISREG(p.stat().st_mode));b=p.read_bytes()
 bindings.append(dict(path=str(p),bytes=len(b),sha256=sha(b),full_mode=stat.S_IMODE(p.stat().st_mode)));return b

def structured(p,b):
 if p.suffix=='.json':return parse(b)
 if p.suffix=='.jsonl':
  try:return parse(b)
  except (json.JSONDecodeError,UnicodeDecodeError):
   require(b.strip());require(all(x.strip()for x in b.splitlines()));return [parse(x)for x in b.splitlines()]

def checked(root,r,mode=None):
 require(type(r)is dict and type(r['bytes'])is int and r['bytes']>=0 and type(r['sha256'])is str and len(r['sha256'])==64)
 p=root/rel(r['path']);b=read(p);require(len(b)==r['bytes'] and sha(b)==r['sha256'])
 m=r.get('full_mode',mode)
 if m is not None:
  require(type(m)is int or type(m)is str and m=='0444');want=int(m,8)if type(m)is str else m;require(stat.S_IMODE(p.stat().st_mode)==want)
 structured(p,b);return b

def topo(root):
 require(root.is_dir() and not root.is_symlink());names=set();dirs=set()
 for p in root.rglob('*'):
  require(not p.is_symlink());n=rel(p.relative_to(root).as_posix())
  if p.is_file():names.add(n)
  else:require(stat.S_ISDIR(p.stat().st_mode));dirs.add(n)
 expected={q.as_posix()for n in names for q in PurePosixPath(n).parents if str(q)!='.'};require(dirs==expected);return names,dirs

def clock(v):
 require(type(v)is str);z=dt.datetime.fromisoformat(v.replace('Z','+00:00'));require(z.tzinfo is not None and z.utcoffset()==dt.timedelta(0));return z
now=dt.datetime.now(dt.timezone.utc)
def capture(c,base,opid=None):
 require(c['actual_execution']is True and c['completed']is True and type(c['pid'])is int and c['pid']>0 and type(c['exit_code'])is int and c['stdin_supplied']is False)
 require(clock(c['started_utc'])<=clock(c['finished_utc'])<=now)
 if opid is not None:require(c.get('operator_pid',c.get('actual_operator_pid'))==opid)
 for key in ['stdout','stderr']:checked(base,c[key])
 return c
# Complete current packet, manifest self only, exact modes/topology.
mb=read(C/'MANIFEST.json');require(sha(mb)=='3f8d6b38fcd0268df5a32fc006c5a759b2dd61f225f2fa2fa959861a9bcb115f');m=parse(mb)
require(m['schema']=='pr48-strict-current-packet/v1' and m['self_excluded']==['MANIFEST.json'] and type(m['files_count'])is int and m['files_count']==len(m['files'])==1946)
names,dirs=topo(C);require(names=={r['path']for r in m['files']}|{'MANIFEST.json'} and len(dirs)==365);require(len({r['path']for r in m['files']})==1946)
for r in m['files']:checked(C,r,0o444)
require(stat.S_IMODE((C/'MANIFEST.json').stat().st_mode)==0o444)
D=parse(read(C/'CURRENT_DEPENDENCIES.json'));require(len(D['files'])==1798 and len({r['path']for r in D['files']})==1798)
native4={'unsolved_math_prioritization/'+n for n in ['QUEUE.md','state.json','history.jsonl']}|{'draft_pr_publication_program_20260930/inventory.json'}
stable=[r for r in D['current_native13']if r['path']not in native4];require(len(stable)==9);dated=[]
for r in D['files']:
 if r['path']in native4:
  b=read(R/r['path']);dated.append(dict(path=r['path'],live_still_matches=len(b)==r['bytes']and sha(b)==r['sha256']and stat.S_IMODE((R/r['path']).stat().st_mode)==r['full_mode']))
 else:checked(R,r)
for r in stable:checked(R,r)
# Each distinct family manifest and declared ownership; no sibling annexation.
pins=parse(read(C/'build/source_preparation/STATIC_INPUT_BINDINGS.json'));corpora=[]
for key,info in pins['closed_inputs'].items():
 b=checked(R,info['manifest']);m0=parse(b);require(m0['schema']==info['schema']);require(m0['self_excluded']is True if key=='smooth'else m0['self_excluded']==[info['self_name']])
 root=R/info['root'];expected={r['path']for r in m0['files']};require(type(m0['files_count'])is int and m0['files_count']==len(expected)==len(m0['files']))
 if key=='original':
  actual=set(info['authorship_root_files'])
  for sub in info['authorship_directory_roots']:actual|={sub+'/'+n for n in topo(root/sub)[0]}
 else:actual=topo(root)[0]-{info['self_name']}
 require(actual==expected)
 for r in m0['files']:checked(root,r,0o444)
 actualdirs={'.'}|{p.as_posix()for n in expected for p in PurePosixPath(n).parents if str(p)!='.'}
 require(actualdirs=={r['path']for r in info['directories']})
 for d in info['directories']:require(type(d['full_mode'])is int and stat.S_IMODE((root/d['path']).stat().st_mode)==d['full_mode'])
 for r in info['members']:checked(R,r)
 corpora.append(dict(name=key,payload=len(expected),directories_including_root=len(actualdirs),schema=m0['schema'],manifest_sha256=sha(b),self_excluded=m0['self_excluded']))
for folder,selfname,count in [('current_preparation_family','PREPARATION_MANIFEST.json',55),('current_source_adversary_family','MANIFEST.json',86)]:
 root=A/folder;b=read(root/selfname);mm=parse(b);require(mm['self_excluded']==[selfname] and type(mm['files_count'])is int and mm['files_count']==len(mm['files'])==count)
 ns,ds=topo(root);require(ns=={r['path']for r in mm['files']}|{selfname});require(len(ds)==(12 if count==86 else 10))
 for r in mm['files']:checked(root,r,0o444)
 require(stat.S_IMODE((root/selfname).stat().st_mode)==0o444)
 corpora.append(dict(name=folder,payload=count,relative_directories=len(ds),manifest_sha256=sha(b)))
# Actual original17 and immutable11, native proposal copies.
snap=parse(read(C/'original_snapshot_manifest.json'));require(len(snap['files'])==17)
for r in snap['files']:
 n=r['relative_path'];b=read(A/'source_snapshot'/n);require(sha(b)==r['sha256']and len(b)==r['bytes']);require(read(C/'original_archive'/n)==b)
 require(r['git_mode']=='100644' and r['snapshot_full_mode']==0o444)
require(topo(C/'original_archive')[0]=={r['relative_path']for r in snap['files']})
imm=['PARTIAL.md','check_algebra.py','check_results.json','related_source_record.json','source_record.json','turns.jsonl','source_checksums.json','review/author_replay/check_algebra.py','review/author_replay/check_results.json','review/independent_checks.py','review/independent_results.json']
for n in imm:require(read(C/n)==read(A/'source_snapshot'/n))
turns=[parse(x)for x in read(C/'turns.jsonl').splitlines()];require(len(turns)==2 and all(type(x['turn'])is int for x in turns) and [x['turn']for x in turns]==[1,2])
for n,id,code in [('source_record.json',2961,'KP-4.85'),('related_source_record.json',30004403,'OWR-17471-009')]:
 z=parse(read(C/n));require(type(z['id'])is int and z['id']==id and z['problem_number']==code and 'problem'not in z)
for n in native4:
 label=n.replace('/','__');before=read(C/'native4_proposal/preimage'/label);after=read(C/'native4_proposal/prospective'/label)
 if not n.endswith('QUEUE.md'):require(before==after)
 else:
  old=before.splitlines(keepends=True);new=after.splitlines(keepends=True);require(len(old)==len(new));changes=[]
  for i,(a,b)in enumerate(zip(old,new)):
   if a==b:continue
   fields=a.decode().split('|');afterfields=b.decode().split('|');require(len(fields)==len(afterfields)==14 and fields[2].strip()=='2961 / KP-4.85')
   require(all(x==y for j,(x,y)in enumerate(zip(fields,afterfields))if j not in {8,9,11}));require(fields[8].strip()=='queued'and fields[9].strip()=='0/5'and afterfields[8].strip()=='unsolved'and afterfields[9].strip()=='2/5');changes.append(i)
  require(len(changes)==1 and b'30004403 / OWR-17471-009'not in before and b'30004403 / OWR-17471-009'not in after)
for n in ['status.json','readiness.json','review/verdict.json','review/review_summary.json']:
 s=parse(read(C/n));require(s['status']=='unsolved'and s['full_problem_solved']is False and s['project_solved']is False and s['duplicate_shared_budget']is True and s['current_verdict']is None and s['current_model']is None and s['current_reasoning_effort']is None and s['current_deadline_utc']is None)
 for k,v in [('original_substantive_attempts',2),('turn_limit',5),('new_substantive_attempts',0),('audit_turns',0)]:require(type(s[k])is int and s[k]==v)
 require(all(s[k]is False for k in ['paper_created','new_DOI_created','tracker_row_created','novelty_claimed','historical_PASS_transferred','human_peer_review_claimed']))
# Actual AFTER-exit entire final52/104; honest frozen50 prefix.
e=parse(read(C/'CURRENT_EXECUTION_REFERENCE.json'));outer=A/e['audit_relative_outer_capture'];inner=A/e['audit_relative_inner_attempt'];oc=capture(parse(read(outer/'CAPTURE.json')),outer,92331);require(oc['pid']==92332 and oc['exit_code']==0)
require(oc['builder_unchanged_after_child']is True and oc['operator_unchanged_after_child']is True)
for name,source,key in [('PRELAUNCH_BUILDER_SOURCE.py','prepare_current_packet.py','builder_sha256'),('PRELAUNCH_OPERATOR.py','capture_root_builder_operation.py','operator_sha256')]:require(sha(read(outer/name))==oc[key]and read(outer/name)==read(A/'current_preparation_family'/source))
pre=parse(read(outer/'OPERATION_PRELAUNCH.json'));require(pre['argv']==oc['argv']and pre['operator_pid']==oc['operator_pid']and pre['started_utc']==oc['started_utc'])
require(sha(read(outer/'OPERATION_PRELAUNCH.json'))==e['outer_prelaunch_sha256'])
commands=parse(read(inner/'GIT_COMMANDS.json'));prefix=parse(read(C/'build/actual_attempt_prepublication_prefix/GIT_COMMANDS.json'));require(len(commands)==52 and len(prefix)==50 and equal(commands[:50],prefix))
allstreams=[]
for i,c in enumerate(commands):
 capture(c,inner);require(c['exit_code']==0 and c['cwd']==str(R) and c['argv'][0]=='git'and c['argv'][1]in {'branch','rev-parse','show','ls-tree','diff','merge-base'}and c['stderr']['bytes']==0)
 require(clock(oc['started_utc'])<=clock(c['started_utc'])<=clock(c['finished_utc'])<=clock(oc['finished_utc']))
 require(c['stdout']['path']==f'git/{i}.stdout'and c['stderr']['path']==f'git/{i}.stderr');allstreams.extend([dict(command=i,channel=n,**c[n])for n in ['stdout','stderr']])
require(len(allstreams)==104 and parse(read(outer/'stdout.bin'))['manifest_sha256']==sha(mb))
require(read(inner/'PRELAUNCH_BUILDER_SOURCE.py')==read(A/'current_preparation_family/prepare_current_packet.py'))
# ROOT historical42 exact captures/schema, full saved results and printed subsets.
rr=parse(read(A/'root_original_actual_reproduction_v2/ROOT_REPRODUCTION_RESULT.json'));rootgit=rr['complete_actual_Git_captures'];helpers=rr['complete_actual_helper_captures'];require(len(rootgit)==38 and len(helpers)==4)
for c in rootgit+helpers:
 capture(c,R,11716);require(c['exit_code']==0 and c['operator_unchanged']is True and c['stderr']['bytes']==0)
 if c in rootgit:require(c['schema']=='pr48-root-readonly-git-actual-capture/v1'and c['source']is None and c['source_unchanged']is None)
 else:
  require(c['schema']=='pr48-root-unchanged-helper-actual-capture/v1'and type(c['source'])is dict and c['source_unchanged']is True and c['argv']==['/usr/bin/python3','-B',str(R/c['source']['path'])]);checked(R,c['source'])
 for stream in ['stdout','stderr']:
  capturepath=(R/c[stream]['path']).parent/'CAPTURE.json';require(equal(parse(read(capturepath)),c))
require(rr['identical_submitted_counted_independent']is False and equal(rr['entire_historical_and_final_replayed_results']['author_final'],dict(rr['entire_original_author_result'],partial_sha256=sha(read(C/'PARTIAL.md')))))
# Read foreign raw/prior/SQLite ONLY IN PLACE; exact complete serialized importer.
cache=R/'unsolved_math_prioritization/cache';rb=read(cache/'problems.json');pb=read(cache/'research_results.json');raw=parse(rb);prior=parse(pb);require(len(rb)+len(pb)==149266659 and len(raw)==15458 and len(prior)==6701)
byid={str(z['id']):z for z in raw};counts=collections.Counter(z['problem_number']for z in raw);require(len(byid)==15458)
read(cache/'catalog.sqlite');sql=sqlite3.connect('file:'+str(cache/'catalog.sqlite')+'?mode=ro&immutable=1',uri=True);sql.execute('PRAGMA query_only=ON');require(sql.execute('PRAGMA query_only').fetchone()==(1,));rows=[]
for key,payload,report in sql.execute('SELECT key,payload,report FROM records ORDER BY key'):
 expected=dict(byid[key]);code=expected['problem_number'];ambiguous=counts[code]>1 and code in prior
 if ambiguous:expected['_ambiguous_report']=True
 expectedreport={}if ambiguous else prior.get(code,{})
 require(equal(parse(payload),expected)and equal(parse(report),expectedreport));require(payload==json.dumps(expected)and report==json.dumps(expectedreport))
 rows.append(dict(key=key,payload_sha256=sha(payload.encode()),report_sha256=sha(report.encode()),complete_payload_recursive_type_equal=True,complete_report_recursive_type_equal=True,prior_key_present=code in prior,ambiguous_code=ambiguous))
 if key in {'2961','30004403'}:require(code not in prior and report=='{}')
sql.close();require(len(rows)==15458);rootraw=parse(read(A/'ROOT_COMPLETE_RAW_SQL_AUDIT.json'));require(equal(rows,rootraw['complete_row_bindings']))
require(not (C/'prior_report.json').exists()and not (C/'original_archive/prior_report.json').exists())
for n,key in [('source_record.json','2961'),('related_source_record.json','30004403')]:require(equal(parse(read(C/n)),byid[key]))
# Read whole later ROOT inspection/authority, without adopting PASS as new proof.
inspectionraw=read(A/'ROOT_ACTUAL_CURRENT_FREEZE_INSPECTION.json');require(len(inspectionraw)==1305401 and sha(inspectionraw)=='0c18cc86361f02342e2093bfc2d773c72a080da5e9ae316500212c249dae9cc0');ins=parse(inspectionraw)
require(equal(ins['entire_actual_outer_capture'],oc)and equal(ins['entire_final_original_inner_commands'],commands)and ins['whole_review_or_acceptance_approved']is False)
newrecord=read(A/'ROOT_NEW_SOURCE_ADVERSARY_RECORD.json');require(len(newrecord)==529872 and sha(newrecord)=='b66952c3424edf785f8233189447b013d9a01fecdb0bc7f386788a4066b33aa3');adv=parse(newrecord)
require(equal(parse(read(A/'current_source_adversary_family/VERDICT.json')),adv['complete_VERDICT_object']))
result=dict(schema='pr48-independent-whole-current-full-readback/v1',actual_pid=os.getpid(),utc=dt.datetime.now(dt.timezone.utc).isoformat(),status='PASS_CURRENT_FROZEN_BODY_SCOPE_TYPES_CUSTODY_AND_RAW_SQL',candidate_manifest_sha256=sha(mb),current1946_payload=True,relative_directories=365,dependencies=1798,current_native4_dated_readback=dated,stable9_live=True,corpora=corpora,entire_actual_outer_capture=oc,entire_final_original_inner_commands=commands,complete104_stream_bindings=allstreams,frozen50_prefix_of52=True,ROOT42_exact_capture_schemas_checked=True,raw_prior_bytes=149266659,SQL_rows=15458,all_SQL_serialization_recursive_types_and_ROOT_derived_bindings_equal=True,both_keys_absent_SQL_literal_empty_no_priorfile=True,body_bindings=bindings,foreign_bodies_copied=False,production_import_compile_execution=False,future_acceptance_approved=False)
(F/'WHOLE_READBACK_RESULT.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');print(json.dumps({k:v for k,v in result.items()if k not in {'body_bindings','entire_actual_outer_capture','entire_final_original_inner_commands','complete104_stream_bindings'}},indent=2))
