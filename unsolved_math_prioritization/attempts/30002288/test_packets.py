"""Portable controls for all preserved executable packets and the data-only V2."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):raise SystemExit('REJECT: require -I -S -B')
import argparse,hashlib,json,os,pathlib,shutil,stat,subprocess,tempfile,zipfile

def need(b,m):
 if not b:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--package',required=True);a=ap.parse_args();package=pathlib.Path(a.package);meta=json.loads((package/'PUBLICATION_METADATA.json').read_bytes());records=[]
 with tempfile.TemporaryDirectory(prefix='fractional packet controls ') as td:
  temp=pathlib.Path(td)
  for anchor in meta['archives']:
   role=anchor['role'];source=package/role;arc=package/'archives'/anchor['archive']['filename'];mf=package/'manifests'/anchor['manifest']['filename']
   if 'bootstrap' not in anchor:continue
   boot=package/'historical_bootstraps'/anchor['bootstrap']['filename'];entry={'original':'verify_math.py','corrected':'verify_math.py','audit':'independent_diagnostics.py','review2':'review_diagnostics.py'}[role];out={'original':'RESULTS.json','corrected':'RESULTS.json','audit':'INDEPENDENT_DIAGNOSTICS_RESULTS.json','review2':'DIAGNOSTIC_RESULTS.json'}[role]
   for opt in (False,True):
    for name in ['normal','relocation','hostile_cwd','extra_json','extra_sitecustomize','extra_cache','nested_directory','missing_member','changed_entrypoint','changed_results','symlink_member','symlink_root','symlink_ancestor','file_root','fifo_member','changed_manifest','changed_archive','symlink_manifest','symlink_archive','manifest_inside_root','archive_inside_root','unisolated']:
     case=temp/(role+'_'+name+('_O' if opt else ''));case.mkdir();root=case/'payload';shutil.copytree(source,root);ar=arc;m=mf;b=boot;cwd=case;marker=case/'SHOULD_NOT_EXECUTE';env=os.environ.copy()
     evil='open('+repr(str(marker))+',"w").write("executed")\nraise RuntimeError("hostile code")\n'
     if name=='relocation':
      far=case/'far path with spaces';far.mkdir();shutil.move(root,far/'payload');root=far/'payload'
      for f in (arc,mf,boot):shutil.copy2(f,far/f.name)
      ar=far/arc.name;m=far/mf.name;b=far/boot.name
     elif name=='hostile_cwd':
      for n in ['json.py','hashlib.py','pathlib.py','subprocess.py','zipfile.py','fractions.py','math.py','sitecustomize.py','usercustomize.py']:(case/n).write_text(evil)
      env['PYTHONPATH']=str(case);env['PYTHONSTARTUP']=str(case/'sitecustomize.py')
     elif name=='extra_json':(root/'json.py').write_text(evil)
     elif name=='extra_sitecustomize':(root/'sitecustomize.py').write_text(evil)
     elif name=='extra_cache':(root/'__pycache__').mkdir()
     elif name=='nested_directory':(root/'nested').mkdir()
     elif name=='missing_member':(root/'README.md').unlink()
     elif name=='changed_entrypoint':(root/entry).write_text(evil)
     elif name=='changed_results':(root/out).write_text('{}\n')
     elif name=='symlink_member':(root/entry).unlink();(root/entry).symlink_to(source/entry)
     elif name=='symlink_root':(case/'link').symlink_to(root,target_is_directory=True);root=case/'link'
     elif name=='symlink_ancestor':(case/'link').symlink_to(case,target_is_directory=True);root=case/'link/payload'
     elif name=='file_root':root=case/'file';root.write_text('file')
     elif name=='fifo_member':(root/'README.md').unlink();os.mkfifo(root/'README.md')
     elif name=='changed_manifest':m=case/'manifest';m.write_bytes(mf.read_bytes()+b' ')
     elif name=='changed_archive':ar=case/'archive';ar.write_bytes(arc.read_bytes()+b'x')
     elif name=='symlink_manifest':m=case/'manifest';m.symlink_to(mf)
     elif name=='symlink_archive':ar=case/'archive';ar.symlink_to(arc)
     elif name=='manifest_inside_root':m=root/'manifest.json';m.write_bytes(mf.read_bytes())
     elif name=='archive_inside_root':ar=root/'archive.zip';ar.write_bytes(arc.read_bytes())
     cmd=[sys.executable,'-B']+([] if name=='unisolated' else ['-I','-S'])+(['-O'] if opt else [])+[str(b),str(root),str(ar),str(m)]+(['--optimized'] if opt else [])
     r=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,timeout=60);positive=name in ['normal','relocation','hostile_cwd']
     if positive:need(r.returncode==0 and not r.stderr and r.stdout==(source/out).read_bytes(),role+' '+name+' acceptance: '+r.stderr.decode())
     else:need(r.returncode!=0 and not r.stdout,role+' '+name+' failed rejection')
     need(not marker.exists(),role+' '+name+' hostile code executed')
     records.append({'role':role,'name':name,'optimized':opt,'expected':'exact_accept' if positive else 'reject_before_checker','status':'PASS'})
  # Data-only supplement: validate independent pins, inventory, types, all bytes.
  anchor=next(r for r in meta['archives'] if r['role']=='supplement');source=package/'supplement';arc=package/'archives'/anchor['archive']['filename'];mf=package/'manifests'/anchor['manifest']['filename']
  def verify(root,ar,m):
   for p in (root,ar,m):
    for q in [p]+list(p.parents):need(not stat.S_ISLNK(q.lstat().st_mode),'supplement symlink')
   need(stat.S_ISDIR(root.lstat().st_mode),'supplement root')
   for p in (ar,m):need(stat.S_ISREG(p.lstat().st_mode),'supplement metadata type')
   mb=m.read_bytes();need((len(mb),sha(mb))==(anchor['manifest']['bytes'],anchor['manifest']['sha256']),'supplement manifest pin');manifest=json.loads(mb)
   need(set(p.name for p in root.iterdir())==set(manifest['files']),'supplement inventory')
   ab=ar.read_bytes();need((len(ab),sha(ab))==(anchor['archive']['bytes'],anchor['archive']['sha256']),'supplement archive pin')
   with zipfile.ZipFile(ar) as z:
    need(len(z.namelist())==len(set(z.namelist())) and set(z.namelist())==set(manifest['files']) and z.testzip() is None,'supplement archive inventory')
    for n,r in manifest['files'].items():
     p=root/n;need(stat.S_ISREG(p.lstat().st_mode),'supplement member type');data=p.read_bytes();need(r=={'bytes':len(data),'sha256':sha(data)} and z.read(n)==data,'supplement bytes')
     need(stat.S_ISREG(z.getinfo(n).external_attr>>16) and pathlib.PurePosixPath(n).name==n,'supplement ZIP type')
   need(set(manifest['files'])=={'SELECTION_LIMITS.md','STATUS_ADDENDUM.json'},'data-only inventory')
  for name in ['normal','relocation','extra_module','nested_directory','changed_text','missing_member','symlink_member','symlink_root','symlink_ancestor','file_root','changed_manifest','changed_archive']:
   case=temp/('supplement_'+name);case.mkdir();root=case/'payload';shutil.copytree(source,root);ar=arc;m=mf
   if name=='relocation':ar=case/'archive';m=case/'manifest';shutil.copyfile(arc,ar);shutil.copyfile(mf,m)
   elif name=='extra_module':(root/'evil.py').write_text('raise RuntimeError("never run")')
   elif name=='nested_directory':(root/'nested').mkdir()
   elif name=='changed_text':(root/'SELECTION_LIMITS.md').write_text('changed')
   elif name=='missing_member':(root/'STATUS_ADDENDUM.json').unlink()
   elif name=='symlink_member':(root/'SELECTION_LIMITS.md').unlink();(root/'SELECTION_LIMITS.md').symlink_to(source/'SELECTION_LIMITS.md')
   elif name=='symlink_root':(case/'link').symlink_to(root,target_is_directory=True);root=case/'link'
   elif name=='symlink_ancestor':(case/'link').symlink_to(case,target_is_directory=True);root=case/'link/payload'
   elif name=='file_root':root=case/'file';root.write_text('file')
   elif name=='changed_manifest':m=case/'manifest';m.write_bytes(mf.read_bytes()+b' ')
   elif name=='changed_archive':ar=case/'archive';ar.write_bytes(arc.read_bytes()+b'x')
   try:verify(root,ar,m);accepted=True
   except ValueError:accepted=False
   need(accepted==(name in ['normal','relocation']),'supplement control '+name)
   records.append({'role':'supplement','name':name,'expected':'accept' if accepted else 'reject','status':'PASS'})
 print(json.dumps({'status':'PASS','case_count':len(records),'records':records,'hostile_markers_absent':True,'scope':'Artifact checks and finite corroboration only'},sort_keys=True,indent=2))
if __name__=='__main__':main()
