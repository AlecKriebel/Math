"""One unmodified native-documented atomic inner route, isolated in own lane."""
import datetime, hashlib, json, os, pathlib, platform, shutil, stat, subprocess, sys, time
OWN = pathlib.Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23202994/reviews/scope-sol-continuation-20261117')
SOURCE = OWN / 'primary/preprints/An-atomic-certificate-for-triangular-lattice-universal-optimality-September-26-2026'
COPY = OWN / 'run-atomic'
assert not COPY.exists()
assert sys.flags.optimize == 0
shutil.copytree(SOURCE, COPY, copy_function=shutil.copy2)
def guard(root):
    files, directories = {}, {}
    for here, dirs, names in os.walk(root, followlinks=False):
        hp = pathlib.Path(here)
        for name in dirs:
            p = hp / name
            assert p.is_dir() and not p.is_symlink()
            directories[p.relative_to(root).as_posix()] = format(stat.S_IMODE(p.stat().st_mode), '04o')
        for name in names:
            p = hp / name
            assert p.is_file() and not p.is_symlink()
            raw = p.read_bytes()
            files[p.relative_to(root).as_posix()] = dict(bytes=len(raw), SHA256=hashlib.sha256(raw).hexdigest(), mode=format(stat.S_IMODE(p.stat().st_mode), '04o'))
    return dict(root_mode=format(stat.S_IMODE(root.stat().st_mode), '04o'), files=files, directories=directories)
before = guard(COPY)
assert before == guard(SOURCE)
assert before['files']['verification/check_certificate.py']['SHA256'] == '5689152e970b652a8e40c3c120eda3b45320c8745968a5cb416fa9b9dbdc5385'
argv = [sys.executable, '-I', '-B', 'verification/check_certificate.py']
start = datetime.datetime.now(datetime.timezone.utc).isoformat()
tick = time.monotonic()
with (OWN / 'ATOMIC_RUN.stdout').open('xb') as out, (OWN / 'ATOMIC_RUN.stderr').open('xb') as err:
    completed = subprocess.run(argv, cwd=COPY, stdout=out, stderr=err, timeout=60, check=False)
elapsed = time.monotonic() - tick
end = datetime.datetime.now(datetime.timezone.utc).isoformat()
after = guard(COPY)
receipt = dict(schema='row190-single-native-inner-route-v1', argv=argv, cwd=str(COPY), start_UTC=start, end_UTC=end, elapsed_seconds=elapsed, exit_code=completed.returncode, stdout_bytes=(OWN/'ATOMIC_RUN.stdout').stat().st_size, stderr_bytes=(OWN/'ATOMIC_RUN.stderr').stat().st_size, interpreter=sys.executable, Python=sys.version, platform=platform.platform(), flags=str(sys.flags), optimization=0, entrypoint_personally_read_full=True, called_project_bodies='None; checker imports only Python standard-library math; all local definitions read in full', native_selection='Exact atomic inner command called by native reproducibility/reproduce.py --run-upstream; -I -B preserved; no optional TeX/Git/flint/Lean route', before=before, after=after, input_namespace_unchanged=before==after)
with (OWN / 'ATOMIC_RUN_RECEIPT.json').open('x') as stream:
    json.dump(receipt, stream, indent=2)
    stream.write('\n')
print(json.dumps({k:receipt[k] for k in ('exit_code','elapsed_seconds','stdout_bytes','stderr_bytes','input_namespace_unchanged')}))
assert before == after
