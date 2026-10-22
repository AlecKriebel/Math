import pathlib,subprocess,json,hashlib,shutil,sys,datetime,concurrent.futures
R=pathlib.Path(__file__).resolve().parent;A=R.parents[1];P=A.parents[1];E=A/'operations_engineering_04';G=A/'preprint/package/engineering';pin='14ac4e7009a1f4973f81aed776d5c6afd344dea93ff369dd65175427e0492eec';out=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def run_mode(label,flag,opt):
 root=R/'private/suites'/label;pc=root/P.name;ec=pc/'audits/pr952_10400145/operations_engineering_04';ac=ec.parent;ec.mkdir(parents=True);gc=root/'engineering';gc.mkdir();work=root/'work';work.mkdir()
 copied={}
 for name in ['accept_pr952.py',*[]]:
  b=(P/name).read_bytes();(pc/name).write_bytes(b);copied[str(P/name)]={'bytes':len(b),'sha256':sha(b)}
 for name in ['test_operations_proposal.py','test_source_gate_proposal.py','test_native_recovery_proposal.py','test_finalization_logs_recovery.py','BASE_accept_pr952.py','PROPOSED_accept_pr952.py','HISTORICAL_PRE_NATIVE_RECOVERY_accept_pr952.py','HISTORICAL_PROPOSAL04_LOG_GAP_accept_pr952.py']:
  b=(E/name).read_bytes();(ec/name).write_bytes(b);copied[str(E/name)]={'bytes':len(b),'sha256':sha(b)}
 for name in ['source_record_private.txt','ORIGINAL_FILE_RECORDS.json']:(ac/name).write_bytes((A/name).read_bytes())
 shutil.copytree(A/'original',ac/'original');shutil.copytree(A/'original',root/'original');
 for name in ['test_profile.py','test_observations.py','observation_checks.py','verify_package.py','independent_math.py']:
  b=(G/name).read_bytes();(gc/name).write_bytes(b);copied[str(G/name)]={'bytes':len(b),'sha256':sha(b)}
 scripts=[('profile',gc/'test_profile.py',['--originals',str(root/'original/unsolved_math_prioritization/attempts/10400145'),'--verifier-sha256',sha((gc/'verify_package.py').read_bytes()),'--work-dir',str(work)]),('observations',gc/'test_observations.py',[sha((gc/'observation_checks.py').read_bytes())]),('operations',ec/'test_operations_proposal.py',['--core-sha256',pin,'--installed']),('source',ec/'test_source_gate_proposal.py',['--core-sha256',pin,'--installed']),('native',ec/'test_native_recovery_proposal.py',['--proposal-sha256',pin,'--installed']),('finalization',ec/'test_finalization_logs_recovery.py',['--proposal-sha256',pin,'--installed'])]
 rows=[]
 for suite,script,args in scripts:
  cmd=[sys.executable,'-I','-S','-B',*flag,str(script),*args];start=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.run(cmd,cwd=root,capture_output=True);end=datetime.datetime.now(datetime.timezone.utc).isoformat();prefix=R/('SUITE_'+suite+'_'+label);pathlib.Path(str(prefix)+'.stdout.raw').write_bytes(p.stdout);pathlib.Path(str(prefix)+'.stderr.raw').write_bytes(p.stderr);obj=json.loads(p.stdout) if p.returncode==0 else {};launch={'start':start,'end':end,'argv':cmd,'returncode':p.returncode,'outer_optimization':opt,'core_compile_optimization':opt if suite in ('operations','source','native','finalization','profile') else 0,'source_sha256':sha(script.read_bytes()),'exact_unmodified_test_source':True};pathlib.Path(str(prefix)+'.launch.json').write_text(json.dumps(launch,indent=2)+'\n');row={'suite':suite,'mode':label,'returncode':p.returncode,'events':obj.get('event_count',len(obj.get('tests',obj.get('events',[])))),'observed_outer_optimization':obj.get('outer_optimization',obj.get('outer_test_optimization')),'compile_optimization':launch['core_compile_optimization']};rows.append(row);print(json.dumps(row),flush=True)
 return {'mode':label,'copied_public_source_pins':copied,'rows':rows}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:out=list(pool.map(lambda x:run_mode(*x),[('normal',[],0),('O',['-O'],1),('OO',['-OO'],2)]))
(R/'SUITE_REPLAY.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'results':out,'all_returncodes_zero':all(r['returncode']==0 for m in out for r in m['rows']),'real_service_or_Git_mutations':0},indent=2)+'\n')
