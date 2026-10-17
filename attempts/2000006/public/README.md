# E-6322: five-pass mathematical checkpoint

**AMR-019-0006 / AMR0190006 · queue row 1791 · UNSOLVED 5/5 · 16 October 2026**

This checkpoint preserves complete authored proofs, mathematical audits, acceptance reports, public bibliographic/inspection metadata, and auxiliary checkers from five completed research passes. It contains rigorous partial progress, not a solution. No novelty, exhaustive literature coverage, or formal proof-assistant certification is asserted.

## Exact benchmark and broader source question

For arbitrary finite positive a,b,c,d, in three dimensions set

W(F) = a|F|^6 + b|cof F|^3 + c(det F)^2 + d(det F)^(-2)

on det F>0, and W(F)=infinity otherwise. Omega is an arbitrary nonempty bounded connected smooth domain. The full boundary trace is that of a smooth orientation-preserving diffeomorphism defined near the closure. Every finite-energy W^{1,6} map with that trace is a competitor; injectivity and higher regularity are not extra admissibility assumptions.

The unresolved assertion is that every full-class global minimizer has its own epsilon>0 with det Dy>=epsilon almost everywhere on all of Omega, including arbitrarily thin boundary collars. Epsilon need not be uniform over different minimizers or data. Arbitrary allowed nonaffine traces and arbitrary positive coefficients are part of the assertion. Neither this theorem nor an actual compliant global minimizing counterexample is supplied.

The complete [frozen target](recovery_elasticity_1791_20261015/formulation_gate/RESEARCH_TARGET.md) is retained byte-for-byte. Its formulation-stage label is historical; the terminal investigation status is UNSOLVED 5/5.

[Ball, Some Open Problems in Elasticity (2002)](https://people.maths.ox.ac.uk/ball/Articles%20in%20Conference%20Proceedings%20and%20Books/JMB%202002%20re%20Marsden%2060th.pdf), Problem 6 and equation (2.19), concerns a broader adequate-growth program. This benchmark fixes one exponent tuple and a full-class global-minimizer question. A solution would establish one sufficient-condition branch; a counterexample would refute that branch without settling all other growth laws. Conditional, planar, symmetric, small-data, restricted-class, or interior results do not settle either question by relabeling.

## Accepted results and exact remaining gap

- The polyconvex existence baseline and actual almost-everywhere inverse are justified. The inverse has gradient in L^{9/5}, cofactor in L^{9/4}, determinant in L^3, and the prescribed full inverse trace. This is not everywhere injectivity. A full-boundary transported Piola characterization and energy-bounded closure of the exact inverse class are proved.
- Safe inner/outer variations, genuine compatible finite-energy comparison mechanisms, componentwise coercivity, boundary-collar comparisons, and weighted inverse-cube moments are established. The multicomponent endpoint moment retains all nonnegative endpoint and mixed-determinant hypotheses.
- Whole-boundary positivity follows under explicit additional gradient regularity, including a modulus omega with liminf as r decreases to zero of omega(r)^2[1+integral_r^R omega(t)dt/t]=0. A uniform logarithmic modulus exponent greater than 1/3 suffices. No such regularity is proved for arbitrary minimizers.
- Exact weighted cores and specified strong weighted annular profiles are excluded with their stated smoothness, determinant, and scaling assumptions. The critical-axis diagnostic family is nonstationary. There is no tangent-existence theorem or complete singularity/boundary classification; all diagnostic collapsing maps remain nonminimizers.
- A legitimate compensated inverse repair transferring mass m from determinant K>=lambda to K<=kappa must satisfy 3d(lambda^2-kappa^2)m<=R. A fixed signed first-cost bound R<=C0 m for suitable repairs at every positive-measure high level would bound K and prove the benchmark. Actual finite-energy triangular material comparisons are available, but minimizer-specific level alignment and uniform cost per transferred mass have not been constructed. Universal-matrix and expensive-prescribed-repair obstructions do not rule out better tailored repairs.

The missing bridge is an unconditional whole-boundary estimate or an adequate compatible high-level repair family for arbitrary minimizers, or a genuinely minimizing counterexample. Unrestricted natural-exponent inverse additions, boundary-only degeneration, identically rank-deficient limiting profiles, remaining subcritical degeneracies, and weaker/nonexistent power tangents remain outside the proved results.

## Reading guide

Start with the [final acceptance report](research_elasticity_1791_pass5_20261016/audit/FINAL_ACCEPTANCE_REPORT.md) and [final adversarial review](research_elasticity_1791_pass5_20261016/audit/ADVERSARIAL_REVIEW.md). They qualify and consolidate all earlier statements. The [complete proof index](PROOF_INDEX.md) links every retained mathematical narrative, including all five original audits. The reports are complete, not excerpts.

## Reproduction

Python 3.12.14 and the versions in requirements.txt reproduce the recorded output bytes. The original final exact checker deliberately checks byte identity, including software metadata, so a different interpreter/library version may fail historical byte identity even when the mathematics is unchanged.

Run `python verify.py` for the payload and original acceptance-chain hashes. Run `python replay.py` for the auxiliary computations. Both leave this checkpoint unchanged; replay uses disposable clean copies and has no network requirement. Release gates remain active under -O/-OO, and historical checker assertions are explicitly kept enabled. Run `python test_release_guards.py` for the 72-case adversarial release matrix; see [optimization-safe replay](PORTABILITY_FIX.md). See [replay scope](REPLAY_SCOPE.md) for check-by-check coverage and the distinction between fresh algebra replay and historical source-document verification.

## Publication boundary

The payload contains no third-party PDF, source-text extract, rendered source page, dataset contents, private source, private coordination file, or personal content. Public scholarly-source titles, URLs, hashes, sizes, retrieval limitations, and historical inspection results are retained. Source-document byte checks are not represented as fresh checks when their documents are excluded. No external publication, commit, or push is performed by this package.
