"""Read-only family-custody check; never runs scientific code or Git mutations."""
from pathlib import Path
import datetime, hashlib, json

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'ROOT_completed_math_family_readback_20261004'
assert __debug__
assert not OUT.exists(), 'one-shot readback already exists'

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def pin(p):
    b = p.read_bytes()
    return {'path': str(p), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def check(base, row, path_key='path'):
    p = Path(row[path_key])
    if not p.is_absolute():
        p = base / p
    got = pin(p)
    assert got['sha256'] == row['sha256'], (p, 'digest mismatch')
    if 'bytes' in row:
        assert got['bytes'] == row['bytes'], (p, 'byte-count mismatch')
    return got

def artifact_rows(x, field):
    v = x[field]
    if isinstance(v, dict):
        return [dict(r, path=k) for k, r in v.items()]
    return v

def receipt_check(base, name, r):
    assert isinstance(r['pid'], int) and r['pid'] > 0
    assert isinstance(r['argv'], list) and r['argv']
    assert Path(r['cwd']).is_absolute()
    if any(k in r for k in ('start_utc', 'utc_start', 'utc_started')):
        start = r.get('start_utc', r.get('utc_start', r.get('utc_started')))
        end = r.get('end_utc', r.get('utc_end', r.get('utc_ended')))
        assert datetime.datetime.fromisoformat(start) <= datetime.datetime.fromisoformat(end)
    else:
        assert 'utc' in r  # disclosed bootstrap has no start/end interval
    streams = {}
    for key in ('stdout', 'stderr'):
        if isinstance(r.get(key), dict):
            row = r[key]
        else:
            row = {'path': r.get(key+'_path', r.get(key+'_file')),
                   'sha256': r[key+'_sha256']}
            if key+'_bytes' in r:
                row['bytes'] = r[key+'_bytes']
        streams[key] = check(base, row)
    return {'receipt': name, 'pid': r['pid'], 'argv': r['argv'],
            'exit_code': r.get('exit_code', r.get('exit')), 'streams': streams}

started = utc()
families = []
specs = [
    ('arrow_formula_scope_adversary_20261004', 'FINAL_MANIFEST.json', 'files',
     'FORMULA_SCOPE_REPORT.md', True),
    ('jones_algebraic_calibration_adversary_20261004', 'artifact_manifest.json', 'artifacts',
     'FINAL_REPORT.md', False),
    ('fresh_graph_proof_adversary_20261004', 'MANIFEST.json', 'files',
     'ADVERSARIAL_REPORT.md', False),
    ('tournament_domination_adversary_20261004', 'ARTIFACT_MANIFEST.json', 'files',
     'GRAPH_AUDIT_REPORT.md', True),
]
for directory, mf, field, report, exposed in specs:
    base = ROOT / directory
    manifest = json.loads((base / mf).read_text())
    rows = artifact_rows(manifest, field)
    assert len({r['path'] for r in rows}) == len(rows)
    artifacts = [check(base, row) for row in rows]
    receipts = []
    if directory.startswith('tournament_'):
        ledger = [json.loads(x) for x in (base/'ACTUAL_COMMANDS.jsonl').read_text().splitlines()]
        bounded = [json.loads(x) for x in (base/'ACTUAL_COMMANDS_BOUNDED.jsonl').read_text().splitlines()]
        assert ledger[:len(bounded)] == bounded
        receipts += [receipt_check(base, r['name'], r) for r in ledger]
        receipts += [receipt_check(base, 'bootstrap_receipt.json', json.loads((base/'bootstrap_receipt.json').read_text()))]
    else:
        for f in sorted(base.rglob('*.json')):
            x = json.loads(f.read_text())
            if isinstance(x, dict) and 'pid' in x and 'argv' in x:
                receipts.append(receipt_check(base, str(f.relative_to(base)), x))
    source_pins = []
    if directory.startswith('arrow_'):
        x = json.loads((base/'PRIVATE_SOURCE_PINS.json').read_text())
        for row in artifact_rows(x, 'artifacts'):
            source_pins.append(check(base, row))
    elif directory.startswith('jones_'):
        x = json.loads((base/'source_manifest.json').read_text())
        source_pins = [check(base, row) for row in x['records']]
    families.append({'family': directory, 'report': pin(base/report),
                     'first_conclusion': pin(base/'FIRST_CONCLUSION.md'),
                     'prior_opinion_exposed': exposed, 'manifest': pin(base/mf),
                     'artifact_count': len(artifacts), 'receipt_count': len(receipts),
                     'preserved_nonzero_exits': [r for r in receipts if r['exit_code'] != 0],
                     'execution_receipts': receipts, 'private_source_pins': source_pins})

original = ROOT/'original_source_authentication_20261004/original/unsolved_math_prioritization/attempts/10400033'
assert pin(original/'CANDIDATE.md')['sha256'] == 'fc2be9794873073e6482e8dfe93ccfd6c5d6f8674c2058ba0a8fc900d906d698'
assert pin(original/'source_record.json')['sha256'] == '075059240df7ba3bfac89aaf96f8f9fb176b12b61e6e7f7fdd1f8e1d93a8d4bc'
status = json.loads((original/'status.json').read_text())
assert status['status'] == 'claimed_solved' and status['turns_used'] == 1 and 'turn_limit' not in status
ledger = [json.loads(s) for s in (original/'turns.jsonl').read_text().splitlines()]
assert len(ledger) == 3 and all(s['turn'] == 1 for s in ledger)

OUT.mkdir()
result = {'utc_started': started, 'utc_completed': utc(), 'status': 'PASS',
          'operator': pin(Path(__file__)), 'families': families,
          'original_candidate': pin(original/'CANDIDATE.md'),
          'original_source_record': pin(original/'source_record.json'),
          'original_ledger': {'turns_used': 1, 'proof_limit_from_queue': 5,
                              'status_turn_limit_field': 'ABSENT', 'event_count': 3},
          'limits': 'Verifies retained bodies and actual execution stream custody. Does not reproduce unrecorded child environments, prove independence beyond disclosed access records, or convert finite diagnostics into universal theorems.'}
(OUT/'READBACK.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({'status': 'PASS', 'families': [{k:r[k] for k in ('family','artifact_count','receipt_count','prior_opinion_exposed')} for r in families], 'readback': str(OUT/'READBACK.json')}, indent=2))
