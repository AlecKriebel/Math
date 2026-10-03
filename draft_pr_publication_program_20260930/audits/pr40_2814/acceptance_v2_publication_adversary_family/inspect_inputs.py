#!/usr/bin/env python3
"""Independent read-only bytes/topology/AST inspection; no reviewed code loads."""
import ast
import datetime
import difflib
import hashlib
import json
import os
from pathlib import Path, PurePosixPath

ROOT = Path('/Users/alec/Documents/Math')
AUDIT = ROOT / 'draft_pr_publication_program_20260930/audits/pr40_2814'
REV = AUDIT / 'acceptance_execution_preparation_family/integration_source_revision_v2'
record = {}
closures = []
foreign = []

def sha(raw): return hashlib.sha256(raw).hexdigest()
def strict(raw):
    def pairs(items):
        out = {}
        for key, value in items:
            assert key not in out, ('duplicate', key)
            out[key] = value
        return out
    def finite(value): raise ValueError(value)
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=finite)

def canonical(name):
    path = PurePosixPath(name)
    assert type(name) is str and name and not path.is_absolute()
    assert path.as_posix() == name and '..' not in path.parts and '\\' not in name and '\0' not in name
    return path

def read(path):
    path = Path(path)
    assert path.is_file() and not path.is_symlink(), path
    for parent in path.parents:
        assert not parent.is_symlink(), parent
        if parent == ROOT: break
    raw = path.read_bytes()
    name = path.relative_to(ROOT).as_posix()
    info = {'path': name, 'bytes': len(raw), 'sha256': sha(raw)}
    if name in record: assert record[name] == info
    record[name] = info
    return raw

def rows(value):
    if type(value) is dict: value = [dict(v, path=k) for k,v in value.items()]
    assert type(value) is list
    names = []
    for item in value:
        canonical(item['path'])
        size = item.get('bytes', item.get('size'))
        assert type(size) is int and size >= 0
        assert 'size' not in item or 'bytes' not in item or type(item['size']) is int and item['size'] == size
        assert type(item['sha256']) is str and len(item['sha256']) == 64 and all(c in '0123456789abcdef' for c in item['sha256'])
        names.append(item['path'])
    assert len(names) == len(set(names))
    return value

def check(base, value):
    for item in rows(value):
        raw = read(base/item['path'])
        assert len(raw) == item.get('bytes', item.get('size')) and sha(raw) == item['sha256'], item

def exact(base, names, excluded=()):
    assert base.is_dir() and not base.is_symlink()
    files, directories = set(), set()
    for parent, dirs, fnames in os.walk(base, followlinks=False):
        if Path(parent) == base: dirs[:] = [d for d in dirs if d not in excluded]
        for name in dirs + fnames:
            path = Path(parent)/name
            assert not path.is_symlink(), path
            relative = path.relative_to(base).as_posix()
            canonical(relative)
            if path.is_dir(): directories.add(relative)
            else:
                assert path.is_file(), path
                files.add(relative)
    expected_dirs = {p.as_posix() for name in names for p in PurePosixPath(name).parents if str(p) != '.'}
    assert files == set(names) and directories == expected_dirs, (base, sorted(files-set(names)), sorted(set(names)-files))
    return sorted(directories)

def closure(base, manifest_name, expected_pin, count, field='files', exclusions=()):
    raw = read(base/manifest_name)
    assert sha(raw) == expected_pin
    obj = strict(raw)
    members = rows(obj[field])
    assert len(members) == count and manifest_name not in {m['path'] for m in members}
    for key in ['files_count','member_count']:
        if key in obj: assert type(obj[key]) is int and obj[key] == count
    check(base, members)
    dirs = exact(base, {m['path'] for m in members}|{manifest_name}, exclusions)
    closures.append({'root': str(base.relative_to(ROOT)), 'manifest': manifest_name, 'manifest_sha256': expected_pin, 'count':count, 'directories':dirs, 'excluded_root_directories':list(exclusions)})
    return obj

v2=closure(REV, 'PREPARATION_MANIFEST.json', 'e5f0ce1f9cbc890767ef8131ac760d39562c9fba0faf41df208c3d0ebb3832ba',17)
v1=closure(REV.parent/'integration_source_revision','PREPARATION_MANIFEST.json','65e71adae289b4243036f50be90b28bdeadca3dbd3fd99c5dfc605a72e053c0e',15)
closure(AUDIT/'acceptance_revised_static_adversary_family','FIRST_PARTY_MANIFEST.json','0480281a6dd9629183d1d7e2ad98b098a3b5eae8b8b423dbc4bc72eda85403cf',31)
closure(AUDIT/'acceptance_revised_static_adversary_metadata_qualification_family','FIRST_PARTY_MANIFEST.json','bc05c4971ee61d50080005ce2084597098c97acc8a11f66d95d08514524cb8bb',6)
closure(AUDIT/'acceptance_preparation_family','PREPARATION_MANIFEST.json','a7bbde5e024a6e432d7456586651208b3f365170cfc80112e0b98de1cae4c39b',12)
closure(AUDIT/'acceptance_static_adversary_family','FIRST_PARTY_MANIFEST.json','84b0e1c5364fac20617c1242e36c0d5b9130ea2784de81d3557ae8cbe94ab526',22)

for filename, member_key in [('REVISION_BINDINGS.json','immutable_revision_inputs'), ('PREDECESSOR_REVISION_BINDINGS.json','immutable_refs')]:
    check(ROOT,strict(read(REV/filename))[member_key])
inputs=strict(read(REV/'INPUT_BINDINGS.json'))
for binding in inputs['pins'].values(): check(ROOT,[binding])
for item in inputs['closures']:
    base=ROOT/item['root']
    if item['manifest']:
        check(ROOT,[item['manifest']])
        closure(base,Path(item['manifest']['path']).name,item['manifest']['sha256'],item['authored_count_excluding_self'],item['member_field'],item['excluded_root_directories'])
    else:
        check(base,item['files'])
        dirs=exact(base,{m['path'] for m in item['files']})
        closures.append({'root':str(base.relative_to(ROOT)),'manifest':None,'count':len(item['files']),'directories':dirs,'excluded_root_directories':[]})

current=closure(AUDIT/'reviewed_candidate','MANIFEST.json','8de92d903edaec7471f4ecc3df443b7e779732b0ee83cdec507c22025bfae25f',239)
for m in current['files']+[{'path':'MANIFEST.json'}]: assert ((AUDIT/'reviewed_candidate'/m['path']).stat().st_mode & 0o777) == 0o444
dep=strict(read(AUDIT/'reviewed_candidate/CURRENT_PROOF_DEPENDENCIES.json'))
assert dep['dependency_anchor_repository_relative'] == str(AUDIT.relative_to(ROOT)) and len(rows(dep['files'])) == 216
check(AUDIT,dep['files'])
snap=strict(read(AUDIT/'snapshot_manifest.json'))
assert len(rows(snap['files'])) == 13
for member in snap['files']:
    raw=read(AUDIT/'source_snapshot'/member['path'])
    assert raw == read(AUDIT/'reviewed_candidate'/member['path']) == read(AUDIT/'reviewed_candidate/original_archive'/member['path'])
assert strict(read(AUDIT/'source_snapshot/prior_report.json')) is None
assert strict(read(AUDIT/'source_snapshot/turns.json'))['count'] == 0
assert strict(read(AUDIT/'source_snapshot/turns.json'))['substantive_attempts'] == []
assert type(strict(read(AUDIT/'source_snapshot/duplicate_prior_report.json'))) is dict

original_foreign=strict(read(AUDIT/'current_preparation_family/INPUT_PINS.json'))['foreign_inventory']
assert set(original_foreign)=={'primary_scope_family/foreign_cache','geodesic_geometry_family/primary'}
for name,item in original_foreign.items():
    check(AUDIT/name,item['members'])
    dirs=exact(AUDIT/name,{m['path'] for m in item['members']})
    foreign.append({'root':str((AUDIT/name).relative_to(ROOT)),'count':len(item['members']),'directories':dirs,'files':item['members']})
whole=AUDIT/'whole_current_source_first_family'
wf=strict(read(whole/'FOREIGN_PRIMARY_INVENTORY.json'))['exact_recursive_inventory']
assert len(rows(wf))==21 and all(canonical(m['path']).parts[0]=='ROOTforeign_primary' for m in wf)
check(whole,wf)
whole_members=strict(read(whole/'FIRST_PARTY_MANIFEST.json'))['files']
exact(whole,{m['path'] for m in whole_members+wf}|{'FIRST_PARTY_MANIFEST.json'})
foreign.append({'root':str(whole.relative_to(ROOT)),'count':21,'files':wf})

ast_records=[]
for name in ['pr40_guards.py','seal_final_evidence.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py']:
    raw=read(REV/name)
    syntax=ast.parse(raw,filename=str(REV/name))
    ast_records.append({'path':str((REV/name).relative_to(ROOT)),'bytes':len(raw),'sha256':sha(raw),'lines':len(raw.splitlines()),'nodes':sum(1 for _ in ast.walk(syntax)),'imported_compiled_executed':False})
driver=ROOT/'draft_pr_publication_program_20260930/infrastructure/accepted_state_sync/revision2/accepted_state_sync_v2.py'
assert sha(read(driver))=='ca7576ece5bc37a6e569a62764541de773243d38bffa811f4d1174f25635667f'
ast.parse(read(driver),filename=str(driver))

changed=['pr40_guards.py','integrate_reviewed_partial.py','CONTRACT.md','CHANGE_RECORD.json','STATIC_SOURCE_REVIEW.json']
patch=''.join(''.join(difflib.unified_diff(read(REV.parent/'integration_source_revision'/n).decode().splitlines(keepends=True),read(REV/n).decode().splitlines(keepends=True),fromfile='preserved_v1/'+n,tofile='v2/'+n)) for n in changed)
assert patch.encode() == read(REV/'SOURCE_CHANGES.patch')
for n in ['seal_final_evidence.py','state_mirror_reconciliation.py','verify_post_acceptance.py','SCIENTIFIC_SCOPE.json','DRAFT_FINAL_PLAN.json','INPUT_BINDINGS.json','REVISION_BINDINGS.json']:
    assert read(REV/n)==read(REV.parent/'integration_source_revision'/n)
scope=strict(read(REV/'SCIENTIFIC_SCOPE.json'))
draft=strict(read(REV/'DRAFT_FINAL_PLAN.json'))
assert draft['scientific_scope']==scope
assert draft['preparation_manifest_sha256'] is None
assert all(draft[k] is False for k in ['root_full_current_read_completed','root_full_whole_read_completed','independent_whole_current_pass'])
for p in list(record):
    path=ROOT/p
    if path.suffix=='.json': strict(read(path))

print(json.dumps({'status':'PASS_SOURCE_DATA_ONLY','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pid':os.getpid(),'reviewed_code_import_compile_execution':False,'unique_input_members':len(record),'unique_input_bytes':sum(i['bytes'] for i in record.values()),'closures':closures,'foreign_inventories_individually_bound':foreign,'source_AST':ast_records,'input_members':[record[p] for p in sorted(record)],'actual_future_acceptance_claimed':False,'new_substantive_attempts':0,'audit_turns':0},sort_keys=True,indent=2))
