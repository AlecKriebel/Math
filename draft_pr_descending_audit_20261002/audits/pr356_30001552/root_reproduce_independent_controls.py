"""Root's complete native replay of three independent, pre-read control programs."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat
import subprocess
import sys

A = Path(__file__).resolve().parent
CAPTURE = A / 'root_replay_private' / 'independent_controls_001'
PY = '/opt/homebrew/bin/python3.11'

def now():
    return datetime.now(timezone.utc).isoformat()

def sha(data):
    return hashlib.sha256(data).hexdigest()

def inventory(base):
    out = {'files': {}, 'directories': {'.': stat.S_IMODE(base.stat().st_mode)}}
    for path in sorted(base.rglob('*')):
        assert not path.is_symlink(), str(path)
        name = path.relative_to(base).as_posix()
        mode = stat.S_IMODE(path.stat().st_mode)
        if path.is_file():
            data = path.read_bytes()
            out['files'][name] = {'bytes': len(data), 'sha256': sha(data), 'mode': mode}
        elif path.is_dir():
            out['directories'][name] = mode
        else:
            raise AssertionError('Nonregular namespace entry ' + name)
    return out

def write(name, data):
    target = CAPTURE / name
    assert not target.exists(), str(target)
    target.write_text(json.dumps(data, indent=2) + '\n')

assert not CAPTURE.exists(), 'Native capture label already exists; never overwrite it.'
CAPTURE.mkdir(parents=True)
jobs = [
    ('signed_graph', A / 'signed_graph_review', 'proposed_namespace/public/check_signed_graph.py',
     'proposed_namespace/public/SIGNED_GRAPH_CHECKS.json'),
    ('word_overlap', A / 'word_overlap_review', 'public/check_word_overlap.py',
     'public/WORD_OVERLAP_CHECKS.json'),
    ('definition_counterexamples', A / 'definition_counterexample_review', 'public/verify_constraints.py',
     'public/EXPECTED_CHECKS.json'),
]
write('root_runner_pin.json', {'utc': now(), 'path': str(Path(__file__).resolve()),
                             'sha256': sha(Path(__file__).read_bytes()),
                             'assertions_enabled': __debug__, 'python': PY})
assert __debug__
results = []
for name, namespace, relative_program, relative_expected in jobs:
    before = inventory(namespace)
    program = namespace / relative_program
    expected = namespace / relative_expected
    source = program.read_bytes()
    expected_bytes = expected.read_bytes()
    command = [PY, '-B', str(program)]
    pin = {'utc': now(), 'program': str(program), 'program_sha256': sha(source),
           'expected': str(expected), 'expected_sha256': sha(expected_bytes),
           'argv': command, 'cwd': str(A), 'namespace_before': before}
    write(name + '.before.json', pin)
    (CAPTURE / (name + '.executed_source.py')).write_bytes(source)
    started = now()
    result = subprocess.run(command, cwd=A, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            check=False)
    finished = now()
    (CAPTURE / (name + '.stdout')).write_bytes(result.stdout)
    (CAPTURE / (name + '.stderr')).write_bytes(result.stderr)
    after = inventory(namespace)
    record = {'name': name, 'started_utc': started, 'finished_utc': finished,
              'argv': command, 'cwd': str(A), 'exit_code': result.returncode,
              'program_sha256': sha(source), 'stdout_bytes': len(result.stdout),
              'stdout_sha256': sha(result.stdout), 'stderr_bytes': len(result.stderr),
              'stderr_sha256': sha(result.stderr),
              'entire_stdout_exact_expected_bytes': result.stdout == expected_bytes,
              'namespace_entire_files_directories_modes_unchanged': before == after,
              'namespace_file_count': len(before['files']),
              'namespace_directory_count': len(before['directories']),
              'program_and_expected_unchanged': program.read_bytes() == source and expected.read_bytes() == expected_bytes}
    write(name + '.after.json', {'receipt': record, 'namespace_after': after})
    assert result.returncode == 0 and result.stderr == b'', record
    assert result.stdout == expected_bytes and before == after, record
    assert record['program_and_expected_unchanged'], record
    results.append(record)
    print(json.dumps(record), flush=True)
receipt = {'utc': now(), 'status': 'PASS_THREE_WHOLE_NATIVE_INDEPENDENT_CONTROL_OUTPUTS',
           'root_runner_sha256': sha(Path(__file__).read_bytes()),
           'capture': str(CAPTURE.relative_to(A)), 'runs': results,
           'scope': 'Supplemental finite controls; mathematical universal proofs were read separately. No priority conclusion or historical source-five replay.'}
assert not (A / 'ROOT_INDEPENDENT_CONTROLS_REPLAY.json').exists()
(A / 'ROOT_INDEPENDENT_CONTROLS_REPLAY.json').write_text(json.dumps(receipt, indent=2) + '\n')
