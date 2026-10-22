#!/usr/bin/env python3
"""Deterministic explicit allowlist ZIP; existing manifest is never rewritten."""
import argparse,json,zipfile,sys
sys.dont_write_bytecode=True
from pathlib import Path
from verify_package import ROOT,verify
from package_paths import fresh_output,safe_path
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
output=fresh_output(a.out)
verify(bindings=ROOT/'__absent_binding__')
manifest=json.loads(safe_path(ROOT,'PACKAGE_MANIFEST.json').read_text())
names=sorted([r['path'] for r in manifest['members']]+['PACKAGE_MANIFEST.json'])
with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_STORED,allowZip64=False) as z:
    for name in names:
        info=zipfile.ZipInfo(name,date_time=(2026,10,14,0,0,0));info.create_system=3;info.external_attr=0o100644<<16;info.compress_type=zipfile.ZIP_STORED
        z.writestr(info,safe_path(ROOT,name).read_bytes())
print(json.dumps({'archive':str(a.out),'members':len(names),'compression':'ZIP_STORED','fixed_time':'2026-10-14T00:00:00','permissions':'regular-file 0644','order':'lexicographic explicit manifest allowlist'},indent=2))
