#!/usr/bin/env python3
"""One disposable extraction; no actual paper compilation or candidate writes."""
from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess,sys,zipfile,zlib
HERE=Path(__file__).resolve().parent;AUDIT=HERE.parent.parent;PACKAGE=AUDIT/'preprint_v1_0';TMP=HERE/'tmp'
def require(c,m):
 if not c:raise ValueError(m)
def sha(data):return hashlib.sha256(data).hexdigest()
def write(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def main():
 require(not TMP.exists(),'inspect existing own scratch before rerun');TMP.mkdir();clean=TMP/'clean';clean.mkdir()
 receipts=[];aliases=[];faults=[];python=sys.executable
 log=HERE/'EXECUTIONS.jsonl';require(not log.exists(),'execution ledger exists; preserve before rerun')
 def run(label,args,expected=0,env=None):
  result=subprocess.run(args,cwd=clean,capture_output=True,text=True,env=env)
  row={'label':label,'argv':args,'cwd':str(clean),'expected_success':expected==0,'returncode':result.returncode,'stdout':result.stdout,'stderr':result.stderr}
  receipts.append(row)
  with log.open('a') as f:f.write(json.dumps(row)+'\n');f.flush()
  require((result.returncode==0)==(expected==0),'unexpected exit '+label)
  if len(receipts)%50==0:print('validated commands',len(receipts),flush=True)
  return row
 def cli(script,*args,optimized=False):return [python,'-I','-B',*(['-O'] if optimized else []),str(script),*args]
 actual_pdf=(PACKAGE/'paper.pdf').read_bytes()
 with zipfile.ZipFile(PACKAGE/'support.zip') as z:z.extractall(clean)
 allow=json.loads((clean/'SUPPORT_ALLOWLIST.json').read_text())['members']
 independent=TMP/'independent.zip'
 with zipfile.ZipFile(independent,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9,strict_timestamps=True) as z:
  for name in allow:
   info=zipfile.ZipInfo(name,date_time=(2026,10,14,0,0,0));info.create_system=3;info.external_attr=0o100644<<16;info.internal_attr=0;info.compress_type=zipfile.ZIP_DEFLATED
   z.writestr(info,(clean/name).read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
 require(independent.read_bytes()==(PACKAGE/'support.zip').read_bytes(),'closed independent ZIP differs')
 run('README stdlib1 verify',cli(clean/'verify_package.py'))
 run('README stdlib2 mathematical checker replay',cli(clean/'run_checks.py','--out-dir','tmp/recheck'))
 run('README stdlib3 build archive',cli(clean/'build_archive.py','--output','tmp/rebuilt.zip'))
 rebuilt=clean/'tmp/rebuilt.zip';require(rebuilt.read_bytes()==independent.read_bytes(),'documented builder differs')
 run('README stdlib4 verify rebuilt',cli(clean/'verify_package.py','--archive','tmp/rebuilt.zip'))
 write(HERE/'CHECKER_REPLAY.json',json.loads((clean/'tmp/recheck/CHECKS.json').read_text()))
 # Unchanged PDF CLI only, explicitly using a disposable fake compiler.
 bindir=clean/'tmp/fakebin';bindir.mkdir();fake=bindir/'tectonic'
 fake.write_text('#!'+python+'\nimport pathlib,sys\nout=pathlib.Path(sys.argv[sys.argv.index("--outdir")+1]);(out/"paper.pdf").write_bytes(b"%PDF-disposable-fake-compiler-CLI-only\\n")\n');fake.chmod(0o755)
 env=os.environ.copy();env['PATH']=str(bindir)+os.pathsep+env.get('PATH','')
 run('README PDF CLI with fake compiler only',cli(clean/'build_pdf.py','--out-dir','tmp/recompiled'),env=env)
 require((clean/'paper.pdf').read_bytes()==actual_pdf,'clean canonical PDF changed')
 # Supply exact excluded current inputs as well, so guards are tested on ALL.
 for name in json.loads((clean/'EXCLUSION_LEDGER.json').read_text())['local_package_files']:
  if name=='support.zip':continue
  target=clean/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(PACKAGE/name,target)
 protected=[p for p in sorted(clean.rglob('*')) if p.is_file() and p.relative_to(clean).parts[0]!='tmp' and p!=clean/'support.zip']
 initial={p.relative_to(clean).as_posix():p.read_bytes() for p in protected}
 def unchanged():
  for name,data in initial.items():require((clean/name).read_bytes()==data,'protected sentinel changed '+name)
 def refresh_manifest():
  manifest=json.loads(initial['SUPPORT_MANIFEST.json'])
  for r in manifest['entries']:
   data=(clean/r['path']).read_bytes();r['bytes']=len(data);r['sha256']=sha(data)
  write(clean/'SUPPORT_MANIFEST.json',manifest)
 folder=clean/'tmp/alias';folder.mkdir()
 representatives=['paper.tex','paper.pdf','metadata.json','publication/release_metadata.json','publication/zenodo.json','publication/DEPOSIT_BINDING.json','OUTPUT_PINS.json','CURRENT_OUTPUT_PINS.json','CURRENT_OUTPUT_PINS_WHOLE03.json','STATUS.json','CURRENT_STATUS.json','CURRENT_STATUS_WHOLE03.json','PREPARATION_REPORT.md','FINAL_VERIFICATION.json','build_archive.py','verify_package.py']
 # Probe the actual unchanged builder and detect ZipFile's writer opening.
 wrapper=clean/'tmp/writer_probe.py';marker=clean/'tmp/writer_opened.txt'
 wrapper.write_text('import pathlib,runpy,sys,zipfile\nmarker=pathlib.Path(sys.argv[1]);script=sys.argv[2];sys.argv=sys.argv[2:]\noriginal=zipfile.ZipFile\ndef probe(*args,**kw):\n mode=kw.get("mode",args[1] if len(args)>1 else "r")\n if mode in ("w","a","x"):marker.write_text("writer opened\\n")\n return original(*args,**kw)\nzipfile.ZipFile=probe\nrunpy.run_path(script,run_name="__main__")\n')
 for optimized in (False,True):
  mode='optimized' if optimized else 'normal'
  # Existing hardlinks to every protected current input, including all history.
  for i,p in enumerate(protected):
   out=folder/'hardlinked.zip';os.link(p,out)
   row=run(mode+' hardlink '+p.relative_to(clean).as_posix(),cli(clean/'build_archive.py','--output',str(out),optimized=optimized),expected=1)
   require('cannot overwrite protected package input ' in row['stderr'],'hardlink failed after guard')
   require(out.read_bytes()==initial[p.relative_to(clean).as_posix()],'hardlink sentinel changed')
   out.unlink();unchanged();aliases.append({'mode':mode,'kind':'hardlink','protected_path':p.relative_to(clean).as_posix(),'all_sentinels_preserved':True})
  for name in representatives:
   p=clean/name
   row=run(mode+' lexical '+name,cli(clean/'build_archive.py','--output',str(p),optimized=optimized),expected=1)
   require('cannot overwrite protected package input ' in row['stderr'],'lexical alias not guarded');unchanged()
   aliases.append({'mode':mode,'kind':'lexical','protected_path':name,'all_sentinels_preserved':True})
   out=folder/'symlink.zip';out.symlink_to(p)
   row=run(mode+' symlink '+name,cli(clean/'build_archive.py','--output',str(out),optimized=optimized),expected=1)
   require('cannot overwrite protected package input ' in row['stderr'],'symlink alias not guarded');out.unlink();unchanged()
   aliases.append({'mode':mode,'kind':'file symlink','protected_path':name,'all_sentinels_preserved':True})
  directory=folder/'publication';directory.symlink_to(clean/'publication',target_is_directory=True)
  row=run(mode+' directory symlink descriptor',cli(clean/'build_archive.py','--output',str(directory/'DEPOSIT_BINDING.json'),optimized=optimized),expected=1)
  require('cannot overwrite protected package input ' in row['stderr'],'directory symlink not guarded');directory.unlink();unchanged()
  absent=clean/'tmp/nonexistent'
  row=run(mode+' nonexistent parent alias',cli(clean/'build_archive.py','--output',str(absent/'../../metadata.json'),optimized=optimized),expected=1)
  require('cannot overwrite protected package input ' in row['stderr'] and not absent.exists(),'parent created before alias rejection');unchanged()
  for name in ['publication/DEPOSIT_BINDING.json','CURRENT_OUTPUT_PINS_WHOLE03.json']:
   out=folder/'writer_probe.zip';os.link(clean/name,out)
   run(mode+' instrumented writer '+name,cli(wrapper,str(marker),str(clean/'build_archive.py'),'--output',str(out),optimized=optimized),expected=1)
   require(not marker.exists(),'writer opened on rejected alias');out.unlink();unchanged()
  # Ordinary archive regeneration and independent tmp outputs remain valid.
  run(mode+' ordinary support.zip regeneration',cli(clean/'build_archive.py','--output','support.zip',optimized=optimized))
  require((clean/'support.zip').read_bytes()==independent.read_bytes(),'ordinary archive differs');unchanged()
  run(mode+' independent tmp archive',cli(clean/'build_archive.py','--output','tmp/independent_output.zip',optimized=optimized))
  require((clean/'tmp/independent_output.zip').read_bytes()==independent.read_bytes(),'tmp archive differs');unchanged()
  run(mode+' strict present binding',cli(clean/'verify_package.py','--require-deposit-binding',optimized=optimized))
  run(mode+' required missing explicit binding',cli(clean/'verify_package.py','--deposit-binding','tmp/no_binding.json','--require-deposit-binding',optimized=optimized),expected=1)
  # Coherent manifests still cannot evade retained stage/integrity guards.
  for name,key,value in [('CURRENT_STATUS_WHOLE03.json','publication_ready',True),('CURRENT_STATUS_WHOLE03.json','whole_package_reviews_completed',3),('CURRENT_STATUS_WHOLE03.json','ascending_publication_hold_after_pr',1033),('CURRENT_STATUS.json','whole_package_reviews_completed',2),('STATUS.json','whole_package_reviews_completed',1)]:
   p=clean/name;d=json.loads(initial[name]);d[key]=value;write(p,d);refresh_manifest()
   run(mode+' coherent retained stage '+name+' '+key,cli(clean/'verify_package.py',optimized=optimized),expected=1)
   p.write_bytes(initial[name]);(clean/'SUPPORT_MANIFEST.json').write_bytes(initial['SUPPORT_MANIFEST.json']);unchanged()
  # Delete exactly the new alias assertion in disposable source, then rehash.
  script=clean/'build_archive.py';text=initial['build_archive.py'].decode();fault=text.replace("v.require(not alias,'cannot overwrite protected package input '+protected.relative_to(root).as_posix())", "v.require(True,'deliberately deleted alias guard')")
  require(fault!=text,'fault mutation had no effect');script.write_text(fault);refresh_manifest()
  descriptor=clean/'publication/DEPOSIT_BINDING.json';out=folder/'fault_descriptor.zip';os.link(descriptor,out)
  row=run(mode+' deliberately deleted archive guard',cli(wrapper,str(marker),str(script),'--output',str(out),optimized=optimized))
  require(marker.exists() and descriptor.read_bytes()!=initial['publication/DEPOSIT_BINDING.json'],'deliberate guard deletion not exposed')
  faults.append({'mode':mode,'coherent_manifest':True,'descriptor_before_sha256':sha(initial['publication/DEPOSIT_BINDING.json']),'descriptor_after_sha256':sha(descriptor.read_bytes()),'writer_opened':True,'destructive_exit_zero':row['returncode']==0})
  out.unlink();marker.unlink();descriptor.write_bytes(initial['publication/DEPOSIT_BINDING.json']);script.write_bytes(initial['build_archive.py']);(clean/'SUPPORT_MANIFEST.json').write_bytes(initial['SUPPORT_MANIFEST.json']);unchanged()
 require((PACKAGE/'paper.pdf').read_bytes()==actual_pdf,'actual canonical PDF changed')
 write(HERE/'GUARD_CONTROL_RECEIPTS.json',{'pass':True,'protected_inputs_tested':len(protected),'hardlink_rejections':2*len(protected),'lexical_and_symlink_representatives':representatives,'alias_cases':aliases,'writer_probes_rejected_without_open':4,'deliberately_deleted_guard_failures':faults,'all_protected_fixture_bytes_restored':True,'concurrent_filesystem_race_claim':False})
 write(HERE/'REPRODUCTION_RECEIPTS.json',{'pass':True,'checked_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_stdlib_README_commands':4,'unchanged_PDF_CLI':'Disposable fake compiler only; no actual paper compilation/render or candidate PDF marker. Fresh whole03 reviewer owns actual compilation.','commands':receipts,'archive':{'members':len(allow),'bytes':independent.stat().st_size,'sha256':sha(independent.read_bytes()),'closed_independent_identical':True,'python':sys.version,'zlib':zlib.ZLIB_VERSION,'zlib_runtime':zlib.ZLIB_RUNTIME_VERSION},'canonical_pdf_unchanged':True,'own_scratch_removed_after_receipts':True})
 shutil.rmtree(TMP)
 print(json.dumps({'pass':True,'commands':len(receipts),'hardlink_rejections':2*len(protected),'protected_inputs':len(protected),'scratch_deleted':True},indent=2))
if __name__=='__main__':main()
