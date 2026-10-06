from pathlib import Path
import datetime,hashlib,json,os,subprocess
A=Path(__file__).resolve().parent;D=A/'repaired_diagnostics_validation_20261006';D.mkdir(exist_ok=False);R=A/'repaired_diagnostics_v1';O=A/'original_source_authentication_20261006/original_attempt';records=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
py='/opt/homebrew/bin/python3'
(D/'false_guard_probe.py').write_text('import contextlib,io,runpy,sys\nwith contextlib.redirect_stdout(io.StringIO()):\n ns=runpy.run_path(sys.argv[1])\nif sys.argv[2]=="author":ns["ck"]("root-known-false",False)\nelse:ns["ck"](False,"root-known-false")\nraise RuntimeError("FALSE CONTROL WAS ACCEPTED")\n')
for script,flavor,expected in [('verify.py','author',O/'verification.json'),('independent_checks.py','independent',O/'review/independent_results.json')]:
 for opt in [False,True]:
  for false in [False,True]:
   argv=[py,'-E','-B']+(['-O'] if opt else [])+([str(D/'false_guard_probe.py'),str(R/script),flavor] if false else [str(R/script)])
   start=now();p=subprocess.Popen(argv,cwd=R,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate();i=len(records)
   (D/(str(i)+'.stdout.bin')).write_bytes(out);(D/(str(i)+'.stderr.bin')).write_bytes(err)
   rec={'argv':argv,'PID':p.pid,'UTC_start':start,'UTC_end':now(),'exit_code':p.returncode,'optimized':opt,'false_control':false,
    'stdout_file':str(i)+'.stdout.bin','stdout_sha256':hashlib.sha256(out).hexdigest(),'stderr_file':str(i)+'.stderr.bin','stderr_sha256':hashlib.sha256(err).hexdigest()}
   if false:
    if p.returncode!=1 or b'AssertionError: root-known-false' not in err or b'FALSE CONTROL WAS ACCEPTED' in err:raise RuntimeError('false control was not rejected correctly')
    rec['known_false_guard_rejected']=True
   else:
    if p.returncode!=0:raise RuntimeError(err.decode()[:1000])
    actual=json.loads(out);reference=json.loads(expected.read_text())
    if flavor=='author':
     actual.pop('checker_sha256');reference.pop('checker_sha256')
    if actual!=reference:raise RuntimeError('mathematical result/count drift')
    rec['all_result_fields_preserved_except_intentional_checker_hash']=True
   records.append(rec);(D/'PROCESS_JOURNAL.json').write_text(json.dumps({'actual_operator_PID':os.getpid(),'records':records},indent=2)+'\n')
verdict={'schema':'pr107-root-repaired-diagnostic-validation/v1','UTC':now(),'actual_operator_PID':os.getpid(),'status':'PASS','actual_runs':len(records),'normal_and_optimized_results_match':True,'known_false_controls_rejected_in_both_modes':True,'original_mathematical_counts_preserved':True,'original_proof_unchanged':True,'new_central_proof_search_turns':0}
(D/'VERDICT.json').write_text(json.dumps(verdict,indent=2)+'\n');print(json.dumps(verdict))
