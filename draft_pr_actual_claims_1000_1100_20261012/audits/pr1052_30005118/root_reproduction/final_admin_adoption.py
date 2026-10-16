from pathlib import Path
import ast,hashlib,io,json,shutil,stat,subprocess,sys,zipfile
from datetime import datetime,timezone
A=Path(__file__).resolve().parents[1];P=A/'preprint_v1_0';F=A/'finalization/terminal_admin_20261014';R=Path(__file__).parent
def require(c,m):
 if not c:raise RuntimeError(m)
def load(p):return json.loads(p.read_text())
def check(base,r,key='path'):
 p=base/r[key];b=p.read_bytes();require(len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],str(p))
def pin(p):
 b=p.read_bytes();return {'path':str(p.relative_to(A)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
changes=load(F/'CHANGE_INVENTORY.json')['changed_existing_files'];changed={r['path']:r for r in changes};require(len(changed)==10,'admin whitelist')
inputs=load(F/'INPUT_PINS.json')['files']
for r in inputs:check(F/'frozen_before' if r['path'] in changed else A,r)
for r in changes:check(A,r['after']);check(F/'frozen_before',r['before'])
outs=load(F/'OUTPUT_PINS.json')
for r in outs['files']:check(F,r)
for r in outs['current_audit_payload_files']:check(A,r)
base=load(F/'FROZEN_BASELINE.json')
for r in base['protected']:check(A,r)
copies=load(P/'support/COPY_MAP.json')['copies'];require(len(copies)==121 and copies[:99]==base['old_99_copy_records'],'old copy dictionary identities')
for r in copies:
 key='source_snapshot' if 'source_snapshot' in r else 'original_path';check(A,r,key);check(P,r,'package_path')
resolutions=load(P/'support/TERMINAL_HISTORICAL_PIN_RESOLUTION.json')['files']
for r in resolutions:check(A,r,'resolved_before_bytes_audit_relative')
omissions=load(P/'support/TERMINAL_SOURCE_EXCLUSION_LEDGER.json')['individual_omitted_sealed_outputs']
for r in omissions:check(A,r,'source_audit_relative');require(r['distribution']=='OMITTED' and bool(r['reason']),'omission')
metadata=load(P/'.zenodo.json');require(metadata==load(P/'metadata.json')['metadata']==load(P/'zenodo-deposit.json')['metadata']==base['metadata_object'],'exact metadata object')
old=load(F/'frozen_before/preprint_v1_0/zenodo-deposit.json');new=load(P/'zenodo-deposit.json');before=json.loads(json.dumps(new));before['files'][1]['bytes']=old['files'][1]['bytes'];before['files'][1]['sha256']=old['files'][1]['sha256'];require(before==old,'descriptor only ZIP hash/size changes')
native=load(A/'publication/zenodo-deposit.json');require(native['metadata']==metadata and native['files']==[{'path':'../preprint_v1_0/paper.pdf','name':'paper.pdf'},{'path':'../preprint_v1_0/pr1052_support_v1_0.zip','name':'pr1052_support_v1_0.zip'}],'actual repository native upload interface')
names=load(P/'SUPPORT_ALLOWLIST.json')['members'];raw=(P/'pr1052_support_v1_0.zip').read_bytes();buf=io.BytesIO()
with zipfile.ZipFile(io.BytesIO(raw)) as z:
 require(z.namelist()==sorted(names) and z.testzip() is None and len(names)==163,'closed names/CRC')
 for i in z.infolist():
  b=z.read(i);require(b==(P/i.filename).read_bytes(),'payload');require(i.date_time==(2026,10,14,0,0,0) and i.create_system==3 and i.external_attr==(0o100644<<16) and i.compress_type==0 and not i.flag_bits&1,'headers')
  if i.filename!='paper.pdf':b.decode('utf-8')
  if i.filename.endswith('.json'):json.loads(b)
  if i.filename.endswith('.py'):ast.parse(b)
with zipfile.ZipFile(buf,'w',compression=zipfile.ZIP_STORED) as z:
 for n in sorted(names):
  i=zipfile.ZipInfo(n,(2026,10,14,0,0,0));i.create_system=3;i.external_attr=(stat.S_IFREG|0o644)<<16;i.compress_type=0;z.writestr(i,(P/n).read_bytes())
require(buf.getvalue()==raw,'independent CLOSED rebuild')
commands=[]
def run(argv,cwd):
 q=subprocess.run(argv,cwd=cwd,text=True,capture_output=True);commands.append({'argv':argv,'cwd':str(cwd),'returncode':q.returncode,'stdout':q.stdout,'stderr':q.stderr});require(q.returncode==0,str(argv)+q.stderr)
s=R/'tmp/final1052';s.mkdir(parents=True,exist_ok=False)
try:
 with zipfile.ZipFile(io.BytesIO(raw)) as z:z.extractall(s)
 for flags in (['-I','-B'],['-I','-B','-O']):
  run([sys.executable,*flags,'verify_support.py'],s)
  run([sys.executable,*flags,'run_checks.py','--output','_runs/fresh.json'],s)
  run([sys.executable,*flags,'test_integrity.py','--output','_runs/integrity.json'],s)
  run([sys.executable,*flags,'build_support.py','--output','_runs/rebuilt.zip'],s);require((s/'_runs/rebuilt.zip').read_bytes()==raw,'actual rebuild')
  run([sys.executable,*flags,'verify_support.py','--archive','_runs/rebuilt.zip'],s)
finally:shutil.rmtree(s)
for r in outs['files']:check(F,r)
for r in outs['current_audit_payload_files']:check(A,r)
state=load(P/'CURRENT_REVIEW_STATE.json');require(all(type(v) is int and v==0 for v in state['actionable_issue_counts'].values()),'actual severity count types')
x={'utc':datetime.now(timezone.utc).isoformat(),'pr':1052,'status':'ROOT_PASS_TERMINAL_ADMINISTRATION','root_full_finalization_report_changed_code_prose_and_stage_semantics_read':True,'immediate_inputs_rehashed':len(inputs),'authorized_admin_changes':10,'unchanged_immediate_files':len(inputs)-10,'terminal_outputs_rehashed':len(outs['files']),'final_audit_payload_files_rehashed':len(outs['current_audit_payload_files']),'old99_copy_records_preserved':True,'source_equal_copies':len(copies),'historical91_plus134_pin_resolutions_checked':len(resolutions),'individual_omissions_checked':len(omissions),'all30_repair_outputs_and_prior_P3_history_unchanged':True,'protected':base['protected'],'metadata_all_three_objects_exact_unchanged':True,'reviewed_hash_binding_descriptor_changed_only_archive_hash_size':True,'native_repository_upload_manifest':pin(A/'publication/zenodo-deposit.json'),'native_local_check':pin(A/'publication/REPOSITORY_TOOL_LOCAL_CHECK.json'),'native_interface_note':pin(A/'publication/REPOSITORY_UPLOAD_INTERFACE.md'),'native_upload_metadata_exact_same_reviewed_object':True,'archive':pin(P/'pr1052_support_v1_0.zip'),'archive_members':len(names),'payloads':len(names)-1,'independent_closed_rebuild_byte_exact':True,'actual_clean_normal_optimized_support_commands_reproduce':True,'commands':commands,'paper_PDF_source_math_checkers_unchanged':True,'new_compile_render_or_marker':False,'fresh_whole_package_reviews':2,'actionable_issues':0,'publication_ready':True,'all_issues_resolved':True,'published':False,'services_hold':'preceding PR1032 priority cursor','dated_internal_pending_fields':'Immutable captured historical administration; this external current root seal supplies final administrative adoption.'}
(A/'FINAL_INTEGRITY.json').write_text(json.dumps(x,indent=2)+'\n');seal={k:v for k,v in x.items() if k!='commands'};seal['status']='ROOT_SEALED_READY_PENDING_PRIOR_PR1032_CURSOR';seal['final_integrity']=pin(A/'FINAL_INTEGRITY.json');seal['terminal_finalization_report']=pin(F/'FINALIZATION_REPORT.md');seal['terminal_output_pins']=pin(F/'OUTPUT_PINS.json');(A/'FINAL_SEAL.json').write_text(json.dumps(seal,indent=2)+'\n');print(json.dumps({'status':seal['status'],'members':len(names),'copies':len(copies),'old_stage_resolutions':len(resolutions),'archive_sha256':seal['archive']['sha256']}))
