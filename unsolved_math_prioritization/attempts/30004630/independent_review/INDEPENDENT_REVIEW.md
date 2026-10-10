# Independent full audit: quadratic growth without beta_2

**Verdict: PASS_COMPLETE_COUNTEREXAMPLE_TO_UNMODIFIED_IMPLICATION. No mandatory correction.**

The frozen first-turn construction disproves the source implication obtained by deleting beta_2>0 while retaining strict positivity on the ordinary critical cone and the same L2-squared growth conclusion. The cone is exactly {0}; that vacuity is explicit and is permitted by the source. This verdict does not assert that every beta_2=0 problem fails, that all possible strengthened sufficient conditions are false, or that every weaker stability estimate fails.

The review binds COUNTEREXAMPLE.md SHA-256 `a4ffb1e682a235e0221a83edf4b2db2c7fc7b17a02f778884489a1c3dd321cc3` and FROZEN_MANIFEST.json SHA-256 `f67277a60698b0c0abd00a62572bdf95b7ffa79ace62422b1040869425ff5d8a`. All nine author files and three primary PDFs match. The reviewer did not contribute to the author route before freeze, and the frozen files were not edited. This is independent adversarial assistant review, not human peer review or a novelty certification.

## 1. Exact original hypotheses and target

I read the full OWR contribution and visually checked printed pages439–440, then checked the complete critical-cone definition and Theorem4.17 in the referenced analysis. The source really uses the defocusing quintic wave equation on a smooth bounded three-dimensional domain, homogeneous Dirichlet boundary conditions, energy initial data, and pointwise-in-time spatial L2-ball constraints. The example's unit ball, zero initial data, positive constant radius, gamma=beta_1=1 and beta_2=0 satisfy the model's requirements.

The OWR objective has an additional nonnegative terminal velocity term, while the inspected full preprint does not. The proof covers every fixed nonnegative coefficient of that term. OWR states an L2 neighborhood; the full theorem uses an L-infinity-in-time/spatial-L2 neighborhood with L2-squared growth. The countersequence tends to zero in the latter stronger topology. Neither version escapes the example.

The source defines the critical cone by zero first directional derivative within its tangent cone, and expressly defines the substitute second derivative of the sparse norm to be zero at the zero control. There is no assumption that the critical cone contains a nonzero vector. Thus it would change the question to insert nonvacuity or an approximate-critical-cone condition during this audit.

The theorem's proof itself uses beta_2>0 to rule out a normalized weakly null sequence after its weak limit has been shown critical and hence zero. The candidate reproduces exactly the loss of that mechanism, rather than refuting a different finite-dimensional assertion.

## 2. Uniform small-input PDE estimate

The analytic remainder is justified, not merely formal. On the fixed time interval, the source linear energy/Strichartz estimate gives a bounded map L from L1_t L2_x to Y, where Y contains continuous energy states and L4_t L12_x position. Sobolev and mixed-norm interpolation give

    ||y||_(L5_t L10_x)^5
       <= C ||y||_(L4_t L12_x)^4 ||y||_(L-infinity_t H1_0).

Consequently ||y^5||_(L1_t L2_x)<=C||y||_Y^5, and the factorization of y^5-z^5 gives the corresponding fourth-power local Lipschitz estimate. For sufficiently small A=||u||_L1, the map y->L(u-y^5) preserves a ball of radius 2||L||A and is a contraction there. Its constants can be fixed independently of u before choosing rho. The unique fixed point satisfies ||y||_Y=O(A), and y-z=-L(y^5) gives ||y-z||_Y=O(A^5).

The source's uniqueness in this solution class identifies that fixed point with its mild solution. Since every admissible control has A<=rho, choosing rho below the fixed small-input threshold makes the estimate uniform on the entire admissible set. The argument does not assume a numerical value for a PDE constant or obtain it from finite diagnostics.

The normalized radial eigenfunction is correct: multiplying it by r gives a sine eigenmode, its spherical L2 integral is1, and its value at the origin extends smoothly. The linear endpoint kernel is sin(pi(1-t))/pi, giving the stated adjoint pairing.

## 3. Genuine global optimizer

Expanding the terminal tracking square leaves the exact linear pairing, the sparse cost, nonnegative squared-state/velocity/quartic terms, and a nonlinear endpoint error bounded by C0 A^5. Cauchy–Schwarz in space therefore gives the stated lower bound with weight 1-sin(pi t).

On the centered interval, the elementary sine-chord estimate implies 1-cos(pi s)>=2s^2. The bathtub argument has the correct sign on both sides of the central saturated interval. Equal mass cancels the r^2 term, yielding integral s^2 f>=A^3/(12rho^2). Hence the objective gap is at least A^3/(6rho^2)-C0 A^5.

The small-radius choice is sufficient: writing x=A/rho<=1 and k=C0 rho^4<=1/12, this lower bound is (A^3/rho^2)(1/6-kx^2), at least A^3/(12rho^2). It is positive for every nonzero admissible control. Thus zero is the unique global optimizer over all admissible controls, not only stationary, locally optimal, or optimal within the chosen eigenmode. The estimate holds uniformly for all spatial control directions.

## 4. Critical cone and its explicit vacuity

At zero, the smooth derivative is p(t)=-sin(pi t)e. The function lambda(t)=sin(pi t)e is a valid L1-norm subgradient, its norm is at most1, and p+lambda=0. The state regularization and terminal velocity cost have zero first derivative. The constraint multiplier is zero because the radius is strictly positive and the zero control is pointwise inactive.

The tangent cone is the full Lr space in the source definition; equivalently, bounded truncations establish this fact even though the pointwise-ball set has no L1-norm interior. For every nonzero L1 direction v, the first derivative is bounded below by the integral of (1-sin(pi t))||v(t)||. The weight is strictly positive except at one null time. That integral is strictly positive for every nonzero equivalence class v. The same holds for L2 directions. Thus C(0)={0} exactly.

The formal j'' convention at zero agrees with the source, and strict positivity over C(0) minus zero is genuinely vacuous. No uniform positivity on near-critical unit directions is present. For example the normalized pulses are weakly null in L2 and have first-order gaps tending to zero; no fixed nonzero critical vector records them. This is the essential infinite-dimensional feature, not a missing hypothesis in the written theorem.

## 5. Failure of growth in the stronger neighborhood

For u_h=h e on the centered time interval of width2h, the norms are A_h=2h^2, ||u_h||_L2^2=2h^3 and ||u_h||_L-infinity=h. The exact linear endpoint is 2h sin(pi h)/pi^2 times e, and the linear terminal velocity vanishes by symmetry.

I independently computed the leading linear objective gap:

    J(u_h)-J(0)
       = (pi^2/3+2/pi^2) h^4 + o(h^4).

The candidate only needs the weaker O(h^4) bound. The nonlinear endpoint error is O(h^10), the quartic state term O(h^8), and the velocity term O(h^20) for any fixed nu. Cross terms in the terminal square are also higher order. These estimates justify the displayed leading coefficient and, in particular, the ratio to 2h^3 tends to zero. All pulses are feasible for small h and converge in L-infinity. The conclusion therefore defeats both stated neighborhood versions without relying on unbounded-amplitude perturbations.

## 6. Perturbed optimizer existence and the specific stability failure

The direct-method extension for the optional velocity term is sound. U_ad is a bounded closed convex subset of L2 and hence weakly compact. The uniform energy bound and compact H1_0->L2 embedding, together with y_t bounded in L-infinity L2, give a strongly convergent subsequence in C(L2). Likewise y_t is bounded in L-infinity L2, compactly embedded spatially into H^-1, while

    y_tt=Delta y-y^5+u

is uniformly bounded in L-infinity H^-1: y^5 is bounded in L-infinity L^(6/5) by the energy bound and u is bounded in L-infinity L2. Arzela–Ascoli therefore gives strong C(H^-1) convergence of velocities, including the terminal trace.

Almost-everywhere state convergence identifies the weak L^(6/5) limit of the quintic. The retained L4 L12 and energy bounds imply the limiting quintic is in L1 L2, so the weak solution is the unique mild one by the linear Duhamel characterization and source uniqueness. Terminal costs are continuous under the strong convergences. The state norm and L1 control norm are weakly lower semicontinuous. This proves global minimizer existence also with nu>=0.

For the fixed-amplitude comparison pulse, h_epsilon=pi epsilon/(2a) gives mass pi epsilon, terminal displacement epsilon e+O(epsilon^3), and zero linear velocity. Its perturbed gap is -epsilon^2/2+O(epsilon^3); I independently checked the cubic linear coefficient pi^5/(24a^2). Thus the asserted negative comparison is valid for small epsilon with a fixed positive a.

The lower bound for any control uses g_epsilon correctly. Its enclosing parabolic cap has squared L2 norm (8sqrt(2)/15)(epsilon/pi)^(5/2), which is smaller than the simpler constant used by the author. Hence ||g_epsilon||_L2=O(epsilon^(5/4)). If an optimizer had L2 norm at most K epsilon along a sequence, its objective gap would be bounded below by -O_K(epsilon^(9/4))-O_K(epsilon^5), contradicting the comparison -epsilon^2/4. This works for every fixed K and every selection of global optimizers.

The claim is specifically failure of a Lipschitz L2-control bound under this terminal-target perturbation, not failure of all stability. Its local meaning is also consistent: optimality and the base gap give A^3/(12rho^2)<=C epsilon A, hence A=O(sqrt(epsilon)); since ||u||_L2^2<=rho A, all these minimizers do converge to zero in L2. No L-infinity convergence of the perturbed minimizers is asserted or required for this separate stability statement. The growth countersequence itself does converge in L-infinity.

## 7. Exact controls, source credit and disposition

All nine author-file and three source-PDF hashes match. The author's 3,937 exact controls replay byte-for-byte in a separate copy. My checker imports no author code and passes 1,385 exact controls, starting from the general-center wave kernel, computing leading coefficients independently, checking the sharper positive-part norm, and exhaustively testing small rational bathtub densities. These calculations are not a PDE simulation, do not calibrate unknown PDE constants and do not replace the analytic estimates above.

The available full-text sources are the official OWR report and the two identified preprints. The final publisher typesetting was not silently substituted for those inspected versions. The source wave estimates, well-posedness and optimization framework are credited classical inputs.

The packet is a complete counterexample to the literal unmodified sufficient-condition extension after one substantive author turn. A precise campaign promotion may be **claimed_solved,1/5**, explicitly as a negative answer to that implication. It should not be described as disproving all beta_2=0 theory or as a historically certified new discovery. No mandatory correction or additional author search turn is needed for the accepted mathematical scope. Parent retains publication approval.
