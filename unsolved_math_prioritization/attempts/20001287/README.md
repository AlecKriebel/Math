# Spherical simplex volume products

**Problem:** 20001287 / AIM-CONVEX_GEOMETRY-0019, rank 510.

**Original target:** H. Koenig's Question 23 in the AIM list *Mahler's conjecture and duality in convex geometry*, printed page 4.

**Author-stage result:** Complete affirmative deduction from established literature, including equality cases. Fresh independent review pending. No novelty or first-resolution claim.

For every full-dimensional pointed simplicial cone `C ⊂ R^n`, with normalized solid angle `ω` and positive dual `C*`,

\[
 \omega(C)\omega(C^*)\leq4^{-n}.
\]

Equality holds exactly for orthogonal images of the positive orthant. In ordinary spherical measure the sharp value is `vol(S^{n−1})²/4^n`. This is the full original question, rather than just the wedge–orthant family named in the problem index.

The argument is a Gaussian application of geometric-mean Prékopa–Leindler. Its inequality and equality cases are already contained in the framework of Fradelizi–Meyer (2007), Proposition 1; Lehec (2009) explicitly gives the corresponding simplicial-cone/dual-cone integral estimate. This note spells out the deduction and normalization. It does not establish when the AIM question was first explicitly recognized as answered.

A source correction matters: the original PDF defines the positive spherical dual with `≥ 0`; the extracted `> 0` is an OCR error. The volume is unchanged by that boundary difference for the intended simplices.

## Contents

- `PROOF.md`: complete proof, exact scope, equality cases, and primary references
- `LOCAL_EXPANSION.md`: auxiliary all-direction orthant Hessian, not needed for the complete result
- `SOURCE_GATE.md`: source recovery, literature attribution, and prior-attempt checks
- `RESEARCH_LOG.md`: three substantive approaches, stopped early after the full classical deduction
- `check_exact.py` and `exact_results.json`: reproducible finite exact algebra checks
- `FROZEN_AUTHOR_MANIFEST.json`: frozen file hashes for independent review

## Reproduction

Run `python check_exact.py` with Python 3 and SymPy. It checks 18 rational invertible generator matrices in dimensions 1–6, the dual and inverse-Gram formulas, the square certificate for quadratic Young, determinant cancellation, the normalization, and the auxiliary Hessian identities in dimensions 2–8. It performs no network calls or numerical integration.

The checker supports the algebra. It does not replace Prékopa–Leindler, its equality theorem, or the universal proof.

## Primary sources

- [AIM Problem 23](https://aimath.org/WWN/mahlerduality/mahlerduality.pdf)
- [Fradelizi–Meyer, geometric-mean Prékopa–Leindler with equality](https://arxiv.org/abs/math/0609553)
- [Lehec, positive-orthant and dual-cone integral inequalities](https://arxiv.org/abs/1011.2119)
