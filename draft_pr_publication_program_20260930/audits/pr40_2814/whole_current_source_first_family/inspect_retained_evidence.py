"""Own read-only byte/type inspection; never imports or executes audited code."""
from pathlib import Path, PurePosixPath
import collections, datetime, hashlib, json

A = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent
sha = lambda raw: hashlib.sha256(raw).hexdigest()

def require(value, message):
    if not value: raise ValueError(message)

def pairs(items):
    result = {}
    for key, value in items:
        require(key not in result, 'Duplicate key '+key)
        result[key] = value
    return result

def parse(raw):
    return json.loads(raw, object_pairs_hook=pairs,
        parse_constant=lambda value: (_ for _ in ()).throw(ValueError('Nonfinite '+value)))

def read(path):
    require(path.is_file() and not path.is_symlink(), 'Nonregular '+str(path))
    require(all(not p.is_symlink() for p in path.parents), 'Symlink ancestor')
    return path.read_bytes()

def typed(value):
    name = type(value).__name__
    if type(value) is dict: return [name, [[k, typed(v)] for k, v in sorted(value.items())]]
    if type(value) is list: return [name, [typed(v) for v in value]]
    return [name, value]

def type_count(value):
    c = collections.Counter({type(value).__name__: 1})
    if type(value) is dict:
        for v in value.values(): c.update(type_count(v))
    if type(value) is list:
        for v in value: c.update(type_count(v))
    return c

def row(path):
    raw = read(path)
    return {'path': path.relative_to(A).as_posix(), 'size': len(raw), 'sha256': sha(raw)}

def check(root, r):
    name = r['path']; p = PurePosixPath(name)
    require(type(name) is str and name and str(p) == name and not p.is_absolute()
        and all(x not in ('', '.', '..') for x in name.split('/')), 'Unsafe path')
    size = r.get('size', r.get('bytes'))
    require(type(size) is int and size >= 0, 'Size is not integer')
    raw = read(root/name)
    require(len(raw) == size and sha(raw) == r['sha256'], 'Byte mismatch '+name)
    return raw

def inventory(root, excluded):
    files, dirs = set(), set()
    for p in root.rglob('*'):
        name = p.relative_to(root).as_posix()
        if PurePosixPath(name).parts[0] in excluded: continue
        require(not p.is_symlink(), 'Symlink member '+name)
        if p.is_file(): files.add(name)
        else: require(p.is_dir(), 'Special file'); dirs.add(name)
    return files, dirs

def main():
    pins = parse(read(A/'current_preparation_family/INPUT_PINS.json'))
    all_files = set(); closures = []
    for name, info in pins['families'].items():
        root = A/name; entries = info['members']; names = [r['path'] for r in entries]
        require(len(names) == len(set(names)), 'Duplicate family path')
        files, dirs = inventory(root, info['excluded_root_directories'])
        require(files == set(names)|{info['manifest_name']} and dirs == set(info['directories']), 'Exact family topology')
        require(sha(read(root/info['manifest_name'])) == info['manifest_sha256'], 'Manifest pin')
        for r in entries: check(root, r)
        all_files.update(root/n for n in files)
        closures.append({'family':name, 'members':len(entries), 'directories':sorted(dirs), 'exact_root_exclusions':info['excluded_root_directories']})
    for name, info in pins['capture_closures'].items():
        root = A/name
        require(inventory(root, []) == (set(r['path'] for r in info['members']), set(info['directories'])), 'Exact capture topology')
        for r in info['members']: check(root, r)
        all_files.update(root/r['path'] for r in info['members'])
    for r in pins['fixed_inputs']:
        check(A, r); all_files.add(A/r['path'])
    prep = parse(read(A/'current_preparation_family/PREPARATION_MANIFEST.json'))
    require(inventory(A/'current_preparation_family', []) == (set(r['path'] for r in prep['files'])|{'PREPARATION_MANIFEST.json'}, set()), 'Exact preparation topology')
    for r in prep['files']: check(A/'current_preparation_family', r)
    all_files.update((A/'current_preparation_family').iterdir())
    foreign = []
    for prefix, info in pins['foreign_inventory'].items():
        require(inventory(A/prefix, []) == (set(r['path'] for r in info['members']), set(info['directories'])), 'Foreign topology')
        for r in info['members']: check(A/prefix, r)
        foreign.append({'root':prefix,'count':len(info['members']),'all_whole_bytes_checked':True,'copied_as_first_party':False})
    json_rows = []
    for p in sorted(all_files):
        raw = read(p)
        if p.suffix == '.json':
            value = parse(raw)
            json_rows.append(dict(row(p), root_type=type(value).__name__, node_types=dict(type_count(value)),
                complete_typed_tree_sha256=sha(json.dumps(typed(value),ensure_ascii=False,separators=(',',':')).encode())))
    selected = parse(read(A/'root_original_actual_capture/results/SELECTED_COMPLETE_SOURCE_PAIRS.json'))
    for r, n, prior in zip(selected, ('source_record.json','duplicate_record.json'), ('prior_report.json','duplicate_prior_report.json')):
        require(typed(r['raw_problem']) == typed(parse(read(A/'source_snapshot'/n))), 'Whole typed source')
        require(typed(r['raw_report']) == typed(parse(read(A/'source_snapshot'/prior))), 'Whole typed prior')
    require(selected[0]['raw_report'] is None and selected[0]['raw_report_key_present'] is False and typed(selected[0]['sql_fallback_report']) == typed({}), 'Null/fallback conflation')
    capture = parse(read(A/'root_original_actual_capture/CAPTURE.json'))
    for stream in ('stdout','stderr'): check(A/'root_original_actual_capture', capture[stream])
    runs = parse(read(A/'root_family_actual_capture/ROOT_ACTUAL_CAPTURE.json'))['actual_runs']
    for r in runs:
        require(r['actual_execution'] is True and r['completed'] is True and type(r['returncode']) is int and r['returncode'] == 0, 'Actual family completion')
        source = read(A/'root_family_actual_capture'/r['label']/'prelaunch_source.py')
        require(len(source) == r['program_size'] and sha(source) == r['program_sha256'], 'Executed source pin')
        for stream in ('stdout','stderr'): check(A/'root_family_actual_capture', r[stream])
    controls = parse(read(A/'root_family_actual_capture/primary_manifest_controls/RESULT.json'))['controls']
    for r in controls:
        for stream in ('stdout','stderr'):
            raw = read(A/'root_family_actual_capture/primary_manifest_controls/complete_control_streams'/r['label']/('ACTUAL_'+stream.upper()+'.bin'))
            require(len(raw) == r[stream]['size'] and sha(raw) == r[stream]['sha256'], 'Nested actual stream')
        require(type(r['returncode']) is int and r['returncode'] == r['expected_returncode'], 'Control outcome')
    result = {'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(), 'status':'BYTE_TYPE_TOPOLOGY_INSPECTION_PASS',
        'inspector':row(Path(__file__)), 'first_party_files': [row(p) for p in sorted(all_files)],
        'closed_family_exact_topologies':closures, 'separate_foreign_byte_inventories':foreign, 'whole_typed_JSON':json_rows,
        'selected_complete_source_prior_typed_equal':True, 'null_report_distinct_from_SQL_fallback':True,
        'actual_outer_sources_streams_checked':True,'actual_primary_nested_streams_checked':True,
        'proposal_or_old_verifier_imported_or_executed':False, 'scientific_or_current_verdict':None,
        'geometry_fixture_qualification':'Twelve historical fixture trees were deleted by their producer; constructors and complete structured outputs are retained, not the trees.',
        'original_substantive_attempts':0,'turn_limit':5,'new_substantive_attempts':0,'audit_turns':0}
    target = OUT/'RETAINED_EVIDENCE_TYPED_BYTE_TOPOLOGY.json'
    require(not target.exists(), 'Preserve prior receipt')
    target.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'status':result['status'],'first_party_files':len(all_files),'whole_JSON':len(json_rows),'receipt_sha256':sha(read(target))}))

if __name__ == '__main__': main()
