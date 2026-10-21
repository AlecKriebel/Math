#!/usr/bin/env python3
"""Deterministic safe allowlist archive; no source, manifest or descriptor mutation."""
from pathlib import Path
import argparse,importlib.util,zipfile,hashlib,sys
root=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('package_verify',root/'verify_package.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output).resolve()
allow=v.check()
# Protect every current input, including excluded descriptors and stage records.
# Only the designated generated archive and temporary outputs are mutable.
for protected in root.rglob('*'):
 if not protected.is_file() or protected==root/'support.zip' or protected.relative_to(root).parts[0]=='tmp':continue
 alias=out.resolve()==protected.resolve() or (out.exists() and out.samefile(protected))
 v.require(not alias,'cannot overwrite protected package input '+protected.relative_to(root).as_posix())
v.require(out.suffix=='.zip','archive output must end in .zip')
if out.is_relative_to(root):v.require(out==root/'support.zip' or out.is_relative_to(root/'tmp'),'inside package output must be support.zip or under tmp/')
out.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9,strict_timestamps=True) as z:
 for name in allow:
  info=zipfile.ZipInfo(name,date_time=v.FIXED_TIME);info.create_system=3;info.external_attr=0o100644<<16;info.compress_type=zipfile.ZIP_DEFLATED;info.internal_attr=0
  z.writestr(info,(root/name).read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
v.check_archive(out,allow)
print(str(out)+' SHA256 '+hashlib.sha256(out.read_bytes()).hexdigest())
