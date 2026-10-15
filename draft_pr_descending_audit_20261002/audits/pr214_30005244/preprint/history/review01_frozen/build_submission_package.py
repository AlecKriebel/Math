"""Build deterministic authored-only package; no provider or Git writes."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import zipfile

R = Path(__file__).resolve().parent
D = R.parent / 'initial_review_20261015'
payload = {}


def add(p, name):
    assert p.is_file() and not p.is_symlink()
    assert not any(x.startswith('private') or x == '__pycache__' for x in p.parts)
    assert name not in payload, name
    payload[name] = p.read_bytes()


for name in ['README.md', 'dipole_spectrum.tex', 'metadata.json', 'SOURCE_CREDIT_SCOPE.md']:
    add(R / name, name)
for folder in ['verification', 'pr_update/30005244']:
    for p in sorted((R / folder).rglob('*')):
        if p.is_file():
            add(p, folder + '/' + str(p.relative_to(R / folder)))
for name in ['INTAKE.json', 'UPSTREAM_PROVENANCE_RECEIPT.json',
             'ROOT_INITIAL_RECONSTRUCTION.md', 'ROOT_DIRECT_SOURCE_READING.md',
             'ROOT_PRIMARY_RETRIEVAL.json', 'ROOT_MATHEMATICAL_SYNTHESIS.md',
             'ROOT_MATHEMATICAL_ACCEPTANCE.json', 'ROOT_ORIGINAL_EXACT_REPLAY_ACCEPTANCE.json',
             'ROOT_FINAL_PRIORITY_DRAFTING_ACCEPTANCE.json']:
    add(D / name, 'audits/root/' + name)
for name in ['REPLAY_RECEIPT.json', 'new_independent_controls/REPLAY_RECEIPT.json']:
    add(D / 'root_reproduction' / name, 'audits/root_reproduction/' + name)
families = [
    'source_scope_adversary_01', 'kernel_consistency_adversary_01',
    'spectral_fredholm_adversary_01', 'ball_counterexample_adversary_01',
    'priority_author_history_01', 'priority_classical_approximation_01',
    'priority_counterexample_01', 'final_priority_gate_adversary_01', 'root_priority_01',
]
for family in families:
    F = D / family
    m = F / 'SAFE_AUTHORED_MANIFEST.json'
    o = json.loads(m.read_text())
    rows = o if isinstance(o, list) else o.get('safe_authored_files', o.get('files'))
    assert isinstance(rows, list)
    add(m, 'audits/' + family + '/' + m.name)
    for row in rows:
        p = Path(row.get('path', row.get('file')))
        p = p if p.is_absolute() else F / p
        assert p.resolve().is_relative_to(F.resolve())
        raw = p.read_bytes()
        assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256'], p
        add(p, 'audits/' + family + '/' + str(p.relative_to(F)))
for name in ['ROOT_VERIFICATION_RUN.json', 'ROOT_PACKAGE_PREPARATION_ACCEPTANCE.json', 'FINAL_CLEARANCE.json']:
    if (R / name).exists():
        add(R / name, 'audits/manuscript/' + name)
for F in sorted(R.glob('fresh_review_*')):
    m = F / 'SAFE_AUTHORED_MANIFEST.json'
    if not m.exists():
        continue
    o = json.loads(m.read_text())
    rows = o if isinstance(o, list) else o.get('safe_authored_files', o.get('files'))
    assert isinstance(rows, list)
    add(m, 'audits/' + F.name + '/' + m.name)
    for row in rows:
        p = Path(row.get('path', row.get('file')))
        p = p if p.is_absolute() else F / p
        assert p.resolve().is_relative_to(F.resolve())
        raw = p.read_bytes()
        assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256']
        add(p, 'audits/' + F.name + '/' + str(p.relative_to(F)))
rows = [{'path': name, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
        for name, raw in sorted(payload.items())]
manifest = {'scope': 'Authored source, metadata, current qualified source and all 31 original artifacts, finite controls and bounded authored mathematical/priority/manuscript audits. Full third-party payloads and raw searches excluded. This manifest excludes itself.',
            'historical_provenance': 'Historical audits apply to their own pinned inputs. Absolute provenance paths are not executable requirements. Portable entry point: verification/run_checks.py.', 'files': rows}
manifest_bytes = (json.dumps(manifest, indent=2) + '\n').encode()
payload['PACKAGE_FILES.json'] = manifest_bytes
(R / 'PACKAGE_FILES.json').write_bytes(manifest_bytes)
out = R / 'output/dipole_spectrum_verification.zip'
out.parent.mkdir(exist_ok=True)
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
deposit = {'metadata': metadata, 'files': [{'path': 'output/pdf/dipole_spectrum.pdf'}, {'path': 'output/dipole_spectrum_verification.zip'}]}
(R / 'deposit.json').write_text(json.dumps(deposit, indent=2) + '\n')
pins = []
for p in [R / 'dipole_spectrum.tex', R / 'output/pdf/dipole_spectrum.pdf', out, R / 'metadata.json', R / 'deposit.json']:
    raw = p.read_bytes()
    pins.append({'path': str(p.relative_to(R)), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})
receipt = {'utc': datetime.now(timezone.utc).isoformat(), 'stage': 'prepared_for_fresh_sequential_manuscript_review',
           'original_PR_head': '36d5ef15098163e74bf14c2e696f560ce592affd', 'metadata_objects_identical': deposit['metadata'] == metadata,
           'archive_members': len(payload), 'submission_files': pins, 'release_cleared': False}
(R / 'FROZEN_INPUTS.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt, indent=2))
