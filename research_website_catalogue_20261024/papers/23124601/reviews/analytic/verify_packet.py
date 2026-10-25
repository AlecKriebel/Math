"""Read-only custody verifier, with optional in-memory replay of OWN certificates.

Normal invocation requires the final MANIFEST/SEAL. --preseal checks the inputs
before those final objects exist. No archive/source programme is executed.
All invariants use explicit exceptions and remain active under python -O.
"""
from pathlib import Path
from collections import Counter
import argparse, contextlib, copy, datetime, hashlib, io, json, re, runpy, sys

E = Path(__file__).resolve().parent
P = E.parents[3]
S = P / 'papers/23124601/sources'
HEX = re.compile(r'^[0-9a-f]{64}$')


def need(value, reason):
    if not value:
        raise RuntimeError(reason)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def obj(path):
    return json.loads(path.read_text())


def checked(row, base=None):
    need(type(row) is dict, 'binding_object')
    need(type(row.get('path')) is str, 'binding_path')
    need(type(row.get('bytes')) is int and row['bytes'] >= 0, 'binding_bytes')
    need(type(row.get('sha256')) is str and HEX.fullmatch(row['sha256']), 'binding_sha256_schema')
    path = Path(row['path'])
    if base is not None:
        need(not path.is_absolute() and '..' not in path.parts, 'owned_relative_path')
        path = base / path
    else:
        need(path.is_absolute(), 'original_absolute_path')
    need(path.is_file() and not path.is_symlink(), 'binding_regular_file:' + str(path))
    need(path.stat().st_size == row['bytes'], 'binding_size:' + str(path))
    need(sha(path) == row['sha256'], 'binding_hash:' + str(path))
    return path


def table(rows, base=None):
    need(type(rows) is list and rows, 'nonempty_binding_list')
    paths = [checked(row, base) for row in rows]
    need(len(set(map(str, paths))) == len(paths), 'unique_binding_paths')
    return len(paths)


def normalized(value):
    value = copy.deepcopy(value)
    if type(value) is dict:
        value.pop('utc', None)
        value.pop('elapsed_seconds', None)
    return value


def replay_owned(script, outputs):
    """Capture every expected Path.write_text; prohibit all other writes.

    The three owned scripts were inspected in full and use no other mutation
    interface. The originals and existing positive receipts remain unchanged.
    """
    writes = {}
    original_write = Path.write_text
    original_argv = sys.argv[:]
    allowed = {(E / name).resolve() for name in outputs}

    def capture(path, data, *args, **kwargs):
        path = path.resolve()
        need(path in allowed, 'unexpected_owned_replay_output:' + str(path))
        need(type(data) is str, 'owned_replay_text')
        need(path not in writes, 'duplicate_owned_replay_output')
        writes[path] = data.encode(kwargs.get('encoding') or 'utf-8')
        return len(data)

    try:
        Path.write_text = capture
        sys.argv = [str(E / script)]
        with contextlib.redirect_stdout(io.StringIO()):
            runpy.run_path(str(E / script), run_name='__main__')
    finally:
        sys.argv = original_argv
        Path.write_text = original_write
    need(set(writes) == allowed, 'all_owned_replay_outputs_captured')
    for path, data in writes.items():
        if path.name == 'walk20-full-independent.json':
            need(data == path.read_bytes(), 'all810literal_records_reproduced')
        else:
            need(normalized(json.loads(data)) == normalized(obj(path)), 'owned_result_reproduced:' + path.name)
    return {'script': script, 'expected_outputs_captured_in_memory': len(writes), 'status': 'PASS'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--preseal', action='store_true')
    ap.add_argument('--rerun-owned', action='store_true')
    ap.add_argument('--self-control', action='store_true')
    args = ap.parse_args()
    need((E / '.gitignore').read_text() == 'cache/\n', 'ignored_private_cache')
    pinned = {
        S / 'SOURCE_READY.json': '7fd29ea48957c098973ca892a317269b9e2c4fc3b616c252e2dfa8f09a69dbb1',
        S / 'SOURCE_READY_MANIFEST.json': '70e8f139bf0ab0d237558ad79138a023f0a19d4d620533d08f6a82b34686b522',
        S / 'SOURCE_READY_SEAL.json': '14d5c25d8024471d6b06504082329ebc3a90927c6fcb9b3c144f35ce889c29c0',
        E / 'EARLY_SEAL.json': '3a9837ca70883b252772d4b7454598ab84de5492122ad56cc6be4c7de872eb6c',
    }
    for path, expected in pinned.items():
        need(sha(path) == expected, 'independent_original_pin:' + str(path))
    early = obj(E / 'EARLY_SEAL.json')
    need(sha(E / 'EARLY_MANIFEST.json') == early['manifest_sha256'], 'early_manifest_seal')
    need(sha(E / 'EARLY_RECONSTRUCTION.md') == early['notes_sha256'], 'early_notes_seal')
    early_count = table(obj(E / 'EARLY_MANIFEST.json')['files'])
    ready_count = table(obj(S / 'SOURCE_READY_MANIFEST.json')['files'], S)
    need(ready_count == 76, 'exact_source_ready_count')
    originals = obj(E / 'ORIGINAL_BINDINGS.json')
    original_count = table(originals['files'])
    need(dict(Counter(r['kind'] for r in originals['files'])) == originals['counts_by_kind'], 'original_kind_counts')
    cache_count = table(obj(E / 'CACHE_MANIFEST.json')['files'], E)
    owned_count = None
    if not args.preseal:
        seal = obj(E / 'SEAL.json')
        need(sha(E / 'MANIFEST.json') == seal['manifest_sha256'], 'final_manifest_seal')
        need(sha(E / 'REPORT.md') == seal['report_sha256'], 'final_report_seal')
        need(sha(E / 'VERDICT.json') == seal['verdict_sha256'], 'final_verdict_seal')
        mf = obj(E / 'MANIFEST.json')
        owned_count = table(mf['files'], E)
        need(owned_count == mf['owned_bindings'] == seal['owned_bindings'], 'owned_final_count')
        actual = {str(p.relative_to(E)) for p in E.rglob('*') if p.is_file() and 'cache' not in p.relative_to(E).parts and p.name not in ('MANIFEST.json', 'SEAL.json')}
        need(actual == {r['path'] for r in mf['files']}, 'complete_owned_inventory')
        need(original_count == seal['original_bindings'] and cache_count == seal['cache_bindings'], 'seal_original_cache_counts')
    # Confirm every actual source-ready original is bound by the new ledger.
    original_paths = {r['path'] for r in originals['files']}
    for r in obj(S / 'SOURCE_READY_MANIFEST.json')['files']:
        need(str(S / r['path']) in original_paths, 'source_ready_in_full_binding_map')
    expected_status = 'VERIFIED_ORIGINAL_FIXED_GENERATOR_CLASSIFICATION_WITH_CLASSICAL_IMPORTS_AND_EXPLICIT_RUNTIME_LIMITS'
    need(obj(E / 'VERDICT.json')['verdict'] == expected_status, 'literal_custom_verdict')
    need(not obj(E / 'VERDICT.json')['publication_or_page_authority'], 'no_publication_authority')
    for name in ['SMALL_CERTIFICATES.json', 'CROSSING_DAG_CERTIFICATE.json', 'RELATION_CALIBRATIONS.json', 'DAG_FAULT_CONTROLS.json', 'DAG_FAULT_CONTROLS_OPTIMIZED.json']:
        need(obj(E / name)['status'] == 'PASS', 'positive_receipt:' + name)
    for name in ['COMPILE_RECEIPT.json', 'COMPILE_RECEIPT_GCC.json']:
        need(obj(E / name)['exit_code'] != 0 and obj(E / name)['binary_sha256'] is None, 'honest_failed_compilation')
    self_control = None
    if args.self_control:
        bad = copy.deepcopy(originals['files'][0])
        bad['sha256'] = '0' * 64 if bad['sha256'] != '0' * 64 else '1' * 64
        try:
            checked(bad)
        except RuntimeError as exc:
            need(str(exc).startswith('binding_hash:'), 'correct_hash_control_rejection')
            self_control = {'status': 'PASS', 'in_memory_wrong_original_hash_rejected': True}
        else:
            raise RuntimeError('wrong_hash_was_accepted')
    reruns = []
    if args.rerun_owned:
        reruns.append(replay_owned('check_small.py', ['SMALL_CERTIFICATES.json', 'cache/walk20-full-independent.json']))
        reruns.append(replay_owned('check_crossing_dag.py', ['CROSSING_DAG_CERTIFICATE.json']))
        reruns.append(replay_owned('relation_calibrations.py', ['RELATION_CALIBRATIONS.json']))
        # Rehash all preserved inputs after replay; output writes were only captured.
        table(originals['files'])
        table(obj(E / 'CACHE_MANIFEST.json')['files'], E)
    print(json.dumps({
        'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'status': 'PRESEAL_CHECKS_PASS' if args.preseal else 'PASS',
        'optimized_interpreter': bool(sys.flags.optimize),
        'owned_bindings': owned_count,
        'original_bindings': original_count,
        'cache_bindings': cache_count,
        'source_ready_bindings': ready_count,
        'early_bound_files': early_count,
        'self_control': self_control,
        'owned_certificate_reruns': reruns,
        'supplied_source_programmes_executed': False,
        'filesystem_mutations': False,
    }, indent=2))


if __name__ == '__main__':
    main()
