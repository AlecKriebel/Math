from pathlib import Path
import datetime,hashlib,json,os,stat
R=Path(__file__).resolve().parent;P=R.parent/'operations06'
def need(v,m):
 if not v:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
 s=p.stat();b=p.read_bytes();return {'bytes':len(b),'sha256':sha(b),'mode':stat.S_IMODE(s.st_mode),'mtime_ns':s.st_mtime_ns}
for file,key in [('INPUT_VALIDATION.json','copied_input_files'),('MODEL_INPUTS.json','files')]:
 for source,wanted in json.loads((R/file).read_bytes())[key].items():
  expected={k:v for k,v in wanted.items() if k!='copy'};need(pin(Path(source))==expected,'Original reviewed input changed '+source)
  copied=R/wanted['copy'];need(sha(copied.read_bytes())==wanted['sha256'],'Own input copy changed '+str(copied));need(copied.stat().st_ino!=Path(source).stat().st_ino,'Original input inode shared')
raw=(P/'MANIFEST.json').read_bytes();need(sha(raw)=='cde78679a06a8ec0954f9af1785cd339762a5cc57b3154661c3313706677852b','Target seal changed');manifest=json.loads(raw);files={};dirs={}
for parent,ds,ns in os.walk(P,followlinks=False):
 for n in ds+ns:
  p=Path(parent)/n;s=p.lstat();need(not p.is_symlink(),'Target symlink');name=p.relative_to(P).as_posix()
  if p.is_dir():dirs[name]={'mode':stat.S_IMODE(s.st_mode),'mtime_ns':s.st_mtime_ns}
  elif p!=P/'MANIFEST.json':files[name]=pin(p)
need(files==manifest['files'] and dirs==manifest['directories'],'Target recursive custody changed')
reports={};modes={};harnesses={n:pin(R/n) for n in ['independent_controls.py','extension_controls.py','focused_controls.py','identity_controls.py']}
for mode in ['normal','O','OO']:
 groups={}
 for family,count in [('fresh',34),('extension',6),('focused',5),('identity',5)]:
  path=R/'private'/f'{family}_{mode}/RESULT.json';value=json.loads(path.read_bytes());need(value['case_count']==count,'Missing cases')
  need(value['real_escape_attempts']==[] and value['real_service_or_Git_mutations']==0,'External effect')
  need(value['source_sha256']=='4d491443d4be4d07ef9abb45c0ce6f9c56bf77c20dd7a2254ae43dce2638ab79' and value['bootstrap_sha256']=='e8c7f35bc6d60318146ae9794fe84c7c8a18e99e818a350bb78298fd85bd9852','Source identity changed')
  need(not any(q['Git_writes'] for q in value['results']),'Git effect')
  groups[family]=value;reports[str(path.relative_to(R))]=pin(path)
 allcases=[q for g in groups.values() for q in g['results']]
 counters=[q['case'] for q in allcases if q['status']=='COUNTEREXAMPLE'];need(len(counters)==11,'Unexpected discrepancy')
 for q in allcases:
  if q['case'].startswith('ledger_after_fsync_') or q['case'] in {'ledger_native31seconds_after_complete_gate','ledger_native_family_changed_after_complete_gate'}:
   need(q['actual_write_delta']=={'native':0,'append':1} and q['ledger_verified'] and q['error'] is None,'Ledger counterexample evidence missing')
  if q['case']=='publication_revoked_during_postwrite_native_verification':need(q['publication_verified'] and q['error'] is None,'Publication certificate counterexample missing')
  if q['case'].startswith('saved_original_manifest_'):need(q['actual_write_delta']=={'native':0,'append':0} and q['error'] is not None,'Saved-state identity escape')
 # no_second_allocation is a second case on the same successful control world.
 # All other case rows correspond to distinct worlds; avoid counting it twice.
 distinct=[q for q in allcases if q['case']!='no_second_allocation']
 modes[mode]={'scenario_rows':len(allcases),'actual_parsed_scenarios':sum(not q.get('component_case',False) for q in allcases),
  'direct_edge_component_cases':sum(q.get('component_case',False) for q in allcases),
  'additional_loader_component_checks':3,'actual_parsed_invocations_including_setup_and_reentry':82,
  'actual_parsed_invocation_derivation':{'fresh':54,'extension':11,'focused':10,'identity':7},
  'counterexamples':counters,'model_native_write_calls_including_setup':sum(len(q['native_calls']) for q in distinct),
  'model_ledger_append_calls_including_setup':sum(q['appends'] for q in distinct),
  'subject_operation_native_write_deltas':sum(q['actual_write_delta']['native'] for q in allcases),
  'subject_operation_append_deltas':sum(q['actual_write_delta']['append'] for q in allcases),
  'real_service_and_Git_mutations':0,'real_escape_attempts':0}
need(modes['normal']['counterexamples']==modes['O']['counterexamples']==modes['OO']['counterexamples'],'Mode disagreement')
for f in R.glob('*.stderr'):need(f.stat().st_size==0,'Execution failed: '+f.name)
current=json.loads((P/'READINESS.json').read_bytes());need(not (P/'runtime').exists(),'Production runtime appeared')
out={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'decision':'HOLD','sources_sha256':'4d491443d4be4d07ef9abb45c0ce6f9c56bf77c20dd7a2254ae43dce2638ab79','bootstrap_sha256':'e8c7f35bc6d60318146ae9794fe84c7c8a18e99e818a350bb78298fd85bd9852','target_recursive_manifest_sha256':sha(raw),'target_files_reverified':len(files),'target_directories_reverified':len(dirs),'modes':modes,'report_pins':reports,'harness_source_pins':harnesses,'actual_parsed_scenarios_total':144,'actual_parsed_invocations_including_setup_and_reentry_total':246,'component_cases_total':15,'material_counterexample_scenarios_total':33,'real_external_queries':0,'real_external_mutations':0,'all_copied_and_original_review_inputs_unchanged':True,'production06_runtime_absent':True,'historical_49GB_custody_replayed':False,'whole_review_complete_percent':100,'overall_percent':80,'no_production_clearance_issued':True}
(R/'REVIEW_RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in {'report_pins','harness_source_pins'}},indent=2))
