"""Independent genuine ROOT prerequisite/capture reconciliation and negative controls."""
from pathlib import Path
import copy,datetime as dt,hashlib,json,math,os,sys
F=Path(__file__).absolute().parent;A=F.parent;C=A/'reviewed_candidate';checks=[]
assert __debug__ and not sys.flags.optimize
def ck(n,v):
 if v is not True:raise AssertionError(n)
 checks.append(n)
def refuse(n,fun):
 try:fun()
 except (ValueError,AssertionError,KeyError,TypeError):checks.append(n);return
 raise AssertionError(n+' accepted')
def sha(b):return hashlib.sha256(b).hexdigest()
def unique(xs):
 out={}
 for k,v in xs:
  if k in out:raise ValueError('duplicate')
  out[k]=v
 return out
def floating(s):
 x=float(s)
 if not math.isfinite(x):raise ValueError('nonfinite')
 return x
def strict(b):return json.loads(b,object_pairs_hook=unique,parse_float=floating,parse_constant=lambda s: (_ for _ in ()).throw(ValueError(s)))
def obj(p):return strict(p.read_bytes())
def utc(s):
 x=dt.datetime.fromisoformat(s[:-1]+'+00:00' if s.endswith('Z') else s)
 if x.tzinfo is None or x.utcoffset()!=dt.timedelta(0):raise ValueError('UTC')
 return x
def equal(a,b):
 if type(a) is not type(b):return False
 if type(a) is dict:return a.keys()==b.keys() and all(equal(a[k],b[k]) for k in a)
 if type(a) is list:return len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
 return a==b
for b in [b'{"x":1,"x":2}',b'NaN',b'Infinity',b'-Infinity',b'1e999']:
 refuse('strict JSON rejects '+repr(b),lambda b=b:strict(b))
ck('typed zero differs false',equal(0,False) is False);ck('typed absence/null/object differ',equal(None,{}) is False)
prep=obj(A/'current_preparation_family_v2/PREPARATION_MANIFEST.json');cut=utc(prep['utc'])
root=C/'root_approval';ledger=obj(root/'ROOT_PRIMARY_READ_LEDGER.json');science=obj(root/'ROOT_SCIENCE_CARD.json')
scope=(root/'ROOT_CURRENT_KNOWN_RESULT_SCOPE_CERTIFICATE.md').read_bytes();evidence=obj(root/'ROOT_EVIDENCE_BINDINGS.json');fresh=obj(root/'ROOT_CURRENT_INPUT_PREIMAGES.json')
flags=['original13_complete14_path_diff_helpers_results_metadata_fully_read','operative_OWR668669_v1Theorem2_Section22_v2Example1_Lemma9_Theorem3_fully_read','every_degree_all_periods_RP1_full2dplus1_ordinary_real_open_proof_accepted','whole_raw_SQL_prior_presence_or_null_and_literal_empty_fallback_fully_read','unchanged_author51_and_independent848_actual_reproductions_fully_read','both_closed_independent_math_families_fully_read','scoped_original_closure_family_exclusions_first_party_topology_checked','known_Kozhasov_Kummer_preprint_credit_no_discovery_scope_accepted','new_source_adversary_closed_clean_complete_report_personally_read']
for n,x in [('ledger',ledger),('science',science)]:
 ck('actual nine flags '+n,equal(x['root_flags'],{flag:True for flag in flags}) and x['reading_completed'] is True)
 ck('actual ROOT UTC after source closure '+n,cut<=utc(x['created_utc'])<=dt.datetime.now(dt.timezone.utc))
 ck('actual ROOT directory '+n,x['operative_preparation_directory']=='current_preparation_family_v2')
 ck('actual scope hash '+n,x['scope_certificate_sha256']==sha(scope))
 ck('actual evidence hash '+n,x['evidence_bindings_sha256']==sha((root/'ROOT_EVIDENCE_BINDINGS.json').read_bytes()))
 for k,v in [('original_substantive_attempts',0),('original_source_verification_responses',1),('new_substantive_attempts',0),('audit_turns',0)]:ck('actual typed accounting '+n+k,type(x[k]) is int and x[k]==v)
ck('actual science credit gate',science['project_solved'] is False and science['existing_result_credit']==['Khazhgali Kozhasov','Mario Kummer'] and science['source_publication_kind']=='preprint' and science['new_whole_current_gate']=='PENDING')
ck('actual science ledger hash',science['read_ledger_sha256']==sha((root/'ROOT_PRIMARY_READ_LEDGER.json').read_bytes()))
ck('actual science native13 hash',science['current_input_manifest_sha256']==sha((root/'ROOT_CURRENT_INPUT_PREIMAGES.json').read_bytes()))
ck('exact current13/evidence top keys',set(fresh)=={'schema','approved_by_root','created_utc','reason','current_head','files','operative_preparation_directory'} and set(evidence)=={'schema','approved_by_root','created_utc','notes','manifest','proof_notes','summary','raw_audit','source_adversary','operative_preparation_directory'})
for k in ['manifest','proof_notes','summary','raw_audit','source_adversary']:
 row=evidence[k];b=(A/row['path']).read_bytes();ck('complete genuine evidence ref '+k,len(b)==row['bytes'] and sha(b)==row['sha256'])
record=obj(A/evidence['source_adversary']['path']);manifest=obj(A/record['manifest']['path'])
anch=Path(record['manifest']['path']).parent.as_posix();normalized=[{k:x[k] for k in ['path','bytes','sha256']} for x in manifest['files']]
for row in normalized:row['path']=anch+'/'+row['path']
ck('complete SOURCE members normalized exact',equal(record['members'],normalized))
ck('source actual completed root record scope',record['approved_by_root'] is True and record['complete_report_personally_read'] is True and record['closed_clean'] is True and record['mandatory_corrections']==[] and record['report']['path'] in {x['path'] for x in normalized})
completed=obj(A/'ROOT_ACTUAL_CURRENT_FREEZE_INSPECTION.json');readback=obj(F/'READBACK_RESULT.json')
ck('ROOT full final original commands independently match',equal(completed['complete_final_original_inner_commands'],readback['entire_original_final_inner_commands']))
ck('ROOT actual outer capture independently matches',equal(completed['complete_actual_outer_capture'],readback['entire_original_outer_capture']))
ck('ROOT evidence future gates honest',completed['new_whole_current_gate']=='PENDING' and completed['future_acceptance_approved'] is False and completed['old_PASS_transferred'] is False and completed['stable9_live_match'] is True)
def validate_cap(x):
 if x['actual_execution'] is not True or x['completed'] is not True or type(x['pid']) is not int or x['pid']<=0 or type(x['exit_code']) is not int or x['exit_code']!=0 or x['stdin_supplied'] is not False:raise ValueError('actual capture')
 if not (utc(x['started_utc'])<=utc(x['finished_utc'])<=dt.datetime.now(dt.timezone.utc)):raise ValueError('chronology')
toy=copy.deepcopy(readback['entire_original_outer_capture']);validate_cap(toy);checks.append('positive actual capture predicate')
for k,v in [('actual_execution',1),('actual_execution',False),('completed',1),('completed',False),('pid',True),('pid',0),('exit_code',False),('exit_code',1),('stdin_supplied',0),('stdin_supplied',True),('started_utc','2026-10-04T00:00:00Z'),('finished_utc','2026-10-02T00:00:00Z')]:
 refuse('reject forged completion '+k+repr(v),lambda k=k,v=v:validate_cap(dict(toy,**{k:v})))
def native(body,row):
 if type(row['bytes']) is not int or row['bytes']<0 or type(row['full_mode']) is not int or not 0<=row['full_mode']<4096:raise ValueError('native types')
 if len(body)!=row['bytes'] or sha(body)!=row['sha256']:raise ValueError('whole native body')
good={'bytes':3,'sha256':sha(b'abc'),'full_mode':0o644};native(b'abc',good);checks.append('positive complete native predicate')
for k,v in [('bytes',True),('bytes',3.0),('full_mode',True),('full_mode',-1),('full_mode',4096)]:
 refuse('reject native scalar '+k+repr(v),lambda k=k,v=v:native(b'abc',dict(good,**{k:v})))
refuse('reject same length native mutation',lambda:native(b'abd',good))
for mode in range(4096):
 x=dict(good,full_mode=mode);native(b'abc',x)
 checks.append('full typed native mode admitted '+str(mode))
for directory in sorted((F/'captures').iterdir()):
 if not (directory/'CAPTURE.json').exists():
  pre=obj(directory/'PRELAUNCH.json')
  ck('own current outer postexit receipt legitimately absent',pre['operator_pid']==os.getppid() and pre['actual_execution'] is False and pre['completed'] is False)
  continue
 cap=obj(directory/'CAPTURE.json')
 if directory.name=='additional_reconciliation':
  ck('own first failed capture honestly preserved',cap['actual_execution'] is True and cap['completed'] is True and cap['pid']==98221 and type(cap['exit_code']) is int and cap['exit_code']==1 and utc(cap['started_utc'])<=utc(cap['finished_utc']))
 else:
  validate_cap(cap)
 ck('own complete captured source '+directory.name,sha((directory/'PRELAUNCH_SOURCE.py').read_bytes())==cap['source_sha256'])
 ck('own complete captured operator '+directory.name,sha((directory/'PRELAUNCH_OPERATOR.py').read_bytes())==cap['operator_sha256'])
 for channel in ['stdout','stderr']:
  b=(directory/cap[channel]['path']).read_bytes();ck('own full capture stream '+directory.name+channel,len(b)==cap[channel]['bytes'] and sha(b)==cap[channel]['sha256'])
result={'schema':'pr46-whole-independent-prerequisite-and-capture-controls/v1','actual_pid':os.getpid(),'passed':len(checks),'failed':0,'checks':checks,'complete_ROOT_postexit_evidence_reconciled':True,'production_run':False,'future_acceptance_approved':False}
(F/'ADDITIONAL_RECONCILIATION_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['schema','actual_pid','passed','failed','complete_ROOT_postexit_evidence_reconciled']},indent=2))
