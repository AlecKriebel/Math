"""Supplementary mock controls: strict archive schema and immutable notice reads."""
import contextlib, datetime, importlib.util, io, json, pathlib, sys, tempfile, zipfile
from unittest.mock import patch
sys.dont_write_bytecode = True
OUT = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('local_independent_runner', OUT / 'run_review.py')
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)
p = r.p
t = r.t
results = []
with zipfile.ZipFile(io.BytesIO(r.PUB['gns_verification.zip'])) as archive:
    members = {name: archive.read(name) for name in archive.namelist()}
for schema in (1, True, 1.0, 2, False):
    changed = dict(members)
    manifest = p.parse_json(changed['PACKAGE_MANIFEST.json'])
    manifest['schema'] = schema
    changed['PACKAGE_MANIFEST.json'] = p.json_bytes(manifest)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for name, data in changed.items():
            z.writestr(name, data)
    try:
        output = p.archive_binding(buf.getvalue(), r.ORIGINAL, r.PUB, r.SOURCE)
        outcome = 'ACCEPTED'
    except Exception as exc:
        outcome = 'REJECTED'
        output = {'error': str(exc)}
    results.append({'case': 'archive_schema', 'schema_repr': repr(schema), 'schema_type': type(schema).__name__, 'outcome': outcome, 'output': output})
p.require([x['outcome'] for x in results] == ['ACCEPTED', 'ACCEPTED', 'ACCEPTED', 'REJECTED', 'REJECTED'], 'independent control failed')
with tempfile.TemporaryDirectory(dir=OUT, prefix='notice-race-') as td:
    root = pathlib.Path(td)
    publication = root / 'publication'
    publication.mkdir()
    src = publication / 'CURRENT_PRIORITY_AND_STATUS.md'
    src.write_bytes(r.SOURCE)
    for name, data in r.PUB.items():
        (publication / name).write_bytes(data)
    rr = r.ns['receipt']()
    for name in ['ZENODO_PUBLICATION_RECEIPT.json', 'ZENODO_POST_PUBLICATION_INSPECTION.json']:
        (root / name).write_bytes(p.json_bytes(rr))
    base, tree, commit = ('c' * 40, 'd' * 40, 'e' * 40)
    after, _ = p.patch_queue(r.QUEUE, r.DOI)
    current = {}
    calls = []
    real_build = p.build_current_files
    real_pub = p.publication_inputs
    alternate_source = r.SOURCE + b'Notice bytes changed after immutable archive validation.\n'

    def build(*args):
        answer = real_build(*args)
        current.update(answer)
        return answer

    def pub(*args):
        answer = real_pub(*args)
        src.write_bytes(alternate_source)
        return answer

    def git(*args, env=None, input=None):
        calls.append(args)
        if args[0] == 'show':
            if args[1] == p.ORIGINAL + ':' + p.QPATH:
                return after
            if args[1] == base + ':' + p.QPATH:
                return r.QUEUE
            return r.ORIGINAL[args[1].split(':' + p.PREFIX, 1)[1]]
        if args[0] in ['fetch', 'ls-tree', 'read-tree', 'update-index']:
            return b''
        if args[0] == 'rev-parse':
            return (base + '\n').encode()
        if args[0] == 'hash-object':
            return ('f' * 40 + '\n').encode()
        if args[0] == 'write-tree':
            return (tree + '\n').encode()
        if args[0] == 'diff':
            return b'1\t1\tqueue\n' if args[1] == '--numstat' else ('\n'.join(sorted({p.QPATH} | {p.PREFIX + n for n in current})) + '\n').encode()
        if args[0] == 'commit-tree':
            return (commit + '\n').encode()
        raise AssertionError('unexpected mocked Git call ' + repr(args))
    with patch.object(p, 'A', root), patch.object(p, 'PUSHED_RECEIPT', root / 'absent'), patch.object(p, 'local_state', return_value={'head': 'main', 'index_sha256': 'unchanged'}), patch.object(p, 'pr_metadata', return_value=r.META), patch.object(p, 'git', side_effect=git), patch.object(p, 'load_snapshot', return_value=(r.ORIGINAL, r.FROZEN)), patch.object(p, 'publication_inputs', side_effect=pub), patch.object(p, 'build_current_files', side_effect=build), patch.object(sys, 'argv', ['helper', '--doi', r.DOI, '--source-audit', str(src)]), contextlib.redirect_stdout(io.StringIO()):
        p.main()
    receipt = p.parse_json((root / 'INTEGRATION_PREPARED_RECEIPT.json').read_bytes())
    p.require(current['CURRENT_SOURCE_AUDIT.md'].endswith(alternate_source), 'independent control failed')
    p.require(receipt['publication_validation']['current_source_notice_sha256'] == p.sha(r.SOURCE), 'independent control failed')
    p.require(receipt['current_attempt_replay']['integrity'] == 'PASS', 'independent control failed')
    p.require(not any((x[0] == 'push' for x in calls)), 'independent control failed')
    results.append({'case': 'notice_read_race', 'outcome': 'ACCEPTED_MISMATCH', 'validated_notice_sha256': p.sha(r.SOURCE), 'integrated_source_suffix_sha256': p.sha(alternate_source), 'prepared_receipt_saved': True, 'wrapper_integrity': receipt['current_attempt_replay']['integrity'], 'integrated_notice_contains_post_validation_changed_bytes': True, 'all_git_calls_mocked': True, 'push_calls': 0})
obj = {'captured_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'results': results, 'python_optimization': sys.flags.optimize, 'remote_mutations': 0, 'git_mutations': 0, 'writes_outside_review_folder': 0}
(OUT / ('ADDITIONAL_ADVERSARIAL_O' + str(sys.flags.optimize) + '_RESULTS.json' if sys.flags.optimize else 'ADDITIONAL_ADVERSARIAL_RESULTS.json')).write_text(json.dumps(obj, indent=2) + '\n')
with (OUT / 'RESEARCH_LOG.md').open('a') as log:
    log.write('\n' + obj['captured_utc'] + ' — Reproduced two boundary failures: archive schema accepts Boolean true and floating 1.0; full mocked integration accepts a source notice changed after ZIP binding, and integrity replay passes. Exact evidence saved in ADDITIONAL_ADVERSARIAL_RESULTS.json. Completion estimate: 85%.\n')
print(json.dumps(obj, indent=2))
