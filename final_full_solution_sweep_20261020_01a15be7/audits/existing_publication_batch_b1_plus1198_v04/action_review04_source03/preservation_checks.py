"""Read-only preservation check of earlier result and source packets."""
from pathlib import Path
import datetime, hashlib, json, stat
D = Path(__file__).resolve().parent
A = D.parent/'actor01'

def need(ok, msg):
    if not ok:
        raise RuntimeError(msg)

def check(e, root=None):
    p = (root/e['path']) if root else Path(e['path'])
    s = p.stat()
    raw = p.read_bytes()
    need(not p.is_symlink() and len(raw) == e['bytes']
         and hashlib.sha256(raw).hexdigest() == e['sha256'], 'Original preserved bytes changed')
    if 'mode' in e:
        need(stat.S_IMODE(s.st_mode) == e['mode'], 'Original mode changed')
    if 'mtime_ns' in e:
        need(s.st_mtime_ns == e['mtime_ns'], 'Original mtime changed')

counts = {}
old = json.loads((A/'PRESERVATION_BASELINE.json').read_text())['existing_v04_files']
for e in old:
    check(e, A.parent)
counts['original_v04_files'] = len(old)
for relative, name in [('private/sourceprep02/TEXT_PACKET_INDEX.json', 'closed_source02_payloads'),
                       ('private/semantic43_01/SEMANTIC_PACKET_INDEX.json', 'closed_semantic43_payloads')]:
    index = A/relative
    need(not index.is_symlink(), 'Original index symlink')
    payloads = json.loads(index.read_text())['payloads']
    for e in payloads:
        check(e)
    counts[name] = len(payloads)
report = {'at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'status': 'EARLIER_PACKETS_UNCHANGED', **counts,
          'all_recorded_modes_nsmtimes_checked': True, 'originals_modified': False,
          'real_actions': 0, 'root_action_accepted': False, 'publication_ready': False}
with (D/'PRESERVATION_READBACK.json').open('x') as f:
    json.dump(report, f, indent=2)
    f.write('\n')
print(json.dumps(report, indent=2))
