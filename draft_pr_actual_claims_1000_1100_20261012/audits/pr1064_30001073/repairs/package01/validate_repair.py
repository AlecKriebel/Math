#!/usr/bin/env python3
"""Reproduce bounded package repair controls using one disposable extraction.

Writes only its own tmp tree and authored receipt files. Does not compile in or
overwrite the candidate; the actual README compiler runs in a clean extraction.
"""
from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess,sys,zipfile,zlib
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent.parent
PACKAGE=AUDIT/'preprint_v1_0'
SCRATCH=HERE/'tmp'
def require(c,m):
 if not c:raise ValueError(m)
def sha(data):return hashlib.sha256(data).hexdigest()
def write(path,data):path.write_text(json.dumps(data,indent=2)+'\n')
def main():
 require(not SCRATCH.exists(),'own scratch already exists; inspect before removal')
 SCRATCH.mkdir();clean=SCRATCH/'clean';clean.mkdir()
 receipts=[];alias_receipts=[];fault_receipts=[]
 def run(label,argv,cwd,expected=0,env=None):
  proc=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,env=env)
  row={'label':label,'argv':argv,'cwd':str(cwd),'returncode':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr}
  receipts.append(row)
  require((proc.returncode==0)==(expected==0),'unexpected exit '+label)
  return row
 python=sys.executable
 def cli(script,*args,optimized=False):return [python,'-I','-B',*(['-O'] if optimized else []),str(script),*args]
 protected_pdf=PACKAGE/'paper.pdf';pdf_before=protected_pdf.read_bytes()
 with zipfile.ZipFile(PACKAGE/'support.zip') as z:z.extractall(clean)
 # A closed independent builder, not an import of the supplied code.
 allow=json.loads((PACKAGE/'SUPPORT_ALLOWLIST.json').read_text())['members']
 independent=SCRATCH/'independent.zip'
 with zipfile.ZipFile(independent,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9,strict_timestamps=True) as z:
  for name in allow:
   info=zipfile.ZipInfo(name,date_time=(2026,10,14,0,0,0));info.create_system=3;info.external_attr=0o100644<<16;info.internal_attr=0;info.compress_type=zipfile.ZIP_DEFLATED
   z.writestr(info,(PACKAGE/name).read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
 require(independent.read_bytes()==(PACKAGE/'support.zip').read_bytes(),'independent closed ZIP differs')
 archive_receipt={'closed_independent_identical':True,'bytes':independent.stat().st_size,'sha256':sha(independent.read_bytes()),'members':len(allow),'python':sys.version,'zlib':zlib.ZLIB_VERSION,'zlib_runtime':zlib.ZLIB_RUNTIME_VERSION}
 # Execute the actual README positive sequence from the clean extraction.
 run('README verify',cli(clean/'verify_package.py'),clean)
 run('README mathematical checkers',cli(clean/'run_checks.py','--out-dir','tmp/recheck'),clean)
 run('README build ZIP',cli(clean/'build_archive.py','--output','tmp/rebuilt.zip'),clean)
 rebuilt=clean/'tmp/rebuilt.zip'
 require(rebuilt.read_bytes()==(PACKAGE/'support.zip').read_bytes(),'supplied clean ZIP rebuild differs')
 run('README verify rebuilt',cli(clean/'verify_package.py','--archive','tmp/rebuilt.zip'),clean)
 run('README safe actual PDF compilation',cli(clean/'build_pdf.py','--out-dir','tmp/recompiled'),clean)
 require((clean/'paper.pdf').read_bytes()==pdf_before,'clean canonical PDF changed')
 export=clean/'tmp/recompiled/paper.pdf'
 require(export.read_bytes().startswith(b'%PDF-'),'safe export lacks PDF signature')
 archive_receipt['safe_actual_export']={'bytes':export.stat().st_size,'sha256':sha(export.read_bytes()),'scope':'Disposable safe-output compilation only; no new canonical PDF/layout validation claim.'}
 checker_report=json.loads((clean/'tmp/recheck/CHECKS.json').read_text())
 write(HERE/'CHECKER_REPLAY.json',checker_report)
 # Both modes check binding and retained integrity gates.
 manifest_file=clean/'SUPPORT_MANIFEST.json';initial_manifest=manifest_file.read_bytes()
 def refresh_manifest():
  d=json.loads(initial_manifest)
  for rec in d['entries']:
   data=(clean/rec['path']).read_bytes();rec['bytes']=len(data);rec['sha256']=sha(data)
  write(manifest_file,d)
 def fault_file(label,path,change,optimized):
  f=clean/path;old=f.read_bytes();change(f);refresh_manifest()
  run(label,cli(clean/'verify_package.py',optimized=optimized),clean,expected=1)
  f.write_bytes(old);manifest_file.write_bytes(initial_manifest)
 for optimized in (False,True):
  mode='optimized' if optimized else 'normal'
  run(mode+' clean absent binding',cli(clean/'verify_package.py',optimized=optimized),clean)
  run(mode+' required absent binding',cli(clean/'verify_package.py','--require-deposit-binding',optimized=optimized),clean,expected=1)
  run(mode+' strict external binding',cli(clean/'verify_package.py','--archive',str(rebuilt),'--deposit-binding',str(PACKAGE/'publication/DEPOSIT_BINDING.json'),'--require-deposit-binding',optimized=optimized),clean)
  bad=clean/'tmp/bad_binding.json';write(bad,{'schema_version':1})
  run(mode+' malformed explicit binding',cli(clean/'verify_package.py','--deposit-binding',str(bad),optimized=optimized),clean,expected=1)
  default=clean/'publication/DEPOSIT_BINDING.json';default.write_bytes(bad.read_bytes())
  run(mode+' malformed default binding',cli(clean/'verify_package.py',optimized=optimized),clean,expected=1);default.unlink()
  extra=clean/'UNMANIFESTED.txt';extra.write_text('deliberate extra\n')
  run(mode+' unmanifested file',cli(clean/'verify_package.py',optimized=optimized),clean,expected=1);extra.unlink()
  readme=clean/'README.md';readme_old=readme.read_bytes();readme.write_bytes(readme_old+b'fault\n')
  run(mode+' member hash corruption',cli(clean/'verify_package.py',optimized=optimized),clean,expected=1);readme.write_bytes(readme_old)
  traversal=clean/'tmp/traversal.zip'
  with zipfile.ZipFile(traversal,'w') as z:z.writestr('../escape.txt','fault')
  run(mode+' traversal ZIP',cli(clean/'verify_package.py','--archive',str(traversal),optimized=optimized),clean,expected=1)
  run(mode+' missing explicit ZIP',cli(clean/'verify_package.py','--archive',str(clean/'tmp/missing.zip'),optimized=optimized),clean,expected=1)
  def edit_json(f,key,value):
   d=json.loads(f.read_text());d[key]=value;write(f,d)
  fault_file(mode+' coherent old dated stage gate','STATUS.json',lambda f:edit_json(f,'whole_package_reviews_completed',1),optimized)
  fault_file(mode+' coherent current readiness gate','CURRENT_STATUS.json',lambda f:edit_json(f,'publication_ready',True),optimized)
  fault_file(mode+' coherent current review count gate','CURRENT_STATUS.json',lambda f:edit_json(f,'whole_package_reviews_completed',2),optimized)
  fault_file(mode+' coherent current hold gate','CURRENT_STATUS.json',lambda f:edit_json(f,'ascending_publication_hold_after_pr',1033),optimized)
  def badcopy(f):
   d=json.loads(f.read_text());d['copies'][0]['sha256']='0'*64;write(f,d)
  fault_file(mode+' coherent copy-map mismatch','COPY_MAP.json',badcopy,optimized)
  def badsafe(f):
   d=json.loads(f.read_text());d['records']=d['records'][:-1];write(f,d)
  fault_file(mode+' coherent selected-pin mismatch','SAFE_INPUT_PINS.json',badsafe,optimized)
  # Same-byte and malformed self-manifest symlinks must reject before JSON read.
  for malformed in (False,True):
   target=clean/'tmp/manifest_target.json';target.write_bytes(b'not-json' if malformed else initial_manifest)
   manifest_file.unlink();manifest_file.symlink_to(target)
   row=run(mode+(' malformed' if malformed else ' same-byte')+' self-manifest symlink',cli(clean/'verify_package.py',optimized=optimized),clean,expected=1)
   require('missing/symlink member SUPPORT_MANIFEST.json' in row['stderr'],'manifest guard did not run before load')
   manifest_file.unlink();manifest_file.write_bytes(initial_manifest)
  # Allowlist bootstrap must also reject same bytes via a symlink.
  al=clean/'SUPPORT_ALLOWLIST.json';old=al.read_bytes();target=clean/'tmp/allowlist_target.json';target.write_bytes(old);al.unlink();al.symlink_to(target)
  row=run(mode+' allowlist symlink',cli(clean/'verify_package.py',optimized=optimized),clean,expected=1)
  require('missing/symlink member SUPPORT_ALLOWLIST.json' in row['stderr'],'allowlist bootstrap failed')
  al.unlink();al.write_bytes(old)
  # Existing regular members reached through symlink ancestry remain rejected.
  history=clean/'support/history';back=clean/'tmp/history_back';history.rename(back);history.symlink_to(back,target_is_directory=True)
  row=run(mode+' symlink member ancestry',cli(clean/'verify_package.py',optimized=optimized),clean,expected=1)
  require('symlink in member ancestry' in row['stderr'],'ancestry guard missing')
  history.unlink();back.rename(history)
  # A deliberate reintroduction of P3-02 is accepted only by the faulty variant.
  verifier=clean/'verify_package.py';old=verifier.read_bytes()
  changed=old.decode().replace('for name in allow:local_regular(name)',"for name in allow:\n  if name!='SUPPORT_MANIFEST.json':local_regular(name)")
  require(changed!=old.decode(),'fault mutation had no effect');verifier.write_text(changed);refresh_manifest()
  coherent=manifest_file.read_bytes();target=clean/'tmp/coherent_fault_manifest.json';target.write_bytes(coherent);manifest_file.unlink();manifest_file.symlink_to(target)
  row=run(mode+' deliberate manifest-guard deletion',cli(clean/'verify_package.py',optimized=optimized),clean)
  fault_receipts.append({'mode':mode,'fault':'skip self-manifest preflight','coherent_manifest':True,'vulnerability_observed':row['returncode']==0})
  manifest_file.unlink();manifest_file.write_bytes(initial_manifest);verifier.write_bytes(old)
 # PDF alias tests use a fake compiler and an isolated canonical sentinel.
 probe=clean/'tmp/pdf_probe';probe.mkdir();script=probe/'build_pdf.py';script.write_bytes((PACKAGE/'build_pdf.py').read_bytes());(probe/'paper.tex').write_text('disposable CLI fixture\n')
 canonical=probe/'paper.pdf';sentinel=b'%PDF-SENTINEL: DO NOT OVERWRITE\n';canonical.write_bytes(sentinel)
 bindir=probe/'bin';bindir.mkdir();fake=bindir/'tectonic';marker=probe/'compiler_called.txt'
 fake.write_text('#!'+python+'\nimport pathlib,sys\nroot=pathlib.Path(__file__).resolve().parent.parent\n(root/"compiler_called.txt").write_text("called\\n")\nout=pathlib.Path(sys.argv[sys.argv.index("--outdir")+1]);(out/"paper.pdf").write_bytes(b"%PDF-fake-safe-export\\n")\n');fake.chmod(0o755)
 env=os.environ.copy();env['PATH']=str(bindir)+os.pathsep+env.get('PATH','')
 aliasdir=probe/'directory_alias';aliasdir.symlink_to(probe,target_is_directory=True)
 filed=probe/'file_alias';filed.mkdir();(filed/'paper.pdf').symlink_to(canonical)
 hardd=probe/'hardlink_alias';hardd.mkdir();os.link(canonical,hardd/'paper.pdf')
 aliases=[('.', 'dot'),(str(probe),'absolute root'),('nonexistent/..','nonexistent-parent alias'),('directory_alias','directory symlink'),('file_alias','file symlink'),('hardlink_alias','existing hardlink')]
 for optimized in (False,True):
  mode='optimized' if optimized else 'normal'
  for destination,label in aliases:
   if marker.exists():marker.unlink()
   row=run(mode+' PDF '+label,cli(script,'--out-dir',destination,optimized=optimized),probe,expected=1,env=env)
   require(canonical.read_bytes()==sentinel and not marker.exists(),'alias reached compiler or changed sentinel')
   require('aliases canonical paper.pdf' in row['stderr'],'wrong alias rejection')
   require(not (probe/'nonexistent').exists(),'alias rejection created a directory')
   alias_receipts.append({'mode':mode,'alias':label,'canonical_sentinel_unchanged':True,'compiler_never_invoked':True,'directory_created':False})
  if marker.exists():marker.unlink()
  safe=probe/('safe_'+mode)
  run(mode+' PDF safe fake-compiler path',cli(script,'--out-dir',str(safe),optimized=optimized),probe,env=env)
  require(marker.exists() and canonical.read_bytes()==sentinel and (safe/'paper.pdf').read_bytes()==b'%PDF-fake-safe-export\n','safe path failed')
  # Deliberately remove P3-01 guard only in this disposable fixture.
  old=script.read_bytes();fault=old.decode().replace('if target.resolve()==canonical.resolve() or (target.exists() and canonical.exists() and target.samefile(canonical)):', 'if False:')
  require(fault!=old.decode(),'PDF fault mutation had no effect');script.write_text(fault);marker.unlink()
  run(mode+' deliberate PDF-guard deletion',cli(script,'--out-dir','.',optimized=optimized),probe,env=env)
  require(marker.exists() and canonical.read_bytes()!=sentinel,'PDF fault was not observed')
  fault_receipts.append({'mode':mode,'fault':'delete PDF alias guard','sentinel_overwrite_observed':True,'compiler_invoked':True})
  script.write_bytes(old);canonical.write_bytes(sentinel)
 require(protected_pdf.read_bytes()==pdf_before,'actual canonical PDF changed')
 for optimized in (False,True):
  run(('optimized' if optimized else 'normal')+' final actual strict verification',cli(PACKAGE/'verify_package.py','--require-deposit-binding',optimized=optimized),PACKAGE)
 write(HERE/'REPRODUCTION_RECEIPTS.json',{'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pass':True,'actual_README_commands':5,'archive':archive_receipt,'commands':receipts,'canonical_pdf_unchanged':True,'scratch_scope':'One new disposable extraction only; removed after receipts captured.'})
 write(HERE/'GUARD_CONTROL_RECEIPTS.json',{'pass':True,'pdf_rejected_aliases':alias_receipts,'deliberate_faults_observed':fault_receipts,'normal_and_optimized':True,'original_checker_optimized_claim':False,'manifest_symlink_guard_before_json_read':True,'allowlist_bootstrap_and_ancestry_checked':True})
 shutil.rmtree(SCRATCH)
 print(json.dumps({'pass':True,'commands':len(receipts),'alias_rejections':len(alias_receipts),'independent_archive_identical':True,'scratch_deleted':True},indent=2))
if __name__=='__main__':main()
