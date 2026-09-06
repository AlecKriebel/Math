#!/usr/bin/env python3
"""Independent audit orchestration. Never modifies the preserved source."""
import datetime, hashlib, json, os, pathlib, shlex, shutil, subprocess, sys, tarfile, time, zipfile

HERE = pathlib.Path(__file__).resolve().parent
SOURCE = HERE.parent / 'source_snapshot'
SCRATCH = HERE / 'scratch'
LOGS = HERE / 'logs'
REPO = pathlib.Path('/Users/alec/Documents/Math')
PROJECT = 'maximally_collective_stable_turing_patterns_binary_complex_mass_action_networks'
REV = '6f68ad3e795c'
ENV = os.environ.copy()
ENV.update(PYTHONOPTIMIZE='0', PYTHONHASHSEED='0', MPLBACKEND='Agg', SOURCE_DATE_EPOCH='1787443200', FORCE_SOURCE_DATE='1', TZ='UTC', LC_ALL='C', OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1', NUMEXPR_NUM_THREADS='1')
ENV['PATH'] = str(SCRATCH / 'toolchain/TinyTeX/bin/universal-darwin') + ':/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin'
ENV['PYTHONPATH'] = str(SCRATCH / 'pypdf')

def run(label, args, cwd=SOURCE, expected=0, env=None, timeout=1200):
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    before = time.monotonic()
    log = LOGS / (label + '.log')
    try:
        with log.open('w') as out:
            proc = subprocess.run(args, cwd=cwd, env=env or ENV, stdout=out, stderr=subprocess.STDOUT, timeout=timeout)
        status = proc.returncode
    except subprocess.TimeoutExpired:
        status = 'TIMEOUT'
    entry = dict(id=label, started=started, command=shlex.join(str(x) for x in args), cwd=str(cwd), status=status, expected=expected, runtime_seconds=round(time.monotonic()-before, 3), log=str(log.relative_to(HERE)))
    with (HERE / 'COMMAND_RESULTS.jsonl').open('a') as f: f.write(json.dumps(entry)+'\n')
    print(json.dumps(entry), flush=True)
    return status

def verify_manifest(base, manifest):
    seen = set()
    for line in (base/manifest).read_text().splitlines():
        digest, rel = line.split(None, 1)
        rel = rel.strip().removeprefix('*')
        target=(base/rel).resolve()
        assert target.is_relative_to(base.resolve()), rel
        assert rel not in seen, rel
        seen.add(rel)
        assert hashlib.sha256(target.read_bytes()).hexdigest()==digest, rel
    return len(seen)

def setup():
    print('source_manifest_entries',verify_manifest(SOURCE,'release/sha256_manifest.txt'))
    print('public_manifest_entries',verify_manifest(SOURCE/'public/repository','sha256_manifest.txt'))
    print('bundle_hashes',verify_manifest(SOURCE,'release/BUNDLE_SHA256.txt'))
    archive=SCRATCH/'fresh_archive.tar'
    with archive.open('wb') as f:
        subprocess.run(['git','archive',REV,PROJECT],cwd=REPO,stdout=f,check=True)
    archive_root=SCRATCH/'fresh_archive'
    archive_root.mkdir(exist_ok=True)
    with tarfile.open(archive) as t: t.extractall(archive_root)
    archived=archive_root/PROJECT
    fresh={str(p.relative_to(archived)):hashlib.sha256(p.read_bytes()).hexdigest() for p in archived.rglob('*') if p.is_file()}
    snapshot={str(p.relative_to(SOURCE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in SOURCE.rglob('*') if p.is_file()}
    assert fresh == snapshot
    listed={line.split(None,1)[1].strip().removeprefix('./') for line in (archived/'release/sha256_manifest.txt').read_text().splitlines()}
    assert set(fresh)-{'release/sha256_manifest.txt'}==listed
    print('fresh_archive_complete_exact_match',len(fresh),len(listed))
    for bundle in (SOURCE/'release/BUNDLE_SHA256.txt').read_text().splitlines():
        rel=bundle.split(None,1)[1]
        with zipfile.ZipFile(SOURCE/rel) as z:
            assert z.testzip() is None
            for n in z.namelist():
                assert not n.startswith('/') and '..' not in pathlib.PurePosixPath(n).parts
        print('bundle_zip_integrity',rel)
    for name,origin in [('full',SOURCE),('portable',SOURCE/'public/repository'),('minimal',SOURCE/'external_audit/minimal_verifier')]:
        dst=SCRATCH/name
        if not dst.exists(): shutil.copytree(origin,dst)
    print('INTEGRITY_AND_COPIES_PASS')

def verifiers():
    root=SCRATCH/'full'
    modules=sorted(p for p in (root/'independent_verifier').glob('*.py') if p.name not in {'common.py','core.py','pareto_core.py','stable_core.py'})
    assert len(modules)==39
    for p in modules:
        assert run('normal_'+p.stem,['python',str(p)],cwd=root)==0
        assert run('optimized_'+p.stem,['python','-O',str(p)],cwd=root,expected=1)!=0
        assert 'requires assertions' in (LOGS/('optimized_'+p.stem+'.log')).read_text()
    print('ALL_39_NORMAL_AND_OPTIMIZED_PASS')

if __name__=='__main__':
    SCRATCH.mkdir(exist_ok=True); LOGS.mkdir(exist_ok=True)
    action=sys.argv[1]
    if action=='setup': setup()
    elif action=='verifiers': verifiers()
    elif action=='replays':
        run('pinned_toolchain',['bash','environment/check_toolchain.sh'],SCRATCH/'full')
        run('tests',['python','-m','pytest','-q','computation/tests'],SCRATCH/'full')
        run('minimal_replay',['bash','replay.sh'],SCRATCH/'minimal')
        run('portable_full_replay',['bash','replay.sh'],SCRATCH/'portable')
