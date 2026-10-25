"""One-use own-namespace final seal; no supplied code is executed."""
import datetime
import hashlib
import json
from pathlib import Path

D = Path(__file__).resolve().parent
assert D == Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23331258/reviews/adversarial')


def binding(path):
    raw = path.read_bytes()
    return dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def verify(row):
    assert binding(Path(row['path'])) == row, row['path']


assert not (D / 'FINAL_MANIFEST.json').exists()
assert not (D / 'FINAL_SEAL.json').exists()
original = json.loads((D / 'ORIGINAL_BINDINGS.json').read_text())
for row in original['originals']:
    verify(row)
for key in ('source_ready_manifest', 'source_ready_seal', 'outer_archive', 'nested_tar'):
    verify(original[key])
preserved = json.loads((D / 'PRESERVATION_BINDINGS.json').read_text())
for packet in preserved['prior_packets']:
    verify(packet['manifest'])
    verify(packet['seal'])
    for row in packet['owned_files']:
        verify(row)
for row in preserved['primary_objects'] + preserved['primary_receipts']:
    verify(row)
verify(preserved['source_ready_manifest'])
verify(preserved['source_ready_seal'])
assert binding(D / 'EARLY_SEAL.json')['sha256'] == '6a58a6a4836ea9e0eedf9b661f615232ceab830e83b889060512f80a56b0975b'
utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
(D / 'FINAL_PRESERVATION.json').write_text(json.dumps(dict(
    utc=utc, status='ALL_RECORDED_INPUTS_REHASHED_UNCHANGED', originals=60,
    outer_members=50, nested_tar_members=7, prior_packets=8,
    prior_owned_files=114, actual_primary_pdfs=8,
    original_receipt=binding(D / 'ORIGINAL_BINDINGS.json'),
    preservation_receipt=binding(D / 'PRESERVATION_BINDINGS.json')),
    indent=2) + '\n')
with (D / 'RESEARCH_LOG.md').open('a') as f:
    f.write(f'- {utc} — 100%. Complete bounded independent review sealed; all original/primary/prior-owned inputs rehashed unchanged. Complete original theorem survives; no firstness certification, repair, publication authorization or follow-up. Overall203-paper goal ongoing.\n')
rows = []
for path in sorted(D.iterdir()):
    if path.is_file():
        row = binding(path)
        row['path'] = path.name
        rows.append(row)
manifest = dict(utc=utc, record_id='23331258', status='SEALED_COMPLETE_ADVERSARIAL_PACKET',
                files=rows, disposable_ignored_renders_excluded=True)
(D / 'FINAL_MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
seal = dict(utc=utc, manifest='FINAL_MANIFEST.json',
            manifest_sha256=binding(D / 'FINAL_MANIFEST.json')['sha256'],
            owned_files=len(rows), root_authority_retained=True,
            overall_203_goal='ONGOING')
(D / 'FINAL_SEAL.json').write_text(json.dumps(seal, indent=2) + '\n')
for path in D.iterdir():
    if path.is_file():
        path.chmod(0o444)
for name in ('REPORT.md', 'verdict.json', 'DERIVATIONS.md', 'FINAL_MANIFEST.json', 'FINAL_SEAL.json'):
    print(json.dumps(binding(D / name), sort_keys=True))
