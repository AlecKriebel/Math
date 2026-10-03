"""Bounded readback of every original scientific body and actual private reproduction."""
from pathlib import Path
import datetime,hashlib,json,re
F=Path(__file__).resolve().parent
checks=0
def ck(x):
 global checks;assert x;checks+=1
def digest(b):return hashlib.sha256(b).hexdigest()
def identity(p):
 b=p.read_bytes();return {'path':str(p.resolve()),'bytes':len(b),'sha256':digest(b),'mode':format(p.stat().st_mode&0o7777,'04o')}
auth=json.loads((F/'ORIGINAL_AUTHENTICATION.json').read_bytes());ck(auth['head']=='d40d2dae4cff2a5e5a1e12e9a2f8bc3987431c1a');ck(auth['science_file_count']==19)
diff=(F/'captures/original_full_diff/STDOUT.bin').read_bytes();blocks=diff.split(b'diff --git ')[1:];ck(len(blocks)==20);bodyrows=[]
for row in auth['primary_science_files']:
 p=Path(row['local_identity']['path']);body=p.read_bytes();ck(identity(p)==row['local_identity']);ck(hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()==row['git_blob_sha1'])
 block=next(b for b in blocks if b.splitlines()[0]==('a/'+row['repository_path']+' b/'+row['repository_path']).encode());ck(b'new file mode 100644\n' in block)
 patch=b''.join(line[1:]+b'\n' for line in block.splitlines() if line.startswith(b'+') and not line.startswith(b'+++'));ck(patch==body)
 if p.suffix=='.json':json.loads(body);checks+=1
 bodyrows.append(identity(p))
q=next(b for b in blocks if b.splitlines()[0]==b'a/unsolved_math_prioritization/QUEUE.md b/unsolved_math_prioritization/QUEUE.md');minus=[line[1:].decode() for line in q.splitlines() if line.startswith(b'-|')];plus=[line[1:].decode() for line in q.splitlines() if line.startswith(b'+|')];ck(len(minus)==len(plus)==1);ck('30000644 / OWR-1452-008' in minus[0] and '| queued | 0/5 |' in minus[0]);ck('| already_solved | 0/5 |' in plus[0])
proof=F/'original/KNOWN_THEOREM.md';old=F/'original/review/KNOWN_THEOREM.md';replacement=(b'**Disposition: already solved in the original literature. No new solution or novelty claim. Independent source/proof review pending.**',b'**Disposition: already solved in the original literature. No new solution or novelty claim. Independent source/proof review passed; see review/REVIEW.md.**');ck(old.read_bytes().count(replacement[0])==1);ck(old.read_bytes().replace(*replacement)==proof.read_bytes());ck((F/'original/verify.py').read_bytes()==(F/'original/review/submitted_verify.py').read_bytes())
caprows=[]
for d in sorted((F/'captures').iterdir()):
 if d.name=='preparation_readback_v2':
  live=json.loads((d/'PRELAUNCH.json').read_bytes());ck(live['actual_execution'] is False and live['completed'] is False and live['pid'] is None);continue
 pre=json.loads((d/'PRELAUNCH.json').read_bytes());done=json.loads((d/'COMPLETE.json').read_bytes());ck(pre['pid'] is None and pre['actual_execution'] is False and pre['completed'] is False)
 ck(done['actual_execution'] is True and done['completed'] is True and type(done['pid']) is int and done['pid']>0 and type(done['exit_code']) is int);ck(done['created_utc']==pre['created_utc'] and done['created_utc']<=done['finished_utc']);ck(done['argv']==pre['argv'] and done['cwd']==pre['cwd']);ck(done['operator']==identity(d/'OPERATOR_PRELAUNCH.py'));ck(done['operator_unchanged'] is True)
 for n in ['STDOUT.bin','STDERR.bin']:ck(done[n]==identity(d/n))
 for src in done['sources']:
  ck(src['original']==identity(Path(src['original']['path'])));ck(src['saved']==identity(Path(src['saved']['path'])));ck(src['original']['sha256']==src['saved']['sha256'])
 if d.name=='existing_original_git':ck(done['exit_code']==128 and done['status']=='FAIL' and (d/'STDOUT.bin').read_bytes()==b'' and b'could not get object info' in (d/'STDERR.bin').read_bytes())
 elif d.name=='preparation_readback':ck(done['exit_code']==1 and done['status']=='FAIL' and b'FileNotFoundError' in (d/'STDERR.bin').read_bytes() and b'preparation_readback/COMPLETE.json' in (d/'STDERR.bin').read_bytes())
 else:ck(done['exit_code']==0 and done['status']=='PASS' and (d/'STDERR.bin').read_bytes()==b'')
 caprows.append({'name':d.name,'complete':identity(d/'COMPLETE.json'),'pid':done['pid'],'exit_code':done['exit_code']})
commands=json.loads((F/'RETRIEVAL_COMMANDS.json').read_bytes());ck(len(commands)==24)
for x in commands:
 ck(x['actual_execution'] is True and x['completed'] is True and type(x['pid']) is int and x['pid']>0 and x['exit_code']==0);ck(x['started_utc']<=x['finished_utc']);ck(x['operator_source']==identity(F/'retrieve_original.py'));ck(x['stdout']==identity(Path(x['stdout']['path'])));ck(x['stderr']==identity(Path(x['stderr']['path'])) and x['stderr']['bytes']==0)
for replay,expected,count,script in [('author_current','verification.json',211,'verify.py'),('author_frozen','review/submitted_results.json',211,'submitted_verify.py'),('historical_independent','review/independent_results.json',142,'independent_checks.py')]:
 original=F/'original'/expected;p=F/'private_replays'/replay/('independent_results.json' if replay=='historical_independent' else 'verification.json');ck(p.read_bytes()==original.read_bytes());data=json.loads(p.read_bytes());ck(data.get('passed',data.get('assertions'))==count);ck(len(data['checks'])==count and set(data['checks'].values())=={'PASS'});ck(data['sympy_version']=='1.14.0')
 code=F/'original'/('verify.py' if replay=='author_current' else 'review/'+script);ck((F/'private_replays'/replay/script).read_bytes()==code.read_bytes())
v=json.loads((F/'original/review/verdict.json').read_bytes());ck(v['review_sha256']==digest((F/'original/review/REVIEW.md').read_bytes()));ck(v['final_artifact_sha256']==digest(proof.read_bytes()));ck(v['reviewed_artifact_sha256']==digest(old.read_bytes()));a=json.loads((F/'original/attempt.json').read_bytes());t=json.loads((F/'original/turns.json').read_bytes());ck(a['status']=='already_solved' and a['substantive_attempts_used']==0 and a['substantive_attempt_limit']==5 and a['novel_result_claimed'] is False);ck(t['substantive_search_attempts']==0 and len(t['validation_activities'])==1 and t['validation_activities'][0]['charged_as_substantive_search_attempt'] is False)
lit=json.loads((F/'SELECTED_LITERAL_SOURCE.json').read_bytes());ck(lit['raw_research_results_key_present'] is False and lit['raw_research_results_literal_value'] is None);ck(lit['sql_selected_report_literal']=='{}' and lit['original_prior_report_bytes']=='null\n');ck(len(lit['raw_matching_problem_code_records'])==len(lit['raw_exact_normalized_statement_records'])==len(lit['raw_related_term_records'])==1)
primary=json.loads((F/'PRIMARY_DOWNLOAD_LEDGER.json').read_bytes());ck(primary['journal_full_text_retrieved'] is False and len(primary['downloads'])==2);ck(all(x['matches_original_source_provenance'] is True and x['whole_pdf_persisted'] is False for x in primary['downloads']));ck(len(primary['selected_page_commands'])==4)
for c in primary['selected_page_commands']:
 ck(c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['exit_code']==0);ck(c['stdout']==identity(Path(c['stdout']['path'])));ck(c['stderr']==identity(Path(c['stderr']['path'])))
result={'schema':'pr52-original-preparation-readback/v1','status':'PASS_PREPARATION_AUTHENTICATION_AND_LITERAL_REPLAY_ONLY','checks':checks,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'original_science_file_count':19,'original_science_bytes':sum(x['bytes'] for x in bodyrows),'full_diff_bytes':len(diff),'science_body_patch_identity':True,'full_original_science_file_bindings':bodyrows,'actual_captures':caprows,'actual_internal_retrieval_commands':24,'private_replay_current':{'assertions':211,'byte_identical_expected_receipt':True},'private_replay_frozen':{'assertions':211,'byte_identical_expected_receipt':True},'private_replay_historical_independent':{'assertions':142,'byte_identical_expected_receipt':True,'new_independent_mathematical_verdict':False},'original_queue_minus_literal':minus[0],'original_queue_plus_literal':plus[0],'all_root_acceptance_and_publication_authorities':False,'full_journal_proof_certified':False,'source_status_recommendation':'already_solved','native_actions':False}
(F/'PREPARATION_READBACK.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({k:result[k] for k in ['status','checks','original_science_file_count','original_science_bytes','full_diff_bytes','science_body_patch_identity','new_independent_mathematical_verdict'] if k in result},sort_keys=True))
