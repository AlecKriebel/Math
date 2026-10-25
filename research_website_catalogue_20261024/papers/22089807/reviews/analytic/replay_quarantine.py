#!/usr/bin/env python3
"""Copy only statically reviewed certificate inputs, then replay without install/build."""
from pathlib import Path
import hashlib
import json
import os
import runpy
import shutil
import sys

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parents[1]/"sources/published-source/universal_simultaneous_amplification/phase4_landmark_closure/paper_hybrid_threshold"
DEST=HERE/"artifacts/quarantine"
FILES=["main.tex","certificates/verify_leading_algebra.py","certificates/verify_hybrid_lumping.py","certificates/verify_hybrid_coefficients.py","verify_paper_claims.py","vendor/mpmath-1.3.0-py3-none-any.whl","vendor/sympy-1.14.0-py3-none-any.whl"]
if sys.flags.optimize:
    raise RuntimeError("optimized replay refused")
if DEST.exists():
    raise RuntimeError("quarantine already exists; preserve existing evidence")
manifest=[]
for name in FILES:
    source=SOURCE/name
    target=DEST/name
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(source,target)
    digest=hashlib.sha256(target.read_bytes()).hexdigest()
    if digest!=hashlib.sha256(source.read_bytes()).hexdigest():
        raise RuntimeError(f"copy mismatch {name}")
    manifest.append({"file":name,"sha256":digest})
(HERE/"artifacts/quarantine-inputs.json").write_text(json.dumps(manifest,indent=2)+"\n")
for name in FILES[-2:]: sys.path.insert(0,str(DEST/name))
os.chdir(DEST)
print("Runtime:",sys.version)
for name in FILES[1:5]:
    print("RUN",name,flush=True)
    runpy.run_path(str(DEST/name),run_name="__main__")
print("PASS quarantine replay of all four submitted substantive verifiers")
