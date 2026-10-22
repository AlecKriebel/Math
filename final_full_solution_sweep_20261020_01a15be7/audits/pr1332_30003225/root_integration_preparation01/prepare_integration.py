"""Read-only GitHub observation and pure Git tree planning; never applies a plan.

Only GET, git ls-remote and read-only local Git queries are allowed. All writes
are ordinary files under this new audit directory, never a Git object store.
"""
from pathlib import Path
import base64
import datetime
import difflib
import gzip
import hashlib
import io
import json
import os
import stat
import subprocess

P = Path(__file__).resolve().parent
S = P.parent/'publication_preparation_03'
REPO = 'repos/AlecKriebel/Math/'
PROJECT = 'unsolved_math_prioritization/attempts/30003225'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'
PREFIX = 'unsolved_math_prioritization'
ATTEMPTS = PREFIX+'/attempts'


def require(ok, label):
    if not ok:
        raise RuntimeError(label)


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def git_hash(kind, data, algorithm='sha1'):
    return hashlib.new(algorithm, kind.encode()+b' '+str(len(data)).encode()+b'\0'+data).hexdigest()


def compressed(data):
    stream = io.BytesIO()
    with gzip.GzipFile(filename='', fileobj=stream, mode='wb', compresslevel=9, mtime=0) as f:
        f.write(data)
    return stream.getvalue()


def save_json(name, value):
    (P/name).write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)+'\n')


def get(endpoint, label):
    target = P/'private/api'/label
    target.parent.mkdir(exist_ok=True, parents=True)
    if target.exists():
        # Every cache key used here is an immutable Git commit/tree/blob SHA1.
        # Mutable refs are freshly advertised separately; no service action.
        return json.loads(gzip.decompress(target.read_bytes()))
    x = subprocess.run(['gh', 'api', '--method', 'GET', REPO+endpoint], capture_output=True)
    target.write_bytes(compressed(x.stdout))
    target.with_suffix(target.suffix+'.stderr').write_bytes(x.stderr)
    require(x.returncode == 0, 'GET failed '+endpoint)
    return json.loads(x.stdout)


def tree_payload(entries):
    require(len({e['path'] for e in entries}) == len(entries), 'duplicate tree names')
    ordered = sorted(entries, key=lambda e: e['path'].encode()+(b'/' if e['type']=='tree' else b''))
    out = bytearray()
    for e in ordered:
        require('/' not in e['path'] and '\0' not in e['path'] and e['path'] not in ('.', '..'), 'unsafe tree name')
        mode = e['mode'].lstrip('0')
        require(mode in ('40000', '100644', '100755', '120000', '160000'), 'unknown Git mode')
        out.extend(mode.encode()+b' '+e['path'].encode()+b'\0'+bytes.fromhex(e['sha']))
    return bytes(out)


TREES = {}
BLOBS = {}


def tree(oid):
    if oid not in TREES:
        j = get('git/trees/'+oid, 'tree_'+oid+'.json.gz')
        require(j['sha']==oid and not j.get('truncated', False), 'incomplete tree')
        body = tree_payload(j['tree'])
        require(git_hash('tree', body)==oid, 'actual Git tree hash differs')
        TREES[oid] = j['tree']
    return TREES[oid]


def child(entries, name, required=True):
    rows = [e for e in entries if e['path']==name]
    require(len(rows)<=1 and (rows or not required), 'missing/duplicate tree child '+name)
    return rows[0] if rows else None


def lookup(root, path, required=True):
    entries = tree(root)
    for i, part in enumerate(path.split('/')):
        e = child(entries, part, required)
        if e is None:
            return None
        if i < len(path.split('/'))-1:
            require(e['type']=='tree', 'ancestor not tree')
            entries = tree(e['sha'])
    return e


def blob(oid):
    if oid not in BLOBS:
        j = get('git/blobs/'+oid, 'blob_'+oid+'.json.gz')
        require(j['sha']==oid and j['encoding']=='base64', 'Git blob encoding/identity')
        b = base64.b64decode(j['content'])
        require(len(b)==j['size'] and git_hash('blob', b)==oid, 'actual Git blob bytes mismatch')
        BLOBS[oid] = b
    return BLOBS[oid]


def flat_tree(oid, prefix=''):
    rows = {}
    for e in tree(oid):
        n = prefix+e['path']
        if e['type']=='tree':
            rows.update(flat_tree(e['sha'], n+'/'))
        else:
            rows[n] = dict(e, path=n)
    return rows


def row_in(data):
    lines = data.splitlines(keepends=True)
    hits = [i for i, x in enumerate(lines) if b'| 30003225 / OWR-14754-011 |' in x]
    require(len(hits)==1, 'QUEUE unique exact problem row')
    return lines, hits[0], lines[hits[0]].split(b'|')


def current_remote():
    env = dict(os.environ, GIT_OPTIONAL_LOCKS='0', GIT_TERMINAL_PROMPT='0')
    x = subprocess.run(['git', 'ls-remote', 'origin', 'refs/heads/main', 'refs/heads/dot/30003225-nash-intersection-20261013'], capture_output=True, env=env)
    require(x.returncode==0, 'read-only remote advertisement failed')
    return dict((line.split()[1].decode(), line.split()[0].decode()) for line in x.stdout.splitlines())


def main():
    observed = datetime.datetime.now(datetime.timezone.utc).isoformat()
    refs = current_remote()
    main_commit = refs['refs/heads/main']
    pr = json.loads(gzip.decompress((P/'private/initial_PR.stdout.json.gz').read_bytes()))
    files = json.loads(gzip.decompress((P/'private/initial_PR_files_page1.stdout.json.gz').read_bytes()))
    require(pr['head']['sha']==refs['refs/heads/'+pr['head']['ref']], 'PR branch advanced since original observation')
    require(pr['state']=='open' and not pr['merged'] and len(files)==pr['changed_files']==8, 'live original PR scope changed')
    compare = json.loads(gzip.decompress((P/'private/PR_comparison.json.gz').read_bytes()))
    original_base = compare['merge_base_commit']['sha']
    head_commit = json.loads(gzip.decompress((P/'private/head_commit.json.gz').read_bytes()))
    mc = get('git/commits/'+main_commit, 'dated_main_commit_'+main_commit+'.json.gz')
    bc = get('git/commits/'+original_base, 'original_diff_base_commit_'+original_base+'.json.gz')
    head_root, base_root, main_root = head_commit['tree']['sha'], bc['tree']['sha'], mc['tree']['sha']
    head_project = lookup(head_root, PROJECT)
    original_flat = flat_tree(head_project['sha'])
    expected_names = {x['filename'][len(PROJECT)+1:] for x in files if x['filename'].startswith(PROJECT+'/')}
    require(set(original_flat)==expected_names and len(expected_names)==7, 'original project scope not exact seven readers')
    provenance = json.loads((S/'science/SOURCE_PROVENANCE.json').read_text())
    expected_blobs = {v['path']: v for v in provenance['actual_eight_original_blobs']}
    require(set(expected_blobs)=={x['filename'] for x in files}, 'original eight source bindings changed')
    originals = {}
    for f in files:
        e = lookup(head_root, f['filename'])
        b = blob(e['sha'])
        require(e['sha']==f['sha']==expected_blobs[f['filename']]['git_blob'], 'original Git object binding')
        require(sha256(b)==expected_blobs[f['filename']]['sha256'] and len(b)==expected_blobs[f['filename']]['bytes'], 'original content binding')
        originals[f['filename']] = {'entry':e, 'bytes':b}
    print('Original eight actual blobs, project scope and modes authenticated.', flush=True)
    main_project = lookup(main_root, PROJECT, False)
    existing = flat_tree(main_project['sha']) if main_project else {}
    selected = {}
    def select(path, data, mode, source):
        require(path not in selected, 'duplicate selected path')
        require(mode in ('100644', '100755'), 'only regular selected modes')
        selected[path] = {'bytes_value':data, 'mode':mode, 'source':source}
    for name, v in originals.items():
        if name != QUEUE:
            select(name, v['bytes'], v['entry']['mode'], 'original PR head '+pr['head']['sha'])
    pointer = (P/'PUBLICATION.md').read_bytes()
    select(PROJECT+'/PUBLICATION.md', pointer, '100644', 'new reviewed integration pointer; no solution DOI')
    for kind, target in [('release', 'publication'), ('science', 'publication/source')]:
        paths = [q for q in sorted((S/kind).rglob('*')) if q.is_file()]
        require(len(paths)==(6 if kind=='release' else 21), 'exact public source count')
        for q in paths:
            require(not q.is_symlink() and stat.S_IMODE(q.stat().st_mode)==0o644, 'source bytes/mode not regular0644')
            name = q.relative_to(S/kind).as_posix()
            select(PROJECT+'/'+target+'/'+name, q.read_bytes(), '100644', 'frozen preparation03/'+kind+'/'+name)
    head_queue = originals[QUEUE]['bytes']
    base_qe, main_qe = lookup(base_root, QUEUE), lookup(main_root, QUEUE)
    base_queue, main_queue = blob(base_qe['sha']), blob(main_qe['sha'])
    bl, bi, cells_b = row_in(base_queue)
    hl, hi, cells_h = row_in(head_queue)
    ml, mi, cells_m = row_in(main_queue)
    require(len(bl)==len(hl) and bi==hi and all(a==b for i,(a,b) in enumerate(zip(bl,hl)) if i!=bi), 'original QUEUE changes outside target row')
    require(len(cells_b)==len(cells_h)==len(cells_m), 'QUEUE target schema changed')
    changed_cells = [i for i,(a,b) in enumerate(zip(cells_b,cells_h)) if a!=b]
    require(changed_cells==[8,9,11], 'original QUEUE edit not Status/Turns/Findings only')
    proposed_cells = cells_m[:]
    for i in changed_cells:
        require(cells_m[i].strip() in (cells_b[i].strip(), cells_h[i].strip()), 'concurrent target-cell conflict requires HOLD')
        proposed_cells[i] = cells_h[i]
    findings = proposed_cells[11]
    trailing = findings[len(findings.rstrip(b' \t')):]
    proposed_cells[11] = findings.rstrip(b' \t')+b' [Publication package](attempts/30003225/PUBLICATION.md).'+trailing
    new_lines = ml[:]
    new_lines[mi] = b'|'.join(proposed_cells)
    new_queue = b''.join(new_lines)
    require(all(a==b for i,(a,b) in enumerate(zip(ml,new_lines)) if i!=mi), 'other QUEUE bytes changed')
    require(all(proposed_cells[i]==cells_m[i] for i in range(len(cells_m)) if i not in changed_cells), 'unselected target cells changed')
    select(QUEUE, new_queue, main_qe['mode'], 'current live-main QUEUE with original target three-cell edit plus publication pointer')
    for filename,a,b in [('ORIGINAL_QUEUE_EDIT.diff',base_queue,head_queue),('CURRENT_MAIN_QUEUE_EDIT.diff',main_queue,new_queue)]:
        (P/filename).write_text(''.join(difflib.unified_diff(a.decode().splitlines(True),b.decode().splitlines(True),fromfile='before/'+QUEUE,tofile='after/'+QUEUE)))
    save_json('QUEUE_RECONCILIATION.json', {'original_PR_base_field':pr['base']['sha'],'actual_original_diff_merge_base':original_base,
        'original_head':pr['head']['sha'],'base_queue_blob':base_qe['sha'],'original_head_queue_blob':originals[QUEUE]['entry']['sha'],
        'current_main_queue_blob':main_qe['sha'],'new_queue_blob':git_hash('blob',new_queue),'original_changed_cell_indices':changed_cells,
        'original_changes_only_target_row':True,'new_changes_only_target_three_cells':True,'all_other_current_main_QUEUE_bytes_exact':True,
        'publication_pointer_suffix':'[Publication package](attempts/30003225/PUBLICATION.md).',
        'original_base_row':bl[bi].decode(),'original_head_row':hl[hi].decode(),'current_main_row':ml[mi].decode(),'proposed_row':new_lines[mi].decode()})
    payload_dir = P/'private/selected_payloads'
    payload_dir.mkdir()
    unique = {}
    manifest = []
    for path,v in sorted(selected.items()):
        data = v['bytes_value']; oid = git_hash('blob', data)
        if oid not in unique:
            raw = compressed(data); q = payload_dir/(oid+'.blob.gz'); q.write_bytes(raw)
            require(gzip.decompress(q.read_bytes())==data, 'selected gzip readback')
            unique[oid] = {'payload':q.relative_to(P).as_posix(),'gzip_bytes':len(raw),'gzip_sha256':sha256(raw),'gzip_header_hex':raw[:10].hex()}
        manifest.append({'path':path,'mode':v['mode'],'bytes':len(data),'sha256':sha256(data),'git_blob_sha1':oid,
                         'git_object_sha256':git_hash('blob',data,'sha256'),'source':v['source'],**unique[oid]})
    project_entries = dict(existing)
    for row in manifest:
        if row['path'].startswith(PROJECT+'/'):
            name = row['path'][len(PROJECT)+1:]
            if name in existing:
                require(existing[name]['sha']==row['git_blob_sha1'] and existing[name]['mode']==row['mode'], 'existing selected project path conflict')
            project_entries[name] = {'path':name,'mode':row['mode'],'sha':row['git_blob_sha1'],'type':'blob'}
    computed = {}
    def store_tree(path, entries):
        data = tree_payload(entries); oid = git_hash('tree',data)
        d = P/'private/computed_tree_payloads'; d.mkdir(exist_ok=True)
        q = d/(oid+'.tree.gz')
        if not q.exists():q.write_bytes(compressed(data))
        require(gzip.decompress(q.read_bytes())==data, 'computed tree readback')
        computed[path] = {'tree_sha1':oid,'git_object_sha256':git_hash('tree',data,'sha256'),'raw_bytes':len(data),'raw_sha256':sha256(data),
                          'payload':q.relative_to(P).as_posix(),'gzip_sha256':sha256(q.read_bytes()),'entries':sorted(entries,key=lambda e:e['path'])}
        return oid
    def nest(path, flat):
        immediate = {}; folders = {}
        for name,e in flat.items():
            if '/' in name:
                first, rest = name.split('/',1);folders.setdefault(first,{})[rest] = dict(e,path=rest)
            else:immediate[name] = dict(e,path=name)
        for name,children in folders.items():
            require(name not in immediate, 'file/tree name conflict')
            immediate[name] = {'path':name,'mode':'040000','type':'tree','sha':nest(path+'/'+name,children)}
        return store_tree(path,list(immediate.values()))
    project_tree = nest(PROJECT, project_entries)
    def replace(entries, changes):
        m = {e['path']:dict(e)for e in entries};m.update(changes);return list(m.values())
    main_attempts = lookup(main_root, ATTEMPTS)
    attempts_tree = store_tree(ATTEMPTS,replace(tree(main_attempts['sha']),{'30003225':{'path':'30003225','mode':'040000','type':'tree','sha':project_tree}}))
    main_prefix = lookup(main_root,PREFIX)
    queue_new = next(v for v in manifest if v['path']==QUEUE)
    prefix_tree = store_tree(PREFIX,replace(tree(main_prefix['sha']),{'attempts':{'path':'attempts','mode':'040000','type':'tree','sha':attempts_tree},'QUEUE.md':{'path':'QUEUE.md','mode':main_qe['mode'],'type':'blob','sha':queue_new['git_blob_sha1']}}))
    root_tree = store_tree('',replace(tree(main_root),{PREFIX:{'path':PREFIX,'mode':'040000','type':'tree','sha':prefix_tree}}))
    preserved = []
    for path,old_oid,allowed in [('',main_root,{PREFIX}),(PREFIX,main_prefix['sha'],{'attempts','QUEUE.md'}),(ATTEMPTS,main_attempts['sha'],{'30003225'})]:
        before = {e['path']:{k:e[k]for k in['path','mode','type','sha']}for e in tree(old_oid) if e['path'] not in allowed}
        after = {e['path']:{k:e[k]for k in['path','mode','type','sha']}for e in computed[path]['entries'] if e['path'] not in allowed}
        require(before==after,'unselected ancestor siblings differ')
        preserved.append({'ancestor':path or '/', 'unselected_siblings':len(before),'all_names_modes_types_object_ids_exact':True})
    forbidden = [v['path'] for v in manifest if any(x in v['path'].split('/') for x in ('.gitignore','private','.git','primary'))]
    require(not forbidden and len(manifest)==36, 'selected payload scope differs')
    save_json('SELECTED_PAYLOAD_MANIFEST.json', {'schema':'pr1332-readonly-selected-payloads-v1','dated_remote_main':main_commit,
        'original_PR_head':pr['head']['sha'],'project_path':PROJECT,'entries':manifest,'selected_path_count':len(manifest),'unique_blob_count':len(unique),
        'gzip_convention':'GzipFile empty filename, mtime0, compresslevel9; header hex and compressed digest recorded per unique blob. Decompressed bytes are exact Git blob bodies, no Git header.',
        'Git_repository_object_format':'SHA1; git_object_sha256 independently hashes canonical Git header plus body, not a native SHA256 repository object ID.',
        'only_project_plus_target_QUEUE':True,'actual_effects':0})
    save_json('COMPUTED_TREES.json', {'schema':'pr1332-pure-computed-trees-v1','dated_remote_main':main_commit,'original_main_root_tree':main_root,
        'proposed_root_tree':root_tree,'project_tree':project_tree,'trees':computed,'ancestor_unselected_sibling_preservation':preserved,'no_Git_object_store_writes':True})
    originals_receipt = []
    for path,v in sorted(originals.items()):
        b = v['bytes'];originals_receipt.append({'path':path,'mode':v['entry']['mode'],'git_blob_sha1':git_hash('blob',b),'bytes':len(b),'sha256':sha256(b),'git_object_sha256':git_hash('blob',b,'sha256'),'original_source_provenance_exact':True})
    save_json('ORIGINAL_PR_SCOPE.json', {'PR':1332,'head':pr['head']['sha'],'branch':pr['head']['ref'],'base_field':pr['base']['sha'],
        'actual_original_diff_base':original_base,'state':pr['state'],'draft':pr['draft'],'merged':pr['merged'],'full_changed_paths_count':8,
        'original_head_root_tree':head_root,'original_project_tree':head_project['sha'],'original_project_exact_seven_readers':True,
        'actual_original_blobs':originals_receipt,'new_manifest_preserves_all_seven_exact':True,'original_18_44_check_claims_not_newly_replayed':True})
    save_json('DATED_INTEGRATION_PLAN.json', {'schema':'pr1332-readonly-dated-integration-plan-v1','observed_at':observed,
        'remote_refs':refs,'dated_main_commit':main_commit,'dated_main_tree':main_root,'proposed_root_tree':root_tree,'project_tree':project_tree,
        'source_preparation_seal_sha256':'eb2dd4976c896fb32d6287904d38ac26ce486e6eadaa3546c255ed140a7ed891',
        'root_final_scientific_adoption_sha256':'dd39c08a5816492b87e637917e7093859b5e6ea45cbfdddeb31da2755bbd95a8',
        'project_selected_paths':35,'QUEUE_selected_paths':1,'total_selected_paths':36,'unique_selected_blobs':len(unique),
        'main_project_previously_present':bool(main_project),'current_existing_unselected_project_entries':len(existing),
        'stale_local_checkout_not_used':True,'refresh_rule':'HOLD and recompute current main QUEUE/project conflicts/ancestors on any remote-main advance; never apply these dated ancestor hashes to a changed main.',
        'resumable_scope':'Frozen seven originals, PUBLICATION.md and six release plus21 science bytes are reusable subject to source/head/conflict checks; main QUEUE and ancestor trees require fresh rebase.',
        'action_authority':False,'Git_PR_Zenodo_DOI_Sheet_effects':0,'publication_ready_for_service_effects':False,
        'no_solution_DOI_in_pointer':True,'wait_for_other_integration_and_root_current_live_gates':True})
    print(json.dumps({'dated_main':main_commit,'selected_paths':len(manifest),'unique_blobs':len(unique),'project_tree':project_tree,'root_tree':root_tree,'computed_tree_count':len(computed),'preserved_siblings':preserved,'action_authority':False},indent=2),flush=True)


if __name__=='__main__':
    main()
