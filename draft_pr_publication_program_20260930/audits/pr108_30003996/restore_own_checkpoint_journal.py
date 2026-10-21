"""Verify retained checkpoint bytes; --restore restores the exact old local file."""
from pathlib import Path
import argparse, datetime, gzip, hashlib, json, os, shutil
A=Path(__file__).resolve().parent; C=A.parents[2]
def require(c,m):
    if not c: raise RuntimeError(m)
def digest(b): return hashlib.sha256(b).hexdigest()
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--restore', action='store_true'); args=parser.parse_args()
r=json.loads((A/'ROOT_PRIVATE_CHECKPOINT_COMPRESSION_20261006.json').read_text())
source=C/r['compressed_path_relative_to_checkout']; target=C/r['original_path_relative_to_checkout']
require(source.resolve().is_relative_to(C.resolve()) and target.parent.resolve().is_relative_to(C.resolve()),'local scope')
require(source.is_file() and not source.is_symlink(),'regular compressed file')
b=source.read_bytes(); require(len(b)==r['compressed_bytes'] and digest(b)==r['compressed_sha256'],'compressed byte pin')
raw=gzip.decompress(b); require(len(raw)==r['original_bytes'] and digest(raw)==r['original_sha256'],'original roundtrip pin')
restored=False
if args.restore:
    if target.exists():
        require(target.is_file() and not target.is_symlink() and target.read_bytes()==raw,'existing target differs')
    else:
        require(shutil.disk_usage(target.parent).free>len(raw)+1048576,'insufficient restore capacity')
        fd=os.open(target,os.O_WRONLY|os.O_CREAT|os.O_EXCL,r['original_mode'])
        with os.fdopen(fd,'wb') as f: f.write(raw); f.flush(); os.fsync(f.fileno())
        require(target.read_bytes()==raw,'restored bytes'); restored=True
print(json.dumps({'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_PID':os.getpid(),'original_bytes_verified':len(raw),'original_sha256':digest(raw),'restored':restored,'compressed_retained':True}))
