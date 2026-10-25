# Independent adversarial review — Zenodo 22729355

**Disposition: PASS at the exact published hypotheses.** No substantive mathematical defect or unresolved central proof gap was identified. This is an AI mathematical review of the pinned v1.0.11 paper and support, not human peer review, a novelty certificate, or a claim that all related questions have been settled.

The review was completed independently of the current analytic/scope conclusions and historical reviewer judgments. The main manuscript has 19 pages and the supplement 19 pages. Both full source documents, their bibliography, and the included exact coefficient/sign tables were read. Load-bearing support programs were inspected and selected ones rerun in a private working copy. The public PDFs and all six other published files were checked against the fresh acquisition receipt. `verdict.json` binds these exact bytes, the receipt, and the review evidence.

## Exact claims checked

For the displayed indexed network with m ≥ 3 and n=m+1 species, all reaction complexes have size at most two, an inflow is allowed, and rates and equilibrium coordinates are strictly positive. Every positive-equilibrium Jacobian is A_m(a,b)H with a,b>0 and H positive diagonal. Every principal block of order strictly below m is Hurwitz, whereas the core omitting Z has a positive real eigenvalue. This is a statement about this synthetic topology throughout its realization family, not every binary-complex network.

For a realization that is additionally Hurwitz on the stoichiometric tangent c-perp, a positive diagonal diffusion ray has a stationary crossing exactly when

`d_Z > 8 h_Z sum_{j=2}^{m-1}(d_j/h_j)`.

The crossing parameter also depends on a,b; the inequality alone does not give its numerical value. The positive-real-eigenvalue band is exact. The law does not classify all nonreal unstable eigenvalues. The fixed-equilibrium contrast infimum is nonattained; the unit-equilibrium value is 8(m−2). The product inequality `chi_D chi_H > 8(m−2)` and its minimax square-root consequence are topology-specific stationary bounds.

The stable-pattern results are stronger but narrower construction results: the rational unit profile and the stated equilibrium-scaled interval have a simple primary stationary bifurcation on the one-dimensional Neumann interval (0,pi), two reflection-related positive branches for sufficiently small positive mu, and local exponential H1 stability within the fixed integrated-mass class. Their neighborhoods and constants may depend on m and on the chosen family parameter. The scaled family is exponent-optimal against the stationary lower bound; its constants and the global stable frontier remain open.

## Proof audit and adversarial attacks

### Realization quantifiers, conservation, and localization

Main Propositions 2.1–2.2 (pp.3–4), Lemma 3.1 and Theorem 3.2 (pp.4–6), supplement S1–S2:

* Differentiating the mass-action reactions gives the claimed A_m(a,b)H, not an arbitrary kinetically unconstrained matrix. The two positive flux coordinates are independent; conversely the rates `k_r=v_r/(x*)^{y_r}` realize every a,b,H in the stated positive domain.
* `c=(0,4,...,4,2,1)` is semipositive, `c^T Gamma=0`, and rank Gamma=m. The zero coefficient of X1 is acknowledged and does not supply arbitrary-data boundedness. The proof needs only local dynamics near a strictly positive equilibrium.
* The interaction-graph classification is exhaustive: an interior chain vertex can belong to a nontrivial strongly connected block only by completing one of the two long cycles, unless the block is inside the boundary triad. With fewer than m vertices, combinations demanding a larger cycle are excluded. At b=2a one edge disappears; this splits possible components rather than adding new ones.
* The cycle product inequalities remain strict for all positive a,b,H. The boundary triad has positive cubic coefficients and the printed 14-term positive Routh gap. Its two-vertex principal blocks also have negative trace and positive determinant. Thus this is an all-spectrum Hurwitz argument, not merely a determinant sign argument.
* Eliminating the core chain leaves the displayed three-by-three Schur matrix with determinant 2a²b. The signed core minor is `-2 a^(m-1) b product(h_1,...,h_m)`. A negative constant term of its monic characteristic polynomial forces a positive real root. This establishes the maximal proper unstable order even when the complete realization is not homogeneously stable.

Fresh controls constructed the polynomial field directly from reactions, differentiated it, and checked exact Routh determinants for every principal subset below m for m=3,...,7, at three distinct positive rational parameter choices, including b=2a. All omission minors, rank, and polynomial conservation identities agreed. These finite controls support the general graph and Schur proof; they are not substituted for it.

### Principal-minor theorem, stationary threshold, and sharpness

Main Theorem 4.1 (pp.6–7), Proposition 5.1 and Theorems 5.2–5.3 (pp.7–9), supplement S3–S4:

The multilinear principal-minor expansion gives `det(sD-J)=s q(s)`. All coefficients of q beyond its constant term are strictly positive, so q is strictly increasing for s≥0. The additional sum of order-(n−1) signed minors is what makes the characteristic polynomial strictly increasing in a nonnegative real eigenvalue variable. Neither step uses the invalid inference that determinant positivity proves full Hurwitz stability. The n=2 endpoint of the general theorem is legitimate: q has a positive linear coefficient.

For this network, the omission minors are zero when X1 or Xm is omitted, positive with coefficient 16 when an interior Xj is omitted, and negative with coefficient −2 when Z is omitted. Factoring their weighted sum gives the factor eight in the criterion. Homogeneous stability on c-perp implies a simple conservation zero and a positive total order-(n−1) signed-minor sum. It also gives `T(H)=8h_Z sum(1/h_j)>1`; this implication is not asserted in reverse.

The homogeneous right null vector is `H^-1(2,-2,...,-2,0,1)`. Its c-pairing is nonzero on the homogeneously stable set. Differentiating that simple eigenvalue supplies the same threshold and the direction of the crossing. At equality the diffusion polynomial has no positive crossing; one cannot replace the strict inequality by a weak one.

Contrast sharpness is an infimum statement: take all X diffusivities at their common minimum and let d_Z decrease toward T(H) from above. The product bound uses `h_Z/h_j >= h_min/h_max`. The unit profile proves the required stable realization exists, so the topology-wide infimum is approachable. No nonlinear stable-infimum equality is inferred.

Fresh exact Sturm counts checked the positive-crossing count on both sides of and exactly at the threshold for m=3,...,6. Equal diffusion never crossed. The deliberately excluded m=3 scaling H=diag(1,8,1,1), for which T(H)=1, has a double homogeneous zero. This is a useful boundary control: homogeneous stability cannot be silently dropped.

### All-mode exclusion and algebraic simplicity

Main Theorem 6.1 (pp.9–11), Theorem 7.1 (pp.12–14), supplement S5–S8:

The sparse characteristic determinants reduce to `Q F-G`; the factor bounds for Q are valid on the entire closed right half-plane. They do not merely sample Fourier modes. In the unit case, retaining a chain factor gives `|Q|² >= (91/90)²+y²`. In the scaled case, `g_i=(K_(i-1)/K_i)(1+L lambda)+(t−1)/K_i` yields the product estimate used in the 84-term certificate. The homogeneous scaled estimate uses nu L²≥5/4 for nu≥2. The exceptional nu=1 case is separately covered by the displayed cubic Routh inequality; the weaker exceptional endpoint must not be generalized to all m.

I independently regenerated the four modulus polynomials from F,G,P,R, parsed the actual printed TeX tables, and compared every exact coefficient. The term counts 35,77,22,84 all matched. Positive pure-axis terms establish strict positivity away from the origin; the absence of a constant term alone would not have sufficed. The 22-term certificate remains strict away from zero even at its coefficient-parameter endpoint U=0.

The explicit left and right eigenvectors and their nonzero pairing prove algebraic simplicity at the selected zero. The determinant derivative formula gives the same conclusion. The homogeneous conservation zero is removed only from the k=0 block. All nonzero spatial modes retain all species coordinates. Fresh finite eigenvalue stress tests at both certified L endpoints and t=0,1,1.0001,4,9,100 agree; these floating-point tests are supplementary only.

### Cubic sign, harmonics, and the rescaled mass gauge

The quadratic Hessian was obtained by differentiating the reaction field. Since cos²(xi)=(1+cos(2xi))/2 and the Taylor field is `Au+B(u,u)/2`, the forcing in both harmonic equations is `-B(r,r)/4`. The cubic projection is

`ell^T [ B(r,w0) + B(r,w2)/2 ] / (ell^T r)`.

The factors one-quarter and one-half, the second-harmonic operator A−4D, and the mass constraint on w0 are all load-bearing. Direct constrained rational solves at m=3,4,5,7,11 agreed with the negative cubic and positive crossing signs. Replacing the second-harmonic multiplier by one makes the operator singular. Using the old mass gauge for a genuinely nonidentity equilibrium scaling fails the new constraint.

The central universal sign is not justified here by those finite contractions. `generic_cubic_division.py` provides an independent symbolic route: it solves the four-by-four second-harmonic boundary system over Q(m), verifies the interior recurrence, divides the chain-index contraction into a polynomial in i and a single reciprocal term, sums the polynomial exactly, and leaves the reciprocal sum as a formal h. This derives the full identity `N_m=R_m+C_m h` and the gauge scalar S_m. The shift-positive polynomials then give `C_m<0`, `N_m>1/100`, and the stated critical denominator signs for all m≥3. All 26 checks in this separate route passed.

For the scaled dynamics, the mode operator is H(A−t Delta), its left vector is H^-1 ell, and its mass covector is H^-1 c. The stationary second harmonic is unchanged; the zero harmonic is shifted by tau times the homogeneous null vector. The independent index-division calculation also derives tau from this weighted mass constraint and verifies its two derivative formulas. The printed all-nu endpoint comparison proves tau<1/20. With −1/10<S_m<0, the bound N_m(L)>1/200 follows; when tau<0 its contribution is positive, so no unproved lower bound on tau is needed. The scaled left-right pairing is strictly negative. Thus the negative cubic survives the equilibrium rescaling.

The near-threshold example in supplement S9 is a boundary control, not an optimum theorem. Its exact rational cubic is positive on 0<epsilon≤10^-3, while its higher-mode quartic Routh certificates and transversality are valid. The published interval certificate reproduced; independent rational controls at epsilon=10^-3 and 10^-4 also gave the opposite, subcritical sign. This correctly prevents identifying every stationary crossing with a stable supercritical pattern.

### Infinite-dimensional bifurcation and stability interfaces

The source spells out the appropriate spaces: `X_c={u in H_N² : integral c^T u=0}` and the analogous closed L² space Y_c. The k=0 restriction is invertible, k=1 has one-dimensional kernel/cokernel, and the k≥2 blocks are invertible. The Neumann-series bound O(k^-2) gives an H² preimage for compatible L² data, hence closed range and Fredholm index zero. The parameter derivative pairs as `(pi/2) ell^T D r`, which is nonzero.

The original [Crandall–Rabinowitz 1971 paper](https://jxshix.people.wm.edu/2013-taiwan/crandall-rabinowitz-1971-JFA.pdf), Theorem 1.7 on printed pp.325–326, and the graph-domain application Theorem 2.4 on p.330 were checked. The theorem requires the smooth trivial branch, one-dimensional kernel and quotient range, and the nonzero mixed-derivative pairing established above. The stationary nonlinearity is polynomial from H² to L². Its higher smoothness supports the expansion; reflection exchanges the branch halves. The embedding H² into C0 makes sufficiently small branches strictly positive.

The Neumann diffusion generator on the real fixed-integrated-mass L² space is sectorial with compact resolvent; its shifted half-power space is H1. The reaction derivative along a small H² branch is bounded multiplication. The high-frequency numerical-range bound tends to minus infinity, so spectral stability cannot be inferred from or lost through an unexamined infinite tail. A resolvent Neumann series for the bounded reaction perturbation controls that tail, and isolated low eigenvalues continue on the common H² domain. This verifies the Kato perturbation interface directly; the full Kato book was not independently reread.

The coefficient (1−mu) on the highest derivative poses no loss of semilinear regularity: for |mu| small it is positive, and the time change tau=(1−mu)t puts the diffusion generator on a fixed domain with a smooth parameter-dependent reaction term. The mass restriction persists. A symmetry-preserving cutoff and the spectral gap give the usual smooth local center reduction; there is no continuous translation mode on this Neumann interval. The small branch's center eigenvalue is −2 eta mu+O(mu²), and the complementary spectral gap persists for fixed m.

[Henry's publisher preview](https://page-one.springer.com/pdf/preview/10.1007/BFb0089653) gives the complete Theorem 5.1.1 statement on pp.98–99: the sectorial, fractional-space, local Lipschitz and strict spectral-gap hypotheses apply here with alpha=1/2 and a quadratic remainder. [The Chapter 6 preview](https://page-one.springer.com/pdf/preview/10.1007/BFb0089654) supplies Theorem 6.1.2 on pp.143–144. These primary interfaces were checked; the entire book and all smooth-manifold proofs were not reacquired. The full-book USP download timed out. This access limit is not being represented as a new theorem proof or a missing paper-specific estimate.

The robustness statement is a retuned local codimension-one assertion. Positivity, transversality, a finite low-mode gap, uniform high-mode coercivity in a small parameter neighborhood, and continuity of the cubic coefficient suffice. It does not claim that arbitrary nearby parameters are already critical or that a neighborhood works uniformly in dimension.

## Checkable evidence and reproducibility

* `independent_controls.py` and `independent-controls.json`: 1,575 passed checks, including exact principal-block Routh tests, omission minors, threshold Sturm counts, all printed modulus coefficients, constrained harmonic solves, boundary controls and separately labeled floating spectral stress tests.
* `generic_cubic_division.py` and `generic-cubic-division.json`: 26 all-dimension symbolic identities/sign checks, with the distinct index-polynomial-division mechanism described above.
* `published-reproduction.stdout.txt`: fresh successful executions of six inspected published programs: generic cubic recurrence, cubic bound, near-threshold interval, unit mode isolation, scaled mode certificates, and sparse determinant identities. These reproduce the authors' evidence and do not constitute another independent review.
* `independent_simulation.py` and its JSON/stdout: a separate non-proof Radau/cosine-quadrature replay of the m=3, mu=.02, 16-mode illustration, compared with the archived BDF result. The numerical evidence is not used to prove branch stability or an infinite-dimensional error bound.
* `primary-sources/receipt.json`: saved original CR1971 PDF and publisher Henry previews, with URLs and hashes.

The available runtime is Python 3.9 with SymPy 1.14.0, NumPy 2.0.2 and SciPy 1.13.1. This differs from the archived tested NumPy/SciPy versions; exact symbolic results do not depend on their floating eigensolvers. Computations ran with assertions enabled. Source files and archived assets were not modified.

The independent numerical replay returned amplitude 0.3724116215432038 versus archived 0.3724116177478588. Its maximum profile difference was 7.65e-9, fixed-mass drift 8.89e-16, minimum concentration 0.5385930375, and final modal derivative norm 7.43e-11. A separately differentiated analytic Jacobian passed a centered directional-derivative control. The first finite-difference-Jacobian attempt was stopped for runtime cost; the successful run used the same equations with the analytic Jacobian and one BLAS thread. This is a reproducibility observation, not a rigorous numerical error enclosure.

## Limits, independence, and conclusion

No current sibling mathematical report or historical reviewer verdict was read before this conclusion. One sibling acquisition receipt was consulted solely for the original CR1971 PDF URL after another download failed. Raw source code for the scaled certificate incidentally describes an older, superseded endpoint and provides an exact Rouche negative control; that code comment is not used as a historical reviewer opinion or as the basis for the current pass. Published verifier PASS strings are reproduction outputs, not review conclusions. An additional isolated subagent was requested for primary PDE interfaces but the concurrency limit prevented creation.

All mathematically central published claims are covered by the exact arguments above. The review does not certify firstness, exhaustive prior art, biochemical feasibility, weak reversibility, cross-diffusion, immobile species, arbitrary-data global boundedness, far-from-onset dynamics, wave-instability optimality, a globally constant-optimal frontier, or dimension-uniform robustness. The simulations and figure generation were not exhaustively rerun; the exact theorem does not rely on them. No extended repair or new theorem research was undertaken. The result is suitable to proceed through the catalogue's separate root-level publication gate with these scope limitations preserved.
