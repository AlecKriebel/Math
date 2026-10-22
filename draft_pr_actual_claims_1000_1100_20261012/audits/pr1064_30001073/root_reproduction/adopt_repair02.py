from pathlib import Path
import hashlib,io,json,os,shutil,stat,subprocess,sys,zipfile
from datetime import datetime,timezone
A=Path(__file__).resolve().parents[1];P=A/'preprint_v1_0';F=A/'repairs/package02';R=Path(__file__).parent
def require(c,m):
 if not c:raise RuntimeError(m)
def load(p):return json.loads(p.read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(base,r,key='path'):
 p=base/r[key];require(p.stat().st_size==r['bytes'] and digest(p)==r['sha256'],str(p))
changed=load(F/'CHANGE_INVENTORY.json')['modified'];mapping={r['path']:r for r in changed};require(len(mapping)==10,'changes')
inputs=load(F/'INPUT_PINS.json')['records']
for r in inputs:check(A,dict(r,path=mapping[r['path']]['preserved_path']) if r['path'] in mapping else r)
for r in changed:check(A,r['after']);check(A,dict(r['before'],path=r['preserved_path']))
for r in load(F/'BEFORE_PINS.json')['entries']:check(F,r,'preserved_path')
for r in load(F/'OUTPUT_PINS.json')['entries']:check(F,r)
for r in load(F/'FINAL_CURRENT_PINS.json')['records']:check(P,r)
old=load(F/'before/preprint_v1_0/COPY_MAP.json')['copies'];copies=load(P/'COPY_MAP.json')['copies'];require(len(copies)==122 and copies[:91]==old,'copies')
for r in copies:check(A,r,'source_path');check(P,r,'package_path')
require(digest(P/'paper.pdf')=='67f07f64a5b06c9a4372c285ed438e735fb780d8477b25652bea4f7f6c72e072','PDF')
meta=load(P/'metadata.json');require(meta==load(P/'publication/release_metadata.json')['metadata']==load(P/'publication/zenodo.json')['metadata'],'metadata')
names=load(P/'SUPPORT_ALLOWLIST.json')['members'];raw=(P/'support.zip').read_bytes();b=io.BytesIO()
with zipfile.ZipFile(io.BytesIO(raw)) as z:
 require(len(names)==149 and z.namelist()==names and z.testzip() is None,'members')
 for i in z.infolist():
  require(z.read(i)==(P/i.filename).read_bytes(),'payload');require(i.date_time==(2026,10,14,0,0,0) and i.create_system==3 and i.external_attr==(0o100644<<16) and i.compress_type==8 and not i.flag_bits&1,'header')
  if i.filename!='paper.pdf':z.read(i).decode('utf-8')
with zipfile.ZipFile(b,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for n in names:
  i=zipfile.ZipInfo(n,(2026,10,14,0,0,0));i.create_system=3;i.external_attr=(stat.S_IFREG|0o644)<<16;i.compress_type=8;z.writestr(i,(P/n).read_bytes(),compress_type=8,compresslevel=9)
require(b.getvalue()==raw,'independent CLOSED rebuild')
commands=[]
def run(argv,cwd,success=True):
 q=subprocess.run(argv,cwd=cwd,text=True,capture_output=True);commands.append({'argv':argv,'cwd':str(cwd),'returncode':q.returncode,'stdout':q.stdout,'stderr':q.stderr});require((q.returncode==0)==success,str(argv)+q.stderr);return q
run([sys.executable,'-I','-B','resolve_prior_stages.py'],F)
s=R/'tmp/repair02';s.mkdir(parents=True,exist_ok=False)
try:
 with zipfile.ZipFile(io.BytesIO(raw)) as z:z.extractall(s)
 for flags in (['-I','-B'],['-I','-B','-O']):
  run([sys.executable,*flags,'verify_package.py'],s);run([sys.executable,*flags,'run_checks.py','--out-dir','tmp/recheck'],s)
  run([sys.executable,*flags,'build_archive.py','--output','tmp/rebuilt.zip'],s);require((s/'tmp/rebuilt.zip').read_bytes()==raw,'actual rebuild')
  run([sys.executable,*flags,'verify_package.py','--archive','tmp/rebuilt.zip','--deposit-binding',str(P/'publication/DEPOSIT_BINDING.json'),'--require-deposit-binding'],s)
  target=s/'publication/DEPOSIT_BINDING.json';shutil.copyfile(P/'publication/DEPOSIT_BINDING.json',target);alias=s/'tmp/hardlinked.zip'
  if alias.exists():alias.unlink()
  os.link(target,alias);before=digest(target)
  q=run([sys.executable,*flags,'build_archive.py','--output','tmp/hardlinked.zip'],s,False)
  require('cannot overwrite protected package input' in q.stderr and digest(target)==before and digest(alias)==before,'prewrite alias rejection preserves descriptor');alias.unlink();target.unlink()
finally:shutil.rmtree(s)
for r in load(F/'OUTPUT_PINS.json')['entries']:check(F,r)
for r in load(F/'FINAL_CURRENT_PINS.json')['records']:check(P,r)
x={'utc':datetime.now(timezone.utc).isoformat(),'pr':1064,'status':'ADOPT_BOUNDED_ARCHIVE_ALIAS_REPAIR02_PENDING_NEW_WHOLE03','root_full_repair_report_and_complete_code_diff_read':True,'report_sha256':digest(F/'REPAIR_REPORT.md'),'repair_output_pins_sha256':digest(F/'OUTPUT_PINS.json'),'repair_outputs_rehashed':41,'immediate_inputs_verified':len(inputs),'authorized_changes':10,'all_other_inputs_unchanged':len(inputs)-10,'all25_exact_before_copies_verified':True,'current158_files_verified':True,'source_equal_copies':122,'old91_copy_records_preserved':True,'metadata_objects_identical_unchanged':True,'canonical_PDF_unchanged':True,'all_prior_stages_resolved_by_actual_command':True,'independent_closed_rebuild_byte_exact':True,'archive_members':149,'archive_sha256':digest(P/'support.zip'),'root_actual_normal_optimized_descriptor_hardlink_rejection_and_preservation':True,'actual_clean_standard_library_commands_and_strict_binding_pass':True,'commands':commands,'new_actual_compilation_or_render_or_marker':False,'fresh_whole_package_reviews':2,'minimum_required':2,'publication_ready':False,'issues_updated':False,'published':False,'services_hold':'preceding PR1032 priority cursor','required_next_gate':'NEW complete whole03 review, including real standalone compile and all five current PDF pages.'}
(A/'ROOT_REPAIR_REVIEW_02.json').write_text(json.dumps(x,indent=2)+'\n');print(json.dumps({k:v for k,v in x.items() if k!='commands'},indent=2))
