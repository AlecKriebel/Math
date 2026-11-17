"""Owned custody launcher: one unchanged ordinary finite-incidence run only."""
from pathlib import Path
import datetime, hashlib, json, os, stat, subprocess, sys

OWN = Path(__file__).resolve().parent
SOURCE = OWN.parents[1] / 'sources'
TREE = SOURCE / 'published-source/container-001/tree'
GUARDS = OWN / 'INITIAL_SOURCE_GUARDS.json'
PROGRAM = TREE / 'verification/verify_plane32.py'
PYTHON = '/opt/homebrew/bin/python3.11'
CACHE = Path('/Users/alec/Documents/Math/openai_wreath_planar_consequences/sources/family197')
EXPECTED = {
    'random.tex': 'bb172b92ba622e262c2bf124e70c3cd55922200083c09db658615759b81323c4',
    'patterns.tex': '20c6cc1f3fb035150831e5091c98313f04e7a9d8aaa347507020b176394ed4ea',
    'planar.tex': 'e3a1a4e23dd6871a9746ffde05d32297e695f3167b8efa0f0a4cad5da8c9ae6b',
    'topology.tex': 'f1e50e15464174e5ef32d9dfe966fe7e12b4dd480af60a27228d901cc159b1b0',
    'algebra.tex': '71fe26eab4e6a01564a687c522bbceb8923182c0201af9685eac84d9f86a141f',
    'assembly.tex': '3987e23ea7c5c8d217ca539d5a307d59f8eac5b8381a0afe411125e57f0bee4a',
}

def pin(path):
    s = path.lstat()
    if not stat.S_ISREG(s.st_mode):
        raise ValueError('Not a regular file: ' + str(path))
    b = path.read_bytes()
    return {'bytes': len(b), 'SHA256': hashlib.sha256(b).hexdigest(), 'mode': stat.S_IMODE(s.st_mode)}

def source_guard():
    g = json.loads(GUARDS.read_text())
    actual_files, actual_dirs = {}, {}
    for base, dirs, files in os.walk(SOURCE, followlinks=False):
        for name in dirs:
            p = Path(base) / name
            if p.is_symlink():
                raise ValueError('Source symlink')
            actual_dirs[p.relative_to(SOURCE).as_posix()] = stat.S_IMODE(p.stat().st_mode)
        for name in files:
            p = Path(base) / name
            actual_files[p.relative_to(SOURCE).as_posix()] = pin(p)
    if actual_files != {r['path']: {k:r[k] for k in ('bytes','SHA256','mode')} for r in g['files']}:
        raise ValueError('Source file guard changed')
    if actual_dirs != {r['path']:r['mode'] for r in g['directories']}:
        raise ValueError('Source directory guard changed')
    return {'regular_files':len(actual_files), 'child_directories':len(actual_dirs), 'all_initial_buffers_modes_topology_exact':True}

def main():
    names = ['plane32.stdout', 'plane32.stderr', 'plane32.exit', 'PLANE32_RUN.json']
    if any((OWN / n).exists() for n in names):
        raise FileExistsError('Retain prior evidence; this launcher has one invocation only')
    before = source_guard()
    primary = {}
    for name, digest in EXPECTED.items():
        p = CACHE / name
        actual = pin(p)
        if actual['SHA256'] != digest:
            raise ValueError('Primary pin mismatch: ' + name)
        primary[str(p)] = actual
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    command = [PYTHON, str(PROGRAM)]
    with (OWN / names[0]).open('xb') as out, (OWN / names[1]).open('xb') as err:
        completed = subprocess.run(command, cwd=OWN, env=env, stdout=out, stderr=err, check=False)
    with (OWN / names[2]).open('x') as f:
        f.write(str(completed.returncode) + '\n')
    after = source_guard()
    receipt = {'started_UTC':start, 'finished_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'command':command, 'cwd':str(OWN), 'launcher_python':sys.version,
               'environment_delta':{'PYTHONDONTWRITEBYTECODE':'1'}, 'exit':completed.returncode,
               'program':{'path':str(PROGRAM), **pin(PROGRAM)},
               'input':{'path':str(TREE/'data/plane32_incidence.json'), **pin(TREE/'data/plane32_incidence.json')},
               'primary_files':primary, 'source_before':before, 'source_after':after,
               'stdout':pin(OWN/names[0]), 'stderr':pin(OWN/names[1]),
               'scope':'One finite field/projective incidence/Fano/inverse-pairing certificate. No matching, presentation, group multiplication, asphericity, or priority certification.'}
    with (OWN / names[3]).open('x') as f:
        json.dump(receipt,f,indent=2); f.write('\n')
    print(json.dumps({'native_exit':completed.returncode, 'source_unchanged':True, 'receipt':names[3]}))

if __name__ == '__main__':
    main()
