from pathlib import Path
import hashlib,json,datetime,os,sys
D=Path.cwd();now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
records=[]
for folder in [D/'processes',D/'independent_old_example_adversary/processes']:
 for p in sorted(folder.glob('*.json')):
  j=json.loads(p.read_text())
  if 'argv' not in j:continue
  for stream in ['stdout','stderr']:
   f=p.with_suffix('.'+stream)
   if not f.exists() or digest(f)!=j[stream+'_sha256'] or f.stat().st_size!=j[stream+'_bytes']:raise RuntimeError('capture mismatch '+str(f))
  records.append({'record':str(p.relative_to(D)),**j})
(D/'PROCESS_INDEX.json').write_text(json.dumps({'UTC':now,'operator_PID':os.getpid(),'actual_execution_records':records,'documentary_copies':'Other source_bytes/processes records are immutable copies rather than duplicate executions; see the adversary source manifest.','calculation_exit_summary':'All five mathematical diagnostic/exact executions exited 0. One initial bookkeeping verifier exited 1, preserved and repaired.'},indent=2)+'\n')
with (D/'RESEARCH_LOG.md').open('a') as f:f.write('\n- '+now+': Bounded higher-rank/lens priority family audit 100% complete. Four exact old-example reconstructions give equal nonzero squared magnitude 1/3 and normalized square 8. 165 integrity checks pass; corrected bibliography and explicit read/access/source-discrepancy gaps retained. Sealed recursive byte/process packet, no first-counterexample or worldwide-novelty/publication clearance.\n')
files=[]
for p in sorted(D.rglob('*')):
 if p.is_file() and p.name not in ['CLOSED_MANIFEST.json','CLOSURE.json']:
  files.append({'path':str(p.relative_to(D)),'bytes':p.stat().st_size,'sha256':digest(p)})
manifest={'schema':'PR95-higher-rank-priority-byte-manifest/v1','UTC':now,'actual_seal_PID':os.getpid(),'actual_parent_PID':os.getppid(),'observed_executable':sys.executable,'script_argv':sys.argv,'requested_launcher_argv':['python3','seal_packet.py'],'root':str(D),'file_count':len(files),'files':files,'exclusions':['CLOSED_MANIFEST.json (hash in CLOSURE.json)','CLOSURE.json (hash reported to parent in final tool output)'],'privacy':'All primary copyrighted source bytes, extracts and renderings remain private local evidence.'}
(D/'CLOSED_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
closure={'schema':'PR95-higher-rank-priority-closure/v1','UTC':now,'actual_seal_PID':os.getpid(),'bounded_family_complete_percent':100,'new_central_proof_search_turns':0,'budget':'2/5 original author budget retained','old_example':{'group':'ordinary SU(4)','WZW_level':2,'shifted_level':6,'manifolds':['L(64,9)','L(64,25)'],'tau':'-exp(5 pi i/12)/sqrt(3)','both_squared_magnitudes':'1/3','both_S3_normalized_squares':8,'nonzero':True,'conditional_scope':'Printed HT full-category definitions and formulas; conflicting printed complex separation is explicitly unresolved.'},'priority_verdict':'No earlier qualifying explicit full magnitude counterexample located in examined primary scope. First-counterexample and worldwide novelty unestablished; no publication clearance.','manifest_sha256':digest(D/'CLOSED_MANIFEST.json'),'report_sha256':digest(D/'REPORT.md'),'source_ledger_sha256':digest(D/'SOURCE_LEDGER.json'),'search_scope_sha256':digest(D/'SEARCH_SCOPE.json'),'process_index_sha256':digest(D/'PROCESS_INDEX.json'),'integrity_check_sha256':digest(D/'INTEGRITY_CHECK.json'),'file_count':len(files),'execution_record_count':len(records),'all_manifest_entries_self_verified':all((D/r['path']).stat().st_size==r['bytes'] and digest(D/r['path'])==r['sha256'] for r in files),'remaining_gap':'HT source discrepancy and inaccessible final/errata; Takata1996; unlocated HT Gauss follow-up; reliable full Zhang–Carey; unread sections and later versions; literature beyond bounded search.'}
(D/'CLOSURE.json').write_text(json.dumps(closure,indent=2)+'\n')
print(json.dumps({**closure,'closure_sha256':digest(D/'CLOSURE.json')},indent=2))
