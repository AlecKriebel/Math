#!/usr/bin/env python3
import datetime, hashlib, json, os, pathlib, sys
R=pathlib.Path(__file__).resolve().parent
A=R.parent; T=A/'snapshot/unsolved_math_prioritization/attempts/30003508'
def pin(p):
 p=pathlib.Path(p); b=p.read_bytes()
 return {'path':str(p.absolute()),'resolved_path':str(p.resolve()),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'observed_mode':oct(p.stat().st_mode&0o777)}
def matches(p):
 n=pin(p['path']); assert n['sha256']==p['sha256'] and n['bytes']==p['bytes'],p['path']; return n
inputs=[T/'TURN_1.md',T/'TURN_2.md',T/'SOURCE_GATE.md',T/'review/PRIOR_SOURCE_COMPARISON.md',A/'ROOT_MATHEMATICAL_GATE_ACCEPTANCE.json',A/'snapshot_manifest.json',A/'math_scope_adversary_01/OWR_2017_24.pdf',A/'math_scope_adversary_01/OWR_2017_24.fulltext.txt',A/'math_scope_adversary_01/reiss_contribution_1507_1509.txt']
gate=json.loads((A/'ROOT_MATHEMATICAL_GATE_ACCEPTANCE.json').read_text())
assert gate['status']=='PASS_ROOT_PR302_PRECISE_MATHEMATICAL_GATE'
assert gate['original_head']=='eb6e0e999521d84a65f9857d338cad76b84d30db'
inventory={'captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'capture_semantics':'Current body/mode pins at inventory preparation, not invented initial-read-time pins. Original input bodies are immutable snapshot/source reuse; criteria were frozen before substantive priority assessment.','actual_inventory_pid':os.getpid(),'argv':sys.argv,'cwd':os.getcwd(),'original_head':gate['original_head'],'mathematical_gate_is_not_novelty':True,'external_inputs':[pin(p) for p in inputs]}
(R/'INPUT_INVENTORY.json').write_text(json.dumps(inventory,indent=2)+'\n')
receipts=[]; bound=[]; failures=[]
for p in sorted((R/'process_evidence').glob('*/execution.json')):
 e=json.loads(p.read_text()); actual=e['actual_pid']; assert isinstance(actual,int) and actual>0
 assert e['cwd']==str(R) and e['started_utc']<=e['ended_utc']
 for k in ['recorder_source','executed_recorder','executable','stdout.bin','stderr.bin']:
  matches(e[k])
 assert e['recorder_source']['sha256']==e['executed_recorder']['sha256']
 for ap in e.get('argument_file_pins',[]): matches(ap)
 row={'execution':pin(p),'label':e['label'],'actual_pid':actual,'recorder_pid':e['recorder_pid'],'argv':e['argv'],'cwd':e['cwd'],'started_utc':e['started_utc'],'ended_utc':e['ended_utc'],'exit_code':e['exit_code'],'source_at_launch':e['executed_recorder'],'executable_at_launch':e['executable'],'streams_at_completion':[e['stdout.bin'],e['stderr.bin']],'argument_file_pins':e.get('argument_file_pins',[])}
 receipts.append(row)
 if e['exit_code']!=0: failures.append({'label':e['label'],'actual_pid':actual,'exit_code':e['exit_code'],'full_streams':[e['stdout.bin']['path'],e['stderr.bin']['path']]})
 av=e['argv']; paths=[]
 if '--output' in av:
  paths.append(R/av[av.index('--output')+1])
 if pathlib.Path(av[0]).name=='pdftotext': paths.append(R/av[-1])
 if pathlib.Path(av[0]).name=='tesseract': paths.append(R/(av[2]+'.txt'))
 for q in paths:
  if q.is_file(): bound.append({'producer':e['label'],'actual_pid':actual,'producer_exit_code':e['exit_code'],'output':pin(q),'format_is_not_implied_by_filename':True})
controls=json.loads((R/'CONTROL_RESULTS.json').read_text())
assert controls['assertions']==49 and controls['optimized']==0
ce=[r for r in receipts if r['label']=='exact_priority_controls']; assert len(ce)==1
assert ce[0]['actual_pid']==controls['actual_self_pid'] and ce[0]['exit_code']==0
for mp in controls['loaded_modules']: matches(mp)
sources=[]
for p in sorted((R/'private_sources').iterdir()):
 if p.is_file():
  row=pin(p); row['final_mode']='0o444'; row['private_third_party_material']=True
  if p.suffix=='.pdf': row['pdf_magic']=p.read_bytes()[:5]==b'%PDF-'
  sources.append(row)
q=R/'private_sources/luce1999_attempt.pdf'; assert q.is_file() and q.read_bytes()[:5]!=b'%PDF-'
custody={'captured_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'native_receipts':receipts,'genuine_failures':failures,'artifact_producer_bindings':bound,'private_source_pins':sources,'control_summary':{k:controls[k] for k in ['started_utc','ended_utc','actual_self_pid','argv','cwd','optimized','python','executable','sympy','assertions','status']},'loaded_module_count':len(controls['loaded_modules']),'all_control_loaded_module_bodies_authenticated_now':True,'web_evidence_semantics':'WEB_SEARCH_01 through19 are retained tool response bodies. Their reference handles and crawler dates are not process IDs or our audit dates. Search interval is2026-10-05 UTC. No operating-system PID is fabricated for the web tool.','mode_semantics':'Recorder source/output/executable modes in receipts describe launch/completion history. All files in this family are later frozen0444 and directories0555; historical0644 is not rewritten. External runtime binaries are read-only pins and their modes are not changed.','failed_read_semantics':'Tool-only failed sed read of private_sources/none and premature ls checking an undownloaded Linz file are retained in tool history; no native PID/capture invented. Luce download exits0 but is HTML; extraction exits1. Linz native download times out28; no PDF source success claimed.'}
(R/'NATIVE_CUSTODY.json').write_text(json.dumps(custody,indent=2)+'\n')
payload=[p for p in R.rglob('*') if p.is_file()]
total=sum(p.stat().st_size for p in payload)
assert total<=35*1024*1024, total
print(json.dumps({'native_runs_authenticated':len(receipts),'native_failures':failures,'private_files':len(sources),'logical_payload_bytes_before_final_reports':total,'control_assertions':controls['assertions'],'control_loaded_module_count':len(controls['loaded_modules']),'broad_prior_application_status':'independent classical reduction; not located historical diffusion application','criteria':pin(R/'CRITERIA.md')}))
