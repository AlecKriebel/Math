# Pass 4: determinant redistribution and actual cutoff geometry

E-6322, 2026-10-16. This note records precise constraints on structured inverse additions. They limit proposed proof steps, not the possible truth of E-6322.

## 1. A compact rank-one addition cannot improve the determinant everywhere

Let v be an exact inverse and H=Dv. Its cofactor satisfies weak Piola and belongs to L^{9/4}. For a smooth compact scalar phi and a fixed coordinate vector e_i, consider

v_t=v+t e_i phi.

The determinant is exactly affine:

K_t=K+t (cof H)_{i dot} dot grad phi.

The increment is integrable. Weak Piola gives

integral_D (cof H)_{i dot} dot grad phi=0.

Therefore if the determinant increment is nonnegative almost everywhere, it is zero almost everywhere; the same holds for a nonpositive increment. A compact single-component addition which changes K must increase it somewhere and decrease it elsewhere.

In particular, replacing K pointwise by min(K,L) without compensating elsewhere is not the determinant of such an addition unless the truncation changes nothing. This conservation issue is separate from the much harder gradient compatibility and finite-energy issues.

It does not rule out a useful redistribution which decreases large K and increases small K. Constructing that redistribution requires solving a transport equation along the rough cofactor-row field, with the correct boundary/support conditions and control of all terms of V. Those steps are not supplied by the scalar truncation formula.

## 2. An affine cutoff can fail even at a genuine minimizer

The sign obstruction to convex interpolation occurs even when the starting map is a genuine globally minimizing smooth affine diffeomorphism.

Take Omega=B_1 and R=diag(-1,-1,1), a proper rotation. Prescribe the allowed full boundary trace g(x)=Rx. Strict convexity in F in the polyconvex representation, together with the null-Lagrangian mean identities, makes y(x)=Rx the unique primal global minimizer. Its actual inverse is v(z)=Rz on D=B_1, and det Dv=1.

Choose a smooth cutoff eta compactly supported in D, with values in [0,1] and equal to 1/2 on a nonempty ball. Consider the natural affine interpolation

v_tilde=(1-eta)v+eta Id.

It differs from v by a smooth compactly supported field and preserves the prescribed inverse boundary trace. Nevertheless, on the ball where eta=1/2,

Dv_tilde=diag(0,0,1),

det Dv_tilde=0.

Thus its V energy is infinite. All starting maps and cutoff data are smooth, and the starting map is a genuine minimizer. The failure lies solely in this attempted comparison's determinant barrier. The compact-addition theorem correctly treats it as an infinite-energy comparison; it does not make it a finite replacement.

This is not a counterexample to E-6322: the actual minimizer has determinant identically one. It is a counterexample to the assertion that a smooth inverse cutoff toward an arbitrary positive-determinant affine reference automatically has finite energy.

## 3. Remaining structured possibility

The accepted theorem in `../literature/STRUCTURED_NATURAL_EXPONENT_COMPARISONS.md` now proves inverse-class closure for smooth graph transformations u(z)=Phi(z,v(z)) that fix a boundary collar, conditional solely on the resulting V energy being finite. This includes natural affine cutoffs whose differences are only W^{1,9/5}. That class-closure issue is therefore resolved for this structured family. Sections 1–2 and the isolated-amplitude example in `FINITE_ADDITION_INTERVALS.md` show that finite V and positive determinant still need an actual construction.

No arbitrary inverse cutoff, affine interpolation, determinant clamping, or energy-finite amplitude interval is assumed in this pass.
