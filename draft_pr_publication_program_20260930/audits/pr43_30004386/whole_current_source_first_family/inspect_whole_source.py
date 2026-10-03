"""Handwritten read-only whole-source inspection; executes no foreign source."""
from pathlib import Path
import collections, datetime, hashlib, json, os, stat

OWN = Path.cwd().resolve()
AUDIT = OWN.parent
REPO = AUDIT.parents[2]
CANDIDATE = AUDIT / 'reviewed_candidate'
EXPECT_MANIFEST = '4849e6037a5db3dce546a656dcd57063ae83d782c19e24d4e3dff97ebbcdec14'
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
reads = []
failures = []
summaries = {}

def read(path, role, expected=None):
    path = Path(path)
    ls = path.lstat()
    if not stat.S_ISREG(ls.st_mode):
        failures.append({'path': str(path), 'failure': 'not regular file'})
        return None
    raw = path.read_bytes()
    h = hashlib.sha256(raw).hexdigest()
    rec = {'path': str(path.resolve()), 'role': role, 'bytes': len(raw),
           'sha256': h, 'S_IMODE': f'{stat.S_IMODE(ls.st_mode):04o}',
           'entire_bytes_read': True, 'executed': False}
    if expected:
        rec['expected'] = expected
        for k, got in [('sha256', h), ('bytes', len(raw))]:
            if k in expected and expected[k] != got:
                failures.append({'path': str(path), 'failure': f'{k} mismatch', 'got': got, 'expected': expected[k]})
        if 'mode' in expected and expected['mode'] != rec['S_IMODE']:
            failures.append({'path': str(path), 'failure': 'mode mismatch'})
    try:
        txt = raw.decode('utf-8')
        rec['text_lines'] = len(txt.splitlines())
    except UnicodeDecodeError:
        txt = None
        rec['text_lines'] = None
    if path.suffix == '.json':
        try:
            obj = json.loads(raw)
            rec['json_type'] = type(obj).__name__
            rec['json_top_keys'] = list(obj) if isinstance(obj, dict) else None
            counts = collections.Counter()
            def walk(x):
                counts[type(x).__name__] += 1
                if isinstance(x, dict):
                    for v in x.values(): walk(v)
                if isinstance(x, list):
                    for v in x: walk(v)
            walk(obj)
            rec['json_recursive_type_counts'] = dict(counts)
            summaries[str(path.relative_to(AUDIT)) if path.is_relative_to(AUDIT) else str(path)] = {
                'top_keys': rec['json_top_keys'], 'types': dict(counts), 'bytes':len(raw)}
        except Exception as e:
            failures.append({'path':str(path), 'failure':'JSON parse', 'exception':repr(e)})
    reads.append(rec)
    return raw

manifest_raw = read(CANDIDATE / 'MANIFEST.json', 'frozen candidate manifest', {'sha256': EXPECT_MANIFEST})
manifest = json.loads(manifest_raw)
entries = manifest['files']
expected_paths = {e['path'] for e in entries} | {'MANIFEST.json'}
actual_paths = {str(p.relative_to(CANDIDATE)) for p in CANDIDATE.rglob('*') if p.is_file() or p.is_symlink()}
if len(entries) != 347 or len({e['path'] for e in entries}) != len(entries):
    failures.append({'failure':'manifest count or uniqueness'})
if expected_paths != actual_paths:
    failures.append({'failure':'candidate closure', 'missing': sorted(expected_paths-actual_paths), 'extra':sorted(actual_paths-expected_paths)})
for e in entries:
    read(CANDIDATE / e['path'], 'candidate frozen member', e)
if stat.S_IMODE((CANDIDATE/'MANIFEST.json').stat().st_mode) != 0o444:
    failures.append({'failure':'manifest mode not exactly 0444'})
deps = json.loads((CANDIDATE/'CURRENT_DEPENDENCIES.json').read_bytes())
anchor = REPO / deps['anchor_repository_relative']
if anchor.resolve() != AUDIT.resolve():
    failures.append({'failure':'dependency anchor'})
for e in deps['files']:
    read(anchor/e['path'], 'candidate external dependency: '+','.join(e['roles']), e)
for e in deps['current_native13']:
    read(REPO/e['path'], 'candidate current native preimage', e)
execution = json.loads((CANDIDATE/'CURRENT_EXECUTION_REFERENCE.json').read_bytes())
for key in ['audit_relative_outer_capture', 'audit_relative_inner_attempt']:
    p = AUDIT / execution[key]
    for q in sorted(p.rglob('*')):
        if q.is_file() or q.is_symlink():
            read(q, 'completed current actual execution at original path: '+key)
for q in sorted((AUDIT/'root_current_freeze_operator_actual_capture').rglob('*')):
    if q.is_file() or q.is_symlink():
        read(q, 'current ROOT outermost completed operation')
for name in ['ROOT_CURRENT_PREREQUISITES_INSPECTION.json', 'ROOT_PREREQUISITES_PRELAUNCH_SOURCE.py']:
    read(AUDIT/name, 'current ROOT prerequisite actual record/source')

report = {'schema':'INDEPENDENT_WHOLE_CURRENT_SOURCE_READ_v1',
          'started_utc': started, 'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'actual_pid':os.getpid(), 'candidate_manifest_sha256':EXPECT_MANIFEST,
          'candidate_member_count_excluding_manifest':len(entries),
          'candidate_external_dependency_count':len(deps['files']),
          'current_native_preimage_count':len(deps['current_native13']),
          'reads':reads, 'json_summaries':summaries, 'failures':failures,
          'scope':'Mechanical entire-byte/hash/mode/typed JSON inspection only; semantic adversarial verdict separate.',
          'foreign_execution':False, 'native_git_remote_mutations':False}
(OWN/'WHOLE_SOURCE_READ_LEDGER.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['reads','json_summaries']},indent=2))
print('Total individually recorded full reads:',len(reads),'bytes:',sum(x['bytes'] for x in reads))
print('Largest text/source members:',json.dumps(sorted([{'path':r['path'],'bytes':r['bytes'],'lines':r['text_lines']} for r in reads if r['text_lines'] is not None],key=lambda x:x['bytes'],reverse=True)[:15],indent=2))
raise SystemExit(bool(failures))
