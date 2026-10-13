#!/usr/bin/python3
import argparse, datetime, hashlib, json, os, pathlib, stat, subprocess, sys, traceback, types

ROOT = pathlib.Path(__file__).resolve().parent
def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def provenance(path):
    path = pathlib.Path(path)
    raw = path.read_bytes()
    return {"path": str(path.resolve()), "sha256": hashlib.sha256(raw).hexdigest(),
            "size_bytes": len(raw), "mode": format(stat.S_IMODE(path.stat().st_mode), "04o")}

parser = argparse.ArgumentParser()
parser.add_argument("label")
parser.add_argument("--cwd", default=str(ROOT))
parser.add_argument("argv", nargs=argparse.REMAINDER)
args = parser.parse_args()
argv = args.argv[1:] if args.argv and args.argv[0] == "--" else args.argv
if not argv:
    parser.error("argv required")
folder = ROOT / "private" / "commands"
index = len(list(folder.glob("*.json")))
stem = folder / (str(index).zfill(3) + "_" + args.label)
started = utc()
try:
    result = subprocess.run(argv, cwd=args.cwd, capture_output=True)
except OSError:
    result = types.SimpleNamespace(returncode=127, stdout=b'', stderr=traceback.format_exc().encode())
out = pathlib.Path(str(stem) + ".stdout")
err = pathlib.Path(str(stem) + ".stderr")
out.write_bytes(result.stdout)
err.write_bytes(result.stderr)
record = {"label": args.label, "started_utc": started, "finished_utc": utc(),
          "driver_argv": [sys.executable] + sys.argv,
          "argv": argv, "cwd": args.cwd, "exit_code": result.returncode,
          "stdout": provenance(out), "stderr": provenance(err),
          "capture_driver": provenance(__file__)}
pathlib.Path(str(stem) + ".json").write_text(json.dumps(record, indent=2) + "\n")
sys.stdout.buffer.write(result.stdout)
sys.stderr.buffer.write(result.stderr)
sys.exit(result.returncode)
