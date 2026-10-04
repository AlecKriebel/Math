from pathlib import Path
from datetime import datetime,timezone
import json
P=Path(__file__).resolve().parent;A=P/'audits/pr329_20000450'
utc=datetime.now(timezone.utc).isoformat()
s=json.loads((P/'SHARED_GIT_WINDOW_STATUS.json').read_text());assert not s['shared_git_writes_paused']
s.update(utc=utc,descending_active_pr=329,descending_329_workflow_percent=22,
    descending_329_mathematical_verification_percent=45,descending_git_checkpoint_preparing=True,
    descending_checkpoint_scope='PR329 original-source/full22-file freeze and first mathematical audit/replays only; all active reviewer namespaces, raw primary/source/API/Git streams, imported reports and runtimes excluded. No acceptance, merge, paper or publication for329.')
(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(s,indent=2)+'\n')
inv=json.loads((P/'inventory.json').read_text())
for row in inv['items']:
    if row['number']==329:
        row.update(disposition='active_claimed_solved_adversarial_math_audit',audit_directory=str(A),
            original_author_turns='1/5',mathematical_verification_percent=45,workflow_percent=22,
            mathematical_acceptance=False,priority_acceptance=False,publication_ready=False)
(P/'inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
for p in [A/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md']:
    with p.open('a') as f:f.write('\n'+utc+' — PR329 initial audit checkpoint prepared: source-first criteria and three independent families, complete22-file API/object/disk and localGit verification, original88,918-check and inherited29-check replays. Geometry reports no gap; external root replay ongoing. Arithmetic/full division proof still under audit. Mathematical verification45%, workflow22%; no mathematical/priority/publication acceptance, original1/5 unchanged. All excluded statuses skipped entirely.\n')
print(json.dumps({'utc':utc,'checkpoint_scope':s['descending_checkpoint_scope'],'math_percent':45,'workflow_percent':22},indent=2))
