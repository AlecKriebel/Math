"""Read-only107 custody and optional in-memory replay of only OWN controls.

Use without --preseal for the final immutable handoff. Explicit exceptions
remain active under -O. No provided archive programme or older check is run.
"""
from pathlib import Path
from collections import Counter
import argparse, contextlib, copy, datetime, hashlib, io, json, re, runpy, sys

E = Path(__file__).resolve().parent
P = E.parents[3]
S = P / 'papers/23333046/sources'
HEX = re.compile('[0-9a-f]{64}')


def need(v, reason):
    if not v:
        raise RuntimeError(reason)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def obj(p):
    return json.loads(p.read_text())


def check(r, base=None):
    need(type(r) is dict, 'binding_object')
    need(type(r.get('path')) is str, 'binding_path')
    need(type(r.get('bytes')) is int and r['bytes'] >= 0, 'binding_size_schema')
    need(type(r.get('sha256')) is str and HEX.fullmatch(r['sha256']), 'binding_lowercase_sha_schema')
    p = Path(r['path'])
    if base:
        need(not p.is_absolute() and '..' not in p.parts, 'safe_relative_binding')
        p = base / p
    else:
        need(p.is_absolute(), 'absolute_original_binding')
    need(p.is_file() and not p.is_symlink(), 'binding_regular_file:' + str(p))
    need(p.stat().st_size == r['bytes'], 'binding_size:' + str(p))
    need(sha(p) == r['sha256'], 'binding_hash:' + str(p))
    return str(p)


def table(rows, base=None):
    need(type(rows) is list and rows, 'nonempty_binding_list')
    paths = [check(r, base) for r in rows]
    need(len(paths) == len(set(paths)), 'unique_binding_paths')
    return len(rows)


def replay_owned():
    allowed = (E / 'EXACT_CONTROLS.json').resolve()
    captured = []
    oldwrite = Path.write_text
    oldargv = sys.argv[:]

    def capture(p, data, *args, **kwargs):
        need(p.resolve() == allowed and type(data) is str, 'unexpected_owned_replay_write')
        captured.append(data)
        return len(data)

    try:
        Path.write_text = capture
        sys.argv = [str(E / 'exact_controls.py')]
        with contextlib.redirect_stdout(io.StringIO()):
            runpy.run_path(str(E / 'exact_controls.py'), run_name='__main__')
    finally:
        Path.write_text = oldwrite
        sys.argv = oldargv
    need(len(captured) == 1, 'single_owned_control_output')
    actual = json.loads(captured[0])
    expected = obj(allowed)
    actual.pop('utc')
    expected.pop('utc')
    need(actual == expected, 'entire_owned_exact_control_reproduced')
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--preseal', action='store_true')
    ap.add_argument('--self-control', action='store_true')
    ap.add_argument('--replay-owned', action='store_true')
    a = ap.parse_args()
    need((E / '.gitignore').read_text() == 'cache/\n', 'ignored_private_evidence')
    pins = {
        S / 'SOURCE_READY.json': 'ef9681061855c3e1c80e1f4e9b1b9538600bb7c9b15bba18d8fd78e98c38c478',
        S / 'SOURCE_READY_MANIFEST.json': 'b680fea3ffaa1ce5f6ebf1386d70da988b39bb437d04998de90e043618bd1f05',
        S / 'SOURCE_READY_SEAL.json': '0b47008701fdf09019ae4ae87a09d648c90992ab4253b67481ec7bd7b36d355d',
        E / 'EARLY_SEAL.json': '4ecb5a11b79250e96b9a7d6f52cb97a8bb2c1bff472f109c67aee3bb03603005',
        P / 'papers/23124601/reviews/analytic/MANIFEST.json': 'e4e6412bcd7d2e39e295fece9badff158c2cba5a5114695ee64cacef4a952904',
        P / 'papers/23124601/reviews/analytic/SEAL.json': '51fad32511850f042556cc12c51ad431f82465c813e7f39a231e85e6ae5d0d14',
    }
    for p, h in pins.items():
        need(sha(p) == h, 'independent_exact_pin:' + str(p))
    early = obj(E / 'EARLY_SEAL.json')
    need(sha(E / 'EARLY_MANIFEST.json') == early['manifest_sha256'], 'early_manifest_seal')
    need(sha(E / 'EARLY_RECONSTRUCTION.md') == early['notes_sha256'], 'early_notes_seal')
    ec = table(obj(E / 'EARLY_MANIFEST.json')['files'])
    ready = table(obj(S / 'SOURCE_READY_MANIFEST.json')['files'], S)
    need(ready == 163, 'exact_source_ready_count')
    originals = obj(E / 'ORIGINAL_BINDINGS.json')
    oc = table(originals['files'])
    need(dict(Counter(r['kind'] for r in originals['files'])) == originals['counts_by_kind'], 'original_category_counts')
    original_paths = {r['path'] for r in originals['files']}
    need(all(str(S / r['path']) in original_paths for r in obj(S / 'SOURCE_READY_MANIFEST.json')['files']), 'entire_ready_original_map')
    cc = table(obj(E / 'CACHE_MANIFEST.json')['files'], E)
    need(obj(E / 'EXACT_CONTROLS.json')['status'] == 'PASS', 'positive_exact_controls')
    faults = obj(E / 'FAULT_CONTROLS.json')
    need(faults['status'] == 'PASS' and len(faults['controls']) == 6, 'six_fault_controls')
    need(all(r['exit_code'] != 0 and r['actual_expected_rejection'] for r in faults['controls']), 'actual_fault_rejections')
    need(sha(E / 'exact_controls.py') == faults['owned_script_sha256'], 'executed_own_code_identity')
    need(sha(E / 'EXACT_CONTROLS.json') == faults['successful_receipt_sha256'], 'positive_unchanged_by_faults')
    archive = obj(E / 'OWN_ARCHIVE_CHECK.json')
    need(archive['status'] == 'PASS' and len(archive['members']) == archive['all_regular_members_CRC_read_in_memory'] == 154, 'full_archive_member_receipt')
    need(sum(r['bytes'] for r in archive['members']) == archive['expanded_regular_member_bytes'] == 884320, 'archive_expanded_count')
    need(all(r['existing_original_extraction_byte_identity'] for r in archive['members']), 'archive_existing_identity_receipts')
    vc = 'VERIFIED_UNRESTRICTED_COUNTEREXAMPLE_IN_ORIGINAL_UNFRAMED_CATEGORY_WITH_KNOWN_ANTECEDENTS_AND_EXPLICIT_SCOPE_LIMITS'
    need(obj(E / 'VERDICT.json')['verdict'] == vc and not obj(E / 'VERDICT.json')['publication_or_page_authority'], 'literal_custom_verdict')
    own = None
    if not a.preseal:
        seal = obj(E / 'SEAL.json')
        need(sha(E / 'MANIFEST.json') == seal['manifest_sha256'], 'final_manifest_seal')
        need(sha(E / 'REPORT.md') == seal['report_sha256'], 'final_report_seal')
        need(sha(E / 'VERDICT.json') == seal['verdict_sha256'], 'final_verdict_seal')
        mf = obj(E / 'MANIFEST.json')
        own = table(mf['files'], E)
        need(own == mf['owned_bindings'] == seal['owned_bindings'], 'exact_owned_count')
        actual = {str(p.relative_to(E)) for p in E.rglob('*') if p.is_file() and 'cache' not in p.relative_to(E).parts and p.name not in ('MANIFEST.json','SEAL.json')}
        need(actual == {r['path'] for r in mf['files']}, 'full_owned_inventory')
        need(oc == seal['original_bindings'] and cc == seal['cache_bindings'], 'final_original_cache_count')
    control = None
    if a.self_control:
        bad = copy.deepcopy(originals['files'][0])
        bad['sha256'] = '0' * 64
        try:
            check(bad)
        except RuntimeError as exc:
            need(str(exc).startswith('binding_hash:'), 'correct_hash_fault_gate')
            control = True
        else:
            raise RuntimeError('wrong_original_hash_accepted')
    replay = replay_owned() if a.replay_owned else False
    if replay:
        table(originals['files'])
        table(obj(E / 'CACHE_MANIFEST.json')['files'], E)
    print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PRESEAL_CHECKS_PASS' if a.preseal else 'PASS','optimized':bool(sys.flags.optimize),'owned_bindings':own,'original_bindings':oc,'cache_bindings':cc,'source_ready_bindings':ready,'early_bindings':ec,'wrong_hash_rejected':control,'own_exact_controls_replayed_in_memory':replay,'older_or_supplied_programmes_executed':False,'filesystem_mutations':False},indent=2))


if __name__ == '__main__':
    main()
