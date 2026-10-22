# Independent mathematical audit: spherical energy-momentum envelope

Date: 2026-10-10 UTC. Problem 30004486, alias OWR-1703869-006.

## Decision and limits

**ACCEPT the bounded partial theorem in the frozen proof.** No substantive mathematical correction is required for its compactness, rank, multiplier, semiconcavity, one-sided-envelope, or conditional non-staticity conclusions. This is an independent reading and reconstruction, not a conclusion inferred from the software tests.

**Do not accept a solution of the original non-staticity/quantitative-energy problem.** Nothing audited excludes a zero multiplier, determines the sign of a derivative, gives a positive frequency lower bound, or supplies an endpoint energy law. The original target remains unresolved. This audit makes no novelty or exhaustive literature-status claim.

The acceptance applies to fixed kappa > 0, degree zero, the unit round sphere with outward orientation, and only the interval

    I_kappa = (4*pi, 4*pi + epsilon_kappa)

credited to Melcher-Sakellaris. Compactness and uniform constants are asserted on compact subintervals of I_kappa. They are not uniform as j approaches 4*pi, as j approaches the other endpoint, or as kappa varies. The threshold is strictly below 8*pi. The statement about physical solutions is restricted to smooth minimizing profiles. No uniqueness or smoothness of every weak minimizer is needed or accepted as an extra conclusion.

## Accepted manuscript and verification limits

The distributed manuscript is [PROOF.md](PROOF.md), 19,584 bytes; SHA-256 `40d99707a3eb4151e98b82b77fe2f293880bd4b37858d4c8bcd32953706d3124`. Editorial status wording was updated; the mathematical text is unchanged. [ACCEPTANCE.json](ACCEPTANCE.json) binds the exact distributed proof and audit bytes. The independent audit read the complete manuscript and checked its complete frozen input inventory.

The historical author's verifier passed under ordinary Python, -O, and -OO. Its 32 adverse cases were independently rerun. Additional, separately written inventory, semantic-scope, exact-algebra, and logical-negative controls were recorded during the audit. These verify identities and limited algebra only; they cannot establish an infinite-dimensional variational theorem. Public historical counts and inspection coverage are preserved in [SOURCE_METADATA.json](SOURCE_METADATA.json). Programs, raw outputs, generated certificates, datasets and copied source documents/text/images are excluded from this proof-only edition.

## Primary dependencies actually inspected

1. Christof Melcher and Zisis N. Sakellaris, *Curvature stabilized skyrmions with angular momentum*, arXiv:1902.04881v2, 1 May 2019, Letters in Mathematical Physics 109 (2019), 2291-2304. [arXiv](https://arxiv.org/abs/1902.04881), [DOI](https://doi.org/10.1007/s11005-019-01188-6).
   - PDF: 196,034 bytes; SHA256 02b8f5bc70cc57fe3a585a111a42cb28dd60681b13c162eb93c4b88ecf6701cd.
   - Read the complete paper text and bibliography; visually inspected PDF pp.1-9. Pages 1 and 3 were independently rendered during this audit. Pages 2 and 9 confirm the exact credited existence statement and interval. Pages 4-6 fix the momentum and physical signs. Pages 7-9 contain the strict competitor and attainment arguments.
   - The audit imports the published existence theorem, including a smooth minimizer, and the strict trial-energy bound. It does not re-prove their moving-frame construction or the harmonic-map regularity machinery behind their theorem.
2. Haïm Brezis, Jean-Michel Coron, and Elliott H. Lieb, *Harmonic Maps with Defects*, Communications in Mathematical Physics 107 (1986), 649-705. [Author-hosted PDF](https://sites.math.rutgers.edu/~brezis/PUBlications/112-Journal.pdf), DOI 10.1007/BF01205490.
   - PDF: 5,308,470 bytes; SHA256 495fc13f3c13c95ff3463d150887642ad2a30c2af13d5f3b81142b29eb247858.
   - Read and visually inspected Appendix E, PDF pp.51-54, printed pp.699-702: Theorem E.1, Lemmas E.2-E.4, the proof, and Corollary E.5.
   - Crucially, the statement is for arbitrary bounded W1,N sequences converging almost everywhere. It imposes no harmonic-map, stationarity, minimization, or Palais-Smale hypothesis. Its sphere corollary applies at N=2. The separate Theorem E.5 printed below the corollary is a different result and is not used.
3. Christof Melcher, joint work with Zisis N. Sakellaris, *Emergent spin-orbit coupling in a spherical magnet*, Oberwolfach Report 22/2020, printed pp.1168-1171. [Original report](https://ems.press/content/serial-article-files/46860), DOI 10.4171/OWR/2020/22.
   - PDF: 795,156 bytes; SHA256 7b625ed2fd74f0d0dd3c5ad1c37090012ebdfd91ed9e5c86c06b87f7622fd5bc.
   - Read the full contribution and bibliography; independently rendered and inspected PDF pp.31-33, printed pp.1169-1171. These verify the exact spherical model, near-4*pi theorem, and the original energy/frequency/non-staticity question.

During the historical audit, the arXiv metadata and the author-hosted BCL PDF were additionally opened through the web tool. No fresh worldwide status search was made in that audit; the author's bounded search remains only a bounded search. Edition preparation rechecked frozen input bytes and publication integrity without new scholarly-source retrieval, source-text inspection, literature search or mathematical-computation reruns.

The following standard facts remain explicit mathematical background rather than concealed new results: Rellich compactness on the compact sphere; weak lower semicontinuity of the Dirichlet integral; integer degree and strong-H1 continuity for H1 sphere-valued maps; smooth approximation at this critical Sobolev exponent; the finite-dimensional inverse function theorem; basic measure weak-* compactness; and one-dimensional concave-function theory. BCL's proof itself invokes Sobolev degree/density and Morrey embedding. Its primary statement and relevant proof were checked; this is not a recursive re-proof of every reference in its bibliography.

## 1. Model and orientation

The proof's E, Q, S, L and J agree with the primary paper. Its factor one-half in the Dirichlet energy is essential: pointwise |rho_m| <= |grad m|^2/2 gives D >= 4*pi*|Q|, so one unit of concentrated degree costs at least 4*pi. Positive kappa ensures nonnegative anisotropy and makes E control D. The potential is continuous under strong L2 convergence on sphere-valued maps because its integrand is a bounded quadratic function of m.

Joint rotations preserve E and degree and rotate J as a vector. Consequently the infimum at J=j*a agrees with the infimum at |J|=j for fixed j>0. This does not impose a symmetry on individual minimizers.

The declared Landau-Lifshitz convention is the primary paper's equation (4). Its positive joint-rotation generator is

    K_a = a cross m - dm(a cross x).

The report uses a differently signed Poisson-bracket presentation; the proof consistently fixes its physical equation and positive rotation convention directly. No sign from one convention is silently combined with the other.

## 2. First variation at weak H1 fields

Let phi=v cross m for a smooth ambient field v. In an oriented coordinate patch, the variation of the pullback area form is d eta, where eta=m dot (phi cross dm)=v dot dm. Therefore, with f=b dot x,

    delta L_b = integral f d eta = -integral df wedge eta.

For b=e3, f=cos(theta); the last expression is integral v dot m_chi d sigma. Covariance gives the asserted formula for every b. Combining spin and orbital parts yields

    delta J_b[v cross m]
      = integral v dot (dm(X_b)-b cross m)
      = integral m dot (b cross v-dv(X_b)).

Both signs were independently reconstructed. The last equality uses the divergence-free rotation field X_b. In particular the derivative, for fixed smooth v, is continuous in strong L2, although J itself is not being asserted to be globally L2-continuous. This distinction matters for the inverse charts.

For weak maps the formula can be obtained by smooth H1 approximation or by the stated distributional product identity. The quadratic pullback terms converge in L1 under strong H1 approximation: the gradient products converge in L1, while the bounded zeroth-order factors converge in measure, with uniform integrability handling the remaining product. Thus no derivative beyond H1, and no pointwise continuity of m, is required.

## 3. Weak equivariance and the rank obstruction

If b annihilates every momentum derivative, the displayed identity against all smooth v gives dm(X_b)=b cross m as an L2 distributional equality. After normalizing b, define the L2-valued curve

    u(t,x)=R_b(-t)m(R_b(t)x).

The rotation group acts strongly continuously on L2 and has derivative dm(X_b) on H1 fields. Differentiating u in L2 gives zero. Thus u is constant and m is jointly equivariant as an H1 equivalence class. This justifies the passage from weak transport to a true rotation-group identity.

After rotation to e3, write m(theta,chi)=R_3(chi)h(theta) almost everywhere. Local H1 regularity of h follows from this representation on every annulus avoiding the poles. Put t=log(tan(theta/2)) and z=h dot e3. Direct conformal-coordinate calculation gives

    D=pi integral_R (|h_t|^2+1-z^2) dt.

Since h_t is tangent to the target sphere,

    |z_t| <= sqrt(1-z^2)|h_t|.

Cauchy-Schwarz proves z_t in L1. Hence z has limits at both ends of the cylinder. The nonnegative integrable function 1-z^2 and the existence of those limits force z_-, z_+ to belong to {-1,1}. This endpoint argument does not require choosing an azimuthal target phase, and remains valid when the target visits its poles.

The area calculation gives m dot (m_theta cross m_chi)=-z_theta. Therefore

    Q=(z_- - z_+)/2,
    S3=2*pi integral_0^pi sin(theta) z(theta) d theta,
    L3=2*pi(z_-+z_+) - S3,
    J3=2*pi(z_-+z_+).

The transverse components vanish by angular integration. Integration by parts is first performed away from the two poles; the established endpoint limits justify passing to the endpoints. If Q=0, the endpoints coincide, so |J|=4*pi. An annihilator at degree zero and |J|>4*pi is impossible. Since the target of the derivative is finite dimensional, absence of a nonzero annihilator proves surjectivity.

The result says rank deficiency can occur only at this level; it does not say every degree-zero field on the 4*pi level is rank deficient. The section title is correctly read in that necessary-condition sense. Constants provide actual rank-deficient fields there. The hedgehog checks Q=1 and J=0, confirming the degree restriction is indispensable.

## 4. Exact correction charts and uniformity

Choose three smooth fields v_i whose momentum derivative columns form an invertible B at a fixed m. The pointwise rotations T_t n are strong-H1 continuous in (n,t) and preserve the sphere constraint. Their path s -> T_(s*t)n is a strong-H1 continuous homotopy, so degree remains constant.

For precision, set H_n(t)=J(T_t n)-J(n). The first variation formula shows that every fixed finite t-derivative of H_n depends continuously on n in strong L2 and is uniformly bounded for t in a small ball. Indeed the instantaneous generators of T_t depend smoothly only on x and t; integration by parts removes derivatives of n from the momentum variations. Continuity of J itself in H1 then gives the stated parameter-dependent map.

Shrink the n-neighborhood and t-ball until

    sup ||D_t H_n(t)-B|| < 1/(2 ||B^-1||).

The contraction map t -> t+B^-1(y-H_n(t)) is then uniformly contractive. A small common y-ball maps the chosen t-ball into itself. This gives the asserted common inverse radius and derivative bound. Differentiating the inverse identity twice gives

    D^2 t[u,v] = -(D H_n)^-1 D^2 H_n[Dt u,Dt v],

which supplies the uniform second derivative bound without invoking any H1 manifold structure.

For the energy, the formula grad(T_t n)=(grad T_t)n+T_t grad n shows that its first two t-derivatives are continuous under strong H1 convergence and bounded on an H1-bounded n-neighborhood. The chain rule with the inverse chart therefore gives a uniformly bounded q-Hessian. No uniform bound on an entire noncompact H1 ball for inverses is being assumed: invertibility is local at each center and uniform on a suitably shrunken neighborhood.

## 5. Multiplier existence, continuity, and axial alignment

If a variation has zero first momentum derivative, its momentum error is O(s^2). The local correction chart changes it by O(s^2) in H1 and hence changes energy by O(s^2). Constrained minimality for both signs of s forces its first energy derivative to vanish. The resulting linear functional therefore factors uniquely through the onto map to R3. This proves the vector multiplier with smooth ambient rotation tests, even when m is merely H1.

The energy derivative is

    integral grad m : ((grad v) cross m)
      - kappa integral (m dot x)((v cross m) dot x).

The omitted-looking term grad m : (v cross grad m) vanishes componentwise. The displayed expression is strongly-H1 continuous. Together with continuity of the momentum derivative and the fixed invertible chart, the linear system B^T alpha=(delta E[v_i cross m]) proves multiplier continuity on the minimizing set.

Rotational invariance gives F(Rq)=F(q). Exact chart competitors give an upper quadratic support with linear part alpha dot (q'-q). Substituting q'=R_b(s)q and using positive and negative s forces alpha dot (b cross q)=0 for every b. Therefore alpha is parallel to q, hence alpha=omega*a. This is valid without twice differentiating an H1 map under domain rotation and without assuming differentiability of F.

## 6. Physical sign and smooth-profile qualification

For a smooth minimizer, every smooth tangent field phi can be written v cross m using v=m cross phi. Thus the weak multiplier identity gives

    g_E = omega G_a,
    G_a=P_m a - m cross dm(X_a).

Writing w=dm(X_a), with m dot w=0, the vector triple-product formula yields

    -m cross G_a = a cross m - w = K_a.

Since g_E=P_m[-Delta m-kappa(m dot x)x], multiplication by -m cross gives exactly the declared Landau-Lifshitz equation with omega K_a. Equivariance of that equation then verifies the entire rotating trajectory, not merely its initial velocity.

The weak rank result implies K_a is nonzero in L2 at degree zero and j>4*pi. For a smooth field this is also a nonzero smooth vector field somewhere. Consequently the constructed trajectory is static exactly when omega=0. This argument does not manufacture smoothness for a general weak minimizer. Existence of at least one smooth minimizing representative at each j is the explicit imported theorem.

## 7. BCL applicability and subthreshold compactness

Take a bounded H1 sequence with Q(m_n)=0 and limsup E(m_n)<8*pi. Weak H1 compactness and Rellich give a subsequence converging strongly in L2 and almost everywhere to a sphere-valued H1 map. The Jacobian measures have uniformly bounded total variation by the Dirichlet bound. Thus all hypotheses of BCL Theorem E.1 and Corollary E.5 are met.

Its conclusion can be written as rho_m d sigma plus finitely many nonzero integer-weighted point masses 4*pi*q_i at distinct points. Repeated points can be combined and zero coefficients discarded; the empty list is allowed. This is a signed-Jacobian assertion, not an assertion that the entire Dirichlet defect is atomic or quantized.

Here is an independent derivation of the precise energy statement needed. On a subsequence realizing the relevant energy liminf, let mu be the weak-* Dirichlet-energy measure limit and lambda the Jacobian measure limit. Local weak lower semicontinuity gives mu >= D_m d sigma. The pointwise Jacobian estimate implies |lambda| <= mu as measures. Since rho_m d sigma has no atoms, each point in BCL's list obeys

    mu({x_i}) >= 4*pi*|q_i|.

The diffuse lower bound and these finite atom bounds can be added because they are mutually singular. Strong-L2 continuity of the potential then yields

    E(m)+4*pi sum |q_i| <= liminf E(m_n).

Testing the signed limit with the constant function 1 gives Q(m)+sum q_i=0. Combining with E(m)>=D(m)>=4*pi|Q(m)| gives

    liminf E(m_n) >= 4*pi (|sum q_i|+sum |q_i|).

For every nonempty finite list of nonzero integers the parenthesis is at least 2. If the sum is nonzero its absolute value and sum of absolute values are each at least 1; if the sum is zero there is at least one positive and one negative integer. Hence any nontrivial Jacobian defect costs at least 8*pi. Strict subthreshold energy excludes it.

The consequence is Q(m)=0 and J(m_n)->J(m), because the constant test and the three smooth coordinate functions test degree and orbital momentum, while spin converges by L2. It is not yet strong H1 compactness. The proof explicitly observes this and does not falsely promote absence of signed Jacobian defects to absence of all energy defects.

To prove value continuity, exact correction of one minimizer at j0 gives upper semicontinuity e(j0)>=limsup e(j_n). In particular nearby minimizing energies satisfy one strict uniform subthreshold bound. Applying the preceding argument to arbitrary minimizers at those nearby levels gives an admissible weak limit at j0. Its energy is bounded below by e(j0), so the upper bound, weak lower bound, and minimality sandwich coincide. Strong-L2 potential convergence then forces convergence of Dirichlet norms. Weak H1 convergence plus norm convergence is strong H1 convergence.

For a compact K, continuity gives max_K e<8*pi. Every sequence in the union of all M(j), j in K, has a subsequence with j_n->j in K; the same argument makes its maps converge strongly to an element of M(j). In a metric space this is compactness. No representative selection, minimizer uniqueness, or smoothness of the whole minimizing family was used.

The proof's liminf notation is understood after choosing the relevant subsequence, as usual. Choosing an energy-liminf subsequence first makes the measure argument fully explicit; this is a harmless clarification, not a missing estimate.

## 8. Uniform upper supports and semiconcavity

On a slightly larger compact K', the all-minimizer family is strongly H1 compact. Finitely many of the exact correction charts cover it. The minimum inverse radius and maximum Hessian bound over this finite cover give common constants. Reducing the common radius also keeps j+h in the larger interval as needed. At the chart center, the energy derivative along q=(j+h)*a is alpha dot a=omega. Taylor's theorem yields the stated quadratic upper support uniformly over every active minimizer.

Adding the supports at h and -h based at the same minimizer gives the centered second-difference inequality. Subtracting C*j^2/2 produces midpoint concavity on sufficiently short intervals. Continuity upgrades midpoint concavity to concavity by dyadic approximation. Thus e is locally semiconcave. Standard one-dimensional concavity gives local Lipschitz continuity and finite one-sided derivatives at interior points. Its slope jumps are countable: on each concavity interval assign distinct rationals to the disjoint nonempty slope-gap intervals, then use a countable cover of I_kappa.

This does not yield global concavity of e itself. The quadratic subtraction and constants are local, and no sign of e's slope follows.

## 9. Exact envelope extrema, including corner orientation

At a fixed minimizer, division of the upper support by positive h gives e'_+(j)<=omega(m). Division by negative h reverses the inequality and gives e'_-(j)>=omega(m).

For reverse inequalities use an arbitrary minimizer m_h at level j+h, with support evaluated backwards at j:

    e(j) <= e(j+h)-omega(m_h)*h+(C/2)*h^2.

For h>0 this gives the lower bound on the difference quotient by omega(m_h)-C*h/2. All-minimizer compactness supplies a strongly convergent subsequence whose limit belongs to M(j); multiplier continuity passes omega to that limit. Since the right derivative already exists, it is at least min_M(j) omega. Together with the fixed-minimizer upper bound this proves equality.

For h<0 the same division reverses the last inequality, giving an upper bound omega(m_h)-C*h/2. The corresponding compactness argument proves the left derivative is at most max_M(j) omega, and hence equality. The minimum and maximum are attained by multiplier continuity on compact M(j).

Thus the assignments right/minimum and left/maximum are correct. At a differentiability point all minimizing multipliers coincide, even if minimizers are distinct and some are nonsmooth. Only the physical-solution assertion needs a smooth representative.

## 10. Lower bound and unresolved obstruction

The elementary chain |J|<=|S|+|L|<=4*pi+D<=4*pi+E is valid with these normalizations. If a minimizer at j>4*pi attained E=j-4*pi, every inequality in the chain would be equality, including |S|=4*pi. Equality in the sphere-valued averaging inequality forces m to be constant almost everywhere; then L=0 and |J|=4*pi, a contradiction. Therefore j-4*pi<e(j)<8*pi on the credited interval.

Neither this bound nor local semiconcavity excludes a constant interval or a zero derivative. A free symmetry action with regular momentum can have constant Hamiltonian and zero Hamiltonian flow. The symplectic-cylinder example in the proof correctly demonstrates that logical limitation without claiming a spherical counterexample.

At a corner, e'_+<=0<=e'_- merely places zero between the extreme active multipliers. It does not show that zero is attained by an active multiplier. The active slopes 2 and -1 of min(2*h+h^2,-h+2*h^2) provide the stated elementary control. Conversely differentiability with derivative zero does force every active multiplier to vanish; that is a conditional statement, not evidence that any such point exists in the model.

## Adverse mathematical controls

The independently written checks deliberately exercise the following wrong alternatives:

- Reversing the Hamiltonian-generator sign or the orbital-variation sign fails explicit rational vector fixtures.
- Reversing the orbital sign in the degree-zero polar excursion destroys J=4*pi, while constant and hedgehog checks fix orientation and normalization.
- Replacing integer defect weights by arbitrary real weights breaks the 8*pi barrier: q=(1/4,-1/4) has a much smaller formal cost. This is why BCL's exact integer conclusion matters.
- Replacing strict energy below 8*pi by an inclusive threshold does not contradict a unit lost charge and a residual map of opposite degree: their lower-bound costs can sum to exactly 8*pi.
- Discarding degree zero permits a single unit bubble with cost 4*pi. No subthreshold degree-preservation statement is accepted in that setting.
- Absence of Jacobian defects alone does not imply strong H1 convergence. On a coordinate patch, maps into a fixed great circle with angular amplitude c*sin(n*u)/n converge to a constant while retaining nonzero gradient energy; their Jacobians vanish identically. A compact cutoff makes the example global. With kappa=1 and c small, its energies are below 8*pi. This is a mathematical negative example, not a numerical approximation used in the proof.
- Swapping min and max in the one-sided formula fails the exact two-branch corner fixture. Inferring a zero multiplier from a zero-straddling corner also fails that fixture.
- Nonzero action generator plus regular momentum does not force nonzero frequency, as the constant-Hamiltonian cylinder shows.

These controls delimit the accepted result. They are not counterexamples to the original spherical target, and their software implementations supplement the mathematical reconstruction rather than replace it.

## Final audit conclusion

The pinned proof establishes the stated bounded partial theorem, conditional only on the clearly credited existence/regularity input and the correctly identified BCL compactness result, plus standard background facts listed above. The weak-rank proof, finite-dimensional corrections, all-minimizer compactness, multiplier alignment/continuity, uniform upper supports, and envelope extrema close without an unproved uniqueness or all-minimizer-smoothness assumption.

No substantive proof patch is requested. The optional liminf-subsequence clarification and the careful reading of the rank-deficient-level title do not change any conclusion. This AI-assisted manuscript and audit are unrefereed. Acceptance does not mean external human peer review, journal acceptance or formal proof-assistant certification. No substantive finding is omitted, and the mathematical verdict does not depend on omitted software or certificates.
