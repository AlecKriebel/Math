# Turn 4: the exact physical two-obstacle return and its spectral obligations

**Substantive author turn 4 of 5; original unresolved.** This turn returns to the actual exterior Dirichlet equation. It proves an exact reduction of the two-obstacle density sequence to a compact return operator, including a nontrivial observation of its eigenmodes. It then states and proves precisely which uniform spectral data would close the illuminated-region quotient estimate. None of those uniform data is inferred merely from a resonance-location formula.

## 1. Physical operators at a fixed real frequency

Let K_1,K_2 be disjoint compact obstacles with smooth boundaries Gamma_1,Gamma_2 and connected exterior in dimension d≥2. Fix real k>0. For the present application they may be the strictly convex obstacles of the source. Let H_i f be the unique outgoing solution of

    (Delta+k²)H_i f=0 outside K_i,       H_i f|Gamma_i=f.

The usual outgoing exterior Dirichlet problem gives a continuous map from H^(1/2)(Gamma_i) to H^1 on each bounded part of the exterior (up to its own boundary). All constants in this section may depend on k. Set

    A_21=trace_(Gamma_2) H_1,    A_12=trace_(Gamma_1) H_2,
    M=A_12 A_21  on X=H^(1/2)(Gamma_1).

This is the physical quantum-billiard return used in the primary literature, with an outgoing sign convention selected consistently here. Compare A. Iantchenko, [arXiv:math/0702022](https://arxiv.org/abs/math/0702022), Section 1.2, equations (11)–(13). Those operator definitions and the established outgoing Dirichlet well-posedness are background, not new results.

Because the boundaries are separated by positive distance, interior elliptic regularity in a fixed neighborhood of the receiving boundary shows, for every finite s,

    A_ji : H^(1/2)(Gamma_i) -> H^s(Gamma_j)

is bounded. One first bounds H_i f in H^1 near the receiving boundary using the solution operator; the equation gives local H^q bounds by iteration, and the trace theorem gives the displayed bound. The constants depend on the fixed frequency and the chosen neighborhoods. Thus M maps X boundedly into every H^s(Gamma_1). Compact Sobolev inclusion for s>1/2 proves that M:X→X is compact. This argument does not claim smallness or uniformity as k tends to infinity.

Write D_1=partial_(n_1) H_1|Gamma_1 and N_12=partial_(n_1) H_2|Gamma_1, with the same chosen normal throughout. Define

    B=D_1 M−N_12 A_21.                                      (1)

The own-boundary Dirichlet-to-Neumann map sends H^s to H^(s−1), and the cross-boundary normal trace is smoothing by the preceding local argument. Consequently B:X→C^ell(Gamma_1) is bounded for each fixed nonnegative integer ell. Standard smooth-boundary elliptic regularity and Sobolev embedding justify these statements; no high-frequency symbol estimate is needed for them.

## 2. The exact current sequence

If an outgoing field from obstacle 1 has boundary value f_j on Gamma_1, its scattered successor from obstacle 2 has value −A_21 f_j there. The next scattered field from obstacle 1 therefore has value

    f_(j+1)=−A_12(−A_21 f_j)=M f_j.

Its total field on Gamma_1 is the sum of that outgoing field and the preceding field incident from obstacle 2. Its normal derivative is exactly

    eta_j=D_1 M f_j−N_12 A_21 f_j=B M^j f_0.                 (2)

This is the subsequence after full two-reflection returns; indexing the first current differently only shifts j. For a first plane-wave illumination of obstacle 1, f_0 is its negative boundary trace. Formula (2) includes the actual single-obstacle solve at every step. It is not an optical-current approximation, a finite stationary-phase truncation, or an analytic Gaussian replacement. Different cyclic starting obstacles have corresponding operators.

## 3. A physical eigenmode is observed on a dense open set

First, 1 is not an eigenvalue of M at real k>0. Indeed if Mv=v, the outgoing field

    w=H_1 v−H_2 A_21 v

has zero Dirichlet trace on both obstacles, so exterior uniqueness gives w=0 in their common exterior. The field H_1 v can then be extended through K_1 by H_2 A_21 v, since the latter is smooth near K_1 and the fields agree in an exterior neighborhood. This produces an entire outgoing Helmholtz solution; Rellich uniqueness and unique continuation make it zero. Therefore v=0. The same proof can be phrased weakly first and then regularized; for an eigenvector with nonzero eigenvalue the smoothing of M already gives v smooth.

Now let Mv=mu v with mu≠0 and v≠0. Then mu≠1. The total field

    w=mu H_1 v−H_2 A_21 v

has zero Dirichlet trace on all Gamma_1 and normal trace Bv there. If Bv vanished on a nonempty relatively open boundary patch, boundary Cauchy uniqueness would give w=0 in the connected common exterior. Here boundary Cauchy uniqueness follows by extending w by zero across the patch: its zero Dirichlet and Neumann traces eliminate the distributional boundary terms, and the resulting local Helmholtz solution vanishes on one side, so interior unique continuation applies.

Taking the trace on Gamma_2 would now give

    (mu−1) A_21 v=0.

Since mu≠1, this forces A_21 v=0, hence Mv=0, contradicting mu v≠0. Thus the zero set of Bv has empty relative interior. Since Bv is continuous, the set

    {x in Gamma_1 : (Bv)(x)≠0}

is nonempty, open and dense. Any compact subset E of that set has a strictly positive minimum of |Bv|. This does not say Bv is nowhere zero on the entire boundary, and does not give a lower bound uniform in k.

## 4. A fixed-frequency density quotient theorem

Assume M has a nonzero algebraically simple eigenvalue mu whose modulus strictly exceeds the moduli of all other spectral values. Compactness makes its Riesz projection P rank one; write Pf=v ell(f), with ell(v)=1. Set N=M(I−P). Then

    M^j=mu^j P+N^j(I−P).

Choose r with spectral_radius(N)<r<|mu|. The circle |z|=r avoids the spectrum of N. The resolvent integral for N^j gives a finite constant C_r such that

    ||N^j||≤C_r r^j,   j≥0,
    C_r=(r/(2pi)) integral_0^(2pi) ||(r exp(it)I−N)^(-1)|| dt.

Let E be a compact set where Bv never vanishes, and suppose ell(f_0)≠0. Put

    a=min_E |ell(f_0)Bv|>0,
    L=C_r ||B:X→C(E)|| ||I−P|| ||f_0||,
    rho=r/|mu|<1.

By (2), eta_j=mu^j ell(f_0)Bv+e_j with sup_E|e_j|≤L r^j. Whenever (L/a)rho^j≤1/2 the densities eta_j have no zeros on E and

    sup_E |eta_(j+1)/eta_j−mu|
             ≤2(L/a)(r+|mu|)rho^j.                          (3)

This follows by subtracting mu eta_j in the numerator and bounding the denominator below by a|mu|^j/2. If L=0 the sequence is already exactly geometric and (3) holds for every j. The conclusion applies to actual physical densities, but only under the stated spectral and excitation conditions, at the fixed frequency.

## 5. Exactly what would make the theorem uniform at high frequency

For a frequency-dependent compact E_k (or a fixed E), sufficient additional estimates would be, for all large real k,

    |mu(k)−R_(2,k)|≤C_mu/k,
    r(k)/|mu(k)|≤rho_0<1,
    L(k)/a(k)≤C_0 k^p,             p≥0,
    r(k)+|mu(k)|≤C_1.                                      (4)

For an integer

    j≥[(p+1)log k+log(max(1,2C_0))]/|log rho_0|,

the denominator condition follows for k≥1 and equations (3)–(4) give

    sup_(E_k) |eta_(j+1)/eta_j−R_(2,k)|≤(C_mu+C_1)/k.        (5)

The factor 2C_0 in this threshold yields C_0 k^p rho_0^j≤1/(2k), which proves the stated constant. This is a concrete physical sufficient criterion. Compactness by itself proves none of (4), simplicity, or ell(f_0)≠0. The finite-frequency observation theorem in Section 3 does not provide the frequency-uniform minimum in a(k). An exponential projector/observation loss would require a correspondingly longer return count than log k.

## 6. Poincare multiplier and the source's scalar prefactor

For a two-dimensional normal two-bounce orbit with gap d>0 and obstacle curvatures kappa_1,kappa_2>0, use unfolded paraxial coordinates (transverse displacement, transverse slope). Free flight and a convex reflection linearize to

    P_d=[[1,d],[0,1]],       K_i=[[1,0],[2kappa_i,1]].

The flight formula is displacement plus distance times slope. The reflection formula follows because displacement y rotates the surface normal to first order by kappa_i y, and reflection doubles this angular change, with the positive dispersing sign in the unfolded coordinates. Thus one full return has a matrix conjugate to

    C=K_1 P_d K_2 P_d,
    det C=1,
    trace C=2+4d(kappa_1+kappa_2)+4d² kappa_1 kappa_2.

With A=(1+d kappa_1)(1+d kappa_2)>1 its expanding eigenvalue is

    nu=2A−1+2sqrt(A(A−1)),
    nu^(−1/2)=sqrt(A)−sqrt(A−1).                             (6)

This independently matches Turn 1's continued-fraction product. It does not match the printed shortcut audited there. The physical linearized return, the optical transport product and the standard principal monodromy amplitude therefore select the same corrected magnitude. No density asymptotic is proved solely by this agreement.

The primary monodromy paper cited above uses the leading factors nu^(−alpha−1/2) in two dimensions; these are credited background. Its outgoing convention places resonances in the upper half-plane and uses exp(−2ikd). Our exp(+2ikd) convention reverses that sign. In particular the formal equation exp(+2ikd)nu^(−alpha−1/2)=1 has

    k=pi l/d−i(2alpha+1)log(nu)/(4d).

This sign check prevents translating a resonance formula into a real-frequency quotient without matching conventions.

## 7. Resonance locations alone cannot certify a dominant iteration mode

Here is a precise abstract obstruction to that inference, not a scattering counterexample. Fix 0<q<sigma<1 and d>0. The entire matrix families

    M_1(z)=[q exp(2idz)],
    M_2(z)=diag(q exp(2idz),sigma)

have exactly the same zeros, with the same multiplicities, of det(I−M_i(z)), because their determinants differ by the nonzero constant 1−sigma. Nevertheless at real z, the larger-modulus mode of M_2 is sigma. With input (1,1) and observation summing the coordinates, the iterate is

    u_j=(q exp(2idz))^j+sigma^j,

which is nonzero for all j≥1 and has u_(j+1)/u_j→sigma. No resonance is contributed by the extra constant branch. Hence even exact knowledge of this resonance set does not logically imply the desired dominant-mode claim. A theorem controlling the full operator or an auxiliary spectral parameter can rule out such branches; resonance locations alone cannot.

## 8. Status and final route

The exact physical identity (2), compactness, dense-open observation property and conditional quotient estimate (3) are established. Equations (4) identify the remaining uniform obligations. Known resonance/normal-form literature is relevant, but its hypotheses, weighted norms and projections cannot be silently replaced with the constants and physical data needed here. General smooth obstacles and global shadow-boundary quotients remain outside what has been proved.

**Original unresolved at 4/5.** The final author turn will test whether a more realistic vanishing-error regime can replace an all-return spectral theorem using only estimates genuinely supplied at finite iteration. It will not assert that an analytic model or a resonance location theorem has closed the source problem. Uncalibrated completion estimate: 30%.
