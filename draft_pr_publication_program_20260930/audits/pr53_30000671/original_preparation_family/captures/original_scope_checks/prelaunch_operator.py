"""Capture an actual read-only child command inside this family's folder."""
import argparse, datetime, hashlib, json, os, pathlib, subprocess, sys
F = pathlib.Path(__file__).resolve().parent
R = F.parents[3]
def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00', 'Z')
def sha(b):
    return hashlib.sha256(b).hexdigest()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('name')
    ap.add_argument('command', nargs=argparse.REMAINDER)
    args = ap.parse_args()
    assert args.name and '/' not in args.name and args.name not in ('.', '..')
    argv = args.command
    if argv and argv[0] == '--': argv = argv[1:]
    assert argv
    d = F/'captures'/args.name
    d.mkdir(parents=True, exist_ok=False)
    source = pathlib.Path(__file__).read_bytes()
    (d/'prelaunch_operator.py').write_bytes(source)
    child_source = None
    if len(argv)>2 and pathlib.Path(argv[0]).name.startswith('python'):
        candidate=pathlib.Path(argv[2]) if argv[1]=='-B' else pathlib.Path(argv[1])
        if not candidate.is_absolute():candidate=R/candidate
        if candidate.is_file():
            body=candidate.read_bytes();(d/'prelaunch_child.py').write_bytes(body)
            child_source={'path':'prelaunch_child.py','original_path':str(candidate),'bytes':len(body),'sha256':sha(body)}
    started = now()
    proc = subprocess.Popen(argv, cwd=R, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    completed = now()
    (d/'stdout.bin').write_bytes(out)
    (d/'stderr.bin').write_bytes(err)
    cap = {'schema':'pr53-real-readonly-capture/v1', 'pid':proc.pid, 'argv':argv,
           'cwd':str(R), 'started_at':started, 'completed_at':completed,
           'exit_code':proc.returncode, 'operator_sha256':sha(source),
           'stdout':{'path':'stdout.bin','bytes':len(out),'sha256':sha(out)},
           'stderr':{'path':'stderr.bin','bytes':len(err),'sha256':sha(err)},
           'prelaunch_child_source':child_source}
    (d/'CAPTURE.json').write_text(json.dumps(cap, indent=2)+'\n')
    print(json.dumps(cap))
    sys.exit(proc.returncode)
if __name__ == '__main__': main()
