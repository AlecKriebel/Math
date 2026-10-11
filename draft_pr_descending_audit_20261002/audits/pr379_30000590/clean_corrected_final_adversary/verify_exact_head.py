#!/usr/bin/env python3
"""Read-only exact-object and byte-scope verification for corrected PR379."""
import hashlib, json, subprocess
from pathlib import Path

HERE = Path(__file__).absolute().parent
REPO = Path('/Users/alec/Documents/Math')
AUDIT = HERE.parent
HEAD = '4ee3016a755bb3553e712716dcd26b3d031836d0'
BASE = 'e75c8c1792c6e4cdd5ad331094d91b22b8c184a5'
OLD = '90794508688ec07f598e0871bbd1eb38aaf466ce'
TARGET = 'problems/30000590_group_ring_cohomology'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'
WRAPPERS = {'PUBLICATION_MANIFEST.json', 'PUBLICATION_STATUS.md', 'verify_publication.py'}
ADDITIONS = {'CURRENT_SCOPE_CORRECTION.md', 'CURRENT_SCOPE_MANIFEST.json'}

def git(*args):
    return subprocess.check_output(['git', '-C', str(REPO), *args])

def obj(commit, path):
    return git('show', f'{commit}:{path}')

def sha(data):
    return hashlib.sha256(data).hexdigest()

def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

manifest = json.loads((AUDIT / 'scope_repaired_snapshot_manifest.json').read_bytes())
assert manifest['head'] == HEAD and manifest['base'] == BASE and manifest['original_frozen_head'] == OLD
assert len(manifest['files']) == 58
entries = {e['path']: e for e in manifest['files']}
assert len(entries) == 58
for path, e in entries.items():
    data = obj(HEAD, path)
    local = (AUDIT / 'scope_repaired_snapshot' / path).read_bytes()
    assert local == data and len(data) == e['bytes'] and sha(data) == e['sha256'], path
    assert blob(data) == e['git_blob_sha'] == git('rev-parse', f'{HEAD}:{path}').decode().strip(), path
target_files = set(git('ls-tree', '-r', '--name-only', HEAD, '--', TARGET).decode().splitlines())
old_files = set(git('ls-tree', '-r', '--name-only', OLD, '--', TARGET).decode().splitlines())
assert len(target_files) == 57 and len(old_files) == 55
assert target_files | {QUEUE} == set(entries)
added = {p.removeprefix(TARGET+'/') for p in target_files-old_files}
modified = {p.removeprefix(TARGET+'/') for p in old_files if obj(HEAD,p) != obj(OLD,p)}
preserved = [p for p in sorted(old_files) if obj(HEAD,p) == obj(OLD,p)]
assert added == ADDITIONS and modified == WRAPPERS and len(preserved) == 52
diff_paths = set(git('diff', '--name-only', BASE, HEAD).decode().splitlines())
assert diff_paths == set(entries), sorted(diff_paths ^ set(entries))

# Preserve literally every byte of every other queue row, including predecessor380.
before, after = obj(BASE,QUEUE), obj(HEAD,QUEUE)
old_lines, new_lines = before.splitlines(keepends=True), after.splitlines(keepends=True)
assert len(old_lines) == len(new_lines)
changed = [i for i,(a,b) in enumerate(zip(old_lines,new_lines)) if a != b]
assert len(changed) == 1 and changed[0]+1 == 414
i = changed[0]
a,b = old_lines[i].split(b'|'), new_lines[i].split(b'|')
assert len(a) == len(b)
cells = [j for j,(x,y) in enumerate(zip(a,b)) if x != y]
assert cells == [8,9] and a[1].strip() == b[1].strip() == b'403'
assert b'30000590' in old_lines[i] and b'30000590' in new_lines[i]
assert a[8].strip() == b'queued' and a[9].strip() == b'0/5'
assert b[8].strip() == b'unsolved' and b[9].strip() == b'5/5'
rebuilt = old_lines[:]; restored = b[:]
for j in cells: restored[j] = a[j]
rebuilt[i] = b'|'.join(restored)
assert b''.join(rebuilt) == before
row380 = [l for l in old_lines if l.startswith(b'| 380 |')]
assert len(row380) == 1 and row380 == [l for l in new_lines if l.startswith(b'| 380 |')]
assert old_lines[379] == new_lines[379]

commits = {
 'turn1':'d40de2e4e3908689b220ba7efa22bbb99eb0c6fb',
 'turn2':'2d282c6892f711d45179f2239c15d9673aa9476c',
 'turn3':'b6d2b3e642670c924d2f938acef560a5c88ac895',
 'turn4':'aaf5268437e025cdf15c6c6df1410f0502aaa36b',
 'author_final':'a52e939b8302cde1e047bd9397de5a65de218e97',
 'locator_correction':'f8e50ea952ab99932aa6cddd57ba2a6f348c42a0',
 'original_published_head':OLD,
 'current_supplied_base':BASE,
}
for c in commits.values():
    assert subprocess.run(['git','-C',str(REPO),'merge-base','--is-ancestor',c,HEAD],capture_output=True).returncode == 0
bindings=[]
root = AUDIT/'scope_repaired_snapshot'/TARGET
for turn in range(1,6):
    name=f'TURN_{turn}_MANIFEST.json'
    m=json.loads((root/name).read_bytes())
    stage=commits.get(f'turn{turn}',commits['author_final'])
    assert obj(stage,TARGET+'/'+name) == (root/name).read_bytes()
    if turn>1:
        assert m['previous_manifest_sha256'] == sha((root/f'TURN_{turn-1}_MANIFEST.json').read_bytes())
    for e in m['files']:
        data=obj(stage,TARGET+'/'+e['path'])
        assert data==(root/e['path']).read_bytes() and len(data)==e['bytes'] and sha(data)==e['sha256']
        bindings.append({'manifest':name,'commit':stage,'path':e['path'],'sha256':sha(data)})
assert len(bindings)==28
for name,stage,folder in [
 ('FINAL_AUTHOR_MANIFEST.json',commits['author_final'],root),
 ('REVIEW_CORRECTION_MANIFEST.json',commits['locator_correction'],root),
 ('review/REVIEW_MANIFEST.json',OLD,root/'review'),
 ('PUBLICATION_MANIFEST.json',HEAD,root),
 ('CURRENT_SCOPE_MANIFEST.json',HEAD,root)]:
    m=json.loads((root/name).read_bytes())
    assert obj(stage,TARGET+'/'+name)==(root/name).read_bytes()
    for e in m['files']:
        rel=str((folder/e['path']).relative_to(root))
        data=obj(stage,TARGET+'/'+rel)
        assert data==(root/rel).read_bytes() and len(data)==e['bytes'] and sha(data)==e['sha256']
        bindings.append({'manifest':name,'commit':stage,'path':rel,'sha256':sha(data)})
remote=json.loads((root/'review/REMOTE_BINDING.json').read_bytes())
assert len(remote['files'])==43
for e in remote['files']:
    stage=commits['locator_correction']
    data=obj(stage,TARGET+'/'+e['path'])
    assert len(data)==e['bytes'] and blob(data)==e['git_blob_sha'] and data==(root/e['path']).read_bytes()
# Check the superseded publication wrapper's manifest against its own object,
# rather than interpreting its three replaced wrapper bytes as current bytes.
old_publication=json.loads(obj(OLD,TARGET+'/PUBLICATION_MANIFEST.json'))
for e in old_publication['files']:
    data=obj(OLD,TARGET+'/'+e['path'])
    assert len(data)==e['bytes'] and sha(data)==e['sha256']
    if TARGET+'/'+e['path'] in preserved:
        assert data==(root/e['path']).read_bytes()
    bindings.append({'manifest':'historical PUBLICATION_MANIFEST.json','commit':OLD,'path':e['path'],'sha256':sha(data)})
commit_headers={key:git('show','-s','--format=%H %P %cI %s',value).decode().strip() for key,value in commits.items()}
result={
 'status':'PASS','head':HEAD,'base':BASE,'original_head':OLD,
 'actual_git_bindings':58,'target_files':57,'preserved_historical_files':52,
 'modified_current_wrappers':sorted(modified),'additive_files':sorted(added),
 'queue_changed_lines':1,'queue_rank':403,'queue_physical_line':i+1,'queue_changed_pipe_cells':cells,
 'every_other_queue_byte_preserved':True,'physical_queue_line380_byte_preserved':True,
 'displayed_queue_rank380_byte_preserved':True,
 'historical_turn_bindings_from_stage_objects':28,
 'historical_author_bindings_from_author_object':40,
 'recorded_remote_raw_blob_ids_verified_from_correction_object':43,
 'nested_manifest_entries':len(bindings),'historical_publication_manifest_entries':len(old_publication['files']),
 'ancestral_objects_verified':commits,'actual_commit_headers':commit_headers,
 'historical_preserved_paths':preserved,'nested_bindings':bindings,
 'claim_scope':'Exact objects, bytes, ancestry and manifests only; not mathematical proof.'
}
print(json.dumps(result,indent=2))
