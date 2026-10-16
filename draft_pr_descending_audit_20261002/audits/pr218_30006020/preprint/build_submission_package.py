"""Build a deterministic authored-only archive; perform no provider/Git writes."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import zipfile

R = Path(__file__).resolve().parent
D = R.parent / 'initial_review_20261015'
payload = {}


def add(path, name):
    assert path.is_file() and not path.is_symlink()
    assert not any(p.startswith('private') or p == '__pycache__' for p in path.parts)
    assert name not in payload
    payload[name] = path.read_bytes()


for name in ['README.md', 'cylinder_areas.tex', 'metadata.json', 'PROVENANCE_CLARIFICATIONS.md']:
    add(R / name, name)
for folder, target in [('verification', 'verification'), ('pr_update/30006020', 'current_source')]:
    for p in sorted((R / folder).rglob('*')):
        if p.is_file():
            add(p, target + '/' + str(p.relative_to(R / folder)))
for name in ['ROOT_MATHEMATICAL_ACCEPTANCE.md', 'ROOT_MATHEMATICAL_ACCEPTANCE.json',
             'ROOT_DIRECT_PRIMARY_ASSESSMENT.md', 'ROOT_PRIMARY_RETRIEVAL.json',
             'ROOT_FINAL_PRIORITY_DRAFTING_ACCEPTANCE.json',
             'ROOT_ASSEMBLY_PRIMARY_COMPARISON.md', 'ROOT_PRIORITY_FAMILY_CUSTODY_ACCEPTANCE.json']:
    add(D / name, 'audits/root/' + name)
families = [
    ('source_scope_adversary_01', 'SAFE_ARTIFACT_MANIFEST.json', 'safe_authored_files'),
    ('geometry_input_adversary_01', 'SAFE_AUTHORED_MANIFEST.json', 'authored_files'),
    ('assembly_moment_adversary_01', 'SAFE_AUTHORED_MANIFEST.json', 'safe_authored_files'),
    ('gamma_mesoscopic_adversary_01', 'AUTHORED_MANIFEST.json', 'artifacts'),
    ('priority_author_history_01', 'SAFE_AUTHORED_MANIFEST.json', 'allowed_files'),
    ('priority_assemblies_01', 'AUTHORED_MANIFEST.json', 'public_files'),
    ('priority_novelty_challenge_01', 'SAFE_AUTHORED_MANIFEST.json', 'files'),
    ('final_priority_decision_adversary_01', 'SAFE_AUTHORED_MANIFEST.json', 'files'),
    ('root_priority_01', 'SAFE_AUTHORED_MANIFEST.json', 'safe_authored_files'),
]
for family, manifest, key in families:
    F = D / family
    add(F / manifest, 'audits/' + family + '/' + manifest)
    for row in json.loads((F / manifest).read_text())[key]:
        p = Path(row.get('path', row.get('file')))
        p = p if p.is_absolute() else F / p
        assert p.resolve().is_relative_to(F.resolve())
        raw = p.read_bytes()
        assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256']
        add(p, 'audits/' + family + '/' + str(p.relative_to(F)))
add(D / 'root_priority_01/ASSEMBLY_PRIMARY_RETRIEVAL.json',
    'audits/root_priority_01/ASSEMBLY_PRIMARY_RETRIEVAL.json')
rows = [{'path': name, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
        for name, raw in sorted(payload.items())]
payload['PACKAGE_FILES.json'] = (json.dumps({
    'scope': 'Authored manuscript, metadata, finite controls, original-submission provenance and bounded authored audits. No entire third-party source payloads. This manifest excludes itself.',
    'historical_audits': 'Historical manifests and reviews bind their listed frozen inputs. Original submission resides under current_source/history/original_submission_20261001. Absolute archival provenance paths are not executable requirements; the portable verification entry point is verification/run_checks.py.',
    'files': rows,
}, indent=2) + '\n').encode()
out = R / 'output/cylinder_areas_verification.zip'
out.parent.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(out, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for name, raw in sorted(payload.items()):
        info = zipfile.ZipInfo(name, date_time=(2026, 10, 15, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        z.writestr(info, raw)
with zipfile.ZipFile(out) as z:
    assert z.testzip() is None
    for name, raw in payload.items():
        assert z.read(name) == raw
metadata = json.loads((R / 'metadata.json').read_text())
deposit = {'metadata': metadata, 'files': [
    {'path': 'output/pdf/cylinder_areas.pdf'},
    {'path': 'output/cylinder_areas_verification.zip'},
]}
(R / 'deposit.json').write_text(json.dumps(deposit, indent=2) + '\n')
frozen = []
for p in [R / 'cylinder_areas.tex', R / 'output/pdf/cylinder_areas.pdf', out,
          R / 'metadata.json', R / 'deposit.json']:
    raw = p.read_bytes()
    frozen.append({'path': str(p.relative_to(R)), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})
receipt = {'utc': datetime.now(timezone.utc).isoformat(), 'stage': 'prepared_for_fresh_sequential_manuscript_review',
           'original_PR_head': 'dc457c741c779fbf90fbfdcdc73f750b3716f561',
           'metadata_objects_identical': deposit['metadata'] == metadata,
           'archive_members': len(payload), 'archive_payload_manifest': rows,
           'submission_files': frozen, 'release_cleared': False}
(R / 'FROZEN_INPUTS.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({'archive_members': len(payload), 'archive_bytes': out.stat().st_size,
                  'submission_files': frozen}, indent=2))
