from pathlib import Path
import subprocess,sys,tempfile,shutil,os,json,hashlib,datetime,ast,zipfile
OWN=Path(__file__).resolve().parent;AUDIT=OWN.parent;R=OWN/'replays/sealed_assembly';INNER=R/'publication_20261014/verification_package';PRE=R/'publication_20261014/preprint'
PIN='e5122815c93723664c499a2c8c90d1bf01423f4ab522998416fb2effaa950181';OUTER='c43861f2fe0e0282f49833dcd26b3d28cbee0e202653dbeb2b154a6cc86b027b'
def need(c,m):
 if not c:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
records=[]
for mode,more in [('normal',[]),('optimized',['-O'])]:
 flags=['-I','-S','-B',*more]
 for name,kind in [('wrong external pin','wrongpin'),('extra hidden member','hidden'),('extra empty descendant directory','directory'),('symlink at inventory root','rootlink'),('member directory symlink','dirlink'),('same size checker corruption before execution','checker'),('unsafe dot component fixture','dotpath'),('boolean byte count fixture','boolsize'),('duplicate nested row JSON key fixture','duplicatekey'),('absolute member path fixture','absolute'),('duplicate inventory path fixture','duplicatepath')]:
  with tempfile.TemporaryDirectory(prefix='independent controls ',dir=OWN/'replays') as td:
   d=Path(td);root=d/'portable';shutil.copytree(INNER,root);pin=PIN;manifest=root/'package_index.json';index=json.loads(manifest.read_bytes());entry=root/'verify_package.py';marker=d/'executed'
   if kind=='wrongpin':pin='0'*64
   elif kind=='hidden':(root/'.unexpected').write_text('hidden')
   elif kind=='directory':(root/'source/empty-descendant').mkdir()
   elif kind=='rootlink':link=d/'root-link';link.symlink_to(root,target_is_directory=True);entry=link/'verify_package.py'
   elif kind=='dirlink':shutil.rmtree(root/'algebra_audit_01');(root/'algebra_audit_01').symlink_to(INNER/'algebra_audit_01',target_is_directory=True)
   elif kind=='checker':
    # An indexed payload would leave a marker if launched. The wrapper itself remains trusted.
    path=root/'algebra_audit_01/exact_chain_check.py';size=len(path.read_bytes());payload=('from pathlib import Path\nPath('+repr(str(marker))+').touch()\n').encode();need(len(payload)<size,'spy too large');path.write_bytes(payload+b'#'*(size-len(payload)))
   elif kind=='dotpath':index['files'][0]['path']='source/./README.md'
   elif kind=='boolsize':index['files'][0]['bytes']=True
   elif kind=='absolute':index['files'][0]['path']='/tmp/independent-escape'
   elif kind=='duplicatepath':index['files'].append(index['files'][0])
   if kind in {'dotpath','boolsize','absolute','duplicatepath','duplicatekey'}:
    raw=json.dumps(index).encode()
    if kind=='duplicatekey':raw=raw.replace(b'"bytes":',b'"bytes":0,"bytes":',1)
    manifest.write_bytes(raw);pin=sha(raw)
   p=subprocess.run([sys.executable,*flags,str(entry),pin],cwd='/',capture_output=True,text=True,timeout=30)
   need(p.returncode!=0 and not p.stdout,'accepted malformed fixture '+kind);need(not marker.exists(),'payload executed')
   records.append({'mode':mode,'case':name,'returncode':p.returncode,'outcome':'rejected','final_error':p.stderr.splitlines()[-1],'trust':'derived structural fixture pin' if kind in {'dotpath','boolsize','absolute','duplicatepath','duplicatekey'} else 'original release pin'})
 # Probe startup omissions for both gates; omission tests themselves use exact trusted script bytes.
 for kind,script,pin in [('outer',R/'verify_publication.py',OUTER),('inner',INNER/'verify_package.py',PIN)]:
  for omitted in ['-I','-S','-B']:
   altered=[f for f in flags if f!=omitted]
   p=subprocess.run([sys.executable,*altered,str(script),pin],cwd='/',capture_output=True,text=True,timeout=30)
   need(p.returncode!=0 and 'run with python -I -S -B' in p.stderr and not p.stdout,'startup omission escaped')
   records.append({'mode':mode,'case':kind+' omission '+omitted,'returncode':p.returncode,'outcome':'rejected','final_error':p.stderr.splitlines()[-1]})
 # Standalone extracted ZIP remains usable in a different directory, with hostile Python search settings.
 with tempfile.TemporaryDirectory(prefix='relocated archive with spaces ',dir=OWN/'replays') as td:
  td=Path(td);pkg=td/'extracted kit';pkg.mkdir();hostile=td/'hostile';hostile.mkdir();marker=td/'imported'
  for name in ['sitecustomize','usercustomize','hashlib','json','zipfile','fractions','subprocess']:
   (hostile/(name+'.py')).write_text('from pathlib import Path\nPath('+repr(str(marker))+').touch()\nraise RuntimeError("hostile imported")\n')
  with zipfile.ZipFile(PRE/'verification.zip') as z:z.extractall(pkg)
  env=dict(os.environ,PYTHONPATH=str(hostile),PYTHONHOME=str(hostile),PYTHONOPTIMIZE='2')
  p=subprocess.run([sys.executable,*flags,str(pkg/'verify_package.py'),PIN,'--full'],cwd=hostile,env=env,capture_output=True,text=True,timeout=1200)
  need(p.returncode==0 and not p.stderr and not marker.exists(),'hostile relocation failed '+p.stderr)
  data=json.loads(p.stdout);need(data['regular_files']==140 and data['full']['fresh_algebra']['verification_checks_performed']==2110,'wrong relocated coverage')
  records.append({'mode':mode,'case':'full extracted ZIP hostile cwd/startup accepted safely','returncode':p.returncode,'outcome':'accepted','hostile_marker_absent':not marker.exists(),'full_output_sha256':sha(p.stdout.encode())})
# Confirm current guards really survive optimization at syntax level.
asserts={}
for p in [INNER/'verify_package.py',R/'verify_publication.py',INNER/'algebra_audit_01/exact_chain_check.py',INNER/'priority_audit_01/classical_lane/check_operator_blocks.py']:
 count=sum(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(p.read_bytes())));need(count==0,'current assertions');asserts[str(p.relative_to(R))]=count
result={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','cases':records,'case_count':len(records),'acceptances':sum(x['outcome']=='accepted' for x in records),'expected_rejections':sum(x['outcome']=='rejected' for x in records),'current_assert_statement_counts':asserts,'fixture_pins_not_release_authorizations':True}
(OWN/'receipts/ADVERSARIAL_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))
