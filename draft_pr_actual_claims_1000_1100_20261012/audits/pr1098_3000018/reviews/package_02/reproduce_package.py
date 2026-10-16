"""Independent actual unchanged external package execution; no runtime redirection."""
from pathlib import Path
import json,sys,hashlib,subprocess,zipfile,uuid,os,shutil,datetime
R=Path(__file__).resolve().parent;A=R.parents[1];C=A/'preprint_v1_0'
T=Path('/private/tmp')/('pr1098-whole02-'+str(uuid.uuid4()));T.mkdir();records=[];cleanup=[]
def need(x,s):
 if not x:raise ValueError(s)
def dg(b):return hashlib.sha256(b).hexdigest()
def save(n,o):(R/n).write_text(json.dumps(o,sort_keys=True,indent=2)+'\n')
def run(args,expected=0):
 p=subprocess.run(list(map(str,args)),capture_output=True,text=True)
 row={'argv':list(map(str,args)),'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr};records.append(row);save('ACTUAL_COMMANDS.json',{'external_root':str(T),'commands':records,'runtime_ROOT_or_ORIGINAL_modified':False})
 need((p.returncode==0) if expected==0 else p.returncode!=0,'unexpected exit: '+str(args)+'\n'+p.stderr);return p

def cleanup_tree(path):
 pins=[{'path':str(p.relative_to(path)),'bytes':p.stat().st_size,'sha256':dg(p.read_bytes())} for p in sorted(path.rglob('*')) if p.is_file() and not p.is_symlink()]
 cleanup.append({'absolute_path':str(path),'regular_files_before_removal':pins,'only_owned_unsealed_derivatives':True})
 save('EXTERNAL_CLEANUP.json',{'trees':cleanup,'removed':False});shutil.rmtree(path)
 save('EXTERNAL_CLEANUP.json',{'trees':cleanup,'removed':True})

try:
 kit=T/'kit';kit.mkdir()
 with zipfile.ZipFile(C/'pr1098_support_v1_0.zip') as z:
  names=z.namelist();need(len(names)==len(set(names))==102,'102 unique members')
  need(all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in names),'safe names')
  z.extractall(kit)
 for n in ('paper.pdf','pr1098_support_v1_0.zip'):shutil.copyfile(C/n,kit/n)
 initial={str(p.relative_to(kit)):dg(p.read_bytes()) for p in kit.rglob('*') if p.is_file()}
 outcomes=[];builds=[]
 for opt in (False,True):
  cmd=[sys.executable]+(['-O'] if opt else [])+['-B']
  run(cmd+[kit/'code/verify_kit.py'])
  ck=run(cmd+[kit/'code/run_checks.py']);save('CANDIDATE_CHECKS_'+('optimized' if opt else 'normal')+'.json',json.loads(ck.stdout));outcomes.append(ck.stdout)
  run(cmd+[kit/'code/run_checks.py','--invalid'],1)
  arc=T/('rebuilt-'+str(opt)+'.zip');run(cmd+[kit/'code/rebuild_archive.py','--output',arc]);need(arc.read_bytes()==(C/'pr1098_support_v1_0.zip').read_bytes(),'actual archive bytes')
  out=T/('build-'+str(opt))
  try:
   bp=run(cmd+[kit/'code/build_pdf.py','--out-dir',out])
   need((out/'paper.pdf').read_bytes()==(C/'paper.pdf').read_bytes(),'actual PDF byte equality')
   builds.append({'optimized':opt,'success':True,'canonical_bytes_equal':True,'compiler_version':subprocess.check_output(['tectonic','--version'],text=True).strip(),'stdout':bp.stdout,'log':(out/'paper.log').read_text(errors='replace')})
  except Exception as e:
   builds.append({'optimized':opt,'success':False,'exception':repr(e),'stderr':(out/'compiler.stderr').read_text(errors='replace') if (out/'compiler.stderr').exists() else None})
   save('ACTUAL_BUILDS.json',builds)
   raise
  save('ACTUAL_BUILDS.json',builds)
  cleanup_tree(out)
 need(outcomes[0]==outcomes[1],'complete candidate JSON normal/O equality')
 # Unmodified extracted input and output guards. Each fault is individually restored.
 existing=T/'keep';existing.write_bytes(b'existing bytes retained')
 existingdir=T/'keepdir';existingdir.mkdir();symlink=T/'sym';symlink.symlink_to(existing);broken=T/'broken';broken.symlink_to(T/'absent')
 parentlink=T/'kitlink';parentlink.symlink_to(kit,target_is_directory=True)
 hard=T/'hard';os.link(existing,hard)
 targets=[existing,existingdir,symlink,broken,parentlink/'new',kit/'new',A/'whole02-must-not-create',T/'x'/'..'/'new',Path('relative-output'),hard]
 # Physical case aliases really exist on the current filesystem.
 alias=Path(str(kit).upper())
 same=alias.exists() and os.path.samefile(alias,kit)
 if same:targets.append(alias/'new')
 faults=[]
 for opt in (False,True):
  cmd=[sys.executable]+(['-O'] if opt else [])+['-B']
  for writer,flag in [('rebuild_archive.py','--output'),('build_pdf.py','--out-dir')]:
   for target in targets:
    run(cmd+[kit/'code'/writer,flag,target],1);faults.append({'optimized':opt,'writer':writer,'output':str(target),'rejected':True})
  # Source-level load bootstrap protections, before parsing, including symlinked ancestors.
  for inputname in ['MANIFEST.json','ARTIFACT_BINDINGS.json','metadata.json']:
   path=kit/inputname;raw=path.read_bytes()
   for kind in ['missing','duplicate','symlink','hardlink']:
    ext=T/('saved-'+inputname.replace('/','_'));ext.write_bytes(raw)
    if kind=='missing':path.unlink()
    if kind=='duplicate':path.write_text('{"duplicate":1,"duplicate":2}')
    if kind=='symlink':path.unlink();path.symlink_to(ext)
    if kind=='hardlink':path.unlink();os.link(ext,path)
    run(cmd+[kit/'code/verify_kit.py'],1);faults.append({'optimized':opt,'input':inputname,'fault':kind,'rejected':True})
    path.unlink(missing_ok=True);path.write_bytes(raw);ext.unlink()
  # Writer bootstrap hardlinks and symlinks cannot create output first.
  for kind in ['symlink','hardlink']:
   path=kit/'MANIFEST.json';raw=path.read_bytes();ext=T/'saved-manifest';ext.write_bytes(raw);path.unlink()
   path.symlink_to(ext) if kind=='symlink' else os.link(ext,path)
   for writer,flag in [('rebuild_archive.py','--output'),('build_pdf.py','--out-dir')]:
    target=T/('bootstrap-'+kind+writer+str(opt));run(cmd+[kit/'code'/writer,flag,target],1);need(not target.exists(),'bootstrap output absent');faults.append({'optimized':opt,'writer':writer,'fault':'bootstrap-'+kind,'rejected':True})
   path.unlink();path.write_bytes(raw);ext.unlink()
  # Missing downloaded assets fail independently of an existing metadata binding.
  for name in ['paper.pdf','pr1098_support_v1_0.zip']:
   p=kit/name;raw=p.read_bytes();p.unlink();run(cmd+[kit/'code/verify_kit.py'],1);p.write_bytes(raw);faults.append({'optimized':opt,'fault':'missing-'+name,'rejected':True})
  run(cmd+[kit/'code/verify_kit.py'])
 need(existing.read_bytes()==b'existing bytes retained','existing overwrite');hard.unlink()
 final={str(p.relative_to(kit)):dg(p.read_bytes()) for p in kit.rglob('*') if p.is_file()}
 need(initial==final,'kit bytes unchanged')
 save('ACTUAL_REPRODUCTION.json',{'status':'PASS','external_root':str(T),'command_count':len(records),'raw_commands':'ACTUAL_COMMANDS.json','faults':faults,'physical_case_alias_samefile':same,'normal_O_full_JSON_equal':True,'unmodified_actual_scripts':True,'runtime_ROOT_or_ORIGINAL_modified':False,'both_actual_builds_equal_canonical':True,'both_closed_archives_equal_canonical':True,'kit_files_unchanged':len(initial),'no_services':True})
finally:
 if T.exists():cleanup_tree(T)
