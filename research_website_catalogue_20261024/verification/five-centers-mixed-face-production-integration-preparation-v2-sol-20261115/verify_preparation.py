"""Pure closed preparation custody. Standard library only; no project imports or writes.
Default stays inside this immutable packet. --runtime additionally checks the explicit
separate finite durable runtime; it never queries current website/Git/source state.
"""
from pathlib import Path, PurePosixPath
import hashlib
import json
import os
import re
import stat
import sys

O = Path(__file__).resolve().parent
EXCLUDED = {'PREPARATION_MANIFEST.json', 'PREPARATION_SEAL.json', 'PREPARATION_CLOSURE.json'}
LIVE_AUTHORIZED = False
CHECKS = 0

def need(ok, label):
    global CHECKS
    CHECKS += 1
    if not ok:
        raise RuntimeError(label)

def read(path):
    path = Path(path)
    runtime = Path(str(O) + '-runtime')
    need(path == O or O in path.parents or runtime in path.parents, 'only immutable packet or explicit runtime')
    need(stat.S_ISREG(path.lstat().st_mode) and path.resolve() == path, 'ordinary real file')
    return path.read_bytes()

def sha(body):
    return hashlib.sha256(body).hexdigest()

def obj(path):
    return json.loads(read(path))

def pin(path, row):
    body = read(path)
    need(len(body) == row['bytes'] and sha(body) == row['SHA256'], 'whole-byte custody')
    return body

def safe_rel(text):
    path = PurePosixPath(text)
    need(path.parts and not path.is_absolute() and '..' not in path.parts
         and str(path) == text and '\\' not in text, 'exact safe relative path')
    return path

def live_path(path):
    return '.git' in path.parts

def extent(root):
    root = Path(root)
    need(LIVE_AUTHORIZED or not live_path(root), 'source-only: no live namespace inspection')
    need(stat.S_ISDIR(root.lstat().st_mode) and root.resolve() == root, 'ordinary real directory root')
    files, directories = [], []
    def walk(directory):
        with os.scandir(directory) as entries:
            for entry in entries:
                path = Path(entry.path)
                mode = entry.stat(follow_symlinks=False).st_mode
                relative = path.relative_to(root).as_posix()
                if stat.S_ISDIR(mode):
                    directories.append(relative)
                    walk(path)
                else:
                    need(stat.S_ISREG(mode), 'reject symlink or special namespace entry: ' + relative)
                    files.append(relative)
    walk(root)
    return sorted(files), sorted(directories)


def closed_namespace(root, files, directories, terminals=()):
    actual_files, actual_directories = extent(root)
    need(len(files) == len(set(files)) and actual_files == sorted(set(files) | set(terminals)),
         'exact ordinary file extent and exact root terminals only')
    need(directories == sorted(set(directories)) and actual_directories == directories,
         'exact declared directory extent, including legitimate empty directories')
    return actual_files, actual_directories


def runtime_custody(root, preparation_sha, contract_body, held):
    """Pure finite durable-state custody; no authority or live-state observation."""
    contract = json.loads(contract_body)
    need(str(root) == contract['runtime_root'], 'one explicitly named separate runtime')
    try:
        root.lstat()
    except FileNotFoundError:
        return {'phase': 'ABSENT', 'live_state_reverified': False}
    files, directories = extent(root)
    state = obj(root / 'STATE.json')
    need(set(state) == {'schema', 'phase', 'preparation_final_seal_SHA256', 'runtime_contract_SHA256',
                       'root_adoption_SHA256', 'root_commit_approval_SHA256', 'files', 'directories'},
         'exact runtime state fields')
    need(state['schema'] == 'exact11-durable-runtime-state-v1'
         and state['preparation_final_seal_SHA256'] == preparation_sha
         and state['runtime_contract_SHA256'] == sha(contract_body), 'runtime bound to this whole preparation')
    phase = state['phase']
    need(phase in contract['phases'], 'finite durable runtime phase')
    permitted = contract['phases'][phase]
    need(set(state['files']) == set(permitted['files'])
         and files == sorted(permitted['files'] + ['STATE.json'])
         and directories == state['directories'] == permitted['directories'], 'exact finite runtime extent')
    bodies = {}
    for name, row in state['files'].items():
        need(set(row) == {'bytes', 'SHA256'}, 'exact runtime content descriptor')
        bodies[name] = pin(root / safe_rel(name), row)
    adoption = json.loads(bodies['ROOT_ADOPTION.json'])
    need(adoption.get('schema') == 'root_five_centers_mixed_face_exact11_production_adoption_v1'
         and adoption.get('authority') == 'root' and adoption.get('template_not_root_receipt') is False
         and all(adoption.get(k) is True for k in ['root_stage_adopted', 'independent_code_audit_adopted',
                 'complete_current_helper_and_rendered_output_adopted', 'production_install_authorized'])
         and adoption['preparation_final_seal_SHA256'] == preparation_sha
         and adoption['root_stage_reading_SHA256'] == contract['root_stage_reading_SHA256']
         and adoption['runtime_root'] == str(root) and adoption['runtime_contract_SHA256'] == sha(contract_body)
         and sha(bodies['ROOT_ADOPTION.json']) == state['root_adoption_SHA256'], 'bound actual root receipt copy')
    pre = json.loads(bodies['PRE_INSTALL.json'])
    need(pre['root_adoption_SHA256'] == state['root_adoption_SHA256']
         and pre['actual_parent'] == contract['parent']
         and ['public/' + row['path'] for row in pre['exact11']] == contract['gitpaths'], 'bound pre-install receipt')
    if phase != 'PUBLISHED':
        need(state['root_commit_approval_SHA256'] is None, 'no premature publication authority')
    if phase in ['INSTALLED', 'PUBLISHED']:
        pending = json.loads(bodies['PENDING_COMMIT.json'])
        need(pending['root_adoption_SHA256'] == state['root_adoption_SHA256']
             and pending['parent'] == contract['parent'] and pending['gitpaths'] == contract['gitpaths']
             and pending['public_counts'] == [623, 94, 95]
             and pending['shared_index_SHA256_unchanged'] == held['Git']['index_SHA256']
             and pending['protected_raw_records_SHA256'] == held['Git']['protected_raw_records_SHA256']
             and pending['temporary_index_SHA256'] == sha(bodies['commit.index']), 'bound pending commit and temporary index')
        need(all(re.fullmatch('[0-9a-f]{40}', pending[k]) for k in ['commit', 'tree']), 'bounded commit identifiers')
    if phase == 'PUBLISHED':
        approval = json.loads(bodies['ROOT_COMMIT_APPROVAL.json'])
        need(approval['schema'] == 'root_five_centers_mixed_face_exact11_commit_approval_v1'
             and sha(bodies['ROOT_COMMIT_APPROVAL.json']) == state['root_commit_approval_SHA256']
             and approval['authority'] == 'root' and approval['publication_authorized'] is True
             and approval['root_adoption_SHA256'] == state['root_adoption_SHA256']
             and approval['pending_commit_receipt_SHA256'] == sha(bodies['PENDING_COMMIT.json']), 'bound separate commit approval copy')
        for key in ['parent', 'commit', 'tree', 'gitpaths', 'protected_raw_records_SHA256']:
            need(approval[key] == pending[key], 'durable checked commit field: ' + key)
        prepub = json.loads(bodies['PRE_PUBLICATION.json'])
        need(prepub['root_adoption_SHA256'] == state['root_adoption_SHA256']
             and prepub['root_commit_approval_SHA256'] == state['root_commit_approval_SHA256']
             and prepub['old_index_SHA256'] == held['Git']['index_SHA256']
             and prepub['approved_index_SHA256'] == sha(bodies['shared-index.approved'])
             and prepub['commit'] == pending['commit'], 'bound validated publication buffer')
        publication = json.loads(bodies['PUBLICATION.json'])
        need(all(publication[k] == pending[k] for k in ['parent', 'commit', 'tree', 'gitpaths'])
             and publication['counts'] == [623, 94, 95]
             and publication['protected_raw_records_SHA256'] == pending['protected_raw_records_SHA256'],
             'bound durable publication receipt, not fresh live verification')
    return {'phase': phase, 'files': len(files), 'directories': len(directories), 'live_state_reverified': False}


def main():
    need(sys.argv[1:] in [[], ['--preseal'], ['--runtime']], 'bounded pure options')
    preseal = sys.argv[1:] == ['--preseal']
    manifest_body = read(O / 'PREPARATION_MANIFEST.json')
    manifest = json.loads(manifest_body)
    paths = [row['path'] for row in manifest['files']]
    terminals = EXCLUDED if not preseal else {n for n in EXCLUDED if (O / n).exists()}
    files, directories = closed_namespace(O, paths, manifest['directories'], terminals)
    for row in manifest['files']:
        pin(O / safe_rel(row['path']), row)
    references = obj(O / 'REFERENCE_BINDINGS.json')['files']
    need(len(references) == 84, 'all original literal reference descriptors retained')
    for row in references:
        if 'copy' in row:
            pin(O / row['copy'], row)
    need(sha(read(O / 'REFERENCE_BINDINGS.json')) ==
         '8e53208ab8512ef0a25a8d48adf79d90f8b538b8987167bdd0ba631ba339ea09',
         'original84 typed/order/null/absent/history metadata unchanged; descriptors not followed')
    baseline = obj(O / 'HELD_BASELINE_CONTRACT.json')
    need(sha(read(O / 'HELD_BASELINE_CONTRACT.json')) ==
         '69c657c03f3cb70290eab73db966b39296f07fb58afa6c9c2fbed62242259ab2'
         and sha(read(O / 'private/retained-approved-index')) == baseline['Git']['index_SHA256'],
         'whole held original contract and native index')
    template = obj(O / 'ROOT_ADOPTION_TEMPLATE.json')
    for key in ['root_stage_adopted', 'independent_code_audit_adopted',
                'complete_current_helper_and_rendered_output_adopted', 'production_install_authorized']:
        need(template[key] is False, 'false-authority future template')
    need(template['template_not_root_receipt'] is True and template['preparation_final_seal_SHA256'] is None,
         'no invented actual root receipt')
    for name, digest in template['code_files_SHA256'].items():
        need(sha(read(O / safe_rel(name))) == digest, 'whole current body pin')
    need((O / 'hooks/pre-push').lstat().st_mode & 0o7777 == 0o555, 'read-only executable hook')
    runtime = {'phase': 'NOT_INSPECTED', 'live_state_reverified': False}
    if not preseal:
        seal_bytes = read(O / 'PREPARATION_SEAL.json')
        seal = json.loads(seal_bytes)
        need(sha(manifest_body) == seal['MANIFEST_SHA256']
             and sha(read(O / 'PREPARATION_CLOSURE.json')) == seal['CLOSURE_SHA256'], 'whole immutable final controls')
        need(len(paths) == seal['owned_payload_count'] and directories == seal['owned_directories'], 'sealed full extent')
        if sys.argv[1:] == ['--runtime']:
            runtime = runtime_custody(Path(str(O) + '-runtime'), sha(seal_bytes),
                                      read(O / 'RUNTIME_CONTRACT.json'), baseline)
    print(json.dumps({'status': 'PASS_SOURCE_ONLY_V2_CLOSED_PREPARATION_CUSTODY',
                      'mode': 'preseal' if preseal else 'final', 'checks': CHECKS,
                      'owned_payload_count': len(paths), 'owned_directories': directories,
                      'historical_reference_descriptors_followed': False, 'runtime': runtime,
                      'website_dot_git_source_network_subprocess_project_imports_science_writes': False,
                      'production_installation_or_publication_authority': False}, sort_keys=True))

if __name__ == '__main__':
    main()
