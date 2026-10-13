"""Close and immediately authenticate the corrected local review inventory."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import sys
import time
sys.dont_write_bytecode = True
base = Path(__file__).resolve().parent.parent
sys.path.insert(0,str(base/'publicfiles/support'))
from safe_output import write_new, json_bytes
start = dt.datetime.now(dt.timezone.utc).isoformat()
tick = time.monotonic()
invocation = ['/usr/bin/python3','-E','-B','-O',str(Path(__file__).resolve())]

def require(value,message):
    if not value:
        raise ValueError(message)

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
require(sys.flags.ignore_environment == 1 and sys.flags.dont_write_bytecode == 1
        and sys.flags.optimize == 1 and len(sys.argv) == 1,
        'Use the recorded closure invocation: /usr/bin/python3 -E -B -O SCRIPT')
require(not (base/'CLOSED_MANIFEST.json').exists(),'Never overwrite a closed snapshot')
for p in [base]+list(base.parents):
    require(not p.is_symlink(),'Escaping symlink in review-root ancestry')
files = []
links = []
inodes = {}
for p in sorted(base.rglob('*')):
    relative = p.relative_to(base).as_posix()
    if p.is_symlink():
        target = p.resolve(strict=True)
        require(base in target.parents,'Controlled symlink escapes snapshot')
        require(target.is_file(),'Controlled symlink must target synthetic file')
        links.append(dict(path=relative,type='controlled_synthetic_symlink',target=os.readlink(p),
                          target_within_snapshot=True,target_sha256=sha(target)))
    elif p.is_file():
        files.append(dict(path=relative,sha256=sha(p),bytes=p.stat().st_size))
        if p.stat().st_nlink > 1:
            key=(p.stat().st_dev,p.stat().st_ino)
            inodes.setdefault(key,[]).append(relative)
hardlinks = sorted(inodes.values())
for group in hardlinks:
    require(len(group)==(base/group[0]).stat().st_nlink,'Hardlink group has unbound outside members')
    require(all(n.startswith('private/custody_current/') for n in group),
            'Hardlinks outside synthetic custody fixtures')
require(len(links)==10 and len(hardlinks)==10,'Unexpected synthetic fixture link inventory')
require(all(e['path'].startswith('private/custody_current/') for e in links),
        'Symlink outside synthetic fixture scope')
borrowed=json.loads((base/'BORROWED_INPUT_PINS.json').read_text())
manifest=dict(schema='pr97-corrected-closed-review/v2',UTC=dt.datetime.now(dt.timezone.utc).isoformat(),
              files=files,controlled_symlinks=links,hardlink_groups=hardlinks,
              excluded=['CLOSED_MANIFEST.json'],borrowed_input_bindings=borrowed,
              fixture_scope='Ten retained synthetic symlinks and ten synthetic hardlink groups; '
                            'public payload and ZIP have none. Normal control cleanup is documented in REPORT.',
              creator=dict(pid=os.getpid(),command=invocation,interpreter_executable=sys.executable,
                           started_utc=start,source_sha256=sha(Path(__file__).resolve())),
              publication_authorized=False,strict_priority_clearance=False,whole_package_acceptance=False,
              scope='Corrected review snapshot, pending fresh ROOT-appointed whole-package review.')
write_new(base/'CLOSED_MANIFEST.json',json_bytes(manifest))
# Explicit checks stay live under -O; no receipt is mutated after closure.
parsed=json.loads((base/'CLOSED_MANIFEST.json').read_text())
for e in parsed['files']:
    p=base/e['path']
    require(not p.is_symlink() and sha(p)==e['sha256'] and p.stat().st_size==e['bytes'],
            'Own file digest/size changed')
for e in parsed['controlled_symlinks']:
    p=base/e['path']
    require(p.is_symlink() and os.readlink(p)==e['target'] and sha(p.resolve())==e['target_sha256'],
            'Controlled symlink changed')
for group in parsed['hardlink_groups']:
    require(len({((base/n).stat().st_dev,(base/n).stat().st_ino) for n in group})==1,
            'Hardlink witness changed')
expected={e['path'] for e in parsed['files']} | {e['path'] for e in parsed['controlled_symlinks']} | {'CLOSED_MANIFEST.json'}
actual={p.relative_to(base).as_posix() for p in base.rglob('*') if p.is_file() or p.is_symlink()}
require(expected==actual,'Own closed file inventory mismatch')
print(json.dumps(dict(status='PASS',pid=os.getpid(),command=invocation,
                      started_utc=start,finished_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
                      wall_seconds=time.monotonic()-tick,own_regular_files=len(files),
                      controlled_symlinks=len(links),hardlink_groups=len(hardlinks),
                      closed_manifest_sha256=sha(base/'CLOSED_MANIFEST.json'),
                      archive_sha256=sha(base/'pr97_support.zip'),
                      payload_manifest_sha256=sha(base/'publicfiles/MANIFEST.json'),
                      no_writes_after_closed_inventory=True,publication_authorized=False,
                      strict_priority_clearance=False,whole_package_acceptance=False),indent=2))
