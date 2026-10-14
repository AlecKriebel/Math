# Independent mathematical and historical bridge ledger

## Checkable local counterexample using the old C2 input

Set H=L2(B), B the unit ball in R3, T=1, zero initial state, target d=pi*e with ||e||H=1 and -Delta e=pi2*e. Let A=||u||L1(H), r=||u||L2(H). The feasible cap is ||u(t)||H<=rho, rho>0. Fix any finite nu>=0. The smooth part consists of terminal position tracking, optional H^-1 terminal velocity tracking and the quartic state cost; the nonsmooth part is A.

The local state differentiability assertion stated in the prior theorem gives y=z+R, ||R||Y=o(A2), uniformly as A tends to zero, because S(0)=0, S'(0)=L and S''(0)=0. A compatible-state proof independent of the printed codomain issue is given below. Projection of the linear wave gives

    <e,z(1)>=(1/pi) integral sin(pi*t)<e,u(t)>dt <= A/pi.

Write x=<e,y(1)> and x<=b=A/pi+eta(A)*A2, eta>=0, eta(A)->0. The terminal tracking square and nonnegative remaining costs imply

    J(u)-J(0) >= q_A(x)=A-pi*x+x2/2.

For A sufficiently small, b<pi, and q_A decreases on (-infinity,b]. Therefore q_A(x)>=q_A(b), and

    q_A(b)=A2/(2*pi2)-pi*eta*A2+eta*A3/pi+eta2*A4/2
          >= A2/(4*pi2)>0

once eta<=1/(4*pi3). Hence zero is a strict local optimizer, uniformly over all sufficiently small L1 controls, and consequently in either source localization (L2 or L-infinity). No global-optimum claim is needed.

The first directional derivative is integral(||v||-sin(pi*t)<e,v>), positive for every nonzero equivalence class because 1-sin(pi*t)>0 off the single null time 1/2. Bounded truncations verify the full L1/L2 tangent at zero. The ordinary source critical cone is {0}, so its strict positivity premise is vacuous with its explicit substitute j''(0;v2)=0. This is not positivity on an enlarged cone.

For u_h=h*e*indicator(|t-1/2|<h), h<min(rho,1/2),

    A_h=2*h2, r_h2=2*h3, ||u_h||infinity=h,
    z_h(1)=2*h*sin(pi*h)/pi2*e, (z_h)_t(1)=0.

The first-order residual is (pi2/3)*h4+O(h6), the position square is (2/pi2)*h4+O(h6), the nonlinear tracking-linear remainder is o(A_h2)=o(h4), the quartic state term is O(h8), and the velocity cost is o(h8) for fixed nu. The ratio [J(u_h)-J(0)]/r_h2 tends to zero. This is already a complete local-optimizer counterexample to the core implication.

Normalized v_h=u_h/r_h is weakly null in L2: its pairing with any L2 test is bounded by that test's L2 norm on the shrinking time interval. The BW NDC expression is exactly

    1/h - sin(pi*h)/(pi*h2) + sin2(pi*h)/(pi4*h)
      = (pi2/6+1/pi2)*h + O(h3) -> 0.

BW's necessary theorem consequently agrees with the direct growth calculation. It is mathematically applicable; it supplies no extra existential construction.

## Printed differentiability-proof limitation and direct local repair

The source defines its residual e from the compatible state space Y+ to all of C([0,T];E), then asserts e_y is onto that entire pair space. At zero initial data/control, e_y(0,0)z=-xi_z. If F(t)=(0,w) with a fixed nonzero w in H, its first component would force z(t)=0 and hence z_t(t)=0, while its second component would require z_t(t)=-w. Thus surjectivity onto the printed codomain is false. This is a concrete counterexample to that proof step, not a counterexample to its local C2 conclusion.

For the needed local conclusion, use the Banach space of compatible zero-initial-data states with energy-plus-Strichartz norm Y and the bounded zero-data forcing map L:L1(H)->Y. Define

    Gamma(y,u)=y-L(u-y5),           Gamma:Y x L1(H)->Y.

The interpolation Y embeds into L5(L10), and Holder shows that the product of any five Y fields belongs continuously to L1(H). Hence the quintic map is a continuous homogeneous polynomial of degree five and Gamma is C-infinity. At (0,0), Gamma=0 and D_y Gamma=Id_Y. The Banach implicit-function theorem therefore supplies the local solution map, D_u S(0)=L and D_u^2 S(0)=0. Source uniqueness identifies this solution with the actual mild state. Its uniform Frechet Taylor remainder gives the o(A2) used above. The nonlinear state is not assumed to remain in span(e).

This direct local proof uses established linear forcing and interpolation estimates. It does not require the stronger submitted global assertions, and it does not change the historical fact that the specific counterexample is constructed here rather than asserted by an earlier conditional NDC theorem.

## A contrasting instance within the same model

Keep all model choices except take terminal target d=0. Zero is a global optimizer and

    J(u)>=A,             r2=integral||u(t)||H2 dt <= rho*A,
    J(u)-J(0)>=r2/rho.

Every nonzero direction has first derivative ||v||L1>0, so the exact critical cone is again {0}. NDC has lower bound A_h/r_h2>=1/rho on every feasible normalized increment. Thus the same general old results and the same cone size permit positive growth. The threshold-tuned choice of d and its optimizer validation are necessary to settle the constructed failure, rather than follow from mere membership in the abstract framework.

## Historical provenance ledger

| Item | What is verified | Historical role | Missing coverage step |
| --- | --- | --- | --- |
| KM2019 Theorem 4.3 | Statement of state C2 in L1(H), explicit S''; local compatible-state proof above | Prior differentiability assertion; printed codomain proof qualified | No threshold-tuned negative example/local optimizer |
| KM2019 Theorem 4.17 introduction | beta2>0 used for coercivity; beta2=0 left open | Source scope | No beta2=0 negative theorem |
| BW2024 Assumption 2.1, NDC, Theorem 2.18 | Conditional necessary criterion and full proof | Prior abstract framework; applies correctly | No wave-data existence, no local optimizer, no demonstrated wave NDC failure |
| BW2024 section 4 closure | Parabolic/scalar-box unregularized discussion | Strong antecedent for familiar mechanism | Not an asserted theorem covering this nonlinear-wave realization |
| CHW2017 section 5 | Exact-cone insufficiency warning; different PDE/bounds | Required credit | No verified negative Hilbert-ball wave construction |
| CT2015 Example 4.16 | Complete survey reproduction of Dunn integral example | Verified generic counterexample; original attribution indirect | Different objective/constraints and no wave optimizer bridge |
| BRIDGES B1–B8, written 2026-10-14 | Complete mathematical specialization using submitted data | Current audit derivation | Its present proof date cannot establish prior historical resolution |

No absent optional global or perturbation assertion is counted as a coverage gap. The only substantive historical gap in the proposed covering witness is the source-specific existential construction satisfying the actual local premise and vacuous-cone/growth-failure conclusions.
