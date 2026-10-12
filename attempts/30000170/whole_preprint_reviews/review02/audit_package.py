from pathlib import Path,PurePosixPath
from datetime import datetime,timezone
import hashlib,json,zipfile,subprocess,sys,stat
W=Path(__file__).resolve().parent.parent
K=W/'preprint_package_v03'; R=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
mdata=(K/'PACKAGE_MANIFEST.json').read_bytes(); m=json.loads(mdata)
assert sha(mdata)=='197df0ea3d83b19c29e0fcd3548fc309db2c8844e5096b1434c8b82e526d85e2'
files=[]
for e in m['files']:
 p=K/e['path']; b=p.read_bytes(); assert len(b)==e['bytes'] and sha(b)==e['sha256']
 files.append({'path':e['path'],'bytes':len(b),'sha256':sha(b),'mode':oct(stat.S_IMODE(p.stat().st_mode))})
assert len(files)==21
actual={str(p.relative_to(K)) for p in K.rglob('*') if p.is_file()}
assert actual=={e['path'] for e in m['files']}|{'PACKAGE_MANIFEST.json'}
archive=K/'output/nonunique_nearest_stable_complex_quadratics_verification.zip'
E=R/'independent_archive_extraction'; E.mkdir(exist_ok=True)
archive_entries=[]
with zipfile.ZipFile(archive) as z:
 names=z.namelist(); assert len(names)==12 and len(set(names))==12
 for i in z.infolist():
  p=PurePosixPath(i.filename); assert not p.is_absolute() and '..' not in p.parts
  assert not stat.S_ISLNK(i.external_attr>>16)
  b=z.read(i); archive_entries.append({'path':i.filename,'bytes':len(b),'sha256':sha(b)})
  (E/p.name).write_bytes(b)
archive_names={e['path'].split('/')[-1] for e in archive_entries}
assert archive_names=={p.name for p in (K/'verification').iterdir() if p.is_file()}
for p in E.iterdir(): assert p.read_bytes()==(K/'verification'/p.name).read_bytes()
pairs=[('VERIFICATION_README.md','README.md'),('SOURCE_PRIORITY.md','SOURCE_PRIORITY.md'),('SOURCE_PROVENANCE.json','SOURCE_PROVENANCE.json'),('LICENSE.md','LICENSE.md'),('nonunique_nearest_stable_complex_quadratics.tex','nonunique_nearest_stable_complex_quadratics.tex'),('publication_metadata.json','publication_metadata.json')]
for a,b in pairs: assert (K/a).read_bytes()==(E/b).read_bytes()
assert json.loads((K/'zenodo-deposit.json').read_bytes())['metadata']==json.loads((K/'publication_metadata.json').read_bytes())
assert json.loads((K/'zenodo-deposit.json').read_bytes())['files']==m['published_files']
assert len(json.loads((E/'HASHES.json').read_bytes())['files'])==11
runs=[]
for script,expected in [('verify_exact.py','expected_exact.json'),('verify_function_boundary.py','expected_function_boundary.json'),('check_archive_hashes.py',None)]:
 r=subprocess.run([sys.executable,script],cwd=E,capture_output=True)
 assert r.returncode==0 and not r.stderr
 (R/(script+'.stdout')).write_bytes(r.stdout)
 assert expected is None or r.stdout==(E/expected).read_bytes()
 result=json.loads(r.stdout)
 if script=='check_archive_hashes.py': assert result=={'status':'PASS','verified_files':11,'self_exclusion':'HASHES.json only'}
 runs.append({'script':script,'python':sys.version,'exit':r.returncode,'stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),'expected_byte_identical':True if expected else 'no expected file supplied; exact object checked','result':result})
report={'UTC':datetime.now(timezone.utc).isoformat(),'manifest_sha256':sha(mdata),'selected_bodies':files,'selected_total_bytes':sum(e['bytes'] for e in files),'all_files_exhaustively_manifested':True,'archive_members':archive_entries,'archive_flat_body_equality':True,'top_level_duplicate_equality':True,'deposit_metadata_equality':True,'runs':runs}
(R/'PACKAGE_CHECKS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':'PASS','selected_files':len(files),'selected_total_bytes':report['selected_total_bytes'],'archive_members':len(archive_entries),'runs':[{'script':r['script'],'exit':r['exit'],'stdout_bytes':r['stdout_bytes'],'stdout_sha256':r['stdout_sha256'],'expected_byte_identical':r['expected_byte_identical']} for r in runs]},indent=2))
