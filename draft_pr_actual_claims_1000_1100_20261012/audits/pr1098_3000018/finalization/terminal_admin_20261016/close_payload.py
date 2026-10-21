"""Close only the bounded current administrative payload and outer binding."""
from pathlib import Path
import hashlib
import json
import sys

sys.dont_write_bytecode = True
F = Path(__file__).resolve().parent
C = F.parents[1]/'preprint_v1_0'
sys.path.insert(0, str(C/'code'))
from common import archive_bytes

def record(p):
    b = p.read_bytes()
    return {'bytes':len(b), 'sha256':hashlib.sha256(b).hexdigest()}

def save(p, obj):
    p.write_text(json.dumps(obj, sort_keys=True, indent=2)+'\n')

def main():
    original = json.loads((F/'before/preprint_v1_0/MANIFEST.json').read_text())
    old_paths = [r['path'] for r in original['entries']]
    additions = ['TERMINAL_STATUS.json'] + [str(p.relative_to(C)) for p in (C/'terminal').rglob('*') if p.is_file()]
    paths = sorted(set(old_paths + additions))
    if len(paths) != len(old_paths) + len(additions):
        raise ValueError('new administrative member collides with original payload')
    manifest = dict(original)
    manifest['entries'] = [{'path':name, **record(C/name)} for name in paths]
    save(C/'MANIFEST.json', manifest)
    # archive_bytes returns only after ZipFile.close has written the directory.
    (C/'pr1098_support_v1_0.zip').write_bytes(archive_bytes())
    binding = json.loads((F/'before/preprint_v1_0/DEPOSIT_BINDING.json').read_text())
    binding['artifacts'] = {name:record(C/name) for name in binding['artifacts']}
    save(C/'DEPOSIT_BINDING.json', binding)
    save(F/'CLOSED_PAYLOAD.json', {'payload_members':len(paths),
        'archive_members':len(paths)+1, 'paper':record(C/'paper.pdf'),
        'closed_archive':record(C/'pr1098_support_v1_0.zip'),
        'deposit_binding':record(C/'DEPOSIT_BINDING.json'),
        'metadata':record(C/'metadata.json'),
        'native_manifest':record(C/'publication/zenodo-deposit.json'),
        'archive_read_after_close':True})
    print(json.dumps({'payload_members':len(paths), 'archive':record(C/'pr1098_support_v1_0.zip')}))

if __name__ == '__main__':
    main()
