"""SYNTHETIC_NON_RECEIPT. Bounded local Python child runner, never an operations dispatcher."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import datetime,hashlib,json,subprocess,time
ROOT=Path(__file__).resolve().parent
VERSION=sys.argv[1]
PY='/opt/homebrew/opt/python@3.14/bin/python3.14'
RUNS=ROOT/('runs_'+VERSION);RUNS.mkdir(exist_ok=False)
def pin(path):
 raw=path.read_bytes();return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
CASES=['flag_ignore_environment','flag_no_site','flag_dont_write_bytecode','flag_safe_path','flag_optimize','flag_real_optimized','preflight','route_publisher','route_tracker','help','systemexit_none','systemexit_zero','systemexit_bool','systemexit_text','baseexception_tracker','error_preflight','error_publisher','error_tracker','parser_bad_int','parser_unknown','auth_basename','auth_adoption','auth_gate','auth_ready','auth_self','auth_source','auth_source_mode','auth_source_symlink','auth_source_set','cleanup_common_compile','cleanup_common_compile_absent','cleanup_selected_compile','cleanup_selected_compile_absent','cleanup_selected_main','cleanup_selected_main_absent','cleanup_invalid_confirm_publisher','safe_regular','safe_fifo','safe_directory','safe_symlink','safe_mode','safe_oversize','safe_race_fifo','safe_race_directory','safe_race_symlink','safe_race_oversize','safe_socket_kind','safe_char_kind','parser_bad_confirm','parser_choice','parser_missing','route_publisher_inspect','route_publisher_publish','route_publisher_inspect-doi','route_publisher_finalize','route_tracker_recover','route_publisher_inspect_confirm','route_publisher_publish_confirm','route_publisher_inspect-doi_confirm']
rows=[]
for case in CASES+(['baseline_v2_fifo'] if VERSION=='v3' else []):
 version='v2' if case=='baseline_v2_fifo' else VERSION;probe='safe_fifo' if case=='baseline_v2_fifo' else case;runid=VERSION+'__'+case
 argv=[PY,'-E','-S','-B','-P']+(['-O'] if case=='flag_real_optimized' else [])+[str(ROOT/'probe_child_v4.py'),probe,version,runid]
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();tic=time.monotonic();timedout=False
 try:proc=subprocess.run(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=3);exitcode=proc.returncode;stdout=proc.stdout;stderr=proc.stderr
 except subprocess.TimeoutExpired as e:timedout=True;exitcode=None;stdout=e.stdout or b'';stderr=e.stderr or b''
 (RUNS/(case+'.stdout')).write_bytes(stdout);(RUNS/(case+'.stderr')).write_bytes(stderr)
 meta=ROOT/'fixtures'/runid/'probe_result.json';m=json.loads(meta.read_bytes()) if meta.exists() else None
 failures=[]
 if case=='baseline_v2_fifo':status='EXPECTED_V2_FIFO_BLOCK' if timedout else 'BASELINE_CHANGED';failures=[] if timedout else ['v2 did not reproduce known blocking']
 else:
  if timedout:failures.append('bounded child timeout')
  if not m or m.get('status')!='PASS':failures.append('child harness/source assertions failed')
  failedentry=case.startswith(('auth_','cleanup_','error_')) or case in ('systemexit_bool','systemexit_text','baseexception_tracker','parser_bad_int','parser_unknown','parser_bad_confirm','parser_choice','parser_missing')
  expected_exit=1 if failedentry else 0
  if exitcode!=expected_exit:failures.append('actual exit differs expected '+str(expected_exit))
  if failedentry:
   expected_types={'parser_bad_int':'RuntimeError' if VERSION!='v3' else 'SystemExit','parser_unknown':'RuntimeError' if VERSION!='v3' else 'SystemExit','parser_bad_confirm':'RuntimeError','parser_choice':'RuntimeError','parser_missing':'RuntimeError','systemexit_bool':'SystemExit','systemexit_text':'SystemExit','baseexception_tracker':'KeyboardInterrupt','error_preflight':'RuntimeError','error_publisher':'RuntimeError','error_tracker':'OSError'}
   typename=expected_types.get(case)
   if typename is not None and stderr!=('Root PR206 operations failed: '+typename+'\n').encode():failures.append('failure output not exact type-only diagnostic')
   if b'SYNTHETIC_RAW_EXCEPTION_BODY_91' in stdout+stderr or b'Traceback' in stdout+stderr:failures.append('raw body/chaining/traceback leaked')
   if stdout:failures.append('failed entry stdout must be empty')
  elif case=='help':
   if b'usage:' not in stdout or stderr:failures.append('clean help0 output changed')
  elif stderr:failures.append('unexpected stderr')
  status='PASS' if not failures else 'CONTRACT_OR_HARNESS_FAILURE'
 rows.append({'case':case,'source_version':version,'source_pin':pin(ROOT/('reviewed_dispatcher_'+version+'.py')),'argv':argv,'UTC_start':start,'UTC_end':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-tic,'timeout_seconds':3,'timed_out_and_child_killed':timedout,'exit':exitcode,'expected_status':status,'failures':failures,'stdout':{'path':str((RUNS/(case+'.stdout')).relative_to(ROOT)),**pin(RUNS/(case+'.stdout'))},'stderr':{'path':str((RUNS/(case+'.stderr')).relative_to(ROOT)),**pin(RUNS/(case+'.stderr'))},'metadata':{'path':str(meta.relative_to(ROOT)),**pin(meta)} if meta.exists() else None,'child_check_count':len(m.get('checks',[])) if m else 0})
result={'SYNTHETIC_NON_RECEIPT':True,'source_version':VERSION,'status':'PASS' if not any(x['failures'] for x in rows) else 'FINDING_OR_HARNESS_FAILURE','cases':rows,'case_count':len(rows),'child_check_count':sum(x['child_check_count'] for x in rows),'failed_cases':[x['case'] for x in rows if x['failures']],'python_binary':{'path':str(Path(PY).resolve()),**pin(Path(PY).resolve())},'child_harness':pin(ROOT/'probe_child_v4.py'),'controller':pin(Path(__file__)),'actual_service_calls':0,'actual_ops_receipts':False,'prior_audit_unchanged':True}
(ROOT/('RESULT_'+VERSION+'.json')).write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ('status','source_version','case_count','child_check_count','failed_cases')},sort_keys=True))
raise SystemExit(0 if result['status']=='PASS' else 1)
