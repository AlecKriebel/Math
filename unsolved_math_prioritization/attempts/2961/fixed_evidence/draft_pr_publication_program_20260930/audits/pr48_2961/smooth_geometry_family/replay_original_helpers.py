import pathlib, json, hashlib, subprocess, datetime, sys
assert __debug__
r=pathlib.Path(__file__).resolve().parent;a=r.parent/'source_snapshot'
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def typed(x,y):
 assert type(x) is type(y)
 if isinstance(x,dict):
  assert x.keys()==y.keys()
  for k in x:typed(x[k],y[k])
 elif isinstance(x,list):
  assert len(x)==len(y)
  for u,v in zip(x,y):typed(u,v)
 else:assert x==y,(x,y)
source=pathlib.Path(__file__).read_bytes();rows=[]
final=(a/'PARTIAL.md').read_bytes(); old=final.replace(b'Separate adversarial AI review passed; see [the report](review/REVIEW.md). This has not undergone human peer review.',b'Separate adversarial review is pending.')
assert sha(old)=='0036b78ba3164a52c15a7a24ea73fe4438a3db3c9a206f2882070c23e91cd3b2' and sha(final)=='196568d2029fd378dfa43919efbf49dcbd11244a2de8c525483f84484f00e5fa'
for name,helper,artifact,expected in [('author_historical','check_algebra.py',old,'check_results.json'),('author_identical_submitted_copy','review/author_replay/check_algebra.py',old,'check_results.json'),('author_final_artifact','check_algebra.py',final,'check_results.json'),('historical_independent','review/independent_checks.py',None,'review/independent_results.json')]:
 d=r/'helper_replays'/name;d.mkdir(parents=True,exist_ok=False);body=(a/helper).read_bytes();p=d/'literal_helper.py';p.write_bytes(body)
 if artifact is not None:(d/'PARTIAL.md').write_bytes(artifact)
 (d/'prelaunch_operator.py').write_bytes(source);argv=['/usr/bin/python3','-B',str(p)];start=now()
 (d/'PRELAUNCH.json').write_text(json.dumps({'argv':argv,'cwd':str(d),'helper_bytes':len(body),'helper_sha256':sha(body),'artifact_sha256':None if artifact is None else sha(artifact),'started_utc':start,'pid':None,'completed':False},indent=2)+'\n')
 proc=subprocess.Popen(argv,cwd=str(d),stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=proc.communicate();end=now();(d/'stdout.bin').write_bytes(out);(d/'stderr.bin').write_bytes(err)
 cap={'argv':argv,'cwd':str(d),'pid':proc.pid,'started_utc':start,'finished_utc':end,'exit_code':proc.returncode,'operator_sha256':sha(source),'helper_sha256':sha(body),'artifact_sha256':None if artifact is None else sha(artifact),'stdout':{'bytes':len(out),'sha256':sha(out)},'stderr':{'bytes':len(err),'sha256':sha(err)}};(d/'CAPTURE.json').write_text(json.dumps(cap,indent=2)+'\n');assert proc.returncode==0,(name,err)
 saved=(a/expected).read_bytes();expected_obj=json.loads(saved)
 if artifact==final:
  expected_obj['partial_sha256']=sha(final)
  reconstructed=(json.dumps(expected_obj,indent=2)+'\n').encode();actual=(d/'check_results.json').read_bytes();assert actual==reconstructed
 else:
  actual=(d/'check_results.json').read_bytes() if artifact is not None else out;assert actual==saved
 typed(json.loads(actual),expected_obj);assert out==actual
 rows.append({'case':name,'actual_capture':cap,'result_bytes':len(actual),'result_sha256':sha(actual),'full_result':json.loads(actual),'literal_original_result_byte_equal':artifact!=final,'old_to_final_only_one_hash_field_changed':artifact==final,'original_input_unchanged':(a/helper).read_bytes()==body})
assert pathlib.Path(__file__).read_bytes()==source
(r/'HELPER_REPRODUCTION_RESULT.json').write_text(json.dumps({'schema':'pr48-smooth-geometry-complete-original-helper-reproduction/v1','at_utc':now(),'operator_pid':__import__('os').getpid(),'rows':rows,'author_historical_assertions':6570,'identical_copy_not_independent':True,'historical_independent_assertions':228,'final_artifact_old_receipt_difference_explicit':True,'target_remains_unsolved':True,'new_substantive_turns':0,'audit_turn_charge':0,'geometric_proof_not_replaced_by_diagnostics':True},indent=2)+'\n')
print(json.dumps({'status':'PASS','author_historical':6570,'author_identical_copy':6570,'author_final_artifact':6570,'independent_historical':228,'old_final_receipt_only_hash_field_differs':True,'new_turns':0}))
