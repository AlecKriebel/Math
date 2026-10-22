"""Finite explicit offline selector. Reads frozen leaf manifests; writes only this folder.

No recursive walking, network, subprocess, Git, lock or actual-five capture.
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,stat
HERE=Path(__file__).absolute().parent
CASE=HERE.parent;PROGRAM=CASE.parents[1];CHECKOUT=PROGRAM.parent
PREFIX='draft_pr_publication_program_20260930/';A=PREFIX+'audits/pr214_30005244/'
MAX_BODY=4_000_000
def need(x,msg):
 if type(x) is not bool or not x:raise ValueError(msg)
def p(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def rel(x):
 need(type(x) is str and 0<len(x.encode())<=4096 and not Path(x).is_absolute() and '\\' not in x and all(32<=ord(c)!=127 for c in x) and all(v not in ('','.','..') for v in x.split('/')),'Safe relative path')
 return x
def read_file(path):
 path=Path(path)
 need(path.is_absolute() and path.is_relative_to(CHECKOUT) and path.resolve()==path,'Canonical checkout-owned source')
 opened=[];fd=None
 try:
  q=Path('/');parent=os.open(q,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW);opened.append((q,parent,os.fstat(parent)))
  for part in path.parent.parts[1:]:
   q=q/part;parent=os.open(part,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=parent);opened.append((q,parent,os.fstat(parent)))
  fd=os.open(path.name,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK,dir_fd=parent);before=os.fstat(fd)
  need(stat.S_ISREG(before.st_mode) and stat.S_IMODE(before.st_mode) in (0o444,0o644) and before.st_size<=MAX_BODY,'Bounded declared-mode regular source')
  with os.fdopen(fd,'rb',closefd=False) as f:b=f.read(MAX_BODY+1)
  after=os.fstat(fd);linked=path.lstat()
  fields=lambda s:(s.st_dev,s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
  need(fields(before)==fields(after)==fields(linked) and len(b)==after.st_size,'Source changed during read')
  for q,d,old in opened:
   v,w=os.fstat(d),q.lstat()
   need(stat.S_ISDIR(w.st_mode) and (v.st_dev,v.st_ino)==(w.st_dev,w.st_ino)==(old.st_dev,old.st_ino),'Source ancestor changed')
  b.decode('utf-8');need(b'\0' not in b,'No binary/NUL selected source')
  return b,f'{stat.S_IMODE(after.st_mode):04o}'
 finally:
  if fd is not None:os.close(fd)
  for q,d,s in reversed(opened):os.close(d)
def native(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def public(path):
 rel(path)
 if not path.startswith(A):return False
 forbidden=('private','_private','packet','journal','runtime','_runtime','sandbox','_synthetic','root_admin214_','root_complete214_')
 return not any(x.lower().startswith(forbidden) or x.lower() in ('extracted','objects','inputs') for x in path[len(A):].split('/')) and Path(path).suffix.lower() in ('.json','.md','.py','.txt','.tex','.csv','.patch','.sha256')
REPRODUCTION_PUBLIC_RELOCATIONS={'RUNTIME_METADATA.json': 'authored_execution_outputs/EXECUTION_ENVIRONMENT_METADATA.json', 'harness_run_02_failed/independent_stderr.bin': 'authored_execution_outputs/harness_run_02_failed/independent_stderr.txt', 'harness_run_02_failed/independent_stdout.bin': 'authored_execution_outputs/harness_run_02_failed/independent_stdout.txt', 'independent_stderr.bin': 'authored_execution_outputs/independent_stderr.txt', 'independent_stdout.bin': 'authored_execution_outputs/independent_stdout.txt', 'replay/program_00/stderr.bin': 'authored_execution_outputs/program_00/stderr.txt', 'replay/program_00/stdout.bin': 'authored_execution_outputs/program_00/stdout.txt', 'replay/program_01/stderr.bin': 'authored_execution_outputs/program_01/stderr.txt', 'replay/program_01/stdout.bin': 'authored_execution_outputs/program_01/stdout.txt', 'replay/program_02/stderr.bin': 'authored_execution_outputs/program_02/stderr.txt', 'replay/program_02/stdout.bin': 'authored_execution_outputs/program_02/stdout.txt', 'replay/program_03/stderr.bin': 'authored_execution_outputs/program_03/stderr.txt', 'replay/program_03/stdout.bin': 'authored_execution_outputs/program_03/stdout.txt', 'replay/program_04/private/exact_controls_output.json': 'authored_execution_outputs/program_04/exact_controls_output.json', 'replay/program_04/stderr.bin': 'authored_execution_outputs/program_04/stderr.txt', 'replay/program_04/stdout.bin': 'authored_execution_outputs/program_04/stdout.txt', 'replay/program_05/stderr.bin': 'authored_execution_outputs/program_05/stderr.txt', 'replay/program_05/stdout.bin': 'authored_execution_outputs/program_05/stdout.txt', 'replay/program_06/stderr.bin': 'authored_execution_outputs/program_06/stderr.txt', 'replay/program_06/stdout.bin': 'authored_execution_outputs/program_06/stdout.txt'}
rows={};origins={};closures=[];omissions=[];relocations=[]
def add(path,origin,role,basis,expected=None,carry=False):
 rel(path);b,mode=read_file(origin)
 if expected is not None:need(p(b)=={k:expected[k] for k in ('bytes','sha256')},'Selected pin drift: '+path)
 if not carry:need(public(path),'Explicit newA214 public scope only: '+path)
 row={'path':path,'origin':str(origin),**p(b),'git_blob':native(b),'observed_source_mode':mode,'role':role,'selection_basis':basis}
 need(path not in rows,'Duplicate target: '+path);rows[path]=row;origins[path]=b
 return row
def leaf(n,role):
 return add(A+n,CASE/rel(n),role,'explicit_current_leaf')
def archive(origin_relative,target_relative,role):
 return add(A+target_relative,CHECKOUT/rel(origin_relative),role,'explicit_archived_copy_retaining_original_provenance')
def closure(folder,manifest,seal,role,historical=False):
 f=CASE/folder;mb,mode=read_file(f/manifest);m=json.loads(mb)
 rr=m.get('files',m.get('safe_authored_files'));need(type(rr) is list,'Finite declared manifest rows')
 included=[];excluded=[]
 for row in rr:
  value=row.get('path',row.get('relative_path'))
  need(type(value) is str,'Manifest path')
  src=Path(value) if Path(value).is_absolute() else f/rel(value)
  need(src.is_relative_to(f),'Manifest member escaped its family')
  target=A+str(src.relative_to(CASE))
  source_relative=str(src.relative_to(f))
  if folder=='reproduction_adversary_01' and source_relative in REPRODUCTION_PUBLIC_RELOCATIONS:
   mapped=A+folder+'/'+REPRODUCTION_PUBLIC_RELOCATIONS[source_relative]
   add(mapped,src,role+'; explicit byte-exact authored execution relocation','Root_requested_explicit_scientific_execution_text_copy',row)
   relocations.append({'original_manifest_path':source_relative,'origin':str(src),'archived_target':mapped,
      'bytes':row['bytes'],'sha256':row['sha256'],'UTF8_noNUL_verified':True,
      'scope':'Authored mathematical execution evidence, not native/provider/tracker or third-party raw payload',
      'failed_harness_history_retained':'harness_run_02_failed' in source_relative})
   included.append(mapped)
  elif public(target):
   add(target,src,role+(' HISTORICAL_UNACCEPTED_SOURCE01' if historical else ''),'positive_frozen_family_manifest',row);included.append(target)
  else:
   omission={'path':target,'origin':str(src),'bytes':row['bytes'],'sha256':row['sha256'],
     'reason':'Not selected: private/unsupported binary/log output. Manifest is retained as historical binding, not a claim of full reproduction of omitted payloads.'}
   exclusions=omissions;exclusions.append(omission);excluded.append(omission)
 leaf(folder+'/'+manifest,role+' declared manifest')
 if seal is not None:leaf(folder+'/'+seal,role+' external seal')
 closures.append({'folder':folder,'manifest':p(mb),'included_declared_rows':len(included),'declared_rows':len(rr),
                  'all_declared_payloads_selected':not excluded,'relocated_members':[r for r in relocations if '/'+folder+'/' in r['archived_target']],
                  'omitted_members':excluded,'historical_unaccepted_source01':historical})
def archived_closure(origin_relative,target_relative,manifest,seal,expected,role):
 f=CHECKOUT/rel(origin_relative);mb,unused=read_file(f/manifest)
 need(p(mb)==expected,'Exact frozen archived producer manifest')
 m=json.loads(mb);rr=m['files'];need(type(rr) is list and len(rr)==12,'Exact12 after214 producer payloads')
 targets=[]
 for r in rr:
  n=rel(r['path']);need('/' not in n,'Basename-only frozen producer closure')
  add(A+target_relative+'/'+n,f/n,role,'explicit_archived_frozen_producer_member',r)
  targets.append(A+target_relative+'/'+n)
 for n in [manifest,seal]:
  add(A+target_relative+'/'+n,f/n,role+' manifest/seal','explicit_archived_frozen_producer_metadata')
 closures.append({'origin_folder':origin_relative,'archived_folder':A+target_relative,
  'manifest':p(mb),'declared_rows':12,'included_declared_rows':12,'all_declared_payloads_selected':True,
  'original_source_only_not_execution_relocated':True,'omitted_members':[]})
def create():
 carry_path=PROGRAM/'audits/pr212_30005310/next_checkpoint_carry_preparation_01/PROPOSED_CARRY_INVENTORY.json'
 cb,unused=read_file(carry_path)
 need(p(cb)=={'bytes':150305,'sha256':'47c291d5f4c3bb86ad6745a10d72628d850825d10733707584416550d546ec13'},'Frozen carry inventory')
 carry=json.loads(cb);need(len(carry['files'])==149,'Finite149 carry')
 for r in carry['files']:
  need(r['local_source']==str(CHECKOUT/r['path']) and r['source_mode']=='0444','Exact original carry source')
  row=add(r['path'],Path(r['local_source']),r['evidence_class']+'; '+r['role'],'exact_finite149_carry_exception',r,carry=True)
  need(row['observed_source_mode']=='0444' and row['git_blob']==r['native_blob_sha1'],'Carry readonly/native identity')
 need(sum(r['bytes'] for r in rows.values())==784242,'Exact149 carry bytes')
 for n in ['PROPOSED_CARRY_INVENTORY.json','CARRY_SCOPE_REPORT.md','PUBLIC_MANIFEST.json','EXTERNAL_SEAL.json','TERMINAL_INCLUSION_STATUS.json','VALIDATION_RESULT.json','RESEARCH_LOG.md']:
  archive(str(carry_path.parent.relative_to(CHECKOUT))+'/'+n,'prior212_carry_selection_archive_01/'+n,
          'PR212 finite carry curation metadata; retains summary-only nativecandidate05 omission disclosure')
 for n in ['ROOT_CASE_READY_ADOPTION_ACCEPTANCE_01.json','ROOT_CURRENT_PRIORITY_ADDENDUM_01.md',
  'ROOT_EXISTING_PUBLICATION_ADOPTION_ACCEPTANCE_01.json','ROOT_EXISTING_PUBLICATION_OBSERVATION_01.json',
  'ROOT_INTAKE_RESEARCH_LOG_01.md','ROOT_MATHEMATICAL_ACCEPTANCE_01.json','ROOT_MATHEMATICAL_RECONSTRUCTION_01.md',
  'ROOT_NATIVE_COMPLETION_IDENTITY_ACCEPTANCE_01.json','ROOT_NATIVE_CUSTODY_ACCEPTANCE_01.json',
  'ROOT_NATIVE_CUSTODY_REPLAY_01.py','ROOT_POST_MERGE_MAIN_DRIFT_ACCEPTANCE_01.json',
  'ROOT_PRIORITY_ACCEPTANCE_01.json','ROOT_PRIOR_REVIEW_HISTORY_ACCEPTANCE_01.json',
  'ROOT_PR212_FINITE_CARRY_SELECTION_ACCEPTANCE_01.json','ROOT_COMPLETION_SOURCE_READING_01.json',
  'ROOT_COMPLETION_ENGINE_SOURCE_ACCEPTANCE_02.json',
  'root_external_adoption_recheck_01/ACTUAL_OBSERVATIONS.json','root_primary_source_01/ROOT_PDF_VISUAL_INSPECTION_01.json',
  'root_primary_source_01/ROOT_UPSTREAM_SOURCE_READING_01.json']:
  leaf(n,'Explicit accepted Root/context receipt; source reading01 retains historical unaccepted repair boundary')
 for folder,manifest,seal,role,historical in [
  ('native_source_custody_01','PUBLIC_MANIFEST.json','EXTERNAL_SEAL.json','Authenticated custody authored finite selection',False),
  ('operator_adversary_01','PUBLIC_MANIFEST.json','EXTERNAL_SEAL.json','Independent operator-family audit',False),
  ('geometry_adversary_01','PUBLIC_MANIFEST_01.json','EXTERNAL_SEAL_01.json','Independent geometry-family audit',False),
  ('reproduction_adversary_01','PUBLIC_MANIFEST.json','EXTERNAL_SEAL.json','Independent mathematical reproduction selected authored records',False),
  ('priority_author_updates_01','AUTHORED_MANIFEST.json','EXTERNAL_SEAL.json','Dated author/priority update authored records, not provider raw bodies',False),
  ('priority_classical_01','AUTHORED_MANIFEST.json','EXTERNAL_SEAL.json','Independent classical priority authored records',False),
  ('prior_package_history_adversary_01','PUBLIC_MANIFEST.json','EXTERNAL_SEAL.json','Accepted prior review/publication history audit',False),
  ('native_completion_design_01','PUBLIC_MANIFEST.json','EXTERNAL_SEAL.json','Source-only design context',False),
  ('native_completion_preparation_01','SOURCE_MANIFEST.json','SOURCE_EXTERNAL_SEAL.json','Historical source01 freeze, superseded pending source02 approval',True),
  ('native_completion_preparation_02','SOURCE_MANIFEST.json','SOURCE_EXTERNAL_SEAL.json','Final repaired02 source freeze only, no execution authority',False)]:
  closure(folder,manifest,seal,role,historical)
 closure('native_merge_source_custody_03','PUBLIC_MANIFEST.json','EXTERNAL_SEAL.json',
         'Root authenticated Main/merge finite authored closure; full native structural cache/journals excluded')
 closure('native_completion_source_adversary_01','PUBLIC_MANIFEST.json','EXTERNAL_SEAL.json',
         'Final independent engine source adversary,198 focused controls;01 defect and02 repair retained')
 closure('native_completion_inspect_roundtrip_02','PUBLIC_MANIFEST.json','EXTERNAL_SEAL.json',
         'Owned synthetic actual-inspector path roundtrip source/evidence only; fake Root terminal fixture excluded')
 archived_closure(PREFIX+'ordered_intakes_after_PR214_20261017/preparation_01','after214_consumer_archive_01/preparation_01',
  'SOURCE_MANIFEST.json','PREPARATION_SEAL.json',
  {'bytes':3031,'sha256':'a35ffbe5d27107e9107223b6cab6ff708e3013de46b71c768883c8cdb60974e2'},
  'Frozen after214 inactive consumer/producer evidence; current review/Root acceptance pending')
 for n in ['PR213_PRESERVED_STATUS_INTAKE.json','PR214_PRESERVED_STATUS_INTAKE.json']:
  archive(PREFIX+'ordered_intakes_after_PR212_20261017/'+n,'ordered_intake_evidence_01/'+n,
          'Actual213 status-only skip /214 original claimed-solved eligibility receipt, not mathematics')
 # The consumer is not frozen yet: no guessed binding or selection of its current working files.
 slots=[
  {'id':'after214_consumer_final','status':'UNRESOLVED','required':'Frozen12-file consumer producer closure and published-generated integration are now explicitly archived; genuine independent consumer source review/Root acceptance remain unresolved and must be added by exact positive public pins.'},
  {'id':'logical_selection_preparation_final','status':'UNRESOLVED','required':'This final source/controls/manifest/report closure and later independent exact selection review artifacts; no circular self-hash guessed.'},
  {'id':'native_local_preimages_and_exact_ancestor_scope','status':'UNRESOLVED','required':'Separate Root capture of fresh native selected tuples/full native five bodies, local five bytes/absence, exact ancestor tuple observations. Source-only; not a Main parent admission.'},
  {'id':'logical_exact_packet_adversary','status':'UNRESOLVED','required':'Independent exact final packet audit and Root logical acceptance after all slots and exact captures are resolved. No actual215 authority.'}]
 for x in slots:
  x['blocks_construction']=x['id'] in ('native_completion_source_adversary_final','after214_consumer_final','logical_selection_preparation_final')
  x['resolution_stage']='before_final_selection' if x['blocks_construction'] else ('capture_input' if x['id']=='native_local_preimages_and_exact_ancestor_scope' else 'external_after_construction')
 selection={'schema':'pr214-inactive-positive-selection-v1','UTC':datetime.now(timezone.utc).isoformat(),
   'PR':214,'operational_authority':False,'actual_completion_claimed':False,'actual_completed_count':53,
   'actual_published_count':37,'conditional_target_counts':[54,38],'conditional_target_only':True,
   'files':[rows[k] for k in sorted(rows)],'total_files':len(rows),'total_bytes':sum(r['bytes'] for r in rows.values()),
   'carry_files':149,'carry_bytes':784242,'declared_closures':closures,'explicit_omissions':omissions,'authored_execution_relocations':relocations,
   'unresolved_slots':slots,
   'resolved_source_review_slot':{'actual_Root_source_acceptance':{'path':A+'ROOT_COMPLETION_ENGINE_SOURCE_ACCEPTANCE_02.json','bytes':5973,'sha256':'a31e782e1b58df53b2c8eaa3f279a37f9dca1ebd2753c3dce902a5be1acc9aa3'},
     'source_review_selected_as_finite_closure':True,'not_actual_completion_or_intake_authority':True},
   'five_postimages_not_constructed':True,'actual_five_and_lock_not_read':True,
   'future_engine_source_base':A+'native_completion_preparation_02',
   'future_relative_source_pattern':'_private_logical_packet_01/sources/NNNN.txt',
   'all_body_copies_and_native_preimages_pending_Root_selection':True}
 need(len(rows)+5<=600 and selection['total_bytes']<8_000_000,'Bounded known selection with five/pending budget')
 for name,obj in [('PROPOSED_PUBLIC_SELECTION.json',selection)]:
  (HERE/name).open('x').write(json.dumps(obj,indent=2)+'\n')
 print(json.dumps({'known_selected_files':len(rows),'known_selected_bytes':selection['total_bytes'],
    'pending_slots':len(slots),'carry_files':149,'carry_bytes':784242,'omitted_manifest_rows':len(omissions),
    'no_copies_or_captures_executed':True}))
if __name__=='__main__':create()
