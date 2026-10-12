"""Private, read-only command capture for PR80 custody; no shell interpolation."""
import argparse
import datetime
import hashlib
import gzip
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import stat

ROOT = Path(__file__).resolve().parent
RESERVATION = ROOT / 'native_evidence_capacity_reservation.bin'

def require(ok, message):
    if not ok: raise RuntimeError(message + '; preserve partial state')

def reserve_remaining():
    require(RESERVATION.is_file() and not RESERVATION.is_symlink(), 'Evidence reservation missing')
    s=RESERVATION.stat()
    require(stat.S_ISREG(s.st_mode) and stat.S_IMODE(s.st_mode)==0o600 and s.st_nlink==1
            and s.st_blocks*512>=s.st_size, 'Evidence reservation is not privately allocated')
    return s.st_size

def reserve_evidence_capacity(byte_count):
    require(not sys.flags.optimize, 'Optimization disables capacity checks')
    require(type(byte_count)==int and byte_count==300*1024*1024, 'Unreviewed evidence capacity')
    require(not RESERVATION.exists() and not RESERVATION.is_symlink(), 'Existing reservation must be inspected')
    free=shutil.disk_usage(ROOT).free
    require(free>=byte_count+64*1024*1024, 'Insufficient durable capacity before mutation')
    with RESERVATION.open('xb') as stream:
        os.chmod(RESERVATION,0o600)
        chunk=b'\0'*(1024*1024)
        for _ in range(byte_count//len(chunk)):stream.write(chunk)
        stream.flush();os.fsync(stream.fileno())
    require(reserve_remaining()==byte_count, 'Capacity allocation did not complete')
    return {'UTC':utc(),'actual_PID':os.getpid(),'path':str(RESERVATION),
            'reserved_logical_bytes':byte_count,'actual_allocated_bytes':RESERVATION.stat().st_blocks*512,
            'free_before_allocation':free,'stream_codec':'gzip','raw_evidence_deleted':False}

def durable_write(path, data):
    require(not path.exists() and not path.is_symlink(), 'Existing capture output')
    if RESERVATION.exists():
        remaining=reserve_remaining()
        charged=((len(data)+4095)//4096+1)*4096
        require(remaining>=charged+32*1024*1024, 'Evidence capacity floor reached')
        with RESERVATION.open('r+b') as stream:
            stream.truncate(remaining-charged);stream.flush();os.fsync(stream.fileno())
    with path.open('xb') as stream:
        stream.write(data);stream.flush();os.fsync(stream.fileno())
    require(path.read_bytes()==data, 'Durable capture write readback mismatch')

def compressed_write(path, data):
    stored=gzip.compress(data,compresslevel=6,mtime=0)
    require(gzip.decompress(stored)==data, 'Compressed capture does not round-trip')
    durable_write(path,stored)
    actual=path.read_bytes()
    require(len(actual)==len(stored) and digest(actual)==digest(stored)
            and gzip.decompress(actual)==data,'Stored compressed capture custody mismatch')
    return {'storage_codec':'gzip','storage_bytes':len(stored),'storage_sha256':digest(stored),
            'logical_bytes':len(data),'logical_sha256':digest(data)}

def digest(data):
    return hashlib.sha256(data).hexdigest()

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def capture(label, argv, cwd="/Users/alec/Documents/Math", sources=()):
    require(not sys.flags.optimize, 'Optimization disables capture checks')
    folder = ROOT / "process_evidence" / label
    folder.mkdir(parents=True, exist_ok=False)
    retained = []
    argv_sources = [item for item in argv if item.endswith(".py") and Path(item).is_file()]
    for index, source in enumerate(dict.fromkeys([str(Path(__file__).resolve()), *sources, *argv_sources])):
        path = Path(source).resolve()
        data = path.read_bytes()
        dest = folder / (str(index) + "_" + path.name + '.gz')
        storage=compressed_write(dest,data)
        retained.append({"path": str(path), "retained_path": str(dest), "bytes": len(data), "sha256": digest(data),**storage})
    request = {"label": label, "argv": argv, "cwd": cwd, "requested_at_UTC": utc(), "retained_sources_prelaunch": retained}
    durable_write(folder/'request.json',(json.dumps(request,indent=2)+'\n').encode())
    capacity_before=reserve_remaining() if RESERVATION.exists() else None
    if capacity_before is not None:require(capacity_before>=64*1024*1024,'Insufficient reserved output capacity before child')
    start = utc()
    timer = time.monotonic()
    process = subprocess.Popen(argv, cwd=cwd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    pid = process.pid
    durable_write(folder/'process_started.json',(json.dumps({'actual_PID':pid,'start_UTC':start,
                  'state':'CHILD_STARTED_OUTCOME_PENDING'})+'\n').encode())
    stdout, stderr = process.communicate()
    end = utc()
    durable_write(folder/'process_completed.json',(json.dumps({'actual_PID':pid,'start_UTC':start,
                  'end_UTC':end,'exit_code':process.returncode,'stdout_bytes':len(stdout),
                  'stdout_sha256':digest(stdout),'stderr_bytes':len(stderr),'stderr_sha256':digest(stderr),
                  'state':'CHILD_COMPLETED_STREAM_STORAGE_PENDING'})+'\n').encode())
    stdout_storage=compressed_write(folder/'stdout.bin.gz',stdout)
    stderr_storage=compressed_write(folder/'stderr.bin.gz',stderr)
    result = {**request, "actual_PID": pid, "start_UTC": start, "end_UTC": end, "elapsed_seconds": time.monotonic()-timer, "exit_code": process.returncode, "stdout_bytes": len(stdout), "stdout_sha256": digest(stdout), "stderr_bytes": len(stderr), "stderr_sha256": digest(stderr), "stdout_path": str(folder / "stdout.bin.gz"), "stderr_path": str(folder / "stderr.bin.gz"), 'stdout_storage':stdout_storage,'stderr_storage':stderr_storage,'capacity_reserved_before_child':capacity_before,'capacity_reserved_after_streams':reserve_remaining() if RESERVATION.exists() else None, "launcher_claim": "Only this capture process is described; no upstream launcher/environment certification."}
    durable_write(folder/'result.json',(json.dumps(result,indent=2)+'\n').encode())
    return result, stdout, stderr

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("label")
    parser.add_argument("argv", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    argv = args.argv[1:] if args.argv and args.argv[0] == "--" else args.argv
    result, _, _ = capture(args.label, argv)
    print(json.dumps(result, indent=2))
