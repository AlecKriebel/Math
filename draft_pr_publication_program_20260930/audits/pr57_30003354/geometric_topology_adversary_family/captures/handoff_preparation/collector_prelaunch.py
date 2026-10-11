"""Own/capture one explicitly named family operator. No ROOT helpers are executed."""
import hashlib
import json
import os
import stat
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PYTHON = '/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'


def utc(): return datetime.now(timezone.utc).isoformat()
def sha(data): return hashlib.sha256(data).hexdigest()


def seal_source_index():
    """Collector's final administrative action. No scientific/ROOT operator runs."""
    assert not (ROOT / 'SOURCE.json').exists()
    with (ROOT / 'RESEARCH_LOG.md').open('a') as log:
        log.write(f'- {utc()} — Family mathematical audit and lean evidence handoff complete '
                  f'(sealing collector PID {os.getpid()}); universal derivation passes exact '
                  'scope, five exact controls, one preserved dependency failure. Audit 100%. '
                  'ROOT closure/readback and any acceptance/publication remain pending; '
                  'no future custody facts inferred.\n')
    files = sorted(p for p in ROOT.rglob('*') if p.is_file())
    dirs = [ROOT] + sorted(p for p in ROOT.rglob('*') if p.is_dir())
    assert not any(p.is_symlink() for p in files + dirs)
    assert not any(p.name.endswith(('.pdf', '.png', '.layout.txt')) for p in files)
    for p in files: p.chmod(0o444)
    for p in dirs: p.chmod(0o755)
    entries = []
    for p in files:
        data = p.read_bytes()
        entries.append({'relative_path': str(p.relative_to(ROOT)), 'bytes': len(data),
                        'sha256': sha(data), 'full_mode_07777': format(stat.S_IMODE(p.stat().st_mode), '04o')})
    index = {'schema': 'pr57-geometric-fixed-source-index/v1', 'utc': utc(),
             'sealing_collector_pid': os.getpid(),
             'original_head': '4ecc453d6f9ec2e64cdb2d4b41c018fffbe85b29',
             'family_absolute_path': str(ROOT), 'files': entries,
             'directories': [{'relative_path': '.' if p == ROOT else str(p.relative_to(ROOT)),
                              'full_mode_07777': format(stat.S_IMODE(p.stat().st_mode), '04o')} for p in dirs],
             'self_indexed': False, 'private_primary_cache_required': False,
             'whole_public_primary_bodies_redistributed': False,
             'ROOT_helpers_executed': False, 'ROOT_closed_or_readback_claimed': False}
    with (ROOT / 'SOURCE.json').open('x') as f:
        f.write(json.dumps(index, indent=2, sort_keys=True) + '\n')
    (ROOT / 'SOURCE.json').chmod(0o444)
    index_data = (ROOT / 'SOURCE.json').read_bytes()
    return {'SOURCE_bytes': len(index_data), 'SOURCE_sha256': sha(index_data),
            'indexed_files': len(files), 'total_files_including_SOURCE': len(files) + 1,
            'directory_count': len(dirs), 'ROOT_helpers_executed': False}


def main():
    tag, name = sys.argv[1:]
    assert tag in ('primary_read', 'geometric_controls', 'geometric_controls_v2', 'handoff_preparation')
    assert name in ('read_primary_sources.py', 'geometric_controls.py', 'geometric_controls_v2.py', 'prepare_handoff.py')
    capture = ROOT / 'captures' / tag
    capture.mkdir(parents=True, exist_ok=False)
    operator = ROOT / name
    source = operator.read_bytes(); collector = Path(__file__).read_bytes()
    (capture / 'operator_prelaunch.py').write_bytes(source)
    (capture / 'collector_prelaunch.py').write_bytes(collector)
    argv = [PYTHON, str(operator)]; started = utc()
    with (capture / 'stdout.bin').open('wb') as stdout, (capture / 'stderr.bin').open('wb') as stderr:
        child = subprocess.Popen(argv, cwd=ROOT, stdout=stdout, stderr=stderr)
        metadata = {'collector_pid': os.getpid(), 'owned_child_pid': child.pid,
                    'started_utc': started, 'argv': argv, 'cwd': str(ROOT),
                    'operator_sha256_prelaunch': sha(source), 'collector_sha256_prelaunch': sha(collector),
                    'root_helpers_executed': False, 'root_closed': False}
        (capture / 'PRELAUNCH.json').write_text(json.dumps(metadata, indent=2) + '\n')
        code = child.wait()
    metadata.update(ended_utc=utc(), exit_code=code, operator_sha256_after=sha(operator.read_bytes()),
                    collector_sha256_after=sha(Path(__file__).read_bytes()))
    for stream in ('stdout', 'stderr'):
        data = (capture / (stream + '.bin')).read_bytes()
        metadata[stream + '_bytes'] = len(data); metadata[stream + '_sha256'] = sha(data)
    (capture / 'CAPTURE.json').write_text(json.dumps(metadata, indent=2) + '\n')
    if tag == 'handoff_preparation':
        assert code == 0
        metadata['final_administrative_seal'] = seal_source_index()
    print(json.dumps(metadata, indent=2, sort_keys=True)); print((capture / 'stdout.bin').read_text())
    sys.exit(code)


if __name__ == '__main__': main()
