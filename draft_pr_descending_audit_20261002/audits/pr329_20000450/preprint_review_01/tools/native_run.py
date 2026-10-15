#!/usr/bin/env python3
"""Run argv without a shell; retain actual process streams and native UTC clocks."""
import argparse
import json
import pathlib
import subprocess

p = argparse.ArgumentParser()
p.add_argument("--label", required=True)
p.add_argument("--cwd", required=True)
p.add_argument("argv", nargs=argparse.REMAINDER)
a = p.parse_args()
argv = a.argv[1:] if a.argv[:1] == ["--"] else a.argv
root = pathlib.Path(__file__).resolve().parents[1]
out = root / "evidence" / a.label
out.parent.mkdir(parents=True, exist_ok=True)
if out.with_suffix(".stdout").exists():
    raise SystemExit("Refusing to overwrite retained evidence")
out.with_suffix(".argv.json").write_text(json.dumps({"argv": argv, "cwd": a.cwd}, indent=2) + "\n")
clock = ["/bin/date", "-u", "+%Y-%m-%dT%H:%M:%SZ"]
with out.with_suffix(".native-time.txt").open("wb") as times:
    times.write(b"START ")
    times.flush()
    subprocess.run(clock, stdout=times, stderr=subprocess.STDOUT, check=True)
    with out.with_suffix(".stdout").open("wb") as stdout, out.with_suffix(".stderr").open("wb") as stderr:
        try:
            result = subprocess.run(argv, cwd=a.cwd, stdout=stdout, stderr=stderr)
            status = result.returncode
        except BaseException as e:
            stderr.write((repr(e) + "\n").encode())
            status = 125
    times.write(b"END ")
    times.flush()
    subprocess.run(clock, stdout=times, stderr=subprocess.STDOUT, check=True)
    times.write(f"EXIT {status}\n".encode())
print(out.with_suffix(".native-time.txt").read_text(), end="")
print(out.with_suffix(".stdout").read_text(errors="replace"), end="")
print(out.with_suffix(".stderr").read_text(errors="replace"), end="")
raise SystemExit(status)
