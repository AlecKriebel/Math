"""Standalone pure preparation custody. No project imports, network, subprocess or writes."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import sys

O = Path(__file__).resolve().parent
EXCLUDED = {'PREPARATION_MANIFEST.json', 'PREPARATION_SEAL.json', 'PREPARATION_CLOSURE.json'}
N = 0


def need(ok, label):
    global N
    N += 1
    if not ok:
        raise ValueError(label)


def read(path):
    need(path.is_file() and not path.is_symlink() and path.resolve() == path, 'real regular input')
    return path.read_bytes()


def digest(path):
    return hashlib.sha256(read(path)).hexdigest()


def obj(path):
    return json.loads(read(path))


def pinned(root, row):
    rel = PurePosixPath(row['path'])
    need(not rel.is_absolute() and '..' not in rel.parts and str(rel) == row['path'], 'safe exact payload path')
    path = root / rel
    body = read(path)
    need(len(body) == row['bytes'] and hashlib.sha256(body).hexdigest() == row['SHA256'], 'whole owned bytes')


def main():
    need(sys.argv[1:] in [[], ['--preseal']], 'bounded pure custody options')
    preseal = sys.argv[1:] == ['--preseal']
    manifest = obj(O / 'PREPARATION_MANIFEST.json')
    names = [r['path'] for r in manifest['files']]
    for row in manifest['files']:
        pinned(O, row)
    actual = {p.relative_to(O).as_posix() for p in O.rglob('*') if p.is_file()}
    need(len(names) == len(set(names)) and actual - EXCLUDED == set(names), 'whole preparation extent')
    need(not (O / 'run-state').exists(), 'preparation has not executed installation')
    need((O / 'hooks/pre-push').stat().st_mode & 0o7777 == 0o555, 'read-only executable guard')
    capture = obj(O / 'PREFLIGHT_CAPTURE.json')
    git = capture['Git']
    need(digest(O / 'private/shared-index.before') == git['index_SHA256']
         and digest(O / 'private/protected-index.raw-records') == git['protected_raw_records_SHA256'],
         'whole native index and all protected raw records')
    need(git['index_record_count'] - git['protected_record_count'] == 2, 'fresh index protects all except two existing aggregates')
    need(digest(O / 'private/staged-deletions.z') == capture['staged_deletions']['SHA256'], 'whole staged deletion list')
    for row in obj(O / 'REFERENCES.json')['files']:
        path = Path(row['path']); body = read(path)
        need(len(body) == row['bytes'] and hashlib.sha256(body).hexdigest() == row['SHA256'], 'unchanged reference body')
    template = obj(O / 'ROOT_ADOPTION_TEMPLATE.json')
    for key in ['root_stage_adopted', 'independent_code_audit_adopted',
                'complete_current_helper_and_rendered_output_adopted', 'production_install_authorized']:
        need(template[key] is False, 'template grants no authority')
    need(template['template_not_root_receipt'] is True and template['preparation_final_seal_SHA256'] is None,
         'false-authority template only')
    for name, value in template['code_files_SHA256'].items():
        need(digest(O / name) == value, 'exact full current code pin')
    need(obj(O / 'CONTROL_RESULTS.json')['status'] == 'PASS_STATIC_AND_MEMORY_ONLY_CONTROLS', 'bounded own controls')
    need(obj(O / 'PREFLIGHT_FINAL.json')['status'] == 'PASS_READ_ONLY_EXACT11_PREFLIGHT', 'actual final live read fences')
    for root_name, seal_hash, manifest_key, rows_key in [
        ('lefschetz-link-private-stage-sol-20261115',
         'b42073395a01c7a60c733627212df7d56f484023662119a215a8b6cb57b89575', 'owned_manifest_SHA256', 'files'),
        ('lefschetz-link-independent-code-audit-sol-20261115',
         'afe06ee13def341fe2798f25aee2ad971477a442ad6320357f2b3cf2dafa1ed0', 'manifest', 'payloads')]:
        root = O.parent / root_name
        need(digest(root / 'FINAL_SEAL.json') == seal_hash, 'actual immutable current writer/audit seal')
        seal = obj(root / 'FINAL_SEAL.json'); expected = seal[manifest_key]
        need(digest(root / 'OWNED_MANIFEST.json') == (expected['SHA256'] if isinstance(expected, dict) else expected),
             'current packet manifest seal')
        values = obj(root / 'OWNED_MANIFEST.json')[rows_key]
        rows = [dict(row, path=name) for name, row in values.items()] if isinstance(values, dict) else values
        actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
        need(actual == {r['path'] for r in rows} | {'OWNED_MANIFEST.json', 'FINAL_SEAL.json'}, 'whole current packet extent')
        for row in rows:
            pinned(root, row)
    if not preseal:
        seal = obj(O / 'PREPARATION_SEAL.json')
        need(digest(O / 'PREPARATION_MANIFEST.json') == seal['MANIFEST_SHA256']
             and digest(O / 'PREPARATION_CLOSURE.json') == seal['CLOSURE_SHA256'], 'final preparation seal')
        need(seal['owned_payload_count'] == len(names), 'final complete payload extent')
    print(json.dumps({'status': 'PREPARATION_CUSTODY_PASS', 'mode': 'preseal' if preseal else 'final',
                      'checks': N, 'owned_payload_count': len(names),
                      'protected_index_records': git['protected_record_count'],
                      'current_stage_or_audit_root_adopted': False, 'installation_or_push_executed': False,
                      'project_imports_network_subprocess_science_or_writes': False}, sort_keys=True))


if __name__ == '__main__':
    main()
