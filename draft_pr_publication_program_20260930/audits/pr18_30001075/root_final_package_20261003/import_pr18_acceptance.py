"""Record one actual present-day PR18 acceptance mirror after its observed merge."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import stat
import subprocess
import sys

if sys.flags.optimize or sys.argv[1:] != ['--exclusive-window-confirmed']:
    raise RuntimeError('Requires the confirmed shared writer window')
own=Path(__file__).resolve().parent
a18=own.parent
program=a18.parents[1]
repo=program.parent
canonical=repo/'unsolved_math_prioritization/attempts/30001075'
def sha(body): return hashlib.sha256(body).hexdigest()
def js(value): return json.dumps(value,sort_keys=True)
def git(*args):
    child=subprocess.run(['git',*args],cwd=repo,capture_output=True)
    if child.returncode:
        raise RuntimeError(child.stderr.decode(errors='replace'))
    return child.stdout
def must(condition,message):
    if not condition: raise RuntimeError(message)
def binding(p):
    return {'path':p.relative_to(repo).as_posix(),'sha256':sha(p.read_bytes())}
merge=json.loads((own/'NATIVE_MERGE_RESULT.json').read_bytes())
base=git('rev-parse','HEAD').decode().strip()
must(base==merge['merge_commit'],'Main moved since actual PR18 merge')
must(git('branch','--show-current').strip()==b'main' and not git('diff','--cached','--name-only').strip(),'Main and a clean real index required')
must(git('ls-remote','--heads','origin','main').decode().split()[0]==base,'Remote main differs')
receipt=program/'audits/pr45_9900007/root_pr18_actual_github_merged_readback_capture/stdout.bin'
remote=json.loads(receipt.read_bytes())
must(remote['state']=='MERGED' and remote['headRefOid']==merge['submitted_head'] and remote['mergeCommit']['oid']==base,'GitHub merge is not independently confirmed')
must(remote['body']==(own/'ACCEPTED_PR_BODY.md').read_text(),'PR body readback differs')
remote_path=a18/'pr_merged.json'
must(not remote_path.exists(),'Do not overwrite an existing merge receipt')
remote_path.write_bytes(receipt.read_bytes())
plan=json.loads((a18/'native_acceptance_plan_20261003/PLAN.json').read_bytes())
for item in plan['original_scientific_files_to_preserve_exactly']:
    must(sha((repo/item['canonical_path']).read_bytes())==item['sha256'],'Original canonical source changed')
source=json.loads((canonical/'source_record.json').read_bytes())
with sqlite3.connect('file:'+str(repo/'unsolved_math_prioritization/cache/catalog.sqlite')+'?mode=ro',uri=True) as db:
    raw,report=db.execute('SELECT payload,report FROM records WHERE key=?',('30001075',)).fetchone()
p=json.loads(raw); r=json.loads(report)
must(p==source,'Preserved source differs from exact cached source')
review_hash=sha(js([p,r]).encode())
must(review_hash==json.loads((canonical/'readiness.json').read_bytes())['review_hash'],'Original source pair fingerprint differs')
state_path=repo/'unsolved_math_prioritization/state.json'
history_path=repo/'unsolved_math_prioritization/history.jsonl'
state_before=state_path.read_bytes(); history_before=history_path.read_bytes()
must(state_before==git('show',base+':'+state_path.relative_to(repo).as_posix()) and history_before==git('show',base+':'+history_path.relative_to(repo).as_posix()),'Native state/history contain foreign edits')
state=json.loads(state_before)
must('30001075' not in state and all(json.loads(line).get('id')!='30001075' for line in history_before.splitlines()),'Acceptance already exists; do not duplicate')
must(history_before.endswith(b'\n'),'History must have a complete last line')
publication=a18/'publication/PUBLICATION_VERIFICATION.json'
pub=json.loads(publication.read_bytes())
must(pub['published'] is True and pub['all_public_bytes_identical'] is True,'Publication unverified')
now=dt.datetime.now(dt.timezone.utc).isoformat()
acceptance={'schema':'pr18-current-acceptance/v1','at':now,'actual_author_pid':os.getpid(),
    'problem_id':'30001075','problem_code':'OWR-2090-028','pr':18,
    'outcome':'claimed_solved_accepted_and_published','reviewed_head':merge['submitted_head'],
    'merge_commit':base,'merged_at':remote['mergedAt'],'doi':pub['DOI'],'record_url':pub['record_url'],
    'exact_scope':'Literal OWR44/2008 Conjecture4: spatial union of complete supporting-plane common tangent lines to any three pairwise disjoint convex subsets of R3 has Lebesgue outer measure zero, including nonclosed, unbounded and all affine dimensions.',
    'stronger_conjecture3_established_by_this_result':False,
    'accepted_proof':binding(a18/'preprint_v1/paper.tex'),
    'published_pdf':binding(a18/'preprint_v1/common_tangent_nullness.pdf'),
    'published_verification_package':binding(a18/'preprint_v1/common_tangents_null_locus_v1.zip'),
    'first_fresh_wholepackage_review':binding(a18/'preprint_round1_adversary_family/VERDICT.json'),
    'second_NEW_fresh_wholepackage_review':binding(a18/'preprint_round2_adversary_family/VERDICT.json'),
    'priority_assessment':binding(a18/'ROOT_CURRENT_PRIORITY_ASSESSMENT_20261003.json'),
    'publication_verification':binding(publication),'remote_merge_readback':binding(remote_path),
    'original_candidate_sha256':sha((canonical/'CANDIDATE.md').read_bytes()),
    'original_files_are_dated_inputs_not_final_proof':True,
    'original_budget':'1/5','new_central_attempts':0,
    'review_status':'Unrefereed; extensive AI-assisted solving, drafting and verification; no conventional external human peer review or formal proof certification claimed.',
    'historical_first_priority_asserted':False,
    'tracker_range':None,'tracker_row_written':False,'tracker_status':'Google CLI401 expired/revoked; human credential reconnection pending',
    'workflow_completion_estimate_percent':98}
acceptance_path=canonical/'acceptance.json'
must(not acceptance_path.exists(),'Canonical acceptance already exists')
acceptance_path.write_text(json.dumps(acceptance,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
current_path=canonical/'CURRENT_RESULT.md'
current=current_path.read_text()
old='A present-day acceptance mirror will bind the actual merge commit after it is known; no historical lifecycle transitions are reconstructed.'
must(current.count(old)==1,'Current result sentence changed')
current_path.write_text(current.replace(old,f'Present-day acceptance.json binds the independently confirmed merge commit `{base}`. The state and history record one current acceptance mirror; no historical lifecycle transitions are reconstructed.'))
event={'at':now,'event':'acceptance_mirror_import','id':'30001075','pr':18,
    'status':'preprint_published','turns_used':1,'turn_limit':5,'doi':pub['DOI'],
    'review_hash':review_hash,'source_record_hash':sha(js(p).encode()),
    'source_report_hash':sha(js(r).encode()),'statement_hash':sha(p['statement'].encode()),
    'note':'Human-authorized current acceptance mirror; no historical readiness/candidate/verification transitions reconstructed.',
    'evidence':{'authorization':'human_authorized_current_acceptance_mirror',
        'import_is_present_day_mirror':True,'historical_transitions_asserted':False,
        'reviewed_head':merge['submitted_head'],'accepted_source':binding(canonical/'source_record.json'),
        'canonical_acceptance':binding(acceptance_path),'artifact':binding(a18/'preprint_v1/paper.tex'),
        'original_budget_ledger':binding(canonical/'turns.jsonl'),'queue_explicit_budget':'1/5',
        'publication':binding(publication),'merge_commit':base,'remote_acceptance':binding(remote_path),
        'duplicate_ids':[],'tracker_row_written':False}}
event['event_id']=sha(js(event).encode())
state['30001075']=event
state_path.write_text(json.dumps(state,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
history_path.write_bytes(history_before+json.dumps(event,ensure_ascii=False,sort_keys=True).encode()+b'\n')
must({k:v for k,v in json.loads(state_path.read_bytes()).items() if k!='30001075'}==json.loads(state_before),'Foreign state entries changed')
must(history_path.read_bytes().startswith(history_before) and len(history_path.read_bytes().splitlines())==len(history_before.splitlines())+1,'History prefix or event count changed')
entry=f'\n## {now} — PR18 accepted and published, tracker pending\n\nExact original head merged at `{base}` and GitHub confirmed MERGED. The accepted manuscript and published files are linked by present-day acceptance records; 15 historical source blobs and original 1/5 budget remain unchanged. Two fresh whole-package reviews are complete. DOI {pub["DOI"]}. Workflow estimate: 98%; discovery resolution: 100% within literal Conjecture4 scope. Google tracker remains unwritten pending expired/revoked credential reconnection. No new central discovery attempts.\n'
for log in [program/'RESEARCH_LOG.md',a18/'RESEARCH_LOG.md']:
    with log.open('a') as f: f.write(entry)
selected={state_path,history_path,acceptance_path,current_path,remote_path,program/'RESEARCH_LOG.md',a18/'RESEARCH_LOG.md'}
for pth in own.iterdir():
    if pth.is_file() and pth.name!='ACCEPTANCE_CHECKPOINT_RESULT.json': selected.add(pth)
selected.update(pth for pth in (own/'integration_step1').rglob('*') if pth.is_file())
for folder in (program/'audits/pr45_9900007').glob('root_pr18_*_actual_capture'):
    selected.update(pth for pth in folder.iterdir() if pth.is_file())
for pth in selected:
    must(not pth.is_symlink() and stat.S_ISREG(pth.lstat().st_mode),'Nonregular selected file')
paths=sorted(pth.relative_to(repo).as_posix() for pth in selected)
path_bytes={pth.encode() for pth in paths}
pins={pth:sha((repo/pth).read_bytes()) for pth in paths}
def foreign_index():
    return b'\0'.join(e for e in git('ls-files','--stage','-z').split(b'\0') if e and e.split(b'\t',1)[1] not in path_bytes)
foreign=foreign_index()
must(git('rev-parse','HEAD').decode().strip()==base,'Main moved before acceptance commit')
git('add','--',*paths)
must(foreign_index()==foreign,'Foreign index changed')
git('commit','--only','-m','Bind PR18 native acceptance to actual merge and published DOI','--',*paths)
commit=git('rev-parse','HEAD').decode().strip()
changed=set(git('diff-tree','--no-commit-id','--name-only','-r','-z',commit).split(b'\0'))-{b''}
must(changed<=path_bytes and git('rev-parse',commit+'^').decode().strip()==base,'Unexpected acceptance commit scope/parent')
must(foreign_index()==foreign and all(sha((repo/pth).read_bytes())==pin for pth,pin in pins.items()),'Foreign index or selected files drifted')
git('push','origin','main')
remote_main=git('ls-remote','--heads','origin','main').decode().split()[0]
must(remote_main==commit and foreign_index()==foreign,'Acceptance push readback mismatch')
record={'schema':'pr18-native-acceptance-checkpoint/v1','UTC':dt.datetime.now(dt.timezone.utc).isoformat(),
    'actual_pid':os.getpid(),'merge_commit':base,'acceptance_commit':commit,'remote_main':remote_main,
    'event_id':event['event_id'],'exactly_one_present_day_history_event':True,
    'other_state_entries_unchanged':True,'complete_history_prefix_unchanged':True,
    'all_15_original_files_unchanged':True,'foreign_index_unchanged':True,
    'DOI':pub['DOI'],'tracker_row_written':False,'workflow_percent':98,'new_central_attempts':0}
(own/'ACCEPTANCE_CHECKPOINT_RESULT.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
