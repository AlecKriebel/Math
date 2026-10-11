"""Complete external capture, genuine prerequisite and own capture reconciliation."""
from pathlib import Path
import datetime as dt, hashlib, json, os, stat, sys
F=Path(__file__).absolute().parent;A=F.parent;R=A.parents[2];E=A.parent/'pr45_9900007';C=A/'reviewed_candidate'
assert __debug__ and not sys.flags.optimize
checks=0;bindings=[];captures=[]
def ck(v):
 global checks
 assert v;checks+=1
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):
 ck(not p.is_symlink() and stat.S_ISREG(p.stat().st_mode) and all(not q.is_symlink() for q in p.parents))
 b=p.read_bytes();bindings.append({'path':str(p),'bytes':len(b),'sha256':sha(b),'full_mode':stat.S_IMODE(p.stat().st_mode)});return b
def obj(p):return json.loads(read(p))
def clock(v):
 ck(type(v) is str);t=dt.datetime.fromisoformat(v.replace('Z','+00:00'));ck(t.tzinfo is not None and t.utcoffset()==dt.timedelta(0));return t
def stream(root,row):
 ck(type(row) is dict and type(row['bytes']) is int and row['bytes']>=0)
 b=read(root/row['path']);ck(len(b)==row['bytes'] and sha(b)==row['sha256']);return b
def explicit(d):
 files=set(p.name for p in d.iterdir());ck(files=={'CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin'})
 c=obj(d/'CAPTURE.json');ck(c['schema']=='root-explicit-command-capture/v1' and c['actual_execution'] is True and c['completed'] is True and c['stdin_supplied'] is False and type(c['pid']) is int and c['pid']>0 and type(c['exit_code']) is int)
 ck(clock(c['started_utc'])<=clock(c['finished_utc'])<=dt.datetime.now(dt.timezone.utc));ck(sha(read(d/'prelaunch_operator.py'))==c['operator_sha256'] and c['operator_unchanged'] is True)
 so=stream(d,c['stdout']);se=stream(d,c['stderr'])
 ck(c['exit_code']==c['expected_exit_code'])
 if c['exit_code']==0:ck(se==b'')
 captures.append({'directory':str(d),'entire_capture':c,'entire_stdout_UTF8':so.decode(),'entire_stderr_UTF8':se.decode()});return c,so,se
for d in sorted(E.glob('root_pr47*_capture')):
 if (d/'CAPTURE.json').exists():explicit(d)
for n in ['root_cover_algebra_closure_actual_capture','root_cover_algebra_closed_readback_actual_capture','root_gauge_geometry_verify_actual_capture']:
 d=E/n
 if d.exists():explicit(d)
named={Path(x['directory']).name:x for x in captures}
for prefix,source,pid,verifier in [('root_pr47_source_v2',A/'current_preparation_family_v2/PREPARATION_MANIFEST.json',32176,32684),('root_pr47_source_v2_adversary',A/'current_source_adversary_family_v2/SELF_MANIFEST.json',48213,48451)]:
 close=named[prefix+'_closure_actual_capture'];verify=named[prefix+'_closed_readback_actual_capture'];m=obj(source);t=m.get('utc',m.get('created_utc'))
 ck(close['entire_capture']['pid']==pid and verify['entire_capture']['pid']==verifier)
 ck(clock(close['entire_capture']['started_utc'])<=clock(t)<=clock(close['entire_capture']['finished_utc'])<clock(verify['entire_capture']['started_utc']))
 for x in [close,verify]:ck(json.loads(x['entire_stdout_UTF8'])['manifest_sha256']==sha(read(source)))
author=named['root_pr47_current_prerequisites_authoring_actual_capture'];ck(author['entire_capture']['pid']==53137)
printed=json.loads(author['entire_stdout_UTF8']);ck(printed['future_acceptance_approved'] is False and printed['new_whole_current_review']=='PENDING')
for row in printed['five_prerequisites']+[printed['source_record']]:stream(A,row)
ck(len(printed['five_prerequisites'])==5)
ck(clock(author['entire_capture']['started_utc'])<=clock(printed['created_utc'])<=clock(author['entire_capture']['finished_utc']))
ar=obj(A/'ROOT_NEW_SOURCE_ADVERSARY_RECORD.json');ck(ar['future_acceptance_approved'] is False and ar['current_whole_verdict'] is None and ar['production_executed'] is False and ar['closed_clean'] is True)
ck(sha(read(A/'ROOT_NEW_SOURCE_ADVERSARY_RECORD.json'))=='dd99ada155d0d43091444c6b5154e53ab41a3df640665019d98b3379250f01f5')
for x in ar['complete_external_closing_and_readback_evidence']:
 d=R/x['directory'];ck(obj(d/'CAPTURE.json')==x['entire_actual_capture']);ck(obj(d/'stdout.bin')==x['entire_stdout_value'])
 for row in x['members']:stream(R,row);ck(stat.S_IMODE((R/row['path']).stat().st_mode)==row['full_mode'])
for row in ar['members']:stream(A,row)
ck(obj(A/ar['report']['path']) if False else read(A/ar['report']['path'])==read(C/'new_source_adversary'/ar['report']['path']))
read(A/'author_ROOT_current_prerequisites.py')
draft=obj(A/'current_preparation_family_v2/DRAFT_ROOT_READ_LEDGER.json'); flags={k:True for k in draft['root_flags']}
ledger=obj(A/'ROOT_PRIMARY_READ_LEDGER.json');science=obj(A/'ROOT_SCIENCE_CARD.json');fresh=obj(A/'ROOT_CURRENT_INPUT_PREIMAGES.json');evidence=obj(A/'ROOT_EVIDENCE_BINDINGS.json')
for o in [ledger,science]:
 ck(o['root_flags']==flags and o['reading_completed'] is True and o['operative_preparation_directory']=='current_preparation_family_v2')
 ck(type(o['original_substantive_attempts']) is int and o['original_substantive_attempts']==1 and type(o['audit_turns']) is int and o['audit_turns']==0 and type(o['new_substantive_attempts']) is int and o['new_substantive_attempts']==0)
 ck(clock(o['created_utc'])==clock(printed['created_utc']))
 for k,n in [('scope_certificate_sha256','ROOT_CURRENT_SCOPE_CERTIFICATE.md'),('preparation_manifest_sha256','current_preparation_family_v2/PREPARATION_MANIFEST.json'),('source_qualification_sha256','current_preparation_family_v2/SOURCE_PRECISION_QUALIFICATIONS.md'),('evidence_bindings_sha256','ROOT_EVIDENCE_BINDINGS.json')]:ck(o[k]==sha(read(A/n)))
ck(science['status']=='unsolved' and science['full_problem_solved'] is False and science['realized_example_instanton_rank_computed'] is False and science['universal_normal_vanishing_false'] is True and science['novelty_claimed'] is False)
for k in ['current_model','current_reasoning_effort','current_deadline_utc','current_verdict']:ck(science[k] is None)
for k in ['paper_created','new_DOI_created','tracker_row_created']:ck(science[k] is False)
ck(science['read_ledger_sha256']==sha(read(A/'ROOT_PRIMARY_READ_LEDGER.json')) and science['current_input_manifest_sha256']==sha(read(A/'ROOT_CURRENT_INPUT_PREIMAGES.json')))
for k in ['manifest','proof_notes','summary','raw_audit','source_adversary']:stream(A,evidence[k])
# Every genuine prerequisite Git child and complete streams, with actual null sources.
for d in sorted((A/'root_current_prerequisite_Git_actual_captures').iterdir()):
 c=obj(d/'CAPTURE.json');ck(c['actual_execution'] is True and c['completed'] is True and type(c['exit_code']) is int and c['exit_code']==0 and c['source'] is None and c['source_unchanged'] is None)
 ck(clock(author['entire_capture']['started_utc'])<=clock(c['started_utc'])<=clock(c['finished_utc'])<=clock(author['entire_capture']['finished_utc']))
 stream(d,c['stdout']);ck(stream(d,c['stderr'])==b'')
# Own earlier captures: failed inspections are retained, never relabeled PASS.
own=[]
for d in sorted((F/'captures').iterdir()):
 if not (d/'CAPTURE.json').exists():continue
 c=obj(d/'CAPTURE.json');pre=obj(d/'PRELAUNCH.json')
 ck(c['actual_execution'] is True and c['completed'] is True and type(c['exit_code']) is int and c['pid']>0 and c['operator_pid']==pre['operator_pid'])
 ck(clock(c['started_utc'])<=clock(c['finished_utc'])<dt.datetime.now(dt.timezone.utc))
 ck(sha(read(d/'PRELAUNCH_SOURCE.py'))==c['source_sha256'] and sha(read(d/'PRELAUNCH_OPERATOR.py'))==c['operator_sha256'])
 stream(d,c['stdout']);stream(d,c['stderr']);own.append(c)
result={'schema':'pr47-whole-independent-external-and-prerequisite-reconciliation/v1','actual_pid':os.getpid(),'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'status':'PASS','assertions':checks,'complete_external_records_and_streams':captures,'own_prior_actual_captures':own,'entire_source_adversary_record':ar,'complete_body_bindings':bindings,'ROOT_author53137_and_actual_five_verified':True,'historical_source_only_flags_not_future_current_authority':True,'original_cover_closing10880_persistent_prelaunch_invented':False,'future_acceptance_approved':False}
(F/'SUPPLEMENTAL_READBACK.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','actual_pid':os.getpid(),'assertions':checks,'external_captures':len(captures),'own_prior_captures':len(own)}))
