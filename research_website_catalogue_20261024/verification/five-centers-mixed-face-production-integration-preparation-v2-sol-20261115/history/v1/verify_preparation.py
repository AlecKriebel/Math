"""Pure source-only custody. No project imports, live paths, network, subprocess or writes."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import sys

O = Path(__file__).resolve().parent
P = O.parent.parent
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
EXCLUDED = {'PREPARATION_MANIFEST.json', 'PREPARATION_SEAL.json', 'PREPARATION_CLOSURE.json'}
CHECKS = 0


def need(ok, label):
    global CHECKS
    CHECKS += 1
    if not ok:
        raise ValueError(label)


def read(path):
    need(path != W and W not in path.parents and '.git' not in path.parts, 'source-only, never a live descriptor')
    need(not path.is_symlink() and path.is_file() and path.resolve() == path, 'real regular held input')
    return path.read_bytes()


def sha(body):
    return hashlib.sha256(body).hexdigest()


def obj(path):
    return json.loads(read(path))


def pin(path, row):
    body = read(path)
    need(len(body) == row['bytes'] and sha(body) == row['SHA256'], 'whole source-only input')
    return body


def names(root):
    entries = list(root.rglob('*'))
    need(not any(p.is_symlink() for p in entries), 'no held namespace symlinks')
    return {p.relative_to(root).as_posix() for p in entries if p.is_file()}


def main():
    need(sys.argv[1:] in [[], ['--preseal']], 'bounded pure option')
    preseal = sys.argv[1:] == ['--preseal']
    manifest = obj(O / 'PREPARATION_MANIFEST.json')
    paths = []
    for row in manifest['files']:
        rel = PurePosixPath(row['path'])
        need(not rel.is_absolute() and '..' not in rel.parts, 'safe owned path')
        pin(O / str(rel), row); paths.append(row['path'])
    need(len(paths) == len(set(paths)) and names(O) - EXCLUDED == set(paths), 'complete preparation extent')
    need(not (O / 'run-state').exists(), 'no installer runtime has occurred')
    for row in obj(O / 'REFERENCE_BINDINGS.json')['files']:
        body = pin(Path(row['path']), row)
        if 'copy' in row:
            need(body == read(O / row['copy']), 'whole copied original without normalization')
    source_seals = [
        ('five-centers-mixed-face-private-stage-sol-20261115',
         '1fb0b5d399d013a729e3d709e18581e011d1643f88e1622f63dd62d2169cd24f'),
        ('five-centers-mixed-face-independent-code-audit-sol-20261115',
         'c80ea0ca5c4aca8137ecf1bffca4c8effad7ddd81489c1c0153e6b150580f4ec')]
    for kind, (directory, expected) in enumerate(source_seals):
        root = O.parent / directory
        seal_bytes = read(root / 'FINAL_SEAL.json')
        need(sha(seal_bytes) == expected, 'same authenticated actual seal bytes')
        seal = json.loads(seal_bytes)
        if kind == 0:
            data = json.loads(pin(root / 'OWNED_MANIFEST.json', seal['manifest']))
            rows = [(str(root / name), row) for name, row in data['payloads'].items()]
            excluded = {'OWNED_MANIFEST.json', 'FINAL_SEAL.json'}
        else:
            data = json.loads(pin(root / 'FINAL_MANIFEST.json', seal['bindings']['FINAL_MANIFEST.json']))
            rows = [(row['path'], row) for row in data['files']]
            excluded = {'FINAL_MANIFEST.json', 'FINAL_SEAL.json', 'FINAL_CLOSURE.json'}
            pin(root / 'FINAL_CLOSURE.json', seal['bindings']['FINAL_CLOSURE.json'])
        need(names(root) == {Path(path).relative_to(root).as_posix() for path, row in rows} | excluded,
             'exact current writer/audit interfaces and full history extent')
        for path, row in rows:
            pin(Path(path), row)
    template = obj(O / 'ROOT_ADOPTION_TEMPLATE.json')
    for key in ['root_stage_adopted', 'independent_code_audit_adopted',
                'complete_current_helper_and_rendered_output_adopted', 'production_install_authorized']:
        need(template[key] is False, 'future template grants no actual authority')
    need(template['template_not_root_receipt'] is True and template['preparation_final_seal_SHA256'] is None,
         'never a self-created root receipt')
    for path, value in template['code_files_SHA256'].items():
        need(sha(read(O / path)) == value, 'whole current body pin')
    contract = obj(O / 'HELD_BASELINE_CONTRACT.json')
    need(contract['source_data_only'] is True and contract['current_live_website_dot_git_or_remote_requeried_by_preparation'] is False,
         'held-data observation not a fresh live scan')
    need(sha(read(O / 'private/retained-approved-index')) == contract['Git']['index_SHA256']
         and contract['Git']['index_record_count'] == 58554
         and contract['Git']['protected_record_count'] == 58552, 'new-scope held whole native index buffer')
    need(obj(O / 'SOURCE_ONLY_PREFLIGHT.json')['status'] == 'PASS_SOURCE_ONLY_HELD_PREFLIGHT', 'actual new read-only closure')
    need(obj(O / 'CONTROL_RESULTS.json')['status'] == 'PASS_NEW_BOUNDED_SOURCE_ADAPTER_AND_TOY_CONTROLS', 'necessary new bounded fixtures')
    need((O / 'hooks/pre-push').stat().st_mode & 0o7777 == 0o555, 'prepared read-only executable hook')
    if not preseal:
        seal = obj(O / 'PREPARATION_SEAL.json')
        need(sha(read(O / 'PREPARATION_MANIFEST.json')) == seal['MANIFEST_SHA256']
             and sha(read(O / 'PREPARATION_CLOSURE.json')) == seal['CLOSURE_SHA256'], 'final immutable preparation')
        need(seal['owned_payload_count'] == len(paths), 'complete final extent')
    print(json.dumps({'status': 'PASS_SOURCE_ONLY_PREPARATION_CUSTODY', 'mode': 'preseal' if preseal else 'final',
                      'checks': CHECKS, 'owned_payload_count': len(paths), 'held_protected_native_records': 58552,
                      'website_or_dot_git_access': False, 'project_imports_network_subprocess_science_or_writes': False,
                      'installation_or_publication_authority': False}, sort_keys=True))


if __name__ == '__main__':
    main()
