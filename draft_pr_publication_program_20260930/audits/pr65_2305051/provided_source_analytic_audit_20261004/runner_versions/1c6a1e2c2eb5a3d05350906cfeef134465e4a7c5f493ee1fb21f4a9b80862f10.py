#!/usr/bin/env python3
"""Execute one command and preserve actual process provenance and byte streams."""
import argparse, datetime, hashlib, json, os, pathlib, subprocess, sys

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()

p = argparse.ArgumentParser()
p.add_argument('--name', required=True)
p.add_argument('--cwd', required=True)
p.add_argument('--pin', action='append', default=[])
p.add_argument('--streams-dir')
p.add_argument('command', nargs=argparse.REMAINDER)
a = p.parse_args()
command = a.command[1:] if a.command and a.command[0] == '--' else a.command
root = pathlib.Path(__file__).resolve().parent
receipt_dir = root / 'receipts'
receipt_dir.mkdir(parents=True, exist_ok=True)
prefix = receipt_dir / a.name
start = now()
pins = [{'path': str(pathlib.Path(x).resolve()), 'sha256': sha(x)} for x in a.pin]
proc = subprocess.Popen(command, cwd=a.cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = proc.communicate()
end = now()
stream_prefix = (pathlib.Path(a.streams_dir) / a.name) if a.streams_dir else prefix
stream_prefix.parent.mkdir(parents=True, exist_ok=True)
out_path, err_path = pathlib.Path(str(stream_prefix)+'.stdout'), pathlib.Path(str(stream_prefix)+'.stderr')
out_path.write_bytes(out)
err_path.write_bytes(err)
receipt = {
    'schema': 'actual-subprocess-receipt-v1',
    'name': a.name, 'started_utc': start, 'finished_utc': end,
    'pid': proc.pid, 'argv': command, 'cwd': a.cwd, 'exit_code': proc.returncode,
    'source_pins': pins,
    'runner': {'pid': os.getpid(), 'argv': [sys.executable] + sys.argv,
               'cwd': os.getcwd(), 'path': str(pathlib.Path(__file__).resolve()),
               'sha256': sha(__file__)},
    'stdout': {'path': str(out_path), 'sha256': sha(out_path), 'bytes': len(out)},
    'stderr': {'path': str(err_path), 'sha256': sha(err_path), 'bytes': len(err)},
}
pathlib.Path(str(prefix)+'.json').write_text(json.dumps(receipt, indent=2)+'\n')
sys.stdout.buffer.write(out)
sys.stderr.buffer.write(err)
raise SystemExit(proc.returncode)
