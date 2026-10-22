import pathlib,shutil,hashlib,subprocess,sys,datetime,json,os
R=pathlib.Path('/Users/alec/Documents/Math');A=R/'draft_pr_claimed_solved_900_1000_20261012/audits/pr967_2616';D=A/'reviews/closure_package_adversary_01';T=D/'private_tmp';O=A/'original/unsolved_math_prioritization/attempts/2616';C=T/'original_cold_final';shutil.copytree(O,C);(T/'original_exec_tmp_final').mkdir()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
records=json.loads((A/'ORIGINAL_FILE_RECORDS.json').read_text())['files']
for name,e in records.items():
 p=C/name.removeprefix('unsolved_math_prioritization/attempts/2616/');b=p.read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256']
loader="import pathlib,hashlib,sys; p=pathlib.Path(sys.argv[1]); raw=p.read_bytes(); expected=sys.argv[2]; exec('if hashlib.sha256(raw).hexdigest()!=expected: raise RuntimeError(\"external initial source pin mismatch\")'); sys.argv=[str(p),*sys.argv[3:]]; exec(compile(raw,str(p),'exec',dont_inherit=True,optimize=sys.flags.optimize),{'__name__':'__main__','__file__':str(p)})"
env=dict(os.environ);env.update(TMPDIR=str(T/'original_exec_tmp_final'),TMP=str(T/'original_exec_tmp_final'),TEMP=str(T/'original_exec_tmp_final'))
rows=[]
for mode,flags in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
 for script,pin,args in [('BOOTSTRAP.py','128bfd14af0273eb4bd850ae95be8a0cbe908795c0032c003894809d733575b5',[str(C)]),('mutation_tests.py','bfdce9c386882fdb92840e977a6466fe4c4618d0094429e7651396d574fc9ce6',['--root',str(C),'--bootstrap-sha256','128bfd14af0273eb4bd850ae95be8a0cbe908795c0032c003894809d733575b5'])]:
  cmd=[sys.executable,'-I','-S','-B',*flags,'-c',loader,str(C/script),pin,*args];start=now();out=subprocess.run(cmd,cwd=C,capture_output=True,timeout=240,env=env);label=script.replace('.py','')+'_'+mode
  (D/(label+'.stdout.raw')).write_bytes(out.stdout);(D/(label+'.stderr.raw')).write_bytes(out.stderr)
  row={'label':label,'argv':cmd,'started_utc':start,'completed_utc':now(),'returncode':out.returncode,'stdout':{'bytes':len(out.stdout),'sha256':sha(out.stdout)},'stderr':{'bytes':len(out.stderr),'sha256':sha(out.stderr)},'authenticated_initial_sha256':pin,'actual_uid':os.getuid(),'private_cold_copy':True};rows.append(row)
  assert out.returncode==0,(label,out.stderr.decode());j=json.loads(out.stdout);assert j['status']=='PASS';assert j.get('negative_controls',53)==53
out={'utc':now(),'actual_python':sys.version,'uid':os.getuid(),'historical_runtime_not_reproduced':True,'original_directory_write_probes':'NOT_RUN','new_private_copy_writes_only':True,'runs':rows};(D/'ORIGINAL_REPRODUCTIONS.json').write_text(json.dumps(out,indent=2)+'\n')
orig=(C/'author/public/verify.py').read_bytes();supp=(A/'supplemental/verify_robust.py').read_bytes();assert sha(supp)=='05ad68c46fa8ffa56a002786d5178dfaae558f671208b36912ee45711a99c07e'
old=b'except (Invalid, ValueError, TypeError, KeyError, OSError, UnicodeError) as exc:';new=b'except (Invalid, ValueError, TypeError, KeyError, OSError, UnicodeError, RecursionError) as exc:'
assert orig.count(old)==1 and orig.replace(old,new)==supp
fixture=(C/'author/public/fixtures.json').read_bytes();(T/'verify_robust.py').write_bytes(supp)
cases=[('valid_pinned_fixture',fixture,True),('valid_exact65536_boundary',fixture+b' '*(65536-len(fixture)),True),('reject_exact65537_boundary',fixture+b' '*(65537-len(fixture)),False),('deep_array2000',b'['*2000+b'0'+b']'*2000,False),('deep_object2000',b'{"a":'*2000+b'0'+b'}'*2000,False),('deep_array950',b'['*950+b'0'+b']'*950,False),('duplicate_key',fixture.replace(b'"schema_version": 1',b'"schema_version": 1,"schema_version":1'),False),('boolean_integer',fixture.replace(b'"problem_id": 2616',b'"problem_id":true'),False)]
runs=[]
for mode,flags in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
 for label,payload,accept in cases:
  cmd=[sys.executable,'-I','-S','-B',*flags,'-c',loader,str(T/'verify_robust.py'),sha(supp),'--stdin'];start=now();r=subprocess.run(cmd,input=payload,cwd=T,capture_output=True,timeout=30,env=env)
  assert (r.returncode==0)==accept and json.loads(r.stdout if accept else r.stderr)['ok'] is accept
  runs.append({'mode':mode,'label':label,'argv':cmd,'started_utc':start,'completed_utc':now(),'input_bytes':len(payload),'input_sha256':sha(payload),'returncode':r.returncode,'stdout':r.stdout.decode(),'stderr':r.stderr.decode(),'expected_accept':accept})
 origcmd=[sys.executable,'-I','-S','-B',*flags,'-c',loader,str(C/'author/public/verify.py'),sha(orig),'--stdin'];start=now();r=subprocess.run(origcmd,input=b'['*2000+b'0'+b']'*2000,cwd=T,capture_output=True,timeout=30,env=env)
 assert r.returncode!=0 and b'RecursionError' in r.stderr
 runs.append({'mode':mode,'label':'original_deep_array2000_adverse_retained','argv':origcmd,'started_utc':start,'completed_utc':now(),'returncode':r.returncode,'stdout':r.stdout.decode(),'stderr':r.stderr.decode(),'uncaught_RecursionError':True})
(D/'SUPPLEMENTAL_REPRODUCTIONS.json').write_text(json.dumps({'utc':now(),'supplemental_sha256':sha(supp),'one_catch_only_change':True,'supplemental_actual_case_count':24,'original_adverse_case_count':3,'runs':runs},indent=2)+'\n')
print(json.dumps({'full_original_runs':len(rows),'supplemental_cases':24,'original_adverse_retained':3,'uid':os.getuid(),'python':sys.version.split()[0]}))
