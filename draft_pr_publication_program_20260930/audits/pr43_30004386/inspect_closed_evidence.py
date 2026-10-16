"""ROOT whole-byte/typed evidence inspection, separate from mathematical proof."""
from pathlib import Path, PurePosixPath
import datetime as dt
import hashlib
import json
import math
import os
import stat

A = Path(__file__).resolve().parent
COUNT = 0


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def parse(raw):
    def pairs(items):
        out = {}
        for k, v in items:
            assert k not in out
            out[k] = v
        return out
    o = json.loads(raw, object_pairs_hook=pairs,
                   parse_constant=lambda v: (_ for _ in ()).throw(ValueError(v)))
    def visit(v):
        global COUNT
        COUNT += 1
        if type(v) is float:
            assert math.isfinite(v)
        elif type(v) is dict:
            for k, x in v.items():
                assert type(k) is str
                visit(x)
        elif type(v) is list:
            for x in v:
                visit(x)
        else:
            assert type(v) in (str, int, bool, type(None))
    visit(o)
    return o


def bound(base, row, frozen=False):
    name = row['path']; n = PurePosixPath(name)
    assert type(name) is str and not n.is_absolute() and n.as_posix() == name
    assert not {'.', '..', '.git', '__pycache__'}.intersection(n.parts)
    p = base / name
    assert p.is_file() and not p.is_symlink()
    assert all(not d.is_symlink() for d in p.parents)
    raw = p.read_bytes(); size = row.get('bytes', row.get('size'))
    assert type(size) is int and size >= 0
    assert len(raw) == size and sha(raw) == row['sha256']
    if frozen:
        assert stat.S_IMODE(p.stat().st_mode) == 0o444
    if name.endswith('.json'):
        parse(raw)
    elif name.endswith('.jsonl'):
        assert not raw or raw.endswith(b'\n')
        for line in raw.splitlines():
            parse(line)
    return raw


def closure(directory, self_name, pin, fields, frozen=False):
    base = A / directory; raw = (base / self_name).read_bytes()
    assert sha(raw) == pin
    manifest = parse(raw)
    rows = [row for field in fields for row in manifest[field]]
    names = {row['path'] for row in rows}
    assert len(names) == len(rows) and self_name not in names
    actual_files, actual_dirs = set(), set()
    for p in base.rglob('*'):
        assert not p.is_symlink()
        assert p.is_file() or p.is_dir()
        (actual_files if p.is_file() else actual_dirs).add(p.relative_to(base).as_posix())
    expected_dirs = {p.as_posix() for name in names for p in PurePosixPath(name).parents if p.as_posix() != '.'}
    assert actual_files == names | {self_name} and actual_dirs == expected_dirs
    for row in rows:
        bound(base, row, frozen)
    if frozen:
        assert stat.S_IMODE((base / self_name).stat().st_mode) == 0o444
    return {'directory': directory, 'manifest_sha256': pin, 'members': len(rows),
            'bytes': sum(row['bytes'] for row in rows), 'complete_manifest': manifest}


def main():
    snapshot = parse((A / 'snapshot_manifest.json').read_bytes())
    assert len(snapshot['files']) == 16
    for row in snapshot['files']:
        bound(A / 'source_snapshot', row, True)
    diff = (A / 'original_diff.patch').read_bytes()
    assert len(diff) == snapshot['diff_bytes'] and sha(diff) == snapshot['diff_sha256']
    assert diff.count(b'diff --git ') == 17
    assert (A / 'source_snapshot/turns.jsonl').read_bytes() == b''
    reproduction = A / 'root_original_actual_reproduction'
    result = parse((reproduction / 'RESULT.json').read_bytes())
    runs = parse((reproduction / 'ACTUAL_RUNS.json').read_bytes())
    # Real captures and every source/stream/result are bound by the complete
    # reproduction manifest. This inspector creates no new scientific run.
    own_manifest = reproduction / 'MANIFEST.json'
    rr = closure('root_original_actual_reproduction', 'MANIFEST.json', sha(own_manifest.read_bytes()), ['files'])
    cc = closure('compactness_source_family', 'OWNERSHIP_MANIFEST.json',
                 '9abc7c0dba6d4167201eec93608772be0bb26f31faf03e21805650e7d8ebc2b9',
                 ['first_party_files', 'foreign_individually_excluded'])
    pp = closure('probability_source_family', 'SELF_MANIFEST.json',
                 'de68537cda5407bf5b0c1a4dcd28de7ae51c96932d4b3af84aca389d82607e7c', ['files'])
    assert len(cc['complete_manifest']['first_party_files']) == 18
    assert len(cc['complete_manifest']['foreign_individually_excluded']) == 8
    assert pp['complete_manifest']['first_party_file_count'] == 43
    assert pp['complete_manifest']['individual_foreign_file_count'] == 23
    for row in parse((A / 'source_snapshot/source_checksums.json').read_bytes()):
        raw = (A / 'foreign_primary' / {'original.pdf': 'owr2020.pdf', 'jkp2022.pdf': 'jkp_v2.pdf'}[row['cache_filename']]).read_bytes()
        assert len(raw) == row['bytes'] and sha(raw) == row['sha256']
    output = {'schema': 'pr43-root-closed-evidence-inspection/v1',
              'utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'actual_pid': os.getpid(),
              'status': 'PASS', 'snapshot16_and_complete_diff17': True,
              'closed_reproduction': rr, 'compactness_family': cc, 'probability_family': pp,
              'entire_reproduction_result': result, 'entire_actual_runs': runs,
              'typed_nodes_visited': COUNT, 'scientific_helpers_executed': False,
              'original_substantive_attempts': 0, 'new_substantive_attempts': 0,
              'audit_turns': 0, 'future_whole_current_verdict': None}
    with (A / 'ROOT_CLOSED_EVIDENCE_INSPECTION.json').open('x') as f:
        json.dump(output, f, indent=2); f.write('\n')
    print(json.dumps({'status': 'PASS', 'actual_pid': os.getpid(),
                      'members': [rr['members'], cc['members'], pp['members']],
                      'typed_nodes_visited': COUNT,
                      'result_sha256': sha((A / 'ROOT_CLOSED_EVIDENCE_INSPECTION.json').read_bytes())}))


if __name__ == '__main__':
    main()
