from pathlib import Path
import argparse, datetime, hashlib, json, os, subprocess, sys

F = Path(__file__).resolve().parent
R = Path('/Users/alec/Documents/Math')

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def row(path):
    b = path.read_bytes()
    return {'path': path.relative_to(F).as_posix(), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('name')
    ap.add_argument('argv', nargs=argparse.REMAINDER)
    a = ap.parse_args()
    assert a.name and '/' not in a.name and a.name not in ('.', '..')
    argv = a.argv[1:] if a.argv[:1] == ['--'] else a.argv
    assert argv
    d = F / 'captures' / a.name
    d.mkdir(parents=True, exist_ok=False)
    pre = d / 'prelaunch_operator.py'
    pre.write_bytes(Path(__file__).read_bytes())
    child = Path(argv[2]) if len(argv) > 2 and argv[1] == '-B' else None
    if child is not None and child.is_file():
        (d / 'prelaunch_child.py').write_bytes(child.read_bytes())
    t0 = now()
    p = subprocess.Popen(argv, cwd=R, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    t1 = now()
    (d / 'stdout.bin').write_bytes(out)
    (d / 'stderr.bin').write_bytes(err)
    cap = {'schema': 'pr53-independent-complete-command-capture/v1', 'pid': p.pid,
           'argv': argv, 'cwd': str(R), 'started_at': t0, 'completed_at': t1,
           'exit_code': p.returncode, 'status': 'PASS' if p.returncode == 0 else 'FAIL',
           'operator_prelaunch': row(pre), 'stdout': row(d / 'stdout.bin'),
           'stderr': row(d / 'stderr.bin')}
    if (d / 'prelaunch_child.py').exists():
        cap['child_prelaunch'] = row(d / 'prelaunch_child.py')
    (d / 'CAPTURE.json').write_text(json.dumps(cap, indent=2) + '\n')
    print(json.dumps(cap, indent=2))
    sys.exit(p.returncode)

if __name__ == '__main__':
    main()
