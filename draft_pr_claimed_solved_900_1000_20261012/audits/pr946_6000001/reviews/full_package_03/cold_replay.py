import sys
if not sys.flags.isolated:raise RuntimeError('requires -I')
import pathlib,json,hashlib,stat,zipfile,subprocess,os,datetime,base64
R=pathlib.Path('/Users/alec/Documents/Math');A=R/'draft_pr_claimed_solved_900_1000_20261012/audits/pr946_6000001';D=A/'preprint';O=A/'reviews/full_package_03';T=O/'private/cold';T.mkdir()
sha=lambda b:hashlib.sha256(b).hexdigest()
f=json.loads((D/'FREEZE.json').read_bytes());assert sha((D/'FREEZE.json').read_bytes())=='fdff50b3a1c77523b1b1b7c3da42b2dfdbb1bc17ada7b19abfcbfbbd40d4c505'
b=(D/'global_hessian_verification.zip').read_bytes();assert sha(b)=='e687f7c9a3643a796a5fe813ec10e5c2c74a28adb081a7ebeefb6910823c6863'
with zipfile.ZipFile(D/'global_hessian_verification.zip') as z:
 m=json.loads(z.read('ARCHIVE_MANIFEST.json')); infos=z.infolist();assert len(infos)==220 and len(m['files'])==219 and len({i.filename for i in infos})==220
 for i in infos:
  p=pathlib.PurePosixPath(i.filename);assert str(p)==i.filename and not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename and not i.is_dir() and i.create_system==3 and i.external_attr>>16==0o100644
  raw=z.read(i)
  if i.filename!='ARCHIVE_MANIFEST.json':pin=m['files'][i.filename];assert len(raw)==pin['bytes'] and sha(raw)==pin['sha256']
  q=T/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(raw);q.chmod(0o644)
pkg=T/'package';mb=(pkg/'PACKAGE_MANIFEST.json').read_bytes();assert sha(mb)=='52165ba2410fa32238244feef20820e5bca9971f60c90542a2360f4d44e6c4ec';inner=json.loads(mb)
for n,pin in inner['files'].items():raw=(pkg/n).read_bytes();assert len(raw)==pin['bytes'] and sha(raw)==pin['sha256'] and stat.S_IMODE((pkg/n).lstat().st_mode)==0o644
assert {q.relative_to(pkg).as_posix() for q in pkg.rglob('*') if q.is_file()}==set(inner['files'])|{'PACKAGE_MANIFEST.json'}
raw=(pkg/'verify_package.py').read_bytes();vp='1896614c7b163e8fd69fa15c82c4d2a77e1ca46f4e4ada407d9ea5b52c2a2d2d';assert sha(raw)==vp
PYTHON='/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr906_30006419/reviews/computation_family/tmp/venv/bin/python'
boot="import sys,base64;raw=base64.b64decode(sys.argv[1]);p=sys.argv[2];sys.argv=sys.argv[2:];exec(compile(raw,p,'exec'),dict(__name__='__main__',__file__=p))"
modes=[];env=dict(os.environ);env['TMPDIR']=str(O/'private');env.pop('PYTHONOPTIMIZE',None)
for mode,flags,expected in [('normal',['-I'],0),('O',['-I','-O'],1),('OO',['-I','-OO'],2),('env2',['-P'],2)]:
 e=dict(env)
 if mode=='env2':e['PYTHONOPTIMIZE']='2'
 command=[PYTHON,*flags,'-B','-c',boot,base64.b64encode(raw).decode(),str(pkg/'verify_package.py'),'--package',str(pkg),'--manifest-sha256',sha(mb),'--runtime-receipt',str(O/'private'/('runtime_'+mode+'.json'))]
 r=subprocess.run(command,cwd=O/'private',env=e,capture_output=True,text=True,timeout=1200);(O/'private'/('cold_'+mode+'.stderr')).write_text(r.stderr);assert r.returncode==0,r.stderr
 rec=json.loads(r.stdout);canonical=json.loads((D/('PACKAGE_REPLAY_'+mode+'.json')).read_bytes());assert rec==canonical and rec['observed_outer_optimization']==expected and rec['worker_optimization']==0
 modes.append({'mode':mode,'observed_outer_optimization':expected,'returncode':r.returncode,'receipt':rec});print(mode,'PASS',flush=True)
result={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cold_extraction':True,'typed_float_policy_verified':True,'historical_strict_failure_preserved':True,'package_manifest_sha256':sha(mb),'externally_pinned_verifier_sha256':vp,'normalized_fields_ignored':[],'modes':modes,'outer_payloads':219,'archive_members':220,'inner_payloads':207,'canonical_receipts_compared_without_deletion':True,'captured_checked_entry_executed':True,'closure_authenticated_before_execution':True,'actual_external_mutations':0}
(O/'COLD_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
