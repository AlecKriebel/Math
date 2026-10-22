# Exact result identity and independently checked alternative deductions

This is an identity/priority audit. It does not newly certify either full proof. Parent-provided analytic and numerical closures for the finite-polynomial theorem are separate evidence, not achievements claimed by this family.

## The exact common target

Let P consist of all monic real polynomials of finite degree n>=1 whose n roots, with multiplicity, lie in [-1,1]. Write E_f={x in R: |f(x)|<1}. The common infimum is the exact real number L, not a terminating displayed decimal. Wang's theorem additionally states |E_f|>L for every f and supplies a finite-polynomial recovery sequence. DPT Theorem1.1 states inf_f|E_f|=inf_mu|{U_mu>0}|=D for all Borel probabilities mu on [-1,1]; that statement alone does not supply finite nonattainment. The modern primary problem page has the same finite-polynomial question. Its original1958 reference permits general radii; only r=1 is compared here.

## The candidate measures and equations are identical

Use Q for Wang's q, s=(1-Q)/(1+Q), H=2Q/(1+Q)^2, and A=log(H)/log(Q). Use s for the DPT q; the overloaded letters in the manuscripts must not be equated literally. Define ell(y)=log((1+y)/(1-y)). Then

    H=(1-s^2)/2,
    log Q=-ell(s),
    A=log(2/(1-s^2))/ell(s)=p_DPT(s).

Consequently the two probability measures have exactly the same endpoint atom and density:

    A delta_{-1} + (t+1-2As)/(pi(t+1)sqrt((t-a)(1-t))) dt,
    a=2s^2-1, a<t<1.

For an exterior coordinate u_W>1, set y=(u_W-1)/(u_W+1), so u_W=(1+y)/(1-y). Direct rational calculation gives

    (u_W-Q)/(1-Q u_W)=(s+y)/(s-y),
    s^2-H(u_W+1/u_W)=(2s^2-1-y^2)/(1-y^2)=X_s(y).

Both logarithms are real after the displayed absolute value is applied. All quantities 1-y,1+y,1+s are positive for 0<y,s<1. The branch 1<u_W<Q^{-1} maps to 0<y<s, and u_W>Q^{-1} maps to s<y<1. Thus Wang's two exterior root equations become DPT's F_R=0 and F_L=0 with the correct physical sides. If their DPT roots are u_D and v_D,

    X_s(u_D)-X_s(v_D)
      = H[(u_W(v_D)+1/u_W(v_D))-(u_W(u_D)+1/u_W(u_D))].

The lengths agree exactly at every corresponding admissible candidate, not merely to displayed precision. DPT's third contact equation and Wang's unique global minimization use different closure mechanisms. Equality of their chosen exact optimal constants follows if their respective full lower/sharpness theorems hold; matching decimal strings alone does not prove that assertion. In the parent-verified finite theorem, the global infimum is fixed independently of this alternative proof. No second result-family row arises from a different proof or coordinates.

The authored standard-library check_identity.py expands rational identities into exact multivariate polynomials and rejects two deliberately false alternatives (a missing factor2 and a wrong branch sign). Nine identities pass in ordinary, -O and -OO modes with identical output. The logarithm equalities and physical ordering are justified above, rather than treated as polynomial identities. These checks do not certify DPT contact signs, forcing boxes or endpoint inequalities.

## Independent checks of DPT's measure-approximation deduction

DPT Lemma2.1 is sound by a direct kernel-truncation argument. For probabilities on [-1,1], truncate the logarithmic singularity in an L1 compactly supported kernel that agrees with -log|x| on [-3,3]. Weak convergence gives pointwise convergence of convolution with each bounded continuous truncated kernel; dominated convergence gives L1 convergence on [-2,2]. The untruncated/truncated L1 error is at most the kernel's L1 error, uniformly over all probabilities, by Tonelli. Taking the truncation parameter to infinity proves U_mu_j -> U_mu in L1([-2,2]).

For the sign-set approximation in Lemma2.2, a zero plateau is a genuine boundary issue: weak convergence or L1 potential convergence alone does not imply convergence of strict sign-set lengths. Orient mu by reflection so its mean m<=0. One can independently prove U_mu(x)>0 for -1<x<0: |x-t|<=1-xt for x,t in [-1,1], since the difference of the squares is (1-x^2)(1-t^2)>=0. Hence E log|x-t|<=E log(1-xt)<=log(1-xm)<=0. Strictness holds if there is interior support, or if the endpoint distribution is nondegenerate by strict concavity; the remaining endpoint point mass allowed by m<=0 is delta_{-1}, also strict. Exterior zeroes have measure zero by strict monotonicity of U outside [-1,1]. Therefore almost every zero-level point lies in (0,1].

Perturb by mu_e=(1-e)mu+e delta_{-1}. At such zero-level points the added potential -log(x+1) is strictly negative, so the strict positive set does not acquire a plateau. At points of nonzero finite potential its sign converges to the original sign. Infinite potentials occur only on a null set because the logarithmic potential is L1 on [-2,2]. All sign sets lie in (-2,2). Dominated convergence gives L(mu_e)->L(mu). For almost every e, the zero set of U_mu_e has measure zero by Fubini: at almost every x its defining affine equation in e has at most one zero; the simultaneous-zero exception x=-2 or0 is null. Choose such e decreasing to0.

For any probability with null zero set, choose weakly approximating equal-weight empirical measures. The inclusion

    E_n symmetric_difference E
      subset {|U|<=eta} union {|U_n-U|>eta}

and Markov's inequality prove convergence of lengths, first n->infinity then eta->0. A diagonal choice proves the DPT empirical approximation statement and equality of the finite-polynomial and all-probability infima. Equal empirical weights give actual finite monic polynomials. This deduction is independently checked here, conditional only on elementary measure facts; it does not validate DPT's distinct lower-bound construction. In particular, arbitrary minimizing-measure uniqueness and general-r classifications are not consequences asserted by this audit.

## Independently checked conditional skeleton of the other proof

The full29-page DPT text was read. Its mechanism is distinct from Wang's circle-block calibration: normalize a hypothetical finite-atomic counterexample, choose an exceptional interval set T with length h and window endpoint beta=1+h/2, form a positive dual measure with atoms z=r+h-D and r, and compress the exceptional intervals left/right to control its two possible potential minima at -1 and alpha.

The density/residue construction has mass one because its Cauchy transform has coefficient1/w at infinity; the possible atom at beta when T ends there is necessary and explicitly retained. The contour variation formula differentiates the moving interval factor into half the difference of two simple-pole kernels. Its derivative kernel has numerator xi-1-log|xi| and the stated denominators. The functions a(u)=u(u-1-log u)/(u-1)^2 and b(v)=v(1+v+log v)/(1+v)^2 yield the required opposing compression signs. The exact derivative and b-a algebra are among the authored polynomial checks. The endpoint-collision passage is justified by uniform convergence of the normalized square-root factors on fixed contours separated from the evaluation point. Taking x->alpha requires continuity; the text uses the vanishing square-root density there and absence of an atom.

Given literal endpoint-potential formulas B.6, the contact value/derivative identities B.1 and all the strict numerical inequalities6.4--6.7, the two-branch choice C=max(1,C0) is valid: if C0>1, strict convexity at h=0 and positive h derivative give L>=0, while R=0 and -z-C0>0. If C0<=1, move along (r+h-tau,tau), use L_h-L_r>0 and L_r<0 plus the final boundary value to obtain L(r,h,1)>0, and use R_C>0 to obtain R(r,h,1)>=0. The same C works in both compressed comparisons. On the resulting dual support U_mu<=0, with a strictly negative contribution at z<ell of positive mass, while U_lambda>=0 on root support. Tonelli applies after adding a compact-support lower bound to the kernel; no integrability cancellation of two infinities is required. This gives the stated contradiction.

DPT sharpness uses the same one-cut probability as above. Its Cauchy-transform residue and jump give the endpoint atom and density; normalization at infinity sets the constant plateau to zero. The two simple exterior zeroes yield exactly the interval (z*,r*) of lengthD; the plateau itself is excluded because the sign inequality is strict. The independently checked empirical approximation then supplies finite recovery. These implications are coherent conditional on the stated contact construction and imported normal form.

Limits: this family did not independently prove the imported Tao finite normal-form reduction as used by DPT Lemma3.1; did not reproduce the three Arb certificates (contact existence, global forcing, endpoint square/line); and did not independently reconstruct every literal branch/primitive reduction in B.4--B.6 and B.12--B.16. The five supplied proof scripts were captured; two numerical scripts and the README were read fully, while the endpoint script and symbolic scripts were statically inspected at their proof/branch/driver interfaces. No supplied script was run. Full29-page reading is not full-proof independent verification. The parent finite-polynomial closure does not depend on accepting these alternative computational gates.
