from pathlib import Path
import os,sys,json,hashlib,subprocess,datetime,shutil,difflib,zipfile
O=Path(__file__).resolve().parent;A=O.parents[1];P=A.parents[2];D=A/'preprint'
CORE=P/'draft_pr_claimed_solved_900_1000_20261012/accept_pr952.py';CS='854a8694e3b4b46d3eff32f207729d2637c262b9714d8a7b052289450831e908';VS='ba18bdcd863c3dca65c86be711564527ce19e4c859204b66095e39d366f453d7';MS='156b69a86fb749058dab16c39e2dffee047a6c752fdcf10d099ffb639c2d36d6';ZS='607dec129916a702b5863add8b51770c900768be64b0d549e0ec75811fbe56e0'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def save(n,x):(O/n).write_text(json.dumps(x,indent=2)+'\n')
def launch(label,cmd,cwd,env):
 start=now();r=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,timeout=240)
 (O/(label+'.stdout.json')).write_bytes(r.stdout);(O/(label+'.stderr.txt')).write_bytes(r.stderr);save(label+'.launch.json',{'started_utc':start,'completed_utc':now(),'argv':cmd,'cwd':str(cwd),'returncode':r.returncode,'stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr)})
 if r.returncode:raise RuntimeError(label+' failed; raw evidence retained')
 return json.loads(r.stdout)
base=O/'private_checks';base.mkdir(exist_ok=True);hostile=base/'hostile';hostile.mkdir(exist_ok=True);marker=base/'IMPORT_POISON_EXECUTED'
for name in ('json.py','sitecustomize.py','usercustomize.py'):(hostile/name).write_text('from pathlib import Path\nPath('+repr(str(marker))+').write_text("executed")\nraise RuntimeError("POISON")\n')
env=dict(os.environ,TMPDIR=str(base),PYTHONPATH=str(hostile),PYTHONUSERBASE=str(hostile),PYTHONOPTIMIZE='2')
r=subprocess.run([sys.executable,'-B','-c','import json'],cwd=hostile,env=env,capture_output=True);(O/'HOSTILE_POSITIVE_CONTROL.stdout.txt').write_bytes(r.stdout);(O/'HOSTILE_POSITIVE_CONTROL.stderr.txt').write_bytes(r.stderr);assert r.returncode and marker.exists();marker.unlink();save('HOSTILE_POSITIVE_CONTROL.json',{'utc':now(),'returncode':r.returncode,'marker_observed':True,'real_positive_control':True})
with zipfile.ZipFile(D/'habiro-rank-interpolation-verification-v1.0.zip') as z:raw=z.read('verify_package.py')
assert sha(raw)==VS;verifier=base/'verify_package.py';verifier.write_bytes(raw);verifier.chmod(0o644)
modes=[]
for label,flags in [('normal',[]),('O',['-O']),('OO',['-OO']),('env2',[])]:
 work=base/('work_'+label);work.mkdir(exist_ok=True);e=env if label=='env2' else dict(os.environ,TMPDIR=str(base));cmd=[sys.executable,'-I','-S','-B',*flags,str(verifier),'--archive',str(D/'habiro-rank-interpolation-verification-v1.0.zip'),'--archive-sha256',ZS,'--manifest-sha256',MS,'--run-checkers','--work-dir',str(work)]
 receipt=launch('COLD_'+label,cmd,hostile,e);assert not marker.exists();expected=json.loads((D/('PACKAGE_REPLAY_'+label+'.json')).read_text())['receipt'];assert receipt==expected,(label,'receipt inequality');assert len(receipt['replays'])==12
 modes.append({'mode':label,'observed_outer_optimization':receipt['outer_runtime']['optimize'],'returncode':0,'receipt':receipt})
save('COLD_REPLAY.json',{'status':'PASS','utc':now(),'cold_extraction':True,'package_manifest_sha256':MS,'externally_pinned_verifier_sha256':VS,'normalized_fields_ignored':[],'modes':modes})
print('four actual cold modes passed',flush=True)
fixtures=base/'engineering';fixtures.mkdir(exist_ok=True)
for name in ('test_profile.py','test_observations.py','observation_checks.py','verify_package.py','independent_math.py'):shutil.copyfile(A/'package_engineering_01'/name,fixtures/name)
ops=base/'operations';ops.mkdir(exist_ok=True)
changes={}
for name in ('test_operations.py','test_source_gate.py'):
 raw=(A/'operations_engineering_02'/name).read_text();old="OWN=Path(__file__).resolve().parent;P=OWN.parents[2];";replacement="OWN=Path(__file__).resolve().parent;P=Path("+repr(str(P/'draft_pr_claimed_solved_900_1000_20261012'))+"); # REVIEWER_HARNESS: fixed trusted core/private-input root only\n"
 assert old in raw;new=raw.replace(old,replacement,1);(ops/name).write_text(new);(O/(name+'.REVIEWER_HARNESS.diff')).write_text(''.join(difflib.unified_diff(raw.splitlines(True),new.splitlines(True),fromfile='authenticated/'+name,tofile='reviewer_owned/'+name)));changes[name]={'original_sha256':sha(raw.encode()),'adapted_sha256':sha(new.encode()),'changes':'Only P fixture/core/privateinput location; mutations remain disabled; guards unchanged'}
save('REVIEWER_HARNESS_ADAPTATIONS.json',changes)
results=[]
for label,flags in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
 e=dict(os.environ,TMPDIR=str(base));work=base/('profile_'+label);work.mkdir(exist_ok=True)
 for kind,script,args,want in [('PROFILE',fixtures/'test_profile.py',['--originals',str(A/'original/unsolved_math_prioritization/attempts/10400145'),'--verifier-sha256',VS,'--work-dir',str(work)],92),('OBSERVATIONS',fixtures/'test_observations.py',[sha((fixtures/'observation_checks.py').read_bytes())],None),('OPERATIONS',ops/'test_operations.py',['--core-sha256',CS],61),('SOURCE_GATE',ops/'test_source_gate.py',['--core-sha256',CS],18)]:
  result=launch(kind+'_'+label,[sys.executable,'-I','-S','-B',*flags,str(script),*args],base,e);count=result.get('event_count',len(result.get('tests',[])));assert want is None or count==want,(kind,count,want);results.append({'kind':kind,'outer_mode':label,'result':result});print(kind,label,count,flush=True)
save('ENGINEERING_REPLAY_SUMMARY.json',{'utc':now(),'status':'PASS','results':results})
