#!/usr/bin/env python3
"""Pure helper checks only; no prepare/assess/Git/service call occurs here."""
from pathlib import Path
import ast, copy, csv, datetime, hashlib, importlib.util, io, json, os, stat, sys, tempfile, unittest, zipfile

O = Path(__file__).resolve().parent
D = O.parent / 'native_publication_integration_plan_20261006'
HELPER_SHA = 'd4a322d8abf8e4e2e259b6d865ea3839e5ace5c7bc4aa3f89fc527c6dda4a9f6'
source = (D / 'prepare_review_bundle.py').read_bytes()
if hashlib.sha256(source).hexdigest() != HELPER_SHA:
    raise RuntimeError('Sealed helper changed')
module = importlib.util.module_from_spec(importlib.util.spec_from_file_location('prepare_review_bundle', D / 'prepare_review_bundle.py'))
sys.modules['prepare_review_bundle'] = module
exec(compile(source, str(D / 'prepare_review_bundle.py'), 'exec'), module.__dict__)
h = module
# Original fixtures use D only as a temporary-directory parent. Redirect it in
# memory so every temporary file stays in this review's allowed output scope.
h.D = O
test_source = (D / 'test_review_bundle.py').read_bytes()
original_tests = {'__name__': 'sealed_writer_tests', '__file__': str(D / 'test_review_bundle.py')}
exec(compile(test_source, original_tests['__file__'], 'exec'), original_tests)
suite = unittest.defaultTestLoader.loadTestsFromTestCase(original_tests['ScopeFixtures'])
stream = io.StringIO()
writer_result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
if not writer_result.wasSuccessful():
    raise RuntimeError(stream.getvalue())

results = []
def record(name, status, detail):
    results.append({'name': name, 'status': status, 'detail': detail})

target = {'id': h.K, 'local_status': 'claimed_solved', 'turns_used': 2,
          'eligible': False, 'rank': None, 'ev': 0.2, 'holds': [], 'reasons': ['old']}
for char in ['\v', '\f', '\x1c', '\x1d', '\x1e', '\x85', '\u2028', '\u2029']:
    data = ('id,local_status,turns_used,eligible,rank,ev,holds,reasons\r\n'
            'fixture,queued,0,True,1,0.1,"keep' + char + 'this",old\r\n'
            '30003996,queued,0,True,2,0.2,,old\r\n').encode()
    output = h.csv_overlay(data, target)
    rows = list(csv.DictReader(io.StringIO(output.decode(), newline='')))
    old_rows = list(csv.DictReader(io.StringIO(data.decode(), newline='')))
    preserved = rows[0] == old_rows[0] and len(rows) == 2 and rows[1]['turns_used'] == '2'
    if preserved:
        raise RuntimeError('Expected all-size CSV counterexample disappeared: ' + repr(char))
    record('CSV_UNRELATED_U+' + format(ord(char), '04X'), 'counterexample_reproduced',
           {'input': data.decode(), 'output': output.decode(), 'parsed_rows': rows,
            'mechanism': 'str.splitlines counts extra Unicode/control separators that csv.reader.line_num does not count'})

old = [{'id': h.K, 'local_status': 'queued', 'turns_used': 0, 'eligible': True, 'rank': 1},
       {'id': 'other', 'local_status': 'queued', 'turns_used': 0, 'eligible': True, 'rank': 2}]
new = copy.deepcopy(old)
new[0].update(local_status='claimed_solved', turns_used=2, eligible=False, rank=None)
new[1]['eligible'] = False
rows, drift = h.scoped_catalog(old, new, {h.K: {'status': 'claimed_solved', 'turns_used': 2},
                                         'other': {'status': 'queued', 'turns_used': 0}})
if rows[1] != old[1] or len(drift) != 1:
    raise RuntimeError('Scoped restoration control failed')
record('ELIGIBILITY_DRIFT_EXPLANATION_INCOMPLETE', 'accepted_but_baseline_restored',
       {'drift': drift, 'preserved_row': rows[1],
        'mechanism': 'Eligibility-only drift passes while native status queued/turns0 remains unchanged; helper never checks eligible formula'})

with tempfile.TemporaryDirectory(dir=O, prefix='small_fixture_') as temporary:
    root = Path(temporary)
    (root / 'data').write_bytes(b'safe')
    (root / 'link').symlink_to(root / 'data')
    try:
        h.regular(root / 'link')
    except ValueError:
        record('SYMLINK_CONTROL', 'rejected', 'No external write or extraction')
    else:
        raise RuntimeError('Symlink unexpectedly accepted')
    cfg = root / 'template.json'
    cfg.write_text(json.dumps({'schema': 'pr108-native-publication-integration-config/v1',
                              'mode': 'review_bundle_only', 'template_only': True,
                              'commissioned_after_independent_review': True}))
    original_reader = h.Reader.run
    def forbidden_external(*args, **kwargs):
        raise RuntimeError('Fixture attempted an external read')
    h.Reader.run = forbidden_external
    try:
        try:
            h.prepare(cfg)
        except ValueError as exc:
            if 'Template configuration cannot run' not in str(exc):
                raise
            record('TEMPLATE_EXTERNAL_READ_SENTINEL', 'rejected_before_external_reads', str(exc))
        else:
            raise RuntimeError('Template accepted')
    finally:
        h.Reader.run = original_reader

# Run only the exact static original-authentication guard slice against an
# in-memory fake Git reader and tiny source fixtures. No prepare call occurs.
with tempfile.TemporaryDirectory(dir=O, prefix='auth_fixture_') as temporary:
    fixture = Path(temporary)
    original = O.parent / 'original_source_authentication_20261006'
    auth = json.loads((original / 'ORIGINAL_BLOB_MANIFEST.json').read_bytes())
    qauth = json.loads((original / 'QUEUE_STATUS_PROJECTION.json').read_bytes())
    blobs = {entry['path']: (original / 'original_attempt' / entry['relative_path']).read_bytes()
             for entry in auth['files']}
    original_queue = qauth['selected_row'].encode() + b'\n'
    # Preserve actual selected-row content, but use a small synthetic whole queue
    # consistently in its metadata and fake Git response.
    qauth['whole_QUEUE_bytes'] = len(original_queue)
    qauth['whole_QUEUE_sha256'] = h.sha(original_queue)
    qauth['selected_row_sha256'] = '0' * 64
    for entry in auth['files']:
        if entry['relative_path'] == 'README.md': entry['relative_path'] = 'RESEARCH_LOG.md'
        elif entry['relative_path'] == 'RESEARCH_LOG.md': entry['relative_path'] = 'README.md'
        path = fixture / 'original_attempt' / entry['relative_path']
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(blobs[entry['path']])
    (fixture / 'ORIGINAL_BLOB_MANIFEST.json').write_text(json.dumps(auth))
    (fixture / 'QUEUE_STATUS_PROJECTION.json').write_text(json.dumps(qauth))
    class InMemoryGit:
        def git(self, *args, retain=True):
            if args[0] == 'ls-tree':
                return ('\n'.join(sorted(blobs)) + '\n').encode()
            requested = args[1].split(':', 1)[1]
            if requested == h.P + 'QUEUE.md': return original_queue
            return blobs[requested]
    auth_guard = '\n'.join(line[4:] if line.startswith('    ') else line
                           for line in source.decode().splitlines()[350:370])
    env = {**h.__dict__, 'ORIGINAL': fixture, 'reader': InMemoryGit()}
    exec(compile(auth_guard, '<sealed-helper-lines-351-370>', 'exec'), env)
    if env['original_files']['RESEARCH_LOG.md'] != blobs[h.N + 'README.md']:
        raise RuntimeError('Expected authentication path-map counterexample disappeared')
    record('ORIGINAL_AUTH_PATH_MAP_AND_ROW_HASH', 'counterexample_reproduced',
           {'exact_helper_lines': '351-370', 'mode': 'extracted static guard, fake in-memory Git',
            'accepted_swapped_README_and_RESEARCH_LOG_relative_paths': True,
            'accepted_false_selected_row_sha256': qauth['selected_row_sha256'],
            'current_authenticated_manifest_is_correct': True,
            'mechanism': 'Guard authenticates each HEAD blob but not path == N + relative_path; selected_row_sha256 is not recomputed'})

buf = io.BytesIO()
with zipfile.ZipFile(buf, 'w') as z:
    z.writestr('safe', b'payload')
    # A second selected member must be rejected. zipfile emits a harmless warning.
    z.writestr('safe', b'payload')
try:
    h.zip_member(buf.getvalue(), 'safe', 7)
except ValueError:
    record('ZIP_DUPLICATE_SELECTED_MEMBER', 'rejected', 'No extraction or output path')
else:
    raise RuntimeError('Duplicate selected ZIP member accepted')

document = {'schema': 'pr108-native-static-offline-adversary/v1',
            'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'actual_operator_PID': os.getpid(), 'optimized': not __debug__,
            'helper_sha256': HELPER_SHA, 'original_writer_fixture_tests': writer_result.testsRun,
            'original_writer_fixtures_passed': writer_result.wasSuccessful(),
            'writer_fixture_temporary_directory_redirected_in_memory_to': str(O),
            'no_real_prepare_native_assess_export_Git_service_or_cache_write': True,
            'additional_controls_or_counterexamples': results, 'original_writer_test_output': stream.getvalue()}
(O / ('RESULTS_OPTIMIZED.json' if not __debug__ else 'RESULTS_NORMAL.json')).write_text(json.dumps(document, indent=2, ensure_ascii=False) + '\n')
print(json.dumps({'writer_tests': writer_result.testsRun, 'checks': len(results),
                  'counterexamples': sum(x['status'] == 'counterexample_reproduced' for x in results),
                  'optimized': not __debug__, 'PID': os.getpid()}))
