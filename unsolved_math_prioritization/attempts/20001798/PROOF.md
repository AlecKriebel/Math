# An Airy worked example connecting wild harmonic bundles and recursion

Problem 20001798, AIM-GEOMETRY-0136. First substantive author turn, 2026-10-01. Candidate for independent source and mathematical review. This is a worked example assembled from classical inputs, with an explicit scaling deduction. No historical priority claim is made.

## 1. Exact target and precise result

Boalch's original Problem 1.28 asks to describe the relation between WKB, Eynard–Orantin (EO), Dumitrescu–Mulase (DM) topological recursion and the (wild) nonabelian Hodge correspondence, at least in one example. It does not prescribe Airy, an arbitrary wild type, or a theorem asserting convergence of Stokes coordinates. The archived primary statement and current-literature distinctions are pinned in SOURCE_GATE.md and SOURCES.md.

Here is one precise relationship for the Airy spectral curve. On the complex plane put

    E = O^2,   A(x) = [[0,1],[x,0]],   phi = A(x) dx.

For every R>0 there is a smooth determinant-one harmonic metric H_R for the Higgs field R phi. It has the prescribed decoupled wild growth at infinity. Its actual flat twistor connections

    nabla_(R,zeta) = D_(H_R) + zeta^(-1) R phi + zeta R phi^(dagger H_R)

satisfy, for each fixed nonzero complex hbar,

    nabla_(R,hbar R) --> nabla^Airy_hbar := d + hbar^(-1) phi

in C-infinity on every compact subset of C as R decreases to zero. In the displayed fixed holomorphic frame the error is O(R^(4/3)) in every fixed C^m seminorm, locally uniformly for hbar in C*. The scalar equation of the limiting connection is

    (hbar^2 d^2/dx^2 - x) psi = 0.

The all-order formal WKB solutions of this scalar equation are exactly the normalized principal specializations of EO recursion on x=t^2, y=t, with Bergman kernel dt_1 dt_2/(t_1-t_2)^2. They also agree with DM's PDE recursion for this genus-zero example. Thus a genuine wild harmonic bundle, its conformal connection limit, the corresponding scalar oper and both recursions are related in one explicit example.

There are two independent parameters and two different limiting operations: first R tends to zero with nonzero hbar fixed; then hbar is the formal WKB parameter of the limiting oper. No interchange of these limits is asserted. No convergence of Stokes coordinates at infinity, no general wild conformal-limit theorem and no new Borel-summability theorem is asserted. Whether the literal request is met by this worked-example relationship is an explicit part of the independent source review.

## 2. Classical radial input and frame convention

The required input is the fiducial solution described in Mazzeo–Swoboda–Weiss–Witt (MSWW), Section 3.2, equations (24)–(27), Lemma 3.3 and Corollary 3.4. There is a positive solution psi_0(rho) of

    (rho d/drho)^2 psi_0 = (rho^2/2) sinh(2 psi_0),

with the complete differentiated asymptotics

    exp(-psi_0(rho)) ~ rho^(1/3) sum_(j>=0) a_j rho^(4j/3),  a_0>0,
    psi_0(rho) = O(rho^(-1/2) exp(-rho)) at infinity.

The expansions at zero hold to every order, with corresponding derivative bounds. Define, for r=|x|>0,

    h_R(r) = psi_0((8/3) R r^(3/2)),
    H_R(x) = diag(r^(1/2) exp(h_R(r)), r^(-1/2) exp(-h_R(r))).       (2.1)

This is the metric in the fixed holomorphic frame of A(x), not the identity metric in MSWW's R-dependent unitary fiducial frame. Indeed, MSWW Proposition 3.5 uses

    g_R = diag(exp(u_R),exp(-u_R)),   u_R = -(1/4) log r - h_R/2,
    phi_fid = g_R^(-1) phi g_R.

Pulling the unit metric back to the original frame gives H_R=(g_R^(-1))^* g_R^(-1), exactly (2.1). This also explains why divergence of the unitary-frame Higgs entries as R tends to zero is not a contradiction to Section 4 below.

Set k(z)=|z|^(1/2) exp(h_1(|z|)) off zero. The differentiated expansion shows that k is a strictly positive smooth function on C, radial and smooth in |z|^2 near zero. In particular k(0)>0. Thus both entries of (2.1) extend smoothly and positively across x=0. The global radial solution is defined for every finite r, so this constructs a metric on all of C, not just a punctured local germ.

## 3. Hitchin equation and the wild end

Write v_R=log(H_R,11)=(1/2)log r+h_R. In the fixed holomorphic frame

    D_R = d + diag(partial v_R,-partial v_R),
    A^(dagger H_R) = [[0,bar(x) exp(-2v_R)],[exp(2v_R),0]].

The coefficient of dx wedge dbar(x) in the Chern curvature is diag(-v_(x barx),v_(x barx)); the coefficient of [phi,phi^(dagger H_R)] is

    diag(exp(2v_R)-|x|^2 exp(-2v_R), -exp(2v_R)+|x|^2 exp(-2v_R))
    = diag(2r sinh(2h_R),-2r sinh(2h_R)).

MSWW's radial equation is

    h_R'' + h_R'/r = 8 R^2 r sinh(2h_R).

Since partial_x partial_barx=(1/4) times the Euclidean Laplacian, it gives

    F_(D_R) + R^2 [phi,phi^(dagger H_R)] = 0.

The Higgs field is holomorphic. These facts prove flatness of nabla_(R,zeta) for every zeta!=0: the pure (2,0) and (0,2) terms vanish on a curve, the covariant cross derivatives vanish, and the remaining (1,1) terms are exactly Hitchin's equation. Smoothness extends this identity across zero.

This is genuinely an irregular or wild example. Near infinity pull back by x=t^2. The two eigenvectors e_+=(1,t)^T and e_-=(1,-t)^T have eigenforms +2R t^2 dt and -2R t^2 dt for R phi. Their irregular primitives are +/- (2/3)R t^3. In u=1/t these have poles of order three; the eigenforms have poles of order four. The pullback Gram matrix in these eigenvectors is exactly

    2|t| [[cosh(h_R(|t|^2)),sinh(h_R(|t|^2))],
           [sinh(h_R(|t|^2)),cosh(h_R(|t|^2))]].                  (3.1)

Consequently the two eigenlines have norm squared asymptotic to 2|t| and their normalized off-diagonal metric term decays exponentially as exp(-(8/3)R|t|^3), with the differentiated estimates inherited from the radial solution. The deck involution t -> -t exchanges the eigenlines; the original metric and Higgs field descend. Equivalently, in the original frame the norms of the basis vectors have growth |x|^(1/4) and |x|^(-1/4). These explicit growth rates specify the metric-compatible filtration; integer changes of a chosen meromorphic lattice must be accompanied by the corresponding filtration shifts.

This is the degree-one polynomial Hitchin example in the wild harmonic-bundle correspondence. Dumas–Neitzke, Section 2.4, describes the polynomial Hitchin section with precisely the self-duality equation and the compatible logarithmic growth condition, and cites the existence/uniqueness correspondence inputs. Here the radial formula supplies the solution directly. After swapping the basis, their polynomial is P_2=-x. Their convention of putting R^2 in the polynomial is related to R phi by a constant diagonal gauge; no equality of these different displayed frames is assumed. The end behavior (3.1), rather than a compact-surface theorem, is the reason this example is wild.

## 4. Exact small-R scaling and actual connection limit

The definition of h_R gives the exact identity

    h_R(r)=h_1(R^(2/3)r),
    H_R(x)=diag(R^(-1/3) k(R^(2/3)x), R^(1/3)/k(R^(2/3)x)).       (4.1)

Put epsilon=R^(2/3). Because k is smooth, positive and radial, near zero log k(z)=log k(0)+O(|z|^2), with its full smooth Taylor expansion. On each fixed compact K and for each m>=0 this implies

    ||partial log k(epsilon x)||_(C^m(K)) = O(epsilon^2)=O(R^(4/3)).

For m=0 the extra factor comes from the vanishing gradient at zero; for m>=1 the chain rule and the differentiated Taylor remainder give the same bound (higher powers of epsilon are harmless). The x-independent factors R^(+/-1/3) in (4.1) disappear on differentiating. Therefore

    D_R = d + O_(C^m(K))(R^(4/3)).                               (4.2)

Moreover the adjoint term is exactly

    R^2 A^(dagger H_R)
      = [[0,bar(x) R^(8/3) k(epsilon x)^(-2)],
         [R^(4/3) k(epsilon x)^2,0]].                            (4.3)

All its fixed compact C^m seminorms are O(R^(4/3)); positivity of k near zero bounds its reciprocal and all needed derivatives. Now set zeta=hbar R. The flat connection becomes

    nabla_(R,hbar R)=D_R+hbar^(-1) phi+hbar R^2 phi^(dagger H_R).

Equations (4.2)–(4.3) prove the claimed C-infinity compact limit and rate. The estimates are uniform when hbar ranges over a compact subset of C*. Notice that H_R itself generally diverges through the constant diagonal factors; metric convergence was never claimed.

For completeness, if normalized parallel transport is taken from a fixed base point along a fixed compact family of smooth paths, the usual integral equation for parallel transport and its differentiated equations show convergence to the Airy parallel transport. The limiting connection is holomorphic, although the positive-R connections in the original frame are not. This assertion is about finite compact paths. It gives no estimate uniform along paths escaping to infinity and hence no assertion about the Stokes filtrations.

## 5. The oper and WKB normalization

For a horizontal column Y=(psi,eta)^T of d+hbar^(-1)A dx,

    hbar psi'=-eta,   hbar eta'=-x psi.

Eliminating eta gives hbar^2 psi''=x psi. Conversely, every scalar solution gives the horizontal column (psi,-hbar psi')^T. Thus the scalar identification is exact for nonzero hbar. With the plus sign in our connection, the WKB branch with leading exponent +integral sqrt(x) dx corresponds to the negative Higgs eigenvalue in the horizontal system. This sheet-label reversal does not change the spectral curve or scalar operator.

Choose a simply connected domain avoiding x=0 and a branch t=sqrt(x). For a formal solution write

    psi_form=exp(sum_(m>=0) hbar^(m-1) S_m(x)),
    P=hbar partial_x log psi_form=sum_(n>=0) hbar^n p_n(x).

The Riccati equation is P^2+hbar P'=x. Choosing p_0=t fixes every later p_n uniquely:

    p_n=-(p_(n-1)' + sum_(i=1)^(n-1) p_i p_(n-i))/(2t), n>=1.

With p_n=c_n t^(1-3n), c_0=1, this reads

    c_n= -1/2 [((4-3n)/2)c_(n-1) + sum_(i=1)^(n-1)c_i c_(n-i)].  (5.1)

Fix the integration constants by

    S_0=2t^3/3,   S_1=-(1/2)log t,
    S_n=2c_n/[3(1-n)] t^(3-3n), n>=2.                          (5.2)

Thus p_1=-1/(4t^2), p_2=-5/(32t^5),

    S_2=5/(48t^3),  S_3=5/(64t^6).

An x-independent formal scalar factor is a normalization freedom. Our choices set the stable primitives to vanish at t=infinity and choose the indicated unstable logarithm. Replacing t by -t gives the opposite WKB sheet. On the negative sheet over positive x it is the standard decaying Airy expansion, up to its x-independent normalization. Actual Airy contour-integral solutions and their sectorial asymptotic expansions are classical; DM Section 7.1, equations (7.11)–(7.17), makes this connection explicit. Their existence does not identify limits of normalized positive-R Stokes solutions.

## 6. EO and DM recursion give this same WKB series to every order

Use the normalization sphere with x=t^2, y=t, omega_(0,1)=2t^2 dt and omega_(0,2)=B=dt_1 dt_2/(t_1-t_2)^2. The local involution at the simple ramification point is t -> -t. With the convention

    K(t_0,t)=(integral_(-t)^t B(t_0,s)) / [2(y(t)-y(-t))dx(t)],

the kernel is

    K(t_0,t)=dt_0/[4t(t_0^2-t^2)dt].

Use this kernel in the usual EO residue recursion at t=0, including the pullback sign d(-t)=-dt. Stable free energies are obtained by integrating each variable from infinity. Define their principal-specialized combination by

    S_m^TR(t)=sum_(2g-2+n=m-1) (1/n!) F_(g,n)(t,...,t), m>=2.    (6.1)

The unstable S_0,S_1 are those in (5.2). This is a formal local definition; no divergent infinite integral of omega_(0,1) is being taken.

Dumitrescu–Mulase prove the all-order identification in their Section 7 Airy example, using Theorem 6.1 and the specific residue/PDE agreement established in Section 7.2. Their normalization coordinate s has x=4/s^2, y=-2/s. Under t=-2/s it becomes ours, B is unchanged as a bidifferential, and their base point s=0 becomes our infinity. The constants of integration therefore coincide. Their genus-zero argument explicitly checks that the extra apparent residue contributes zero and hence that EO residue recursion and their PDE recursion agree. This is essential: their Remark 5.7 warns that this agreement is not a blanket higher-genus theorem.

More explicitly, the credited Airy intersection-number formula in these conventions is

    F_(g,n)(t_1,...,t_n)
      = 2^(-(2g-2+n)) sum_(d_1+...+d_n=3g-3+n)
          <tau_(d_1)...tau_(d_n)>_(g,n)
          product_i [(2d_i-1)!! t_i^(-(2d_i+1))],              (6.2)

where (-1)!!=1. Its mixed derivative gives the EO differentials with the factor (-1)^n and (2d_i+1)!! instead. Formula (6.2) is the pullback of DM's formula (7.18), not a newly asserted intersection theorem. The principal specialization (6.1), with the two unstable terms fixed, satisfies hbar^2 psi''=x psi to all formal orders by the cited Airy theorem. Riccati uniqueness (5.1) then identifies every derivative of S_m^TR with p_m; both stable primitives vanish at infinity, so their constants agree as well.

As direct normalization checks, the first EO residues are

    omega_(0,3)=-dt_0 dt_1 dt_2/(2t_0^2 t_1^2 t_2^2),
    omega_(1,1)=-dt/(16t^4).

Their integrated principal terms are 1/(12t^3) and 1/(48t^3), respectively, totaling 5/(48t^3). At the next order, <tau_1 tau_0^3>_(0,4)=1 and <tau_2 tau_0>_(1,2)=<tau_1 tau_1>_(1,2)=1/24 give 1/(24t^6)+7/(192t^6)=5/(64t^6). These checks fix the factors of two, sheet convention and primitive base point; finite checks are not used to prove the all-order theorem.

## 7. Category, scope and conclusion

The original plane bundle extends meromorphically across infinity. A chosen holomorphic lattice there need not be DM's O(-1) direct-sum O(1) compactification. Our identification is of the meromorphic spectral curve, the displayed scalar Airy operator, and their restrictions to C; it does not claim equality of different holomorphic extensions or filtered lattices without the necessary lattice shifts. The harmonic metric and its compatible growth are specified directly in Sections 2–3, so the nonabelian-Hodge object is not being imported from a compact theorem with missing hypotheses.

The example supplies the following rigorous chain: the classical radial wild harmonic metric produces actual flat connections; their explicit scaling yields the Airy oper on compact sets; its formal WKB coefficients coincide to all orders with both EO and DM recursion in a common normalization. Classical Airy analytic solutions realize these formal asymptotics on sectors. This describes a relation among all four objects named in the original question in one nontrivial wild example.

Compact connection convergence does not prove convergence in a topology controlling the irregular end. Dumas–Neitzke Section 2.9 discusses the stronger polynomial conformal-limit expectation and its Stokes consequences; neither that expectation in general nor those consequences for this family are deduced here. The optional stronger global-Stokes route was not used in the proof. This is a source-scoped worked example with classical credits, not a solution of an unstated general wild-Hodge conjecture.
