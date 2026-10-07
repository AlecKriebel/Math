# Acceptance report: problem 30004818

7 October 2026. Rank 944. Five completed author approaches; full solution not obtained.

## Result

**Accept all five retained mathematical partial results within their stated scope.** No change to a mathematical conclusion is required. The OWR orientable-product existence question remains unresolved by this package.

1. Finite-image covering: if the image has order d, the connected lift has d boundary circles and genus 1+d(g−1). Standard bottom-collar bands give g₄(#ᵈK)≤dg and therefore g_st(K)≤g. The exact Boden–Nagel punctured-manifold compression hypotheses are satisfied.
2. Image-subgroup covers: the original surface lifts unchanged. The explicit abelian Kleinian quotient models embed in S³, proving the stated abelian-image hyperbolic obstruction and excluding genus-one savings in complete orientable hyperbolic manifolds.
3. Equivariant and companion tests: the orientation-preserving free annulus quotient is impossible. The disjoint two-component link-concordance criterion gives genus at most one; with r spectator intersections the proven bound is only 1+r. No required equivariant surface or disjoint link concordance has been constructed.
4. Product intersection obstruction: the local-boundary relative class vanishes over Z, even with torsion in H₁(M), and the absolute intersection form is zero. The stated closed algebraic dual and intersecting-tori transplantation are excluded. The capped absolute class need not vanish.
5. Concordance norm and Floer bound: a valid single-surface strip insertion establishes the norm properties without a disjoint-surfaces assumption. Hedden–Raoux's actual relative-adjunction theorem, local connected-sum filtration, nonzero Floer classes, and conjugate Spinᶜ structures prove |τ(K)|≤g_{M×I}(K) for every closed connected oriented M. The cap-class pairing is retained and canceled correctly.

Miller's exact order-two, arbitrarily large topological four-genus family is a valid surviving test family. It is not a verified orientable-product counterexample. The work makes no novelty, human-review, or formal-proof claim.

## Evidence

- Full proof audit: `MATHEMATICAL_AUDIT.md`
- Detailed primary-source Floer check: `floer/FLOER_AND_MILLER_AUDIT.md`
- Frozen input identity: `input_pins.json`
- PDF hash and independent text-extraction correspondence: `source_reextraction_checks.json`
- Reproducible arithmetic/integrity checker: `verify_audit.py`
- Finite-check output: `independent_checks.json`
- Optional exact textual clarifications: `OPTIONAL_CLARIFICATIONS.diff`
- Patch verification: `patch_dry_run.json`
- Output pins and explicit artifact/exclusion lists: `AUDIT_MANIFEST.json`

All seven authored-file byte counts and hashes match the supplied manifest. All ten original source PDFs were freshly extracted; each text matched its saved extraction byte for byte. The independent verifier passes 601 covering cases, 23 saved equivariant cases, 1,001 smoothing cases, 40,401 norm triangle inequalities, and 2,001 determinant cases. Those are arithmetic checks, not certificates of the geometric proofs.

## Clarifications and preservation

The optional patch expands the strip model, gives an explicit general Floer nonvanishing citation, fixes F₂/basepoint/cap/reversal conventions, and turns the source report's stale one-approach count into a historical note. These are editorial/citation clarifications and are not necessary to rescue a false theorem. The patch was tested only on temporary copies. Original authored files remain byte-identical.

Downloaded primary PDFs, their extracted text, and source screenshots are not authored publication deliverables. Do not publish this directory wholesale; use only the explicit authored-artifact allowlist in the manifest. No repository, queue, branch, PR, or publication was changed by this audit.
