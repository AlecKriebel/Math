# Real-variable Nyman criterion: audited partial results

Problem 30002495 / OWR-12866-002, queue rank 986. **Unsolved, 5/5.** No proof of RH, its negation, or the full methodological equivalence is claimed. No novelty claim is made.

- original/: full frozen authored proofs, five-approach ledger, source-scope notes and finite controls
- independent_audit/: full independent mathematical audit, exact optimization-safety patch, corrected checker, and reproducible audit controls
- corrected/: separately rehashed adoption of the same full author packet, with all 16 assertion sites replaced by explicit checks
- ROOT_ACCEPTANCE.md: precise accepted scope, correction, endpoint warning, and remaining gaps
- VERIFY_PUBLICATION.py, TEST_MUTATIONS.py, MUTATION_RESULTS.json and PUBLICATION_MANIFEST.json: externally anchored integrity, exact-patch replay, and finite-control checks

The actual Möbius endpoint H2 moment diverges. The conditional endpoint hypothesis is a failed-route diagnosis, not a viable RH proof approach. Local damped convergence and subcritical bounds leave the global endpoint estimate unproved.

## Trust and reproduction

Obtain the publication-manifest SHA-256 and verifier SHA-256 from the external draft-PR description or another independently trusted record. Do not derive both trusted values from the packet under examination. Bootstrap the verifier before executing it:

```sh
python3 -I -B -c 'import hashlib,pathlib,stat,sys; p=pathlib.Path(sys.argv[1]); d=p.read_bytes() if stat.S_ISREG(p.lstat().st_mode) else b""; h=hashlib.sha256(d).hexdigest(); h==sys.argv[2] or sys.exit("Verifier bootstrap mismatch"); sys.argv=[str(p),*sys.argv[3:]]; exec(compile(d,str(p),"exec"),{"__name__":"__main__","__file__":str(p)})' VERIFY_PUBLICATION.py TRUSTED_VERIFIER_SHA256 --expected-manifest TRUSTED_MANIFEST_SHA256
```

The default replay explicitly tests ordinary, -O, and -OO children. For one child mode use --mode ordinary, --mode optimized or --mode double_optimized. --check-only verifies bytes, inventory, binding and exact patch replay without running the control programs.

After the bootstrap succeeds, run:

```sh
python3 -I -B TEST_MUTATIONS.py --expected-manifest TRUSTED_MANIFEST_SHA256 --expected-verifier TRUSTED_VERIFIER_SHA256
```

Only Python's standard library is required for verification; full mutation tests require a POSIX filesystem for FIFO and symlink controls. Verification is offline. Runtime version is metadata and is excluded only from the audit receipt comparison; other claimed deterministic receipts are compared byte-for-byte. The published original checker is historical evidence and must not be used as an optimization-safe checker; use corrected/ or the outer verifier.

This is an AI-assisted, unrefereed report and independent AI audit, not human peer review or a formal proof certificate. No source copies, source extracts, dataset contents, or private coordination material are distributed.
