import sys,pathlib,json,os,subprocess,zipfile,hashlib,datetime,stat
R=pathlib.Path(__file__).parent;A=R.parents[1];D=A/'preprint';W=A/'publication/workflow';P=A.parents[1];PY=json.loads((D/'PACKAGE_REPLAY_normal.json').read_bytes())['command'][0]
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(p,d):
 raw=(json.dumps(d,indent=2,allow_nan=False)+'\n').encode();p=R/p
 with p.open('wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
 assert p.read_bytes()==raw
mode=sys.argv[1]
if mode=='cold':
 s={'__name__':'review07_profile','__file__':str(D/'package/profile/verify_package.py')};exec(compile((D/'package/profile/verify_package.py').read_bytes(),str(D/'package/profile/verify_package.py'),'exec',dont_inherit=True,optimize=0),s)
 raw=(D/'anti-invariant-four-manifold-verification-v1.0.zip').read_bytes();manifest=json.loads((D/'package/PACKAGE_MANIFEST.json').read_bytes());expected=dict(manifest['files']);expected['PACKAGE_MANIFEST.json']={'bytes':len((D/'package/PACKAGE_MANIFEST.json').read_bytes()),'sha256':hashlib.sha256((D/'package/PACKAGE_MANIFEST.json').read_bytes()).hexdigest(),'mode':'100644'}
 inventory=s['inspect_archive'](raw,expected);save('ZIP_METADATA.json',{'utc':utc(),'members':258,'metadata_before_decompression':True,'matched_closed_namespace_and_bytes':inventory})
 root=R/'private_cold_rerun';root.mkdir()
 with zipfile.ZipFile(D/'anti-invariant-four-manifold-verification-v1.0.zip') as z:
  for info in z.infolist():
   p=root/info.filename;p.parent.mkdir(parents=True,exist_ok=True)
   with p.open('xb') as f:f.write(z.read(info));f.flush();os.fsync(f.fileno())
   p.chmod(0o644)
 labels=['normal','O','OO','env2'];rows=[]
 for label,opt in zip(labels,[0,1,2,0]):
  cmd=[PY,'-I','-S','-B']+(['-'+('O'*opt)] if opt else [])+[str(root/'profile/verify_package.py'),'--root',str(root),'--manifest-sha256',manifest_sha:='a25e28435f84374bf6e6705c9e5bc91952236d9f5fc5dc48e05ad29d62956b23','--run-checkers'];env=os.environ.copy(); tmp=R/'cold_child_tmp';tmp.mkdir(exist_ok=True);env['TMPDIR']=str(tmp);env['TMP']=str(tmp);env['TEMP']=str(tmp); started=utc()
  if label=='env2':env.update(PYTHONOPTIMIZE='2',PYTHONPATH=str(R/'nonexistent_poison'),PYTHONSTARTUP=str(R/'nonexistent_startup'))
  p=subprocess.run(cmd,capture_output=True,text=True,env=env,cwd=R)
  receipt=json.loads(p.stdout) if p.returncode==0 else None
  row={'mode':label,'observed_outer_optimization':receipt['outer_runtime']['optimize'] if receipt else None,'returncode':p.returncode,'receipt':receipt}
  save('COLD_MODE_'+label+'.json',{'started_utc':started,'utc':utc(),'command':cmd,'stdout':p.stdout,'stderr':p.stderr,**row})
  assert p.returncode==0 and row['observed_outer_optimization']==opt and receipt==json.loads((D/('PACKAGE_REPLAY_'+label+'.json')).read_bytes())['receipt']
  rows.append(row)
 save('COLD_REPLAY.json',{'status':'PASS','utc':utc(),'cold_extraction':True,'package_manifest_sha256':manifest_sha,'externally_pinned_verifier_sha256':hashlib.sha256((root/'profile/verify_package.py').read_bytes()).hexdigest(),'normalized_fields_ignored':[],'modes':rows});print('cold four exact canonical receipts PASS')
elif mode=='profile':
 cmd=[PY,'-I','-S','-B',str(D/'package/profile/test_profile.py'),'--driver',str(D/'package/profile/verify_package.py'),'--originals',str(A/'original/unsolved_math_prioritization/attempts/30004549'),'--output-dir',str(R/'profile')]
 p=subprocess.run(cmd,capture_output=True,text=True,cwd=R);save('PROFILE_EXECUTION.json',{'utc':utc(),'command':cmd,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr});print(p.stdout,p.stderr);assert p.returncode==0
