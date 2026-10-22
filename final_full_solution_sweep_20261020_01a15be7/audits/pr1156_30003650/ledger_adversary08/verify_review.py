#!/usr/bin/env python3
"""Strict closed evidence verification; no project/helper import or service call."""
import hashlib,json,re
from pathlib import Path
HERE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def require(v,m):
 if not v:raise RuntimeError(m)
def verify_entries(entries,root):
 names=[]
 for e in entries:
  require(set(e)=={'path','bytes','sha256'},'Invalid entry schema')
  name=e['path'];p=root/name
  require(not Path(name).is_absolute() and '..' not in Path(name).parts,'Unsafe relative path')
  require(not p.is_symlink() and p.is_file() and p.resolve().is_relative_to(root.resolve()),'Unsafe bound file')
  b=p.read_bytes();require(len(b)==e['bytes'] and sha(b)==e['sha256'],'Bound bytes differ: '+name);names.append(name)
 require(len(set(names))==len(names),'Duplicate path')
 return set(names)
def verify_instance(name):
 p=HERE/(name+'.json');b=p.read_bytes();require((HERE/(name+'.sha256')).read_text().split()[0]==sha(b),'Instance seal differs');m=json.loads(b);verify_entries(m['files'],HERE)
 for e in m.get('input_pins',[])+m.get('fresh_capture_inputs',[]):
  a=Path(e['original']).read_bytes();c=(HERE/e['snapshot']).read_bytes();require(len(a)==e['bytes'] and sha(a)==e['sha256'] and a==c,'Instance input mismatch')
 return m

def main():
 b=(HERE/'MANIFEST.json').read_bytes();require((HERE/'MANIFEST.sha256').read_text().split()[0]==sha(b),'Manifest seal mismatch');m=json.loads(b);listed=verify_entries(m['files'],HERE)
 actual={str(p.relative_to(HERE)) for p in HERE.rglob('*') if p.is_file() and not({'private','__pycache__'}&set(p.relative_to(HERE).parts)) and p.name not in {'MANIFEST.json','MANIFEST.sha256'}}
 require(listed==actual,'Public manifest not closed')
 pm=json.loads((HERE/'PRIVATE_SNAPSHOT_MANIFEST.json').read_text());private=verify_entries(pm['files'],HERE)
 require(private=={str(p.relative_to(HERE)) for p in (HERE/'private').rglob('*') if p.is_file()},'Private manifest not closed')
 for e in json.loads((HERE/'SOURCE_PINS.json').read_text())['files']:
  a=Path(e['original']).read_bytes();c=(HERE/e['snapshot']).read_bytes();require(len(a)==e['bytes'] and sha(a)==e['sha256'] and a==c,'Original/source snapshot changed')
 require(sha((HERE.parent/'reconcile_external_ledger_v8.py').read_bytes())=='5ed4576eacf0d23d73db5d73e6cf1461b486b7a1520a90cbd8e650015f6f2c54','Target changed')
 require(not(HERE.parent/'ROOT_LEDGER_REVIEW08_ACCEPTANCE.json').exists(),'Generic v8 acceptance must remain absent')
 verify_instance('ACTUAL_INSTANCE_MANIFEST');verify_instance('FRESH_INSTANCE_MANIFEST')
 a=json.loads((HERE/'ACTUAL_INSTANCE_AUDIT.json').read_text());f=json.loads((HERE/'FRESH_INSTANCE_COMPARISON.json').read_text());literal=json.loads((HERE/'LITERAL10_SUPPLEMENT.json').read_text())
 require(a['account_records']==197 and a['ledger_rows']==181 and a['bare10_occurrences']==5 and a['resolver_occurrences']==1041 and a['native_machine_url_occurrences']==7551 and a['query_occurrences']==201 and a['fragment_occurrences']==13 and a['no_unresolved_identity_leads'] and not a['unresolved'] and not a['semantic_or_target_leads'] and not a['known_payload_md5_leads'],'Exact instance result differs')
 require(f['changed_leaf_count']==152 and len(f['changed_records'])==24 and f['only_exact_eight_nonnegative_integer_stats_counters_changed'] and f['all_other_fields_keysets_types_lists_values_equal'] and f['ledger_rows_identical']==181,'Fresh counter comparison differs')
 require(literal['adds_to_the5_standalone_bare_occurrences']==64 and not literal['unresolved'],'Literal substring supplement differs')
 prior=json.loads((HERE.parent/'ledger_adversary07/RESULTS_NORMAL.json').read_text());modes=[];total=unsafe=conservative=0
 for i,name in enumerate(['RESULTS_NORMAL.json','RESULTS_OPTIMIZED.json','RESULTS_DOCSTRINGS_REMOVED.json']):
  main=json.loads((HERE/name).read_text());q=json.loads((HERE/('QUERY_BOUNDARY_MODE_'+str(i)+'.json')).read_text());s=json.loads((HERE/('SERIALIZATION_MODE_'+str(i)+'.json')).read_text());n=json.loads((HERE/('NEW_BOUNDARY_MODE_'+str(i)+'.json')).read_text());l=json.loads((HERE/('LEDGER_SEMANTIC_MODE_'+str(i)+'.json')).read_text())
  require(len(main['results'])==600 and q['case_count']==50 and s['case_count']==21 and n['case_count']==204 and l['case_count']==40,'Incomplete matrix')
  require([r['case'] for r in main['results']]==[r['case'] for r in prior['results']],'Retained600 controls/order changed')
  retained=main['results']+q['results']+s['results'];require(len(retained)==671 and all(r['passed'] for r in retained),'Retained671 regression failed')
  require(main['originals_unchanged'] and not main['denied_real_service_attempts'] and not any(x['denied_actual_services'] for x in [q,s,n,l]),'Originals changed or real service attempted')
  allr=retained+n['results']+l['results'];bad=[r for r in allr if not r['passed']];u=[r for r in bad if r['error'] is None and r['state']['append']==1 and r['receipt_saved']];c=[r for r in bad if r['error'] is not None and r['state']['append']==0 and r['expected']=='pass']
  require(len(allr)==915 and len(bad)==96 and len(u)==90 and len(c)==6,'Unexpected classification count')
  require(len([r for r in n['results'] if not r['passed'] and r['error'] is None])==70 and len([r for r in l['results'] if not r['passed']])==20,'Fresh finding counts differ')
  require(all(r['error'].startswith('RuntimeError: Unresolved bare short DOI') for r in c),'Conservative halt mechanism changed')
  require(not any(r['unexpected_service_paths'] or r['error'] and '[Errno 28]' in r['error'] for r in allr),'Unexpected path or infrastructure failure')
  p=next(r for r in main['results'] if r['case']=='v7_actual197_native_account_and_actual181_ledger')
  require(p['state']['account_gets']==197 and p['state']['reads']==3 and p['state']['pr_reads']==2 and p['state']['append']==1 and p['simulated_ledger_rows']==182 and p['state']['exclusive_intents']==1 and p['state']['directory_fsync']>=1 and p['state']['file_fsync']>=1,'Native positive incorrect')
  modes.append([(r['case'],r['expected'],r['passed'],r['error'] is None,r['state'],r['receipt_saved'],r['simulated_ledger_rows']) for r in allr]);total+=len(allr);unsafe+=len(u);conservative+=len(c)
 require(modes[0]==modes[1]==modes[2],'Optimization results differ')
 v=json.loads((HERE/'VERDICT.json').read_text());require(v['ready_for_existing_publication_record'] is False and len(v['material_findings'])==3,'Verdict differs')
 summary=json.loads((HERE/'VALIDATION_SUMMARY.json').read_text());require(summary['primary_executions']==total==2745 and summary['unsafe_verified_mock_appends']==unsafe==270 and summary['conservative_halts']==conservative==18,'Summary counts differ')
 print(json.dumps({'closed_manifest_verified':True,'public_files':len(actual),'private_files':len(private),'primary_executions':total,'retained671_regressions':2013,'unsafe_verified_mock_appends':unsafe,'conservative_halts':conservative,'all_modes_agree':True,'actual_service_attempts':0,'preserved_and_fresh_instance_unresolved_identity_leads':0,'generic_v8_readiness':False},indent=2))
if __name__=='__main__':main()
