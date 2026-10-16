#!/usr/bin/env python3
"""Deterministic ZIP of the explicitly owned publication supplement."""
from pathlib import Path
import hashlib,json,zipfile
root=Path(__file__).resolve().parents[1]
files=['main.tex','README.md','CURRENT_THEOREM.md','DEPENDENCY_LEDGER.md','APPROACH_TABLE.md',
       'SOURCE_MANIFEST.json','bibliography.bib','code/binary_compiler.py',
       'code/build_verification_package.py','code/clean_reproduction.py',
       'reviews/reduction_adversary.md','reviews/reduction_adversary_check.py',
       'reviews/reduction_adversary_independent_receipt.json',
       'agent_notes/binary_compiler.md','agent_notes/binary_compiler_check_results.json',
       'agent_notes/upstream_determinization.md','agent_notes/upstream_determinization_sha256.txt',
       'agent_notes/determinization_algebra_check.py','agent_notes/determinization_algebra_check_results.json',
       'agent_notes/upstream_complementation.md','agent_notes/upstream_complementation_sha256.txt',
       'agent_notes/upstream_algebra_check.py','agent_notes/upstream_algebra_check.json',
       'agent_notes/formal_reproduction.md','agent_notes/priority.md',
       'receipts/root_compiler_check.json','receipts/clean_reproduction.json']
manifest={p:{'bytes':(root/p).stat().st_size,'sha256':hashlib.sha256((root/p).read_bytes()).hexdigest()}
          for p in sorted(files)}
with zipfile.ZipFile(root/'verification.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for name in sorted(files):
        info=zipfile.ZipInfo(name,(2026,10,6,0,0,0));info.external_attr=0o100644<<16
        info.compress_type=zipfile.ZIP_DEFLATED
        z.writestr(info,(root/name).read_bytes())
    info=zipfile.ZipInfo('PACKAGE_CONTENTS.json',(2026,10,6,0,0,0));info.external_attr=0o100644<<16
    info.compress_type=zipfile.ZIP_DEFLATED
    z.writestr(info,json.dumps(manifest,indent=2,sort_keys=True)+'\n')
print(json.dumps({'files':len(files)+1,'sha256':hashlib.sha256((root/'verification.zip').read_bytes()).hexdigest(),
                  'bytes':(root/'verification.zip').stat().st_size},indent=2))
