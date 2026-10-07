# Bounded-region fermion counterexample, revision 2

Problem **30006191 / OWR-14299085-005**, queue rank 967. Disposition: **claimed_solved**, **1/5** substantive approaches.

The complete [bounded-region proof](author/BOUNDED_REGION_PROOF.md) supplies one fixed bounded ball, one smooth compactly supported potential, and one fixed normalized test function in dimension three. Explicit particle-number-dependent Slater states and times tending to zero yield annihilation differences whose vector norm and operator norm tend to 2. Both density-density and normal-ordered interactions are covered.

The witnesses vary with particle number. Strong-operator continuity survives; no fixed-vector or fixed-normal-state discontinuity is asserted. This is an existential counterexample, not a result for all potentials or dimensions, a fixed-density assertion, a CAR-invariance claim, or a historical novelty claim.

## Accepted frozen inputs

- [Author proof and controls](author/README.md): manifest SHA-256 `d6a0862cbf2f6500cc5fd7ee2239e0e8a2c5864c9d09a6cd9a13b1b4f99176ef`.
- [Complete independent audit A](audit_a/INDEPENDENT_AUDIT.md): PASS unchanged; manifest SHA-256 `75c4fdb635d14131759bc47d779c95079c719373d7f9305a649f9f60bf26bfc4`.
- [Complete independent audit B](audit_b/AUDIT_REPORT.md): ACCEPT unchanged; manifest SHA-256 `180bee30c70c810f8f92984fd4604ba7fdc25201ff2e579ed99f686935b1a6fd`.

The proof is 12,771 bytes, SHA-256 `2b7c22cfc54049a9e51fe5eb4eb283ba911e6f27e8b6e4dc9557927bc04d7350`. Each audit checked those identical final bytes independently. Author-stage statements that audits remain pending are preserved historical freeze text; the two complete acceptance reports supersede that staging status.

## Version and attribution

Revision 2 replaces an earlier prior-result disposition because a full-space theorem alone did not settle the literal bounded-interaction-region formulation. The proof here directly treats that cutoff and does not invoke a prior discontinuity theorem. The earlier packet and its scope-correction audit are retained separately, not silently rewritten or included as the accepted result.

Oliver Siebert remains credited for related literature, including [Discontinuity of Continuum Fermion Dynamics](https://arxiv.org/abs/2609.34402) and [On the thermodynamic limit of interacting fermions in the continuum](https://arxiv.org/abs/2409.10495). The original problem is in [Oberwolfach Report 7/2025](https://ems.press/content/serial-article-files/51350), printed pages 364–365 and 371. Source titles, URLs, fingerprints, and inspection records appear in [the source manifest](author/SOURCE_MANIFEST.json) and [audit B's source inspection](audit_b/SOURCE_INSPECTION.json). No source PDFs, extracted source text, or dataset contents are distributed here.

## Portable verification

With Python 3.10+:

    python verify_package.py --integrity-only

For all author and independent numerical controls, install NumPy, SciPy, and SymPy in your preferred environment, then run:

    python verify_package.py

The publication replay used Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, and SymPy 1.14.0. The wrapper validates the exact file set, sizes, hashes, and frozen manifests. It runs controls in a temporary copy because audit A writes its result beside its script. No retained source is required; optional source-byte checking is available through the frozen author and audit B scripts.

[PACKAGE_MANIFEST.json](PACKAGE_MANIFEST.json) freezes all distributed files except itself. Hashes are corruption controls, not signatures or substitutes for a mathematical proof. [PUBLICATION_VERIFICATION.json](PUBLICATION_VERIFICATION.json) records the publication-stage replay and negative controls. The finite tests corroborate identities; the written proof and full analytical audits establish the continuum and limiting claims.
