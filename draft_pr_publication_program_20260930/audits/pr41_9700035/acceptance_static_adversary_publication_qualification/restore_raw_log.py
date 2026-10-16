import gzip,hashlib,json
from pathlib import Path
p=Path(__file__).resolve().parent;r=p.parents[3];o=json.loads((p/'QUALIFICATION.json').read_bytes());c=(p/o['compressed']['path']).read_bytes();assert len(c)==o['compressed']['bytes'] and hashlib.sha256(c).hexdigest()==o['compressed']['sha256'];b=gzip.decompress(c);assert len(b)==o['original']['bytes'] and hashlib.sha256(b).hexdigest()==o['original']['sha256'];t=r/o['original']['path'];assert t.parent.is_dir() and not t.is_symlink() and not any(x.is_symlink() for x in t.parents)
if t.exists():assert t.is_file() and t.read_bytes()==b
else:
 with t.open('xb') as f:f.write(b)
t.chmod(0o444)
print('Original full typed-node file and closed-family bytes restored exactly.')
