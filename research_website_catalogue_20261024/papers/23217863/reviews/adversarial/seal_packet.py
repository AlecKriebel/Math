"""One-use own-namespace final sealing after recorded input rehashes."""
from pathlib import Path
import datetime
import hashlib
import json

D = Path(__file__).resolve().parent
assert D == Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23217863/reviews/adversarial')


def binding(path):
    raw = path.read_bytes()
    return dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def verify(row):
    assert binding(Path(row['path'])) == row, row['path']


assert not (D / 'FINAL_MANIFEST.json').exists()
assert not (D / 'FINAL_SEAL.json').exists()
assert binding(D / 'EARLY_SEAL.json')['sha256'] == 'e818c5efc3ae6ebfc48d7d224c1dd1a97192eba8a370ff3de133832d5d3cb746'
early = json.loads((D / 'EARLY_SEAL.json').read_text())
for name in ('ledger', 'source_ready', 'source_manifest', 'source_seal', 'actual_reader', 'control_tex'):
    verify(early[name])
original = json.loads((D / 'ORIGINAL_BINDINGS.json').read_text())
for row in original['originals']:
    verify(row)
for name in ('source_manifest', 'source_seal', 'archive'):
    verify(original[name])
preserved = json.loads((D / 'PRESERVATION_BINDINGS.json').read_text())
for packet in preserved['prior_packets']:
    verify(packet['manifest'])
    verify(packet['seal'])
    for row in packet['owned_files']:
        verify(row)
for row in preserved['actual_primary_pdf_objects'] + preserved['raw_primary_receipts']:
    verify(row)
utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
(D / 'FINAL_PRESERVATION.json').write_text(json.dumps(dict(
    utc=utc, status='ALL_RECORDED_INPUTS_REHASHED_UNCHANGED', originals=50,
    complete_zip_members=41, primary_pdf_objects=10, prior_packets=9,
    prior_owned_files=130, original_receipt=binding(D / 'ORIGINAL_BINDINGS.json'),
    preservation_receipt=binding(D / 'PRESERVATION_BINDINGS.json')),
    indent=2) + '\n')
with (D / 'RESEARCH_LOG.md').open('a') as f:
    f.write(f'- {utc} — 100%. Complete original theorem survives bounded independent review; all recorded inputs unchanged, final packet sealed. No repair, priority certification, follow-up or publication authorization; root authority retained and overall203 goal ongoing.\n')
rows = []
for path in sorted(D.iterdir()):
    if path.is_file():
        row = binding(path)
        row['path'] = path.name
        rows.append(row)
manifest = dict(utc=utc, record_id='23217863', status='SEALED_COMPLETE_ADVERSARIAL_PACKET',
                files=rows, ignored_disposable_renders_excluded=True)
(D / 'FINAL_MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
(D / 'FINAL_SEAL.json').write_text(json.dumps(dict(
    utc=utc, manifest='FINAL_MANIFEST.json', manifest_sha256=binding(D / 'FINAL_MANIFEST.json')['sha256'],
    owned_files=len(rows), root_authority_retained=True, overall_203_goal='ONGOING'),
    indent=2) + '\n')
for path in D.iterdir():
    if path.is_file():
        path.chmod(0o444)
for name in ('REPORT.md', 'verdict.json', 'DERIVATIONS.md', 'UPSTREAM_PROOF_AUDIT.md', 'FINAL_MANIFEST.json', 'FINAL_SEAL.json'):
    print(json.dumps(binding(D / name), sort_keys=True))
