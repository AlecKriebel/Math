import pathlib,shutil,hashlib,subprocess,sys,datetime,json,os
R=pathlib.Path('/Users/alec/Documents/Math');P=R/'draft_pr_claimed_solved_900_1000_20261012';A=P/'audits/pr967_2616';D=A/'reviews/closure_package_adversary_01';T=D/'private_tmp/cold_final';E=A/'closure_engineering_01'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
expected={'close_pr967.py':'c6231a47758a6b037ed005883d39e374946e38bd9aec0c74eb33df3afe2d2a45','finalize_pr967_and_gate_next.py':'47520f8f86889db8c5b85fc7000486773d2ca4e8601ad00531bad2fdce5143cb'}
for name,h in expected.items():assert sha((E/('FINAL02_'+name)).read_bytes())==h
manifest=json.loads((E/'MANIFEST.json').read_text());suite=(E/'test_offline.py').read_bytes();assert sha(suite)==manifest['files']['test_offline.py']['sha256']
assert not T.exists();CP=T/'effort';CA=CP/'audits/pr967_2616';CE=CA/'closure_engineering_01';CE.mkdir(parents=True)
for name in expected:shutil.copyfile(E/('FINAL02_'+name),CP/name)
for name in ['ORIGINAL_FILE_RECORDS.json','source_record_private.txt']:shutil.copyfile(A/name,CA/name)
shutil.copytree(A/'original',CA/'original');shutil.copyfile(E/'test_offline.py',CE/'test_offline.py')
loader="import pathlib,hashlib,sys; p=pathlib.Path(sys.argv[1]); raw=p.read_bytes(); expected=sys.argv[2]; exec('if hashlib.sha256(raw).hexdigest()!=expected: raise RuntimeError(\"external initial source pin mismatch\")'); sys.argv=[str(p),*sys.argv[3:]]; exec(compile(raw,str(p),'exec',dont_inherit=True,optimize=0),{'__name__':'__main__','__file__':str(p)})"
receipts=[]
for mode,flags in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
 cmd=[sys.executable,'-I','-S','-B',*flags,'-c',loader,str(CE/'test_offline.py'),sha(suite),'--core-sha256',expected['close_pr967.py'],'--wrapper-sha256',expected['finalize_pr967_and_gate_next.py']]
 start=now();out=subprocess.run(cmd,cwd=CP,capture_output=True,timeout=120)
 (D/('OFFLINE_'+mode+'.stdout.raw')).write_bytes(out.stdout);(D/('OFFLINE_'+mode+'.stderr.raw')).write_bytes(out.stderr)
 receipt={'started_utc':start,'completed_utc':now(),'returncode':out.returncode,'argv':cmd,'stdout':{'bytes':len(out.stdout),'sha256':sha(out.stdout)},'stderr':{'bytes':len(out.stderr),'sha256':sha(out.stderr)},'externally_authenticated_initial_suite_sha256':sha(suite),'captured_initial_suite_compile_optimization':0,'actual_interpreter_outer_mode':mode,'actual_service_mutations':0,'private_cold_copy':True}
 (D/('OFFLINE_'+mode+'.launch.json')).write_text(json.dumps(receipt,indent=2)+'\n');receipts.append(receipt)
 assert out.returncode==0,(mode,out.stderr.decode())
 j=json.loads(out.stdout);assert j['event_count']==200 and j['outer_optimization']==len(flags[0])-1 if flags else j['event_count']==200 and j['outer_optimization']==0
print(json.dumps([{'mode':r['actual_interpreter_outer_mode'],'returncode':r['returncode'],'stdout':r['stdout']} for r in receipts],indent=2))
