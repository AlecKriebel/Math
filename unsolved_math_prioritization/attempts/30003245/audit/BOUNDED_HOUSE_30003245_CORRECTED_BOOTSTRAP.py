"""Verify all external pins before opening the archive or executing its checker.
Run with python -I -S [-O] BOOTSTRAP.py ARCHIVE.zip MANIFEST.json.
Standard library only. No network; temporary extraction of the pinned checker only.
"""
import hashlib
import json
import pathlib
import stat
import subprocess
import sys
import tempfile
import zipfile

ARCHIVE_PIN = {'filename': 'BOUNDED_HOUSE_30003245_CORRECTED_SAFE.zip', 'bytes': 13956, 'sha256': 'a09a0aea6ad9199401a6afb36e1cad67d8bc4dd70a5ed9b3838f6f8bbd209004'}
MANIFEST_PIN = {'filename': 'BOUNDED_HOUSE_30003245_CORRECTED_EXTERNAL_MANIFEST.json', 'bytes': 2089, 'sha256': 'b7023a117f2275a012e3c09f95ffe967742827b3ada7bff040598376b0bccd78'}

def require(condition, message):
    if not condition:
        raise SystemExit("REJECTED BEFORE EXECUTION: " + message)

def read_pinned(path, pin):
    data = pathlib.Path(path).read_bytes()
    require(len(data) == pin["bytes"], "byte count " + pin["filename"])
    require(hashlib.sha256(data).hexdigest() == pin["sha256"], "SHA-256 " + pin["filename"])
    return data

require(len(sys.argv) == 3, "supply archive and manifest paths")
archive_data = read_pinned(sys.argv[1], ARCHIVE_PIN)
manifest_data = read_pinned(sys.argv[2], MANIFEST_PIN)
manifest = json.loads(manifest_data)
require(manifest["archive"] == ARCHIVE_PIN, "manifest archive binding")
expected = {row["name"]: row for row in manifest["members"]}
require(len(expected) == len(manifest["members"]) == 8, "expected member count")
# Open exactly the already pinned bytes, eliminating reopen races.
import io
with zipfile.ZipFile(io.BytesIO(archive_data)) as archive:
    infos = archive.infolist()
    names = [info.filename for info in infos]
    require(len(names) == len(set(names)) == 8 and set(names) == set(expected), "member set")
    verified = {}
    for info in infos:
        require(info.filename == pathlib.PurePosixPath(info.filename).name, "flat safe member name")
        require(not stat.S_ISLNK(info.external_attr >> 16), "symlink member")
        row = expected[info.filename]
        require(info.file_size == row["bytes"], "declared member size")
        data = archive.read(info)
        require(len(data) == row["bytes"] and hashlib.sha256(data).hexdigest() == row["sha256"], "member binding")
        verified[info.filename] = data
print("PINS VERIFIED: 8 members", flush=True)
with tempfile.TemporaryDirectory(prefix="bounded-house-verified-") as temporary:
    checker = pathlib.Path(temporary) / "verify_arithmetic.py"
    checker.write_bytes(verified["verify_arithmetic.py"])
    command = [sys.executable, "-I", "-S"]
    if sys.flags.optimize:
        command.append("-O")
    command.append(str(checker))
    result = subprocess.run(command, cwd=temporary, check=False, timeout=60)
    raise SystemExit(result.returncode)
