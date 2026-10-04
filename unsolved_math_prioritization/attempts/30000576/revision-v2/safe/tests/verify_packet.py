#!/usr/bin/env python3
"""Safe packet binding and optional unchanged-history check; not a proof assistant."""
import argparse
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
a=argparse.ArgumentParser()
a.add_argument('--history-root',type=Path)
args=a.parse_args()
passed=[]
def check(name,yes):
    assert yes,name
    passed.append(name)
def read(name):return json.loads((ROOT/name).read_text())
def verify(path,record):
    b=path.read_bytes()
    return len(b)==record['bytes'] and hashlib.sha256(b).hexdigest()==record['sha256']
t=read('TARGET.json')
check('correct_target_revision',(t['id'],t['revision'])==(30000576,2))
check('all_positive_time_parts',t['questions']==['all positive time maps chaotic?','some positive time map chaotic?'])
check('both_fields_covered',len(t['field_gap_handled_by_exhaustive_cases'])==2)
check('source_access_limit_retained',not t['full_2009_proof_inspected'] and not t['original_field_directly_confirmed'])
check('complete_bridge_pending_review',t['bridge_complete_candidate'] and t['independent_review_required'])
check('no_false_novelty',not t['new_counterexample_claimed'] and not t['novelty_claimed'])
check('honest_approach_count',t['substantive_approaches_completed']==1 and t['unused_approaches']==4)
proof=(ROOT/'PROOF.md').read_text()
check('bridge_stages_present',all(x in proof for x in [
    'Dense synchronized periodic tuples','Transitivity of finite diagonal powers',
    'From transitivity to a dense orbit','Complex Banach structure and strong continuity',
    'Nonchaotic positive-time maps remain nonchaotic','If X={0}']))
r=read('EXACT_TEST_RESULTS.json')
check('finite_tests_labeled',r['status']=='pass' and r['finite_controls_only'] and not r['hypercyclicity_numerically_tested'])
s=read('SOURCE_MANIFEST.json')
k=next(x for x in s['sources'] if x['id']=='KALMES2006')
check('new_primary_source_bound',k['pdf']['bytes']==625711 and len(k['pdf']['sha256'])==64)
h=read('HISTORY_BINDING.json')
check('original_freeze_preserved',h['original_freeze_sha256']=='23236036135d52baef409a058a8df2cea2792c6faefd5004b669c14abdfa454d')
if args.history_root:
    check('historical_file_bytes_unchanged',all(verify(args.history_root/x['historical_packet']/x['path'],x) for x in h['files']))
f=read('FREEZE_MANIFEST.json')
listed={x['path']:x for x in f['files']}
actual={x.relative_to(ROOT).as_posix() for x in ROOT.rglob('*') if x.is_file() and x.name!='FREEZE_MANIFEST.json'}
check('exact_safe_allowlist',set(listed)==actual)
check('safe_hashes_match',all(verify(ROOT/n,x) for n,x in listed.items()))
check('sources_excluded',all(not n.endswith(('.pdf','.png','.html','.zip')) and Path(n).name not in ['problems.json','research_results.json'] for n in actual))
print(json.dumps({'status':'pass','checks':passed,'mathematical_proof_machine_verified':False,
                  'fresh_independent_review_performed':False},indent=2))
