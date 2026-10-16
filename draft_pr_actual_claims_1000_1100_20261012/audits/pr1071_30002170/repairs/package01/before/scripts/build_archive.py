#!/usr/bin/env python3
"""Deterministic explicit allowlist ZIP; existing manifest is never rewritten."""
import argparse,json,zipfile,sys
sys.dont_write_bytecode=True
from pathlib import Path
from verify_package import ROOT,verify
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args()
verify(bindings=ROOT/'__absent_binding__')
manifest=json.loads((ROOT/'PACKAGE_MANIFEST.json').read_text())
names=sorted([r['path'] for r in manifest['members']]+['PACKAGE_MANIFEST.json'])
if a.out.resolve().is_relative_to(ROOT.resolve()) and a.out.resolve().parent==ROOT:raise SystemExit('Place generated archive outside frozen root, e.g. _tmp/rebuild.zip.')
a.out.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(a.out,'w',compression=zipfile.ZIP_STORED,allowZip64=False) as z:
    for name in names:
        info=zipfile.ZipInfo(name,date_time=(2026,10,14,0,0,0));info.create_system=3;info.external_attr=0o100644<<16;info.compress_type=zipfile.ZIP_STORED
        z.writestr(info,(ROOT/name).read_bytes())
print(json.dumps({'archive':str(a.out),'members':len(names),'compression':'ZIP_STORED','fixed_time':'2026-10-14T00:00:00','permissions':'regular-file 0644','order':'lexicographic explicit manifest allowlist'},indent=2))
