#!/usr/bin/env python3
"""Independent direct-source retrieval with native stdout/stderr/header retention."""
import datetime
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
def stamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def retrieve(label, url):
    target = ROOT / "native" / label
    target.mkdir(parents=True, exist_ok=False)
    headers = target / "http_headers.txt"
    argv = ["/usr/bin/curl", "--location", "--fail-with-body", "--show-error",
            "--connect-timeout", "25", "--max-time", "120", "--dump-header", str(headers), url]
    start = stamp()
    with (target / "stdout.bin").open("wb") as out, (target / "stderr.txt").open("wb") as err:
        result = subprocess.run(argv, stdout=out, stderr=err)
    end = stamp()
    record = {"argv": argv, "start_utc": start, "end_utc": end,
              "exit_code": result.returncode, "stdout": "stdout.bin",
              "stderr": "stderr.txt", "http_headers": "http_headers.txt"}
    (target / "run.json").write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps({"label": label, "exit_code": result.returncode,
                      "bytes": (target / "stdout.bin").stat().st_size,
                      "start_utc": start, "end_utc": end}))

if __name__ == "__main__":
    retrieve(sys.argv[1], sys.argv[2])
