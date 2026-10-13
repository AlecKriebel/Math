# Independent mathematical audit: Leroux entropy target 30000127

## Decision and scope

**Accept the corrected packet as rigorous conditional partial results and precisely limited obstructions. The full three-state hydrodynamic Oleinik target remains unresolved, at 5/5 substantive approaches.** This audit is not a sixth approach, an unconditional hydrodynamic theorem, or a novelty claim.

The frozen original manifest has SHA256 `6e5176946e05030e4ef98dd96123036e57433c080c3e7b9207bda7812a82cc31`. Every original file was checked against it and preserved. The corrected report differs only by (i) repairing finite-scale empirical face membership for the actual source smoothers, with a uniform normalization proof, and (ii) making sharpness explicit using scalar rarefaction fans. The contextual patch records both changes and the README additions. No original proof claim was strengthened to an unconditional three-state statement.

The one error found is local to the microscopic-to-face explanation: integral normalization of a smooth kernel does not imply that its discrete weights sum to one. This does not invalidate the conditional PDE theorem or its application to strong subsequential limits, because the correction is uniformly vanishing. It is separate from the full system's initial-trace issue.

## 1. Model, scales, signs, and state space

The OWR note's exchange orientation and rates match the packet: `(1,0)` and `(0,-1)` have asymmetric rate 1; `(1,-1)` has rate 2; the fields are hole density `eta=1-omega^2` and signed spin `xi=-omega`. No creation or spin-flip process is present. For product probabilities `P(0)=rho`, `P(+1)=(1-rho-u)/2`, `P(-1)=(1-rho+u)/2`, direct summation of the transported conserved quantity over these three transitions gives currents `rho*u` and `rho+u^2-1`. Symmetric bond contributions cancel in expectation. The second constant has zero spatial derivative, so the stated PDE is correct.

Fritz–Toth v2 instead reverses the spin sign and the asymmetric ordered pairs, uses a torus, and accelerates by `n L_n+n^2 sigma_paper K_n`. The simultaneous conversion `n=epsilon^(-1)`, `sigma_paper=epsilon*sigma_micro` gives the packet's generator scaling. Its conditions become `epsilon*sigma_micro -> 0`, `epsilon*sigma_micro^2 -> infinity`, and `(sigma_micro/epsilon)^(1/3) << ell << sigma_micro`. The lower block bound diverges, while the upper implies `epsilon*ell -> 0`. The illustrative logarithmic scale satisfies each condition and each stated ratio.

These calculations do not transfer a periodic theorem to the infinite line. The saved Fritz 2012 survey, Theorem 4.1, does state strong local L1 tightness and weak entropy limit points on the line, referring to Fritz–Nagy for localization. The latter's uniqueness theorem is for a scalar relaxation with extra dynamics. The corrected packet appropriately treats the prescribed weak Cauchy equation as an input rather than claiming to re-prove infinite-volume hydrodynamics.

The coordinates are globally continuous on the closed physical triangle. Their inverse is `rho=-ab`, `u=a+b`; the image of `[0,1] x [-1,0]` lies in the triangle because

`1-rho-u=(1-a)(1-b) >= 0`, and `1-rho+u=(1+a)(1+b) >= 0`.

Conversely the root formulas give `a>=0`, `b<=0`, while the same factorizations force `a<=1` and `b>=-1`. The discriminant is `(a-b)^2`; the only degeneracy is `a=b=0`. This means zero holes and balanced charges, not the all-hole configuration `(rho,u)=(1,0)`. The Jacobian eigenvalues are `2a+b` and `a+2b`, and differentiation with respect to their own invariants gives 2 in both cases. Both Oleinik conditions therefore have the upper-bound orientation in the packet.

## 2. Natural-order obstruction and the finite ring event

For the ordered configurations used in Approach 1, the cylinder observable `1{omega_1=1}` is increasing and equal to zero at both initial states. The sole bond that can bring a positive spin to site 1 has rate `sigma+2` in the lower configuration and `sigma+1` in the upper configuration. The difference is exactly 1 for every stirring strength. Differentiability of the semigroup on this bounded local observable forces the opposite inequality if the process were attractive. This proves failure of this coordinatewise order; it says nothing about other orders or couplings. Independent checks also evaluated rings of lengths 3, 4, 5, and 7.

On the 15-site ring, weights `1,2,3,2,1` divided by 9 give residue-class weight 1/3, so the initial period-three configuration has every triangular average `(1/3,0)`. The displayed finite adjacent-swap route preserves all species counts and produces five consecutive zero spins. At their center the same average is `(1,0)`, whose invariants `(1,-1)` differ from the initial `(1/sqrt(3),-1/sqrt(3))`.

The probabilistic assertion is justified analytically, not by merely finding a path: all 30 prescribed effective swaps have rate at least `sigma>0`; the total effective jump rate is at most `15(sigma+2)`. The probability of precisely those jumps in order before time t, and no others up to t, is at least

`exp(-15(sigma+2)t) * (sigma*t)^30 / 30! > 0`.

This finite-volume, fixed-scale event invalidates an exact pathwise empirical rectangle principle. It gives no lower bound uniform in hydrodynamic scale, and is not a counterexample to the macroscopic conjecture.

## 3. Affine entropies and the conditional rectangle

For every c, `S_c=rho+c*u-c^2` is affine and `F_c=f_1+c*f_2-c^3=(u+c)S_c`. Thus its conservation identity follows directly from the two weak equations. The pair `(|S_c|,(u+c)|S_c|)` is convex in the conserved variables and satisfies entropy compatibility on both affine branches; it is precisely the generalized family used in the inspected sources. The packet expressly assumes generalized interior inequalities, so it does not silently rely on an unjustified smooth convex approximation at this interface.

Adding or subtracting the affine equality and dividing by 2 gives the two positive-part inequalities with the correct sign. Their transport speed is bounded by 2 for the four thresholds. The factorization `S_c=(a-c)(c-b)` gives, respectively:

- upper a: `S_A1<=0`;
- lower a: `S_A0>=0`;
- lower b: `S_B0<=0`;
- upper b: `S_B1>=0`.

All factors divided by in these equivalences have a strict sign under the stated positive/negative thresholds. The trivial sides `a>=0` and `b<=0` need no entropy trace; this observation should not be read as automatically proving every other degenerate-side constraint.

The backward cone sign is correct. A decreasing spatial cutoff of `|x-x0|-R-2(t-s)` has `psi_s+2|psi_x|<=0`, hence `psi_s+(u+c)psi_x<=0`. The nonnegative continuity inequality, including its prescribed initial entropy term, then bounds the final interval mass by the initial expanded interval mass. Standard time cutoffs give this for almost every final time, sufficient for the asserted almost-everywhere rectangle statement. Nonnegativity and exhaustion force every violation to vanish.

This uses the initial terms in an essential way. Strong local L1 continuity is sufficient because these entropies are Lipschitz on the bounded state set. Weak initial convergence alone is not sufficient. The conclusion is a conditional invariant region, not positive-wave decay or unconditional uniqueness.

## 4. Smooth characteristic identity

Diagonalization and differentiation yield `D_+p=-2p^2-pq`, `D_-q=-2q^2-pq`. Since `D_+b=(a-b)q` and `D_-a=-(a-b)p`, the gap obeys `D_+d=-dq`, `D_-d=-dp`. The quotient rule then cancels exactly to give

`D_+(p/d)=-2d(p/d)^2`, `D_-(q/d)=-2d(q/d)^2`.

Along a classical characteristic extending back to time zero, reciprocation for a positive initial quotient gives the stated integral formula. For a nonpositive initial quotient, ODE uniqueness preserves the sign as long as the classical solution exists. A blow-up is not a permitted continuation through infinity. Bounds `0<delta<=d<=M` consequently imply the upper derivative bound `M/(2 delta t)`.

The regularity and characteristic-domain qualifications are essential. Products of weak derivatives and weighted values at `d=0` are not defined by this proof. No transmission law through shocks, uniform stochastic approximation estimate, or semigroup membership is obtained here.

## 5. Physical viscosity and the strict local maximum test

Independent symbolic reconstruction starts with the conserved-variable equation and multiplies by the inverse coordinate Jacobian. The mixed second derivative of `U=(-ab,a+b)` is `(-1,0)`, yielding the opposite corrections `-2 nu a_x b_x/d` and `+2 nu a_x b_x/d`. This is the physical isotropic viscosity, not a diagonal viscosity substituted in invariant coordinates.

Differentiating this reconstructed system independently recovers equation (6), including `-2 nu P Q_x`. At the report's jet, direct quotient differentiation gives `P=1`, `Q=0`, `P_x=0`, `P_xx=0`, and `Q_x=-M`. Crucially, the third derivative must be `a_xxx=M+1`; replacing it by M gives `P_xx=-1`, which the mutation control rejects. Production is `-2+2 nu M`.

A flat second derivative alone would not prove a local maximum. The report correctly offers a strict version: reduce `a_xxx` by a positive small e, retaining `P_x=0` and giving `P_xx=-e<0`; production becomes `-2+nu(2M-e)`, still positive for sufficiently large M. Smooth local polynomials realize the jets, and continuity keeps a and b in the strict physical interior on a small neighborhood. The strictly parabolic conserved-variable equation has local smooth solutions from smooth extensions of such data, so the jet is a legitimate differential comparison test. This invalidates the specified maximum-principle inequality, not all viscous estimates or the stochastic limit.

## 6. Exact scalar face theorem and entropy interface

Global face-valuedness and face-valued bounded initial data are explicit inputs. On F0, F+, and F-, the second conservation law has quadratic flux `u^2+beta*u+gamma` with `(beta,gamma)=(0,0),(1,1),(-1,1)`. The first law is redundant: on F+ its flux differs by a constant from the scalar one; on F- its equation is the negative scalar equation, up to a constant flux; on F0 it vanishes identically.

Every scalar absolute-value entropy is obtained from the full system family with a positive division factor:

- F0: c=k and division by `|k|` for k nonzero;
- F+: c=k+1 and division by `1+c`;
- F-: c=k-1 and division by `1-c`.

The resulting flux is exactly `(u+k+beta)|u-k|`, equal to the Kruzhkov flux difference. On the sloping faces the division factors are in `[1,2]`. For F0 at k=0, the entropy error is at most `|k|`, and the flux error at most `2|u||k|+k^2`; thus both converge uniformly on the bounded range. This validates passage to k=0 against compactly supported test functions. Outside the scalar range, the entropy is affine and its equality follows from the weak equation. Integral representation by absolute values plus an affine term supplies every C2 convex scalar entropy required by Chen–Rascle.

The saved Chen–Rascle author PDF, Definition 1.1(a)-(b), requires a bounded weak Cauchy solution with the initial linear term and convex entropy inequalities only for positive times. Condition (1.7) rules out nontrivial affine flux intervals. Its Section 4 Main Theorem then supplies the initial entropy inequality and unique Kruzhkov solution. The three quadratic fluxes are smooth, globally have second derivative 2, and satisfy this nondegeneracy condition. No L1 integrability on the entire line, BV hypothesis, positivity gap, or pre-existing nonlinear initial trace is imposed by this theorem. Its proof's normal-trace and entropy-production steps were inspected, in addition to the statement. We use the theorem in one space dimension for these scalar equations only.

The bounded initial state on each face supplies bounded scalar initial data. The weak Cauchy equation in Theorem 4 is therefore exactly the missing hypothesis needed to apply the scalar trace theorem. This validates uniqueness **inside the globally face-valued class**, not every two-component weak entropy solution with the same data.

## 7. Hopf–Lax, both invariants, and sharpness

The affine transformation `z=2u+beta` preserves the scalar entropy solution and converts its PDE to Burgers. A bounded z0 has a globally Lipschitz primitive H0. The quadratic term in Hopf–Lax is coercive against the primitive's at-most-linear growth, so minimizers exist. Differentiability in x identifies the solution by `(x-y_x)/t`. Comparing the two optimality inequalities at x<x' yields `(x'-x)(y_x'-y_x)>=0`, including when minimizers are not initially specified uniquely. At differentiability points this gives the upper slope `1/t` for z, hence `1/(2t)` for u. The standard Hopf–Lax/entropy-solution correspondence is a scalar PDE input; the finite algebra checker does not purport to prove it.

F+ has `a=u+1,b=-1`; F- has `a=1,b=u-1`; F0 has `a=max(u,0),b=min(u,0)`. Each truncation is increasing and 1-Lipschitz. Increasing u increments are contracted; negative increments remain nonpositive. Thus the one-sided upper bound passes to both truncations without differentiating at u=0. A full-measure pointwise representative gives the asserted distributional derivative inequality, including the degenerate point on F0.

The corrected report adds explicit rarefaction fans proving optimality of the common coefficient 1/2. On a sloping face the constant invariant separately admits coefficient zero. This distinction avoids overstating individual sharpness for a constant function. These fans are examples within Approach 5, not another route toward the coupled problem.

## 8. Normalization correction and limiting-face bridge

The inspected source smoother is `W_ell(theta)=(1/ell) sum_k K((theta-k)/ell)`, where K is nonnegative, compactly supported, normalized by its integral, and at least C1. Fritz–Toth v2 specifies C2; the OWR kernel is smooth. Discrete total mass need not equal one.

For a concrete admissible v2 kernel, let `K(s)=35(1-s^2)^3/32` on `[-1,1]` and zero elsewhere. The function and its first two derivatives vanish at the endpoints, and its integral is one. At integer sampling phase,

`W_ell(0)=1+7/(48 ell^4)-5/(96 ell^6)`.

In particular `W_2(0)=2065/2048`. The same nonunit-mass phenomenon is compatible with smooth compact kernels; the correction proof applies uniformly to both source regularity classes. The C2 example is enough to refute the original unconditional finite-scale sentence for the v2 source.

For the rigorous uniform estimate, partition the line into intervals of length h=1/ell centered at the sample nodes. For a node s_k and its interval I_k,

`|h K(s_k)-integral_{I_k} K(s) ds| <= h integral_{I_k}|K'(s)| ds`.

The fundamental theorem of calculus proves this bound; summation gives `sup_theta |W_ell(theta)-1| <= ||K'||_1/ell`. Compact support makes the sums finite. The bound does not depend on phase, hence is uniform in spatial position. Periodization on the torus gives the identical lifted sum, so it changes nothing. The actual block conditions imply ell tends to infinity.

The absent-species identities are exact even before normalization: no zero spins gives `rho_hat=0`; no negative spins gives `rho_hat=W_ell+u_hat`; no positive spins gives `rho_hat=W_ell-u_hat`. For small enough epsilon the mass W is positive. Dividing the two fields by W produces convex combinations of the two allowed spin-state vectors, hence an exactly face-valued profile. Each raw component has absolute value at most W, so raw-minus-normalized is bounded by `|W-1|` in each component. The estimate is uniform in configuration and time. Therefore raw and normalized profiles have the same strong local L1 limits, all in the corresponding closed face. This is a complete bridge to the conditional face theorem. It neither supplies the weak Cauchy equation nor changes the separate trace audit.

## 9. Source-v2 trace issue and version boundary

The saved arXiv v2 PDF's Section 3.2 topology integrates against dt dx. The initial-entropy term in Proposition 2, printed page 22 before equation (32), is not continuous in that topology. This was checked both in extracted text and in the page image. The packet's thin-time-layer example proves the topology claim directly; it is not represented as a PDE solution. Similarly, equal fine oscillations between `(0,1)` and `(0,-1)` have weak mean `(0,0)` but absolute-affine entropy averages 1/2 instead of 1/4 at c=1/2. The numbers and convexity direction are correct.

This establishes a limitation of the displayed inference, not falsity of the hydrodynamic conclusion or impossibility of a separate trace proof. The statement is restricted to the saved v2 bytes. No journal proof was independently inspected. Fritz–Nagy Section 2.3 explicitly distinguishes weak profile convergence from nonlinear initial entropy control; its Section 5.2 uses a scalar weak Cauchy identity and scalar uniqueness results. Chen–Rascle provides the needed scalar theorem, but no analogous two-component result is inferred here.

## 10. Deterministic uniqueness-source scope

The Bressan–Goatin author preprint was checked at the hypotheses, Theorems 1–2, inequality (2.5), and Section 6 proof interface. Its compact convex invariant-coordinate state domain lies in a smooth strictly hyperbolic region and satisfies cross-state (SH): speeds at different states remain ordered, and the corresponding eigenvectors remain independent. In the present coordinates the packet's sufficient conditions follow because

`sup_E lambda_-=A1+2B1`, `inf_E lambda_+=2A0+B0`,

and the determinant of the two cross-state coordinate eigenvectors is `b_2-a_1`, nonzero if `A0>B1`. The rectangle is convex in conserved coordinates by its affine entropy half-space representation. The theorem uses L1 perturbations of a reference state and strong L1 time continuity; its proof of characterization passes from positive-time BV control to time zero using this continuity. These assumptions cannot be deleted.

The full physical triangle includes the degenerate point and has overlapping cross-state speed ranges. Bressan–Marconi–Vaidya 2025 Section 4 Theorem 4.1 is a semigroup existence/stability theorem in the paper's strictly hyperbolic Temple setting. Its proof treats front-tracking trajectories, not arbitrary stochastic entropy limits. Neither source provides automatic invariant-rectangle confinement, repairs the full initial trace, or proves membership of every hydrodynamic limit in its semigroup. The packet's restrictions are correct.

## 11. Reproducibility, interpretation, and acceptance limits

`audit_checks.py` recomputes the microscopic current, global polynomial coordinate identities, both entropy branches and scalar restrictions, cone signs, physical viscosity and strict jet, ring generator witness, kernel counterexample, truncation property, minimizer-cost identity, and rarefaction slope. It uses exact rational/symbolic arithmetic and explicit exceptions. Polynomial identities and inequalities with analytic sign arguments provide the mathematical proof; rational grids are only additional controls.

`run_audit.py` executes the inherited and independent checkers under normal Python, -O, and -OO. It runs the three inherited mutations and five independent mutations in every mode. The independent mutants alter the scalar-face flux, reverse the cone direction, drop the physical mixed derivative, corrupt the third-order jet, and assume exact source-kernel normalization. Baseline success and mutation rejection are separate outcomes.

The replay takes place as a nonroot user in an actual mode-0555 directory with mode-0444 checker files. Before execution, attempts to create a file and to append to an existing checker must fail with a permission error. Full fixture and original-packet hashes are compared before and after. This tests real filesystem behavior, rather than merely describing a read-only intention. It does not prove absence of writes everywhere else on the machine, and is not claimed to do so.

The execution evidence contains no source bodies, datasets, private correspondence, or coordination material. Source metadata and inspection locators are separate from the public mathematical report. The final acceptance does not certify compactness, stochastic convergence, source theorem correctness from first principles, novelty, or a general three-state bound. The stopping status is the same unresolved bounded program with corrected conditional partial results.

## Source links

- [Fritz, OWR 43/2004, printed pp. 2260–2262](https://ems.press/content/serial-article-files/45959)
- [Fritz–Toth, arXiv:math/0304481v2](https://arxiv.org/abs/math/0304481v2)
- [Fritz, 2012 survey, Section 4](https://publikacio.uni-eszterhazy.hu/3223/1/AMI_39_from83to108.pdf)
- [Fritz–Nagy, ALEA 1 (2006), Sections 2.3 and 5.2](https://alea.impa.br/articles/v1/01-16.pdf)
- [Chen–Rascle author preprint, Definition 1.1 and Section 4](https://people.maths.ox.ac.uk/chengq/preprints/rascle99/rascle99.pdf)
- [Bressan–Goatin author preprint](https://www.math.ntnu.no/conservation/1998/039.html)
- [Bressan–Marconi–Vaidya, 2025, Section 4](https://arxiv.org/abs/2505.00420)
