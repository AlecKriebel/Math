#!/usr/bin/env python3
"""Own administrative closure; never executes/imports reviewed helpers.
Only writes this independent family, after the entire frozen current review.
Actual administrative PID/UTC/output appear in the caller's tool transcript.
Scientific executions have their separate complete prelaunch/stdio receipts.
"""
from pathlib import Path,PurePosixPath
import datetime,hashlib,json,math,os,stat,sys
R=Path(__file__).resolve().parent;C=R.parent/'reviewed_candidate'
CURRENT='3431ca2dfb332500f3815ea1e61f089744b3bacd9c3659018537016b9396fbfa'
SEAL='f6b27ee8f8a4ba2ccaf6448f1031d2b3103dd03134e096cdccc4247e2b78aa0e'
ROOTCAP='68a9cc23f0b5fedd6624d4e7474b707d8f2727b4ac78193232ff16b4cc376d34'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def H(b):return hashlib.sha256(b).hexdigest()
def check(x,s):
 if not x:raise ValueError(s)
def pairs(xs):
 d={}
 for k,v in xs:check(k not in d,'duplicate JSON key');d[k]=v
 return d
def const(s):raise ValueError(s)
def floating(s):
 x=float(s);check(math.isfinite(x),'nonfinite JSON number');return x
def J(b):return json.loads(b,object_pairs_hook=pairs,parse_constant=const,parse_float=floating)
def load(p):return J(p.read_bytes())
def safe(n):
 p=PurePosixPath(n)
 check(type(n) is str and n and not p.is_absolute() and p.as_posix()==n and '\\' not in n and not {'.','..','.git','__pycache__'}&set(p.parts),'unsafe relative name')
 return n
def inventory(root):
 files=set();dirs=set();check(root.is_dir() and not root.is_symlink(),'regular root')
 for p in root.rglob('*'):
  check(not p.is_symlink(),'symlink '+str(p));n=safe(p.relative_to(root).as_posix())
  if p.is_file():files.add(n)
  else:check(p.is_dir(),'special member '+n);dirs.add(n)
 required={p.as_posix() for n in files for p in PurePosixPath(n).parents if p.as_posix()!='.'}
 check(dirs==required,'unexpected empty directories');return files
def row(p):
 b=p.read_bytes();return {'path':safe(p.relative_to(R).as_posix()),'size':len(b),'sha256':H(b)}
def retained(root,item):
 p=root/safe(item['path']);check(p.is_file() and not p.is_symlink(),'regular capture path')
 b=p.read_bytes();size=item.get('bytes',item.get('size'))
 check(type(size) is int and size>=0 and len(b)==size and H(b)==item['sha256'],'complete retained member')
 return b
def clock(t):
 x=datetime.datetime.fromisoformat(t)
 check(x.tzinfo and x.utcoffset()==datetime.timedelta(0),'explicit aware UTC');return x
def main():
 started=now();check(not (R/'FIRST_PARTY_MANIFEST.json').exists(),'new closure only')
 check(H((R/'SOURCE_FIRST_SCOPE_SEAL.md').read_bytes())==SEAL,'initial source seal immutable')
 raw=(C/'MANIFEST.json').read_bytes();check(H(raw)==CURRENT,'frozen current manifest')
 m=J(raw);check(len(m['files'])==547 and m['self_excluded']==['MANIFEST.json'],'exact547/self current')
 names=set()
 for item in m['files']:
  n=safe(item['path']);check(n not in names,'duplicate current path');names.add(n)
  retained(C,item);check(item['mode']=='0444' and stat.S_IMODE((C/n).stat().st_mode)==0o444,'current immutable mode')
 check(inventory(C)==names|{'MANIFEST.json'},'current exact final membership')
 check(H((R.parent/'root_current_freeze_actual_capture/CAPTURE.json').read_bytes())==ROOTCAP,'root actual current capture unchanged')
 captures=[]
 for name in ['whole_current_actual_capture','supplemental_actual_capture','presentation_stdio_actual_capture','math_boundary_actual_capture','administrative_preclosure_actual_capture']:
  if name=='administrative_preclosure_actual_capture' and '--validate-only' in sys.argv:continue
  obj=load(R/name/'CAPTURE.json')
  check(obj['actual_execution'] is True and obj['completed'] is True and type(obj['pid']) is int and obj['pid']>0 and type(obj['returncode']) is int and obj['returncode']==0 and obj['stdin_supplied'] is False,'own actual complete exit0 capture')
  check(clock(obj['started_utc'])<=clock(obj['finished_utc']),'ordered own clocks')
  source=retained(R,obj['source']);check(source==Path(obj['argv'][2]).read_bytes(),'exact own prelaunch executed source')
  for ch in ['stdout','stderr']:retained(R,obj[ch])
  check(obj['stdout']['path']!=obj['stderr']['path'] and obj['stderr'].get('bytes',obj['stderr'].get('size'))==0,'distinct complete own channels')
  captures.append({'path':name+'/CAPTURE.json','sha256':H((R/name/'CAPTURE.json').read_bytes()),'pid':obj['pid'],'exit_code':obj['returncode'],'started_utc':obj['started_utc'],'finished_utc':obj['finished_utc'],'source_sha256':obj['source']['sha256']})
 early=load(R/'independent_run_receipts.json')
 for obj in early:
  check(type(obj['pid']) is int and obj['pid']>0 and obj['returncode']==0 and clock(obj['started_utc'])<=clock(obj['completed_utc']),'actual early own run')
  retained(R,obj['authored_input'])
  for ch in ['stdout','stderr']:retained(R,obj[ch])
 whole=load(R/'WHOLE_CURRENT_INSPECTION_RESULT.json');supp=load(R/'SUPPLEMENTAL_READONLY_RESULT.json');stdio=load(R/'CURRENT_PRESENTATION_STDIO_RESULT.json');mathres=load(R/'INDEPENDENT_MATH_BOUNDARY_RESULTS.json')
 check(whole['status']=='PASS_INDEPENDENT_WHOLE_CURRENT_BYTE_TYPED_DATA_CONTROLS' and whole['authored_members']==547 and whole['whole_JSON_objects_parsed']==135 and whole['all_SQL_rows_independently_compared']==15458,'actual complete whole inspection')
 check(supp['status']=='PASS_OWN_SUPPLEMENTAL_READONLY_SOURCE_RECEIPT_FINITE_CONTROLS' and supp['independent_original_Git_queries']==34 and supp['unique_current_python_sources']==22 and supp['independent_finite_guard_controls']==17,'actual source/finite controls')
 check(stdio['status']=='PASS_OWN_FULL_STDIO_AND_CURRENT_PRESENTATION_CONTROLS' and stdio['stream_files']==296 and stdio['nonempty_stderr_files']==15,'actual complete stream controls')
 check(mathres['status']=='PASS_OWN_INDEPENDENT_EXACT_MATH_BOUNDARY_CONTROLS' and mathres['passed']==144 and mathres['failed']==0 and len(mathres['checks'])==144 and all(x['result']=='PASS' for x in mathres['checks']),'actual exact144 math controls')
 foreign=[]
 for p in sorted((R/'sources').rglob('*')):
  if p.is_file():foreign.append(row(p))
 check(len(foreign)==17,'individual own foreign source cache17')
 (R/'FOREIGN_SOURCES.json').write_text(json.dumps({'classification':'Foreign primary bodies, extracted/rendered source bodies and exact raw/SQL provenance copies; excluded from authorship, individually bound in final manifest. No whole directory exclusion.','files':foreign,'count':len(foreign)},indent=2)+'\n')
 result={'verdict':'PASS_QUALIFIED_UNSOLVED_PARTIAL_NEW_WHOLE_CURRENT','review_completed':True,'review_completion_percent':100,'new_unconditional_discovery_percent':0,'full_problem_solved':False,'partial_valid':True,'novelty_claimed':False,'mandatory_repairs':[],'scientific_scope':{'unconditional':'Interior expected-length asymptotic and full-length liminf lower bound.','conditional':'Full all-pair prescribed route-union asymptotic under additional t^4 P(D>t)->0; finite fourth moment suffices.','remaining_gap':'Expected full exterior route-union length o(k) under ordinary SIRSN axioms, or an admissible full-SIRSN counterexample.','original_vs_published':'Indexed2012 unconditional question differs from published2014 request for sufficient additional assumptions.','import_limits':'Exact appended Kahn proof qualification; credited existence/uniqueness and continuum foundations imported; no exhaustive literature or novelty certification.'},'reviewed_current':{'path':C.relative_to(R.parents[3]).as_posix(),'manifest_sha256':CURRENT,'members':547,'all_modes':'0444','final_bytes_reverified_before_closure':True,'current_runtime_verdict_remains_present_null_and_PENDING':True},'original':{'head':'292b95ca601f166e6d246e609cf7ed5ca5653e25','base':'c6975ca76f9f667f1250ba403d0e6da2aafe14d0','members':16,'diff_paths':17,'whole_diff_bytes':201709,'proof_sha256':'464af6d259f9275ca9f0056567f5301bc228465fa0ddaf2faece0920cab6bd7c'},'initial_source_seal_sha256':SEAL,'root_current_capture_sha256':ROOTCAP,'root_builder_pid':36236,'root_current_HEAD_at_freeze':'6f7cdb80ac4ed9d7e1179380de540a4eb5d9a534','whole_inspection':{'JSON_objects':135,'typed_nodes':47673,'current_bytes':4970010,'all_SQL_joins':15458,'raw_JSON_bytes':149266659,'dependency_rows':469,'foreign_dependency_inputs':29,'all_original_saved_actual_checks':[211,3809],'all_family_check_objects':[1326,122],'whole_stdio_files':296,'whole_stdio_bytes':1551131,'whole_JSON_streams':45,'whole_JSON_stream_nodes':17031,'nonempty_stderr_bodies':15,'Python_source_copies':58,'unique_Python_sources':22,'complete_source_deltas':7,'independent_original_Git_queries':34,'independent_math_controls':144,'independent_guard_controls':17},'own_actual_capture_receipts':captures,'early_capture_receipt':'independent_run_receipts.json','exposure_disclosure':'Initial source seal predates candidate/family/root contents; later unfiltered agent inventory exposed sibling preparation-summary metadata, immediately disclosed before expressly authorized source-preparation/current inspection. No false perpetual nonexposure claim.','nonblocking_limitations':['CURRENT_CONTEXT and CURRENT_AUDIT_SCOPE inherit appended-below/follows wording without embedding those bodies; exact operative four-surface append and body binding verified.','Builder enforces eighttrue science-card flags more fully than read-ledger flags; actual ledger and card independently verified identical exact eighttrue.','Older network guard does not reject extra empty directories; current builder and own current closure inventory do.','Old sibling captures lacking a recorded child PID remain dated limited records, not invented complete captures.','35227-byte stopped-builder source is deterministic reverse-edit reconstruction, not direct old executed-source capture.'],'original_substantive_attempts':2,'substantive_attempt_limit':5,'new_substantive_attempts':0,'audit_turns':0,'candidate_helpers_imported_or_executed':False,'shared_native_Git_remote_writes':False,'external_human_contact':False,'paper_DOI_tracker_promotion':False,'own_foreign_source_files':len(foreign),'administrative_closure_started_utc':started,'administrative_closure_pid':os.getpid(),'reported_utc':now()}
 (R/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 if '--validate-only' in sys.argv:
  print(json.dumps({'status':'PASS_OWN_ADMINISTRATIVE_PRECLOSURE_VALIDATION','pid':os.getpid(),'started_utc':started,'finished_utc':now(),'current_manifest_sha256':CURRENT,'current547_final_bytes_modes_exact':True,'source_seal_unchanged':True,'scientific_captures_complete_valid':True,'own_manifest_not_yet_written':True,'own_file_modes_not_yet_changed':True,'full_problem_solved':False},indent=2));return
 with (R/'RESEARCH_LOG.md').open('a') as log:log.write('\n- '+now()+': Entire frozen CURRENT review and all own controls complete; qualified partial PASS, full indexed target UNSOLVED. Exact final current bytes/modes/membership rechecked, source seal unchanged, all own actual receipt channels/source/PIDs/clocks verified. Administrative exact family closure follows with17 individually itemized foreign source bodies and only the literal root self manifest excluded. Review100%, new discovery0%, original2/5,new0/audit0.\n')
 members=inventory(R);check('FIRST_PARTY_MANIFEST.json' not in members,'literal root self absent before close')
 foreign_names={x['path'] for x in foreign};owned=sorted(members-foreign_names)
 check(all(not (R/x).is_symlink() for x in members),'own nonsymlinks')
 files=[row(R/n) for n in owned]
 for n in members:os.chmod(R/n,0o444)
 check(all(stat.S_IMODE((R/n).stat().st_mode)==0o444 for n in members),'all owned/foreign modes0444')
 manifest={'status':'CLOSED_NEW_WHOLE_CURRENT_SOURCE_FIRST_REVIEW','closed_utc':now(),'administrative_pid':os.getpid(),'reviewed_current_manifest_sha256':CURRENT,'source_first_seal_sha256':SEAL,'result_sha256':H((R/'RESULT.json').read_bytes()),'report_sha256':H((R/'WHOLE_CURRENT_ADVERSARIAL_REVIEW.md').read_bytes()),'excluded':['FIRST_PARTY_MANIFEST.json'],'files_count':len(files),'foreign_count':len(foreign),'all_members_0444':True,'files':files,'foreign_files':foreign}
 dest=R/'FIRST_PARTY_MANIFEST.json';dest.write_text(json.dumps(manifest,indent=2)+'\n');os.chmod(dest,0o444)
 check(inventory(R)==set(x['path'] for x in files)|foreign_names|{'FIRST_PARTY_MANIFEST.json'},'exact final self-only family membership')
 for item in files+foreign:retained(R,item)
 print(json.dumps({'administrative_closure_pid':os.getpid(),'status':manifest['status'],'closed_utc':manifest['closed_utc'],'manifest':row(dest),'owned_members':len(files),'foreign_members':len(foreign),'exact_recursive_membership':True,'all0444':True,'verdict':result['verdict'],'full_problem_solved':False,'report':row(R/'WHOLE_CURRENT_ADVERSARIAL_REVIEW.md'),'result':row(R/'RESULT.json')},indent=2))
if __name__=='__main__':main()
