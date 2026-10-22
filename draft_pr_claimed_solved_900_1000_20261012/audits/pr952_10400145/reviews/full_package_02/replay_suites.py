import concurrent.futures,datetime,difflib,hashlib,json,pathlib,subprocess,sys
ROOT=pathlib.Path('/Users/alec/Documents/Math');P=ROOT/'draft_pr_claimed_solved_900_1000_20261012';A=P/'audits/pr952_10400145';R=A/'reviews/full_package_02';S=R/'private_suites';S.mkdir()
PIN='888a068e26e0adcc3f493817ef46c46b6bdd5a4f848a4d907e4f4af2b5f592a8';VER='ba18bdcd863c3dca65c86be711564527ce19e4c859204b66095e39d366f453d7'
def sha(b):return hashlib.sha256(b).hexdigest()
adapt=[]
for name in ['test_operations_installed.py','test_source_gate_installed.py','test_native_recovery.py','BASE_accept_pr952.py','PROPOSED_accept_pr952.py']:
 src=A/'operations_engineering_03'/name;b=src.read_bytes();text=b.decode();new=text
 if name.startswith('test_'):
  old="OWN=Path(__file__).resolve().parent;P=OWN.parents[2]";replacement="OWN=Path(__file__).resolve().parent;P=Path("+repr(str(P))+")"
  if old not in new:raise RuntimeError('adaptation target missing')
  new=new.replace(old,replacement,1)
 (S/name).write_text(new)
 adapt.append({'source':str(src.relative_to(ROOT)),'source_sha256':sha(b),'copy_sha256':sha(new.encode()),'diff':''.join(difflib.unified_diff(text.splitlines(True),new.splitlines(True),fromfile=str(src),tofile=str(S/name)))})
for name in ['test_profile.py','test_observations.py','verify_package.py','observation_checks.py','independent_math.py']:
 src=A/'package_engineering_01'/name;b=src.read_bytes();(S/name).write_bytes(b);adapt.append({'source':str(src.relative_to(ROOT)),'source_sha256':sha(b),'copy_sha256':sha(b),'diff':''})
(R/'HARNESS_ADAPTATIONS.json').write_text(json.dumps({'path_only':True,'adaptations':adapt},indent=2)+'\n')
tasks=[]
for mode,flag in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
 work=S/('work_'+mode);work.mkdir()
 for label,name,args in [
 ('operations','test_operations_installed.py',['--core-sha256',PIN]),
 ('source_gate','test_source_gate_installed.py',['--core-sha256',PIN]),
 ('native_recovery','test_native_recovery.py',['--proposal-sha256',PIN,'--installed']),
 ('profile','test_profile.py',['--originals',str(A/'original/unsolved_math_prioritization/attempts/10400145'),'--verifier-sha256',VER,'--work-dir',str(work)]),
 ('observations','test_observations.py',[sha((S/'observation_checks.py').read_bytes())])]:
  tasks.append((label,mode,[sys.executable,'-I','-S','-B',*flag,str(S/name),*args]))
def launch(task):
 label,mode,args=task;start=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.run(args,cwd=S,capture_output=True);end=datetime.datetime.now(datetime.timezone.utc).isoformat()
 stem=f'SUITE_{label}_{mode}';(R/(stem+'.stdout.raw')).write_bytes(p.stdout);(R/(stem+'.stderr.raw')).write_bytes(p.stderr)
 rec={'label':label,'mode':mode,'args':args,'started_utc':start,'completed_utc':end,'returncode':p.returncode,'source_compilation_optimization':0 if label in ['operations','source_gate','native_recovery','observations'] else {'normal':0,'O':1,'OO':2}[mode]}
 if p.returncode==0:
  o=json.loads(p.stdout);rec.update(event_count=o.get('event_count',len(o.get('events',o.get('tests',[])))) ,declared_status=o.get('status'))
 (R/(stem+'.launch.json')).write_text(json.dumps(rec,indent=2)+'\n');return rec
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:rows=list(executor.map(launch,tasks))
(R/'SUITE_REPLAY_SUMMARY.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'rows':rows,'scope':'Copied authenticated test sources; only location adaptation; actual installed core; inert mutation boundaries. Installed operations core and observation module compile optimize=0 even under O/OO; profile compiles per outer optimization.'},indent=2)+'\n')
print('SUITES_COMPLETE',[(r['label'],r['mode'],r['returncode'],r.get('event_count')) for r in rows])
