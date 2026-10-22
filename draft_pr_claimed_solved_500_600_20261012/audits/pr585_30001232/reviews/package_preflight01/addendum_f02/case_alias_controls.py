"""Actual unmodified-producer checks on a case-insensitive filesystem."""
import pathlib,tempfile,shutil,os,subprocess,json,hashlib
R=pathlib.Path(__file__).resolve().parent.parent;A=R.parent.parent;C=R/'.cache';D=C/'cache/scratch/copied_audit';PY=A/'root_reproduction/.cache/venv/bin/python'
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(C/'tmp'))
assert hashlib.sha256((D/'publication/make_package.py').read_bytes()).hexdigest()=='4a8b9b4b0fce6ecc2bd3f0595801e62f5214e7532e8b41567be4a852b3af9dd1'
rows=[]
for excluded in ['.cache','sources','scratch','qa','.secrets','.private']:
 with tempfile.TemporaryDirectory(dir=C/'tmp') as tmp:
  root=pathlib.Path(tmp)/'audit';shutil.copytree(D,root,symlinks=True)
  family=root/'reviews/geometry01'; lower=root/excluded/'aliased_geometry01';lower.parent.mkdir(parents=True,exist_ok=True);shutil.copytree(family,lower,symlinks=True)
  upper=root/excluded.upper()/'aliased_geometry01';assert upper.exists() and upper.samefile(lower)
  shutil.rmtree(family);family.symlink_to(upper,target_is_directory=True)
  leaf=family/'SHA256SUMS';resolved=leaf.resolve()
  p=subprocess.run(['/usr/bin/sandbox-exec','-p','(version 1) (allow default) (deny network*)',str(PY),'-B',str(root/'publication/make_package.py')],cwd=root/'publication',env=env,capture_output=True,text=True)
  assert p.returncode==0,(excluded,p.stderr)
  z=(root/'publication/verification_package.zip').read_bytes()
  rows.append({'excluded_real_component':excluded,'supplied_ancestor_alias':excluded.upper(),'same_filesystem_object_confirmed':upper.samefile(lower),'resolved_relative_source':str(resolved.relative_to(root)),'leaf_symlink':leaf.is_symlink(),'producer_source_unchanged':(root/'publication/make_package.py').read_bytes()==(D/'publication/make_package.py').read_bytes(),'actual_unmodified_producer_process_returncode':p.returncode,'invalid_source_rejected':False,'selected_family_bytes_are_preserved_authored_data':True,'zip_byte_identical_to_current':z==(D/'publication/verification_package.zip').read_bytes(),'zip_sha256':hashlib.sha256(z).hexdigest()})
(R/'addendum_f02/CASE_ALIAS_CONTROLS.json').write_text(json.dumps({'status':'SOURCE_EXCLUSION_GUARD_FAILURES','filesystem_case_insensitive_aliases_confirmed':True,'controls':rows,'scope':'All tests used copies. No raw third-party bytes were used: the unchanged producer selected the same sealed authored family from a directory it promises to exclude. This demonstrates an exclusion bypass without a new caller or changed validation/selector code, not a current archive leak.'},indent=2)+'\n')
print(json.dumps(rows,indent=2))
