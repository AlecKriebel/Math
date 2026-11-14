"""Read-only original/early/final custody and retained-results verification.

No source or arithmetic program is executed; stdout is the only output.
"""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from fractions import Fraction as Q
import datetime,hashlib,json
O=Path(__file__).resolve().parent
checks={}
def load(p):return json.loads(Path(p).read_text())
def binding(p):
 b=Path(p).read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def same(row):return binding(row['path'])=={k:row[k] for k in ('bytes','sha256')}
def need(x,name):
 checks[name]=bool(x)
 if not x:raise RuntimeError('analytic read-only verification:'+name)
initial=load(O/'INITIAL_MANIFEST.json');early=load(O/'INITIAL_SEAL.json')
need(binding(O/'INITIAL_MANIFEST.json')['sha256']==early['manifest_sha256'] and binding(O/'INITIAL_LEDGER.md')['sha256']==early['initial_ledger_sha256'],'initial_seal_identity')
need(all(same(r) for r in initial['files']) and early['no_foreign_primary_code_inventory_or_opinions_read'] is True,'all_initial_objects_immutable')
need(binding(O/'INITIAL_SEAL.json')['sha256']=='c2610abb2fd753ca0e6d86a20626593fb554d5b9d2b49d0ee9b5671d55585b89','fixed_independence_seal')
protected=load(O/'PROTECTED_BINDINGS.json')
need(len(protected['files'])==914 and protected['source_originals']==153 and protected['prior_stage_owned_files']==761 and all(same(r) for r in protected['files']),'all914_original_and_prior_stage_bindings')
custody=load(O/'PRIMARY_CUSTODY.json')
need(all(same(r['identity']) for r in custody['actual_read_primary_bodies']),'actual_primary_body_bytes_in_place')
need(all(same(r) for r in custody['whole_original_native_provider_receipts_bound_in_place']),'whole_provider_receipts_unchanged')
need(custody['Morpurgo2002_web_only']['actual_downloaded_PDF'] is False and custody['Morpurgo2002_web_only']['raw_body_byte_hash'] is None and custody['foreign_fulltext_copied_into_analytic_public_payload'] is False,'honest_primary_access_limits')
summary=load(O/'CHECKS_SUMMARY.json');need(summary['status']=='PASS' and summary['actual_runs']==len(summary['runs'])==4,'four_actual_arithmetic_runs')
for name in ('deposited-arithmetic','independent-arithmetic'):
 outputs=[]
 for mode in ('normal','optimized'):
  stem=O/(name+'-'+mode);e=load(stem.with_suffix('.execution.json'));r=load(stem.with_suffix('.stdout'));outputs.append(r)
  need(e['verified'] is True and e['exit_code']==0 and e['stderr_bytes']==0 and not stem.with_suffix('.stderr').read_bytes(),'actual_run:'+name+':'+mode)
  need(binding(e['command'][-1])=={'bytes':e['script_bytes'],'sha256':e['script_sha256']},'executed_code_identity:'+name+':'+mode)
  need(('-O' in e['command'])==(mode=='optimized'),'actual_mode:'+name+':'+mode)
  need(r.get('accepted') is True if name=='deposited-arithmetic' else r.get('status')=='PASS','actual_success:'+name+':'+mode)
 need(outputs[0]==outputs[1],'mode_result_equality:'+name)
own=load(O/'independent-arithmetic-normal.stdout');source=load(O/'deposited-arithmetic-normal.stdout')
need(own['independent_checks']==len(own['check_names'])==23 and all(own['controls'].values()),'independent23_checks_and_controls')
need(Q(own['cylinder_lower'])==Q(source['cylinder_lower_exact'])==Q(1106714561,1700054750) and Q(own['cylinder_margin'])==Q(3357947,3400109500)>0,'exact_displayed_lower_and_margin')
need(Q(own['small_time_upper'])<Q(629002,10**6) and len(own['middle_intervals'])==6 and all(Q(r['independent_bound'])<Q(r['printed_upper'])<Q(321,500) for r in own['middle_intervals']),'all_printed_table_ceilings')
need([Q(r['a']) for r in own['middle_intervals']]==[Q(k,10) for k in range(14,20)] and [Q(r['b']) for r in own['middle_intervals']]==[Q(k,10) for k in range(15,21)],'complete_middle_interval_coverage')
archive=load(O/'RECURSIVE_CUSTODY.json')
need(archive['status']=='PASS' and archive['regular_occurrences']==142 and archive['containers']==4 and archive['expanded_bytes_all_depths']==928042 and archive['all_CRC_hash_and_existing_bytes_equal'] is True,'retained_complete_recursive_custody')
verdict=load(O/'VERDICT.json')
need(verdict['record_id']==23383952 and verdict['role']=='analytic' and verdict['assessment']=='FULL_ORIGINAL_FINITE_THEOREM_AND_ATTAINMENT_SUPPORTED' and verdict['unresolved_central_analytic_gap'] is None and verdict['promotion_authority'] is False and verdict['follow_up'] is None,'custom_scientific_limits')
if '--preseal' not in sys.argv:
 m=load(O/'MANIFEST.json');s=load(O/'SEAL.json');actual={str(p.relative_to(O)) for p in O.rglob('*') if p.is_file()}-{'MANIFEST.json','SEAL.json'}
 need(actual=={r['relative_path'] for r in m['files']} and len(actual)==m['payload_files'],'complete_own_payload_set')
 need(all(binding(O/r['relative_path'])=={k:r[k] for k in ('bytes','sha256')} for r in m['files']),'all_own_payload_hashes')
 need(s['manifest']==binding(O/'MANIFEST.json') and s['source_repair'] is False and s['promotion_authority'] is False,'final_seal_and_authority_limits')
print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','checks':len(checks),'preseal':'--preseal' in sys.argv,'protected_originals':914,'complete_original_claim_supported':True,'arithmetic_programs_reexecuted':False,'source_programs_executed':False,'writes':0},indent=2))
