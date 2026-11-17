"""Read-only data diagnosis authorized by root after literal v1 fail-stop."""
import datetime
import hashlib
import json
from pathlib import Path
import stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
S = P / 'verification/wreath-dyadic-stress-stage-sol-20261116'
OWN = P / 'verification/stage3-post-publication-audit-sol-20261117'
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
expected = json.loads((S / 'PROSPECTIVE_PUBLIC.json').read_bytes())
started = datetime.datetime.now(datetime.timezone.utc).isoformat()

def census(root):
    files, directories, exceptional = [], [], []
    stack = [root]
    while stack:
        here = stack.pop()
        for path in here.iterdir():
            rel = path.relative_to(root).as_posix()
            info = path.lstat()
            mode = format(stat.S_IMODE(info.st_mode), '04o')
            if stat.S_ISDIR(info.st_mode):
                directories.append({'path': rel, 'mode': mode})
                stack.append(path)
            elif stat.S_ISREG(info.st_mode):
                raw = path.read_bytes()
                files.append({'path': rel, 'bytes': len(raw), 'SHA256': hashlib.sha256(raw).hexdigest(), 'mode': mode})
            else:
                exceptional.append({'path': rel, 'raw_mode': info.st_mode})
    return {'root': str(root), 'root_mode': format(stat.S_IMODE(root.lstat().st_mode), '04o'), 'files': sorted(files, key=lambda x: x['path']), 'directories': sorted(directories, key=lambda x: x['path']), 'regular_files': len(files), 'child_directories': len(directories), 'exceptional_entries': exceptional}

def compare(old, new):
    result = {'nonlist_values': {k: {'expected': old[k], 'observed': new.get(k)} for k in old if k not in ('files', 'directories') and old[k] != new.get(k)}}
    for label, keys in [('files', {'path', 'bytes', 'SHA256', 'mode'}), ('directories', {'path', 'mode'})]:
        before, after = old[label], new[label]
        bm, am = {x['path']: x for x in before}, {x['path']: x for x in after}
        result[label] = {'expected_count': len(before), 'observed_count': len(after), 'expected_duplicates': len(before) - len(bm), 'observed_duplicates': len(after) - len(am), 'expected_invalid_schema': [x for x in before if set(x) != keys], 'observed_invalid_schema': [x for x in after if set(x) != keys], 'missing': sorted(set(bm) - set(am)), 'extra': sorted(set(am) - set(bm)), 'different_path_mode_hash_byte_maps': {k: {'expected': bm[k], 'observed': am[k]} for k in sorted(set(bm) & set(am)) if bm[k] != am[k]}, 'order_differences': [{'index': i, 'expected_path': a['path'], 'observed_path': b['path']} for i, (a, b) in enumerate(zip(before, after)) if a['path'] != b['path']]}
    return result

staged, live = census(S / 'candidate/public'), census(W)
result = {'schema': 'exact-post-failure-inventory-topology-diagnostic-v1', 'started_UTC': started, 'completed_UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'expected_to_actual_stage': compare(expected, staged), 'expected_to_actual_live': compare(expected, live), 'actual_stage_to_actual_live': compare(staged, live), 'root_identities_preserved': {'expected': expected['root'], 'actual_stage': staged['root'], 'actual_live': live['root']}, 'exceptional_entries': {'stage': staged['exceptional_entries'], 'live': live['exceptional_entries']}, 'expected_top_keys': list(expected), 'actual_top_keys': list(staged), 'new_audit_invocation': False, 'native_index_or_objects_read': False, 'completion_percent': 65}
with (OWN / 'SCHEMA_TOPOLOGY_DIAGNOSTIC.json').open('x') as out:
    json.dump(result, out, indent=2)
    out.write('\n')
print(json.dumps({'schema': result['schema'], 'result_path': str(OWN / 'SCHEMA_TOPOLOGY_DIAGNOSTIC.json')}))
