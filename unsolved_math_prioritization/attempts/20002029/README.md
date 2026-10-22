# Critical-weight conformal invariants from Schouten jets

Problem 20002029 / AIM-GEOMETRY-0367, originally Robin Graham's Problem 10 at the 2003 AIM workshop on conformal structure.

**Status: partial results, five substantive attempts; the general problem remains unresolved.** This package gives a dimension-six nonexistence proof and several exact obstruction certificates. All claims remain subject to fresh independent review. It makes no priority, novelty, peer-review, or general-resolution claim.

The original question concerns even dimensions n>=4 and pointwise scalar conformal invariants of weight -n that admit universal polynomial formulas made only from complete metric contractions of covariant derivatives of the Schouten tensor. There is no conformally-flat or global-integral qualification.

## Results

1. **Undifferentiated-factor elimination.** An invariant whose every monomial contains an undifferentiated P factor vanishes. At critical weight this excludes candidates supported wholly on lengths L>n/3.
2. **First-jet nonexistence.** Every negative-weight polynomial scalar conformal invariant built only from P and nabla P vanishes in dimension n>=4. The proof uses explicit Cotton translations and a finite-jet metric construction.
3. **Dimension six.** The classical three-generator conformal-invariant classification and three explicit Ricci-flat Riemannian metrics give a restriction matrix with determinant -65536/3125. This proves the original nonexistence statement for n=6, subject to review.
4. **Two dimension-eight examples excluded.** The entire span of the two explicit critical divergence invariants in Case et al., arXiv:2404.11319v4, equation (3.4), has no nonzero pure-Schouten representative. Two Ricci-flat witnesses give determinant -448/9.
5. **A limit of the test method.** A nonzero conformal invariant of weight -8, the squared norm of a Weyl Pontryagin four-form, vanishes on every diagonal-curvature/Kasner metric. Thus no number of such tests can certify the entire dimension-eight invariant space.

The n=4 negative answer was already recorded in the original AIM source. No full proof for even n>=8 or counterexample in those dimensions is provided here. In particular, the dimension-eight blind-spot invariant is not claimed to have a Schouten-only formula.

## Files and reproduction

The complete proofs and the unsuccessful general-dimension route are in ATTEMPT_1.md through ATTEMPT_5.md. SOURCE_GATE.md records the precise source scope and bibliographic limits.

Run from this directory:

    python checks/verify_cotton_span.py
    python checks/check_kasner_restrictions.py
    python checks/verify_divergence_restrictions.py
    python checks/verify_kasner_blindspot.py

The dimension-six script requires SymPy; the other checks use Python's standard library. Author reproduction used Python 3.12 and SymPy 1.14.0. The four saved .result.json files record successful exact runs. Finite checks validate displayed certificates and identities; they are not substitutes for the general proofs or an exhaustive classification.

## Primary references

- AIM, [Conformal Structure in Geometry, Analysis, and Physics](https://aimath.org/WWN/confstruct/confstruct.pdf), 2003, Problem 10, PDF page 24.
- L. J. Peterson, ed., [Future Directions of Research in Geometry](https://arxiv.org/abs/0708.2170), SIGMA 3 (2007), 081; Graham's two-part characterization conjecture.
- C. Fefferman and C. R. Graham, [The Ambient Metric](https://arxiv.org/abs/0710.0919), 2012; equations (6.3), (9.3), Proposition 6.5, Theorem 8.3, Proposition 8.4, and Theorem 9.4.
- J. S. Case, A. Khaitan, Y.-J. Lin, A. J. Tyrrell and W. Yuan, [Computing renormalized curvature integrals on Poincare–Einstein manifolds](https://arxiv.org/abs/2404.11319), v4, 20 April 2026; equation (3.4).
