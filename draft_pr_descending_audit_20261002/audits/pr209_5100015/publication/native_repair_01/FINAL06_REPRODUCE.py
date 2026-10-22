"""Replay the frozen final exact-source native probes in a fresh owned folder.

Use the existing standard runtime with -B. No live providers are reachable from
the fixture; every GH/GWS/public-download operation is an in-memory protocol.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, importlib.util, json, sys, types

HERE = Path(__file__).resolve().parent
manifest = json.loads((HERE / 'EXACT_SOURCE_INPUTS_06.json').read_text())
source = {}
for row in manifest['files']:
    raw = (HERE / row['path']).read_bytes()
    if len(raw) != row['bytes'] or hashlib.sha256(raw).hexdigest() != row['sha256']:
        raise RuntimeError('Frozen source hash differs: ' + row['path'])
    source[Path(row['path']).name] = raw
sys.path.insert(0, str(HERE))
spec = importlib.util.spec_from_file_location('native_replay', HERE / 'probes_06.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
out = HERE / ('reproduction_' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
out.mkdir(exist_ok=False)
m.HERE = out
m.b.HERE = out
m.b.RUNS = out / 'fixtures'
m.b.SNAP = out / 'source_snapshot'
m.b.SNAP.mkdir()
m.b.SOURCE = source
for name, raw in source.items():
    (m.b.SNAP / name).write_bytes(raw)
real = sys.stdout
tests = [('baseline', m.baseline), ('payloads', m.payloads),
    ('forged_prepared', m.forged_prepared), ('metadata', m.metadata),
    ('main_boundaries', m.main_boundaries), ('large_scope', m.large_scope),
    ('unknown_objects', m.unknown_objects), ('merge_races', m.merge_races),
    ('unknown_main', m.unknown_main), ('remaining_guards', m.remaining_guards),
    ('branch_unknown_and_placeholder', m.branch_unknown_and_placeholder),
    ('pending_ready_and_merge_objects', m.pending_ready_and_merge_objects),
    ('safe_advance_recovery',m.safe_advance_recovery),
    ('recovery_rejections',m.recovery_rejections),
    ('metadata_after_public',m.metadata_after_public)]
for label, fn in tests:
    sys.stdout = types.SimpleNamespace(write=lambda s: None, flush=lambda: None)
    try:
        m.test(label, fn)
    finally:
        sys.stdout = real
    print(json.dumps(m.RESULTS[-1]), flush=True)
    m.archive_completed_group(out,m.b.RUNS,'replay_'+label)
result = dict(utc=datetime.now(timezone.utc).isoformat(),
    frozen_source_hashes_verified=True, groups=len(m.RESULTS),
    all_pass=all(x['status'] == 'PASS' for x in m.RESULTS),
    output_folder=str(out), live_provider_calls=0, local_Git_mutations=0)
(out / 'REPRODUCTION_RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
raise SystemExit(0 if result['all_pass'] else 1)
