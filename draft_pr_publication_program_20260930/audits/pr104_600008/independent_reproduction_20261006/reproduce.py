#!/usr/bin/env python3
"""Exact unmodified replay, deliberately false controls, and one raw execution ledger."""
from pathlib import Path
import datetime, hashlib, json, shutil, subprocess

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / 'original_source_authentication_20261006/original_attempt'
REPLAY = ROOT / 'exact_replay'
INPUT_NAMES = ['ANALYTIC_CRITERION.md', 'verify.py', 'review/independent_checks.py',
               'verification.json', 'review/independent_results.json', 'source_record.json']
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
for src, dest in [('ANALYTIC_CRITERION.md', 'ANALYTIC_CRITERION.md'),
                  ('verify.py', 'verify.py'),
                  ('review/independent_checks.py', 'review/independent_checks.py'),
                  ('ANALYTIC_CRITERION.md', 'review/author_replay/ANALYTIC_CRITERION.md')]:
    target = REPLAY / dest
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SOURCE / src, target)
records = json.loads((ROOT/'EXECUTIONS.json').read_text()) if (ROOT/'EXECUTIONS.json').exists() else []
def run(label, argv):
    record = {'label': label, 'started_utc': utc(), 'argv': argv, 'cwd': str(ROOT)}
    if argv[-1].endswith('.py') and Path(argv[-1]).is_file():
        record['source_sha256']=sha(Path(argv[-1]))
    result = subprocess.run(argv, cwd=ROOT, text=True, capture_output=True)
    record.update(finished_utc=utc(), exit_code=result.returncode,
                  stdout=result.stdout, stderr=result.stderr)
    records.append(record)
    (ROOT / 'EXECUTIONS.json').write_text(json.dumps(records, indent=2) + '\n')
    print(label + ': exit ' + str(result.returncode), flush=True)
    return record
for label, relative in [('author', 'verify.py'), ('old_independent', 'review/independent_checks.py')]:
    script = str(REPLAY / relative)
    for optimized in (False, True):
        flags = ['-E', '-B'] + (['-O'] if optimized else [])
        run(label + ('_optimized' if optimized else '_normal'), ['/usr/bin/python3'] + flags + [script])
        code = ('import runpy; ns=runpy.run_path(' + repr(script) + '); '
                'ns["ck"]("forced_false_control", False); '
                'print("FORCED_FALSE_ACCEPTED: assertion enforcement absent")')
        run(label + ('_false_optimized' if optimized else '_false_normal'),
            ['/usr/bin/python3'] + flags + ['-c', code])
run('new_ambient_diagnostics', ['/usr/bin/python3', '-E', '-B', str(ROOT / 'ambient_diagnostics.py')])
run('independent_minimal_guard_repair_assessment', ['/usr/bin/python3', '-E', '-B', str(ROOT/'assess_guard_repair.py')])
reference = { 'author': json.loads((SOURCE / 'verification.json').read_text()),
              'old_independent': json.loads((SOURCE / 'review/independent_results.json').read_text()) }
comparison = {}
for label in reference:
    executed = next(r for r in reversed(records) if r['label'] == label + '_normal')
    observed = json.loads(executed['stdout'])
    comparison[label] = {'observed_exact_assertions': observed['exact_assertions'],
                         'reference_exact_assertions': reference[label]['exact_assertions'],
                         'counts_match': observed['checks'] == reference[label]['checks'],
                         'artifact_sha256_match': observed['artifact_sha256'] == reference[label]['artifact_sha256']}
(ROOT / 'REPRODUCTION_COMPARISON.json').write_text(json.dumps(comparison, indent=2) + '\n')
manifest = {'created_utc': utc(), 'inputs': [
    {'path': str(SOURCE / n), 'sha256': sha(SOURCE / n), 'bytes': (SOURCE / n).stat().st_size}
    for n in INPUT_NAMES], 'outputs': []}
for p in [ROOT.parent/'primary_sources_20261006/gkt2007.txt',
          ROOT.parent/'primary_sources_20261006/tabachnikov2015.txt',
          ROOT.parent/'repaired_diagnostics_v1/verify.py',
          ROOT.parent/'repaired_diagnostics_v1/independent_checks.py',
          ROOT.parent/'repaired_diagnostics_v1/ANALYTIC_CRITERION.md',
          ROOT.parent/'repaired_diagnostics_v1/author_replay/ANALYTIC_CRITERION.md']:
    manifest['inputs'].append({'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size})
for p in sorted(ROOT.rglob('*')):
    if p.is_file() and p.name != 'MANIFEST.json':
        manifest['outputs'].append({'path': str(p.relative_to(ROOT)), 'sha256': sha(p), 'bytes': p.stat().st_size})
(ROOT / 'MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
