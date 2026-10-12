#!/usr/bin/env python3
"""Close only this adversary's artifacts, no candidate execution or mutation."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
F = Path(__file__).absolute().parent
R = F.parent.parents[2]
def sha(raw):
    return hashlib.sha256(raw).hexdigest()
def require(ok, message):
    if not ok:
        raise ValueError(message)
def regular(p):
    require(not p.is_symlink() and all(not q.is_symlink() for q in p.parents)
            and stat.S_ISREG(p.stat().st_mode), 'regular nonsymlink file')
    return p.read_bytes()
require(F.name == 'current_source_adversary_family' and R == Path('/Users/alec/Documents/Math'), 'exact own root')
require(not (F / 'SELF_MANIFEST.json').exists(), 'never overwrite closure')
cap = json.loads(regular(F / 'OWN_STATIC_INSPECTION_ACTUAL_CAPTURE/CAPTURE.json'))
require(cap['actual_execution'] is True and cap['completed'] is True and type(cap['pid']) is int
        and cap['pid'] == 62163 and type(cap['exit_code']) is int and cap['exit_code'] == 0
        and cap['source_unchanged'] is True and cap['operator_unchanged'] is True, 'genuine own static capture')
for name, key, original in [('PRELAUNCH_SOURCE.py', 'source_sha256', 'inspect_static_source.py'),
                           ('PRELAUNCH_OPERATOR.py', 'operator_sha256', 'capture_own_static_inspection.py')]:
    raw = regular(F / 'OWN_STATIC_INSPECTION_ACTUAL_CAPTURE' / name)
    require(sha(raw) == cap[key] and raw == regular(F / original), 'own prelaunch exact source')
for channel in ['stdout', 'stderr']:
    raw = regular(F / 'OWN_STATIC_INSPECTION_ACTUAL_CAPTURE' / cap[channel]['path'])
    require(len(raw) == cap[channel]['bytes'] and sha(raw) == cap[channel]['sha256'], 'own complete exact stream')
require(not regular(F / 'OWN_STATIC_INSPECTION_ACTUAL_CAPTURE/stderr.bin'), 'own empty stderr')
inputs = json.loads(regular(F / 'STATIC_INPUT_MANIFEST.json'))
for row in inputs['static_input_files']:
    p = R / row['path']
    raw = regular(p)
    require(len(raw) == row['bytes'] and sha(raw) == row['sha256']
            and format(stat.S_IMODE(p.stat().st_mode), '05o') == row['full_stat_S_IMODE'], 'input changed before own closure: ' + row['path'])
for tree in inputs['exact_closed_trees']:
    root = R / tree['root']
    require(root.is_dir() and not root.is_symlink()
            and format(stat.S_IMODE(root.stat().st_mode), '05o') == tree['root_full_stat_S_IMODE'], 'closed tree root')
    actual_files, actual_dirs = [], []
    for p in sorted(root.rglob('*')):
        require(not p.is_symlink(), 'no symlink in closed input tree')
        mode = p.stat().st_mode
        row = dict(path=p.relative_to(root).as_posix(), full_stat_S_IMODE=format(stat.S_IMODE(mode), '05o'))
        if stat.S_ISREG(mode):
            actual_files.append(row)
        else:
            require(stat.S_ISDIR(mode), 'no special input tree member')
            actual_dirs.append(row)
    require(actual_files == tree['files'] and actual_dirs == tree['directories'], 'closed input tree unchanged')
require(not (F.parent / 'reviewed_candidate').exists() and not (F.parent / 'reviewed_candidate').is_symlink(), 'candidate still absent at source-only closure')
now = dt.datetime.now(dt.timezone.utc).isoformat()
with (F / 'RESEARCH_LOG.md').open('a') as handle:
    handle.write('\n- ' + now + ' — Closed independent source preparation safety review after full source reading and actual static evidence inspection. No mandatory repair found; optional certificate line strictness is not a gate. Own actual capture PID62163, exit0, 1830 mechanical predicates, 280 individually pinned inputs and13 exact trees. Source review100%; project discovery0%. ROOT prerequisites/freeze/NEW whole-current review remain PENDING. All input bytes/full modes/topology unchanged at closure; no candidate execution or native/Git/remote mutation. Actual own closure PID' + str(os.getpid()) + '.\n')
names, directories = [], []
for p in sorted(F.rglob('*')):
    require(not p.is_symlink(), 'own no symlink')
    mode = p.stat().st_mode
    name = p.relative_to(F).as_posix()
    if stat.S_ISREG(mode):
        p.chmod(0o444)
        names.append(name)
    else:
        require(stat.S_ISDIR(mode), 'own no special member')
        directories.append(name)
wanted = {q.as_posix() for name in names for q in PurePosixPath(name).parents if q.as_posix() != '.'}
require(set(directories) == wanted, 'own exact nonempty topology')
files = []
for name in names:
    p = F / name
    raw = regular(p)
    require(stat.S_IMODE(p.stat().st_mode) == 0o444 and len(raw) < 100 * 1024 * 1024, 'own literal full0444 size')
    files.append(dict(path=name, bytes=len(raw), sha256=sha(raw), full_stat_S_IMODE='00444',
                      classification='first_party_independent_review_artifact', novelty_claim=False))
manifest = dict(schema='PR43_NEW_SOURCE_ADVERSARY_SELF_ONLY_CLOSURE_v1', utc=now, actual_closure_pid=os.getpid(),
      files_count=len(files), files=files, self_excluded=['SELF_MANIFEST.json'], manifest_full_stat_S_IMODE='00444',
      directories=[dict(path=name, full_stat_S_IMODE=format(stat.S_IMODE((F / name).stat().st_mode), '05o')) for name in directories],
      input_manifest_sha256=sha(regular(F / 'STATIC_INPUT_MANIFEST.json')), foreign_copied_members=[],
      attributed_input_bytes_are_not_own_authored_science=True, candidate_source_import_compile_execution=False,
      ROOT_approval_or_actual_freeze_attested=False, NEW_whole_current_gate='PENDING', current_whole_verdict=None,
      source_review_completion_percent=100, project_discovery_percent=0)
with (F / 'SELF_MANIFEST.json').open('x') as handle:
    json.dump(manifest, handle, indent=2, ensure_ascii=False, allow_nan=False)
    handle.write('\n')
(F / 'SELF_MANIFEST.json').chmod(0o444)
require({p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_file()} == set(names) | {'SELF_MANIFEST.json'}, 'exact own self-only file closure')
require(stat.S_IMODE((F / 'SELF_MANIFEST.json').stat().st_mode) == 0o444, 'own manifest full0444')
for row in files:
    raw = regular(F / row['path'])
    require(len(raw) == row['bytes'] and sha(raw) == row['sha256'], 'final own byte pin')
print(json.dumps(dict(status='CLOSED_NEW_SOURCE_ONLY_ADVERSARY_NO_MANDATORY_REPAIR', actual_closure_pid=os.getpid(),
      files_count=len(files), self_manifest_sha256=sha(regular(F / 'SELF_MANIFEST.json')),
      verdict_sha256=sha(regular(F / 'VERDICT.json')), source_review_sha256=sha(regular(F / 'SOURCE_SAFETY_REVIEW.md')),
      NEW_whole_current_gate='PENDING', actual_freeze_certified=False), indent=2))
