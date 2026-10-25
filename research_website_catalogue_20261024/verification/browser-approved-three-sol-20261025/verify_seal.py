"""Validate this partial bundle without changing files or contacting any service."""
from pathlib import Path
import gzip
import hashlib
import json

OUT = Path(__file__).resolve().parent
manifest_path = OUT/'evidence-manifest.json'
seal = json.loads((OUT/'SEAL.json').read_text())
assert hashlib.sha256(manifest_path.read_bytes()).hexdigest() == seal['manifest_sha256']
manifest = json.loads(manifest_path.read_text())
for entry in manifest['files']:
    p = Path(entry['path'])
    raw = p.read_bytes()
    assert len(raw) == entry['bytes'], str(p)
    assert hashlib.sha256(raw).hexdigest() == entry['sha256'], str(p)
    assert 'private' not in p.relative_to(OUT).parts
compression = json.loads((OUT/'baseline-compression-receipt.json').read_text())
raw_baseline = gzip.decompress((OUT/'preservation-before.json.gz').read_bytes())
assert len(raw_baseline) == compression['uncompressed_bytes']
assert hashlib.sha256(raw_baseline).hexdigest() == compression['uncompressed_sha256']
assert len(json.loads(raw_baseline)['files']) == 125037
report = json.loads((OUT/'report.json').read_text())
assert report['all_gates_complete'] is False
assert report['full_browser_PASS'] is False
assert report['native_tracker_acceptance'] is False
assert report['index_completed_counts'] == [50, 50, 50]
shots = json.loads((OUT/'screenshot-manifest.json').read_text())
assert shots['count'] == 22 and shots['accepted'] == 17 and shots['excluded'] == 5
for entry in shots['screenshots']:
    assert (entry['width'],entry['height']) in ((2056,1146),(390,844))
assert (OUT/'.gitignore').read_text() == 'private/\n'
print(json.dumps({'status':'PARTIAL_BUNDLE_SEAL_VERIFIED','files':manifest['file_count'],'raw_screenshots':shots['count'],'baseline_entries':125037,'all_browser_gates_complete':False},indent=2))
