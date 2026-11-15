"""New namespace/runtime fixtures only; extracted current pure definitions, no installer/Git."""
import sys
sys.dont_write_bytecode = True
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import tempfile

O = Path(__file__).resolve().parent


def require(ok, why):
    if not ok:
        raise RuntimeError(why)


def denied(action):
    try:
        action()
    except RuntimeError:
        return
    raise RuntimeError('required rejection missing')


def functions(name, root):
    tree = ast.parse((O / name).read_bytes())
    selected = {'need', 'sha', 'read', 'obj', 'pin', 'safe_rel', 'extent', 'live_path',
                'closed_namespace', 'runtime_custody', 'sealed_namespace'}
    definitions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in selected]
    env = dict(Path=Path, PurePosixPath=__import__('pathlib').PurePosixPath, hashlib=hashlib,
               json=json, os=os, re=re, stat=stat, O=root, W=Path('/unread/toy-live'),
               LIVE_AUTHORIZED=False, CHECKS=0)
    exec(compile(ast.Module(body=definitions, type_ignores=[]), '<own-current-selected-definitions>', 'exec'), env)
    return env


def put(root, name, value):
    body = value if isinstance(value, bytes) else json.dumps(value, sort_keys=True).encode()
    (root / name).write_bytes(body)
    return body


def state(root, phase, contract, prep, approval=None):
    names = contract['phases'][phase]['files']
    descriptors = {}
    for name in names:
        body = (root / name).read_bytes()
        descriptors[name] = {'bytes': len(body), 'SHA256': hashlib.sha256(body).hexdigest()}
    return {'schema': 'exact11-durable-runtime-state-v1', 'phase': phase,
            'preparation_final_seal_SHA256': prep,
            'runtime_contract_SHA256': hashlib.sha256(json.dumps(contract, sort_keys=True).encode()).hexdigest(),
            'root_adoption_SHA256': hashlib.sha256((root / 'ROOT_ADOPTION.json').read_bytes()).hexdigest(),
            'root_commit_approval_SHA256': approval, 'files': descriptors, 'directories': []}


def runtime_cases(env, root):
    contract = json.loads((O / 'RUNTIME_CONTRACT.json').read_bytes())
    contract['runtime_root'] = str(root)
    body = json.dumps(contract, sort_keys=True).encode()
    prep = 'b' * 64
    held = json.loads((O / 'HELD_BASELINE_CONTRACT.json').read_bytes())
    adoption = {'schema': 'root_five_centers_mixed_face_exact11_production_adoption_v1',
                'authority': 'root', 'template_not_root_receipt': False,
                'root_stage_adopted': True, 'independent_code_audit_adopted': True,
                'complete_current_helper_and_rendered_output_adopted': True,
                'production_install_authorized': True, 'preparation_final_seal_SHA256': prep,
                'root_stage_reading_SHA256': contract['root_stage_reading_SHA256'],
                'runtime_root': str(root), 'runtime_contract_SHA256': hashlib.sha256(body).hexdigest()}
    # This is explicitly owned toy data; it is never a fixed real root authority receipt.
    root.mkdir()
    adoption_body = put(root, 'ROOT_ADOPTION.json', adoption)
    adoption_sha = hashlib.sha256(adoption_body).hexdigest()
    put(root, 'PRE_INSTALL.json', {'root_adoption_SHA256': adoption_sha, 'actual_parent': contract['parent'],
        'exact11': [{'path': p.removeprefix('public/')} for p in contract['gitpaths']]})
    check = lambda: env['runtime_custody'](root, prep, body, held)
    put(root, 'STATE.json', state(root, 'INSTALL_STARTED', contract, prep))
    require(check()['phase'] == 'INSTALL_STARTED', 'valid finite started checkpoint')
    put(root, 'commit.index', b'owned toy index, no Git or index parser execution')
    pending = {'root_adoption_SHA256': adoption_sha, 'parent': contract['parent'],
               'commit': 'a' * 40, 'tree': 'c' * 40, 'gitpaths': contract['gitpaths'],
               'public_counts': [623, 94, 95], 'shared_index_SHA256_unchanged': held['Git']['index_SHA256'],
               'protected_raw_records_SHA256': held['Git']['protected_raw_records_SHA256'],
               'temporary_index_SHA256': hashlib.sha256((root / 'commit.index').read_bytes()).hexdigest()}
    pending_body = put(root, 'PENDING_COMMIT.json', pending)
    denied(check)  # Partial next-phase extent cannot inherit the earlier phase's success.
    put(root, 'STATE.json', state(root, 'INSTALLED', contract, prep))
    require(check()['phase'] == 'INSTALLED', 'valid installed durable checkpoint')
    (root / 'unlisted-empty').mkdir(); denied(check); (root / 'unlisted-empty').rmdir()
    put(root, 'anonymous-future-payload', b'unsealed'); denied(check); (root / 'anonymous-future-payload').unlink()
    original = (root / 'commit.index').read_bytes()
    put(root, 'commit.index', b'changed'); denied(check); put(root, 'commit.index', original)
    s = state(root, 'INSTALLED', contract, prep); s['phase'] = 'UNDECLARED'; put(root, 'STATE.json', s); denied(check)
    put(root, 'STATE.json', state(root, 'INSTALLED', contract, prep))
    os.mkfifo(root / 'fifo'); denied(check); (root / 'fifo').unlink()
    (root / 'link').symlink_to(root / 'commit.index'); denied(check); (root / 'link').unlink()
    approval = {'schema': 'root_five_centers_mixed_face_exact11_commit_approval_v1',
                'authority': 'root', 'publication_authorized': True, 'root_adoption_SHA256': adoption_sha,
                'pending_commit_receipt_SHA256': hashlib.sha256(pending_body).hexdigest(),
                **{k: pending[k] for k in ['parent', 'commit', 'tree', 'gitpaths', 'protected_raw_records_SHA256']}}
    approval_sha = hashlib.sha256(put(root, 'ROOT_COMMIT_APPROVAL.json', approval)).hexdigest()
    approved = put(root, 'shared-index.approved', b'owned toy approved raw bytes')
    put(root, 'PRE_PUBLICATION.json', {'root_adoption_SHA256': adoption_sha,
        'root_commit_approval_SHA256': approval_sha, 'old_index_SHA256': held['Git']['index_SHA256'],
        'approved_index_SHA256': hashlib.sha256(approved).hexdigest(), 'commit': pending['commit']})
    put(root, 'PUSH.stdout', b'owned toy stdout, never an actual push')
    put(root, 'PUBLICATION.json', {**{k: pending[k] for k in ['parent', 'commit', 'tree', 'gitpaths', 'protected_raw_records_SHA256']},
                                  'counts': [623, 94, 95]})
    put(root, 'STATE.json', state(root, 'PUBLISHED', contract, prep, approval_sha))
    require(check()['phase'] == 'PUBLISHED', 'valid post-publication pure custody without live reads')
    approval['commit'] = 'd' * 40
    bad_body = put(root, 'ROOT_COMMIT_APPROVAL.json', approval)
    put(root, 'STATE.json', state(root, 'PUBLISHED', contract, prep, hashlib.sha256(bad_body).hexdigest()))
    denied(check)  # Rehashing a mismatched receipt cannot bless a different approved commit.
    return {'valid_phases': ['INSTALL_STARTED', 'INSTALLED', 'PUBLISHED'],
            'rejected': ['partial-next-phase', 'unlisted-empty-directory', 'anonymous-file', 'changed-buffer',
                         'unknown-phase', 'FIFO', 'symlink', 'rehashed-mismatched-approval']}


def audit_namespace_case(env, root):
    packet = root / 'toy-audit'; packet.mkdir(); (packet / 'inputs').mkdir()
    files = []
    for i in range(721):
        name = 'payload%03d' % i
        put(packet, name, b'x')
        files.append({'path': str(packet / name), 'bytes': 1, 'SHA256': hashlib.sha256(b'x').hexdigest()})
    manifest = put(packet, 'FINAL_MANIFEST.json', {'files': files})
    closure = put(packet, 'FINAL_CLOSURE.json', b'own toy closure')
    descriptor = lambda b: {'bytes': len(b), 'SHA256': hashlib.sha256(b).hexdigest()}
    seal = put(packet, 'FINAL_SEAL.json', {'own_final_owned_payloads': 721,
        'bindings': {'FINAL_MANIFEST.json': descriptor(manifest), 'FINAL_CLOSURE.json': descriptor(closure)}})
    put(root, 'SEALED_NAMESPACE_CONTRACT.json', {'audit_directories': ['inputs']})
    env.update(A=packet, AUDIT_SEAL=hashlib.sha256(seal).hexdigest())
    env['sealed_namespace']('audit')
    (packet / 'extra-empty').mkdir(); denied(lambda: env['sealed_namespace']('audit')); (packet / 'extra-empty').rmdir()
    os.mkfifo(packet / 'fifo'); denied(lambda: env['sealed_namespace']('audit')); (packet / 'fifo').unlink()
    return {'audit_actual_function_721_toy_payloads': True, 'declared_empty_inputs_preserved': True,
            'unlisted_empty_directory_and_FIFO_rejected': True}


def main():
    results = []
    with tempfile.TemporaryDirectory(prefix='v2-custody-fixture-', dir=O / 'private') as directory:
        parent = Path(directory)
        for name in ['exact11_lib.py', 'verify_preparation.py']:
            root = parent / name.removesuffix('.py'); root.mkdir()
            env = functions(name, root)
            packet = root / 'packet'; packet.mkdir(); (packet / 'inputs').mkdir(); put(packet, 'body', b'x')
            check = lambda: env['closed_namespace'](packet, ['body'], ['inputs'])
            check()
            (packet / 'extra').mkdir(); denied(check); (packet / 'extra').rmdir()
            os.mkfifo(packet / 'fifo'); denied(check); (packet / 'fifo').unlink()
            (packet / 'link').symlink_to(packet / 'body'); denied(check); (packet / 'link').unlink()
            put(packet, 'PREPARATION_SEAL.json', b'nested terminal name is not excluded'); denied(check)
            (packet / 'PREPARATION_SEAL.json').unlink()
            # Standalone path scope is this toy root; all fixtures stay within the new private child.
            runtime = root / 'run'; result = runtime_cases(env, runtime)
            item = {'body': name, 'closed_namespace_positive_and4_negative_cases': True, 'runtime': result}
            if name == 'exact11_lib.py':
                item['audit_namespace'] = audit_namespace_case(env, root)
            results.append(item)
    print(json.dumps({'status': 'PASS_NEW_V2_NAMESPACE_AND_FINITE_RUNTIME_CONTROLS', 'results': results,
                      'only_new_private_toy_writes': True, 'installer_Git_science_renderer_upstream_campaigns': False}, indent=2))

if __name__ == '__main__':
    main()
