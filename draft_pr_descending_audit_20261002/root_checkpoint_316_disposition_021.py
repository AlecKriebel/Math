"""Checkpoint only completed PR316 disposition artifacts, preserving every foreign path."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, subprocess
P = Path(__file__).resolve().parent
R = P.parent
A = P / 'audits/pr316_9900002'
NAME = 'checkpoint_316_disposition_021'
utc = lambda: datetime.now(timezone.utc).isoformat()
sha = lambda b: hashlib.sha256(b).hexdigest()
load = lambda p: json.loads(p.read_bytes())
def require(c, label):
    if not c:
        raise RuntimeError(label)
def git(*args):
    return subprocess.check_output(['/usr/bin/git', *args], cwd=R, env=dict(os.environ, GIT_OPTIONAL_LOCKS='0'))
def window():
    require(not load(P/'SHARED_GIT_WINDOW_STATUS.json')['shared_git_writes_paused'], 'Shared writes paused')
window()
require(not (P/(NAME+'_receipt.json')).exists(), 'Already checkpointed')
require(git('branch','--show-current') == b'main\n', 'Not on main')
require(not git('diff','--cached','--raw','-z'), 'Index must be empty')
parent = git('rev-parse','HEAD').decode().strip()
require(git('ls-remote','origin','refs/heads/main').decode().split()[0] == parent, 'Main/remote differ')
d = load(A/'PRIORITY_CORRECTION_DISPOSITION.json')
require(d['status'] == 'PASS_RECLASSIFIED_ALREADY_SOLVED_LEFT_DRAFT_BY_CLAIMED_ONLY_SCOPE' and d['workflow_percent'] == 100 and not d['merge'] and not d['paper'], 'Disposition not complete')
g = load(A/'ROOT_FINAL_CORRECTION_ACCEPTANCE.json')
require(g['status'] == 'PASS_FINAL_PRIORITY_CORRECTION_READY_FOR_BRANCH_UPDATE', 'Final review gate missing')
for name, expected in g['final_packet'].items():
    q = A/'priority_correction_packet'/name
    require(q.stat().st_size == expected['bytes'] and sha(q.read_bytes()) == expected['sha256'], 'Final packet changed')
stamp = utc()
inventory = load(P/'inventory.json')
row = next(x for x in inventory['items'] if x['number'] == 316)
row.update(workflow_percent=100, audit_workflow_percent=100, mathematical_verification_percent=100,
           mathematical_acceptance=True, bounded_priority_audit_percent=100,
           priority_adjudication_accepted=True, adjudicated_status='already_solved',
           priority_acceptance=False, publication_ready=False, original_submitted_status='claimed_solved',
           actual_PR_status_correction_performed=True, current_review_head=d['head'],
           disposition='reclassified_already_solved_left_draft_by_claimed_only_scope',
           paper=False, zenodo_upload=False, doi=None, tracker_row=False, merged=False, closed=False)
(P/'inventory.json').write_text(json.dumps(inventory,indent=2)+'\n')
shared = load(P/'SHARED_GIT_WINDOW_STATUS.json')
shared.update(utc=stamp, descending_active_pr=316, descending_316_workflow_percent=100,
              descending_316_bounded_priority_audit_percent=100, descending_316_priority_complete=True,
              descending_316_complete=True, descending_316_preprint_ready=False,
              descending_git_checkpoint_preparing=True,
              descending_checkpoint_scope='PR316 completed: verified mathematics, classical-corollary already_solved correction remotely published to original draft; left unmerged under claimed-only scope, no paper/Zenodo/tracker.')
(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(shared,indent=2)+'\n')
scope = load(P/'CURRENT_SCOPE.json')
scope.update(utc=stamp, current_eligible_pr=None, last_completed_pr=316,
             last_completed_disposition=row['disposition'], next_descending_filter_pending=True)
(P/'CURRENT_SCOPE.json').write_text(json.dumps(scope,indent=2)+'\n')
(A/'README.md').write_text('''# Completed descending audit: PR316 / 9900002

The original claimed_solved submission passed mathematical review. Its general negative answer to Thorisson Problem 1.2 is an exact elementary corollary of Erickson's 1970 alpha-zero renewal theorem; the operational outcome is already_solved. No earlier explicit announcement answering the later named problem was authenticated. The specific valid lacunary construction lies outside the regularly varying class; its exact historical priority remains unestablished.

Distinct independent proof families, a source-first priority audit and fresh adversarial reviews passed. Root reproduced 7852 author, 646 inherited, 6124 independent geometric, 263 fresh probability and 1773 fresh normalization controls. A disposable replay also passed 80 artifact and 1959 exact endpoint controls. These finite checks supplement analytical proofs. Primary Erickson pages were visually verified; Thorisson's exact hypotheses and question were checked in indexed institutional primary text, with full original binary/visual access unavailable.

The accepted current correction preserves all 15 historical author/review files and author 1/5. Only three presentation wrappers, one additive priority note and the problem's own QUEUE status/turn cells changed relative to current main. Original submission, independent reports, final packet, native execution receipts and exact remote readback are bound in the audit manifests. The preparation receipt remains a dated pre-review record. The reviewer artifacts were initially observed as 0644 and explicitly frozen to 0444 without byte changes; failed metadata-only attempts are retained separately.

'''+f'PR draft head `{d["head"]}` was nonforce pushed and all 20 current files independently authenticated by API bytes. The PR remains open and draft. Under the current claimed_solved-only scope it receives no merge, paper, Zenodo upload, DOI, tracker row or release. Mathematics100%, bounded priority100%, workflow100%; this effort is complete and the overall persistent goal remains active. No outside individual was contacted.\n')
entry = (stamp+' — PR316 completed: submitted math100%, bounded priority100%, workflow100%. '
         'Fresh correction adversary and bounded finalization recheck accepted; all final bytes/native execution counts bound. '
         'Nonforce pushed corrected draft '+d['head']+' and read back exact title/body/all20 files; '
         'all15 historical artifacts and author1/5 preserved, own QUEUE cells8/9 only. '
         'Operational already_solved from verified Erickson1970 corollary; prior explicit named-question announcement not authenticated. '
         'Left OPEN draft unmerged by claimed-only scope; no paper/Zenodo/DOI/tracker/release. '
         'Original metadata-only KeyError and original mode-assumption failure retained; science checks passed, no unnecessary replay. '
         'Overall goal active; advance descending to next submitted claimed_solved excluding8.\n')
for q in [P/'RESEARCH_LOG.md', A/'RESEARCH_LOG.md']:
    with q.open('a') as f:
        f.write('\n'+entry)
owned = [P/n for n in ['RESEARCH_LOG.md','SHARED_GIT_WINDOW_STATUS.json','CURRENT_SCOPE.json','inventory.json',
                       'checkpoint_316_priority_020_receipt.json',Path(__file__).name]]
owned += [A/n for n in ['README.md','RESEARCH_LOG.md','root_replay_correction_review.py',
    'root_finalize_priority_correction.py','root_finalize_priority_correction_recovery.py',
    'root_integrate_priority_correction.py','root_integrate_priority_correction_recovery.py','root_accept_final_correction.py','ROOT_CORRECTION_REPLAY.json','ROOT_CORRECTION_REVIEW_FREEZE.json',
    'PRIORITY_CORRECTION_FINALIZATION.json','ROOT_FINAL_CORRECTION_ACCEPTANCE.json',
    'PRIORITY_CORRECTION_PUSH_INTENT.json','PRIORITY_CORRECTION_DISPOSITION.json',
    'priority_corrected_snapshot_manifest.json']]
owned += list((A/'priority_correction_packet').iterdir())
owned += [A/'priority_correction_review'/n for n in ['CORRECTION_REVIEW.md','REVIEW_MANIFEST.json','RESEARCH_LOG.md','validate_artifacts.py',
    'executions/artifact_validation.json','executions/independent_endpoint_controls.json']]
bounded = A/'priority_correction_finalization_review'
owned += [q for q in bounded.rglob('*') if q.is_file()]
require(owned and all(q.is_file() and not q.is_symlink() for q in owned), 'Invalid owned file')
require(not any(q.suffix in ['.pdf','.png','.bin'] or 'private' in str(q.relative_to(P)) for q in owned), 'Private/source binary in allowlist')
paths = {str(q.relative_to(R)) for q in owned}
allow = P/(NAME+'_allowlist.json')
paths.add(str(allow.relative_to(R)))
def foreign():
    index, bodies = {}, {}
    for item in git('ls-files','--stage','-z').split(b'\0'):
        if item:
            meta, path = item.split(b'\t',1)
            if path.decode() not in paths:
                index.setdefault(path,[]).append(meta)
    for path in git('diff','--name-only','-z').split(b'\0'):
        if path and path.decode() not in paths:
            q = R/path.decode()
            bodies[path] = (q.exists(),q.read_bytes() if q.is_file() else None,q.stat().st_mode & 0o7777 if q.exists() else None)
    return index,bodies
before = foreign()
allow.write_text(json.dumps({'utc':utc(),'paths':sorted(paths),'scope':'Completed PR316 correction and accepted mathematical/priority/finalization review; no copyrighted primary sources or raw private executions.',
    'file_pins':{rel:{'bytes':(R/rel).stat().st_size,'sha256':sha((R/rel).read_bytes())} for rel in sorted(paths) if (R/rel).is_file()},
    'math_percent':100,'bounded_priority_percent':100,'workflow_percent':100},indent=2)+'\n')
for phase, argv in [('stage',['/usr/bin/git','add','--',*sorted(paths)]),
    ('commit',['/usr/bin/git','commit','--only','-m','Complete PR316 verified classical-priority correction; retain unmerged draft','--',*sorted(paths)]),
    ('push',['/usr/bin/git','push','origin','main'])]:
    window()
    require(foreign() == before,'Foreign state changed before '+phase)
    started = utc()
    (P/(NAME+'_'+phase+'_preexecution.json')).write_text(json.dumps({'utc':started,'argv':argv,'program_sha256':sha(Path(__file__).read_bytes())},indent=2)+'\n')
    run = subprocess.run(argv,cwd=R,capture_output=True)
    for k,b in [('stdout',run.stdout),('stderr',run.stderr)]:
        (P/(NAME+'_'+phase+'.'+k)).write_bytes(b)
    (P/(NAME+'_'+phase+'.json')).write_text(json.dumps({'argv':argv,'started_utc':started,'ended_utc':utc(),'exit_code':run.returncode,
        'stdout_sha256':sha(run.stdout),'stderr_sha256':sha(run.stderr)},indent=2)+'\n')
    require(run.returncode == 0,phase+' failed: '+run.stderr.decode(errors='replace'))
    require(foreign() == before,'Foreign state changed after '+phase)
commit = git('rev-parse','HEAD').decode().strip()
changed = set(git('diff-tree','--no-commit-id','--name-only','-r',commit).decode().splitlines())
require(changed <= paths and git('ls-remote','origin','refs/heads/main').decode().split()[0] == commit,'Unexpected scope/remote')
for rel in paths:
    q = R/rel
    require(git('show',commit+':'+rel) == q.read_bytes(),'Committed bytes differ: '+rel)
require(not git('diff','--cached','--raw','-z') and foreign() == before,'Final foreign/index state changed')
receipt = {'utc':utc(),'status':'PASS_PR316_COMPLETED_DISPOSITION_CHECKPOINT_PUSHED','parent':parent,'commit':commit,
    'changed_paths':len(changed),'allowlist_paths':len(paths),'remote_main_exact':True,'entire_index_empty':True,
    'foreign_index_and_tracked_bytes_modes_preserved':True,'pr316_head':d['head'],'operational_status':'already_solved',
    'math_percent':100,'bounded_priority_percent':100,'workflow_percent':100,'merged':False,'paper':False,'zenodo':False,'tracker':False,'goal_complete':False}
(P/(NAME+'_receipt.json')).write_text(json.dumps(receipt,indent=2)+'\n')
shared = load(P/'SHARED_GIT_WINDOW_STATUS.json')
shared.update(utc=utc(),descending_git_checkpoint_preparing=False,last_owned_checkpoint=commit,last_owned_checkpoint_pushed=True)
(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(shared,indent=2)+'\n')
with (P/'RESEARCH_LOG.md').open('a') as f:
    f.write('\n'+utc()+' — Completed PR316 disposition audit pushed '+commit+'; exact remote and scoped bytes verified, foreign work preserved. Math/priority/workflow100%; goal active.\n')
print(json.dumps(receipt,indent=2))
