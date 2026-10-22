"""Auditor's isolated replay/control harness; only authenticated packet executes."""
import sys
if not sys.flags.isolated or not sys.flags.no_site: raise SystemExit('Use python -I -S.')
import os, pathlib, hashlib, json, subprocess, shutil, tempfile, zipfile
if len(sys.argv)!=2: raise SystemExit('usage: replay_controls.py DIRECTORY_CONTAINING_AUTHOR_INPUTS')
base=pathlib.Path(sys.argv[1]).resolve()
archive=base/'CM_REDUCTION_30002364_AUTHOR_SAFE_FREEZE.zip'
boot=base/'CM_REDUCTION_30002364_AUTHOR_BOOTSTRAP.py'
manifest=base/'CM_REDUCTION_30002364_AUTHOR_EXTERNAL_MANIFEST.json'
pins={archive:'32f5ec9f310f62566906cf6b0ff4a1e8cef5a6e9442ecb995c91525a1fb9879e',boot:'897a75796bef8d980a0c12808a21ddd9a71cefa7dbf54bd6cf12c8f14ad2d6a5',manifest:'24d868b99bd75c586313062c107bb6d6b1f2f5d5efb939f17d1401e1da6c8212',base/'CM_REDUCTION_30002364_AUTHOR_VALIDATION_RECEIPT.json':'fdefdaa0d0f2644439925b80ee0f15c94357fd45bf946978a07c709ebe852174'}
def require(x,msg):
 if not x: raise RuntimeError(msg)
for p,h in pins.items(): require(hashlib.sha256(p.read_bytes()).hexdigest()==h,'external pin '+p.name)
records=[]
with tempfile.TemporaryDirectory(prefix='cm audit controls ') as tmp:
 t=pathlib.Path(tmp); original=t/'original';original.mkdir()
 with zipfile.ZipFile(archive) as z:
  names=z.namelist(); require(len(names)==len(set(names)),'duplicate ZIP entries')
  for name in names:
   require(pathlib.PurePosixPath(name).name==name,'unsafe ZIP entry')
   (original/name).write_bytes(z.read(name))
 expected=json.loads(manifest.read_bytes())['files']
 require(set(names)==set(expected),'ZIP inventory differs')
 for name,rec in expected.items():
  b=(original/name).read_bytes();require(len(b)==rec['bytes'] and hashlib.sha256(b).hexdigest()==rec['sha256'],'ZIP member pin')
 def run(name,root,success,manifest_arg=manifest,extra=(),cwd=None,env=None,flags=('-I','-S'),direct=False,expected_message=None):
  cmd=[sys.executable,*flags,str(root/'verify_math.py')] if direct else [sys.executable,*flags,str(boot),str(root),str(manifest_arg),*extra]
  p=subprocess.run(cmd,cwd=cwd or t,env=env,capture_output=True,text=True)
  out=(p.stdout+p.stderr).strip()
  ok=(p.returncode==0)==success and (expected_message is None or expected_message in out)
  records.append({'name':name,'expected_success':success,'exit_code':p.returncode,'output':out,'passed':ok})
  require(ok,name)
 def clone(name):
  root=t/name;shutil.copytree(original,root);return root
 run('authenticated ordinary Python semantics',original,True)
 run('authenticated optimized checker',original,True,extra=('--optimized',))
 run('authenticated optimized bootstrap and checker',original,True,extra=('--optimized',),flags=('-I','-S','-O'))
 run('authenticated relocated root containing spaces',clone('relocated packet with spaces'),True)
 marker=t/'EXECUTED_UNTRUSTED'
 malicious=f"__import__('pathlib').Path({str(marker)!r}).write_text('untrusted')\n"
 for module in ('fractions.py','hashlib.py','json.py','pathlib.py','sitecustomize.py','usercustomize.py'):
  root=clone('shadow '+module);(root/module).write_text(malicious)
  run('reject inventory shadow '+module,root,False,expected_message='strict inventory mismatch')
 root=clone('cache');(root/'__pycache__').mkdir();run('reject cache directory',root,False,expected_message='strict inventory mismatch')
 root=clone('tamper');(root/'verify_math.py').write_text(malicious);run('reject modified checker before execution',root,False,expected_message='file digest mismatch')
 root=clone('proof tamper');(root/'PROOF.md').write_text('changed');run('reject modified proof before execution',root,False,expected_message='file digest mismatch')
 root=clone('missing');(root/'README.md').unlink();run('reject missing file',root,False,expected_message='strict inventory mismatch')
 root=clone('symlink member');(root/'README.md').unlink();(root/'README.md').symlink_to(original/'README.md');run('reject symlink member',root,False,expected_message='non-regular inventory member')
 link=t/'symlink root';link.symlink_to(original,target_is_directory=True);run('reject symlink root',link,False,expected_message='not a real canonical directory')
 root=clone('manifest inside');inside=root/'external.json';inside.write_bytes(manifest.read_bytes());run('reject manifest inside packet',root,False,manifest_arg=inside,expected_message='must be external')
 bad=t/'modified manifest.json';bad.write_bytes(manifest.read_bytes()+b'\n');run('reject mutated external manifest',original,False,manifest_arg=bad,expected_message='manifest digest mismatch')
 symlink=t/'manifest symlink.json';symlink.symlink_to(manifest);run('reject symlink external manifest',original,False,manifest_arg=symlink,expected_message='not a regular canonical file')
 hostile=t/'hostile cwd';hostile.mkdir()
 for module in ('fractions.py','hashlib.py','json.py','pathlib.py','sitecustomize.py','usercustomize.py'):(hostile/module).write_text(malicious)
 env=dict(os.environ,PYTHONPATH=str(hostile),PYTHONSTARTUP=str(hostile/'sitecustomize.py'))
 run('ignore hostile cwd and Python environment',original,True,cwd=hostile,env=env)
 run('reject missing isolation',original,False,flags=('-S',),expected_message='Use python -I -S')
 run('reject missing no-site',original,False,flags=('-I',),expected_message='Use python -I -S')
 run('reject direct checker without isolation',original,False,flags=('-S',),direct=True,expected_message='Use python -I -S')
 require(not marker.exists(),'untrusted payload executed')
result={'schema':'independent-replay-controls-v1','problem_id':30002364,'external_pins':{p.name:h for p,h in pins.items()},'all_passed':all(x['passed'] for x in records),'test_count':len(records),'untrusted_marker_absent':True,'archive_inventory_and_members_verified':True,'tests':records,'scope':'Finite replay/authentication only; mathematical audit is separate.'}
print(json.dumps(result,sort_keys=True,indent=2))
