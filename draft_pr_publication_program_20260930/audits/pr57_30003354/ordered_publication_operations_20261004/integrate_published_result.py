"""Prospective PR57-only exact-head merge and present-day publication mirror.

UNEXECUTED AT SOURCE HANDOFF. Requires ROOT's current final gate after source
reading, actual repository-kit publication and public-file/metadata verification,
actual unique GWS tracker readback, and an acknowledged PR57 exclusive shared
Git/index window. This helper uploads nothing and writes no spreadsheet or PR.
Both phases capture real serial subprocess argv/PID/UTC/exit. Failure preserves
partial state: no reset, stash, abort, branch switch, force push or blind retry.
"""
import argparse, base64, datetime as dt, hashlib, json, os, re, sqlite3, stat, subprocess, sys
from pathlib import Path
HEAD='4ecc453d6f9ec2e64cdb2d4b41c018fffbe85b29'
ID='30003354'; CODE='OWR-15208-008'; QUEUE='unsolved_math_prioritization/QUEUE.md'
PREFIX='unsolved_math_prioritization/attempts/'+ID
STATE='unsolved_math_prioritization/state.json'; HISTORY='unsolved_math_prioritization/history.jsonl'
GOAL=Path('/Users/alec/.codex/attachments/4df73d3d-641f-4907-b9ad-c47c468f2589/goal-objective.md')
GOAL_SHA='1e29852cafce156dbc3b745f9d1b7bf973b6d07e4a3c924b901ad27754128d04'
PAIR_SHA='0bd321aaf672e74ea23dc3a6708a5a2df569df4c51bed66fc17f86cb3dafc6a3'
CLAIM=('For every fixed finite integer r>=0, normalized uniformization on the plane and sphere is discontinuous '
       'from ordinary compact-open C^r metrics to compact-open C^(r+1) maps, witnessed by smooth complete '
       'strictly positive-curvature metrics converging to a smooth admissible metric.')
QUEUE_NOTE=('Verified negative answer for specified normalized uniformization on plane and sphere at every finite integer r>=0; '
            'ordinary compact-open C^r metrics, C^(r+1) normalized maps; smooth complete strictly positive-curvature witnesses; '
            'classical mechanisms credited; bounded priority audit with residual unindexed-realization risk; '
            'AI-assisted, unrefereed; original1/5; exact public files and unique tracker row verified')
def sha(b):return hashlib.sha256(b).hexdigest()
def jb(x):return (json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
def must(ok,m):
 if not ok:raise RuntimeError(m)
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('phase',choices=['merge','mirror']);ap.add_argument('--gate',type=Path,required=True)
 ap.add_argument('--exclusive-window-confirmed',action='store_true',required=True);ap.add_argument('--root-after-source-reading',action='store_true',required=True);args=ap.parse_args()
 must(not sys.flags.optimize and args.exclusive_window_confirmed and args.root_after_source_reading,'Nonoptimized ROOT source-reading/confirmed-window invocation required')
 own=Path(__file__).resolve().parent;audit=own.parent;repo=own.parents[3]
 phase_dir=own/'private'/('integration-'+args.phase);must(not phase_dir.exists(),'Prior attempt exists: preserve and inspect actual partial state; never blindly retry')
 phase_dir.mkdir(parents=True);(phase_dir/'PRELAUNCH_SOURCE.py').write_bytes(Path(__file__).read_bytes());commands=[]
 def run(argv,allowed=(0,)):
  start=dt.datetime.now(dt.timezone.utc).isoformat();proc=subprocess.Popen(argv,cwd=repo,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  out,err=proc.communicate();n=str(len(commands)+1);(phase_dir/(n+'.stdout')).write_bytes(out);(phase_dir/(n+'.stderr')).write_bytes(err)
  commands.append({'argv':argv,'actual_pid':proc.pid,'started_UTC':start,'finished_UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'exit_code':proc.returncode,'stdout_sha256':sha(out),'stderr_sha256':sha(err)})
  (phase_dir/'COMMANDS.json').write_bytes(jb(commands));must(proc.returncode in allowed,'Actual command failed; partial state and real streams retained');return out,proc.returncode
 def git(*x):return run(['git','--no-optional-locks',*x])[0]
 def binding(p):
  p=p.resolve();p.relative_to(repo);return {'path':p.relative_to(repo).as_posix(),'sha256':sha(p.read_bytes())}
 def checked(b):
  must(set(b)=={'path','sha256'},'Evidence binding shape differs');p=repo/b['path'];must(not p.is_symlink(),'Evidence symlink forbidden');p=p.resolve();p.relative_to(repo)
  must(p.is_file() and sha(p.read_bytes())==b['sha256'],'Bound evidence bytes drifted');return p
 # Status-first fresh intake before reading any scientific review/custody.
 initial_pr=json.loads(run(['gh','pr','view','57','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,baseRefName,mergeCommit'])[0])
 must(initial_pr['headRefOid']==HEAD and initial_pr['baseRefName']=='main','Initial incoming identity drifted: stop')
 initial_queue=json.loads(run(['gh','api','repos/AlecKriebel/Math/contents/'+QUEUE+'?ref='+HEAD])[0]);initial_rows=[x for x in base64.b64decode(initial_queue['content']).decode().splitlines() if '| '+ID+' /' in x]
 must(len(initial_rows)==1 and initial_rows[0].split('|')[8].strip()=='claimed_solved' and initial_rows[0].split('|')[9].strip()=='1/5','Initial literal status is not claimed_solved1/5: skip entirely before scientific inputs')
 must((args.phase=='merge' and initial_pr['state']=='OPEN' and initial_pr['isDraft'] is True) or (args.phase=='mirror' and initial_pr['state']=='MERGED'),'Wrong initial phase lifecycle: stop')
 inputs_path=own/'SOURCE_BINDINGS.json';inputs_pin=binding(inputs_path);inputs=json.loads(inputs_path.read_bytes())
 must(inputs['schema']=='pr57-ordered-publication-operation-source-bindings/v1' and inputs['ROOT_authority'] is False and inputs['helper_executed'] is False,'Wrong prospective SOURCE bindings')
 must(binding(Path(__file__))==inputs['integration_helper'],'Operative helper source differs from read SOURCE version')
 gate_path=args.gate.resolve();gate_path.relative_to(audit);gate_pin=binding(gate_path);gate=json.loads(gate_path.read_bytes())
 must(gate['schema']=='pr57-ordered-publication-final-gate/v1' and gate['PR']==57 and gate['reviewed_head']==HEAD and gate['exact_claim']==CLAIM,'Wrong current ROOT gate/head/scope')
 for key in ['publication_authorized','root_personally_read_helper_source','root_personally_revalidated_exact_package','all_current_substantive_findings_resolved','full_specified_finite_integer_source_target_resolved','never_process_initially_nonclaimed_PRs']:
  must(gate[key] is True,'Actual ROOT review/authorization missing: '+key)
 must(gate['eligible_intake_literal_status']=='claimed_solved' and gate['original_budget']=='1/5' and gate['new_central_proof_attempts']==0,'Eligibility/budget differs')
 must(gate['bounded_priority_audit_complete'] is True and gate['worldwide_priority_guarantee'] is False and gate['PR50_exception_extended'] is False,'Bounded priority must not become exception/exhaustive certification')
 must(gate['human_peer_review'] is False and gate['formal_proof_certification'] is False and gate['AI_tools_used_extensively'] is True,'Review qualifications differ')
 must(gate['source_bindings']==inputs_pin and gate['goal_objective_sha256']==GOAL_SHA and sha(GOAL.read_bytes())==GOAL_SHA,'Current gate/source/objective drift')
 for key in ['ROOT_final_package_adjudication','ROOT_priority_adjudication','ROOT_current_exact_package_readback','original_authentication','original_custody','current_SOURCE_custody','priority_custody','manifest','clean_reviews','final_artifacts']:
  must(gate[key]==inputs[key],'ROOT gate must bind exact operative SOURCE input: '+key)
 evidence=[inputs[k] for k in ['ROOT_final_package_adjudication','ROOT_priority_adjudication','ROOT_current_exact_package_readback','original_authentication','original_custody','current_SOURCE_custody','priority_custody','manifest']]+inputs['clean_reviews']+inputs['review_reports']+inputs['review_custodies']+inputs['final_artifacts']
 for p in evidence:checked(p)
 current_readback=json.loads(checked(inputs['ROOT_current_exact_package_readback']).read_bytes())
 must(current_readback['schema']=='pr57-ordered-exact-package-resumption/v1' and current_readback['reviewed_head']==HEAD and current_readback['existing_two_independent_review_rounds_retained'] is True and current_readback['source_or_PDF_edit_or_compile_performed'] is False,'Actual current exact-package ROOT readback differs')
 final=json.loads(checked(inputs['ROOT_final_package_adjudication']).read_bytes())
 must(final['preprint_package_ready_for_ordered_publication'] is True and final['ROOT_all_six_final_PDF_pages_personally_inspected'] is True and final['ROOT_full_final_editorial_diff_and_portable_checker_read'] is True,'Prior exact-package adjudication differs')
 # Frozen 2026-10-03 absence flags remain historical. The actual publication
 # gate below supplies current publication authority; no old packet is edited.
 must(final['actual_external_upload_performed'] is False and final['native_acceptance_completed'] is False and final['DOI'] is None,'Frozen source historical absence flags changed')
 reviews=inputs['clean_reviews'];must(len(reviews)==2 and len({checked(x).parent for x in reviews})==2,'Two distinct independent package review rounds required')
 first=json.loads(checked(reviews[0]).read_bytes());second=json.loads(checked(reviews[1]).read_bytes())
 must(first['verdict']=='PASS_NO_ACTIONABLE_MATHEMATICAL_OR_SCIENTIFIC_CLAIM_DEFECT_FOUND' and not first['mathematical_issues'] and not first['claim_issues'],'Round1 no longer clean')
 must(second['verdict']=='NO_ESSENTIAL_ISSUES_FOUND' and second['all_six_PDF_pages_personally_inspected'] is True,'Final round2 verdict differs')
 for key in ['actionable_mathematical_issues','actionable_scientific_claim_issues','actionable_reproducibility_issues','actionable_PDF_layout_issues','actionable_publication_packet_issues']:
  must(second[key]==[],'Final round2 issue persists')
 def custody(b):
  index=checked(b);records=json.loads(index.read_bytes())['files']
  items=([dict(v,path=k) for k,v in records.items()] if isinstance(records,dict) else records)
  for item in items:
   p=Path(item['path']);p=p if p.is_absolute() else index.parent/p;p.resolve().relative_to(index.parent)
   must(not p.is_symlink() and p.is_file(),'Frozen custody member nonregular/missing');body=p.read_bytes()
   mode=item.get('full_mode_07777',item.get('full_mode',item.get('mode')));mode=int(mode,8) if isinstance(mode,str) else mode
   must(len(body)==item['bytes'] and sha(body)==item['sha256'] and stat.S_IMODE(p.stat().st_mode)==mode,'Frozen custody member body/mode drift')
 for b in [inputs['original_custody'],inputs['current_SOURCE_custody'],inputs['priority_custody']]+inputs['review_custodies']:custody(b)
 manifest_path=checked(inputs['manifest']);must(manifest_path==audit/'publication_package_v1/zenodo-deposit.json','Wrong operative package')
 manifest=json.loads(manifest_path.read_bytes());must(set(manifest)=={'metadata','files'} and len(manifest['files'])==2,'Exact two-upload-file domain differs')
 upload={}
 for x in manifest['files']:
  p=(manifest_path.parent/x['path']).resolve();must(p.parent==manifest_path.parent and x['name']==p.name and not p.is_symlink(),'Upload path/name escapes operative package');upload[x['name']]=p
 must(set(upload)=={'integer_endpoint_discontinuity.pdf','integer-endpoint-discontinuity-verification-v1.zip'},'Wrong exact upload pair')
 pub=json.loads(checked(gate['publication_verification']).read_bytes());tracker=json.loads(checked(gate['tracker_verification']).read_bytes())
 must(pub['published'] is True and pub['all_public_bytes_identical'] is True and pub['manifest']==inputs['manifest'],'Actual publication/public-file verification missing')
 must(pub['repository_upload_kit_used'] is True and pub['intended_metadata_identical'] is True,'Repository-kit and exact metadata verification required')
 checked(pub['inspection_receipt']);checked(pub['upload_receipt'])
 doi=pub['DOI'];record=pub['record_id'];must(isinstance(record,int) and re.fullmatch(r'10\.5281/zenodo\.[0-9]+',doi) and doi=='10.5281/zenodo.'+str(record),'Actual published record DOI differs')
 must(pub['record_url']=='https://zenodo.org/records/'+str(record),'Public record URL differs');resolution=pub['DOI_resolution']
 must(resolution['status']=='resolved' and resolution['http_status']==200 and resolution['resolved_url'].rstrip('/')==pub['record_url'],'Actual DOI resolution not verified')
 readbacks=pub['public_file_readbacks'];must(len(readbacks)==2 and {x['name'] for x in readbacks}==set(upload),'Public-file domain differs')
 for x in readbacks:
  body=upload[x['name']].read_bytes();must(x['HTTP_status']==200 and x['bytes']==len(body) and x['sha256']==sha(body) and x['authentication_sent'] is False,'Actual anonymous public bytes differ')
 must(tracker['DOI']==doi and tracker['append_performed'] is True and tracker['independent_readback_exact'] is True and tracker['fresh_full_table_exactly_one_matching_problem_DOI_row'] is True,'Actual nonduplicate tracker row readback required')
 must(tracker['spreadsheet_id']=='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20' and tracker['sheet_id']==1254632077,'Tracker destination differs')
 must(tracker['actual_four_cells'][0]=='https://www.unsolvedmath.com/problems/'+CODE and tracker['actual_four_cells'][2]=='https://doi.org/'+doi,'Tracker problem/DOI identity differs')
 for key in ['request','append_response','independent_row_readback','fresh_full_table_values','fresh_full_table_formulas','fresh_actual_commands']:checked(tracker[key])
 evidence += [gate['publication_verification'],gate['tracker_verification'],pub['inspection_receipt'],pub['upload_receipt']]+[tracker[k] for k in ['request','append_response','independent_row_readback','fresh_full_table_values','fresh_full_table_formulas','fresh_actual_commands']]
 auth=json.loads(checked(inputs['original_authentication']).read_bytes());originals=auth['original_science_files'];must(auth['original_head']==HEAD and len(originals)==17 and auth['complete_diff_file_count']==18,'Original domain differs')
 source=json.loads((audit/'original_preparation_family/original/source_record.json').read_bytes());must(source['id']==int(ID) and source['problem_number']==CODE and 'upstream_report' not in source,'Original flat selected problem/upstream-report field differs')
 original_paths={x['repository_path'] for x in originals};mirror_paths={PREFIX+'/acceptance.json',PREFIX+'/CURRENT_RESULT.md',STATE,HISTORY};owned_paths=original_paths|{QUEUE} if args.phase=='merge' else mirror_paths;owned_bytes={p.encode() for p in owned_paths}
 def committed_originals(commit):
  for x in originals:
   p=x['repository_path'];must(sha(git('show',commit+':'+p))==x['sha256'],'Original committed body differs');t=git('ls-tree',commit,'--',p).decode().split();must(t[0]==x['git_mode'] and t[2]==x['git_blob_sha1'],'Original committed mode/blob differs')
 def foreign_index():return b'\0'.join(x for x in git('ls-files','--stage','-z').split(b'\0') if x and x.split(b'\t',1)[1] not in owned_bytes)
 def foreign_dirty():return {p.decode() for p in git('diff','--name-only','-z').split(b'\0') if p and p not in owned_bytes}
 def body_state(path):
  p=repo/path
  if not p.exists() and not p.is_symlink():return {'exists':False}
  m=p.lstat().st_mode;must(stat.S_ISREG(m),'Foreign dirty nonregular path: preserve');return {'exists':True,'mode':m,'sha256':sha(p.read_bytes())}
 must(git('branch','--show-current').strip()==b'main','Stay on main');must(not git('diff','--cached','--name-only','-z'),'Whole real index must be empty; preserve foreign staging')
 merge_head=Path(git('rev-parse','--git-path','MERGE_HEAD').decode().strip());merge_head=merge_head if merge_head.is_absolute() else repo/merge_head;must(not merge_head.exists(),'Another merge exists: preserve')
 base=git('rev-parse','HEAD').decode().strip();must(git('ls-remote','--heads','origin','main').decode().split()[0]==base,'Main/remote baseline differs');valid_pause_bases={base}
 if args.phase=='mirror':
  prior_merge=json.loads((own/'NATIVE_MERGE_RESULT.json').read_bytes());must(prior_merge['schema']=='pr57-published-result-native-merge/v1' and prior_merge['submitted_head']==HEAD and prior_merge['merge_commit']==base and prior_merge['DOI']==doi and prior_merge['gate']==gate_pin,'Actual previous merge identity differs')
  must(git('show','-s','--format=%P',base).decode().strip().split()==[prior_merge['base'],HEAD],'Continuous window lacks exact two-parent transition');valid_pause_bases.add(prior_merge['base'])
 window_path=repo/'draft_pr_descending_audit_20261002/SHARED_GIT_WINDOW_STATUS.json'
 def check_window():
  w=json.loads(window_path.read_bytes());must(w['shared_git_writes_paused'] is True and w['paused_for'].startswith('PR57 ordered publication native integration'),'No actual acknowledged exclusive PR57 native-integration window; intake-only windows are rejected')
  must(w['dirty_tracked_bodies_modes_frozen_after_acknowledgement'] is True and w['all_staged_path_count']==0 and w['owned_staged_paths']==[],'Acknowledged frozen foreign bodies/modes and empty shared index required')
  must(w['local_main_at_pause']==w['remote_main_at_pause'] and w['local_main_at_pause'] in valid_pause_bases,'Actual pause baseline differs');return w
 window=check_window();window_pin=binding(window_path);(phase_dir/'ACKNOWLEDGED_WINDOW.json').write_bytes(jb(window));foreign_stage=foreign_index();dirty=foreign_dirty();foreign_bodies={p:body_state(p) for p in dirty}
 def preserve():
  check_window();must(binding(window_path)==window_pin,'Acknowledged writer-window bytes changed');must(foreign_index()==foreign_stage,'Foreign index entries changed')
  must(foreign_dirty()==dirty and all(body_state(p)==x for p,x in foreign_bodies.items()),'Foreign dirty path set/body/mode changed')
  for b in evidence:checked(b)
  must(binding(inputs_path)==inputs_pin and binding(gate_path)==gate_pin and sha(GOAL.read_bytes())==GOAL_SHA,'SOURCE/gate/objective changed')
 def source_identity():
  m=json.loads((repo/'unsolved_math_prioritization/manifest.json').read_bytes());must(m['revision']==inputs['source_revision'],'Current source revision differs')
  for n in ['problems.json','research_results.json']:
   b=(repo/'unsolved_math_prioritization/cache'/n).read_bytes();must({'bytes':len(b),'sha256':sha(b)}==m['files'][n],'Raw corpus differs from source manifest')
  raw=json.loads((repo/'unsolved_math_prioritization/cache/problems.json').read_bytes());must([p for p in raw if str(p['id'])==ID]==[source],'Unique raw typed problem differs')
  reports=json.loads((repo/'unsolved_math_prioritization/cache/research_results.json').read_bytes());must(CODE not in reports,'Selected raw report no longer absent')
  with sqlite3.connect('file:'+str(repo/'unsolved_math_prioritization/cache/catalog.sqlite')+'?mode=ro',uri=True) as db:
   row=db.execute('SELECT payload,report FROM records WHERE key=?',(ID,)).fetchone();revision=db.execute('SELECT revision FROM metadata').fetchall()
  must(row and json.loads(row[0])==source and row[1] is not None and row[1]=='{}' and json.loads(row[1])=={},'SQL typed problem/non-NULL TEXT {} fallback differs');must(revision==[(m['revision'],)],'SQL revision differs')
  pair=sha(json.dumps([source,{}],sort_keys=True).encode());must(pair==PAIR_SHA,'Selected current typed-pair hash differs');selected=[x for x in json.loads((repo/'unsolved_math_prioritization/catalog.json').read_bytes()) if x['id']==ID];must(len(selected)==1 and selected[0]['review_hash']==pair,'Catalog selected fingerprint differs')
  return {'raw_problem_equals_flat_original_and_SQL':True,'raw_report_key_present':False,'raw_report':'ABSENT; no raw value','SQL_report_is_NULL':False,'SQL_report_literal':'{}','original_source_record_is_flat_problem':True,'original_upstream_report_field_present':False,'original_upstream_report':'ABSENT; no wrapper value','review_hash':pair,'review_hash_uses':'Current SQL typed pair [problem, {}]; no absent field is promoted to null.','source_revision':m['revision']}
 identity=source_identity();preserve()
 pr=json.loads(run(['gh','pr','view','57','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,headRefName,baseRefName,mergeCommit,mergedAt,url'])[0]);must(pr['headRefOid']==HEAD and pr['baseRefName']=='main','Actual PR identity differs')
 # Fresh literal eligibility precedes every mutation, including object import.
 aq=json.loads(run(['gh','api','repos/AlecKriebel/Math/contents/'+QUEUE+'?ref='+HEAD])[0]);submitted=base64.b64decode(aq['content']);blob=hashlib.sha1(b'blob '+str(len(submitted)).encode()+b'\0'+submitted).hexdigest();must(blob==aq['sha']==auth['original_queue_destination_blob_sha1'],'Fresh submitted QUEUE blob differs')
 rows=[x for x in submitted.decode().splitlines() if '| '+ID+' /' in x];must(len(rows)==1 and rows[0].split('|')[8].strip()=='claimed_solved' and rows[0].split('|')[9].strip()=='1/5','Fresh literal submitted status is not claimed_solved1/5: stop without processing')
 if args.phase=='merge':must(pr['state']=='OPEN' and pr['isDraft'] is True,'Original open draft required before object import')
 _,available=run(['git','--no-optional-locks','cat-file','-e',HEAD+'^{commit}'],allowed=(0,128))
 if available!=0:
  must(args.phase=='merge','Previously merged object missing: inspect');preserve();git('fetch','--no-tags','--no-write-fetch-head','origin','refs/pull/57/head');git('cat-file','-e',HEAD+'^{commit}')
  reread=json.loads(run(['gh','pr','view','57','--repo','AlecKriebel/Math','--json','headRefOid,state,isDraft'])[0]);must(reread['headRefOid']==HEAD and reread['state']=='OPEN' and reread['isDraft'] is True,'PR drift during object import: inspect')
 committed_originals(HEAD);turns=json.loads(git('show',HEAD+':'+PREFIX+'/turns.json'));must(turns['substantive_proof_attempts']==1 and turns['budget']==5 and len(turns['turns'])==1 and turns['turns'][0]['number']==1,'Actual original sole1/5 ledger changed')
 queue_before=(repo/QUEUE).read_bytes();must(queue_before==git('show',base+':'+QUEUE),'Uncommitted native queue changes: preserve')
 if args.phase=='merge':
  incoming=json.loads(run(['gh','api','repos/AlecKriebel/Math/pulls/57/files?per_page=100'])[0]);must(len(incoming)==18 and {p['filename'] for p in incoming}==owned_paths,'Fresh incoming GitHub file domain differs')
  common=git('merge-base',base,HEAD).decode().strip();must({p.decode() for p in git('diff','--name-only','-z',common,HEAD).split(b'\0') if p}==owned_paths,'Local exact-head incoming domain differs')
  for p in original_paths:must(not (repo/p).exists() and not (repo/p).is_symlink(),'Original native path already exists')
  lines=queue_before.decode().splitlines(keepends=True);ix=[i for i,x in enumerate(lines) if '| '+ID+' /' in x];must(len(ix)==1,'Native row not unique');i=ix[0];cells=lines[i].split('|')
  must(len(cells)==14 and cells[8].strip()=='queued' and cells[9].strip()=='0/5' and not cells[12].strip(),'Native queued0/5 DOI-empty baseline differs')
  cells[8]=' preprint_published ';cells[9]=' 1/5 ';cells[11]=' '+QUEUE_NOTE+' ';cells[12]=' '+doi+' ';lines[i]='|'.join(cells);accepted_queue=''.join(lines).encode()
  must(git('rev-parse','HEAD').decode().strip()==base,'Main moved before merge');preserve();_,merge_exit=run(['git','--no-optional-locks','merge','--no-ff','--no-commit',HEAD],allowed=(0,1))
  conflicts={p.decode() for p in git('diff','--name-only','--diff-filter=U','-z').split(b'\0') if p};must(conflicts<={QUEUE} and merge_head.read_text().strip()==HEAD,'Unexpected conflict/parent: retain partial merge')
  preserve();(repo/QUEUE).write_bytes(accepted_queue)
  for x in originals:
   p=repo/x['repository_path'];must(sha(p.read_bytes())==x['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o644,'Imported original body/mode differs')
  git('add','--',QUEUE);must(not git('diff','--name-only','--diff-filter=U','-z'),'Unresolved conflicts');must({p.decode() for p in git('diff','--cached','--name-only','-z').split(b'\0') if p}==owned_paths,'Merge staged domain differs')
  preserve();git('commit','-m','Accept PR57 published finite-integer normalized uniformization counterexamples');commit=git('rev-parse','HEAD').decode().strip()
  must(git('show','-s','--format=%P',commit).decode().strip().split()==[base,HEAD],'Exact two-parent merge differs');must((repo/QUEUE).read_bytes()==accepted_queue,'Accepted queue differs');must({p.decode() for p in git('diff','--name-only','-z',base,commit).split(b'\0') if p}==owned_paths,'Committed merge domain differs');committed_originals(commit)
  must(not git('diff','--cached','--name-only','-z'),'Entire index not empty after merge commit');preserve();git('push','origin','main');must(git('ls-remote','--heads','origin','main').decode().split()[0]==commit,'Actual merge push readback differs');preserve()
  receipt={'schema':'pr57-published-result-native-merge/v1','UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),'base':base,'submitted_head':HEAD,'merge_commit':commit,'remote_main':commit,'DOI':doi,'gate':gate_pin,'source_bindings':inputs_pin,'acknowledged_shared_writer_window':window_pin,'merge_exit_code':merge_exit,'conflicts':sorted(conflicts),'all_17_original_bodies_modes_blobs_unchanged':True,'queue_only_target_four_cells_changed':True,'foreign_dirty_path_set_bodies_modes_and_index_unchanged':True,'current_source_identity':identity,'original_budget':'1/5','new_central_proof_attempts':0,'native_mirror_pending':True,'GitHub_merged_readback_not_yet_asserted':True};out=own/'NATIVE_MERGE_RESULT.json'
 else:
  must(pr['state']=='MERGED' and pr['mergeCommit']['oid']==base,'Actual GitHub exact merge unconfirmed; do not infer from push');committed_originals(base)
  state_before=(repo/STATE).read_bytes();history_before=(repo/HISTORY).read_bytes();must(state_before==git('show',base+':'+STATE) and history_before==git('show',base+':'+HISTORY),'Native state/history foreign changes: preserve');state=json.loads(state_before)
  must(ID not in state and all(str(json.loads(x).get('id'))!=ID for x in history_before.splitlines()),'Existing target mirror: do not duplicate');must(history_before.endswith(b'\n'),'History incomplete last line')
  for p in mirror_paths-{STATE,HISTORY}:must(not (repo/p).exists() and not (repo/p).is_symlink(),'Current acceptance destination exists')
  rows=[x for x in queue_before.decode().splitlines() if '| '+ID+' /' in x];must(len(rows)==1 and rows[0].split('|')[8].strip()=='preprint_published' and rows[0].split('|')[9].strip()=='1/5' and rows[0].split('|')[11].strip()==QUEUE_NOTE and rows[0].split('|')[12].strip()==doi,'Actual accepted queue row differs');now=dt.datetime.now(dt.timezone.utc).isoformat()
  acceptance={'schema':'pr57-current-published-result-acceptance/v1','at':now,'actual_author_pid':os.getpid(),'problem_id':ID,'problem_code':CODE,'pr':57,'reviewed_head':HEAD,'merge_commit':base,'merged_at':pr['mergedAt'],'outcome':'full_specified_finite_integer_endpoint_negative_answer_published','status':'preprint_published','full_specified_source_target_solved':True,'exact_scope':CLAIM,'doi':doi,'record_url':pub['record_url'],'final_gate':gate_pin,'source_bindings':inputs_pin,'final_artifacts':inputs['final_artifacts'],'clean_reviews':reviews,'publication_verification':gate['publication_verification'],'tracker_verification':gate['tracker_verification'],'tracker_range':tracker['range'],'tracker_row_written':True,'current_source_identity':identity,'original_scientific_files_are_dated_inputs':True,'original_budget':'1/5','original_turn_ledger':binding(repo/(PREFIX+'/turns.json')),'new_central_proof_attempts':0,'bounded_primary_source_priority_search':True,'classical_logarithmic_and_twisting_mechanisms_credited':True,'residual_earlier_unindexed_geometric_realization_risk':True,'worldwide_priority_guarantee':False,'RP2_result':False,'noninteger_topology_result':False,'smooth_topology_result':False,'abstract_homeomorphism_obstruction':False,'AI_tools_used_extensively':True,'human_peer_review':False,'formal_proof_certification':False,'native_status_is_present_day_mirror':True,'historical_lifecycle_transitions_reconstructed':False}
  (repo/(PREFIX+'/acceptance.json')).write_bytes(jb(acceptance))
  current=('# Accepted current result — PR57 / '+CODE+'\n\n**Integer endpoint discontinuity of normalized uniformization for positively curved surfaces**, Alec Kriebel. DOI: https://doi.org/'+doi+'. Published record: '+pub['record_url']+'.\n\n'+CLAIM+'\n\nFor each fixed finite nonnegative integer r, the metric sequence and its smooth admissible limit lie in the plane or sphere source regime. Their unique point-normalized uniformizing diffeomorphisms fail C^(r+1) convergence. The r=1 construction requires the small C^1 conformal correction for the full nonlinear inverse-coordinate curvature operator. This gives the negative answer for the specified finite-integer endpoint parametrization; it does not assert a result on RP2, noninteger Holder or smooth topologies, or rule out abstract homeomorphisms.\n\nThe 2017 Oberwolfach report was published on 3 January 2018. Classical logarithmic and twisting mechanisms are credited. A bounded primary-source priority audit through 3 October 2026 located no earlier full geometric resolution; an earlier unindexed geometric realization remains a residual risk. No exhaustive worldwide-first or novel general endpoint-mechanism claim is made. The 374 finite exact diagnostic cases supplement the universal written proof and do not establish all-r validity, global curvature, completeness or novelty on their own.\n\nacceptance.json binds the actual ROOT decision, two separate adversarial review rounds, final source/PDF/package, actual repository-kit upload with verified intended metadata and anonymous public bytes, actual unique GWS tracker row, and GitHub exact-head merge. All seventeen original scientific bodies, modes and blobs from head `'+HEAD+'` remain unchanged as dated inputs. Frozen SOURCE packets keep their truthful dated no-upload/no-acceptance assertions.\n\nThe raw upstream report key and the original flat source record\'s upstream_report field are both absent, with no report value. The current SQL fallback is non-NULL TEXT `{}`. No absent value is treated as a JSON null placeholder; the current native review_hash uses the typed pair [problem, {}]. Original substantive proof attempts remain 1/5, recorded in original turns.json; no fictional status.json, turns.jsonl, historical lifecycle transitions or additional proof attempts are introduced. State/history receive one present-day acceptance mirror.\n\nAI tools were used extensively in construction, derivation, drafting, adversarial review and verification. This preprint is unrefereed and has no conventional human peer review, journal acceptance or formal proof-assistant certification.\n')
  (repo/(PREFIX+'/CURRENT_RESULT.md')).write_text(current)
  js=lambda x:json.dumps(x,sort_keys=True).encode();event={'at':now,'event':'acceptance_mirror_import','id':ID,'pr':57,'status':'preprint_published','turns_used':1,'turn_limit':5,'doi':doi,'review_hash':PAIR_SHA,'source_record_hash':sha(js(source)),'source_report_hash':sha(js({})),'statement_hash':sha(source['statement'].encode()),'note':QUEUE_NOTE,'evidence':{'import_is_present_day_mirror':True,'historical_transitions_asserted':False,'reviewed_head':HEAD,'merge_commit':base,'canonical_acceptance':binding(repo/(PREFIX+'/acceptance.json')),'original_budget_ledger':binding(repo/(PREFIX+'/turns.json')),'queue_explicit_budget':'1/5','current_source_identity':identity,'final_gate':gate_pin,'publication':gate['publication_verification'],'tracker':gate['tracker_verification'],'full_specified_finite_integer_source_target_solved':True,'worldwide_priority_guarantee':False}}
  event['event_id']=sha(js(event));state[ID]=event;(repo/STATE).write_bytes(jb(state));(repo/HISTORY).write_bytes(history_before+json.dumps(event,ensure_ascii=False,sort_keys=True).encode()+b'\n')
  must({k:v for k,v in json.loads((repo/STATE).read_bytes()).items() if k!=ID}==json.loads(state_before),'Other native states changed');must((repo/HISTORY).read_bytes().startswith(history_before) and len((repo/HISTORY).read_bytes()[len(history_before):].splitlines())==1,'History prefix/event count changed');must((repo/QUEUE).read_bytes()==queue_before,'Mirror changed queue');must(git('rev-parse','HEAD').decode().strip()==base,'Main moved before mirror staging')
  preserve();git('add','--',*sorted(mirror_paths));must({p.decode() for p in git('diff','--cached','--name-only','-z').split(b'\0') if p}==mirror_paths,'Mirror staged domain differs');preserve();git('commit','-m','Bind PR57 published endpoint result to exact merge DOI and tracker');commit=git('rev-parse','HEAD').decode().strip()
  must(git('show','-s','--format=%P',commit).decode().strip()==base,'Current administrative parent differs');must({p.decode() for p in git('diff','--name-only','-z',base,commit).split(b'\0') if p}==mirror_paths,'Committed mirror domain differs');committed_originals(commit);must(not git('diff','--cached','--name-only','-z'),'Entire index not empty after mirror commit');preserve();git('push','origin','main');must(git('ls-remote','--heads','origin','main').decode().split()[0]==commit,'Actual mirror push readback differs');preserve()
  receipt={'schema':'pr57-published-result-native-mirror/v1','UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_pid':os.getpid(),'merge_commit':base,'acceptance_commit':commit,'remote_main':commit,'DOI':doi,'tracker_range':tracker['range'],'gate':gate_pin,'source_bindings':inputs_pin,'event_id':event['event_id'],'acknowledged_shared_writer_window':window_pin,'current_source_identity':identity,'other_native_states_and_history_prefix_preserved':True,'exactly_one_present_day_acceptance_event':True,'foreign_dirty_path_set_bodies_modes_and_index_unchanged':True,'all_17_original_bodies_modes_blobs_unchanged':True,'original_budget':'1/5','new_central_proof_attempts':0,'worldwide_priority_guarantee':False,'program_completion_not_conferred':True};out=own/'NATIVE_ACCEPTANCE_RESULT.json'
 committed_originals(commit);must(not git('diff','--cached','--name-only','-z'),'Entire real index must be empty after phase');must(not out.exists(),'Actual receipt exists: preserve');out.write_bytes(jb(receipt));print(json.dumps(receipt,indent=2))
if __name__=='__main__':
 try:main()
 except Exception as error:
  import traceback
  own=Path(__file__).resolve().parent
  phase=sys.argv[1] if len(sys.argv)>1 and sys.argv[1] in ['merge','mirror'] else 'unknown'
  directory=own/'private'/('integration-'+phase)
  if directory.exists():
   failure=directory/'FAILURE.json'
   if not failure.exists():failure.write_bytes(jb({'UTC':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_helper_pid':os.getpid(),'phase':phase,'error_type':type(error).__name__,'error':str(error),'traceback':traceback.format_exc(),'partial_state_retained':True,'no_reset_stash_abort_or_recovery_attempted':True}))
  raise
