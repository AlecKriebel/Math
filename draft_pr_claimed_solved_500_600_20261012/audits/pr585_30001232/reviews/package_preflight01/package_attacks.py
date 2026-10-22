import ast, hashlib, json, os, pathlib, shutil, subprocess, sys, tempfile
R=pathlib.Path(__file__).resolve().parent; A=R.parent.parent; C=R/'.cache'; E=C/'extracted'
PY=A/'root_reproduction/.cache/venv/bin/python'
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(C/'tmp'))
sha=lambda b: hashlib.sha256(b).hexdigest()
# Rebuild with the real, unmodified producer in an unrelated ancestor named cache/scratch.
D=C/'cache/scratch/copied_audit'; P=D/'publication'; P.mkdir(parents=True,exist_ok=False)
for path in E.rglob('*'):
 if path.is_file():
  n=path.relative_to(E)
  # Flat publication selections are installed into their repository layout.
  if len(n.parts)==1 and n.name in {'seshadri_counterexample.tex','README.md','CORRECTIONS.md','BUILD.json','PDF_QA.json','requirements.txt','integrity.py','run_all.py','make_package.py','JOBS.json','SEALS.json'}:
   target=P/n
  elif n.as_posix()=='metadata.json': target=P/'zenodo-deposit.json'
  elif n.as_posix()=='MANIFEST.json': continue
  else: target=D/n
  target.parent.mkdir(parents=True,exist_ok=True); target.write_bytes(path.read_bytes())
(P/'seshadri_counterexample.pdf').write_bytes((A/'publication/seshadri_counterexample.pdf').read_bytes())
proc=subprocess.run(['/usr/bin/sandbox-exec','-p','(version 1) (allow default) (deny network*)',str(PY),'-B',str(P/'make_package.py')],env=ENV,capture_output=True,text=True)
assert proc.returncode==0,(proc.stdout,proc.stderr)
assert (P/'verification_package.zip').read_bytes()==(A/'publication/verification_package.zip').read_bytes()
producer={'status':'PASS','bytes_identical_zip':True,'sha256':sha((P/'verification_package.zip').read_bytes()),'unrelated_cache_scratch_ancestor_allowed':True,'os_network_denied':True,'summary':json.loads(proc.stdout)}
# Compile the exact nested source guard as a test callable. Its body is unchanged.
source=(P/'make_package.py').read_text(); mod=ast.parse(source)
main=next(n for n in mod.body if isinstance(n,ast.FunctionDef) and n.name=='main')
add=next(n for n in main.body if isinstance(n,ast.FunctionDef) and n.name=='add')
sys.path.insert(0,str(P)); from integrity import safe_path
namespace={'AUDIT':D,'safe_path':safe_path,'files':{}}
exec(compile(ast.Module(body=[add],type_ignores=[]),'exact_producer_add_guard','exec'),namespace)
fn=namespace['add']; guard=[]
def test(label,name,path,want_reject):
 namespace['files']={}
 try: fn(name,path)
 except (RuntimeError,OSError,ValueError) as e: rejected=True; reason=str(e)
 else: rejected=False; reason='accepted'
 guard.append({'case':label,'archive_name':name,'source_relative_lexical':str(path.relative_to(D)) if path.is_relative_to(D) else str(path),'expected_reject':want_reject,'rejected':rejected,'expectation_met':rejected==want_reject,'result':reason})
regular=D/'CURRENT_CORRECTIONS.md'
test('allowed_source','probe.txt',regular,False)
for comp in ['.cache','sources','scratch','qa','.secrets','contains.private.data']:
 q=D/comp/'probe.txt';q.parent.mkdir(parents=True,exist_ok=True);q.write_text('excluded')
 test('excluded_source_'+comp,'probe.txt',q,True)
for name in ['../probe','/probe','a/../probe','a//probe','./probe','a\\probe','C:probe']:
 test('unsafe_archive_'+name,name,regular,True)
link=D/'probe_link';link.symlink_to(regular)
test('leaf_symlink','probe.txt',link,True)
outside=C/'outside_producer.txt';outside.write_text('out of audit')
test('escape_source','probe.txt',outside,True)
via=D/'through_link';via.symlink_to(outside)
test('symlink_escape','probe.txt',via,True)
# An ancestor symlink into an excluded path must be rejected after resolution.
alias=D/'source_alias';alias.symlink_to(D/'sources',target_is_directory=True)
test('resolved_excluded_source','probe.txt',alias/'probe.txt',True)
(D/'ordinary_alias').mkdir()
test('lexical_parent_alias_inside_audit','probe.txt',D/'ordinary_alias/../CURRENT_CORRECTIONS.md',True)
namespace['files']={};fn('probe.txt',regular)
try: fn('probe.txt',regular)
except RuntimeError: guard.append({'case':'duplicate_archive_path','rejected':True,'expected_reject':True,'expectation_met':True})
else: raise RuntimeError('duplicate accepted')
# Independently mutate frozen extraction copies and actually run the full entrypoint.
mutations=[]
for case in ['changed_payload','missing_payload','extra_payload','symlink_payload','changed_original_resealed_snapshot_and_outer','changed_expected_job_result_resealed_outer']:
 with tempfile.TemporaryDirectory(dir=C/'tmp') as tmp:
  cp=pathlib.Path(tmp)/'package';shutil.copytree(E,cp)
  if case=='changed_payload': (cp/'CURRENT_CORRECTIONS.md').write_bytes((cp/'CURRENT_CORRECTIONS.md').read_bytes()+b'changed')
  elif case=='missing_payload': (cp/'CURRENT_CORRECTIONS.md').unlink()
  elif case=='extra_payload': (cp/'EXTRA').write_text('extra')
  elif case=='symlink_payload': (cp/'EXTRA_LINK').symlink_to(cp/'CURRENT_CORRECTIONS.md')
  elif case=='changed_original_resealed_snapshot_and_outer':
   snap=json.loads((cp/'ORIGINAL_SNAPSHOT.json').read_bytes());rec=next(r for r in snap['files'] if r['path'].endswith('/author/PROOF.md')); f=cp/'original'/rec['path'];f.write_bytes(f.read_bytes()+b'changed');rec['size']=f.stat().st_size;rec['sha256']=sha(f.read_bytes());(cp/'ORIGINAL_SNAPSHOT.json').write_text(json.dumps(snap,indent=2)+'\n')
   # Re-seal all changed outer records, defeating mere internal consistency.
   mf=json.loads((cp/'MANIFEST.json').read_bytes())
   for n in ['ORIGINAL_SNAPSHOT.json','original/'+rec['path']]:mf['files'][n]={'bytes':(cp/n).stat().st_size,'sha256':sha((cp/n).read_bytes())}
   (cp/'MANIFEST.json').write_text(json.dumps(mf,indent=2)+'\n')
  else:
   job=json.loads((cp/'JOBS.json').read_bytes())[0];f=cp/job['record'];obj=json.loads(f.read_bytes());obj['method']='altered expected result';f.write_text(json.dumps(obj)+'\n')
   # Remove seal obstacle solely in this copy so this test reaches JSON replay comparison.
   # Instead of modifying production code, mutate an unsealed recorded strict gate output.
   shutil.rmtree(cp);shutil.copytree(E,cp)
   n='root_reproduction/ORIGINAL_STRICT_BASELINE.json';f=cp/n;obj=json.loads(f.read_bytes());obj['limits']='altered expected result';f.write_text(json.dumps(obj)+'\n')
   mf=json.loads((cp/'MANIFEST.json').read_bytes());mf['files'][n]={'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())};(cp/'MANIFEST.json').write_text(json.dumps(mf,indent=2)+'\n')
  p=subprocess.run(['/usr/bin/sandbox-exec','-p','(version 1) (allow default) (deny network*)',str(PY),'-B',str(cp/'run_all.py')],env=ENV,cwd=cp,capture_output=True,text=True)
  assert p.returncode!=0,(case,p.stdout,p.stderr)
  reason=p.stderr.strip().splitlines()[-1]
  if case=='changed_original_resealed_snapshot_and_outer': assert 'Original snapshot binding differs' in reason
  if case=='changed_expected_job_result_resealed_outer': assert 'Complete JSON mismatch: verify_original_snapshot.py' in reason
  mutations.append({'case':case,'actual_process_rejected':True,'returncode':p.returncode,'reason':reason,'completed_jobs_before_rejection':len(p.stdout.splitlines())})
result={'producer_rebuild':producer,'guard_source_sha256':sha((P/'make_package.py').read_bytes()),'exact_nested_add_AST_used_without_body_changes':True,'source_guard_cases':guard,'source_guard_expectation_failures':[v for v in guard if not v['expectation_met']],'actual_package_mutations':mutations,'tests_do_not_establish_authenticity':True}
(R/'PACKAGE_ATTACKS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'producer':producer,'guard_failures':result['source_guard_expectation_failures'],'package_mutations':mutations},indent=2))
