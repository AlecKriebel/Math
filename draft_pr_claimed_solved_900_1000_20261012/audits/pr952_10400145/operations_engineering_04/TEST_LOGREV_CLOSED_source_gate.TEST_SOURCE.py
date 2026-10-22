#!/usr/bin/env python3
"""Exercise actual PR952 source_gate with private ephemeral RO-SQLite fixtures.
No private source body is printed or retained. No real Git/service call occurs.
Repinned controls alter only loaded test globals to reach independent guards.
"""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):raise SystemExit('Use -I -S -B')
import argparse,copy,hashlib,json,sqlite3,tempfile
from pathlib import Path
OWN=Path(__file__).resolve().parent;P=OWN.parents[2];A=P/'audits/pr952_10400145';CORE=OWN/'PROPOSED_accept_pr952.py'
def sha(b):return hashlib.sha256(b).hexdigest()
p=argparse.ArgumentParser();p.add_argument('--core-sha256',required=True);p.add_argument('--installed',action='store_true');a=p.parse_args();CORE=P/'accept_pr952.py' if a.installed else CORE;raw=CORE.read_bytes()
if sha(raw)!=a.core_sha256:raise SystemExit('external core pin mismatch')
n={'__name__':'_inert_real_source_gate_','__file__':str(CORE)};exec(compile(raw,str(CORE),'exec',dont_inherit=True,optimize=sys.flags.optimize),n)
private=(A/'source_record_private.txt').read_bytes()
if sha(private)!=n['PRIVATE']:raise SystemExit('private source pinned identity mismatch')
original=json.loads(private);problem=original['problem'];prior=original['prior_research']
if type(prior) is not dict or not prior or sha(json.dumps(prior,sort_keys=True).encode())!=n['PRIOR_REPORT_SHA']:raise SystemExit('actual nonempty prior identity mismatch')
events=[]
def need(ok,message):
 if not ok:raise RuntimeError(message)
def encode(x):return (json.dumps(x,sort_keys=True)+'\n').encode()
def blocked(*args,**kwargs):raise RuntimeError('No real external command allowed')
n['run']=blocked
(OWN/'private_tmp').mkdir(exist_ok=True)
with tempfile.TemporaryDirectory(prefix='source-gate-',dir=OWN/'private_tmp') as td:
 root=Path(td);audit=root/'audit';audit.mkdir();cache=root/'unsolved_math_prioritization/cache';cache.mkdir(parents=True);db=cache/'catalog.sqlite'
 n.update(ROOT=root,A=audit)
 private_path=audit/'source_record_private.txt'
 base_catalog=[{'id':10400145,'present':True,'holds':[],'statement_hash':n['STATEMENT'],'review_hash':n['REVIEW']}]
 blobs={};constant_names=['PRIVATE','PRIOR_REPORT_SHA','REVIEW','STATEMENT'];constants={k:n[k] for k in constant_names}
 def rebuild(payload=problem,report=prior):
  if db.exists():db.unlink()
  with sqlite3.connect(db) as c:
   c.execute('CREATE TABLE records (key TEXT,payload TEXT,report TEXT)');c.execute('INSERT INTO records VALUES(?,?,?)',(n['KEY'],json.dumps(payload),json.dumps(report)))
 def reset():
  n.update(constants);private_path.write_bytes(private);blobs.clear();blobs[n['CATALOG']]=encode(base_catalog);blobs[n['RELATED']]=encode({'groups':[]});rebuild()
 n['blob']=lambda ref,path:blobs[path]
 def observe(name,positive=False):
  before=sha(db.read_bytes());contents=sorted(p.name for p in cache.iterdir())
  try:result=n['source_gate']('SYNTHETIC_IMMUTABLE_PARENT')
  except (RuntimeError,ValueError,TypeError,KeyError,sqlite3.Error) as error:
   need(not positive,'positive source gate rejected: '+str(error));events.append({'test':name,'status':'REJECTED_EXPECTED','guard':str(error)})
  else:
   need(positive,'adverse source guard accepted: '+name)
   need(result['prior_research_sha256']==constants['PRIOR_REPORT_SHA'] and result['raw_prior_report_matched_frozen_report'] is True,'positive report identity not recorded')
   events.append({'test':name,'status':'PASS','private_sha256':result['private_record_sha256'],'prior_research_sha256':result['prior_research_sha256'],'review_hash':result['review_hash']})
  need(before==sha(db.read_bytes()) and contents==sorted(p.name for p in cache.iterdir()),'source gate mutated SQLite/cache')
 reset();observe('actual_nonempty_frozen_prior_matches_raw_SQLite_and_review',True)
 reset();modified=copy.deepcopy(prior);modified['work_done']={'inert_alteration':1};rebuild(report=modified);observe('altered_raw_prior_report_rejected')
 reset();rebuild(report={});observe('empty_raw_prior_report_rejected')
 reset();rebuild(report=None);observe('null_raw_prior_report_rejected')
 reset();modified=copy.deepcopy(problem);modified['statement']=problem['statement']+' INERT MUTATION';rebuild(payload=modified);observe('altered_raw_nested_statement_rejected')
 reset();modified=copy.deepcopy(original);modified['prior_research']['work_done']={'inert_alteration':2};private_path.write_bytes(encode(modified));observe('altered_private_prior_without_repin_rejected')
 reset();modified=copy.deepcopy(original);modified['prior_research']['work_done']={'inert_alteration':3};private_path.write_bytes(encode(modified));n['PRIVATE']=sha(private_path.read_bytes());observe('repinned_private_report_still_rejects_canonical_prior_sha')
 reset();modified=copy.deepcopy(original);modified['problem']['statement']+=' INERT MUTATION';private_path.write_bytes(encode(modified));n['PRIVATE']=sha(private_path.read_bytes());observe('repinned_private_statement_still_rejects_statement_sha')
 reset();modified=copy.deepcopy(original);modified['review_hash']='e'*64;private_path.write_bytes(encode(modified));n['PRIVATE']=sha(private_path.read_bytes());observe('repinned_private_review_field_rejects_expected_review')
 reset();modified=copy.deepcopy(original);modified['review_hash']='e'*64;private_path.write_bytes(encode(modified));n['PRIVATE']=sha(private_path.read_bytes());n['REVIEW']='e'*64;observe('synthetic_repin_isolates_recomputed_review_hash_guard')
 reset();modified=copy.deepcopy(base_catalog);modified[0]['holds']=['INERT_HOLD'];blobs[n['CATALOG']]=encode(modified);observe('current_catalog_hold_rejected')
 reset();modified=copy.deepcopy(base_catalog);modified[0]['present']=False;blobs[n['CATALOG']]=encode(modified);observe('current_catalog_absence_rejected')
 reset();modified=copy.deepcopy(base_catalog);modified[0]['review_hash']='e'*64;blobs[n['CATALOG']]=encode(modified);observe('current_catalog_review_hash_rejected')
 reset();modified=copy.deepcopy(base_catalog);modified[0]['statement_hash']='e'*64;blobs[n['CATALOG']]=encode(modified);observe('current_catalog_statement_hash_rejected')
 reset();blobs[n['RELATED']]=encode({'groups':[{'ids':[n['KEY']],'inert':'membership'}]});observe('new_related_target_membership_rejected')
 reset()
 with sqlite3.connect(db) as c:c.execute('INSERT INTO records SELECT * FROM records')
 observe('duplicate_SQLite_target_rejected')
 reset()
 with sqlite3.connect(db) as c:c.execute('DELETE FROM records')
 observe('missing_SQLite_target_rejected')
 reset();observe('actual_nonempty_report_rechecked_after_all_adverse_controls',True)
print(json.dumps({'schema':'pr952-source-gate-repair-inert-controls-v1','status':'PASS_REAL_FUNCTION_INERT_SQLITE_CONTROLS','outer_optimization':sys.flags.optimize,'installed_actual_source_executed':a.installed,'core_sha256':a.core_sha256,'events':events,'event_count':len(events),'SQLite_bytes_unchanged_by_gate':True,'private_fixture_bodies_retained':False,'test_only_repins_do_not_change_production_source':True,'real_Git_calls':0,'real_service_calls':0,'acceptance_authority':False,'full_review_credit':False},sort_keys=True))
