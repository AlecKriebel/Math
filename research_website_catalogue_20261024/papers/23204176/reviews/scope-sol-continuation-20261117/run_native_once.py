"""One isolated, unmodified documented native route; data orchestration only."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import time

OWN = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23204176/reviews/scope-sol-continuation-20261117')
SOURCE = OWN.parent.parent / 'sources/archives/01-source-and-verification.zip.extracted'
RUN = OWN / 'native-isolated'
CACHE = OWN / 'tectonic-cache'
TMP = OWN / 'native-tmp'
OLD_CACHE = Path('/Users/alec/Library/Caches/Tectonic')


def profile(root):
    out = {}
    for p in [root] + sorted(root.rglob('*')):
        s = p.lstat()
        row = {'mode': oct(stat.S_IMODE(s.st_mode))}
        if stat.S_ISDIR(s.st_mode):
            row.update(kind='directory', empty=not any(p.iterdir()))
        else:
            assert stat.S_ISREG(s.st_mode), 'regular files only'
            data = p.read_bytes()
            row.update(kind='file', bytes=len(data), SHA256=hashlib.sha256(data).hexdigest())
        out[p.relative_to(root).as_posix()] = row
    return out


def write(name, value):
    p = OWN / name
    assert not p.exists()
    p.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


assert not RUN.exists() and not CACHE.exists() and not TMP.exists()
source_before = profile(SOURCE)
cache_before = profile(OLD_CACHE)
shutil.copytree(SOURCE, RUN, copy_function=shutil.copy2)
shutil.copytree(OLD_CACHE, CACHE, copy_function=shutil.copy2)
TMP.mkdir()
assert profile(RUN) == source_before
assert profile(CACHE) == cache_before
write('NATIVE_INPUT_GUARDS_BEFORE.json', {'source': source_before, 'isolated_input': profile(RUN), 'existing_cache': cache_before})
python = shutil.which('python3')
assert python and shutil.which('tectonic')
env = os.environ.copy()
env['TMPDIR'] = str(TMP)
env['TECTONIC_CACHE_DIR'] = str(CACHE)
argv = [python, 'reproduce.py']
start = datetime.datetime.now(datetime.timezone.utc).isoformat()
tick = time.monotonic()
with (OWN / 'NATIVE.stdout.txt').open('wb') as stdout, (OWN / 'NATIVE.stderr.txt').open('wb') as stderr:
    result = subprocess.run(argv, cwd=RUN, env=env, stdout=stdout, stderr=stderr, check=False)
elapsed = time.monotonic() - tick
after = {'source': profile(SOURCE), 'isolated_after': profile(RUN), 'existing_cache': profile(OLD_CACHE),
         'isolated_cache_after': profile(CACHE), 'temporary_after': profile(TMP)}
write('NATIVE_INPUT_GUARDS_AFTER.json', after)
receipt = {'started_UTC': start, 'finished_UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'elapsed_seconds': elapsed, 'argv': argv, 'cwd': str(RUN), 'exit_code': result.returncode, 'invocations': 1,
           'environment_overrides': {'TMPDIR': str(TMP), 'TECTONIC_CACHE_DIR': str(CACHE)},
           'unmodified_ordinary_route': True, 'source_guard_exact': after['source'] == source_before,
           'original_existing_cache_guard_exact': after['existing_cache'] == cache_before,
           'stdout_bytes': (OWN / 'NATIVE.stdout.txt').stat().st_size,
           'stderr_bytes': (OWN / 'NATIVE.stderr.txt').stat().st_size,
           'stdout_SHA256': hashlib.sha256((OWN / 'NATIVE.stdout.txt').read_bytes()).hexdigest(),
           'stderr_SHA256': hashlib.sha256((OWN / 'NATIVE.stderr.txt').read_bytes()).hexdigest(),
           'no_installs_interpreter_switch_repairs_retries': True,
           'finite_checks_and_TeX_build_do_not_certify_geometric_Hodge_input': True}
write('NATIVE_EXECUTION.json', receipt)
assert receipt['source_guard_exact'] and receipt['original_existing_cache_guard_exact']
print(json.dumps({'native_exit_code': result.returncode, 'elapsed_seconds': elapsed, 'stdout_bytes': receipt['stdout_bytes'], 'stderr_bytes': receipt['stderr_bytes']}))
