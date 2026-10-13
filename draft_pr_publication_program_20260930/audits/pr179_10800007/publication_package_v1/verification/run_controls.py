"""Replay fifteen exact control models in ordinary and optimized Python."""
from pathlib import Path
import argparse,datetime,hashlib,json,subprocess,sys
BASE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(v,label):
 if not v:raise RuntimeError(label)
def now():return datetime.datetime.now(datetime.UTC).isoformat()
EXPECTED={
'baseline':None,'positive_control_reverse_orientation':None,
'wrong_embedding_b0':'universal_second_slice_identity',
'wrong_system_xy':'universal_second_slice_identity',
'wrong_general_jacobian':'universal_general_jacobian',
'wrong_path_seam':'universal_path_nonzero_and_bounded',
'wrong_path_bound':'universal_path_nonzero_and_bounded',
'bounded_but_discontinuous_seam':'polynomial_path_continuous_join',
'root_endpoints_equal':'exact_path_endpoints',
'path_through_zero':'universal_path_nonzero_and_bounded',
'zero_scale':'positive_example_scale',
'touching_open_disk_boundary':'strict_example_disk_inclusion',
'continuous_hidden_zero':'supported_norm_degree_at_most_two',
'negative_jacobian_exponent':'nonnegative_integer_jacobian_power',
'unknown_jacobian_variable':'supported_jacobian_variable'}
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path);args=parser.parse_args()
 if args.output:require(not args.output.exists(),'Existing replay receipt: choose a new output path')
 started=now();checker=BASE/'verify.py';cpin=sha(checker);proofpin=sha(BASE/'MANUSCRIPT.tex')
 expectations=json.loads((BASE/'CONTROL_EXPECTATIONS.json').read_text())
 require(set(expectations['positive_models'])=={k for k,v in EXPECTED.items() if v is None},'Positive catalogue mismatch')
 require(set(expectations['scientifically_invalid_or_unsupported_models'])=={k for k,v in EXPECTED.items() if v is not None},'Negative catalogue mismatch')
 rows=[]
 for name,reason in EXPECTED.items():
  model=BASE/'models'/(name+'.json');mpin=sha(model)
  for mode,flags in [('ordinary',[]),('optimized',['-O'])]:
   command=[sys.executable,'-E','-S','-B','-P',*flags,str(checker),str(model)]
   begin=now();r=subprocess.run(command,cwd=BASE,capture_output=True,text=True,timeout=30);end=now()
   require(sha(checker)==cpin and sha(model)==mpin and sha(BASE/'MANUSCRIPT.tex')==proofpin,'Replay input drift')
   raw=r.stdout if reason is None else r.stderr
   data=json.loads(raw)
   if reason is None:
    require(r.returncode==0 and data['status']=='PASS' and not r.stderr,'Baseline replay failure')
    require(data['checker_sha256']==cpin and data['model_sha256']==mpin,'Child input hash mismatch')
    require(data['topological_assumptions_verified_by_code'] is False,'Unsupported topological certification')
   else:require(r.returncode==1 and data.get('status')=='FAIL' and data.get('reason')==reason and not r.stdout,'Scientific negative-control failure')
   rows.append({'model':'models/'+name+'.json','mode':mode,'started_UTC':begin,'finished_UTC':end,
   'command':command,'cwd':str(BASE),'returncode':r.returncode,
   'expected_status':'PASS' if reason is None else 'FAIL','actual_status':data['status'],
   'expected_reason':reason,'actual_reason':data.get('reason'),'model_SHA256':mpin,
   'checker_SHA256':cpin,'stdout':r.stdout,'stderr':r.stderr,
   'stdout_SHA256':hashlib.sha256(r.stdout.encode()).hexdigest(),
   'stderr_SHA256':hashlib.sha256(r.stderr.encode()).hexdigest(),'result_matches_scientific_expectation':True})
 result={'status':'ALL_EXACT_CONTROL_EXPECTATIONS_MATCHED','started_UTC':started,'finished_UTC':now(),
 'python_version':sys.version,'python_executable':sys.executable,'checker_SHA256':cpin,
 'driver_SHA256':sha(Path(__file__)),'manuscript_SHA256':proofpin,
 'models':len(EXPECTED),'actual_processes':len(rows),'positive_PASS_runs':sum(x['expected_reason'] is None for x in rows),
 'invalid_or_unsupported_FAIL_runs':sum(x['expected_reason'] is not None for x in rows),
 'topology_is_in_written_proof_not_code':True,'results':rows}
 if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:result[k] for k in ['status','models','actual_processes','positive_PASS_runs','invalid_or_unsupported_FAIL_runs','checker_SHA256','manuscript_SHA256']}))
if __name__=='__main__':main()

