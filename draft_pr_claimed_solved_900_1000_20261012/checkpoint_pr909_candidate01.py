#!/usr/bin/env python3
"""Record verified candidate preparation, without acceptance or publication."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
P=Path(__file__).resolve().parent;A=P/'audits/pr909_30001345';D=A/'publication';now=datetime.now(timezone.utc).isoformat()
def require(x,label):
 if not x:raise RuntimeError(label)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
f=json.loads((D/'PREPUBLICATION_FREEZE.json').read_text())
require(sha(D/'PREPUBLICATION_FREEZE.json')=='c58e74cd19d42ac1b867dc9add2f6c3ab9075248dcac0e19432f851ccba7509f','Freeze changed')
for n,pin in f['files'].items():require(sha(D/n)==pin['sha256'] and (D/n).stat().st_size==pin['bytes'],'Frozen byte changed')
snap=json.loads((A/'ORIGINAL_SNAPSHOT.json').read_text())
for n,pin in snap['files'].items():require(sha(A/'original'/n)==pin,'Original changed')
record={'utc':now,'revision_candidate':1,'freeze_sha256':sha(D/'PREPUBLICATION_FREEZE.json'),'package_manifest_sha256':f['package_manifest_sha256'],'original_files_unchanged':28,'pdf_pages_visually_verified':4,'full_outer_replays':['normal','O','OO','env2'],'all_full_replay_json_identical':len({(D/('PACKAGE_REPLAY_'+n+'.json')).read_bytes() for n in ['normal','O','OO','env2']})==1,'hostile_inventory_runs_rejected':140,'false_assertion_child_runs_rejected':4,'corrupted_copies_rejected_before_execution':4,'first_copy_challenge_invocation':'An incorrect manually supplied external pin was rejected safely before any copy/replay. Corrected invocation used the actual authenticated build pin and all4 copy controls passed. No failing publication artifact was accepted.','live_description_repaired_and_read_back':True,'publication_disposition':'pending_user_outcome_preference; attributed proposed note only','full_package_review_01':'new_clean_context_adversary_running','acceptance_merge_zenodo_stage_publish_tracker_actions':False,'original_recovery_count':'1 verified/5; earlier-attempt count unavailable'}
require(record['all_full_replay_json_identical'],'Replay differs')
(D/'CANDIDATE_PREPARATION_RECEIPT.json').write_text(json.dumps(record,indent=2)+'\n')
s=json.loads((P/'CURRENT_STATE.json').read_text());s.update(utc=now,phase='PR909_attributed_candidate01_frozen_full_review01_running_disposition_pending',active_pr_completion_estimate_percent=60,shard_completion_estimate_percent=(4+.6)/12*100,publication_disposition='PR909 proposed classical-corollary outcome pending; no acceptance/merge/stage/publish');(P/'CURRENT_STATE.json').write_text(json.dumps(s,indent=2)+'\n')
entry=f'\n{now} — PR909 checkpoint60% workflow/shard38.33% estimated: scoped mathematical theorem verified, novelty/current-openness unestablished. A four-page explicitly attributed classical-corollary candidate and closed105-payload verification package are prepared, native/export compilation and all-page QA pass. All28 original bytes/recovery history unchanged. Four outer replay modes give identical PASS,140 structural rejection controls,4 false-assertion child controls and4 post-copy corruption controls pass. Live PR provenance description repaired/read back without accepting or merging. A NEW clean-context full-package adversary01 is running. Outcome preference for this attributed-note repair remains pending; no Zenodo staging/publication or sheet/native acceptance action.\n'
for n in [P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md']:
 with n.open('a') as h:h.write(entry)
paths=[(D/n).relative_to(P.parent).as_posix() for n in f['files']]
paths += [(D/n).relative_to(P.parent).as_posix() for n in ['PREPUBLICATION_FREEZE.json','BUILD_RECEIPT.json','PACKAGE_REPLAY_normal.json','PACKAGE_REPLAY_O.json','PACKAGE_REPLAY_OO.json','PACKAGE_REPLAY_env2.json','PACKAGE_GUARD_CHALLENGES.json','COPY_GUARD_CHALLENGE.json','PDF_VISUAL_QA.json','LOCAL_ZENODO_CHECK.json','CANDIDATE_PREPARATION_RECEIPT.json']]
paths += [(A/n).relative_to(P.parent).as_posix() for n in ['PR_DESCRIPTION_BEFORE_REPAIR.json','PR_DESCRIPTION_CORRECTED.md','PR_DESCRIPTION_REPAIR.json','ROOT_PRIORITY_MECHANISM_CHECK.md','PUBLICATION_FRAMING.md','RESEARCH_LOG.md']]
paths += [(P/n).relative_to(P.parent).as_posix() for n in ['repair_pr909_description.py','checkpoint_pr909_candidate01.py','CURRENT_STATE.json','RESEARCH_LOG.md','checkpoints/checkpoint30.json']]
(P/'checkpoints/checkpoint31_paths.json').write_text(json.dumps(sorted(set(paths)),indent=2)+'\n')
print(json.dumps(record,indent=2))
