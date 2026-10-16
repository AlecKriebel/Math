from pathlib import Path
import ast, hashlib, io, json, shutil, stat, subprocess, sys, zipfile
from datetime import datetime, timezone
A=Path(__file__).resolve().parents[1]; P=A/'preprint_v1_0'; F=A/'finalization/terminal_admin_20261014'
def require(c,m):
 if not c: raise RuntimeError(m)
def load(p): return json.loads(p.read_text())
def check(base,r,field='path'):
 p=base/r[field];b=p.read_bytes();require(len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],str(p))
def pin(p):
 b=p.read_bytes();return {'path':str(p.relative_to(A)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
changes=load(F/'CHANGE_INVENTORY.json')['changed_existing_files']; changed={r['path']:r for r in changes}
require(len(changed)==12,'authorized changes')
inputs=load(F/'INPUT_PINS.json')['files']
for r in inputs:check(F/'frozen_before' if r['path'] in changed else A,r)
for r in changes:check(A,r['after']);check(F/'frozen_before',r['before'])
outputs=load(F/'OUTPUT_PINS.json')
for r in outputs['files']:check(F,r)
for r in outputs['final_audit_payload_files']:check(A,r)
baseline=load(F/'FROZEN_BASELINE.json')
for r in baseline['protected']+baseline['root_adoptions']:check(A,r)
for r in baseline['originals']['files']:check(A,r,'snapshot_path')
copies=load(P/'EVIDENCE_COPY_MAP.json')['copies'];old=baseline['existing_evidence_copies']['copies']
require(len(copies)==141 and copies[:97]==old,'old mapping unchanged')
for r in copies:check(A,r,'source_audit_relative');check(P,r,'package_path')
omitted=load(P/'evidence/TERMINAL_SOURCE_EXCLUSION_LEDGER.json')['individual_omitted_sealed_outputs']
for r in omitted:check(A,r,'source_audit_relative');require(bool(r['reason']) and r['distribution']=='OMITTED','honest omission')
require(len(omitted)==23,'individual omissions')
metadata=load(P/'.zenodo.json')
require(load(P/'zenodo_metadata.json')=={'metadata':metadata} and load(P/'zenodo-deposit.json')['metadata']==metadata,'metadata equivalence')
names=sorted(load(P/'ALLOWLIST.json')['members']+['MANIFEST.json']);original=(P/'pr1047_supportkit_v1.0.zip').read_bytes();buf=io.BytesIO()
require(len(names)==204 and 'paper/matroid_rank_obstruction.pdf' not in names and 'zenodo-deposit.json' not in names,'external selection boundary')
with zipfile.ZipFile(io.BytesIO(original)) as z:
 require(z.namelist()==names and z.testzip() is None,'closed member names/CRC')
 for i in z.infolist():
  b=z.read(i);require(b==(P/i.filename).read_bytes(),'member bytes')
  require(i.date_time==(2026,10,14,0,0,0) and i.create_system==3 and i.external_attr==(0o100644<<16) and i.compress_type==0 and not i.flag_bits&1,'ZIP headers')
  b.decode('utf-8')
  if i.filename.endswith('.json'):json.loads(b)
  if i.filename.endswith('.py'):ast.parse(b)
with zipfile.ZipFile(buf,'w',compression=zipfile.ZIP_STORED) as z:
 for n in names:
  i=zipfile.ZipInfo(n,(2026,10,14,0,0,0));i.create_system=3;i.external_attr=(stat.S_IFREG|0o644)<<16;i.compress_type=0;z.writestr(i,(P/n).read_bytes())
require(buf.getvalue()==original,'independent closed archive bytes')
commands=[]
def run(argv,cwd):
 r=subprocess.run(argv,cwd=cwd,text=True,capture_output=True);commands.append({'argv':argv,'cwd':str(cwd),'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr});require(r.returncode==0,'command '+str(argv)+r.stderr)
scratch=Path(__file__).parent/'tmp/final1047';require(not scratch.exists(),'new scratch only');scratch.mkdir(parents=True)
try:
 with zipfile.ZipFile(io.BytesIO(original)) as z:z.extractall(scratch)
 (scratch/'verification_output').mkdir()
 for flags in (['-I','-B'],['-I','-B','-O']):
  run([sys.executable,*flags,'scripts/verify_package.py'],scratch)
  run([sys.executable,*flags,'scripts/check_mathematics.py','--output-dir','verification_output'],scratch)
  run([sys.executable,*flags,'scripts/build_supportkit.py'],scratch)
  require((scratch/'pr1047_supportkit_v1.0.zip').read_bytes()==original,'actual clean build')
  run([sys.executable,*flags,'scripts/verify_package.py'],scratch)
finally:shutil.rmtree(scratch)
for r in outputs['files']:check(F,r)
for r in outputs['final_audit_payload_files']:check(A,r)
utc=datetime.now(timezone.utc).isoformat()
integrity={'utc':utc,'pr':1047,'status':'ROOT_PASS_FINAL_ADMINISTRATION','root_full_finalization_report_and_changed_code_prose_read':True,'input_pins_verified':len(inputs),'authorized_administrative_changes':len(changes),'unchanged_preexisting_files':len(inputs)-len(changes),'terminal_outputs_rehashed':len(outputs['files']),'final_audit_payload_files_rehashed':len(outputs['final_audit_payload_files']),'source_equal_copies':len(copies),'old_copies_preserved':97,'individual_omissions_checked':len(omitted),'protected_inputs':baseline['protected'],'original_files_checked':9,'metadata_objects_identical':True,'archive':pin(P/'pr1047_supportkit_v1.0.zip'),'archive_members':len(names),'closed_archive_full_payload_and_headers_checked':True,'independent_closed_rebuild_byte_exact':True,'actual_clean_normal_optimized_build_byte_exact':True,'commands':commands,'new_compilation_or_render':False,'reviewed_PDF_source_unchanged':True,'fresh_whole_package_reviews':2,'actionable_issues':0,'publication_ready':True,'published':False,'services_hold':'preceding PR1032 priority cursor','historical_stage_semantics_preserved':True,'internal_dated_parent_pending_fields':'Preserved captured terminal administration; this external current root seal supplies final administrative adoption.'}
(A/'FINAL_INTEGRITY.json').write_text(json.dumps(integrity,indent=2)+'\n')
seal={k:v for k,v in integrity.items() if k!='commands'};seal['status']='ROOT_SEALED_READY_PENDING_PRIOR_PR1032_CURSOR';seal['final_integrity']=pin(A/'FINAL_INTEGRITY.json');seal['terminal_finalization_report']=pin(F/'FINALIZATION_REPORT.md');seal['terminal_output_pins']=pin(F/'OUTPUT_PINS.json');(A/'FINAL_SEAL.json').write_text(json.dumps(seal,indent=2)+'\n')
print(json.dumps({'status':seal['status'],'members':len(names),'copies':len(copies),'inputs':len(inputs),'outputs':len(outputs['files']),'archive_sha256':seal['archive']['sha256'],'publication_ready':True,'published':False}))
