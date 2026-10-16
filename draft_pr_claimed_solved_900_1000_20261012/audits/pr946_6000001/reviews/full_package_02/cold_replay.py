from pathlib import Path,PurePosixPath
import base64,datetime,hashlib,json,os,stat,subprocess,zipfile
R=Path('/Users/alec/Documents/Math');A=R/'draft_pr_claimed_solved_900_1000_20261012/audits/pr946_6000001';D=A/'preprint';O=A/'reviews/full_package_02';S=O/'private/cold_repeat';S.mkdir()
T=O/'private/temp';T.mkdir(exist_ok=True)
PYTHON=R/'draft_pr_claimed_solved_900_1000_20261012/audits/pr906_30006419/reviews/computation_family/tmp/venv/bin/python'
def h(x):return hashlib.sha256(x).hexdigest()
def need(x,m):
 if not x:raise RuntimeError(m)
raw=(D/'global_hessian_verification.zip').read_bytes();need(h(raw)=='0b6883acc22bc986ab7250157568041a3fe90770372b30d95e369d84952497d0','zip pin')
with zipfile.ZipFile(D/'global_hessian_verification.zip') as z:
 names=z.namelist();am=z.read('ARCHIVE_MANIFEST.json');need(h(am)=='2790863687ae7bf92c62f03d13c8102b7341d687709df8d1c74b41326126b986','outer pin');m=json.loads(am);need(len(names)==len(set(names))==220 and set(names)==set(m['files'])|{'ARCHIVE_MANIFEST.json'},'closed inventory')
 for i in z.infolist():
  pp=PurePosixPath(i.filename);need(not pp.is_absolute() and '..' not in pp.parts and str(pp)==i.filename and i.create_system==3 and (i.external_attr>>16)==0o100644 and not i.is_dir(),'safe regular member')
  b=z.read(i);need(i.filename=='ARCHIVE_MANIFEST.json' or {'bytes':len(b),'sha256':h(b)}==m['files'][i.filename],'payload pin')
  p=S/i.filename;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);p.chmod(0o644)
need({str(x.relative_to(S)) for x in S.rglob('*') if x.is_file()}==set(names),'cold disk closed')
manifest='52165ba2410fa32238244feef20820e5bca9971f60c90542a2360f4d44e6c4ec';v=(S/'package/verify_package.py').read_bytes();need(h(v)=='1896614c7b163e8fd69fa15c82c4d2a77e1ca46f4e4ada407d9ea5b52c2a2d2d','verifier external pin');need(h((S/'package/PACKAGE_MANIFEST.json').read_bytes())==manifest,'manifest pin')
inner=json.loads((S/'package/PACKAGE_MANIFEST.json').read_bytes())
for name,pin in inner['files'].items():
 b=(S/'package'/name).read_bytes();need(h(b)==pin['sha256'] and len(b)==pin['bytes'] and stat.S_IMODE((S/'package'/name).stat().st_mode)==0o644,'dependency closure')
BOOT='import sys,base64; p=sys.argv[2];sys.argv=sys.argv[2:];exec(compile(base64.b64decode(sys.argv.pop(1)) if False else base64.b64decode(BYTES),p,"exec"),dict(__name__="__main__",__file__=p))'
# A separately supplied literal, captured authenticated byte string executes with actual startup flags.
BOOT='import sys,base64;raw=base64.b64decode(sys.argv[1],validate=True);p=sys.argv[2];sys.argv=sys.argv[2:];exec(compile(raw,p,"exec"),dict(__name__="__main__",__file__=p))'
modes=[]
for label,flags,envopt,want in [('normal',['-I','-B'],None,0),('O',['-I','-B','-O'],None,1),('OO',['-I','-B','-OO'],None,2),('env2',['-P','-B'],'2',2)]:
 env={k:v for k,v in os.environ.items() if not k.upper().startswith('PYTHON')};env['TMPDIR']=str(T)
 if envopt:env['PYTHONOPTIMIZE']=envopt
 args=[str(PYTHON),*flags,'-c',BOOT,base64.b64encode(v).decode(),str(S/'package/verify_package.py'),'--package',str(S/'package'),'--manifest-sha256',manifest,'--runtime-receipt',str(O/'private'/('runtime_'+label+'.json'))]
 r=subprocess.run(args,env=env,capture_output=True,text=True,timeout=1200,cwd=S);(O/'private'/('cold_'+label+'.stdout')).write_text(r.stdout);(O/'private'/('cold_'+label+'.stderr')).write_text(r.stderr)
 need(r.returncode==0,'mode '+label+' failed '+r.stderr);j=json.loads(r.stdout);canonical=json.loads((D/('PACKAGE_REPLAY_'+label+'.json')).read_bytes());need(j==canonical,'FULL canonical receipt differs '+label);need(j['observed_outer_optimization']==want and j['worker_optimization']==0,'observed optimization')
 modes.append({'mode':label,'observed_outer_optimization':j['observed_outer_optimization'],'returncode':r.returncode,'receipt':j});print(label,'PASS',flush=True)
 (O/'private/cold_progress.json').write_text(json.dumps(modes,indent=2)+'\n')
result={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'cold_extraction':True,'package_manifest_sha256':manifest,'externally_pinned_verifier_sha256':h(v),'normalized_fields_ignored':[],'modes':modes,'outer_payloads':219,'outer_members':220}
(O/'COLD_MODES.json').write_text(json.dumps(result,indent=2)+'\n')
