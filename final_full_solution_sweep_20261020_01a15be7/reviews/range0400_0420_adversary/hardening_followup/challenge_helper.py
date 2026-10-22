"""Independent malformed-cache controls; all writes stay inside this follow-up."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import os,json,hashlib,subprocess,importlib.util,copy,datetime
REPO=Path('/Users/alec/Documents/Math')
OUT=Path(__file__).resolve().parent
INPUTS=OUT/'inputs'
MODE='optimized' if sys.flags.optimize else 'normal'
os.environ['GIT_OPTIONAL_LOCKS']='0'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
sys.path.insert(0,str(INPUTS))
spec=importlib.util.spec_from_file_location('hardened_scope_snapshot',INPUTS/'pinned_scope_check.py')
helper=importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)

def git(args):
 return subprocess.run(args,cwd=REPO,capture_output=True,check=True).stdout

def ensure(sha):
 git(['git','cat-file','-e',sha+'^{commit}'])
helper.run=git
helper.ensure_commit=ensure
fixture=OUT/('fixtures_'+MODE)
(fixture/'eligibility').mkdir(parents=True,exist_ok=True)
helper.ROOT=fixture
inventory=json.loads((INPUTS/'inventory_range_snapshot.json').read_text())
evidence={n:json.loads((INPUTS/f'pr{n:04d}.json').read_text()) for n in range(400,421)}
records={r['number']:r for r in inventory['pull_requests']}


def set_input(n,e,inv=None):
 (fixture/'rest_inventory.json').write_text(json.dumps(inv or {'pull_requests':[records[n]]}))
 (fixture/'eligibility'/f'pr{n:04d}.json').write_text(json.dumps(e))

actual=[]
for n in range(400,421):
 set_input(n,evidence[n]);saved=[];helper.atomic_json=lambda path,value:saved.append(value)
 result=helper.check(n)
 if len(saved)!=1 or saved[0] is not result:raise RuntimeError('Unexpected receipt-writer behavior')
 actual.append(result)
(OUT/f'actual_range_{MODE}.json').write_text(json.dumps(actual,indent=2)+'\n')
results=[]

def case(name,mutation,expected='reject',n=400,inventory_mutation=None,note=None):
 e=copy.deepcopy(evidence[n]);inv={'pull_requests':[copy.deepcopy(records[n])]}
 mutation(e)
 if inventory_mutation:inventory_mutation(inv)
 set_input(n,e,inv);saved=[];helper.atomic_json=lambda path,value:saved.append(value)
 try:
  r=helper.check(n);observed='pass';error=None;error_class=None
 except Exception as ex:
  r=None;observed='reject';error=str(ex);error_class=type(ex).__name__
 item={'case':name,'pr':n,'expected':expected,'observed':observed,'as_expected':observed==expected,'receipt_count':len(saved),'error_class':error_class,'error':error,'queue_blob_equal':[b['equal'] for b in r['queue_blobs']] if r else None,'note':note}
 if observed=='reject' and saved:raise RuntimeError('Rejected cache wrote a receipt')
 results.append(item)

# Path multiset and type challenges, including equal-count duplicate replacement.
case('duplicate_cached_path_append',lambda e:e['changed_paths'].append(e['changed_paths'][0]))
case('duplicate_cached_path_same_count',lambda e:e['changed_paths'].__setitem__(-1,e['changed_paths'][0]))
case('cached_paths_dictionary',lambda e:e.update(changed_paths={p:True for p in e['changed_paths']}))
case('cached_paths_null',lambda e:e.update(changed_paths=None))
case('cached_path_nested_list',lambda e:e['changed_paths'].__setitem__(-1,[e['changed_paths'][-1]]))
case('cached_path_integer',lambda e:e['changed_paths'].__setitem__(-1,7))
case('cached_path_boolean',lambda e:e['changed_paths'].__setitem__(-1,True))
case('cached_paths_reordered',lambda e:e['changed_paths'].reverse(),'pass')

# file_count must be a JSON integer, including the one-file bool==1 boundary.
for label,value in [('bool_true',True),('bool_false',False),('float_equal',49.0),('numeric_string','49'),('null',None),('negative',-1),('zero',0),('smaller',48),('larger',50)]:
 case('file_count_'+label,lambda e,v=value:e.update(file_count=v))
case('file_count_bool_true_one_file',lambda e:e.update(file_count=True),n=415)
case('file_count_float_equal_one_file',lambda e:e.update(file_count=1.0),n=415)
case('file_count_missing',lambda e:e.pop('file_count'))

# Cached files must contain exactly the same filename multiset.
case('files_missing_entry',lambda e:e['files'].pop())
case('files_extra_duplicate_entry',lambda e:e['files'].append(copy.deepcopy(e['files'][0])))
case('files_duplicate_name_same_count',lambda e:e['files'][-1].update(filename=e['files'][0]['filename']))
case('files_wrong_name_same_count',lambda e:e['files'][-1].update(filename='foreign/REPORT.md'))
case('files_filename_key_missing',lambda e:e['files'][-1].pop('filename'))
case('files_filename_null',lambda e:e['files'][-1].update(filename=None))
case('files_filename_list',lambda e:e['files'][-1].update(filename=[e['files'][-1]['filename']]))
case('files_string_entry',lambda e:e['files'].__setitem__(-1,e['files'][-1]['filename']))
case('files_null',lambda e:e.update(files=None))
case('files_dictionary',lambda e:e.update(files={str(i):f for i,f in enumerate(e['files'])}))
case('files_reordered',lambda e:e['files'].reverse(),'pass')

# Independent row/queue checks still fail closed for material changes.
case('queue_change_missing',lambda e:e.update(queue_changes=[]))
case('queue_change_duplicated',lambda e:e['queue_changes'].append(copy.deepcopy(e['queue_changes'][0])))
case('queue_change_wrong_path',lambda e:e['queue_changes'][0].update(path='foreign/QUEUE.md'))
case('queue_change_null',lambda e:e.update(queue_changes=None))
case('added_row_missing',lambda e:e.update(added_queue_rows=[]))
case('added_row_duplicate',lambda e:e['added_queue_rows'].append(copy.deepcopy(e['added_queue_rows'][0])))
case('added_row_wrong_status',lambda e:e['added_queue_rows'][0].update(status='claimed_solved'))
case('added_row_wrong_id',lambda e:e['added_queue_rows'][0].update(problem_id='foreign'))
case('added_row_wrong_source',lambda e:e['added_queue_rows'][0].update(source_line=e['added_queue_rows'][0]['source_line']+' '))
case('added_row_wrong_queue_path',lambda e:e['added_queue_rows'][0].update(queue_path='foreign/QUEUE.md'))
case('added_rows_null',lambda e:e.update(added_queue_rows=None))
case('added_row_empty_object',lambda e:e['added_queue_rows'].__setitem__(0,{}))

# Intended scope: cached whole-blob/patch fields are not an identity gate.
case('well_formed_different_cached_queue_sha_disclosed',lambda e:e['queue_changes'][0].update(sha='0'*40),'pass',note='Existing design: actual paths/rows are checked; mismatch is explicitly disclosed.')
case('actual_411_merged_context_difference',lambda e:None,'pass',n=411,note='Uses real, unchanged merged-context QUEUE cache.')
case('files_blob_sha_ignored_by_scope',lambda e:e['files'][-1].update(sha='0'*40),'pass',note='Receipt claims path and row scope, not all file-byte identity.')
case('cached_queue_patch_ignored_by_scope',lambda e:e['queue_changes'][0].update(patch='deliberately wrong cached patch'),'pass',note='Actual pinned patch is independently read; cached added rows remain checked.')

# Additional schema boundaries: distinguish permissive extras from false claims.
case('extra_unrelated_queue_change_ignored',lambda e:e['queue_changes'].append({'path':'foreign/QUEUE.md','sha':'0'*40,'patch':'bogus'}),'pass',note='No advertised full-cache-schema validation; actual canonical QUEUE path remains independently checked.')
case('empty_added_rows_object_on_header_only_pr',lambda e:e.update(added_queue_rows={}),'pass',n=415,note='Empty mapping is vacuously iterated as no rows; narrow schema permissiveness, actual row set remains empty.')
case('numeric_equal_pr_float',lambda e:e.update(pr=400.0),'pass',note='Numerically equal JSON number accepted by identity comparison; no wrong PR bound.')
case('conflicting_duplicate_inventory_entry_ignored',lambda e:None,'pass',inventory_mutation=lambda inv:inv['pull_requests'].append({**inv['pull_requests'][0],'headRefOid':'0'*40}),note='The first matching inventory entry is used; inventory uniqueness remains upstream responsibility.')

# Strong fail-closed requirement for every rejected malformed cache, even under -O.
if any(not r['as_expected'] for r in results):raise RuntimeError('Unexpected control outcome')
if any(r['receipt_count']!=1 for r in results if r['observed']=='pass'):raise RuntimeError('Accepted cache failed to write one observational receipt')
pr411=next(r for r in actual if r['pr']==411)
if len(pr411['queue_blobs'])!=1 or pr411['queue_blobs'][0]['equal'] is not False:raise RuntimeError('Actual411 disclosed context difference was lost')
summary={'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mode':MODE,'optimization':sys.flags.optimize,'helper_sha256':hashlib.sha256((INPUTS/'pinned_scope_check.py').read_bytes()).hexdigest(),'actual_range_pass_count':len(actual),'actual_411_queue_blobs':pr411['queue_blobs'],'control_count':len(results),'rejected_count':sum(r['observed']=='reject' for r in results),'accepted_count':sum(r['observed']=='pass' for r in results),'all_expected':all(r['as_expected'] for r in results),'results':results,'provider_or_shared_git_mutations':False,'receipt_writes_redirected':True,'bytecode_disabled':sys.dont_write_bytecode}
(OUT/f'controls_{MODE}.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='results'},indent=2))
