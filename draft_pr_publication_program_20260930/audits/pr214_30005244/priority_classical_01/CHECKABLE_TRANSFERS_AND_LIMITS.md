# Exact-model overlaps and checkable bridges

This is a priority comparison conditional on Root's correctness gate. It neither reopens correctness nor certifies historical novelty. PRIMARY_SOURCE_LEDGER.json pins every primary body and the precise pages read. No whole-paper absence inference is made from selected passages.

## 1. The zero-diagonal interaction and cubic shift are prior

Yurkin-Maltsev-Hoekstra2006, published pp2579-2580, Eqs2-18, explicitly includes the original Purcell-Pennypacker prescription: point-sample the off-diagonal Green tensor and neglect the dynamic self term M_i. The cube self term L_i=(4pi/3)I is explicit. Thus the target's basic finite interaction is not a new discretization.

Here is the normalization transfer. Let epsilon be constant relative permittivity and write the source susceptibility as chi=(epsilon-1)/(4pi). Its Green tensor is G_Y=(D²+kappa² I)e^{i kappa r}/r. Therefore the target kernel is K_kappa=-G_Y/(4pi). With M_i omitted, the source's field-system matrix is

    A_Y^h = [1+(epsilon-1)/3] I + (epsilon-1) T_kappa^h
          = -(epsilon-1)(z I-T_kappa^h),
    z = 1/(1-epsilon)-1/3.

This agrees with CDN2023v3 Eq1.8. Retaining M_i or integrating cell interactions gives another scheme; it must not silently replace the target. No material conversion is needed in the theorem itself.

The 2006 consistency argument then assumes inverse control in Eq65, with Eq66 as its consequence (printed2583-2584). Its regular-field, L1 error estimates do not establish uniform L2 resolvent bounds over off-interval contours, arbitrary masks satisfying(G), or norm Riesz convergence. The complete2015 erratum corrects weighted discretization and Eq6; it leaves Eq65 as an assumption. It supplies no missing inverse theorem.

The 2006 discussion already reports Rahola's sphere discretized-spectrum comparison. Thus sphere-spectrum numerical overlap is prior independently of the inaccessible thesis. It is not defensible to infer a rigorous general convergence theorem from that report: Rahola's full proof was unavailable here, and CDN2023v3 pp2-3 describes the corresponding figures as numerical experiments and identifies an overshoot.

## 2. The abstract spectral endgame is classical, with a precise transfer

Let B_h,B be uniformly bounded selfadjoint operators with spectra in a common real interval J, B_h -> B strongly, and C_h -> C in norm with C_h,C compact. Put S_h=B_h+C_h, S=B+C. Off J set

    R_h(z)=(z-B_h)^-1, F_h(z)=R_h(z) C_h.

The common bound is dist(z,J)^-1. Resolvent identities imply strong convergence of R_h and of their adjoints, uniformly on compact z-sets on each fixed vector. Compact multiplication gives F_h -> F in norm, locally uniformly. This is precisely the mechanism of Anselone-Palmer Proposition3.1 (applied also after taking adjoints), and regular/compact approximation as in Anselone-Treuden Sections8-9. Analytic Fredholm factorization

    z-S_h=(z-B_h)(I-F_h(z))

gives uniform inverse stability and no pollution on compact resolvent subsets off J. With G_h=(I-F_h)^-1 F_h, the Riesz integral has integrand R_h+G_h R_h. The first term integrates to zero on a disk avoiding J, and G_h R_h -> G R in norm by adjoint-strong compact multiplication. Hence the embedded Riesz projections converge in norm. Distance below one between projections gives equal finite ranks; their ranges have both gap directions bounded by that distance. This includes algebraic clusters, without preserving individual Jordan blocks.

This is a complete conditional classical implication. The note does not introduce a new general spectral approximation theorem.

Two literal citation shortcuts would be wrong:

1. AP's direct spectral-sequence theorem requires strong convergence and collective compactness of the differences. The full embedded S_h are finite rank. If {S_h-S} were collectively compact, AP Proposition2.1 would force S compact. Already on a ball the continuum S is noncompact. AP must therefore be used after compact factorization, not on the full DDA sequence as though its hypotheses were automatic.
2. DNR1978 assumes P1: sup over unit vectors in X_h of ||(A-A_h)x|| ->0, and P2: density of X_h. Strong convergence alone is not P1. For example, on l2, X_n=span(e1,...,en), A=0, and A_n the projection onto e_n give strong convergence and P2, but the restricted norm in P1 is always one. Changing occupied-cell spaces on the whole ambient H also do not automatically satisfy DNR's literal density hypothesis. Its general spectral conclusions are antecedents, not an unchecked direct theorem application.

The projection upgrade also cannot be inferred from strong convergence alone. Let X_n x=<x,e_n>e1 and K the projection onto e1 in l2. X_n ->0 strongly, but ||K X_n||=1. Strong adjoint convergence is the extra ingredient available here from the selfadjoint static resolvents.

## 3. What the sampled estimates add, and how much is routine

The nontrivial exact-model prerequisite is CDN's established bounded static lattice multiplier and exact real numerical-range interval, including its overshoot. Those results are expressly credited. The remaining limits can be verified by short classical estimates:

- On a smooth compactly supported test field, subtract its center value against a radial cutoff. Exact cubic reflections/permutations and trace zero cancel the static constant term, a cancellation already used in YMH2006 Eqs50-53. The discrete and continuous near terms are bounded by C delta using h³ sum_{0<|hj|<delta}|hj|^-2 <= C delta. Away from zero, ordinary Riemann sums converge. A |x|^-3 tail bound yields full-space L2 convergence. The prior uniform lattice bound then extends it by density. Condition(G) implies strong convergence of the mask multipliers, so their compressions converge strongly by bounded-product rules.
- The dynamic remainder is O(1/r) on bounded difference sets, an already established continuum static-plus-HS structure (Zhou Section2.1, with sign/conjugation convention checked). Its sampled-cell kernel has near-diagonal squared integral at most C(delta+h); the continuum bound is C delta. Away from the diagonal, uniform continuity plus the product-mask symmetric-difference bound gives L2 kernel convergence. Hence C_h -> C in HS norm. The omitted same-cell block leaves no nonzero self term.

These are useful verifications for the actual sample matrix and changing masks, not a new principle of quadrature or singular-integral cancellation. They make the classical transfer concrete. No read primary passage was verified to have already assembled all of them for this exact(G), fixed-complex-frequency, zero-diagonal model and projection topology. Conversely, their routine character means absence of an identical theorem sentence is not novelty evidence.

Budko-Samokhin's read continuum symbol/decomposition passages assume Holder continuity of contrast across the boundary; they do not themselves establish the(G) sampled-matrix claim. Zhou's principal polynomial theorem is formulated on the divergence-free physical subspace Phi; that smaller-space essential spectrum must not be substituted for the full L2 target. For real kappa his e^{-i kappa r} convention gives

    S_kappa = -conjugation G_Zhou conjugation - I/3,
    lambda_S = -conjugate(lambda_Zhou)-1/3.

## 4. Prior continuum poles give an especially direct bridge

ALZ's ETH2020-08 Eqs2.1-2.2 use the same outgoing fundamental solution and T_D^k=(k²+grad div)g_k*, so exactly

    S_kappa = -T_D^kappa-I/3.

For a bounded smooth domain and real kappa>0, Theorem3.2 proves Im lambda_T>0 for every eigenvalue other than -1; Theorem3.7 identifies these as finite-type poles. Hence each corresponding target eigenvalue has negative imaginary part. This is an actual theorem-to-target transfer, not merely related sphere physics.

On the unit ball, Root's accepted static gap 1/15, isolating radius1/30, and ||C_kappa||<=2kappa² imply a rank-three perturbed cluster at kappa=10^-4 by the ordinary resolvent/Riesz perturbation argument. Its mapped T eigenvalues are near -1/3, so exclude the exceptional -1. ALZ therefore proves all eigenvalues of this cluster nonreal. The independent trace certificate in the published note is checkable but is not a new existence mechanism; its nonreality conclusion can alternatively use this credited prior theorem.

Ammari-Millien2019 already uses static spectral decomposition and small-frequency volume-operator perturbation. Its displayed rank-one resolvent term in Lemma4.1 needs a one-dimensional eigenspace; the sphere dipole has dimension three. Substituting that lemma without replacing the pole term by the full rank-three projection would miss a hypothesis. This limits that particular shortcut, not the broad classical perturbation credit.

## 5. The rational-mask obstruction is an elementary combination

Yurkin-Mishchenko2018 SectionIX/footnote22 explicitly notes that point-tested cubic DDA depends only on center values, and smoothing between those centers leaves a fixed matrix unchanged. The countable-sampling failure is therefore familiar. Even more simply, the bounded measurable representative (B minus Q³) union{0} has exactly the ball's continuum operator and only one rational-grid sample. It is not compact, so it does not by itself cover the published compact-support refinement.

That refinement follows by a standard measure construction plus the same classical spectral-persistence argument. Enumerate Q³ intersect bar(B) as q_k and set

    U_j=union_k B(q_k,2^{-j-k-4}), F_j=bar(B) minus U_j.

The elementary volume bound is (4pi/3)2^{-3j-12}/7. Each F_j is compact, positive volume, empty interior, and avoids every rational sample; the masks tend strongly to the ball mask. Static compressions share [-1/3,2/3] and converge strongly. The dynamic kernels converge in HS norm by dominated convergence. The classical transfer in Section2 therefore retains a nonreal ball pole in an isolating nonreal disk for all sufficiently large finite j. Restoring the isolated point0 changes no L2 volume operator and makes every unshifted h=1/n matrix exactly3x3zero. Select one such j.

This is a checkable general removal-and-persistence construction. It is appropriately described as a compact-support scope obstruction combining classical ingredients, not a new sampling pathology or a new radiation pole. The exact retained-pole/one-anchor conjunction was not verified as a printed earlier result in the read corpus. No novelty conclusion follows from that limited negative finding.

The strong topology matters: when two indicator masks differ on positive volume, their multiplier distance in operator norm is one, however small that volume. Small removed volume alone does not supply norm-small static perturbations. The existential j and the restriction to the specified unshifted rational meshes must remain explicit.

## 6. Spectrum comparison alone does not certify inverses

For an elementary falsification of that inference, take A_n=I-N_n, where N_n is the n-dimensional one-step nilpotent shift. Then sigma(A_n)={1}, ||A_n||<=2, but A_n^-1 e_n=(1,...,1), so ||A_n^-1||>=sqrt(n). This is not a DDA counterexample; it explains why sphere spectrum plots or spectral-set convergence cannot silently discharge YMH's inverse assumption for these nonnormal matrices.
