"""Bounded reviewer child custody; no imported runner used."""
import datetime, hashlib, json, os, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def digest(data):
    return hashlib.sha256(data).hexdigest()

def run(name, argv, cwd, role, inputs=(), timeout=60):
    out = ROOT / 'actual_processes' / name
    out.mkdir(parents=True, exist_ok=False)
    before = [{'path':str(Path(p)), 'sha256':digest(Path(p).read_bytes())} for p in inputs]
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    child = subprocess.Popen(argv, cwd=str(cwd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    timed_out = False
    try:
        stdout, stderr = child.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        child.kill()
        stdout, stderr = child.communicate()
    end = datetime.datetime.now(datetime.timezone.utc).isoformat()
    (out/'stdout.bin').write_bytes(stdout)
    (out/'stderr.bin').write_bytes(stderr)
    receipt = {'argv':argv,'cwd':str(cwd),'pid':child.pid,'UTC_start':start,'UTC_end':end,
        'exit':child.returncode,'timeout':timed_out,'role':role,'inputs_before':before,
        'inputs_after':[{'path':str(Path(p)), 'sha256':digest(Path(p).read_bytes())} for p in inputs],
        'stdout':{'bytes':len(stdout),'sha256':digest(stdout)},
        'stderr':{'bytes':len(stderr),'sha256':digest(stderr)}}
    (out/'receipt.json').write_text(json.dumps(receipt, indent=2)+'\n')
    return child.returncode, stdout, stderr, receipt
