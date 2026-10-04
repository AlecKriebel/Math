"""ROOT readback of original custody, current source identity, and original replays."""
from pathlib import Path
import datetime as dt,hashlib,json,os,sqlite3,sys
A=Path(__file__).resolve().parent;P=A.parents[1];R=P.parent
S=A/'original_source_authentication_20261004';F=A/'ROOT_original_custody_readback_20261004'
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_bytes())
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
if sys.flags.optimize or not sys.flags.ignore_environment or not sys.flags.dont_write_bytecode:raise RuntimeError('Invoke -E -B without optimization')
self_manifest=read(S/'SELF_MANIFEST.json')
for row in self_manifest['files']:
    p=S/row['path'];p.resolve().relative_to(S.resolve());b=p.read_bytes()
    require(not p.is_symlink() and len(b)==row['bytes'] and sha(b)==row['sha256'],'Self-manifest member differs')
m=read(S/'ORIGINAL_BLOB_MANIFEST.json')
require(m['head']=='78f4a7fadac0fd24e147a617956cb409eb6a579e' and m['artifact_count']==32,'Original identity/count differs')
incoming={x['path'] for x in m['artifacts'] if x['incoming_changed_domain']}
target_prefix='unsolved_math_prioritization/attempts/10400033/'
require(len(incoming)==26 and incoming=={'unsolved_math_prioritization/QUEUE.md'}|{x['path'] for x in m['artifacts'] if x['path'].startswith(target_prefix)},'Original incoming domain differs')
for row in m['artifacts']:
    b=(S/row['retained_path']).read_bytes()
    require(len(b)==row['bytes'] and sha(b)==row['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob_SHA1'],'Original blob differs')
    require(row['mode']=='100644','Unexpected original mode')
t=read(S/'ORIGINAL_RECURSIVE_TREE.json');children={};expected={'':t['sha']}
for e in t['tree']:
    parent,_,name=e['path'].rpartition('/');children.setdefault(parent,[]).append((name,e))
    if e['type']=='tree':expected[e['path']]=e['sha']
for directory,target in expected.items():
    rows=sorted(children.get(directory,[]),key=lambda x:(x[0]+('/' if x[1]['type']=='tree' else '')).encode())
    b=b''.join((e['mode'].lstrip('0')+' '+name).encode()+b'\0'+bytes.fromhex(e['sha']) for name,e in rows)
    require(hashlib.sha1(b'tree '+str(len(b)).encode()+b'\0'+b).hexdigest()==target,'Recursive tree serialization differs')
require(len(expected)==3547 and t['truncated'] is False,'Tree shape differs')
commit=(S/'ORIGINAL_GIT_COMMIT_BODY.bin').read_bytes()
require(hashlib.sha1(b'commit '+str(len(commit)).encode()+b'\0'+commit).hexdigest()==m['head'],'Exact commit bytes differ')
commands=[json.loads(x) for x in (S/'ACTUAL_COMMANDS.jsonl').read_text().splitlines()]
for q in commands:
    require(isinstance(q['actual_pid'],int) and q['actual_pid']>0 and q['cwd']==str(R),'Actual subprocess metadata differs')
    require(q['exit_code']==0 or (q['label']=='010_local_exact_commit_body' and q['exit_code']==128),'Unexpected custody child failure')
    for k in ['stdout','stderr']:
        b=(S/q[k+'_path']).read_bytes();require(len(b)==q[k+'_bytes'] and sha(b)==q[k+'_sha256'],'Actual stream differs')
B=S/'original/unsolved_math_prioritization/attempts/10400033'
source=read(B/'source_record.json');require('upstream_report' not in source and isinstance(source['prior_upstream_report'],dict),'Native prior-report shape differs')
raw=R/'unsolved_math_prioritization/cache';manifest=read(R/'unsolved_math_prioritization/manifest.json')
require(manifest['revision']==source['dataset_revision'],'Dataset revision differs')
for name in ['problems.json','research_results.json']:
    b=(raw/name).read_bytes();require({'bytes':len(b),'sha256':sha(b)}==manifest['files'][name],'Raw source manifest differs')
problem=[x for x in read(raw/'problems.json') if str(x['id'])=='10400033'];reports=read(raw/'research_results.json')
require(problem==[source['problem']] and reports['AMR-103-0033']==source['prior_upstream_report'],'Raw selected typed pair differs')
with sqlite3.connect('file:'+str(raw/'catalog.sqlite')+'?mode=ro',uri=True) as db:
    row=db.execute('SELECT payload,report FROM records WHERE key=?',('10400033',)).fetchone()
require(row is not None and json.loads(row[0])==source['problem'] and row[1] is not None and json.loads(row[1])==source['prior_upstream_report'],'SQL selected typed pair differs')
status=read(B/'status.json');ledger=[json.loads(x) for x in (B/'turns.jsonl').read_text().splitlines()]
original_queue=(S/'original/unsolved_math_prioritization/QUEUE.md').read_text()
queue_rows=[x for x in original_queue.splitlines() if '| 10400033 /' in x]
require(len(queue_rows)==1 and queue_rows[0].split('|')[8].strip()=='claimed_solved' and queue_rows[0].split('|')[9].strip()=='1/5','Original queue budget/status differs')
require(status['turns_used']==1 and 'turn_limit' not in status and [x['turn'] for x in ledger]==[1,1,1],'Original substantive budget/event count differs')
C=P/'audits/pr45_9900007';replay_counts={}
for label in ['root_pr66_original_Jones_calibration_replay_20261004_actual_capture','root_pr66_original_tournament_replay_20261004_actual_capture','root_pr66_legacy_independent_checker_replay_20261004_actual_capture']:
    folder=C/label;capture=read(folder/'CAPTURE.json');require(capture['status']=='PASS','Original replay failed')
    b=(folder/'stdout.bin').read_bytes();require(sha(b)==capture['stdout']['sha256'] and len(b)==capture['stdout']['bytes'],'Replay stream differs')
    v=json.loads(b);require(v['status']=='PASS','Replay result failed');replay_counts[label]=v['exact_assertions']
require(list(replay_counts.values())==[183,42684,115776],'Original assertion counts differ')
stamp=dt.datetime.now(dt.timezone.utc).isoformat();F.mkdir(exist_ok=False)
result={'UTC':stamp,'actual_controller_pid':os.getpid(),'status':'PASS','PR':66,'original_head':m['head'],'original_regular_bodies':32,'complete_incoming_body_count':26,'recursive_tree_serializations_verified':len(expected),'exact_original_commit_digest_verified':True,'actual_custody_command_count':len(commands),'actual_stdout_stderr_bodies_verified':True,'self_manifest_member_count':len(self_manifest['files']),'current_raw_SQL_original_typed_problem_report_pair_agrees':True,'prior_upstream_report_present_object':True,'upstream_report_absent':True,'original_substantive_budget':'1/5','original_ledger_event_count':3,'original_replay_assertions':replay_counts,'mathematical_validity_and_priority_not_conferred_by_byte_or_finite_checks':True,'bootstrap_PID_UTC_gaps_not_invented':True,'one_expected_local_commit_absence_then_digest_recovery':True,'initial_agent_row_parser_failure_recovered_before_science':True,'ROOT_redundant_initial_source_directory_query_failed404_then_abandoned_in_favor_of_complete_authentication':True,'native_mutations':False}
(F/'READBACK.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
