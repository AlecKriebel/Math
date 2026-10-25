"""Read-only validation of retained browser evidence; write only its own receipt."""
from pathlib import Path
import datetime
import hashlib
import json
import struct
import sys

OUT = Path(__file__).resolve().parent
BASE = OUT.parent

def digest(path):
    raw = path.read_bytes()
    return {'path': str(path), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

def check_entries(entries):
    result = []
    for expected in entries:
        path = Path(expected['path'])
        actual = digest(path) if path.exists() else {'path': str(path), 'bytes': None, 'sha256': None}
        actual['matches'] = actual['bytes'] == expected['bytes'] and actual['sha256'] == expected['sha256']
        result.append(actual)
    return result

def jpeg_dimensions(raw):
    assert raw[:2] == b'\xff\xd8'
    index = 2
    while index < len(raw):
        if raw[index] != 255:
            index += 1
            continue
        while raw[index] == 255:
            index += 1
        marker = raw[index]
        index += 1
        if marker in (0xD8, 0xD9, 0x01) or 0xD0 <= marker <= 0xD7:
            continue
        size = int.from_bytes(raw[index:index+2], 'big')
        if marker in (0xc0, 0xc1, 0xc2, 0xc3, 0xc5, 0xc6, 0xc7, 0xc9, 0xca, 0xcb, 0xcd, 0xce, 0xcf):
            height, width = struct.unpack('>HH', raw[index+3:index+7])
            return [width, height]
        index += size
    raise ValueError('JPEG frame dimensions not found')

baseline = json.loads((OUT/'preservation-before.json').read_text())
old_files = check_entries(baseline['files'])
readiness_path = BASE/'local-braid-wave-cantor-20261025/readiness-manifest.json'
readiness = json.loads(readiness_path.read_text())
ready_files = check_entries(readiness['files'])
frozen = json.loads((OUT/'frozen-manifests-after-browser.json').read_text())
frozen_results = []
for item in frozen['manifests']:
    manifest = json.loads(Path(item['manifest']).read_text())
    entries = check_entries(manifest['files'])
    frozen_results.append({'manifest': item['manifest'], 'manifest_matches_prior_hash': digest(Path(item['manifest']))['sha256'] == item['manifest_sha256'], 'checked': len(entries), 'all_match': all(e['matches'] for e in entries)})
shots = json.loads((OUT/'screenshot-manifest.json').read_text())['screenshots']
shot_checks = []
for shot in shots:
    path = Path(shot['path'])
    d = digest(path)
    dims = jpeg_dimensions(path.read_bytes())
    shot_checks.append({'file': path.name, 'bytes_match': d['bytes'] == shot['bytes'], 'sha256_match': d['sha256'] == shot['sha256'], 'dimensions': dims, 'dimensions_match': dims == [shot['width'], shot['height']]})
shot_map = {e['file']: e for e in shot_checks}
report = json.loads((OUT/'report.json').read_text())
for record in report['records']:
    assert shot_map[record['desktop']['capture']]['dimensions'] == [2056,1146]
    assert shot_map[record['narrow_browser_viewport']['capture']]['dimensions'] == [390,844]
    assert shot_map[record['visible_narrow_count']['capture']]['dimensions'] == [390,844]
cleanup = json.loads((OUT/'browser-cleanup.json').read_text())
assert cleanup['ownTabsAfter'] == []
assert len(cleanup['userTabsAfter']) == 11
assert any(e['id']=='963520539' for e in cleanup['userTabsAfter'])
result = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'evidence_preservation_files': len(old_files), 'evidence_preservation_all_match': all(e['matches'] for e in old_files), 'readiness_manifest': digest(readiness_path), 'readiness_reference_count': len(ready_files), 'readiness_reference_all_match': all(e['matches'] for e in ready_files), 'readiness_references': ready_files, 'frozen_manifests': frozen_results, 'raw_screenshot_count': len(shot_checks), 'raw_screenshots': shot_checks, 'cleanup_own_tabs':0, 'protected_sheet_listed': True}
result['all_pass'] = (result['evidence_preservation_all_match'] and result['readiness_reference_all_match'] and all(e['manifest_matches_prior_hash'] and e['all_match'] for e in frozen_results) and all(e['bytes_match'] and e['sha256_match'] and e['dimensions_match'] for e in shot_checks))
if '--write-receipt' in sys.argv:
    (OUT/'final-preservation-audit.json').write_text(json.dumps(result,indent=2)+'\n')
assert result['all_pass']
print(json.dumps({k:v for k,v in result.items() if k not in ('readiness_references','raw_screenshots')},indent=2))
