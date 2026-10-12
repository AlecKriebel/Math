# Bounded adversarial report: peripheral projection and observable topology

UTC checkpoint: 2026-10-05 19:09. Completion of this bounded family: 100%.
PR 91, problem 30003052 / OWR-14215-004.
Immutable head: `2ea84c5de45cb92783b5b55057af1f52590be6bf`.

**Verdict: pass for the peripheral mechanism, the exact unimodular point
spectrum, and the complete J-empty spectral row.** No counterexample or
mathematical defect was found in the original classification's Sections 2–4
and 6 under the exact stated finite-dimensional contraction hypotheses.
This is a bounded mathematical audit; it makes no priority, originality,
publication-readiness, or human peer-review determination.

## Independence and authenticated body

The independent obligations and complete mathematical reconstruction were
written before reading `CLASSIFICATION.md`. The reconstruction uses the
contractive spectral projection, uniform stable-orbit comparison, and dense
coordinate polynomials with Cesaro averaging. Afterwards the preserved
classification body was read in full to compare the actual proof.

That body is 11040 bytes, SHA256
`0abd5dd0918905b3a6c1e9c62a57097645bba6334cb625a4a4e88f2c12c4416b`.
Its independently computed Git blob SHA1 is
`5372a75fe97b87f7e6d135c62ed0f2504b566e00`, agreeing with the supplied original
manifest. The body's association with the immutable head and mode `100644`
is supplied by that manifest; this family did not redo the root's complete
20-file Git/mode authentication.

No author's reviewer, author replay, source checker, source verification, or
historical source body was read. No outside individual was contacted. No
Git/index/branch, native proof, PR, release, Zenodo, or tracker mutation occurred.

## Verified claims and failure modes tested

| Obligation | Original body location | Bounded conclusion |
|---|---|---|
| Peripheral Jordan blocks are semisimple | lines 49–60 | Power boundedness excludes a length-two Jordan chain by reverse triangle inequality; every longer block contains one. Stable Jordan blocks are allowed and decay. |
| Recurrence gives unbounded indices | lines 62–69 | Compact-torus convergent subsequences with growing index gaps furnish n_j tending to infinity and all peripheral phases tending to 1. The original shorthand recurrence claim is valid. |
| P is contractive for the actual norm | lines 68–77 | Operator-norm convergence of contractive powers proves ||P||<=1, without orthogonality. An explicit valid oblique example has Euclidean ||P|| squared equal to 5 but supplied-norm ||P||=1. |
| Every orbit comparison remains in U and is uniform | lines 85–98 | A^n x and A^n Px belong to U, and the stable difference is bounded by ||A^n(I-P)||. Compactness gives uniform continuity and hence uniform observable convergence. |
| Nonzero eigenfunctions survive restriction | lines 100–103 | f=fP and P(U)=V force f|V nonzero. Pullback hP supplies the reverse correspondence. |
| Exact group Gamma, rather than closure(Gamma) | lines 116–140 | Coordinate/conjugate monomials supply every group element. The self-adjoint separating algebra is dense in C(V); contractive Cesaro means kill each fixed polynomial for lambda outside Gamma and hence kill any alleged eigenfunction. |
| Dense-group boundary does not introduce eigenvalues | lines 132–140 | The polynomial is fixed before taking the average length to infinity. No uniform frequency gap over the dense group is assumed. |
| Full peripheral spectrum | lines 142–144 | Invertible isometry gives spectrum in the circle. Dense Gamma fills it by closedness; finite Gamma gives K_B^q=I and an explicit polynomial resolvent outside Gamma. |
| J-empty nilpotent complement and zero | lines 195–218 | Q=fP gives closed commuting summands. The complement is nilpotent and nonzero exactly when F is nonzero, contributing precisely spectral and point eigenvalue 0. |
| E=0, A=0, A=I, repeated phases | lines 77, 144, 220–223 | Singleton peripheral ball gives Gamma={1}; nonzero nilpotent space gives {0,1}; identity gives {1}; repeated phases only repeat valid monomial weights. |

The exact proof, including explicit estimates and a polynomial resolvent, is in
`INDEPENDENT_PROOF.md`. There is no unsupported transfer of this family's
central difficulty to an equivalent claim. Stone-Weierstrass is used with all
its compact-space hypotheses explicitly checked, not with a substitute
observable space or an invariant-measure assumption.

## Reproducible finite controls

Run from the canonical checkout:

```text
python3 draft_pr_publication_program_20260930/audits/pr91_30003052/peripheral_projection_adversary_20261005/adversary_checks.py
```

Actual execution UTC `2026-10-05T19:08:26.659331+00:00`, PID 26677, exited 0.
All six independent finite controls passed:

1. A two-dimensional oblique projection in an explicitly adapted complex norm,
   including exact power gaps 2^(-n).
2. A peripheral phase -1 with a stable nontrivial Jordan block and oblique P;
   even powers converge to P, while odd powers approach -P.
3. A rejected peripheral Jordan candidate, with exact powers [[1,n],[0,1]].
4. Exact monomial weights for peripheral phases i and -1, yielding all fourth
   roots through nonnegative coordinate/conjugate exponents.
5. Exact cyclotomic Cesaro cancellation for a primitive eighth root outside
   the fourth-root group.
6. Exact nilpotent/peripheral splitting, a concrete zero eigenfunction, and
   the E=0 nilpotent endpoint.

`CHECK_RESULTS.json` records actual process metadata and the evidence. These
controls are supplementary falsification attempts. They do not approximate the
infinite-dimensional operator spectrum; the analytic proof supplies that result.

## Strongest result and exact remaining gap

For every stated A, this family verifies

    sigma_p(K_A) intersect T = Gamma.

It also verifies, whenever J is empty,

    sigma_p(K_A) = Gamma union Z_A,
    sigma(K_A)   = closure(Gamma) union Z_A.

The J-nonempty interior eigenfunction construction and full closed-disc spectrum
were not independently audited by this family, even though their text appears
in the classification read for comparison. Historical-source identity,
attribution, priority, the original research budget, and global promotion
decisions belong to the root's separate work. The root subsequently supplied
local primary-PDF paths and hashes; this family has not read those PDFs. Those
are scope limitations, not detected defects in the
local mechanism. No repair of the original Sections 2–4 or 6 is required by the
findings of this family.
