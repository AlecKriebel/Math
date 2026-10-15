# Independent covariance, source, and certificate-boundary review

Target: PR 662 / problem 2306086 / Hayman-Lingham Problem 6.86. Reviewed immutable head: `e31701151c331a6eed9224fb37a75a374ea1043e`. Date: 2026-10-15 UTC. This review is restricted to the native 24-file packet captured in `SCOPE_AND_SNAPSHOT.json`.

**Disposition: PASS for the stated qualitative fixed-point theorem and accompanying exact partial results. No mandatory mathematical or source-scope correction identified.** This does not certify an explicit or sharp quantitative answer, a formal proof, numerical interval bounds, historical priority, or present literature status.

## 1. Independent source binding and exact target

I independently retrieved the official versioned [arXiv PDF](https://arxiv.org/pdf/1809.07200v2), extracted its text, freshly rendered complete printed pages 114 and 147, and visually read both full pages, including surrounding context and the target's update. The [versioned record](https://arxiv.org/abs/1809.07200v2) identifies Hayman and Lingham and the 2018-09-21 revision. The PDF has 256 pages, 1,706,228 bytes, and SHA-256 `8e28fd4403a07e4e19a9816b7efaafddf9f475d59cf8c34a8255cb03833ed4f0`.

Printed page 114 defines S by analyticity and univalence in the unit disk with expansion f(z)=z+sum(n>=2) a_n z^n. Problem 6.86, completely contained on printed page 147, asks whether the familiar estimate

    |z0 f''(z0)/f'(z0) - 2 rho^2/(1-rho^2)| <= 4 rho/(1-rho^2)

can improve under real-on-real, equivalently real-coefficient, functions. It is phrased at a fixed evaluation point. The target itself neither repeats S nor explicitly defines rho; the packet transparently uses the standard analytic schlicht context and rho=|z0|. This is a reasonable contextual reading. The meromorphic class would not support the quoted classical inequality in this unrestricted form.

The source does not explicitly demand a sharp formula, numerical effectiveness, extremizers, or the complete variability region. Therefore the proved qualitative improvement is responsive to its literal wording. It would be unjustified to turn an unspoken demand for a sharp formula into a blocking scope defect. The conclusion must, however, retain its nonreal-point qualification. Real nonzero points do not improve, and z0=0 makes the original displayed expression zero. The dated update records the authors' historical report, not current openness or novelty.

Source metadata, page bindings, source-copy boundaries, and exact interpretation limits are recorded in `SOURCE_BINDINGS.json`. Full PDF/text/page-image inputs remain only under ignored `tmp/`.

## 2. Strongest verified theorem and load-bearing quantifiers

For S_R, the normalized real-coefficient schlicht class, put

    A_f(z)=(1-|z|^2) f''(z)/f'(z) - 2 conjugate(z).

The established statement is

    for every z in D\R, there exists epsilon(z)>0 such that
    for every f in S_R, |A_f(z)| <= 4-epsilon(z).

For real x, max(f in S_R)|A_f(x)|=4. For every compact K contained in D\R there is a single positive epsilon_K valid for all f and z in K. These are stronger quantifiers than merely having |A_f(z)|<4 separately for each f.

The area-theorem equality argument is sufficient and noncircular. The exterior odd square-root construction is single valued because F(z)/z is zero free on a simply connected disk. Its univalence follows from the univalence of F, oddness, and nonvanishing. Equality in the weighted area sum forces the higher Laurent coefficients to vanish and identifies the Koebe rotation. Applying this to a normalized Koebe transform shows that equality for the original function forces a one-ray omitted set; it does not assume the original function is itself already a normalized Koebe rotation.

Real symmetry then makes that omitted ray a real ray. Comparing the map with an appropriately scaled real Koebe map by **inverse composition**, the zero-fixing disk automorphism has derivative of modulus one. Normalization forces the endpoint distance to be 1/4 and the original map to be k_+ or k_-. The controlling scope note correctly fixes the frozen proof's word "quotient" to mean this composition.

The strict norm deficit for these two equality maps excludes equality at a nonreal point. The proved growth bound makes S normal, and normalized local-uniform limits remain nonconstant and injective. Real symmetry is closed. Derivative convergence and zero-free limiting derivative make f -> A_f(z) continuous on the compact class. Its maximum is attained, so exclusion of equality gives a strict uniform-in-f gap. Joint compactness yields the compact-set version. No unsupported switch from separate strictness to a strict supremum occurs.

The original centered expression is z A_f(z)/(1-|z|^2). Thus the strict radius is (4-epsilon(z))|z|/(1-|z|^2). On a nonzero real point, the two Koebe maps give the two opposite endpoints of the classical disk, also ruling out a smaller containing disk obtained by shifting its center. At zero, A_f(0)=2a_2 is auxiliary; it is not the degenerate source expression.

## 3. Covariance, inverse, and one-variable reduction

For real a in (-1,1), let phi_a(w)=(w+a)/(1+a w), and let g=T_a f be the normalized Koebe transform. The chain rule gives exactly

    A_g(w) = (1+a conjugate(w))/(1+a w) * A_f(phi_a(w)).

The displayed phase is correct; its reciprocal is generally wrong. Its modulus is one. The normalization factors also give T_{-a}(T_a f)=f, so the transform is a bijection of S_R. Consequently M(w)=M(phi_a(w)) for M(z)=max(f in S_R)|A_f(z)|, and reflection gives M(conjugate(z))=M(z). The independently authored controls verify this identity with an arbitrary pre-Schwarzian symbol, rather than only on special test maps.

The invariant is delta(z)=|Im z|/|1-z^2|. Both numerator and denominator transform by (1-a^2)/|1+a z|^2. The identity

    |1-z^2|^2=(1-|z|^2)^2+4(Im z)^2

puts delta in [0,1/2). For x=Re z and r=|z|, the proposed a=2x/(1+r^2+sqrt((1+r^2)^2-4x^2)) lies in (-1,1); the discriminant is (1-r^2)^2+4(Im z)^2>0. The real part of (z-a)/(1-a z) has numerator x a^2-(1+r^2)a+x, which vanishes. The formulas delta=t/(1+t^2) and t=2 delta/(1+sqrt(1-4 delta^2)) select the unique t in [0,1). Thus evaluation of M reduces to M(i t), without evaluating that unknown function.

## 4. Exact lower bounds, crossing, and limiting obstructions

Direct differentiation confirms P_{k_+/-}(z)=(+/-4+2z)/(1-z^2) and

    |A_{k_+/-}(z)|^2 = 16-48 delta(z)^2.

For h(z)=z/(1-z^2), the identity

    h(z)-h(w)=(z-w)(1+z w)/((1-z^2)(1-w^2))

proves univalence in D. Its imaginary-axis value is A_h(i t)=8 i t/(1+t^2). Applying the bijective real transforms supplies this second lower bound at every point, not just on the imaginary diameter. Hence

    max{4 sqrt(1-3 delta^2), 8 delta} <= M(z) < 4   (Im z != 0).

The branches cross at delta=1/sqrt(7). At i/2 the squared Koebe value is 208/25 and the squared h value is 256/25, so Koebe maps alone cannot be extremizers there. This is exact, separate from all ODE computations.

As delta tends to zero, the Koebe lower bound tends to four. As delta tends to 1/2, the h lower bound tends to four; z=i t, t increasing to one, realizes the latter. These are two different obstructions to one positive epsilon over every nonreal point. The controlling scope note correctly uses delta for the first obstruction. Euclidean imaginary part going to zero near a real boundary endpoint does not suffice: along z=1-e+i e, e decreasing to zero, delta^2 tends to 1/8. The independently authored controls check this counterpath exactly.

## 5. Convex-hull failure and nonlinear obstruction

The average q=(k_++k_-)/2=z(1+z^2)/(1-z^2)^2 is typically real, but q'(z)=(1+6z^2+z^4)/(1-z^2)^3 has a simple zero at z*=i(sqrt(2)-1). Its second derivative is nonzero there, so P_q has a pole.

The obstruction is stronger than the single undefined ratio. For |e|<1 let q_e=((1+e)k_++(1-e)k_-)/2. These maps remain in the convex hull and are typically real. Writing N=1+6z^2+z^4 and R=4z(1+z^2), one has q_e'=(N+e R)/(1-z^2)^3. At z*, R is nonzero and N has a simple zero, so

    P_{q_e}(z*) = N'(z*)/(e R(z*)) + R'(z*)/R(z*) + 6z*/(1-z*^2).

The coefficient N'(z*)/R(z*)=2+sqrt(2) is nonzero. Thus the relaxed functional is unbounded at that fixed point even after excluding the member with derivative zero there. These relaxed maps are not asserted to be univalent. A linear extreme-point theorem cannot repair this nonlinear ratio problem.

## 6. Loewner admissibility and numerical boundary

For u=cos(theta), p_u(w)=(1-w^2)/(1-2u w+w^2) is the average of the two conjugate-parameter Herglotz functions with unit-circle parameters exp(+/-i theta). It has positive real part in D. Finite positive-time solutions of w'=-w p_u(w) stay in D, remain holomorphic in their initial condition, preserve conjugation, and are injective by ODE uniqueness. Their derivative at zero is exp(-T). Piecewise constant switching preserves these properties.

The normalized analytic branches of h_u(w)=w(1-w)^(u-1)(1+w)^(-u-1) satisfy w h_u'/h_u=1/p_u with positive real part, proving starlikeness and univalence. Hence exp(T) h_tail(w_T(z)) belongs to S_R. For the saved endpoint tails, u=+1 gives k_- and u=-1 gives k_+. The code uses these signs correctly. The first/second derivative jet equations and the pre-Schwarzian composition formula are correct; the normalization factor exp(T) cancels from the ratio.

The four saved floating-point values reproduce, including the value near 3.61249 at i*0.45. Replaying the supplied independent RK45 calculation with isolated pinned dependencies differs from the saved values by at most 5.25e-14. A separately authored replay integrates (w,d,b=e/d), with b'=v''(w)d and manually derived rational v derivatives; it differs by at most 1.34e-14. Both numerical outputs are identical under ordinary and optimized Python. No submitted numerical module was imported, and the optimizer was not rerun.

These agreements establish that the saved evaluations reproduce within the reported floating-point comparison tolerance. They **do not** provide interval ODE enclosures, a certified strict lower-bound theorem exceeding the elementary envelope, global extremality, optimizer convergence, or a sharp upper bound. The packet already labels these values as uncertified and retains false certification flags. No mandatory repair is needed at this boundary.

## 7. Executed checks and package preservation

The submitted checker was inspected before execution. Ordinary and optimized outer invocations both pass the 24-file publication checker with replay and all 24 negative mutation cases. In each mode it replays 3,558 authored exact controls, the 32 supplied symbolic checks, and 48 supplied binding/replay/preservation checks. The optional numerical invocation also passes, adding the 16 saved numerical-reproduction checks. Temporary copied packets stayed under this review's ignored tmp via TMPDIR. Native files were not edited.

The separately authored `independent_controls.py` passes 87 checks with identical ordinary/optimized JSON: 45 mathematical/symbolic controls and 42 native snapshot/archive binding checks. All 24 native SHA-256/size bindings match the snapshot. Both frozen ZIPs match their byte counts and SHA-256 values, with exact inventories of 10 author files and 6 audit files; every member equals its native counterpart byte for byte. A final replay after all work reconfirmed native preservation.

Core checks use the program's pinned interpreter at `draft_pr_claimed_solved_600_700_20261012/tooling/math-venv/bin/python`: Python 3.12.14, SymPy 1.14.0. Optional numerical checks use a new review-local ignored venv with the same Python base, SymPy 1.14.0, mpmath 1.3.0, NumPy 2.2.6, and SciPy 1.15.3. No shared environment was changed. `TEST_RESULTS.json` binds the executed artifacts and records the exact distinctions among symbolic, binding, and numerical evidence.

## 8. Gaps, mandatory corrections, and optional refinements

Mandatory corrections: **none for the controlling scoped theorem or current packet**.

The strongest verified result is the qualitative strict improvement at every fixed nonreal point, uniformly over S_R, together with its compact-set extension, exact invariance/lower bounds, and the nonlinear relaxation obstruction. The exact remaining quantitative gaps are an explicit positive upper-gap formula, the sharp function M(i t), general nonreal extremizers, and the full variability region. Historical priority and current literature status remain independently unverified. This review does not promote those gaps to solved claims or treat them as a failure of the proved qualitative theorem.

Optional presentation refinements are to retain the controlling scope note beside any detached frozen author file (its historical unresolved/pending labels otherwise need context), and to specify the endpoint tail sign correspondence if the numerical construction is excerpted. The existing scope clarification already addresses the inverse-composition wording and delta-limit qualification. No paper drafting, outreach, remote action, or closure action was performed.
