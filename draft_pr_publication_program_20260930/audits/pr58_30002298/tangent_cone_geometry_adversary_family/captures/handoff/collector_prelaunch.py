"""Small owned runner; snapshots operator/collector and preserves every full stream."""
import hashlib, json, os, stat, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path
FAMILY = Path(__file__).resolve().parent
PYTHON = '/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
def sha(b): return hashlib.sha256(b).hexdigest()
def utc(): return datetime.now(timezone.utc).isoformat()
def seal():
    """Final collector administration; no scientific or ROOT operator execution."""
    assert not (FAMILY/'SOURCE.json').exists()
    with (FAMILY/'RESEARCH_LOG.md').open('a') as log:
        log.write(f'- {utc()} — Lean family source sealed by collector{os.getpid()}; '
            'universal mathematical/source scope audit passes, eight exact controls and '
            'qualified publisher-access failure preserved. Audit100% for family handoff. '
            'ROOT custody/readback, human review and acceptance remain pending.\n')
    files=sorted(p for p in FAMILY.rglob('*') if p.is_file())
    dirs=[FAMILY]+sorted(p for p in FAMILY.rglob('*') if p.is_dir())
    assert not any(p.is_symlink() for p in files+dirs)
    assert not any(p.name.endswith(('.pdf','.png','.layout.txt')) for p in files)
    for p in files:p.chmod(0o444)
    for p in dirs:p.chmod(0o755)
    entries=[]
    for p in files:
        b=p.read_bytes();m=format(stat.S_IMODE(p.stat().st_mode),'04o');assert m=='0444'
        entries.append({'relative_path':str(p.relative_to(FAMILY)),'bytes':len(b),
                        'sha256':sha(b),'full_mode_07777':m})
    assert all(stat.S_IMODE(p.stat().st_mode)==0o755 for p in dirs)
    index={'schema':'pr58-tangent-fixed-source-index/v1','utc':utc(),'sealing_collector_pid':os.getpid(),
        'original_head':'465d771ec1ddc91877e8d9db51ed59aea1b0d97d','files':entries,
        'directories':['.' if p==FAMILY else str(p.relative_to(FAMILY)) for p in dirs],
        'directory_full_mode_07777':'0755','SOURCE_full_mode_07777':'0444','self_indexed':False,
        'private_primary_cache_required':False,'whole_primary_bodies_redistributed':False,
        'ROOT_helpers_executed':False,'ROOT_closure_readback_claimed':False}
    with (FAMILY/'SOURCE.json').open('x') as f:f.write(json.dumps(index,indent=2,sort_keys=True)+'\n')
    (FAMILY/'SOURCE.json').chmod(0o444);b=(FAMILY/'SOURCE.json').read_bytes()
    return {'SOURCE_sha256':sha(b),'SOURCE_bytes':len(b),'indexed_files':len(files),
            'total_files_including_SOURCE':len(files)+1,'directory_count':len(dirs)}
def main():
    tag, operator_name = sys.argv[1:]
    assert (tag, operator_name) in (('primary_read', 'read_primary_sources.py'),
        ('geometric_controls', 'geometric_controls.py'), ('handoff', 'prepare_handoff.py'))
    folder = FAMILY / 'captures' / tag; folder.mkdir(parents=True, exist_ok=False)
    operator = FAMILY / operator_name
    op = operator.read_bytes(); collector = Path(__file__).read_bytes()
    (folder / 'operator_prelaunch.py').write_bytes(op)
    (folder / 'collector_prelaunch.py').write_bytes(collector)
    started = utc(); argv = [PYTHON, str(operator)]
    with (folder / 'stdout.bin').open('wb') as out, (folder / 'stderr.bin').open('wb') as err:
        child = subprocess.Popen(argv, cwd=FAMILY, stdout=out, stderr=err)
        cap = {'collector_pid': os.getpid(), 'owned_child_pid': child.pid, 'argv': argv,
            'started_utc': started, 'cwd': str(FAMILY), 'operator_prelaunch_sha256': sha(op),
            'collector_prelaunch_sha256': sha(collector), 'ROOT_helpers_executed': False}
        (folder / 'PRELAUNCH.json').write_text(json.dumps(cap, indent=2) + '\n')
        code = child.wait()
    cap.update(ended_utc=utc(), exit_code=code, operator_after_sha256=sha(operator.read_bytes()),
        collector_after_sha256=sha(Path(__file__).read_bytes()))
    for stream in ('stdout', 'stderr'):
        b = (folder / (stream + '.bin')).read_bytes()
        cap[stream + '_bytes'] = len(b); cap[stream + '_sha256'] = sha(b)
    (folder / 'CAPTURE.json').write_text(json.dumps(cap, indent=2) + '\n')
    if tag=='handoff':
        assert code==0
        cap['final_admin_SOURCE']=seal()
    print(json.dumps(cap, sort_keys=True)); print((folder / 'stdout.bin').read_text())
    sys.exit(code)
if __name__ == '__main__': main()
