from pathlib import Path
import json,hashlib,subprocess,datetime,shutil,tempfile,os,stat
A=Path(__file__).resolve().parents[1];F=A/'repairs/preprint_support01_20261016';P=A/'preprint_v1_1';K=P/'kit';O=A/'root_reproduction/support_repair01_20261016';O.mkdir(exist_ok=False)
def need(c,s):
 if not c:raise RuntimeError(s)
def read(p):return json.loads(p.read_text())
def ident(p):
 b=p.read_bytes();return{'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def match(p,r):need(ident(p)=={k:r[k]for k in ['bytes','sha256']},'Pin '+str(p))
for parent,name in [(P,'PREPARATION_SEAL.json'),(F,'REPAIR_SEAL.json')]:
 for r in read(parent/name)['files']:match(parent/r['path'],r)
for r in read(F/'PRESERVED_V1_0_PINS.json')['files']:match(A/r['path'],r)
for r in read(A/'preparation/unknown_priority_20261016/ORIGINAL_INPUT_PINS.json')['files']:match(A/r['path'],r)
for r in read(A/'reviews/package_01/OUTPUT_FINAL_INVENTORY.json')['files']:match(A/'reviews/package_01'/r['path'],r)
match(A/'publication/zenodo-deposit-v1_1.json',read(P/'PREPARATION_SEAL.json')['versioned_native_manifest'])
old=(A/'preprint_v1_0/paper.tex').read_text();new=(P/'paper.tex').read_text()
def proof(s):return s[s.index(r'\section{Statement'):s.index(r'\section{Reproducibility')]
need(proof(old)==proof(new),'Sections1-6 changed')
metadata=read(P/'.zenodo.json');need(metadata==read(K/'.zenodo.json')==read(P/'zenodo-deposit.json')['metadata']==read(A/'publication/zenodo-deposit-v1_1.json')['metadata'],'Exact bibliographic metadata objects')
need('pending root adoption'not in metadata['description']and'No deposit or DOI'not in metadata['description'],'Permanent lifecycle wording')
for text in [new,json.dumps(read(K/'BIBLIOGRAPHIC_OBJECTS.json')),json.dumps(read(K/'SOURCE_CREDITS.json')),json.dumps(metadata['references'])]:
 need('Automorphic Forms: New Directions'in text and'Unitary periods and distinction;'in text,'Current OWR title correction')
need(read(K/'STATUS.json')['publication_ready']is False and'as_of_utc'in read(K/'STATUS.json'),'Dated preparation status')
commands=[]
def run(argv):
 p=subprocess.run(list(map(str,argv)),cwd=O,capture_output=True,text=True);commands.append({'argv':list(map(str,argv)),'cwd':str(O),'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr});save(O/'ACTUAL_COMMANDS.json',commands);need(p.returncode==0,'Command '+str(argv));return p
# Exact original matrix body, only new output/fixture root and frozen kit root adapted.
src=(F/'test_builder.py').read_text();src=src.replace('R=Path(__file__).absolute().parent','R=Path('+repr(str(O))+')').replace("K=R.parents[1]/'preprint_v1_1/kit'",'K=Path('+repr(str(K))+')');runner=O/'test_builder_replay.py';runner.write_text(src)
run(['/opt/homebrew/bin/python3.14','-I','-B',runner,'own_fixture_matrix','ROOT_BUILDER_TEST_RESULTS.json'])
matrix=read(O/'ROOT_BUILDER_TEST_RESULTS.json');need(matrix['mode_processes']==90 and matrix['status']=='PASS','90 actual processes');expected=read(F/'FINAL_BUILDER_TEST_RESULTS.json')
project=lambda rows:[{k:r.get(k)for k in ['case','mode','exit','kit_before_after_identical','no_output_created_on_rejection','output_bytes','output_sha256']}for r in rows]
need(project(matrix['records'])==project(expected['records']),'Full 90 outcomes and preservation results')
tmp=Path(tempfile.mkdtemp(prefix='ROOT1032-repair-',dir='/private/tmp'));archive=P/'pr1032_supportkit_v1.1.zip'
try:
 values=[]
 for py in ['/opt/homebrew/bin/python3.11','/opt/homebrew/bin/python3.14']:
  for flags in [[],['-O']]:values.append(json.loads(run([py,'-I','-B',*flags,K/'scripts/verify_kit.py','--archive',archive]).stdout))
 need(all(v==values[0]for v in values),'Complete whole-kit JSON across installed runtimes/modes')
 built=tmp/'rebuilt.zip';run(['/opt/homebrew/bin/python3.14','-I','-B',K/'scripts/build_archive.py',built]);need(built.read_bytes()==archive.read_bytes(),'Actual outside rebuild identical')
 run(['/opt/homebrew/bin/python3.14','-B',A.parents[2]/'zenodo_deposit_tool/zenodo.py','check',A/'publication/zenodo-deposit-v1_1.json'])
finally:
 cleanup=[]
 for root in [tmp,O/'own_fixture_matrix']:
  for p in sorted(root.rglob('*')):
   s=p.lstat();r={'path':str(p),'mode':stat.S_IFMT(s.st_mode)}
   if p.is_symlink():r['target']=os.readlink(p)
   elif stat.S_ISREG(s.st_mode):r.update(ident(p))
   cleanup.append(r)
 save(O/'OWN_UNSEALED_FIXTURE_CLEANUP.json',{'records':cleanup,'scope':'Only fresh ROOT unsealed physical fixture copies/external ZIP; all regular bytes and link/FIFO identity captured before cleanup. Canonical/old pinned files unchanged.'})
 shutil.rmtree(tmp);shutil.rmtree(O/'own_fixture_matrix')
for r in read(F/'PRESERVED_V1_0_PINS.json')['files']:match(A/r['path'],r)
for r in read(P/'PREPARATION_SEAL.json')['files']:match(P/r['path'],r)
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ROOT_ADOPT_ALL_THREE_BOUNDED_SUPPORT_REPAIRS_NEW_COMPLETE_WHOLE02_REQUIRED','ROOT_full_repair_report_record_current_README_status_metadata_source_correction_builder_and_entire_matrix_source_read':True,'preprint_content_rows_rehashed':49,'repair_content_rows_rehashed':31,'old_v1_0_preparation_native_rows_unchanged':72,'original_input_rows_unchanged':287,'whole01_output_rows_unchanged':650,'sections1_6_exact_bytes_unchanged':True,'sections1_6_SHA256':hashlib.sha256(proof(new).encode()).hexdigest(),'ROOT_actual_commands':commands,'ROOT_actual_independent_matrix_children':90,'complete90_outcomes_and_unchanged_input_results_match_author':True,'visual_coverage':'ROOT actually viewed changed current pages1,8. Other7 current rasters are byte-identical to v1.0 pages previously actually viewed by ROOT. Author actually viewed all9 current pages. No new ROOT compile/render claimed.','three_P3_implementation_status':{'P3-01':'physical outside-kit static preflight and pre-write full regular/hash/allowlist checks; 90 freshROOTcase/mode executions','P3-02':'primary OWR contribution/report titles/joint-work note corrected in current tex/PDF/source-credit/bibliographic/metadata objects; old historical rows remain qualified byte-exact','P3-03':'timeless permanent metadata/paper/docs; explicitly dated preparation-stage STATUS remains false pending actual gates'},'whole_reviews_completed':1,'minimum_whole_reviews_TOTAL':2,'next_gate':'NEW COMPLETE independent whole02 reviewing entire v1.1 and all proof/source/metadata/kit, even if bounded repair has no remaining concern; repeat loop if actionables.','Luo_Zha_overlap':'UNKNOWN, useracceptednonblocking; no bodyretrieval or noveltypromotion','publication_ready':False,'issues_resolved':False,'published':False,'paper':ident(P/'paper.pdf'),'support_archive':ident(archive),'preprint_seal':ident(P/'PREPARATION_SEAL.json'),'repair_seal':ident(F/'REPAIR_SEAL.json'),'local_read_command_errors':'Earlier ROOT bounded-read commands named absent optional files output_boundary.py and REPAIR_NOTES.md; actual builder is self-contained and repair record is REPAIR_RECORD.md. Full actual operative files subsequently read; no candidate failure.'}
save(A/'ROOT_SUPPORT_REPAIR_ADOPTION_01_20261016.json',record);print(json.dumps({'status':record['status'],'top_level_commands':len(commands),'matrix_children':90,'paper':record['paper'],'archive':record['support_archive']}))
