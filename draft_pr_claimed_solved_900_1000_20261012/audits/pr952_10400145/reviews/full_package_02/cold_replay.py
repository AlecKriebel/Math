import datetime,hashlib,json,os,pathlib,subprocess,sys
ROOT=pathlib.Path('/Users/alec/Documents/Math');A=ROOT/'draft_pr_claimed_solved_900_1000_20261012/audits/pr952_10400145';D=A/'preprint';R=A/'reviews/full_package_02'
MAN='fe04fc51d308975f07b00ff788b12a719d8cce2ec5edddc738c8469cf49b30f2';VER='ba18bdcd863c3dca65c86be711564527ce19e4c859204b66095e39d366f453d7';ZIP='5fca36bc43c8b4f64ca236a417b036f4f36874f01476bfd216383e3fd05bbfae'
def need(p,m):
 if not p:raise RuntimeError(m)
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z')
def exact(a,b):return type(a) is type(b) and (set(a)==set(b) and all(exact(a[k],b[k]) for k in a) if type(a) is dict else len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b)) if type(a) is list else a==b)
private=R/'private_cold';private.mkdir();hostile=private/'hostile';hostile.mkdir()
for name in ['json.py','hashlib.py','sitecustomize.py','usercustomize.py']:(hostile/name).write_text("raise RuntimeError('FULL02_HOSTILE_IMPORT_ACTIVE')\n")
b=(D/'package/verify_package.py').read_bytes();need(hashlib.sha256(b).hexdigest()==VER,'verifier anchor');script=private/'verify_package.py';script.write_bytes(b)
env=dict(os.environ);env.update({'PYTHONPATH':str(hostile),'PYTHONSTARTUP':str(hostile/'sitecustomize.py'),'PYTHONDONTWRITEBYTECODE':'1'})
posargs=[sys.executable,'-S','-B','-c','import json']
pos=subprocess.run(posargs,cwd=hostile,env=env,capture_output=True)
(R/'HOSTILE_POSITIVE.stdout.raw').write_bytes(pos.stdout);(R/'HOSTILE_POSITIVE.stderr.raw').write_bytes(pos.stderr)
need(pos.returncode!=0 and b'FULL02_HOSTILE_IMPORT_ACTIVE' in pos.stderr,'hostile positive control did not function')
rows=[]
for mode,flag,opt in [('normal',[],0),('O',['-O'],1),('OO',['-OO'],2),('env2',[],0)]:
 work=private/('work_'+mode);work.mkdir();e=dict(env)
 if mode=='env2':e['PYTHONOPTIMIZE']='2'
 args=[sys.executable,'-I','-S','-B',*flag,str(script),'--archive',str(D/'habiro-rank-interpolation-verification-v1.0.zip'),'--archive-sha256',ZIP,'--manifest-sha256',MAN,'--run-checkers','--work-dir',str(work)]
 start=utc();p=subprocess.run(args,cwd=hostile,env=e,capture_output=True);end=utc()
 (R/f'COLD_{mode}.stdout.raw').write_bytes(p.stdout);(R/f'COLD_{mode}.stderr.raw').write_bytes(p.stderr)
 (R/f'COLD_{mode}.launch.json').write_text(json.dumps({'args':args,'cwd':str(hostile),'hostile_environment':{'PYTHONPATH':str(hostile),'PYTHONOPTIMIZE':e.get('PYTHONOPTIMIZE')},'started_utc':start,'completed_utc':end,'returncode':p.returncode,'verifier_sha256':VER},indent=2)+'\n')
 need(p.returncode==0,'cold failure '+mode);receipt=json.loads(p.stdout);canonical=json.loads((D/f'PACKAGE_REPLAY_{mode}.json').read_bytes())['receipt']
 need(exact(receipt,canonical),'receipt differs '+mode);need(receipt['outer_runtime']['optimize']==opt,'optimization observation');need(len(receipt['replays'])==12,'twelve inner stages');need(all(x['returncode']==0 for x in receipt['replays']),'inner failure')
 rows.append({'mode':mode,'observed_outer_optimization':receipt['outer_runtime']['optimize'],'returncode':p.returncode,'receipt':receipt})
result={'status':'PASS','utc':utc(),'cold_extraction':True,'package_manifest_sha256':MAN,'externally_pinned_verifier_sha256':VER,'normalized_fields_ignored':[],'modes':rows,'functioning_hostile_import_positive_control':{'returncode':pos.returncode,'marker':'FULL02_HOSTILE_IMPORT_ACTIVE'},'scope':'Actual copied authenticated entry verifier on actual current ZIP; private cold extraction performed internally; all inner stages; finite checks only.'}
(R/'COLD_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n');print('COLD_FOUR_MODES_EXACT_PASS')
