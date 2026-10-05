#!/usr/bin/env python3
"""Reproducibly package an intentional edit of this source-free audit."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import zipfile

sys.dont_write_bytecode=True
from verify_audit import FILES

ROOT=Path(__file__).resolve().parent


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    out=args.output.resolve()
    if out.parent==ROOT:raise ValueError('archive must be outside package')
    m={'schema':1,'files':{}}
    for name in sorted(FILES):
        p=ROOT/name
        if not p.is_file() or p.is_symlink():raise ValueError('missing or symlinked file: '+name)
        raw=p.read_bytes();m['files'][name]={'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
    (ROOT/'MANIFEST.json').write_text(json.dumps(m,indent=2,sort_keys=True)+'\n')
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in sorted(FILES|{'MANIFEST.json'}):
            info=zipfile.ZipInfo(name,(2000,1,1,0,0,0));info.create_system=3;info.external_attr=0o100644<<16
            z.writestr(info,(ROOT/name).read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    raw=out.read_bytes()
    print(json.dumps({'filename':out.name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'entries':len(FILES)+1},sort_keys=True))


if __name__=='__main__':main()
