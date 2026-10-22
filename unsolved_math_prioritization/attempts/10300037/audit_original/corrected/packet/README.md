# 10300037: even-sided lamination complement audit and partials

**Disposition: unresolved in this packet, 5/5 substantive mathematical approaches. Independent scoped audit accepted after corrections; see the companion AUDIT.md.**

Delman–Roberts have publicly announced persistence for non-torus alternating knots, using the relevant even-meridional-cusp geometry. This packet does not contradict that announcement or claim the original question is currently open. It has not verified a complete universal proof. Its purpose is a qualified mathematical attempt and source-status correction, not a new solution.

The five routes in PROOF.md are: parity/cover descent, peripheral surgery arithmetic, an explicit analytic saddle filling, a global double-diamond sufficient subclass, and connected-sum gluing with its geometric limitation. The local lemmas are proved for their stated models; the global subclass inputs are credited to their authors. Lookup, auditing, code checks, and packaging are not counted as approaches.

Read PROOF.md for full statements, dependencies, and the precise remaining gap. SOURCE_AUDIT.md explains the announced-versus-inspected distinction and the corpus terminology correction. APPROACH_LEDGER.json records outcomes. CLAIMS.json fixes conservative scope. SOURCE_PINS.json and CORPUS_BINDINGS.json contain only public-source/corpus verification metadata, without source text or dataset contents.

## Verification

Run `python3 bootstrap.py` from the enclosing frozen directory. This authenticates AUTHOR_MANIFEST.json against an external constant and verifies every packet file before executing verify.py. The bootstrap itself must first be compared to its separately supplied SHA-256 receipt; a replaced trust anchor is not self-authenticating. The packet verifier is read-only and uses only the Python standard library. Run `python3 test_bootstrap.py` for normal, -O, -OO, relocated read-only, byte-tampering, malformed/schema, missing/extra-path, symlink and code-before-authentication controls.

If the private source and corpus files are available separately, `python3 packet/verify_inputs.py SOURCE_DIRECTORY CORPUS_DIRECTORY` checks the pinned PDF bytes and the entire corpus files plus canonical selected records. Those inputs are intentionally not distributed in this packet. The default bootstrap does not claim to re-fetch or inspect external sources.

Finite exact checks are regression controls for formulas and bookkeeping, not proofs of general topology or independent mathematical peer review. Nothing is uploaded, merged, or published by these scripts.
