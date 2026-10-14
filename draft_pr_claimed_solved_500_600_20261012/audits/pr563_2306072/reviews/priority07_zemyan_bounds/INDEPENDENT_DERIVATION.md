# Independent source derivation

Recorded before reading any old family report or the candidate proof/publication.

## Definitions and exact source assertions

Both papers define S as normalized univalent analytic maps on the unit disk, sigma as actual global support points of a nonconstant continuous complex-linear functional L. Their arcs are C minus f(D), not arbitrarily drawn quadratic-differential trajectories. With an outward orientation, write theta = arg w, phi = arg w_prime, beta = phi - theta. The papers call sign changes of theta_prime wiggles (G) and sign changes of phi_prime wavers (V). Their radial angle is the unsigned angle between tangent and radial lines, alpha = |beta| on the branch |beta| < pi/4. Neither G nor V is defined by beta_prime.

2005: Proposition 2.1 defines f_sharp = |f_prime|/(1+|f|^2), Z=1/(r f_sharp), and gives kappa^2=1+r^2 Z_r^2/4, tau=r Z Z_rtheta/(4 kappa^2), and r Z_rtheta = Z Im(z^2 Sf). Here Sf=(f_doubleprime/f_prime)_prime-(f_doubleprime/f_prime)^2/2 is the usual Schwarzian. Proposition 2.2 says #lambda_r intersect C_rho >= 2 for support points and rho close to 1. Proposition 2.3 identifies curvature critical points with lambda_r union Lambda_0. Theorem 3.1 gives 2+2#G <= #lambda_r intersect C_rho <= #Lambda_0 intersect C_rho for rho sufficiently near 1 (the middle inequality holds for every S and every rho). These are upper bounds for G, not sufficient conditions for a wiggle. All rho-near-1 claims may depend on f.

2005 Remark 3.1 states G and V disjoint, alternating types, an intervening waver between two wiggles, a waver after the last wiggle, and #G<=#V. Theorem 4.1, using Lemma 4.1 |Sf(0)|=6|a3-a2^2|>6(3-2sqrt(2)), gives four Schwarzian-zero arcs emanating from 0 at right angles. The proof and Remark 4.1 do NOT continue this four-intersection statement globally; if four intersections persisted to the boundary, the bound would still allow one wiggle.

2007: Theorem 2.1 says G and V finite. It argues eventual sign stability at infinity and the finite tip, then real-analytic uniqueness on a compact subarc. Theorem 3.1 states G intersect V empty, alternating wiggle/waver types, and an intervening waver, giving #G<=#V+1. It does not restate/prove the stronger 2005 last-wiggle assertion. These are necessary geometric restrictions conditional on actual support membership, not an existence proof.

## Positive examples and existence implications (complete inventory)

2005 Example 1: Koebe k=z/(1-z)^2, omitted radial half-line (-infinity,-1/4], G=V=empty. Exact z^2 Sk=-6z^2/(1-z^2)^2; Lambda_0 consists of four radial segments.

2005 Example 2: Pearce p_xy=[z-(x+y)z^2/2]/(1-yz)^2, |x|=|y|=1, x != y, support status whenever 0<|arg(-x/y)|<=pi/4. The omitted arc is a nonradial half-line, G=V=empty. Exact Sp=-3(x-y)^2/[2(1-xz)^2(1-yz)^2]. The conjugate specialization y=conjugate(x) gives four Lambda_0 arcs; its two nonlinear arcs satisfy cos(theta)=2r cos(arg x)/(1+r^2). These arcs live in the parameter disk; they are not wiggles of the omitted arc.

2005 Remark 3.2 discusses slight variations of a Pearce function and says that if two simple Z_r zeros persist for every rho sufficiently close to 1, Theorem 3.1 excludes wiggles. This is a no-wiggle condition; compact-open proximity alone is not a demonstrated uniform-in-rho persistence theorem or a construction of a support point. The stated heuristic supplies no new maximizing functional, perturbed map, verified zero count or boundary-uniform estimate.

Both introductions cite Zemyan 2003 for the actual existence of a support point with an interior waver; the conjecture for N wavers is a conjecture. They assert no actual support with a polar wiggle. 2007 p.176 also asserts full-class-S analytic slit maps with infinitely many wiggles/wavers, but explicitly separates them from sigma; there is no support certificate or explicit formula here. Those are not target counterexamples. References are leads, not contents of the cited works.

## Independent angle identities and half-line exclusion

For an outward modulus parametrization r=|w|, w=r exp(i theta), dw/dr=exp(i theta)(1+i r theta_r). Thus beta=arctan(r theta_r), theta_r=tan(beta)/r, and phi=theta+beta. Wiggles are sign changes of beta; wavers concern phi_r=theta_r+beta_r. Nonmonotonic phi alone says nothing sufficient about theta or alpha.

For a half-line w=u+s v, s>=0 with Re(v conjugate(w))>0, theta_s=Im(v conjugate(u))/|w|^2 has constant sign, phi_s=0, beta_s=-theta_s. Since tan(beta)=Im(v conjugate(u))/Re(v conjugate(w)), and the denominator grows at rate |v|^2>0, beta has constant sign and |beta| decreases to zero (or is identically zero). Koebe/Pearce therefore cannot be earlier negative examples for polar argument or unsigned radial angle.

## Proof caveats to verify algebraically

2007 p.178-179 uses g=τ w and g_doubleprime/g_prime to describe d arg(w_prime(τ))/dτ. In general w_prime=(τg_prime-g)/τ^2 and w_doubleprime/w_prime=τg_doubleprime/(τg_prime-g)-2/τ. The imaginary part of g_doubleprime/g_prime is different. For w=1/τ+i+τ, w_prime is real but g_doubleprime/g_prime=2/(i+2τ) has nonzero imaginary part. This is a formula flaw, not an adverse support example. The corrected formula nevertheless is analytic in imaginary part near τ=0 because d_-1 != 0, so it repairs eventual sign stability without yielding any wiggle.

2007 p.177 assumes a regular analytic tip parametrization and also the normalized trajectory equation Q(w) w_prime^2=1. At a simple zero of Q the natural parameter cannot have a finite nonzero tip derivative: w-w0 is proportional to t^(2/3). A regular geometric parameter can still exist. Treat the two parameters separately, and never infer support membership from this equation alone. Lemma 2.1 also requires infinitely many DISTINCT zeros (not merely an infinite repeated sequence) and a conjugation-symmetric neighborhood or its restriction, as required by analytic uniqueness.

