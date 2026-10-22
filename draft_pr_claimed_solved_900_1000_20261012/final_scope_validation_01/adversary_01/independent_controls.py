#!/usr/bin/env python3
"""Cold offline controls. All GraphQL responses below are synthetic fixtures."""
import argparse, contextlib, copy, hashlib, io, json, os, subprocess, sys, tempfile
from datetime import datetime, timezone
from pathlib import Path

HERE=Path(__file__).resolve().parent
SOURCE=HERE/'resweep_draft_statuses_900_1000.py'
SHARED_SOURCE=HERE.parents[1]/SOURCE.name
PIN='fc8ef5d6493c0088d94441e3a1876b9dc99bbaef84a98320647b84d15d5d048e'
if hashlib.sha256(SHARED_SOURCE.read_bytes()).hexdigest()!=PIN:
 raise RuntimeError('Unconditional external whole-source pin mismatch BEFORE compile')
raw=SOURCE.read_bytes()
if hashlib.sha256(raw).hexdigest()!=PIN:
 raise RuntimeError('Unconditional local backing-copy pin mismatch BEFORE compile')
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
OUT=HERE/args.output
if OUT.parent!=HERE or OUT.exists():raise RuntimeError('New own output directory required')
OUT.mkdir();(OUT/'raw_receipts').mkdir()
tests=[];forbidden_calls=[]

def require(ok,label='Control expectation failed'):
 if not ok:raise RuntimeError(label)
def forbidden(*a,**k):
 forbidden_calls.append('unexpected live operation');raise RuntimeError('No live operation authorized')
def ns():
 n={'__file__':str(SOURCE),'__name__':'cold_offline_source'}
 exec(compile(raw,str(SOURCE),'exec'),n)
 n['run']=forbidden
 return n
def check(label,fn):
 try:fn();tests.append({'name':label,'status':'PASS'})
 except Exception as e:tests.append({'name':label,'status':'FAIL','error':type(e).__name__+': '+str(e)})
def rejects(fn):
 try:fn()
 except Exception:return
 raise RuntimeError('Expected closed rejection')
def row(key='25',status='claimed_solved'):
 return '| 1 | '+key+' / SYNTHETIC | synthetic fixture | 0 | 0 | 0 | 2000 | '+status+' | 0 | | | |'
def sha(s):return hashlib.sha256(s.encode()).hexdigest()
def blob(s):
 b=s.encode();return {'__typename':'Blob','isBinary':False,'text':s,'byteSize':len(b),'oid':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
def pr(number=952):
 return {'number':number,'state':'OPEN','isDraft':True,'headRefOid':'1'*40,'headRefName':'draft/synthetic_25','baseRefName':'main','baseRefOid':'a'*40,'baseRef':{'target':{'oid':'b'*40}},'currentBaseRefOid':'b'*40,'url':'https://example.invalid/pull/'+str(number)}
QUEUE='unsolved_math_prioritization/QUEUE.md'
PATHS=[QUEUE,'synthetic_effort_25/metadata.txt']

def scan(label,status='unsolved',paths=None,seed_patch=None,initial_patch=None,pr_patch=None,second_patch=None,queue=None,blob_patch=None,pages=None,expected='SKIP_STATUS_ONLY',clear=True,min_files=1):
 """Run the actual main controller with 101 synthetic PRs and no service calls."""
 n=ns();p=pr();p.update(pr_patch or {})
 q=row(status=status) if queue is None else queue
 seed={'id':'25','pr_head_queue_row_sha256':sha(row(status=status))}
 seed.update(seed_patch or {})
 initial={'number':952,'headRefOid':'1'*40,'entries':[seed]};initial.update(initial_patch or {})
 first={i:{**pr(i),'state':'CLOSED'} for i in range(900,1001)};first[952]=p
 second=copy.deepcopy(first);second[952].update(second_patch or {})
 inventory=[initial if i==952 else {'number':i,'headRefOid':'1'*40,'entries':[{'id':str(i)}]} for i in range(900,1001)]
 seen=[];metadata_calls=0;file_calls=0;queue_calls=0
 filenames=PATHS if paths is None else paths
 page_fixtures=pages or [{'paths':filenames,'count':len(filenames),'more':False,'cursor':None}]
 def fake_graphql(query,variables=None):
  nonlocal metadata_calls,file_calls,queue_calls
  variables=variables or {};seen.append({'kind':'metadata' if 'p900:pullRequest' in query else 'files' if 'changedFiles files(' in query else 'queue','variables':copy.deepcopy(variables)})
  if 'p900:pullRequest' in query:
   require('baseRef{target{oid}}' in query,'Snapshot must request actual live base pointer')
   metadata_calls+=1;require(metadata_calls<=2,'Unexpected extra metadata snapshot')
   return {f'p{i}':copy.deepcopy((first if metadata_calls==1 else second)[i]) for i in range(900,1001)}
  if 'changedFiles files(' in query:
   require('baseRef{target{oid}}' in query,'Each file page must request actual live base pointer')
   require(variables.get('number')==952,'Wrong synthetic numbered PR')
   require(file_calls<len(page_fixtures),'Unexpected extra file pagination')
   z=page_fixtures[file_calls];file_calls+=1
   reply={**p,'changedFiles':z['count'],'files':{'nodes':[{'path':x} for x in z['paths']],'pageInfo':{'hasNextPage':z['more'],'endCursor':z['cursor']}}}
   reply.update(z.get('override',{}))
   return {'pullRequest':copy.deepcopy(reply)}
  if 'object(expression:$expr)' in query:
   queue_calls+=1;require(variables=={'expr':p['headRefOid']+':'+QUEUE},'QUEUE must use exact immutable current head')
   obj=blob(q);obj.update(blob_patch or {});return {'object':obj}
  raise RuntimeError('Unrecognized synthetic GraphQL query')
 n['graphql']=fake_graphql
 with tempfile.TemporaryDirectory(prefix='fixtures-',dir=OUT) as td:
  d=Path(td);(d/'inventory.json').write_text(json.dumps(inventory));n['P']=d
  previous=sys.argv[:];sys.argv=[str(SOURCE),'--receipt-name','receipt.json']
  try:
   with contextlib.redirect_stdout(io.StringIO()):n['main']()
  finally:sys.argv=previous
  result=json.loads((d/'receipt.json').read_bytes())
  record=next(x for x in result['rows'] if x['pr']==952)
  receipt={'provenance':'OFFLINE SYNTHETIC SERVICE FIXTURES; these are not actual GitHub or Git calls','control':label,'actual_live_service_calls':0,'requests_to_synthetic_callable':seen,'synthetic_controller_receipt':result}
  (OUT/'raw_receipts'/(label+'.json')).write_text(json.dumps(receipt,indent=2)+'\n')
  require(record['action']==expected,'Unexpected action '+record['action']+' expected '+expected)
  require(result['pr_count']==101 and len(result['rows'])==101,'Full synthetic numbered range required')
  require(metadata_calls==2,'Both complete metadata snapshots required')
  require(file_calls>=min_files,'Fresh full canonical file pagination required')
  require(result['completion_scope_clear'] is clear,'Wrong completion clear flag')
  require(all(not x['math_or_source_or_artifact_read'] and not x['remote_mutation'] for x in result['rows']),'Out-of-scope processing marker')
  require(not result['source_math_artifact_reads_or_remote_mutations'],'Out-of-scope aggregate marker')
  if expected in ('SKIP_STATUS_ONLY','ELIGIBLE_REQUIRES_PROCESSING'):
   require(record['status']==status,'Fresh literal status not preserved')
   require(queue_calls==1,'Authenticated fresh QUEUE required')
  return result,record,seen

# Arbitrary statuses establish that the fallback is not an exclusion-status whitelist.
for status in ['claimed_solved','already_solved','unsolved','queued','CLAIMED_SOLVED','claimed_solved_extra','a_brand_new_status']:
 label='legacy_fresh_status_'+status
 check(label,lambda status=status,label=label:scan(label,status=status,expected='ELIGIBLE_REQUIRES_PROCESSING' if status=='claimed_solved' else 'SKIP_STATUS_ONLY',clear=status!='claimed_solved'))
check('legacy_ignores_cached_status',lambda:scan('legacy_ignores_cached_status',seed_patch={'pr_head_status':'claimed_solved','status':'claimed_solved'}))
check('legacy_live_base_advance_requires_fresh_filenames',lambda:scan('legacy_live_base_advance_requires_fresh_filenames',initial_patch={'currentBaseRefOid':'c'*40},min_files=1))
check('legacy_stored_base_without_live_pin_requires_fresh_filenames',lambda:scan('legacy_stored_base_without_live_pin_requires_fresh_filenames',initial_patch={'baseRefOid':'a'*40},min_files=1))
check('exact_known_live_base_cache_permitted',lambda:scan('exact_known_live_base_cache_permitted',initial_patch={'currentBaseRefOid':'b'*40},min_files=0))

identity_failures=[
 ('new_head_no_legacy_fallback',{'pr_patch':{'headRefOid':'2'*40}}),
 ('no_queue_no_legacy_fallback',{'paths':['synthetic_effort_25/a']}),
 ('queue_only_no_legacy_fallback',{'paths':[QUEUE]}),
 ('multiple_legacy_roots_fail',{'paths':[QUEUE,'synthetic_effort_25/a','other_effort_25/b']}),
 ('additional_root_fail',{'paths':[QUEUE,'synthetic_effort_25/a','README.md']}),
 ('case_alias_root_fail',{'paths':[QUEUE,'synthetic_effort_25/a','Synthetic_effort_25/b']}),
 ('case_alias_queue_fail',{'paths':['unsolved_math_prioritization/queue.md','synthetic_effort_25/a']}),
 ('suffix_mismatch_fail',{'paths':[QUEUE,'synthetic_effort_26/a']}),
 ('basename_suffix_is_not_root_authority',{'paths':[QUEUE,'other_root/synthetic_effort_25']}),
 ('bare_root_not_directory_fail',{'paths':[QUEUE,'synthetic_effort_25']}),
 ('branch_name_is_not_identity_authority',{'paths':['README.md']}),
 ('multiple_cached_IDs_fail',{'initial_patch':{'entries':[{'id':'25','pr_head_queue_row_sha256':sha(row(status='unsolved'))},{'id':'26','pr_head_queue_row_sha256':sha(row(status='unsolved'))}]}}),
 ('duplicate_cached_same_IDs_fail',{'initial_patch':{'entries':[{'id':'25','pr_head_queue_row_sha256':sha(row(status='unsolved'))}]*2}}),
 ('cached_ID_bool_fail',{'seed_patch':{'id':True}}),
 ('cached_ID_negative_fail',{'seed_patch':{'id':-25}}),
 ('cached_ID_float_fail',{'seed_patch':{'id':25.0}}),
 ('cached_ID_object_fail',{'seed_patch':{'id':{'id':25}}}),
 ('cached_ID_space_fail',{'seed_patch':{'id':'25 '}}),
 ('cached_hash_missing_fail',{'seed_patch':{'pr_head_queue_row_sha256':None}}),
 ('cached_hash_short_fail',{'seed_patch':{'pr_head_queue_row_sha256':'0'*63}}),
 ('cached_hash_uppercase_fail',{'seed_patch':{'pr_head_queue_row_sha256':'A'*64}}),
 ('cached_hash_bool_fail',{'seed_patch':{'pr_head_queue_row_sha256':True}}),
 ('ambiguous_native_IDs_fail',{'paths':[QUEUE,'synthetic_effort_25/a','unsolved_math_prioritization/attempts/25/a','unsolved_math_prioritization/attempts/26/a']}),
]
for label,kw in identity_failures:
 check(label,lambda label=label,kw=kw:scan(label,expected='UNRESOLVED_IDENTITY',clear=False,**kw))

for label,kw in [
 ('fresh_row_different_from_seed_fail',{'seed_patch':{'pr_head_queue_row_sha256':'0'*64}}),
 ('cached_claimed_row_with_fresh_unsolved_fail',{'seed_patch':{'pr_head_queue_row_sha256':sha(row(status='claimed_solved'))}}),
 ('duplicate_target_rows_fail',{'queue':row(status='unsolved')+'\n'+row(status='claimed_solved')}),
 ('missing_exact_target_row_fail',{'queue':row('250','unsolved')}),
 ('wrong_git_blob_oid_fail',{'blob_patch':{'oid':'0'*40}}),
 ('wrong_blob_size_fail',{'blob_patch':{'byteSize':1}}),
 ('boolean_blob_size_fail',{'blob_patch':{'byteSize':True}}),
 ('binary_blob_fail',{'blob_patch':{'isBinary':True}}),
 ('binary_flag_unknown_fail',{'blob_patch':{'isBinary':None}}),
 ('tree_instead_of_blob_fail',{'blob_patch':{'__typename':'Tree'}}),
 ('head_branch_name_not_immutable_fail',{'pr_patch':{'headRefOid':'main'},'initial_patch':{'headRefOid':'main'}}),
 ('fresh_live_base_missing_fail',{'pr_patch':{'currentBaseRefOid':None,'baseRef':None}}),
 ('fresh_live_base_malformed_fail',{'pr_patch':{'currentBaseRefOid':'main','baseRef':{'target':{'oid':'main'}}}}),
 ('filename_parent_traversal_fail',{'paths':[QUEUE,'synthetic_effort_25/../elsewhere/a']}),
 ('filename_dot_segment_fail',{'paths':[QUEUE,'synthetic_effort_25/./a']}),
 ('filename_double_separator_fail',{'paths':[QUEUE,'synthetic_effort_25//a']}),
 ('filename_absolute_fail',{'paths':[QUEUE,'/synthetic_effort_25/a']}),
 ('filename_backslash_fail',{'paths':[QUEUE,'synthetic_effort_25\\a']}),
 ('filename_null_fail',{'paths':[QUEUE,'synthetic_effort_25/\0a']}),
 ('duplicate_filename_fail',{'paths':[QUEUE,'synthetic_effort_25/a','synthetic_effort_25/a']}),
]:
 check(label,lambda label=label,kw=kw:scan(label,expected='UNRESOLVED_READ',clear=False,min_files=0,**kw))

for label,patch in [('head_end_drift',{'headRefOid':'3'*40}),('stored_base_end_drift',{'baseRefOid':'c'*40}),('live_base_end_drift',{'baseRef':{'target':{'oid':'c'*40}},'currentBaseRefOid':'c'*40}),('draft_end_drift',{'isDraft':False}),('state_end_drift',{'state':'CLOSED'})]:
 check(label,lambda label=label,patch=patch:scan(label,second_patch=patch,clear=False))

# Complete multi-page legacy comparison, then all pagination guards.
page_one=[QUEUE]+['synthetic_effort_25/f'+str(i) for i in range(99)]
two_pages=[{'paths':page_one,'count':101,'more':True,'cursor':'cursor-a'},{'paths':['synthetic_effort_25/f99'],'count':101,'more':False,'cursor':None}]
check('legacy_complete_two_page_positive',lambda:scan('legacy_complete_two_page_positive',pages=two_pages,min_files=2))
pagination_failures=[
 ('incomplete_filename_count_fail',[{'paths':PATHS,'count':3,'more':False,'cursor':None}]),
 ('missing_cursor_fail',[{'paths':PATHS,'count':3,'more':True,'cursor':None}]),
 ('repeated_cursor_fail',[{'paths':PATHS,'count':4,'more':True,'cursor':'x'},{'paths':['synthetic_effort_25/b'],'count':4,'more':True,'cursor':'x'}]),
 ('changing_filename_count_fail',[{'paths':PATHS,'count':3,'more':True,'cursor':'x'},{'paths':['synthetic_effort_25/b'],'count':4,'more':False,'cursor':None}]),
 ('boolean_filename_count_fail',[{'paths':PATHS,'count':True,'more':False,'cursor':None}]),
 ('overbound_filename_count_fail',[{'paths':PATHS,'count':3001,'more':False,'cursor':None}]),
 ('file_page_head_drift_fail',[{'paths':PATHS,'count':2,'more':False,'cursor':None,'override':{'headRefOid':'5'*40}}]),
 ('file_page_live_base_drift_fail',[{'paths':PATHS,'count':2,'more':False,'cursor':None,'override':{'baseRef':{'target':{'oid':'5'*40}}}}]),
 ('file_page_stored_base_drift_fail',[{'paths':PATHS,'count':2,'more':False,'cursor':None,'override':{'baseRefOid':'5'*40}}]),
]
for label,pages in pagination_failures:
 check(label,lambda label=label,pages=pages:scan(label,pages=pages,expected='UNRESOLVED_READ',clear=False))

# Native attempt identities retain their established authority; they never use the legacy seed.
check('native_ID_overrides_legacy_seed_without_fallback',lambda:scan('native_ID_overrides_legacy_seed_without_fallback',paths=[QUEUE,'unsolved_math_prioritization/attempts/25/a'],seed_patch={'id':'999','pr_head_queue_row_sha256':'0'*64}))
check('new_head_native_filename_identity_positive',lambda:scan('new_head_native_filename_identity_positive',paths=[QUEUE,'unsolved_math_prioritization/attempts/25/a'],pr_patch={'headRefOid':'2'*40}))
check('integer_legacy_cached_ID_positive',lambda:scan('integer_legacy_cached_ID_positive',seed_patch={'id':25}))

def parser_test(label,fn):
 check(label,lambda:fn(ns()))
parser_test('target_exact_key_prefix_reject',lambda n:rejects(lambda:n['target_status'](row('250','unsolved'),'25')))
parser_test('target_slash_without_spaces_not_key',lambda n:rejects(lambda:n['target_status'](row('25/SYNTHETIC','unsolved'),'25')))
parser_test('target_duplicate_exact_key_reject',lambda n:rejects(lambda:n['target_status'](row()+'\n'+row(),'25')))
parser_test('strict_duplicate_JSON_reject',lambda n:rejects(lambda:n['strict_json']('{"data":{},"data":{}}')))
parser_test('strict_nonfinite_JSON_reject',lambda n:rejects(lambda:n['strict_json']('{"x":NaN}')))
for label,payload in [('graphql_error_even_with_data',{'errors':[{'message':'synthetic'}],'data':{'repository':{}}}),('graphql_missing_data',{}),('graphql_nonobject',[])]:
 def exercise(n,payload=payload):
  n['run']=lambda a:json.dumps(payload)
  rejects(lambda:n['graphql']('query { synthetic }'))
 parser_test(label,exercise)
parser_test('normalized_live_base_ignores_flattened_spoof',lambda n:require(n['normalize_metadata']({**pr(),'currentBaseRefOid':'f'*40})['currentBaseRefOid']=='b'*40))
parser_test('metadata_incomplete_numbered_range_reject',lambda n:(n.update(graphql=lambda *a,**k:{'p900':pr(900)}),rejects(n['metadata'])))
parser_test('immutable_head_branch_name_reject',lambda n:rejects(lambda:n['immutable_queue']('main')))
parser_test('immutable_queue_empty_blob_reject',lambda n:(n.update(graphql=lambda *a,**k:{'object':blob('')}),rejects(lambda:n['immutable_queue']('1'*40))))

result={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS' if all(x['status']=='PASS' for x in tests) and not forbidden_calls else 'FAIL','actual_python_optimization_level':sys.flags.optimize,'source_sha256':hashlib.sha256(raw).hexdigest(),'source_authentication':'Unconditional explicit RuntimeError before compile, checked shared entire source and independent local backing copy against root-supplied external pin','passed':sum(x['status']=='PASS' for x in tests),'failed':sum(x['status']!='PASS' for x in tests),'actual_live_service_calls':0,'unexpected_live_operation_attempts':len(forbidden_calls),'all_service_responses_are_synthetic_fixtures':True,'tests':tests}
(OUT/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['utc','status','actual_python_optimization_level','passed','failed','actual_live_service_calls','unexpected_live_operation_attempts']}))
if result['status']!='PASS':sys.exit(1)
