#!/usr/bin/env python3
"""Root-owned exact first-party checkpoint; never stage foreign or live scopes."""
from pathlib import Path, PurePosixPath
import datetime as dt
import hashlib
import json
import subprocess

R = Path('/Users/alec/Documents/Math')
P = R / 'draft_pr_publication_program_20260930'
A = P / 'audits'
owned = set()
closures = []

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def run(args, **kw):
    return subprocess.run(args, cwd=R, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kw).stdout

def load(p):
    def pairs(items):
        result = {}
        for k, v in items:
            assert k not in result, (p, k)
            result[k] = v
        return result
    return json.loads(p.read_bytes(), object_pairs_hook=pairs)

def add(p):
    assert p.is_file() and not p.is_symlink(), p
    assert all(not q.is_symlink() for q in p.parents), p
    owned.add(p.relative_to(R).as_posix())

def family(rel):
    m = A / rel
    o = load(m)
    rows = next(o[k] for k in ('files', 'authored_files', 'members') if k in o)
    assert isinstance(rows, list)
    names = set()
    for row in rows:
        n = row['path']
        assert isinstance(n, str) and str(PurePosixPath(n)) == n and not n.startswith('/')
        assert not any(c in ('', '.', '..') for c in n.split('/')) and n not in names
        names.add(n)
        p = m.parent / n
        raw = p.read_bytes()
        size = row.get('size', row.get('bytes'))
        assert type(size) is int and len(raw) == size and sha(raw) == row['sha256'], p
        add(p)
    add(m)
    closures.append({'path': m.relative_to(R).as_posix(), 'sha256': sha(m.read_bytes()), 'members': len(rows)})

assert run(['git', 'branch', '--show-current']).strip() == b'main'
assert not run(['git', 'diff', '--cached', '--name-only']).strip()
for rel in (
    'pr38_2765/reviewed_candidate_v2/MANIFEST.json',
    'pr38_2765/whole_current_source_first_family/FAMILY_MANIFEST.json',
    'pr38_2765/whole_current_alias_followup_family/FAMILY_MANIFEST.json',
    'pr38_2765/whole_current_alias_source_revision/FAMILY_MANIFEST.json',
    'pr38_2765/acceptance_preparation_family/alias_source_revision/ALIAS_PREPARATION_MANIFEST.json',
    'pr38_2765/acceptance_preparation_family/integration_source_revision/PREPARATION_MANIFEST.json',
    'pr38_2765/final_evidence_reconciliation/FINAL_MANIFEST.json',
    'pr39_9500008/reviewed_candidate/MANIFEST.json',
    'pr39_9500008/root_closed_families_actual_reproduction_support/ROOT_SUPPORT_MANIFEST.json',
    'pr39_9500008/current_preparation_family/PREPARATION_MANIFEST.json',
    'pr39_9500008/current_preparation_static_adversary_family/FIRST_PARTY_MANIFEST.json',
    'pr39_9500008/root_replay_static_adversary_family/MANIFEST.json',
    'pr39_9500008/root_typed_entry_preparation_family/PREPARATION_MANIFEST.json',
    'pr39_9500008/root_typed_entry_execution_revision/PREPARATION_MANIFEST.json',
    'pr39_9500008/current_execution_revision/REVISION_MANIFEST.json',
    'pr39_9500008/root_typed_entry_actual_capture/TYPED_ENTRY_MANIFEST.json',
    'pr39_9500008/root_typed_entry_actual_capture_v2/TYPED_ENTRY_MANIFEST.json',
    'pr40_2814/primary_scope_family/FIRST_PARTY_MANIFEST.json',
    'pr40_2814/geodesic_geometry_family/ARTIFACT_MANIFEST.json',
    'pr40_2814/root_audit_SQL_qualification_family/FIRST_PARTY_MANIFEST.json',
    'pr40_2814/current_preparation_family/PREPARATION_MANIFEST.json',
):
    family(rel)

for folder in ('pr38_2765/root_v2_alias_actual_capture', 'pr38_2765/root_final_reconciliation_actual_capture',
               'pr39_9500008/root_current_typed_outer_capture', 'pr39_9500008/root_current_typed_outer_capture_v2'):
    for name in ('CAPTURE.json', 'prelaunch_source.py', 'stdout.bin', 'stderr.bin'):
        add(A / folder / name)

for row in load(A / 'pr40_2814/ROOT_ACTUAL_EVIDENCE_INSPECTION.json')['full_actual_capture_members']:
    p = A / 'pr40_2814' / row['path']
    assert len(p.read_bytes()) == row['size'] and sha(p.read_bytes()) == row['sha256']
    add(p)

individual = {
    'pr38_2765': ('ROOT_V2_ALIAS_INSPECTION.json', 'inspect_root_actual_alias_v2.py', 'ROOT_RESEARCH_LOG.md',
                 'acceptance_preparation_family/RESEARCH_LOG.md', 'ROOT_REVIEWED_FINAL_PLAN.json'),
    'pr39_9500008': ('ROOT_ACTUAL_REPLAY_INSPECTION.json', 'ROOT_CLOSED_FAMILIES_ACTUAL_REPRODUCTION.json',
                    'ROOT_CURRENT_INPUT_PREIMAGES.json', 'ROOT_REPLAY_READ_ATTESTATION.json', 'ROOT_REPLAY_SOURCE_REVIEW.json',
                    'ROOT_SCIENCE_CARD.json', 'ROOT_CURRENT_PACKET_INSPECTION.json', 'inspect_root_actual_replay.py',
                    'reproduce_root_closed_families.py', 'ROOT_RESEARCH_LOG.md'),
    'pr40_2814': ('ROOT_PARTIAL_SCOPE_CERTIFICATE.md', 'ROOT_PRIMARY_READ_LEDGER.json', 'ROOT_ACTUAL_EVIDENCE_INSPECTION.json',
                 'inspect_root_actual_evidence.py', 'ROOT_RESEARCH_LOG.md'),
}
for folder, names in individual.items():
    for n in names:
        add(A / folder / n)

now = dt.datetime.now(dt.timezone.utc).isoformat()
notes = {
    'pr38_2765': 'Acceptance approximately97%; independent v2 review and root actual final reconciliation passed, PID72447/exit0. Root scope preserves four qualified partial results, original2/5/new0/audit0. Full target remains unsolved (discovery estimate15%). Integration and postacceptance pending; no paper or DOI.',
    'pr39_9500008': 'Acceptance approximately92%; root original14/88/2 and support2019 reproduction passed. First typed actual outerPID63927 failed only when the builder rejected eight pinned historical .run1 members; all17 malformed controls rejected. New adjacent exact-eight-row capability/source-anchor revision preserves the failure and original505 source. Second actual outerPID66928 passed all20 launches, including17 rejects; current2901/self, dependencies2797, root whole inspectiondb3d53ca passed. Six exact malformed negative inputs remain qualified per path; each typed scope retains one exact duplicate-key negative. New independent whole-current review pending. Full arbitrary random-origin target unsolved (discovery0%); original2/5/new0/audit0; no paper or DOI.',
    'pr40_2814': 'Acceptance approximately75%; root complete primary reading, original13/14/full149MB/all15458 source joins, five actual family runs, closed135 members and complete42 actual capture members verified. Exact SQL qualification records ro only, no immutable/query_only, with no false fault attributed to the closed primary report. Root read all271 current-builder lines and complete contract/overview; actual current freeze and independent whole-current review pending. Original SOURCE_STATUS remains a valid unsolved source-hold partial (project discovery0%); original0/5/new0/audit0; no paper or DOI.',
}
for folder, note in notes.items():
    p = A / folder / 'ROOT_RESEARCH_LOG.md'
    with p.open('a') as f:
        f.write('\n'+now+' — '+note+'\n')
with (P / 'RESEARCH_LOG.md').open('a') as f:
    f.write('\n'+now+' — Program checkpoint:27/180 accepted (15% complete), PR18/20 evidence holds. '+ ' '.join(notes.values()) + '\n')
add(P / 'RESEARCH_LOG.md')
add(Path(__file__).resolve())
records = [{'path': n, 'bytes': len((R/n).read_bytes()), 'sha256': sha((R/n).read_bytes())} for n in sorted(owned)]
preflight = P / 'checkpoints/CHECKPOINT_PREFLIGHT_20261002_1235.json'
assert not preflight.exists()
preflight.write_text(json.dumps({'utc': now, 'current_head': run(['git','rev-parse','HEAD']).decode().strip(),
    'accepted':27,'total':180,'completion_percent':15,'closed_manifests':closures,'exact_owned_files':records,
    'exclusions':'Active unsealed whole-current scopes, foreign PDFs/cache/corpus/SQL/private scratch, symlink fixture trees, and two unrelated tracked referee logs; no broad add.',
    'scope':'Root-owned checkpoint only, not mathematical acceptance or a native historical event.'}, indent=2)+'\n')
add(preflight)
names=sorted(owned)
for start in range(0,len(names),150):
    batch=names[start:start+150]
    run(['git','add','-f','--',*batch])
staged=run(['git','diff','--cached','--name-only','-z']).decode().split('\0')
staged={n for n in staged if n}
assert staged <= owned
for n in staged:
    assert not n.startswith('paper_ii_simultaneous_amplification_referee_audit_2026-08-22/')
pin={r['path']:r for r in records}
for n in staged:
    if n in pin:
        raw=(R/n).read_bytes();assert len(raw)==pin[n]['bytes'] and sha(raw)==pin[n]['sha256']
entries=run(['git','ls-files','--stage','-z']).split(b'\0')
checked=0
for entry in entries:
    if not entry: continue
    meta,n=entry.split(b'\t',1);name=n.decode()
    if name not in staged: continue
    mode,oid,stage=meta.split();assert mode in (b'100644',b'100755') and stage==b'0'
    raw=(R/name).read_bytes();assert oid.decode()==hashlib.sha1(('blob '+str(len(raw))+'\0').encode()+raw).hexdigest()
    checked+=1
assert checked==len(staged)
print(json.dumps({'status':'EXACT_OWNED_CHECKPOINT_STAGED','closed_manifests':len(closures),'owned':len(owned),'staged':len(staged),'bytes':sum(len((R/n).read_bytes()) for n in staged),'accepted':27,'completion_percent':15}))
