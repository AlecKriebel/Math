# Closed-packet read-only verification

Prehash the exact verifier buffer before its first execution, then pass the independently supplied final manifest hash. The manifest hash is external to the recursive packet. This command performs no service call, actor launch, journal mutation or file write. Keep Python isolated, without bytecode writes, and compile at optimize0.

```bash
/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/bin/python3.14 -I -S -B -c 'from pathlib import Path; import hashlib,sys,json; p=Path(sys.argv[1]); b=p.read_bytes(); assert hashlib.sha256(b).hexdigest()==sys.argv[2]; n={"__file__":str(p),"__name__":"_externally_verified_readonly_verifier"}; exec(compile(b,str(p),"exec",optimize=0),n); print(json.dumps(n["verify"](sys.argv[3]),sort_keys=True))' /Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7/audits/existing_publication_remaining34_preparation02/verify_closed_preparation.py f216d57a5cbc81650a871641e3e955703d2fee59d18778f11675dea735c67900 EXTERNALLY_PINNED_FINAL_MANIFEST_SHA256
```

The verifier authenticates each helper's captured compile buffer against the closed manifest before execution. It reuses its already authenticated source and CAS modules during nested replays. All bridge activation remains separately subject to fresh whole independent/root review, current individually adopted semantic DATA and fixed-role authority files. A passing packet verifier supplies no append authority.
