"""Read-only common checks for PR359's exact-live and actual-merge gates.

Only the caller's new evidence directory receives writes. Complete output
comparisons supplement the separately reviewed universal analytical proof.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, stat, subprocess, zipfile

A = Path(__file__).resolve().parent
P = A.parents[1]
R = P.parent
Q = 'unsolved_math_prioritization/QUEUE.md'
PROBLEM = b'30001370'
PY = '/opt/homebrew/bin/python3.11'
sha = lambda b: hashlib.sha256(b).hexdigest()
load = lambda p: json.loads(p.read_bytes())
utc = lambda: datetime.now(timezone.utc).isoformat()


class Capture:
    def __init__(self, purpose):
        self.directory = A/'root_replay_private'/(purpose+'_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f'))
        self.directory.mkdir(parents=True, exist_ok=False)
        self.entries = []

    def run(self, label, args, cwd=R, ok=(0,)):
        args = [str(x) for x in args]
        assert not (self.directory/(label+'.json')).exists()
        started = utc()
        code_pins = [{'path': s, 'bytes': Path(s).stat().st_size, 'sha256': sha(Path(s).read_bytes())}
                     for s in args if s.endswith('.py') and Path(s).is_file()]
        z = subprocess.run(args, cwd=cwd, capture_output=True,
                           env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1',
                                    GIT_OPTIONAL_LOCKS='0', GIT_NO_LAZY_FETCH='1'))
        streams = {}
        for name, b in [('stdout', z.stdout), ('stderr', z.stderr)]:
            f = self.directory/(label+'.'+name)
            f.write_bytes(b)
            streams[name] = {'path': str(f.relative_to(A)), 'bytes': len(b), 'sha256': sha(b)}
        e = {'label': label, 'argv': args, 'cwd': str(cwd), 'started_utc': started,
             'finished_utc': utc(), 'exit_code': z.returncode, 'streams': streams,
             'actual_observed_pre_execution_programs': code_pins}
        self.entries.append(e)
        (self.directory/(label+'.json')).write_text(json.dumps(e, indent=2)+'\n')
        assert z.returncode in ok, (label, z.returncode, z.stderr.decode(errors='replace'))
        return z

    def git(self, *args):
        z = self.run('git_'+str(len(self.entries)), ['git', *args])
        assert not z.stderr
        return z.stdout


def current_clearance():
    c = load(A/'PUBLISHING_CLEARANCE.json')
    assert c['status'] == 'READY_AFTER_TWO_SEQUENTIAL_FRESH_PREPRINT_REVIEWS'
    assert c['second_review_mandatory_findings'] == 0 and len(c['fresh_reviews']) == 2
    pins = {e['path']: {'bytes': e['bytes'], 'sha256': e['sha256']}
            for e in c['sealed_submission_files']}
    assert len(pins) == 4
    for name, pin in pins.items():
        b = (A/'preprint'/name).read_bytes()
        assert {'bytes': len(b), 'sha256': sha(b)} == pin
    for n in (1, 2):
        v = load(A/f'ROOT_PREPRINT_REVIEW0{n}_VERIFICATION.json')
        assert v['mandatory_findings'] == 0 and v['closed_namespace_unchanged']
        assert v['whole_verifier_output_compared'] and v['all_mandatory_submission_findings_resolved']
        assert {e['path']: {'bytes': e['bytes'], 'sha256': e['sha256']}
                for e in v['sealed_submission_files']} == pins
        assert sha((A/f'preprint_review_0{n}'/v['review_seal_path']).read_bytes()) == v['review_seal_sha256']
    return c


def inventory(root):
    entries = {}
    for p in sorted(root.rglob('*')):
        assert not p.is_symlink() and (p.is_file() or p.is_dir())
        e = {'type': 'file' if p.is_file() else 'directory', 'mode': stat.S_IMODE(p.stat().st_mode)}
        if p.is_file():
            b = p.read_bytes()
            e.update(bytes=len(b), sha256=sha(b))
        entries[p.relative_to(root).as_posix()] = e
    return entries


def package_replay(capture):
    scratch = capture.directory/'zip_scratch'
    scratch.mkdir()
    with zipfile.ZipFile(A/'preprint/basin-boundaries-verification.zip') as z:
        members = z.infolist()
        assert len(members) == 74 and len({m.filename for m in members}) == 74
        for m in members:
            p = Path(m.filename)
            assert not m.is_dir() and not p.is_absolute() and '..' not in p.parts
            assert p.parts[0] == 'basin-boundaries-verification'
            assert ((m.external_attr >> 16) & 0o170000) in (0, 0o100000)
            f = scratch/p
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_bytes(z.read(m))
    t = scratch/'basin-boundaries-verification'
    before = inventory(t)
    assert (t/'paper/common_basin_boundaries.tex').read_bytes() == (A/'preprint/common_basin_boundaries.tex').read_bytes()
    assert (t/'paper/zenodo-deposit.json').read_bytes() == (A/'preprint/zenodo-deposit.json').read_bytes()
    original = load(A/'snapshot_manifest.json')
    for e in original['files']:
        if e['path'] == Q:
            continue
        rel = Path(e['path']).relative_to('problems/30001370_basin_boundaries')
        b = (t/'candidate'/rel).read_bytes()
        assert len(b) == e['bytes'] and sha(b) == e['sha256']
    results = []
    saved_runs = load(A/'METADATA_REPAIR_RECEIPT.json')['complete_runs']
    reviewed_outputs = load(A/'ROOT_PREPRINT_PACKAGE_OUTPUT_COMPARISON.json')
    assert reviewed_outputs['status'] == 'PASS_BOTH_REVIEWERS_CURRENT_FULL_PACKAGE_OUTPUTS'
    assert reviewed_outputs['submission_files'] == load(A/'METADATA_REPAIR_RECEIPT.json')['submission_files']
    for label, args in [('default', []), ('full', ['--full']), ('public_priority', ['--public-only'])]:
        program = t/'audits/priority/verify_namespace.py' if label == 'public_priority' else t/'verify_supplement.py'
        z = capture.run('package_'+label, [PY, '-B', program, *args], cwd=t)
        expected = (A/'preprint/private/metadata_repair_001'/(label+'.stdout')).read_bytes()
        old = next(e for e in saved_runs if e['label'] == label)
        assert len(expected) == old['native']['stdout_bytes'] and sha(expected) == old['native']['stdout_sha256']
        assert z.stdout == expected and not z.stderr and json.loads(z.stdout) == old['complete_stdout']
        for review in reviewed_outputs['reviews']:
            record = review['replays'][label]
            assert record['exit_code'] == 0
            assert z.stdout == Path(record['stdout_path']).read_bytes()
            assert Path(record['stderr_path']).read_bytes() == b''
        results.append({'label': label, 'bytes': len(z.stdout), 'sha256': sha(z.stdout), 'entire_saved_output_equal': True})
    assert [r['review'] for r in reviewed_outputs['reviews']] == [1, 2]
    assert inventory(t) == before
    return {'ordinary_zip_files': 74, 'payload_files': 73, 'complete_runs': results,
            'full_package_outputs_compared_to_both_reviewers': True,
            'relocated_package_unchanged': True}


def closed_reviews(capture):
    root_math = load(A/'ROOT_FAMILY_CLOSURE_VERIFICATION.json')
    specs = []
    for e in root_math['families']:
        specs.append((e['family'], e['native_run']['argv'],
                      A/'root_replay_private/family_closures_001'/(e['family']+'.stdout'),
                      e['seal_path'], e['seal_sha256']))
    priority = load(A/'ROOT_PRIORITY_VERIFICATION.json')
    e = next(e for e in priority['runs'] if e['label'] == 'full')
    specs.append(('priority_review', e['native']['argv'],
                  A/'root_replay_private/priority_closure_001/full.stdout',
                  'CLOSURE.json', priority['review_closure_sha256']))
    for n in (1, 2):
        e = load(A/f'ROOT_PREPRINT_REVIEW0{n}_VERIFICATION.json')
        full = next(r for r in e['captures'] if '--public-only' not in r['argv'] and any(str(x).endswith('verify_review.py') for x in r['argv']))
        specs.append((f'preprint_review_0{n}', full['argv'],
                      Path(full['stdout_path']) if 'stdout_path' in full else A/'root_replay_private'/f'preprint_review0{n}_closed_001/full.stdout',
                      e['review_seal_path'], e['review_seal_sha256']))
    results = []
    for name, argv, output, seal, seal_sha in specs:
        namespace = A/name
        assert sha((namespace/seal).read_bytes()) == seal_sha
        before = inventory(namespace)
        z = capture.run('closed_'+name, argv, cwd=A)
        assert not z.stderr and z.stdout == output.read_bytes(), (name, str(output))
        assert inventory(namespace) == before, name
        results.append({'family': name, 'seal_sha256': seal_sha,
                        'whole_files': sum(e['type'] == 'file' for e in before.values()),
                        'whole_output_identical': True, 'closed_namespace_unchanged': True})
    for n in (1, 2):
        c = load(A/f'ROOT_PREPRINT_REVIEW0{n}_CONTROL_REPRODUCTION.json')
        v = A/f'preprint_review_0{n}'
        before = inventory(v)
        controls = c.get('control_runs', [c])
        for i, control in enumerate(controls):
            expected = Path(control['stdout_path']) if 'stdout_path' in control else A/'root_replay_private'/f'preprint_review0{n}_closed_001/controls.stdout'
            z = capture.run('fresh_adversary_controls_'+str(n)+'_'+str(i), control['execution']['argv'], cwd=A)
            assert z.stdout == expected.read_bytes() and not z.stderr
            assert json.loads(z.stdout) == control['complete_stdout']
        assert inventory(v) == before
    return results


def queue_binding(capture, base, target):
    old = capture.git('show', f'{base}:{Q}').splitlines(keepends=True)
    new = capture.git('show', f'{target}:{Q}').splitlines(keepends=True)
    assert len(old) == len(new)
    changes = [i for i, (a, b) in enumerate(zip(old, new)) if a != b]
    assert len(changes) == 1
    i = changes[0]
    before, after = old[i].split(b'|'), new[i].split(b'|')
    assert len(before) == len(after)
    assert before[2].strip().split(b' / ')[0] == PROBLEM
    assert [before[j].strip() for j in (8, 9)] == [b'queued', b'0/5']
    assert [after[j].strip() for j in (8, 9)] == [b'claimed_solved', b'3/5']
    assert [j for j, (a, b) in enumerate(zip(before, after)) if a != b] == [8, 9, 11]
    repaired = load(A/'queue_repair_receipt.json')
    assert new[i].decode() == repaired['new_row'] and old[i].decode() == repaired['old_row']
    assert after[11].strip().endswith(b'bounded priority and two fresh AI preprint reviews passed (unrefereed).')
    return {'queue_physical_line': i+1, 'queue_only_pipe_cells': [8, 9, 11], 'all_other_queue_bytes_equal': True}
