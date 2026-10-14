#!/usr/bin/env python3
"""Deterministic safe allowlist archive; no source, manifest or descriptor mutation."""
from pathlib import Path
import argparse,importlib.util,zipfile,hashlib
root=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('package_verify',root/'verify_package.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output).resolve()
allow=v.check()
v.require(out not in [root/x for x in allow],'cannot overwrite a package input')
out.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9,strict_timestamps=True) as z:
 for name in allow:
  info=zipfile.ZipInfo(name,date_time=v.FIXED_TIME);info.create_system=3;info.external_attr=0o100644<<16;info.compress_type=zipfile.ZIP_DEFLATED;info.internal_attr=0
  z.writestr(info,(root/name).read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
v.check_archive(out,allow)
print(str(out)+' SHA256 '+hashlib.sha256(out.read_bytes()).hexdigest())
