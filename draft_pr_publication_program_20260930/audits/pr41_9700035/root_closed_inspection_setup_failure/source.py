"""Root read-only complete retained evidence inspection; no helper imports."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path, PurePosixPath

A = Path(__file__).resolve().parent
R = A.parents[2]
started = dt.datetime.now(dt.timezone.utc).isoformat()

def sha(b):
    return hashlib.sha256(b).hexdigest()

def parse(b):
    def unique(items):
        out = {}
        for k, v in items:
            assert k not in out, ('duplicate', k)
            out[k] = v
        return out
    return json.loads(b, object_pairs_hook=unique,
                      parse_constant=lambda v: (_ for _ in ()).throw(ValueError(v)))

def eq(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(eq(a[k], v) for k, v in b.items())
    if isinstance(a, list):
        return len(a) == len(b) and all(eq(x, y) for x, y in zip(a, b))
    return a == b

def checked(root, row):
    n = row['path']; p = PurePosixPath(n)
    assert type(n) is str and n and not p.is_absolute() and '..' not in p.parts
    assert str(p) == n and '\\' not in n and '\0' not in n
    z = root/n
    assert z.is_file() and not z.is_symlink() and z.resolve().is_relative_to(root.resolve())
    assert all(not q.is_symlink() for q in z.parents if q != root and q.is_relative_to(root))
    size = row.get('bytes', row.get('size'))
    assert type(size) is int and size >= 0
    raw = z.read_bytes()
    assert len(raw) == size and sha(raw) == row['sha256'], n
    return raw

closures = [
    ('primary_scope_family', 'FIRST_PARTY_MANIFEST.json', '7d8318e0b7f7009ead1e19ae8c58008139da96c1b35ecfbbdf9fbe109ec830a8', 127),
    ('network_tail_measure_family', 'FIRST_PARTY_MANIFEST.json', '1b99b3ad334b970985ed3ba5f11d113fc4ed77793f7922b7b0142479821b750d', 115),
    ('root_original_actual_reproduction', 'MANIFEST.json', 'd8fb8a576676a690f9cb365f426bf3f344780bc1d03fbdc02f8534a44f3487f7', 130),
    ('root_family_controls_actual_reproduction', 'MANIFEST.json', '35f6efc31439e33795820b19d6df7a49451f649e6ccd71fac71956b4d0556840', 15),
]
records = []
for name, self_name, expected, count in closures:
    root = A/name; raw = (root/self_name).read_bytes()
    assert sha(raw) == expected
    m = parse(raw); rows = m['files']; assert type(rows) is list and len(rows) == count
    foreign = []
    if name == 'primary_scope_family':
        f = parse((root/'FOREIGN_CACHE_MANIFEST.json').read_bytes())
        foreign = [{**z, 'path':f['root']+'/'+z['path']} for z in f['files']]
        assert len(foreign) == 21
    if name == 'network_tail_measure_family':
        foreign = m['foreign_files']; assert len(foreign) == 8
    names = [z['path'] for z in rows+foreign]
    assert len(names) == len(set(names)) and self_name not in names
    expected_files = set(names) | {self_name}
    dirs = {p.as_posix() for n in expected_files for p in PurePosixPath(n).parents if p.as_posix() != '.'}
    actual_files = set(); actual_dirs = set(); parsed = 1; total = len(raw)
    for z in root.rglob('*'):
        assert not z.is_symlink() and (z.is_file() or z.is_dir()), str(z)
        (actual_dirs if z.is_dir() else actual_files).add(z.relative_to(root).as_posix())
    assert actual_files == expected_files, (name, actual_files ^ expected_files)
    assert actual_dirs == dirs, (name, actual_dirs ^ dirs)
    for z in rows+foreign:
        b = checked(root,z); total += len(b)
        if z in rows and PurePosixPath(z['path']).suffix == '.json':
            parse(b); parsed += 1
    records.append({'root': name, 'manifest_sha256': expected, 'authored': count,
                    'foreign': len(foreign), 'whole_bytes_checked': total,
                    'strict_complete_JSON_objects': parsed,
                    'exact_recursive_file_and_directory_closure': True})

actual_records = []
for family, receipt in [('root_original_actual_reproduction','ROOT_REPRODUCTION.json'),
                        ('root_family_controls_actual_reproduction','ROOT_FAMILY_REPRODUCTION.json')]:
    base = A/family; o = parse((base/receipt).read_bytes())
    assert o['status'] == 'PASS' and len(o['actual_outer_runs']) == 3
    assert type(o['original_substantive_attempts']) is int and o['original_substantive_attempts'] == 2
    assert type(o['new_substantive_attempts']) is int and o['new_substantive_attempts'] == 0
    assert type(o['audit_turns']) is int and o['audit_turns'] == 0
    for row in o['actual_outer_runs']:
        assert row['actual_execution'] is True and row['completed'] is True
        assert type(row['pid']) is int and row['pid'] > 0
        assert type(row['exit_code']) is int and row['exit_code'] == 0
        assert row['stdin_supplied'] is False and row['status'] == 'PASS'
        s,e = [dt.datetime.fromisoformat(row[k]) for k in ['started_utc','finished_utc']]
        assert s.tzinfo is not None and e.tzinfo is not None
        assert s.utcoffset() == e.utcoffset() == dt.timedelta(0) and s <= e
        source = Path(row['argv'][2]).read_bytes()
        assert sha(source) == row['source_sha256']
        for channel in ['stdout','stderr']:
            checked(base,row[channel])
        actual_records.append(row)

root = A/'root_original_actual_reproduction'
for private,saved,count in [('author_private','verification.json',211),
                            ('original_independent_private','review/independent_results.json',3809)]:
    actual = parse((root/private/saved).read_bytes())
    old = parse((A/'source_snapshot'/saved).read_bytes())
    assert eq(actual,old) and type(actual['passed']) is int and actual['passed'] == count
    assert type(actual['failed']) is int and actual['failed'] == 0 and len(actual['checks']) == count
    assert all(type(k) is str and k and type(v) is str and v == 'PASS' for k,v in actual['checks'].items())
    assert actual['proof_sha256'] == '464af6d259f9275ca9f0056567f5301bc228465fa0ddaf2faece0920cab6bd7c'
froot = A/'root_family_controls_actual_reproduction'
finite = parse((froot/'primary_finite_RESULT.json').read_bytes())
network = parse((froot/'network_measure_finite/NETWORK_MEASURE_CONTROL_RESULTS.json').read_bytes())
assert eq(network,parse((A/'network_tail_measure_family/NETWORK_MEASURE_CONTROL_RESULTS.json').read_bytes()))
assert type(finite['passed']) is int and finite['passed'] == len(finite['checks']) == 1326
assert type(network['checks_passed']) is int and network['checks_passed'] == len(network['checks']) == 122
result = {'schema':'pr41-root-complete-closed-evidence-inspection/v1', 'status':'PASS',
          'started_utc':started,'finished_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
          'actual_inspection_pid':os.getpid(),'source_sha256':sha(Path(__file__).read_bytes()),
          'closures':records,'six_actual_outer_runs':actual_records,
          'whole_original_211_and_3809_typed_objects_equal':True,
          'whole_network_saved_actual_object_equal':True,'primary_finite_checks':1326,
          'network_finite_checks':122,'original_substantive_attempts':2,
          'new_substantive_attempts':0,'audit_turns':0,'full_problem_solved':False,
          'scope':'Complete retained bytes/types/closures and actual captured metadata. Semantic mathematics is in the root scope certificate and read ledger; no future current or whole gate is certified.'}
out = A/'ROOT_CLOSED_FAMILY_INSPECTION.json'
with out.open('xb') as stream:
    stream.write((json.dumps(result,indent=2)+'\n').encode())
print(json.dumps({'status':'PASS','closures':records,'actual_runs':len(actual_records),'source_sha256':result['source_sha256']}))
