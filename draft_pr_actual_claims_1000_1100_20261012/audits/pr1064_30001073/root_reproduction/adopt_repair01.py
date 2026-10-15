from pathlib import Path
import hashlib, io, json, shutil, stat, subprocess, sys, zipfile
from datetime import datetime, timezone
A=Path(__file__).resolve().parents[1]; F=A/'repairs/package01'; P=A/'preprint_v1_0'
def require(c,m):
 if not c: raise RuntimeError(m)
def load(p): return json.loads(p.read_text())
def check(base,r,name='path'):
 p=base/r[name]; b=p.read_bytes()
 require(len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],str(p))
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
changes=load(F/'CHANGE_INVENTORY.json')['modified']; modified={r['path']:r for r in changes}
require(len(modified)==10,'change count')
for r in changes:
 check(A,r['after']); check(A,dict(r['before'],path=r['preserved_path']))
inputs=load(F/'INPUT_PINS.json')['records']
for r in inputs:
 if r['path'] in modified: check(A,dict(r,path=modified[r['path']]['preserved_path']))
 else: check(A,r)
for r in load(F/'BEFORE_PINS.json')['entries']: check(F,r,'preserved_path')
for r in load(F/'OUTPUT_PINS.json')['entries']: check(F,r)
for r in load(F/'FINAL_CURRENT_PINS.json')['records']: check(P,r)
for r in load(P/'CURRENT_OUTPUT_PINS.json')['entries']: check(P,r)
before=load(F/'before/preprint_v1_0/COPY_MAP.json')['copies']; copies=load(P/'COPY_MAP.json')['copies']
require(copies[:72]==before and len(copies)==91,'copy preservation')
for r in copies:
 check(A,r,'source_path'); check(P,r,'package_path')
meta=load(P/'metadata.json')
require(meta==load(P/'publication/release_metadata.json')['metadata']==load(P/'publication/zenodo.json')['metadata'],'metadata objects')
require(digest(P/'paper.pdf')=='67f07f64a5b06c9a4372c285ed438e735fb780d8477b25652bea4f7f6c72e072','canonical PDF')
for f in ('metadata.json','publication/release_metadata.json','publication/zenodo.json','paper.tex','paper.pdf'):
 require((P/f).read_bytes()==(A/'repairs/package01/before/preprint_v1_0'/f).read_bytes() if (A/'repairs/package01/before/preprint_v1_0'/f).exists() else True,'preserved '+f)
names=load(P/'SUPPORT_ALLOWLIST.json')['members']; original=(P/'support.zip').read_bytes(); buf=io.BytesIO()
with zipfile.ZipFile(io.BytesIO(original)) as z:
 require(z.namelist()==names and z.testzip() is None and len(names)==117,'closed members')
 for r in z.infolist():
  require(z.read(r)==(P/r.filename).read_bytes(),'member bytes')
  require(r.date_time==(2026,10,14,0,0,0) and r.create_system==3 and r.external_attr==(0o100644<<16) and r.compress_type==8 and not r.flag_bits&1,'header')
  if r.filename!='paper.pdf': z.read(r).decode('utf-8')
with zipfile.ZipFile(buf,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n in names:
  i=zipfile.ZipInfo(n,(2026,10,14,0,0,0)); i.create_system=3; i.external_attr=(stat.S_IFREG|0o644)<<16; i.compress_type=8
  z.writestr(i,(P/n).read_bytes(),compress_type=8,compresslevel=9)
require(buf.getvalue()==original,'independent closed archive')
commands=[]
def run(argv,cwd,expected=0):
 r=subprocess.run(argv,cwd=cwd,text=True,capture_output=True)
 commands.append({'argv':argv,'cwd':str(cwd),'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
 require(r.returncode==expected,'command '+str(argv)+r.stderr)
run([sys.executable,'-I','-B','resolve_preparation_stage.py'],F)
scratch=Path(__file__).parent/'tmp/repair01'; require(not scratch.exists(),'new scratch only'); scratch.mkdir(parents=True)
try:
 with zipfile.ZipFile(io.BytesIO(original)) as z: z.extractall(scratch)
 for flags in (['-I','-B'],['-I','-B','-O']):
  run([sys.executable,*flags,'verify_package.py'],scratch)
  run([sys.executable,*flags,'run_checks.py','--out-dir','tmp/recheck'+str(len(commands))],scratch)
  run([sys.executable,*flags,'build_archive.py','--output','tmp/rebuilt.zip'],scratch)
  require((scratch/'tmp/rebuilt.zip').read_bytes()==original,'actual rebuild')
  run([sys.executable,*flags,'verify_package.py','--archive','tmp/rebuilt.zip','--deposit-binding',str(P/'publication/DEPOSIT_BINDING.json'),'--require-deposit-binding'],scratch)
finally: shutil.rmtree(scratch)
for r in load(F/'OUTPUT_PINS.json')['entries']: check(F,r)
result={'utc':datetime.now(timezone.utc).isoformat(),'pr':1064,'status':'ADOPT_BOUNDED_REPAIR_PENDING_NEW_WHOLE_02','root_complete_repair_report_and_code_diff_read':True,'repair_report_sha256':digest(F/'REPAIR_REPORT.md'),'repair_output_pins_sha256':digest(F/'OUTPUT_PINS.json'),'repair_outputs_rehashed':37,'all_immediate_input_pins_verified':len(inputs),'unchanged_inputs':len(inputs)-len(modified),'authorized_changes':len(modified),'current_files_verified':125,'current_source_equal_copies':91,'old_copy_records_preserved':72,'closed_archive_members':len(names),'independent_closed_rebuild_byte_exact':True,'archive_sha256':hashlib.sha256(original).hexdigest(),'canonical_pdf_unchanged':True,'metadata_objects_identical':True,'historical_103_pins_resolved_by_actual_command':True,'commands':commands,'fresh_whole_package_reviews':1,'minimum_required':2,'publication_ready':False,'issues_updated':False,'published':False,'services_hold':'preceding PR1032 priority cursor','scope':'Bounded package repair adoption; universal mathematics remains governed by prior proof audits, finite diagnostics are supplemental. No actual candidate compilation/render or new PDF marker.'}
(A/'ROOT_REPAIR_REVIEW_01.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='commands'},indent=2))
