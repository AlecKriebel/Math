# Geometric Chern classes in Arakelov cobordism: partial results

Catalogue 30003773; source OWR-16158-016; ordered row 1832.

**UNSOLVED after five research avenues.** This package does not solve or refute the original geometric arithmetic Chern-class problem. It does not prove current-literature openness.

The strongest construction is a section-dependent, vertical-supported Euler/top-Chern lift. Under the specified derived adjunction and regulator model A = fib(MGL -> j_*D), vertical support kills the target, giving A_Z ≅ MGL_Z. A vector bundle with generically nowhere-zero section therefore has a unique supported arithmetic Euler lift. Its forgotten MGL class is its top Chern class. Independence from arbitrary section changes and a full arithmetic cycle model are not proved.

For the section p of the trivial line over Spec(Z), the supported K-theory detector has length one, hence supported MGL and A classes are nonzero. The forgotten MGL class is zero. No nonvanishing, log(p) formula, or numerical degree is asserted for the forgotten A class. The mixed-characteristic oriented MGL -> KGL map and supported Koszul interpretation are imported primary theorems, not computationally verified here.

## Read and replay

- `partial_results.md`: five avenues, assumptions and remaining obstacle.
- `vertical_euler_classes.md`: strongest geometric partial, with explicit Bott normalization and Koszul degrees.
- `independent_scope_audit.md`, `vertical_euler_audit_receipt.md`, `NORMALIZATION_AUDIT.md`: mathematical acceptance and exact-version boundaries.
- `CLAIM_LEDGER.json`, `ACCEPTANCE_REPORT.md`: scope and import ledger.
- `SOURCE_GATE.md`, `SOURCE_METADATA.json`, `CORPUS_VERIFICATION.json`: bounded source recovery and public metadata only.
- `NORMALIZATION.patch`, `PROVENANCE.json`: version lineage. Original accepted Euler hash is recorded; the patched manuscript is not misrepresented as byte-identical.
- `MANIFEST.json`: exact package inventory, byte counts and SHA-256 hashes.

From this directory run `python -I -B run_checks.py`, then `python -I -B test_corruption_controls.py`. Python standard library only. Both normal and optimized Python execution are tested. See REPRODUCIBILITY.md for limitations.
