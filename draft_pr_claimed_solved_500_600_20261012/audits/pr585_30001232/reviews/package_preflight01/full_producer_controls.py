"""Process controls in copies; the exact producer add guard is never patched."""
import pathlib, tempfile, shutil, subprocess, json, hashlib, os
R=pathlib.Path(__file__).resolve().parent;A=R.parent.parent;C=R/'.cache'; D=C/'cache/scratch/copied_audit'; PY=A/'root_reproduction/.cache/venv/bin/python'
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(C/'tmp'))
rows=[]
for case in ['cache_source','private_source','traversal_source','duplicate_selection','leaf_symlink','outside_ancestor_symlink','lexical_parent_alias_selection']:
 with tempfile.TemporaryDirectory(dir=C/'tmp') as tmp:
  root=pathlib.Path(tmp)/'audit';shutil.copytree(D,root,symlinks=True); pub=root/'publication'; code=pub/'make_package.py'
  if case in ['cache_source','private_source']:
   component='.cache' if case=='cache_source' else '.private'
   path=root/'reviews/geometry01'/component/'test';path.parent.mkdir(parents=True,exist_ok=True);path.write_text('excluded')
   seal=root/'reviews/geometry01/SHA256SUMS';seal.write_text(seal.read_text()+hashlib.sha256(path.read_bytes()).hexdigest()+'  '+component+'/test\n')
  elif case=='traversal_source':
   seal=root/'reviews/geometry01/SHA256SUMS';seal.write_text(seal.read_text()+'0'*64+'  ../../CURRENT_CORRECTIONS.md\n')
  elif case=='duplicate_selection':
   seal=root/'reviews/geometry01/SHA256SUMS';seal.write_text(seal.read_text()+seal.read_text().splitlines()[0]+'\n')
  elif case=='leaf_symlink':
   target=root/'CURRENT_CORRECTIONS.md';raw=target.read_bytes();target.unlink();other=root/'allowed_copy.md';other.write_bytes(raw);target.symlink_to(other)
  elif case=='outside_ancestor_symlink':
   target=root/'reviews/geometry01';outside=pathlib.Path(tmp)/'external_geometry01';shutil.move(str(target),outside);target.symlink_to(outside,target_is_directory=True)
  else:
   # A copy-only new selection supplies the explicitly requested invalid source.
   # All validation code in add() is unchanged; only a caller is added.
   src=code.read_text();needle='    registry = json.loads(files["SEALS.json"])'
   assert needle in src
   code.write_text(src.replace(needle,'    add("alias_probe.txt", AUDIT / "ordinary_alias" / ".." / "CURRENT_CORRECTIONS.md")\n'+needle))
  p=subprocess.run(['/usr/bin/sandbox-exec','-p','(version 1) (allow default) (deny network*)',str(PY),'-B',str(code)],cwd=pub,env=env,capture_output=True,text=True)
  accepted=p.returncode==0
  if case!='lexical_parent_alias_selection': assert not accepted,(case,p.stdout,p.stderr)
  else: assert accepted,(case,p.stdout,p.stderr)
  row={'case':case,'actual_producer_process':True,'returncode':p.returncode,'invalid_source_rejected':not accepted,'validation_body_changed':False,'copy_only_new_caller':case=='lexical_parent_alias_selection','diagnostic':p.stderr.strip().splitlines()[-1] if p.stderr else 'accepted and generated archive'}
  if accepted:
   import zipfile
   with zipfile.ZipFile(pub/'verification_package.zip') as z:
    n='seshadri_counterexample_verification/alias_probe.txt'
    row.update({'archive_contains_alias_selected_payload':n in z.namelist(),'payload_equals_legitimate_file':z.read(n)==(root/'CURRENT_CORRECTIONS.md').read_bytes(),'archive_members':len(z.infolist())})
  rows.append(row)
(R/'FULL_PRODUCER_CONTROLS.json').write_text(json.dumps({'controls':rows,'scope':'Copied process controls; the lexical alias is supplied by a new copy-only caller. No current production selector supplies this alias, and no current frozen archive leak is alleged.'},indent=2)+'\n')
print(json.dumps(rows,indent=2))
