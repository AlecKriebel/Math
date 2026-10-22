import sys
sys.dont_write_bytecode=True
import ast, pathlib,json,hashlib,subprocess,tempfile,shutil,os,re
R=pathlib.Path(__file__).resolve().parent;A=R.parent.parent;C=R/'.cache';E=C/'extracted';BASE=C/'unrelated_cache/scratch/standalone_audit';PYTHON=A/'root_reproduction/.cache/venv/bin/python';SB=['/usr/bin/sandbox-exec','-p','(version 1) (allow default) (deny network*)'];ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(C/'tmp'))
sha=lambda b:hashlib.sha256(b).hexdigest()
rows=[]
# Use copied real producer processes. Never patch guard; only supply a caller when required.
for case in ['cache','sources','scratch','qa','secrets','private','case_CACHE','case_SOURCES','case_SCRATCH','case_QA','case_SECRETS','case_PRIVATE','lexical_parent','archive_parent','archive_absolute','duplicate','leaf_symlink','outside_ancestor','resolved_excluded']:
 with tempfile.TemporaryDirectory(dir=C/'tmp') as td:
  audit=pathlib.Path(td)/'audit';shutil.copytree(BASE,audit);pub=audit/'publication';code=pub/'make_package.py';newcaller=False
  components={'cache':'.cache','sources':'sources','scratch':'scratch','qa':'qa','secrets':'.secrets','private':'p.private.payload'}
  if case.startswith('case_'):
   comp={'CACHE':'.cache','SOURCES':'sources','SCRATCH':'scratch','QA':'qa','SECRETS':'.secrets','PRIVATE':'.private'}[case[5:]]
   target=audit/'reviews/geometry01';dest=audit/comp/'kept_geometry';dest.parent.mkdir();shutil.move(str(target),dest);alias=audit/comp.upper()/'kept_geometry';assert alias.samefile(dest);target.symlink_to(alias,target_is_directory=True)
  elif case in components:
   comp=components[case];f=audit/'reviews/geometry01'/comp/'probe';f.parent.mkdir(parents=True);f.write_text('excluded')
   seal=audit/'reviews/geometry01/SHA256SUMS';seal.write_text(seal.read_text()+sha(f.read_bytes())+'  '+comp+'/probe\n')
  elif case=='lexical_parent':
   (audit/'aliasdir').mkdir();call='add("alias_probe", AUDIT / "aliasdir" / ".." / "CURRENT_CORRECTIONS.md")';newcaller=True
  elif case in ['archive_parent','archive_absolute']:
   call='add('+repr('../probe' if case=='archive_parent' else '/probe')+', AUDIT / "CURRENT_CORRECTIONS.md")';newcaller=True
  elif case=='duplicate':
   call='add("CURRENT_CORRECTIONS.md", AUDIT / "CURRENT_CORRECTIONS.md")';newcaller=True
  elif case=='leaf_symlink':
   f=audit/'CURRENT_CORRECTIONS.md';g=audit/'allowed_copy';g.write_bytes(f.read_bytes());f.unlink();f.symlink_to(g)
  elif case=='outside_ancestor':
   f=audit/'reviews/geometry01';dest=pathlib.Path(td)/'external';shutil.move(str(f),dest);f.symlink_to(dest,target_is_directory=True)
  else:
   f=audit/'reviews/geometry01';dest=audit/'.cache/geometry';dest.parent.mkdir();shutil.move(str(f),dest);f.symlink_to(dest,target_is_directory=True)
  if newcaller:
   source=code.read_text();needle='    registry = json.loads(files["SEALS.json"])';assert needle in source;code.write_text(source.replace(needle,'    '+call+'\n'+needle))
  proc=subprocess.run(SB+[str(PYTHON),'-B',str(code)],cwd=pub,env=ENV,capture_output=True,text=True)
  assert proc.returncode!=0,(case,proc.stdout,proc.stderr)
  rows.append({'case':case,'actual_process_rejected':True,'returncode':proc.returncode,'producer_guard_body_unchanged':True,'new_caller_in_copy_only':newcaller,'diagnostic':proc.stderr.strip().splitlines()[-1]})
# Compile exact AST guard too, to separately test malformed lexical names before file I/O.
source=(BASE/'publication/make_package.py').read_text();module=ast.parse(source);main=next(n for n in module.body if isinstance(n,ast.FunctionDef) and n.name=='main');add=next(n for n in main.body if isinstance(n,ast.FunctionDef) and n.name=='add')
sys.path.insert(0,str(E));from integrity import safe_path
ns={'AUDIT':BASE,'safe_path':safe_path,'files':{}};exec(compile(ast.Module(body=[add],type_ignores=[]),'exact_add_guard','exec'),ns)
guards=[]
for name in ['a/../x','a//x','./x','x\\y','C:x','a/.CACHE/x','a/contains.PRIVATE/x','../x','/x']:
 try:ns['add'](name,BASE/'CURRENT_CORRECTIONS.md')
 except (RuntimeError,ValueError,OSError) as err:guards.append({'archive_name':name,'rejected':True,'diagnostic':str(err)})
 else:raise RuntimeError('Unsafe alias accepted: '+name)
mutants=[]
for case in ['changed_payload','extra_payload','missing_payload','symlink','changed_resealed_original_snapshot_and_outer','changed_resealed_historical_release_manifest_snapshot_outer','changed_resealed_expected_result']:
 with tempfile.TemporaryDirectory(dir=C/'tmp') as td:
  cp=pathlib.Path(td)/'packet';shutil.copytree(E,cp);outer=json.loads((cp/'MANIFEST.json').read_bytes());changed=[]
  if case=='changed_payload':(cp/'CURRENT_CORRECTIONS.md').write_text('changed')
  elif case=='extra_payload':(cp/'EXTRA').write_text('extra')
  elif case=='missing_payload':(cp/'CURRENT_CORRECTIONS.md').unlink()
  elif case=='symlink':(cp/'EXTRA_LINK').symlink_to(cp/'CURRENT_CORRECTIONS.md')
  elif case=='changed_resealed_expected_result':
   n='root_reproduction/ORIGINAL_STRICT_BASELINE.json';f=cp/n;obj=json.loads(f.read_bytes());obj['limits']='false changed expectation';f.write_text(json.dumps(obj)+'\n');changed=[n]
  else:
   snap=json.loads((cp/'ORIGINAL_SNAPSHOT.json').read_bytes());suffix='/author/PROOF.md' if 'original_snapshot' in case else '/RELEASE_MANIFEST.json';rec=next(x for x in snap['files'] if x['path'].endswith(suffix));n='original/'+rec['path'];f=cp/n;f.write_bytes(f.read_bytes()+b'\n');rec['size']=f.stat().st_size;rec['sha256']=sha(f.read_bytes());(cp/'ORIGINAL_SNAPSHOT.json').write_text(json.dumps(snap,indent=2)+'\n');changed=[n,'ORIGINAL_SNAPSHOT.json']
  if changed:
   for n in changed:outer['files'][n]={'bytes':(cp/n).stat().st_size,'sha256':sha((cp/n).read_bytes())}
   (cp/'MANIFEST.json').write_text(json.dumps(outer,indent=2)+'\n')
  proc=subprocess.run(SB+[str(PYTHON),'-B',str(cp/'run_all.py')],cwd=cp,env=ENV,capture_output=True,text=True);assert proc.returncode!=0,(case,proc.stdout)
  diag=proc.stderr.strip().splitlines()[-1]
  if 'snapshot' in case or 'historical_release' in case:assert 'Original snapshot binding differs' in diag,diag
  if case=='changed_resealed_expected_result':assert 'Complete JSON mismatch: verify_original_snapshot.py' in diag,diag
  mutants.append({'case':case,'actual_process_rejected':True,'diagnostic':diag,'returncode':proc.returncode,'jobs_before_failure':len(proc.stdout.splitlines())})
# Separate interpretation: original integrity8 and snapshot4 are actual copied mutations; formula10 are comparisons.
result={'status':'PASS','producer_sha256':sha((BASE/'publication/make_package.py').read_bytes()),'producer_process_controls':rows,'exact_guard_ast_controls':guards,'package_process_mutations':mutants,'original_integrity_mutations_executed_by_nine_job_driver':8,'snapshot_gate_mutations_executed_by_nine_job_driver':4,'pencil_formula_units_are_not_process_mutations':10,'limits':'The guard and replay tests establish rejection/integrity relative to known bytes, not semantic authorship, authenticity, geometry or priority.'}
(R/'ATTACK_LEDGER.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','producer_cases':len(rows),'AST_cases':len(guards),'package_mutants':len(mutants)},indent=2))
