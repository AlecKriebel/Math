"""Replay published evidence without mutating the archived evidence files."""
from pathlib import Path
import argparse, hashlib, json, shutil, subprocess, sys, tempfile, time

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("--full", action="store_true")
args = parser.parse_args()
manifest = json.loads((HERE / "MANIFEST.json").read_text())
for row in manifest["files"]:
    path = HERE / row["path"]
    data = path.read_bytes()
    assert len(data) == row["bytes"]
    assert hashlib.sha256(data).hexdigest() == row["sha256"], row["path"]
tasks = [
    "original_independent/independent_checks.py",
    "geometric_domain_adversary_01/real_cartesian_certificate.py",
    "algebraic_adversary_01/independent_winding_certificate.py",
]
if args.full:
    tasks += [
        "author/verify.py", "original_independent/independent_numeric.py",
        "algebraic_adversary_01/independent_verifier.py",
        "geometric_domain_adversary_01/geometric_audit.py",
    ]
out = HERE / "replay-output"
out.mkdir(exist_ok=True)
receipts = []
for i, task in enumerate(tasks, 1):
    with tempfile.TemporaryDirectory(prefix="k307-replay-") as td:
        directory = Path(td)
        script = directory / Path(task).name
        shutil.copyfile(HERE / task, script)
        start = time.monotonic()
        result = subprocess.run([sys.executable, str(script)], cwd=directory,
                                capture_output=True, text=True)
        label = f"{i:02d}-{script.stem}"
        (out / (label + ".stdout.txt")).write_text(result.stdout)
        (out / (label + ".stderr.txt")).write_text(result.stderr)
        for generated in directory.glob("*.json"):
            shutil.copyfile(generated, out / (label + "-" + generated.name))
        receipts.append({"script": task, "returncode": result.returncode,
                         "elapsed_seconds": time.monotonic() - start})
        (out / "RUN_RECEIPTS.json").write_text(json.dumps(receipts, indent=2) + "\n")
        print(task, "PASS" if result.returncode == 0 else "FAIL", flush=True)
        if result.returncode:
            raise SystemExit(result.returncode)
print("PASS: integrity and all selected verification programs")
