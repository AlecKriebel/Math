"""Read-only frozen-package audit and isolated offline reproduction."""
from pathlib import Path,PurePosixPath
import ast,datetime,hashlib,json,os,shutil,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[3]; PAPER=REPO/'simplicial_embedding_gap_30000439'
TMP=ROOT/'tmp';TMP.mkdir(exist_ok=True)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def record(path):
 data=path.read_bytes();return {'bytes':len(data),'sha256':sha(data)}
def invoke(args,cwd):
 env=dict(os.environ,TMPDIR=str(TMP),PYTHONNOUSERSITE='1',PYTHONPATH='')
 r=subprocess.run(args,cwd=cwd,env=env,capture_output=True,text=True,timeout=300)
 return {'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
expected={'paper.tex':(13438,'b44203e0c969b55c19fe23c687553f776635a4c20a8c4e3a1b43caa944b26e82'),
'output/paper.pdf':(75140,'5325fceeed4352f74b531a033e8474ca1fabeeff0a6b6ecb54337e17dadb4dd6'),
'output/source-and-verification.zip':(120059,'b1e4a1c22fc3eec24c9d8f479b48110ddf6d72052181995037de64b99d46791f'),
'output/zenodo-upload-kit.zip':(None,'4a5042b1e089c680bb7af5dee2d619099ad197dead6fe5483690993c91146b61'),
'output/api-metadata.json':(None,'21d80250464ed40d6937090434d43be4b92969b97288b7823809f4b350d4359a')}
inputs={name:record(PAPER/name) for name in expected}
for name,(size,digest) in expected.items():
 assert inputs[name]['sha256']==digest,name
 if size is not None:assert inputs[name]['bytes']==size,name
GATE=PAPER.parent/'draft_pr_publication_program_20260930/audits/pr16_30000439/publication_gate_input.json'
assert record(GATE)['sha256']=='89d1cf9d951591674f29a9ab26aaad26149d1780b2913020de662fabddf93a03'
(ROOT/'INPUT_BINDING.json').write_text(json.dumps({'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':invoke(['git','rev-parse','HEAD'],REPO)['stdout'].strip(),'files':inputs,'gate':record(GATE),'seal':record(ROOT/'INDEPENDENT_PROOF_SEAL.md')},indent=2)+'\n')
with zipfile.ZipFile(PAPER/'output/source-and-verification.zip') as z:
 infos=z.infolist(); assert z.testzip() is None
 names=z.namelist();assert len(names)==len(set(names))==42
 assert all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts for n in names)
 assert all(i.date_time==(2026,10,1,0,0,0) and i.external_attr==0o100644<<16 for i in infos)
 members={n:z.read(n) for n in names}
 whitelist=json.loads(members['public-files.json'])['files']
 assert set(names)==set(whitelist)|{'api-metadata.json','PACKAGE_MANIFEST.json'}
 for name in whitelist:assert members[name]==(PAPER/name).read_bytes(),name
 manifest=json.loads(members['PACKAGE_MANIFEST.json'])
 assert set(manifest['files'])==set(names)-{'PACKAGE_MANIFEST.json'}
 for name,data in members.items():
  if name!='PACKAGE_MANIFEST.json':assert manifest['files'][name]=={'sha256':sha(data),'bytes':len(data)},name
 assert manifest['paper_pdf']=={'name':'paper.pdf',**inputs['output/paper.pdf']}
 with zipfile.ZipFile(PAPER/'output/zenodo-upload-kit.zip') as kit:
  assert kit.testzip() is None and set(kit.namelist())=={'paper.pdf','source-and-verification.zip','api-metadata.json','zenodo-deposit.json','SHA256SUMS','UPLOAD.md'}
  assert kit.read('paper.pdf')==(PAPER/'output/paper.pdf').read_bytes()
  assert kit.read('source-and-verification.zip')==(PAPER/'output/source-and-verification.zip').read_bytes()
  assert kit.read('api-metadata.json')==members['api-metadata.json']==(PAPER/'output/api-metadata.json').read_bytes()
  canonical=json.loads((PAPER/'zenodo-deposit.json').read_text())
  assert json.loads(kit.read('zenodo-deposit.json'))['metadata']==canonical['metadata']==json.loads(members['api-metadata.json'])['metadata']
  assert kit.read('SHA256SUMS')==(PAPER/'output/SHA256SUMS').read_bytes()
 extracted=TMP/'extracted';extracted.mkdir(exist_ok=True)
 z.extractall(extracted)
imports={}
for name,data in members.items():
 if name.endswith('.py'):
  tree=ast.parse(data);found=[]
  for node in ast.walk(tree):
   if isinstance(node,ast.Import):found += [n.name.split('.')[0] for n in node.names]
   elif isinstance(node,ast.ImportFrom):found.append((node.module or '').split('.')[0])
  assert all(n in sys.stdlib_module_names for n in found), (name,found)
  assert not set(found)&{'socket','urllib','http','requests','ftplib','smtplib'},(name,found)
  imports[name]=sorted(set(found))
text_scan={name:{'bytes':len(data),'forbidden_path':any(part in {'tmp','__pycache__','.git','output','documents'} or part.startswith('.') for part in PurePosixPath(name).parts)} for name,data in members.items()}
assert not any(r['forbidden_path'] for r in text_scan.values())
# Canonical TeX, PDF, metadata and originals must survive the runtime repair.
old_gate=json.loads((GATE.parent/'round1_publication_gate_input.json').read_text())
assert old_gate['paper_sha256']==inputs['paper.tex']['sha256']
assert old_gate['package']['metadata_sha256']==inputs['output/api-metadata.json']['sha256']
assert old_gate['package']['deposited_files']['paper.pdf']==inputs['output/paper.pdf']
old_zip=PAPER/'tmp/round1_frozen/source-and-verification.zip'
assert old_zip.exists()
with zipfile.ZipFile(old_zip) as old:
 changed=[n for n in names if old.read(n)!=members[n]]
 assert set(changed)=={'README.md','verification/README.md','PACKAGE_MANIFEST.json'},changed
 assert record(old_zip)['sha256']==old_gate['package']['deposited_files']['source-and-verification.zip']['sha256']
for name in ['README.md','verification/README.md']:
 assert b'Python 3.10 or newer' in members[name] and b'Python 3.9' not in members[name]
print('Static hashes, exact inventory, metadata, runtime repair and stdlib imports: PASS',flush=True)
runner=invoke([sys.executable,'-S','verification/run_all.py'],extracted)
(ROOT/'OFFLINE_RUN_STDOUT.txt').write_text(runner['stdout']);(ROOT/'OFFLINE_RUN_STDERR.txt').write_text(runner['stderr'])
assert runner['returncode']==0,runner
print('All five pinned checks in extracted archive: PASS',flush=True)
(extracted/'output').mkdir(exist_ok=True)
shutil.copyfile(PAPER/'output/paper.pdf',extracted/'output/paper.pdf')
rebuild=invoke([sys.executable,'-S','build_package.py'],extracted)
assert rebuild['returncode']==0,rebuild
for name in ['source-and-verification.zip','zenodo-upload-kit.zip','api-metadata.json','SHA256SUMS','package-build.json']:
 assert (extracted/'output'/name).read_bytes()==(PAPER/'output'/name).read_bytes(),name
report={'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','python':sys.version,'source_members':len(names),'imports':imports,'repair_changed_members':changed,'old_zip_sha256':record(old_zip)['sha256'],'metadata_exact':True,'deterministic_rebuild_byte_identical':True,'runner_returncode':runner['returncode'],'rebuild_returncode':rebuild['returncode'],'inventory':text_scan,'rebuild_output':rebuild['stdout']}
(ROOT/'PACKAGE_REPRODUCTION.json').write_text(json.dumps(report,indent=2)+'\n')
print('Deterministic full rebuild: PASS',flush=True)
