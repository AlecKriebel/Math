#!/usr/bin/env python3
"""Pure, inert positive/negative controls for PR observation predicates."""
import sys
if not(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):raise SystemExit('use -I -S -B')
import copy,hashlib,json,types
from pathlib import Path
HERE=Path(__file__).absolute().parent
# Caller authenticates these bytes before running; CLI supplies an external seal.
if len(sys.argv)!=2:raise SystemExit('external observation_checks.py SHA256 required')
raw=(HERE/'observation_checks.py').read_bytes()
if hashlib.sha256(raw).hexdigest()!=sys.argv[1]:raise SystemExit('external observation source seal differs')
v=types.ModuleType('checks');exec(compile(raw,'observation_checks.py','exec',optimize=0),v.__dict__)
events=[]
def need(ok,message):
    if not ok:raise RuntimeError(message)
def reject(name,call):
    try:call()
    except v.Reject as e:events.append({'test':name,'status':'REJECTED','message':str(e)})
    else:raise RuntimeError('accepted '+name)
def node(**kw):
    n={'number':952,'state':'OPEN','isDraft':True,'headRefOid':v.HEAD,'headRefName':'candidate','baseRefName':'main','baseRefOid':'1'*40,'url':'https://github.com/AlecKriebel/Math/pull/952','title':'test','body':'test','mergeable':'MERGEABLE','mergeStateStatus':'CLEAN','baseRef':{'name':'main','target':{'oid':'2'*40}},'currentBaseRefOid':'2'*40}
    n.update(kw);return n
before=node();after=node(mergeStateStatus='UNKNOWN',mergeable='UNKNOWN')
b=v.bracket(before,after);need(b['authority_equal'] and set(b['all_observation_differences'])=={'mergeable','mergeStateStatus'},'computed observations classification');events.append({'test':'computed_change_preserved_without_false_identity_drift','status':'PASS'})
reject('unknown_cannot_merge',lambda:v.require_fresh_mergeable(after));v.require_fresh_mergeable(before)
drift=node(headRefOid='3'*40);reject('head_change',lambda:v.bracket(before,drift))
merged=node(state='MERGED',mergeCommit={'oid':'4'*40},mergedAt='2026-10-16T20:00:00Z')
advanced=copy.deepcopy(merged);advanced.update(mergeable='UNKNOWN',mergeStateStatus='UNKNOWN',currentBaseRefOid='5'*40);advanced['baseRef']['target']['oid']='5'*40
need(v.bracket(merged,advanced,True)['authority_equal'],'advancing main is not merged PR drift');events.append({'test':'merged_PR_identity_survives_unrelated_main_advance','status':'PASS'})
page=copy.deepcopy(before);page.update(changedFiles=2,files={'nodes':[{'path':'unsolved_math_prioritization/QUEUE.md'},{'path':'unsolved_math_prioritization/attempts/10400145/README.md'}],'pageInfo':{'hasNextPage':False,'endCursor':'last'}})
r=v.complete_paths([page],before,before);need(r['live_base_oid']=='2'*40 and v.next_target_identity(r)=='10400145','actual live base vs associated baseRefOid');events.append({'test':'actual_live_base_and_complete_target_positive','status':'PASS'})
missing=copy.deepcopy(before);missing.pop('baseRef');reject('associated_baseRefOid_cannot_replace_actual_pointer',lambda:v.complete_paths([page],missing,missing))
reject('live_main_advances_during_gate',lambda:v.complete_paths([page],before,advanced))
for label,edit in [('wrong_count',lambda p:p.update(changedFiles=3)),('duplicate',lambda p:p['files']['nodes'].append(p['files']['nodes'][0])),('incomplete',lambda p:p['files']['pageInfo'].update(hasNextPage=True)),('body_not_path',lambda p:p['files']['nodes'][0].update(body='excluded mathematics')),('noncanonical_path',lambda p:p['files']['nodes'][0].update(path='a/../b'))]:
    p=copy.deepcopy(page);edit(p);reject(label,lambda p=p:v.complete_paths([p],before,before))
p1=copy.deepcopy(page);p1['files']={'nodes':[page['files']['nodes'][0]],'pageInfo':{'hasNextPage':True,'endCursor':'first'}}
p2=copy.deepcopy(page);p2['files']={'nodes':[page['files']['nodes'][1]],'pageInfo':{'hasNextPage':False,'endCursor':'last'}}
need(len(v.complete_paths([p1,p2],before,before)['paths'])==2,'two page positive');events.append({'test':'complete_two_pages_positive','status':'PASS'})
empty=v.native_absence({},[]);need(empty['historical_native_turn_count']=='UNKNOWN' and empty['historical_native_count_authenticated'] is False,'native unknown');events.append({'test':'current_absence_does_not_authenticate_historical_zero','status':'PASS'})
reject('native_target_entry',lambda:v.native_absence({'10400145':{}},[]));reject('native_target_history',lambda:v.native_absence({},[{'id':10400145}]))
print(json.dumps({'schema':'pr952-offline-observation-tests-v1','status':'PASS_INERT_CONTROLS','tests':events,'real_service_mutations':0,'complete_acceptance_authority':False},sort_keys=True))
