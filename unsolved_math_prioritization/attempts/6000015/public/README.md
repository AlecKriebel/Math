# 6000015: Stein tangent bundles of complete Hessian manifolds

**Partial result; original target unresolved after five substantive attempts.**

The main proved special case is that T(Ω/Γ) is Stein for every open line-free polyhedral Ω and every free properly discontinuous affine Γ, without compactness of the base. The proof uses facet logarithms and a proper strictly plurisubharmonic exhaustion on a strip quotient by a real lattice.

Additional results:
- an exact complete Kähler lift of every complete Hessian metric;
- a complete Hessian two-torus whose squared fiber norm has a negative Levi direction surviving all scalar reparametrizations with positive derivative;
- Steinness of arbitrary convex translation quotients and of one-dimensional tangent manifolds;
- a continuous, generally non-strict plurisubharmonic exhaustion for compact line-free convex quotients.

Read [PROOF.md](PROOF.md) for all claims, hypotheses and the remaining gap, [SOURCE_GATE.md](SOURCE_GATE.md) for source/prior-result boundaries, and [ATTEMPT_LOG.md](ATTEMPT_LOG.md) for the five mathematical approaches.

## Reproduce

Run `python verify.py` with Python 3 and SymPy (tested with 1.14.0). The deterministic JSON should match [verification_results.json](verification_results.json). It contains 60 exact identities and finite controls: affine-support Levi matrices, torus eigenvalues and obstruction, cubic symmetry, strip-barrier and lattice-projection formulas, a nonsimplicial facet example, and the support-envelope degeneracy. These supplement the written proofs; they do not prove the unresolved general theorem.

`FROZEN_MANIFEST.json` records the SHA-256 digest and byte length of each frozen author file. Source reading copies and private records are not publication material. The work is AI-assisted and unrefereed; independent review, when available, is a separate record. No priority claim is made.
