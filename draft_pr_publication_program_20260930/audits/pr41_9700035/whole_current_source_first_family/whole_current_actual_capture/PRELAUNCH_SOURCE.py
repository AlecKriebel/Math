#!/usr/bin/env python3
"""Fresh independently authored read-only whole-current/data inspection.
Never imports or executes a candidate or family helper. Writes only own folder.
"""
from pathlib import Path,PurePosixPath
import ast,collections,datetime,hashlib,json,math,os,sqlite3,stat
R=Path(__file__).resolve().parent
A=R.parent
REPO=R.parents[3]
C=A/'reviewed_candidate'
EXPECTED='3431ca2dfb332500f3815ea1e61f089744b3bacd9c3659018537016b9396fbfa'

def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def H(b):return hashlib.sha256(b).hexdigest()
def check(x,message):
 if not x:raise ValueError(message)
def pairs(xs):
 d={}
 for k,v in xs:
  check(k not in d,'Duplicate JSON object key '+k);d[k]=v
 return d
def flt(s):
 v=float(s);check(math.isfinite(v),'Nonfinite JSON float');return v
def reject(s):raise ValueError('Non-JSON constant '+s)
def J(b):return json.loads(b,object_pairs_hook=pairs,parse_float=flt,parse_constant=reject)
def relative(s):
 check(type(s) is str and s and '\\' not in s,'Invalid relative path')
 q=PurePosixPath(s)
 check(not q.is_absolute() and q.as_posix()==s and not {'.','..','.git','__pycache__'}&set(q.parts),'Unsafe path '+s)
 return s
def file(p,size,sha):
 check(p.is_file() and not p.is_symlink(),'Nonregular input '+str(p))
 b=p.read_bytes();check(type(size) is int and len(b)==size and H(b)==sha,'Size/SHA mismatch '+str(p));return b
def contents(root):
 files=set();dirs=set()
 for p in root.rglob('*'):
  check(not p.is_symlink(),'Symlink '+str(p));check(p.is_file() or p.is_dir(),'Special file '+str(p))
  n=relative(p.relative_to(root).as_posix())
  (files if p.is_file() else dirs).add(n)
 required={t.as_posix() for n in files for t in PurePosixPath(n).parents if t.as_posix()!='.'}
 check(dirs==required,'Extra empty directory '+str(root));return files

def typed_walk(v,path=''):
 yield {'pointer':path,'type':type(v).__name__,'value':v if not isinstance(v,(dict,list)) else None}
 if isinstance(v,dict):
  for k,x in v.items():yield from typed_walk(x,path+'/'+k.replace('~','~0').replace('/','~1'))
 elif isinstance(v,list):
  for i,x in enumerate(v):yield from typed_walk(x,path+'/'+str(i))

def main():
 started=now();manifest_raw=(C/'MANIFEST.json').read_bytes();check(H(manifest_raw)==EXPECTED,'Frozen CURRENT manifest changed')
 manifest=J(manifest_raw);check(manifest['self_excluded']==['MANIFEST.json'],'Only root self exclusion allowed')
 check(type(manifest['files_count']) is int and manifest['files_count']==len(manifest['files'])==547,'CURRENT exact547')
 names=[];inventory_rows=[];json_objects={};text_hashes={};ast_hashes={};walk_count=0
 walk=R/'WHOLE_CURRENT_TYPED_VALUE_WALK.jsonl'
 with walk.open('w') as w:
  for row in manifest['files']:
   check(set(row)=={'path','bytes','sha256','mode'},'Typed CURRENT row');n=relative(row['path']);check(n not in names,'Repeated CURRENT path');names.append(n)
   b=file(C/n,row['bytes'],row['sha256']);check(row['mode']=='0444' and stat.S_IMODE((C/n).stat().st_mode)==0o444,'CURRENT mode '+n)
   inventory_rows.append({'path':n,'bytes':len(b),'sha256':H(b),'mode':'0444'})
   if n.endswith('.json'):
    obj=J(b);json_objects[n]=obj
    for leaf in typed_walk(obj):w.write(json.dumps({'file':n,**leaf},ensure_ascii=False,allow_nan=False)+'\n');walk_count+=1
   if n.endswith('.py'):
    ast.parse(b);ast_hashes[n]=H(b)
   if n.endswith(('.md','.py','.patch')):b.decode('utf8');text_hashes[n]=H(b)
 check(contents(C)==set(names)|{'MANIFEST.json'},'CURRENT full recursive membership differs')
 check(stat.S_IMODE((C/'MANIFEST.json').stat().st_mode)==0o444,'Self-manifest mode')
 # Whole typed original saved and actual outputs, with every stored check value.
 original=J((C/'original_snapshot_manifest.json').read_bytes())
 check(len(original['files'])==16 and len(original['changed_paths'])==17,'Original16/17')
 for row in original['files']:
  b=file(C/'original_archive'/relative(row['path']),row['size'],row['sha256'])
  check(b==(A/'source_snapshot'/row['path']).read_bytes(),'Archive source differs')
 immutable=['PROOF.md','verify.py','verification.json','source_record.json','prior_report.json','source_provenance.json','turns.json','review/independent_checks.py','review/independent_results.json','review/review_summary.json']
 for n in immutable:check((C/n).read_bytes()==(C/'original_archive'/n).read_bytes(),'Current math anchor differs '+n)
 check(H((C/'PROOF.md').read_bytes())=='464af6d259f9275ca9f0056567f5301bc228465fa0ddaf2faece0920cab6bd7c','Exact proof')
 checks={}
 for n,count,actual in [('verification.json',211,'author_private/verification.json'),('review/independent_results.json',3809,'original_independent_private/review/independent_results.json')]:
  o=json_objects[n];check(type(o['passed']) is int and o['passed']==count and type(o['failed']) is int and o['failed']==0,'Saved counts')
  check(type(o['checks']) is dict and len(o['checks'])==count and all(type(k) is str and type(v) is str and v=='PASS' for k,v in o['checks'].items()),'All saved checks')
  p='root_verification/root_original_actual_reproduction/'+actual
  check((C/p).read_bytes()==(C/n).read_bytes() and json_objects[p]==o,'Whole actual output differs')
  checks[n]={'declared':count,'every_name_and_value_read':True,'actual_full_bytes_equal':True,'whole_typed_object_equal':True}
 # Exact29 itemized foreign dependencies; all remaining dependencies bound too.
 deps=json_objects['CURRENT_PROOF_DEPENDENCIES.json'];check(deps['dependency_anchor_repository_relative']==A.relative_to(REPO).as_posix(),'Repository dependency anchor')
 seen=set();foreign=[];multiple=[]
 for row in deps['files']:
  n=relative(row['path']);check(n not in seen,'Duplicate dependency');seen.add(n);file(A/n,row['bytes'],row['sha256'])
  role=row['role'];check(type(role) in (str,list),'Role type')
  roles=[role] if type(role) is str else role
  check(all(type(x) is str and x for x in roles) and len(set(roles))==len(roles),'Role values')
  if type(role) is list:check(roles==sorted(roles),'Roles sorted');multiple.append({'path':n,'roles':roles})
  if 'foreign_primary_hash_only' in roles:
   foreign.append(row);check('family_evidence/'+n not in names,'Foreign body was copied')
 check(len(foreign)==29,'Exactly21+8 foreign')
 foreign_counts=collections.Counter(x['path'].split('/')[0] for x in foreign)
 check(dict(foreign_counts)=={'primary_scope_family':21,'network_tail_measure_family':8},'Foreign class counts')
 # Exact family-owned and root-owned recursive source closure/pins.
 pins=json_objects['build/INPUT_PINS.json']
 for name,info in pins['families'].items():
  authored={row['path'] for row in info['members']};foreign_set={row['path'] for row in info['foreign_members']}
  check(not authored&foreign_set and len(authored)==info['first_party_count'] and len(foreign_set)==info['foreign_count'],'Family disjoint classes')
  check(contents(A/name)==authored|foreign_set|{info['manifest']['path']},'Original family closure')
  check(contents(C/'family_evidence'/name)==authored|{info['manifest']['path']},'Copied family closure excludes only explicit foreign inputs')
 for label,info in pins['root_support'].items():
  p=C/'root_verification'/info['directory'];m=J((p/'MANIFEST.json').read_bytes())
  check(H((p/'MANIFEST.json').read_bytes())==info['manifest_sha256'],'Root support manifest pin')
  check(m['files']==info['members'] and len(m['files'])==info['member_count'],'Whole root support rows')
  check(contents(p)=={x['path'] for x in m['files']}|{'MANIFEST.json'},'Exact root support closure')
  for row in m['files']:file(p/relative(row['path']),row['bytes'],row['sha256'])
 # Every root actual outer capture has genuine positive PID, complete distinct channels,
 # aware chronological UTC clocks, exit0 and the exact retained source.
 capture_checks=[]
 for label,info in pins['root_support'].items():
  prefix='root_verification/'+info['directory'];obj=json_objects[prefix+'/'+info['receipt']]
  check(obj['status']=='PASS' and len(obj['actual_outer_runs'])==3,'Root support completed triple')
  for run in obj['actual_outer_runs']:
   check(run['actual_execution'] is True and run['completed'] is True and type(run['pid']) is int and run['pid']>0 and type(run['exit_code']) is int and run['exit_code']==0 and run['stdin_supplied'] is False,'Actual root run fields')
   t=[datetime.datetime.fromisoformat(run[k]) for k in ('started_utc','finished_utc')]
   check(all(v.tzinfo and v.utcoffset()==datetime.timedelta(0) for v in t) and t[0]<=t[1],'Real ordered UTC clocks')
   check(run['stdout']['path']!=run['stderr']['path'],'Distinct root channels')
   for channel in ('stdout','stderr'):
    row=run[channel];file(C/prefix/relative(row['path']),row['bytes'],row['sha256'])
   check(type(run['argv']) is list and all(type(x) is str and x for x in run['argv']) and type(run['cwd']) is str,'Actual argv/cwd')
   capture_checks.append({'kind':label,'pid':run['pid'],'exit_code':run['exit_code'],'source_sha256':run['source_sha256'],'started_utc':run['started_utc'],'finished_utc':run['finished_utc']})
 # Complete family results differ in layout; read every entry at its true type.
 primary=json_objects['family_evidence/primary_scope_family/finite_controls_actual_capture_v2/RESULT.json']
 check(type(primary['passed']) is int and primary['passed']==1326 and type(primary['failed']) is int and primary['failed']==0 and len(primary['checks'])==1326 and all(type(x) is str for x in primary['checks']) and len(set(primary['checks']))==1326,'All1326 primary names')
 network=json_objects['family_evidence/network_tail_measure_family/NETWORK_MEASURE_CONTROL_RESULTS.json']
 check(type(network['checks_passed']) is int and network['checks_passed']==122 and len(network['checks'])==122 and all(type(x) is dict and type(x['result']) is str and x['result']=='PASS' for x in network['checks']),'All122 network objects')
 # Current four metadata objects, genuine card/ledger, false/null drafts.
 for n in ['attempt.json','status.json','readiness.json','review/verdict.json']:
  o=json_objects[n];check(o['full_problem_solved'] is False and o['novelty_claimed'] is False,'No solved promotion')
  for k,v in [('original_substantive_attempts',2),('substantive_attempt_limit',5),('new_substantive_attempts',0),('audit_turns',0)]:check(type(o[k]) is int and o[k]==v,'Current typed accounting')
  check(all(k in o and o[k] is None for k in ['current_model','current_reasoning_effort','current_deadline_utc','current_verdict']),'Present null runtime/verdict')
 card=json_objects['root_verification/ROOT_SCIENCE_CARD.json'];ledger=json_objects['primary_evidence/ROOT_PRIMARY_READ_LEDGER.json']
 check(card['status']=='UNSOLVED' and card['partial_valid'] is True and card['full_problem_solved'] is False and card['new_whole_current_gate']=='PENDING','Root scoped pending card')
 check(set(card['root_flags'])==set(ledger['root_flags']) and len(card['root_flags'])==8 and all(x is True for x in card['root_flags'].values()) and all(x is True for x in ledger['root_flags'].values()) and ledger['reading_completed'] is True,'Genuine exact8true ledger/card')
 for n in ['build/DRAFT_ROOT_READ_LEDGER.json','build/DRAFT_ROOT_SCIENCE_CARD.json']:
  o=json_objects[n];check(all(x is False for x in o['root_flags'].values()),'Draft flags remain false')
  check(o.get('reading_completed',False) is False and o.get('partial_valid',False) is False,'Draft approvals remain false')
 # Prospective queue: only3 named columns, all other lines/bytes preserved.
 q=(C/'queue_proposal/QUEUE_PREIMAGE.md').read_bytes();p=(C/'queue_proposal/QUEUE_PROSPECTIVE.md').read_bytes();before=q.splitlines(keepends=True);after=p.splitlines(keepends=True)
 check(len(before)==len(after),'Queue line count');differences=[i for i,(a,b) in enumerate(zip(before,after)) if a!=b];check(len(differences)==1,'Queue only1row')
 i=differences[0];left=before[i].decode().split('|');right=after[i].decode().split('|');check(len(left)==len(right)==14,'Queue exact12 columns')
 changed=[j for j,(a,b) in enumerate(zip(left,right)) if a!=b];check(changed==[8,9,11] and left[2].strip()=='9700035 / AMR-096-0035' and right[8].strip()=='unsolved' and right[9].strip()=='2/5','Only status/turns/findings')
 patch=json_objects['CURRENT_QUEUE_PATCH.json'];check(H(q)==patch['whole_preimage_sha256'] and H(p)==patch['whole_prospective_sha256'],'Queue pins')
 # Independent full raw/SQL read, including duplicate-code importer convention.
 rawpath=REPO/'unsolved_math_prioritization/cache';rawb=(rawpath/'problems.json').read_bytes();reportb=(rawpath/'research_results.json').read_bytes();raw=J(rawb);reports=J(reportb)
 byid={str(x['id']):x for x in raw};codes=collections.Counter(x['problem_number'] for x in raw)
 check(len(raw)==len(byid)==15458 and len(reports)==6701,'Full raw counts')
 db=sqlite3.connect('file:'+str((rawpath/'catalog.sqlite').resolve())+'?mode=ro&immutable=1',uri=True);db.execute('PRAGMA query_only=ON');check(db.execute('PRAGMA query_only').fetchone()==(1,),'SQLite query-only')
 rows=db.execute('SELECT key,payload,report FROM records ORDER BY key').fetchall();check(len(rows)==15458,'Full SQLite count')
 for key,payload,report in rows:
  expected=dict(byid[key]);code=expected['problem_number']
  if codes[code]>1 and code in reports:expected['_ambiguous_report']=True
  prior={} if expected.get('_ambiguous_report') else reports.get(code,{})
  check(J(payload)==expected and J(report)==prior,'Raw/SQL whole joined object '+key)
 db.close()
 check(byid['9700035']==json_objects['source_record.json'] and reports['AMR-096-0035']==json_objects['prior_report.json'] and reports['AMR-096-0035'],'Original PRESENT prior whole equality')
 result={'status':'PASS_INDEPENDENT_WHOLE_CURRENT_BYTE_TYPED_DATA_CONTROLS','started_utc':started,'completed_utc':now(),'pid':os.getpid(),'current_manifest_sha256':EXPECTED,'authored_members':547,'self_only_recursive_membership':True,'all_modes_0444':True,'all_current_bytes':sum(x['bytes'] for x in inventory_rows),'whole_JSON_objects_parsed':len(json_objects),'whole_JSON_typed_walk_entries':walk_count,'typed_walk':{'path':walk.name,'bytes':walk.stat().st_size,'sha256':H(walk.read_bytes())},'AST_only_sources':len(ast_hashes),'text_source_patch_whole_bytes_read':len(text_hashes),'all_dependency_rows_verified':len(seen),'foreign_members':foreign,'multiple_role_dependencies':multiple,'original16_full17_paths':True,'original_check_objects':checks,'family_full_check_counts':[1326,122],'actual_root_capture_details':capture_checks,'raw_corpus_bytes':len(rawb)+len(reportb),'all_SQL_rows_independently_compared':len(rows),'source_PRESENT_prior_whole_equal':True,'queue_named_columns_only':True,'no_candidate_imports_or_execution':True,'no_native_Git_remote_mutation':True,'scientific_disposition':'No unconditional theorem inferred from these finite/data controls; analytic review is separate.'}
 (R/'WHOLE_CURRENT_INSPECTION_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 (R/'WHOLE_CURRENT_INPUT_READ_LEDGER.json').write_text(json.dumps({'manifest_sha256':EXPECTED,'all_files':inventory_rows,'all_python_AST_hashes':ast_hashes,'all_text_hashes':text_hashes},indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k not in ['foreign_members','multiple_role_dependencies','actual_root_capture_details']},indent=2))
if __name__=='__main__':main()
