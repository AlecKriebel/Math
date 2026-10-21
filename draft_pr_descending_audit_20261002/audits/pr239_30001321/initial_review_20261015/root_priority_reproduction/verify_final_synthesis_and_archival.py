"""Root-owned exact replay and private/public integrity checks; no network or Git."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
D = HERE.parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pin(path, row):
    raw = path.read_bytes()
    expected_size = row.get('bytes', row.get('byte_length'))
    assert expected_size is None or len(raw) == expected_size, str(path)
    assert sha(path) == row['sha256'], str(path)
    return dict(path=str(path.relative_to(D)), bytes=len(raw), sha256=sha(path))


public = []
seals = []
for family, filename, key in [
    ('priority_historical_01', 'AUTHORED_MANIFEST.json', 'files'),
    ('priority_local_limit_01', 'PUBLIC_AUTHORED_MANIFEST.json', 'files'),
    ('priority_recent_01', 'AUTHORED_MANIFEST.json', 'files'),
    ('priority_bridge_01', 'PUBLIC_AUTHORED_MANIFEST.json', 'files'),
    ('priority_conlon_song_01', 'PUBLIC_AUTHORED_MANIFEST.json', 'files'),
    ('priority_synthesis_adversary_01', 'PUBLIC_AUTHORED_MANIFEST.json', 'files'),
    ('priority_bmp_archival_01', 'authored_manifest.json', 'artifacts'),
]:
    folder = D / family
    manifest = folder / filename
    rows = json.loads(manifest.read_text())[key]
    for row in rows:
        path = folder / row['path']
        assert path.resolve().is_relative_to(folder.resolve())
        assert not set(path.relative_to(folder).parts).intersection({'private', 'private_sources', 'private_reading'})
        public.append(pin(path, row))
    seals.append(dict(family=family, manifest=str(manifest.relative_to(D)), sha256=sha(manifest), entries=len(rows)))

# This includes 22 saved responses/PDF copies, not 22 independent papers.
conlon = D / 'priority_conlon_song_01'
conlon_private = []
for row in json.loads((conlon / 'source_manifest.json').read_text()):
    path = conlon / row['private_file']
    assert path.resolve().is_relative_to((conlon / 'private').resolve())
    conlon_private.append(pin(path, row))
assert len(conlon_private) == 22

# The initial local-limit public receipt also contained one transient challenge
# query. Preserve the full original seal privately and verify only the declared
# error field, appended log, and manifest metadata changed.
local = D / 'priority_local_limit_01'
current_local_manifest = json.loads((local / 'PUBLIC_AUTHORED_MANIFEST.json').read_text())
clean = current_local_manifest['sanitation']
private_receipt_path = local / clean['private_seal_receipt']
assert private_receipt_path.resolve().is_relative_to((local / 'private_reading').resolve())
assert sha(private_receipt_path) == clean['private_seal_receipt_sha256']
private_receipt = json.loads(private_receipt_path.read_text())
assert len(private_receipt['payloads']) == 29
for row in private_receipt['payloads']:
    pin(private_receipt_path.parent / row['path'], row)
old_manifest_path = private_receipt_path.parent / 'PUBLIC_AUTHORED_MANIFEST.json'
assert sha(old_manifest_path) == clean['original_public_manifest_sha256']
old_manifest = json.loads(old_manifest_path.read_text())
assert len(old_manifest['files']) == len(current_local_manifest['files']) == 28
old_by_name = {row['path']: row for row in old_manifest['files']}
changed = []
for row in current_local_manifest['files']:
    if row != old_by_name[row['path']]:
        changed.append(row['path'])
assert sorted(changed) == ['BMP_FAILED_ROUTES.json', 'RESEARCH_LOG.md']
old_routes = json.loads((private_receipt_path.parent / 'BMP_FAILED_ROUTES.json').read_text())
new_routes = json.loads((local / 'BMP_FAILED_ROUTES.json').read_text())
url_pattern = r"(https://validate\.perfdrive\.com/[^\s'\"<>?]+)\?[^\s'\"<>]*"
cleaned_error, replacements = re.subn(url_pattern, r'\1', old_routes[0]['error'])
assert replacements == 1 and cleaned_error == new_routes[0]['error']
old_routes[0]['error'] = cleaned_error
assert old_routes == new_routes
old_log = (private_receipt_path.parent / 'RESEARCH_LOG.md').read_bytes()
assert (local / 'RESEARCH_LOG.md').read_bytes().startswith(old_log)
assert not clean['scientific_findings_changed'] and not clean['primary_evidence_changed']

# Run the original synthesis integrity verifier without changing its folder.
synthesis = D / 'priority_synthesis_adversary_01'
run = subprocess.run(['python3', '-I', '-B', str(synthesis / 'verify_review.py')], capture_output=True, timeout=60)
(HERE / 'synthesis_verifier_stdout.json').write_bytes(run.stdout)
(HERE / 'synthesis_verifier_stderr.txt').write_bytes(run.stderr)
assert run.returncode == 0 and not run.stderr
assert json.loads(run.stdout)['four_family_manifest_entries'] == 89

# Its controls write a dated receipt, so copy the unchanged source and all
# required public inputs into a separate owned workspace before execution.
workspace = HERE / ('synthesis_replay_workspace_' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
workspace.mkdir(exist_ok=False)
for seal in seals[:4]:
    source = D / seal['family']
    target = workspace / seal['family']
    target.mkdir()
    filename = Path(seal['manifest']).name
    shutil.copy2(source / filename, target / filename)
    for row in json.loads((source / filename).read_text())['files']:
        dest = target / row['path']
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source / row['path'], dest)
replay = workspace / 'priority_synthesis_adversary_01'
replay.mkdir()
shutil.copy2(synthesis / 'independent_controls.py', replay / 'independent_controls.py')
assert sha(synthesis / 'independent_controls.py') == sha(replay / 'independent_controls.py')
run = subprocess.run(['python3', '-I', '-B', 'independent_controls.py'], cwd=replay, capture_output=True, timeout=60)
(HERE / 'synthesis_controls_stdout.json').write_bytes(run.stdout)
(HERE / 'synthesis_controls_stderr.txt').write_bytes(run.stderr)
assert run.returncode == 0 and not run.stderr
actual = json.loads(run.stdout)
expected = json.loads((synthesis / 'INDEPENDENT_CONTROLS_RECEIPT.json').read_text())
actual.pop('created_utc')
expected.pop('created_utc')
assert actual == expected and actual['exact_assertions'] == 13328

# Replay the current, sanitized BMP verifier; it also verifies the privately
# preserved original seal and the exact single-row redaction.
bmp = D / 'priority_bmp_archival_01'
run = subprocess.run(['python3', '-I', '-B', str(bmp / 'verify_archival_pass.py')], capture_output=True, timeout=60)
(HERE / 'bmp_sanitized_stdout.json').write_bytes(run.stdout)
(HERE / 'bmp_sanitized_stderr.txt').write_bytes(run.stderr)
assert run.returncode == 0 and not run.stderr
assert run.stdout == (bmp / 'verification_result.json').read_bytes()
sanitation = json.loads((bmp / 'sanitation_receipt.json').read_text())
original_receipt = bmp / sanitation['private_original_receipt_path']
assert (HERE / 'bmp_archival_stdout.json').read_bytes() == (original_receipt.parent / 'verification_result.json').read_bytes()

# Recheck the preceding four families' 134 full-source/evidence pins against
# actual retained bytes; source objects are unchanged by authored resealing.
previous = json.loads((D / 'ROOT_PRIORITY_PIN_VALIDATION.json').read_text())
earlier_private = [pin(D / row['path'], row) for row in previous['private_evidence_pins_verified']]
assert len(earlier_private) == 134

receipt = dict(
    utc=datetime.now(timezone.utc).isoformat(), status='PASS',
    current_public_seals=seals, public_pins=public,
    public_pins_verified=len(public), conlon_saved_private_objects_verified=conlon_private,
    conlon_saved_private_objects_count=22,
    local_limit_sanitation_original_private_payloads_verified=29,
    local_limit_only_error_field_and_appended_log_changed=True,
    BMP_current_sanitized_verifier_replayed=True, BMP_stdout_byte_identical=True,
    BMP_original_stdout_preserved_and_byte_identical=True, BMP_saved_private_objects_verified=31,
    preceding_four_family_private_pins_rechecked=earlier_private,
    total_primary_or_evidence_object_pins=134 + 22 + 31,
    synthesis_integrity_verifier_replayed=True, synthesis_exact_controls=13328,
    synthesis_replay_only_ignored_key='created_utc', all_other_fields_identical=True,
    limitations='Artifact and finite-control checks; analytic reports separately read in full. No novelty certificate.',
    private_reading_objects_publishable=False,
)
(D / 'ROOT_FINAL_PRIORITY_VALIDATION.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({k: v for k, v in receipt.items() if k not in ['public_pins', 'conlon_saved_private_objects_verified', 'preceding_four_family_private_pins_rechecked']}, indent=2))
