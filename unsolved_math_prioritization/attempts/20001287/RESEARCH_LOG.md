# Research log: three substantive approaches and early completion

Problem 20001287 / AIM-CONVEX_GEOMETRY-0019. Date: 2026-10-03.

The five-approach budget was stopped after the third substantive route supplied a complete proof of the exact original target from established literature. The counting below records mathematical approaches, not tool calls or source searches.

## 1. Gram-matrix reduction, tensorization, and scope tests

Recovered the source and converted spherical measure to standard Gaussian cone probability. For `C=A R_+^n`, the positive dual is `A^{-T}R_+^n`; the target is exactly `q(G)q(G^{-1})≤4^{-n}` with `G=A^TA`. This avoided the frequent covariance/precision and polar-sign confusions.

Rechecked the old wedge–orthant computation and its orthogonal-product factorization. For a planar opening `α`, the relative product is `1−4(α−π/2)²/π²`; it is maximal only at a right wedge. Products of independent wedge blocks obey the product of these relative factors. These calculations do not cover coupled Gram matrices and are prior partial material.

A proposed extension using only inequalities valid for every convex cone was ruled out exactly: the circular self-dual cone of half-angle `π/4` in `R^3` has normalized product `((2−√2)/4)²>1/64`. Its violation reduces to `529>512`. Thus simpliciality is indispensable and a general-cone endpoint estimate cannot give the requested sharp result without an additional structural input.

Outcome: an exact all-matrix integral target, several calibrated subfamilies, and a clear obstruction to overgeneralization; no complete proof yet.

## 2. All-direction local Hessian at the orthant

Expanded the Gaussian orthant probability using independent half-normal moments. For zero-diagonal symmetric `H`, obtained

`4^n q(I+H)q((I+H)^{-1}) = 1 − [(2π−4)Σ h_ij²+(4−π)||H1||²]/π² + O(||H||³)`.

Both coefficients are positive. This proves strict local maximality in every fixed dimension, including coupled angular perturbations. The detailed density cancellation, normalization, uniform Taylor justification, and planar calibration are in `LOCAL_EXPANSION.md`; exact symbolic checks cover dimensions 2–8. A separate derivation using Gaussian sign moments agreed with the coefficients.

Outcome: a rigorous local result; it did not by itself exclude a larger product far from the orthant. Historical novelty was not established and is not claimed.

## 3. Multiplicative Prékopa–Leindler and the classical complete answer

Applied quadratic Young to the precision-matrix integrands:

`exp(−x^TGx/2) exp(−y^TG^{-1}y/2) ≤ exp(−x·y)`.

The right side is the square of a standard Gaussian evaluated at the coordinatewise geometric mean. The change `x_i=e^{u_i}` converts this to ordinary Prékopa–Leindler, including its Jacobians. It follows that

`I(G)I(G^{-1}) ≤ (π/2)^n`,

which is exactly the sharp `4^{-n}` cone-probability product after normalization.

The literature check located the precise established machinery: Fradelizi–Meyer (2007), Proposition 1, and Lehec (2009), Lemma 8 and the dual-cone step of Theorem 9. Fradelizi–Meyer's equality criterion forces `G` diagonal, giving exactly the orthogonal-orthant equality cases. No log-concavity assumption on the unconditional extensions is required.

Outcome: complete affirmative deduction for the original universal problem, with equality. Stop early at **3/5**. Classify as a literature-implied result, not a new-resolution claim. The issue of who first explicitly linked this theorem to the AIM question remains historical, not a gap in the proof.

## Final verification and handoff

The exact script passes for 18 rational generator matrices, seven Hessian dimensions, the determinant and normalization identities, the square certificate, the wedge check, and the nonsimplicial obstruction. The script is supplemental; the proof relies on the cited analytical theorem. The authored package is frozen for an independent mathematical/source audit before any publication action.
