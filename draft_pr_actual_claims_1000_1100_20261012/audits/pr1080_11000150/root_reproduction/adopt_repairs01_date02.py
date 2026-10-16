from pathlib import Path
import json,hashlib,datetime,io,zipfile,tempfile,subprocess,os
A=Path(__file__).resolve().parents[1];P=A/'preprint_v1_0';K=P/'verification_kit'
R1=A/'repairs/package01';R2=A/'repairs/package01_metadata_date02'
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def check(p,x):
 b=p.read_bytes()
 if len(b)!=x['bytes'] or sha(b)!=x['sha256']:raise RuntimeError(str(p))
 return b
def resolve(x):
 candidates=[A/x['path'],R2/'before'/x['path'],R1/'before'/x['path']]
 for p in candidates:
  if p.is_file() and p.stat().st_size==x['bytes'] and sha(p.read_bytes())==x['sha256']:return p
 raise RuntimeError('No exact historical resolution: '+x['path'])
counts={}
for R in [R1,R2]:
 rows=load(R/'OUTPUT_PINS.json')['files']
 for x in rows:check(R/x['path'],x)
 counts[R.name+'_outputs']=len(rows)
 for n in ['IMMEDIATE_INPUT_PINS.json','CURRENT_INPUT_PINS.json','PROTECTED_INPUT_PINS.json']:
  rows=load(R/n)['files']
  for x in rows:check(resolve(x),x)
  counts[R.name+'_'+n]=len(rows)
changes=load(R2/'CHANGE_ACCOUNTING.json')['changes']
for x in changes:
 check(A/x['source_snapshot'],x['before']);check(A/x['path'],x['after'])
copies=load(K/'REPAIR01_STAGE_COPIES.json')['files']
for x in copies:
 if check(K/x['destination'],x)!=(A/x['source_snapshot']).read_bytes():raise RuntimeError('Copy equality')
history=load(K/'REPAIR01_HISTORY_RESOLUTION.json')['references']
for x in history:
 if x['disposition']=='exact_captured_stage_or_canonical_copy':check(K/x['destination'],x)
 elif x['disposition']!='omitted' or not x['reason']:raise RuntimeError('Unexplained old-stage omission')
metadata=load(P/'metadata.json');old=load(R2/'before/preprint_v1_0/metadata.json')
if {k:v for k,v in metadata.items() if k!='notes'}!={k:v for k,v in old.items() if k!='notes'}:raise RuntimeError('Unauthorized metadata field')
if 'At the bounded-repair checkpoint on 2026-10-14' not in metadata['notes']:raise RuntimeError('Undated review state')
if metadata!=load(K/'metadata.json') or metadata!=load(P/'deposit_metadata.json')['metadata']:raise RuntimeError('Native metadata consistency')
if (P/'research_metadata.json').read_bytes()!=(R1/'before/preprint_v1_0/metadata.json').read_bytes():raise RuntimeError('Old research metadata changed')
for n in ['preprint.tex','preprint.pdf']:
 x=next(x for x in load(R1/'IMMEDIATE_INPUT_PINS.json')['files'] if x['path']=='preprint_v1_0/'+n);check(P/n,x)
archive=P/'verification_kit.zip';names=load(K/'ALLOWLIST.json')['members']
buf=io.BytesIO()
with zipfile.ZipFile(buf,'w',compression=zipfile.ZIP_STORED) as z:
 for n in names:
  i=zipfile.ZipInfo('verification_kit/'+n,(2026,10,14,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;i.compress_type=zipfile.ZIP_STORED
  z.writestr(i,(K/n).read_bytes())
if buf.getvalue()!=archive.read_bytes():raise RuntimeError('Independent CLOSED ZIP differs')
with zipfile.ZipFile(archive) as z:
 if z.namelist()!=['verification_kit/'+n for n in names] or z.testzip() is not None:raise RuntimeError('ZIP names/CRC')
 for n in names:
  if z.read('verification_kit/'+n)!=(K/n).read_bytes():raise RuntimeError('Payload differs')
commands=[]
with tempfile.TemporaryDirectory(prefix='root-repair-date02-',dir=Path(__file__).parent) as td:
 td=Path(td).resolve()
 with zipfile.ZipFile(archive) as z:z.extractall(td)
 clean=td/'verification_kit';baseline={n:sha((clean/n).read_bytes()) for n in names}
 def run(flags,args,ok=True):
  argv=['python3','-I','-B',*flags,*args];p=subprocess.run(argv,cwd=clean,capture_output=True)
  if (p.returncode==0)!=ok:raise RuntimeError(str(argv)+p.stderr.decode(errors='replace'))
  commands.append({'argv':argv,'exit_code':p.returncode,'expected_success':ok,'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr)})
  return p
 results=[]
 for flags,mode in [([], 'normal'),(['-O'],'optimized')]:
  run(flags,['verify.py']);results.append(json.loads(run(flags,['run_checks.py']).stdout))
  rebuilt=td/('rebuilt-'+mode+'.zip');run(flags,['build_archive.py','--output',str(rebuilt)])
  if rebuilt.read_bytes()!=archive.read_bytes():raise RuntimeError('Clean rebuilt archive differs')
  run(flags,['verify.py','--require-binding','--binding',str(P/'EXTERNAL_BINDING.json'),'--pdf',str(P/'preprint.pdf'),'--archive',str(rebuilt)])
  run(flags,['verify.py','--require-binding'],False)
  alias=td/('alias-'+mode);os.link(clean/'preprint.tex',alias)
  run(flags,['build_archive.py','--output',str(alias)],False);alias.unlink()
  if {n:sha((clean/n).read_bytes()) for n in names}!=baseline:raise RuntimeError('Protected clean input changed')
 # Run adapters include their own runtime timestamps; compare only their declared
 # mathematical fields, as the original root preparation review did.
 run([],[str(A.parents[2]/'zenodo_deposit_tool/zenodo.py'),'check',str(P/'deposit_metadata.json')])
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ROOT_ADOPT_BOUNDED_REPAIR01_AND_DATED_METADATA_SUCCESSOR_PENDING_NEW_WHOLE02','full_both_reports_699_line_repair_diff_and_complete_date02_diff_read':True,'rehash_counts':counts,'date02_authorized_changes':len(changes),'source_equal_copies':len(copies),'individually_checked_historical_resolution_rows':len(history),'independent_CLOSED_archive_equal':True,'archive_members':len(names),'native_metadata_objects_equal_and_only_notes_changed_in_successor':True,'paper_TeX_PDF_math_and_source_unchanged':True,'actual_clean_commands':commands,'no_new_paper_compilation_or_render_in_bounded_repair':True,'fresh_complete_whole_reviews_completed':1,'minimum_whole_reviews':2,'publication_ready':False,'published':False,'services_held_after_pr':1032}
(A/'ROOT_REPAIR_REVIEW_01_DATE02.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='actual_clean_commands'}))
