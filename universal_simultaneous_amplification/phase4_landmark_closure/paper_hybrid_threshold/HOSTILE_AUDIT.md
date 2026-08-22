# Paper II hostile-audit ledger

Date: 2026-08-21 (America/Los_Angeles)

This ledger distinguishes proof obligations from exact computational checks.
It contains no claim that a numerical solve proves an asymptotic statement.

| Obligation | Required hostile check | Evidence boundary |
|---|---|---|
| fitness-independent family | every graph parameter, including the dyadic weak cut, is selected before fitness is quantified | analytic theorem proof |
| graph class | every finite graph is connected, loopless, undirected, and positively weighted on its stated edges | construction inspection |
| finite strong lumping | both update kernels commute with the stated orbit action | proof plus 512-state/108-fibre labelled audit |
| weak-cut trace | fast mixed states are transient and the Schur complement gives introduction rate times local fixation | analytic finite-state proof |
| gain-scale uniformity | cut error and center errors are `o(q/C)`, not merely `o(1)` | analytic compact-uniform estimates |
| center establishment | stopped drift comparisons cover the route from one core mutant to a density strip | analytic proof |
| center cleanup | the density strip reaches full fixation, including pendant cleanup, with failure negligible at gain scale | analytic proof |
| reciprocal invasion | reverse-fitness portal values are `o(C^{-1})` uniformly on each fitness compact, which is the scale needed by the sweep | analytic proof |
| pair gate | all four introduction rates have the stated orientation and yield `Z_B` and `Z_D` | rate derivation plus exact coefficient audit |
| global sweep | the two-coordinate macro chain retains adverse reversals and controls all `q` satellites | analytic proof |
| response functions | center, pair, pendant, and baseline terms occur on one common scale with correct signs | exact algebra plus analytic estimates |
| sextic threshold | root count, quadratic minimizer, tangency, and derivative signs are exact | two symbolic certificates |
| rational-edge family | endpoint margins and algebraic threshold are exact | symbolic certificate |
| claim boundary | optimality is limited to fixed positive parameters in the displayed first-order response model; no unrestricted upper bound is inferred | abstract, theorem, discussion, and package integration audit |
| computational boundary | replay coverage is not described as a computer proof of the weak-cut or population asymptotics | Data and Code Availability and package notes |

The finite affine-separator calculation from the v1 package is intentionally
absent.  It is not load bearing: the main theorem includes fitness `3/2`, so
a sufficiently large graph already has both normalized fixation ratios above
one there.  The sparse numerical core diagnostic is likewise absent from the
public replay and release archive.

## Final verdict

Three independent final reviewers re-read the corrected theorem chain and
the frozen manuscript after the literature update, major-revision response,
and targeted specialist rereview.  In particular, they re-audited the adapted
hidden-coordinate drift, explicit stopped cleanup recursion, adverse pendant
reset, killed-Green tail, finite-horizon immigration maximum, and rule-specific
reciprocal renewal at the claimed gain scales.  No substantive
theorem, rate, scale, quantifier, citation, rendering, replay, or package
objection remained.  The deterministic archive was independently regenerated and
clean-extracted; its internal manifest, pinned replay, and byte-identical PDF
rebuild all passed.  Human confirmation of contact, funding,
competing-interest, contribution, license, and portal fields remains an
explicit pre-submission gate rather than a research-package claim.
