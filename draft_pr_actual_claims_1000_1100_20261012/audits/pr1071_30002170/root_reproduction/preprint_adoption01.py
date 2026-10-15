from pathlib import Path
import hashlib, io, json, shutil, stat, subprocess, sys, zipfile
from datetime import datetime, timezone
A=Path(__file__).resolve().parents[1];P=A/'NEWpreprint_v1_0'
def require(c,m):
 if not c:raise RuntimeError(m)
def load(p):return json.loads(p.read_text())
def check(base,r,key='path'):
 p=base/r[key];b=p.read_bytes();require(len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],str(p))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for r in load(P/'FROZEN_INPUTS.json')['records']:check(A,r)
for r in load(P/'INPUT_OUTPUT_PINS.json')['records']:check(P,r)
copies=load(P/'INPUT_COPY_MAP.json')['copies']
for r in copies:check(A,r,'original_path');check(P,r,'package_copy')
meta=load(P/'metadata.json');require(meta==load(P/'metadata_wrapped.json')['metadata']==load(P/'deposit.json')['metadata'],'metadata objects')
rows=load(P/'PACKAGE_MANIFEST.json')['members']
for r in rows:check(P,r)
names=sorted([r['path'] for r in rows]+['PACKAGE_MANIFEST.json']);raw=(P/'PR1071_preprint_v1_0_support.zip').read_bytes();buf=io.BytesIO()
with zipfile.ZipFile(io.BytesIO(raw)) as z:
 require(z.namelist()==names and z.testzip() is None and len(names)==77,'archive members')
 for i in z.infolist():
  b=z.read(i);require(b==(P/i.filename).read_bytes(),'payload bytes')
  require(i.date_time==(2026,10,14,0,0,0) and i.create_system==3 and i.external_attr==(0o100644<<16) and i.compress_type==0 and not i.flag_bits&1,'archive headers')
  if i.filename!='paper.pdf':b.decode('utf-8')
with zipfile.ZipFile(buf,'w',compression=zipfile.ZIP_STORED,allowZip64=False) as z:
 for n in names:
  i=zipfile.ZipInfo(n,(2026,10,14,0,0,0));i.create_system=3;i.external_attr=(stat.S_IFREG|0o644)<<16;i.compress_type=0;z.writestr(i,(P/n).read_bytes())
require(buf.getvalue()==raw,'independent CLOSED ZIP rebuild')
commands=[]
def run(argv,cwd):
 r=subprocess.run(argv,cwd=cwd,text=True,capture_output=True);commands.append({'argv':argv,'cwd':str(cwd),'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr});require(r.returncode==0,'command '+str(argv)+r.stderr)
scratch=Path(__file__).parent/'tmp/preprint1071';require(not scratch.exists(),'new scratch only');scratch.mkdir(parents=True)
findings=[]
try:
 clean=scratch/'clean';clean.mkdir()
 with zipfile.ZipFile(io.BytesIO(raw)) as z:z.extractall(clean)
 for flags in (['-B'],['-B','-O']):
  run([sys.executable,*flags,'scripts/verify_package.py'],clean)
  run([sys.executable,*flags,'scripts/check.py','--out',str(scratch/('check'+str(len(commands))))],clean)
  out=scratch/'rebuilt.zip';run([sys.executable,*flags,'scripts/build_archive.py','--out',str(out)],clean);require(out.read_bytes()==raw,'actual rebuilt archive')
  run([sys.executable,*flags,'scripts/verify_package.py','--bindings',str(P/'UPLOAD_BINDINGS.json'),'--archive',str(out),'--require-bindings'],clean)
 # A disposable same-package path demonstrates a direct violation of the
 # documented promise that builders never rewrite frozen content.
 victim=clean/'custody/ROOT_MATH_AUDIT.md';before=victim.read_bytes()
 run([sys.executable,'-B','scripts/build_archive.py','--out',str(victim)],clean)
 after=victim.read_bytes();require(after!=before,'unsafe output control must expose overwrite')
 findings.append({'id':'ROOT-P3-ARCHIVE-FROZEN-OUTPUT-01','severity':'P3','path':'scripts/build_archive.py','trigger':'--out points to an existing frozen member in a subdirectory, e.g. custody/ROOT_MATH_AUDIT.md','observed_returncode':0,'frozen_member_bytes_before':len(before),'frozen_member_sha256_before':hashlib.sha256(before).hexdigest(),'frozen_member_bytes_after':len(after),'frozen_member_sha256_after':hashlib.sha256(after).hexdigest(),'violation':'The root-only output-directory check admits nested frozen members; opening the ZIP overwrites input before payload reads, despite the no-frozen-content-mutation promise.','required_repair':'Reject all frozen member aliases before any write, including resolved symlinks and existing hardlinks; constrain output to documented disposable locations, test controls normally and under -O. Audit all output interfaces for the same preservation promise.'})
finally:shutil.rmtree(scratch)
for r in load(P/'INPUT_OUTPUT_PINS.json')['records']:check(P,r)
result={'utc':datetime.now(timezone.utc).isoformat(),'pr':1071,'status':'ROOT_PREPRINT_P3_REPAIR_REQUIRED_FULL_REVIEW_PENDING','root_full_paper_tex_preparation_report_supplement_and_code_read':True,'all_seven_current_pdf_pages_actually_viewed':True,'paper_pdf_sha256':digest(P/'paper.pdf'),'paper_tex_sha256':digest(P/'paper.tex'),'preparation_output_pins_sha256':digest(P/'INPUT_OUTPUT_PINS.json'),'preparation_output_pins_verified':92,'prior_inputs_rehashed_unchanged':204,'source_equal_copies':50,'metadata_objects_identical':True,'archive_sha256':hashlib.sha256(raw).hexdigest(),'archive_members':77,'independent_closed_rebuild_byte_exact':True,'actual_clean_normal_optimized_reproductions_pass':True,'commands':commands,'finding_counts':{'P0':0,'P1':0,'P2':0,'P3':len(findings)},'findings':findings,'universal_mathematics_accepted_from_prior_audit':True,'source_journal_v1_boundaries_consistent':True,'publication_ready':False,'issues_resolved':False,'fresh_whole_package_reviews':0,'minimum_required':2,'services_hold':'preceding PR1032 priority cursor','candidate_unchanged':True,'new_candidate_compilation_or_marker':False}
(A/'ROOT_PREPRINT_REVIEW_01.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='commands'},indent=2))
