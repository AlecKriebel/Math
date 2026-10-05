#!/usr/bin/env python3
"""Authenticate and freeze this family's own outputs, without shared writes."""
import datetime,hashlib,json,lzma,os,pathlib,sys
R=pathlib.Path(__file__).resolve().parent
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
 p=pathlib.Path(p);b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'mode_observed_before_freeze':oct(p.stat().st_mode&0o777),'sealed_mode':'0o444' if p.is_relative_to(R) else oct(p.stat().st_mode&0o777)}
def authenticate(p):
 path=pathlib.Path(p['path'])
 if path.is_file():b=path.read_bytes()
 else:b=lzma.decompress(pathlib.Path(str(path)+'.xz').read_bytes())
 assert len(b)==p['bytes'] and hashlib.sha256(b).hexdigest()==p['sha256'],path
inputs=json.loads((R/'INPUT_INVENTORY.json').read_text())
for p in inputs['external_inputs']:authenticate(p)
native=[]
for p in sorted((R/'process_evidence').glob('*/execution.json')):
 if p.parent.name=='final_close':continue
 e=json.loads(p.read_text());assert e['cwd']==str(R) and isinstance(e['actual_pid'],int) and e['actual_pid']>0
 assert e['started_utc']<=e['ended_utc']
 for key in ['recorder_source','executed_recorder','executable','stdout.bin','stderr.bin']:authenticate(e[key])
 for item in e.get('argument_file_pins',[]):authenticate(item)
 native.append({'execution':pin(p),'actual_pid':e['actual_pid'],'exit_code':e['exit_code'],'label':e['label']})
c=json.loads((R/'CONTROL_RESULTS.json').read_text())
assert c['assertions']==49 and c['actual_self_pid']==38376 and c['optimized']==0 and len(c['loaded_modules'])==612
for p in c['loaded_modules']:authenticate(p)
comp=json.loads((R/'SOURCE_COMPACTION.json').read_text());rest=json.loads((R/'RESTORED_DERIVATIVE_ARCHIVES.json').read_text())
for item in comp['pdf_archives']+rest['restored_derivative_archives']:authenticate(item['original']);authenticate(item['archive'])
assert len(rest['restored_derivative_archives'])==55
v=json.loads((R/'VERDICT.json').read_text())
assert v['covering_historically_earlier_publication_found'] is False and v['new_reduction_alone_is_historical_blocker'] is False and v['publication_or_merge_clearance'] is False
assert (R/'CRITERIA.md').stat().st_mode&0o777==0o444
log=R/'RESEARCH_LOG.md'
with log.open('a') as f:f.write('\n- '+now()+': Native final closure actualPID'+str(os.getpid())+' authenticated external immutable input bodies, complete historical native streams/source/executable/argument pins,612 control module pins,19 byte-lossless whole-PDF archives and55 exact retained PNG archives. Scientific family work100%; bounded historical gaps and independent-check-pending label preserved. Final output inventory and0444/0555 freeze follow in this same source.\n')
core=['REPORT.md','VERDICT.json','CRITERIA.md','TIKHONOV_EXISTENCE_REDUCTION.md','INITIAL_INDEPENDENT_MECHANISM_ASSESSMENT.md','MECHANISM_REDUCTION_AUDIT.md','INPUT_INVENTORY.json','NATIVE_CUSTODY.json','RESEARCH_LOG.md','SOURCE_COMPACTION.json','RESTORED_DERIVATIVE_ARCHIVES.json','CONTROL_RESULTS.json']
closure={'status':'PASS_NATIVE_CUSTODY_AND_BOUNDED_MECHANISM_AUDIT_CLOSURE','actual_child_pid':os.getpid(),'argv':sys.argv,'cwd':os.getcwd(),'utc':now(),'source':pin(pathlib.Path(__file__)),'python':sys.version,'actual_executable':pin(pathlib.Path(sys.executable).resolve()),'core_payload':[pin(R/p) for p in core],'native_prior_run_count':len(native),'native_prior_runs':native,'historical_genuine_failures':[x for x in native if x['exit_code']!=0],'exact_checks':49,'control_module_pins_authenticated':612,'all_external_input_bodies_authenticated':True,'all_native_prior_source_and_stream_bodies_authenticated':True,'all_original_pdf_and_png_archive_bodies_authenticated':True,'pdf_archives':len(comp['pdf_archives']),'restored_png_archives':55,'criteria_already_frozen':True,'storage_target_note':'ROOT expressly preferred retaining all exact historical bodies to strict35MB operational target.','freeze_semantics':'Own files0444/directories0555; historical native modes retained; external modes not changed. Final process stdout/stderr/execution and output inventory exclude themselves from payload hashes to avoid cycles. Final driver uses already-open streams/metadata FD after freezing and pins completed streams plus output inventory.','historical_novelty_assertion':'No covering earlier spectral-approach theorem located within inspected sources. New classical diffusion reduction is pending separate independent adversarial check, and is not an earlier-publication finding or a historical blocker.'}
(R/'CLOSURE.json').write_text(json.dumps(closure,indent=2)+'\n')
excluded={R/'OUTPUT_INVENTORY.json'}|{R/'process_evidence/final_close'/n for n in ['execution.json','stdout.bin','stderr.bin']}
files=[p for p in sorted(R.rglob('*')) if p.is_file() and p not in excluded]
rows=[pin(p) for p in files]
inventory={'utc':now(),'status':'SEALED_PAYLOAD_INVENTORY','payload':rows,'payload_count':len(rows),'stored_payload_bytes':sum(p['bytes'] for p in rows),'excluded_cycle_boundaries':[str(p) for p in sorted(excluded)],'final_native_envelope':'process_evidence/final_close/execution.json','file_mode':'0o444','directory_mode':'0o555','historical_modes':'mode_observed_before_freeze is genuine observation. sealed_mode specifies the subsequent verified chmod in this same native closing process.'}
(R/'OUTPUT_INVENTORY.json').write_text(json.dumps(inventory,indent=2)+'\n')
for p in R.rglob('*'):
 if p.is_file():p.chmod(0o444)
for p in sorted((p for p in R.rglob('*') if p.is_dir()),key=lambda p:len(p.parts),reverse=True):p.chmod(0o555)
R.chmod(0o555)
assert all(p.stat().st_mode&0o777==0o444 for p in R.rglob('*') if p.is_file())
assert all(p.stat().st_mode&0o777==0o555 for p in R.rglob('*') if p.is_dir()) and R.stat().st_mode&0o777==0o555
print(json.dumps({'status':closure['status'],'actual_child_pid':os.getpid(),'payload_count':len(rows),'stored_payload_bytes':inventory['stored_payload_bytes'],'native_prior_run_count':len(native),'all_original_archive_bodies_authenticated':True,'all_files0444_dirs0555':True,'core_pins':{p:pin(R/p)['sha256'] for p in ['REPORT.md','VERDICT.json','INPUT_INVENTORY.json','OUTPUT_INVENTORY.json','TIKHONOV_EXISTENCE_REDUCTION.md','CLOSURE.json']}}))
