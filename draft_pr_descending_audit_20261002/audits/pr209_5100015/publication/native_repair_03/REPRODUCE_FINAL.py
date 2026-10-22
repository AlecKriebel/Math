"""Replay exact final sources offline inside one NEW writable sandbox.

Invoke with the existing Python runtime -B and one new absolute folder path.
Original sealed evidence is read only; all providers are fixture protocols.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, shutil, subprocess, sys

HERE = Path(__file__).resolve().parent
PYTHON = '/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
if len(sys.argv) != 2:
    raise RuntimeError('Provide one new sandbox path')
target = Path(sys.argv[1]).absolute()
target.mkdir(exist_ok=False)
pub = target / 'publication'
work = pub / 'native_repair_03'
snapshot = work / 'candidate_sources_01'
snapshot.mkdir(parents=True)
inputs = json.loads((HERE / 'FINAL_SOURCE_INPUTS.json').read_bytes())
for row in inputs['files']:
    raw = (HERE / 'candidate_sources_01' / row['path']).read_bytes()
    if len(raw) != row['bytes'] or hashlib.sha256(raw).hexdigest() != row['sha256']:
        raise RuntimeError('Exact final source differs')
    (snapshot / row['path']).write_bytes(raw)
    (pub / row['path']).write_bytes(raw)
for name in ['binding_fixture_source.py', 'legacy_fixture_source.py', 'archive_completed_group.py',
        'probes_joint_final.py', 'probes_joint_compact.py', 'receipt_controls.py', 'R03_regression.py',
        'CANDIDATE_INPUTS_01.json', 'FINAL_SOURCE_INPUTS.json']:
    shutil.copyfile(HERE / name, work / name)
observed = []
for program, label in [('receipt_controls.py', 'receipt'), ('R03_regression.py', 'R03')]:
    with (target / (label + '.stdout.jsonl')).open('xb') as out, (target / (label + '.stderr.txt')).open('xb') as err:
        result = subprocess.run([PYTHON, '-B', str(work / program)], stdout=out, stderr=err)
    row = dict(program=program, actual_exit=result.returncode, utc=datetime.now(timezone.utc).isoformat())
    print(json.dumps(row), flush=True)
    observed.append(row)
    (target / 'ACTUAL_CHILD_EXITS.json').write_text(json.dumps(observed, indent=2) + '\n')
    if result.returncode:
        raise SystemExit(result.returncode)
    if label == 'receipt':
        shutil.copyfile(work / 'RESULTS_01.json', work / 'RECEIPT_RESULTS_BEFORE_R03.json')
raise SystemExit(0)
