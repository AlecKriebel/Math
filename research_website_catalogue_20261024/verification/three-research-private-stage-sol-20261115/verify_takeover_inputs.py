#!/usr/bin/env python3
"""Pure default: authenticate fixed three source namespaces and whole interfaces.

No project imports, scientific execution, subprocess, network or writes. All
external files must be listed in the frozen original reference input or be
within its exact protected namespace. Historical blobs are compared literally,
not relabelled as a new semantic scientific reading.
"""
from pathlib import Path
import hashlib, json, os, stat, sys

N = Path(__file__).absolute().parent
P = N.parent.parent
ALLOWED = {}
CHECKS = 0
TYPED_NODES = 0

def need(ok, message):
    global CHECKS
    CHECKS += 1
    if not ok:
        raise ValueError(message)

def pin(data):
    return {'bytes': len(data), 'SHA256': hashlib.sha256(data).hexdigest()}

def read(path):
    path = Path(path)
    need(path.is_absolute() and '..' not in path.parts, 'absolute canonical path')
    need(path.is_relative_to(N) or str(path) in ALLOWED, 'only owned or exact original input')
    for parent in path.parents:
        need(not parent.is_symlink(), 'no symlink ancestor')
    first = path.lstat()
    need(stat.S_ISREG(first.st_mode), 'regular file')
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        before = os.fstat(fd)
        need((first.st_dev, first.st_ino) == (before.st_dev, before.st_ino), 'held identity')
        parts = []
        while True:
            part = os.read(fd, 1048576)
            if not part:
                break
            parts.append(part)
        after = os.fstat(fd)
        final = path.lstat()
        need((before.st_size, before.st_mtime_ns, before.st_ctime_ns) == (after.st_size, after.st_mtime_ns, after.st_ctime_ns), 'stable whole buffer')
        need((final.st_dev, final.st_ino) == (before.st_dev, before.st_ino), 'stable pathname')
        data = b''.join(parts)
        need(len(data) == before.st_size, 'whole read')
        if str(path) in ALLOWED:
            need(pin(data) == ALLOWED[str(path)], 'original whole-byte pin ' + str(path))
        return data
    finally:
        os.close(fd)

def bound(row):
    data = read(Path(row['path']))
    need(pin(data) == {key: row[key] for key in ['bytes', 'SHA256']}, 'reference same-buffer pin')
    return data

def permit_original(row):
    path = Path(row['path'])
    need(path.is_absolute() and path.is_relative_to(P) and '..' not in path.parts, 'literal original reference stays within programme')
    value = {key: row[key] for key in ['bytes', 'SHA256']}
    need(str(path) not in ALLOWED or ALLOWED[str(path)] == value, 'no conflicting original pin')
    ALLOWED[str(path)] = value

def typed(a, b):
    global TYPED_NODES
    TYPED_NODES += 1
    need(type(a) is type(b), 'literal original JSON type')
    if type(a) is dict:
        need(list(a) == list(b), 'whole original key order')
        for key in a:
            typed(a[key], b[key])
    elif type(a) is list:
        need(len(a) == len(b), 'whole original list length')
        for x, y in zip(a, b):
            typed(x, y)
    else:
        need(a == b, 'literal scalar/null/history')

def namespace(group):
    root = Path(group['root'])
    expected_files = {row['relative_path']: row for row in group['files']}
    expected_dirs = set(group['directories'])
    files, directories = [], []
    def visit(directory):
        first = directory.lstat()
        need(stat.S_ISDIR(first.st_mode), 'ordinary namespace directory')
        for path in sorted(directory.iterdir()):
            name = path.relative_to(root).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISDIR(mode):
                need(name in expected_dirs, 'no unlisted original directory')
                directories.append(name)
                visit(path)
            elif stat.S_ISREG(mode):
                need(name in expected_files, 'no unlisted original file')
                need(Path(expected_files[name]['path']) == path, 'exact original namespace path')
                bound(expected_files[name])
                files.append(name)
            else:
                raise ValueError('special original namespace entry')
        last = directory.lstat()
        need((first.st_dev, first.st_ino, first.st_mtime_ns, first.st_ctime_ns) == (last.st_dev, last.st_ino, last.st_mtime_ns, last.st_ctime_ns), 'stable namespace enumeration')
    visit(root)
    need(sorted(files) == sorted(expected_files) and sorted(directories) == sorted(expected_dirs), 'whole original extent')
    need(len(files) == group['file_count'] and len(directories) == group['directory_count'], 'original extent counts')
    need(group['no_exclusions'] is True, 'no source namespace exclusions')
    return [len(files), len(directories)]

def main():
    need(sys.argv[1:] == [], 'pure default only')
    reference_raw = read(N / 'REFERENCE_INPUTS.json')
    need(pin(reference_raw) == {'bytes': 1143550, 'SHA256': '5cdedc034da6e31114db6490667e5f558819bf73cc224105fdc54c595e459855'}, 'immutable prior reference')
    ref = json.loads(reference_raw)
    records = ref['records']
    need([row['record_id'] for row in records] == ['23418581', '23202966', '23205305'], 'fixed132135136 only')
    need([row['sheet_row'] for row in records] == [132, 135, 136], 'excluded133137')
    for group in ref['complete_frozen_namespaces_by_reference'].values():
        for row in group['files']:
            ALLOWED[row['path']] = {key: row[key] for key in ['bytes', 'SHA256']}
    core = ref['qualified_core']
    for row in [core['reference'], *core['named17_original_plus_sole_authorized405b']]:
        ALLOWED[row['path']] = {key: row[key] for key in ['bytes', 'SHA256']}
    for row in records:
        for key in ['adoption', 'approved_config', 'approved_MAIN', 'approved_copy', 'approved_head_source', 'approved_Bib']:
            item = row[key]
            ALLOWED[item['path']] = {key: item[key] for key in ['bytes', 'SHA256']}
    extents = {name: namespace(group) for name, group in ref['complete_frozen_namespaces_by_reference'].items()}
    for row in [core['reference'], *core['named17_original_plus_sole_authorized405b']]:
        bound(row)
    need(len(core['named17_original_plus_sole_authorized405b']) == 18, '17 original plus one sole authorized405b')
    need(next(row for row in core['named17_original_plus_sole_authorized405b'] if row['path'].endswith('/checkpoint_subtree.py'))['SHA256'] == '405b0357fd20a2e14893ce6c3c1a0f81910894ccd8ffaddac4e25014138fb9c0', 'sole qualified checkpoint')
    total_main = 0
    for row in records:
        buffers = {key: bound(row[key]) for key in ['adoption', 'approved_config', 'approved_MAIN', 'approved_copy', 'approved_head_source', 'approved_Bib']}
        total_main += len(buffers['approved_MAIN'])
        config = json.loads(buffers['approved_config'])
        if row['record_id'] == '23418581':
            ready = json.loads(read(P / 'papers/23418581/sources/SOURCE_READY.json'))
            typed(ready, config['source_binding']['whole_original_source_ready'])
            for wrapper in config['source_binding']['whole_native_API_objects']:
                permit_original(wrapper['original'])
                typed(json.loads(bound(wrapper['original'])), wrapper['whole_original_object'])
            wrapper = config['review_metadata']['root_authority']
            permit_original(wrapper['original'])
            typed(json.loads(bound(wrapper['original'])), wrapper['whole_literal_object'])
            for wrapper in config['review_metadata']['whole_original_scientific_verdicts']:
                permit_original(wrapper['original'])
                typed(json.loads(bound(wrapper['original'])), wrapper['whole_original_object'])
            assets = ready['all_native_assets_in_original_order']
            need(config['canonical_url'] is None and config['AA'] is None and config['follow_up'] is None, '132 historical nulls retained')
            need(config['production_authority'] is False, '132 historical nonauthority retained')
        else:
            assets = config['publication']['all_original_assets']
            need(config['promotion']['canonical_url'] is None and config['promotion']['AA'] is None and config['promotion']['follow_up'] is None, '135136 historical nulls retained')
            need(config['promotion']['production_install_authority'] is False and config['promotion']['root_copy_adopted'] is False, '135136 historical nonauthority retained')
        typed(assets, row['native_assets_in_original_order'])
        for asset in assets:
            data = bound(asset)
            need(hashlib.md5(data).hexdigest() == asset['original_api_file_object']['checksum'].removeprefix('md5:'), 'whole native checksum')
        need(buffers['approved_MAIN'].startswith(('<main id="' + row['semantic_main_id'] + '">').encode()), 'whole semantic MAIN anchor')
        need(row['production_authority'] is False and row['source_canonical_and_AA_fields_remain_null'] is True, 'reference nonauthority')
    need(total_main == 40599, 'whole three MAIN40599B')
    print(json.dumps({'status': 'TAKEOVER_ORIGINAL_INPUTS_AND_INTERFACES_UNCHANGED', 'checks': CHECKS, 'typed_nodes': TYPED_NODES, 'protected_namespaces': extents, 'total_protected_files': sum(counts[0] for counts in extents.values()), 'whole_MAIN_bytes': total_main, 'qualified_original_core': 17, 'sole_authorized_checkpoint405b': True, 'new_scientific_rereview': False, 'source_or_original_helper_execution': False, 'writes': 0, 'network_requests': 0, 'publication_authority': False, 'canonical_url': None, 'AA': None, 'follow_up': None}, sort_keys=True))

if __name__ == '__main__':
    main()
