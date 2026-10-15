from pathlib import Path
import hashlib,io,json,os,shutil,stat,subprocess,sys,zipfile
from datetime import datetime,timezone
A=Path(__file__).resolve().parents[1];P=A/'preprint_v1_0';K=P/'verification_kit';R=Path(__file__).parent
def require(c,m):
 if not c:raise RuntimeError(m)
def load(p):return json.loads(p.read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(base,r,key='path'):
 p=base/r[key];require(p.stat().st_size==r['bytes'] and digest(p)==r['sha256'],str(p))
for r in load(P/'INPUT_PINS.json')['files']:check(A,r)
for r in load(P/'OUTPUT_PINS.json')['files']:check(P,r)
ledger=load(K/'COPY_EXCLUSION_LEDGER.json');copies=0
for r in ledger['files']:
 check(A,r)
 if r['disposition']=='byte_identical_copy':check(K,r,'destination');copies+=1
 else:require(r['disposition']=='omitted' and bool(r['reason']),'omission')
for r in ledger['historical_pin_references']:
 if r['disposition']=='hash_identical_canonical_copy':require(digest(K/r['destination'])==r['sha256'],'historical mapping')
 else:require(r['disposition']=='omitted' and bool(r['reason']),'historical omission')
require(copies==60,'copies');require((P/'metadata.json').read_bytes()==(P/'deposit_metadata.json').read_bytes()==(K/'metadata.json').read_bytes(),'metadata')
names=load(K/'ALLOWLIST.json')['members'];raw=(P/'verification_kit.zip').read_bytes();buf=io.BytesIO();prefix='verification_kit/'
with zipfile.ZipFile(io.BytesIO(raw)) as z:
 require(z.namelist()==[prefix+n for n in names] and z.testzip() is None and len(names)==72,'members')
 for i in z.infolist():
  b=z.read(i);require(b==(K/i.filename[len(prefix):]).read_bytes(),'payload');b.decode('utf-8');require(i.date_time==(2026,10,14,0,0,0) and i.create_system==3 and i.external_attr==(0o100644<<16) and i.compress_type==0 and not i.flag_bits&1,'header')
with zipfile.ZipFile(buf,'w',compression=zipfile.ZIP_STORED) as z:
 for n in names:
  i=zipfile.ZipInfo(prefix+n,(2026,10,14,0,0,0));i.create_system=3;i.external_attr=(stat.S_IFREG|0o644)<<16;i.compress_type=0;z.writestr(i,(K/n).read_bytes())
require(buf.getvalue()==raw,'closed independent rebuild')
commands=[]
def run(argv,cwd,success=True):
 q=subprocess.run(argv,cwd=cwd,text=True,capture_output=True);commands.append({'argv':argv,'cwd':str(cwd),'returncode':q.returncode,'stdout':q.stdout,'stderr':q.stderr});require((q.returncode==0)==success,str(argv)+q.stderr);return q
s=R/'tmp/preprint1080';s.mkdir(parents=True,exist_ok=False)
try:
 with zipfile.ZipFile(io.BytesIO(raw)) as z:z.extractall(s)
 clean=s/'verification_kit'
 for flags in (['-I','-B'],['-I','-B','-O']):
  run([sys.executable,*flags,'verify.py'],clean);run([sys.executable,*flags,'run_checks.py'],clean)
  run([sys.executable,*flags,'build_archive.py','--output',str(s/'rebuilt.zip')],clean);require((s/'rebuilt.zip').read_bytes()==raw,'actual rebuild')
  run([sys.executable,*flags,'verify.py','--require-binding','--binding',str(P/'EXTERNAL_BINDING.json'),'--pdf',str(P/'preprint.pdf'),'--archive',str(s/'rebuilt.zip')],clean)
 run([sys.executable,'-I','-B','fault_checks.py'],clean)
 victim=clean/'preprint.tex';before=digest(victim);alias=s/'hardlinked.zip';os.link(victim,alias)
 q=run([sys.executable,'-I','-B','build_archive.py','--output',str(alias)],clean);require(digest(victim)!=before,'output alias probe');after=digest(victim)
finally:shutil.rmtree(s)
repo=A.parents[2];q=run([sys.executable,'-B',str(repo/'zenodo_deposit_tool/zenodo.py'),'check',str(P/'deposit_metadata.json')],repo,False)
findings=[{'id':'ROOT-P3-ARCHIVE-HARDLINK-01','severity':'P3','path':'verification_kit/build_archive.py','trigger':'Existing --output hardlink outside kit targets allowlisted preprint.tex','returncode':0,'before_sha256':before,'after_sha256':after,'required_repair':'Reject aliases to protected inputs and delivery files before output writes, including resolved symlinks and existing samefile hardlinks.'},{'id':'ROOT-P2-ZENODO-MANIFEST-01','severity':'P2','path':'deposit_metadata.json','trigger':'Repository upload kit local check of supplied custom deposit metadata','returncode':q.returncode,'error':q.stderr,'required_repair':'Supply reviewed native Zenodo API metadata and repository-kit {metadata,files} manifest naming exact PDF/ZIP. Keep custom research metadata separately identified; align all bibliographic and scope/disclosure fields. Local upload-kit check must pass.'}]
for r in load(P/'OUTPUT_PINS.json')['files']:check(P,r)
visual=R/'tmp/visual1080';images=[{'page':n,'bytes':(visual/f'page-{n}.png').stat().st_size,'sha256':digest(visual/f'page-{n}.png'),'actually_root_viewed':True} for n in range(1,8)]
x={'utc':datetime.now(timezone.utc).isoformat(),'pr':1080,'status':'ROOT_PREPRINT_P2_P3_REPAIRS_REQUIRED_FULL_REVIEW_PENDING','root_full_paper_preparation_report_and_reproduction_interfaces_read':True,'root_all_seven_current_pdf_pages_actually_viewed':True,'page_renders':images,'paper_pdf_sha256':digest(P/'preprint.pdf'),'paper_tex_sha256':digest(P/'preprint.tex'),'output_pins_sha256':digest(P/'OUTPUT_PINS.json'),'output_pins_rehashed':90,'preexisting_inputs_rehashed_unchanged':194,'exact_copies':copies,'historical_pin_references_checked':len(ledger['historical_pin_references']),'three_custom_metadata_files_byte_identical':True,'archive_members':72,'archive_sha256':hashlib.sha256(raw).hexdigest(),'independent_closed_rebuild_byte_exact':True,'actual_clean_normal_optimized_checks_rebuild_strict_binding_pass':True,'commands':commands,'findings':findings,'finding_counts':{'P0':0,'P1':0,'P2':1,'P3':1},'mathematics_credited_scope_consistent_with_root_acceptance':True,'restricted_arbitrary_length_clause':'complete negative answer','full_higher_genus_maximum_classification_bundle':'partial, unresolved in this work','priority_and_novelty':'UNKNOWN','publication_ready':False,'fresh_whole_package_reviews':0,'minimum_required':2,'published':False,'services_hold':'preceding PR1032 priority cursor','candidate_unchanged':True,'new_candidate_compilation_or_marker':False}
(A/'ROOT_PREPRINT_REVIEW_01.json').write_text(json.dumps(x,indent=2)+'\n');shutil.rmtree(visual);print(json.dumps({k:v for k,v in x.items() if k not in ['commands','page_renders']},indent=2))
