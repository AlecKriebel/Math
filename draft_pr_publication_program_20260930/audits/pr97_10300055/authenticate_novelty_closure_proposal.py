"""Authenticate the fresh bounded disposition evidence before requested closure."""
from pathlib import Path
import datetime, hashlib, json, os
A=Path(__file__).resolve().parent
C=A.parents[2]
D=A/'novelty_disposition_adversary_20261006'
def require(ok,message):
    if not ok: raise RuntimeError(message)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((D/'MANIFEST.json').read_text())
expected={'MANIFEST.json'}
for row in m['own_files']:
    p=D/row['file'];expected.add(row['file'])
    require(p.is_file() and not p.is_symlink() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'own body changed')
require({p.relative_to(D).as_posix() for p in D.rglob('*') if p.is_file()}==expected,'own inventory changed')
inputs=json.loads((D/'INPUTS.json').read_text())
for row in inputs['borrowed_inputs']:
    p=Path(row['path'])
    require(p.is_file() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'borrowed body changed')
require(sha(Path(inputs['instructions']['path']))==inputs['instructions']['sha256'],'instruction changed')
v=json.loads((D/'VERDICT.json').read_text())
require(v['close_without_publication_supported'] and not v['demonstrably_new_contribution_established']
        and v['standard_closed_smooth_conditional_scope_implied_by_prior_results']
        and not v['full_original_scope_historical_already_solved_established'],'disposition mismatch')
note=A/'CLOSING_PRIORITY_NOTE_20261006.md'
require(note.is_file() and not note.is_symlink(),'closing note missing')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
result={'schema':'pr97-human-directed-novelty-closure-ready/v1','UTC':now,'operator_PID':os.getpid(),
 'PR':97,'original_head':'fb50facb2a7389bb272bbf0b5cbd80c24c79b992','original_literal_status':'claimed_solved',
 'user_directive':'Hmm is there anything new in ours? If not, we should probably close the PR as already_solved then',
 'disposition':'close_without_merge_or_publication_no_established_novel_contribution',
 'ordinary_smooth_target_implied_by_prior_results':True,'corrected_mathematics_valid':True,
 'supplement_novelty_established':False,'full_original_historical_already_solved_authenticated':False,
 'global_queue_status_change_proposed':False,'no_established_novel_contribution':True,
 'independent_disposition_review_authenticated':True,'own_files_including_manifest':len(expected),
 'borrowed_inputs':len(inputs['borrowed_inputs']),'review_manifest_sha256':sha(D/'MANIFEST.json'),
 'closing_comment_file':note.name,'closing_comment_sha256':sha(note),
 'global_queue_sha256_before':sha(C/'unsolved_math_prioritization/QUEUE.md'),
 'original_author_effort':'2/5','new_central_proof_search_turns':0,
 'prior_publication_disposition_question_superseded_by_user_novelty_directive':True,
 'closure_executed':False,'DOI':None,'publication_authorized':False,'workflow_percent':70,
 'program_completion_percent':13/99*100}
with (A/'ROOT_NOVELTY_CLOSURE_READY_20261006.json').open('x') as stream:
    stream.write(json.dumps(result,indent=2)+'\n')
with (A/'RESEARCH_LOG.md').open('a') as stream:
    stream.write('\n### '+now+' — human novelty-based closure directive adjudicated\n'
      'Human asks whether anything is new and proposes closing if not. Root reread original question, full current candidate, pertinent source criteria and classical imports, then read the fresh bounded independent disposition report in full and authenticated all5 own files and12 borrowed inputs. No demonstrated novel contribution is established; ordinary smooth target is a classical corollary, regularity supplement useful but novelty unestablished. Closure without publication is supported. Closing note distinguishes prior-theorem implication from an unauthenticated literal earlier exact full-original answer; global queued status and counters remain unchanged. Publication-choice question is superseded by this human novelty directive; no qualified publication authorization inferred. Original author2/5, extra proof-search0; PR97workflow70%, program13/99=13.13%. Actual same-head closure remains to execute and verify.\n')
print(json.dumps({'UTC':now,'operator_PID':os.getpid(),'review_authenticated':True,
                  'closure_supported':True,'global_historical_status_change':False}))
