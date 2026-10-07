# Fresh V2 dependency audit: the full CM Hodge input

Checkpoint: 2026-10-07 05:02:56 UTC. Assigned audit coverage: 100%. This is a coverage estimate for the requested CM dependency audit, not an estimate that the entire K3 research program or publication objective is complete.

## Verdict and independence

**No substantive defect or counterexample was found in the requested CM dependency chain.** I directly read the pinned CM source argument before reading the archived CM reports. The source, rather than those reports, controls this conclusion. A new child independently derived the Hecke normalization and cubic polynomial from the two assigned source sections; its conclusions are incorporated below. No publication files, upstream sources, shared Git state, or external applications were changed. No external individual was contacted.

This audit checks the deduction of rational Hodge algebraicity for CM abelian varieties through the four-factor surface construction, with the explicitly cited standard Weil/splitting, arithmetic-group, abelian-moduli, good-reduction comparison, and degree-one Weil-weight results. It is a mathematical source audit; it is not a formal proof, conventional human refereeing, independent novelty audit, or certification of the unrelated Kuga–Satake/Floer input. Section 07's generalized-Hodge/Tate/standard-conjecture consequences are outside the pivotal CM input used by the follow-on and were not audited here.

I read the original target at `/Users/alec/.codex/attachments/236d83ea-ee16-4344-9bf8-fb179081c720/Pasted text.txt`. The reviewed source directory is:

`sources/pinned/preprints/The-rational-Hodge-conjecture-for-CM-abelian-varieties-September-30-2026/build/sections/`

The source content matches the archived hashes for these pivotal modules:

| Source | SHA-256 |
| --- | --- |
| 01-introduction.tex | cfaf3d085e9138e9818754cf3493a55be497e57a2c0432242f4dae5089f4720a |
| 02-tensors.tex | e7b6dee31ff3296e6fe1cbfda70441de47b5c6042c0a7216ac52b8b68eaa7e2f |
| 03-surface.tex | 0faa31073f2eec34a82a2ce7554dcc903c8136bb4bffc43d73a85bffee672d5b |
| 04-theta.tex | c3c42f2820a8f42b7e1b4dda2e4c984336fde72b09f7683afb3bed9e64237027 |
| 05a-moduli.tex | 3e25d6ae9fddf3ed47a695aad97714400c12e358beef24e703027b9a801ba346 |
| 05b-frobenius.tex | fa981f76a7ebc75b4395e4266b0619b08b74273cba346f3217ea5b736172b428 |
| 05b-satake-frobenius.tex | 36aaa88e48f9c556daa5b474b37caa51607dd6f7453a5d9607ea07b7267f84f3 |
| 05c-cm-types.tex | 7cd65bc8883c6bf513c89e841ae85812be096354516c1b90f58e81b52cb5bd79 |
| 06-assembly.tex | c9d120f17ba3b1da5b8f92700eb9bca3ca3502e9ec6a6e81558d8a44f2310a2f |

## Theta covariance, common levels, and continuity

At 04:105–255, the alternating trace product is well defined and nondegenerate by trace duality. The active positive filtration is `L tensor P_mu` together with `ann(L) tensor P_mu^*`; its annihilator description is holomorphic. Its determinant is `L^(2n)` times a constant line, whose **special-unitary** action is trivial. Thus its square root times the projected first tensor gives `L tensor Q^* = Omega_D^1`, and the double-alternating second tensor gives `L^2 tensor wedge^2 Q^* = K_D`. The constant determinant line must be retained for the later scalar action, and the source does retain it.

For `J=CZ+D`, independently comparing the Gaussian transformations in 04:406–511 gives the coefficient law `T_k(gZ)=j(g,Z) Sym^k(J) T_k(Z)` when the finite input is transformed directly on the left. The identity

`J^(-1) Im(gZ)^(-1) J^(-t) = Im(Z)^(-1) - 2i J^(-1)C`

cancels the Jacobi quadratic exponential. The bundle orientation follows from `g e_Z=e_(gZ)J`; the symmetric tensor belongs to the positive filtration, not its dual. The completion has no linear term, so the first tensor remains holomorphic.

The source uses the circle-scalar unitary splitting, then restricts to SU(V). The active determinant character is `ell^(2n)`, so its even winding permits the real double lift with square-root character `ell^n`. The two real lifts differ by a character of a connected semisimple group and hence agree. Finite smoothness then provides a stabilizer for each **finite** input family. The needed circle extension, character restrictions, and rational compatibility are explicit in [Borade et al., sections 3.1–3.1.1 and 4.1–4.1.1](https://link.springer.com/article/10.1007/s00029-025-01047-4); the global discussion specifies that rational unitary points land in the canonical rational symplectic section.

The sparse-input proof at 04:715–765 only takes a limit in a single fiber. For a fixed lattice vector `x0`, the other terms in `x0+k O_F^3` have norm at least `k ||m||/2` for sufficiently large k. Their polynomially weighted Gaussian tails tend to zero. The Minkowski lattice spans the real position space, so the resulting limits complex-span the first-tensor fiber. A finite-dimensional span is closed, and finitely many actual inputs can therefore be selected before choosing the level. No common level for the infinite limiting sequence is assumed.

At 04:855–899, theta factorization in adapted rational direct-sum coordinates is a finite sum of product inputs. The degree-two mixed coefficient is one with the stated Taylor normalization. Both unmixed terms vanish under double alternation because their multiplicity vectors lie on one line. The mixed term is the wedge of the projected first tensors, up to a fixed nonzero constant. Selecting independent cotangent values gives a nonzero endpoint top form.

The potentially fatal continuity issue is addressed at 04:786–851 and 910–946: the rational W, symplectic form, G-action, reference coordinates, finite representation, finite input, and quotient all remain fixed. Only compact-place multiplicity subspaces vary; these remain SU(3)-invariant, and their determinant characters stay trivial. The active total filtration remains exactly fixed. Smooth frames for the constant lines can be chosen in a small parameter neighborhood. A finite cover of the compact quotient by precompact lifted charts gives positive lower bounds for Im Z and bounds for every fixed derivative order. The rational support stays in fixed lattice cosets. Gaussian summability therefore gives the claimed smooth continuity on one quotient.

The sign relation permits local relabeling, followed by weak approximation of one vector in W(E). Nonzero norm, inertia, and the projection `z -> h(z,w) h(w,w)^(-1) w` are continuous. The active definite plane imposes no additional sign obstruction. Thus rational endpoint data approach the original **total** positive filtration without changing the total input. Pairing with the initial nonzero top form remains nonzero. Factoring both endpoints afterward produces finitely many individual inputs, for which one further unramified common cover exists. Its degree multiplies the nonzero integral. I found no hidden exchange of varying levels with the limit.

## PEL tuples and ordinary specialization

At 05a:157–201, the finite-type action locus has a concrete bound. For each fixed ring generator b, choose m with `m/(1+bar(b)b)` integral. The product of the two action endomorphisms is [m], so both are isogenies and the first has degree at most `m^(6s)`. The graph's product ample bundle induces `2 lambda (1+bar(b)b)`, giving finitely many Hilbert polynomials by abelian Riemann–Roch. The graph locus and the finitely many homomorphism/ring/Rosati identities provide a finite-type scheme. Homomorphism rigidity gives unramifiedness over fixed polarized moduli, and the extension property for abelian schemes over DVRs gives properness there. Proper and quasi-finite implies finite. This is finiteness over polarized moduli; it is not an assertion that CM points form a finite set.

Its reduced complex local loci are the compatible ball domains (05a:203–226). Definite nonactive completions rule out an E-isotropic vector since s>=2; compact arithmetic quotients follow. Finite type gives finitely many components. Compactness plus quasi-projectivity gives projectivity. The determinant of a unitary lattice automorphism is an integral norm-one unit even for a nonfree lattice; all its archimedean conjugates have modulus one, so it is a root of unity and is killed by a sufficiently deep marking level.

The marking deliberately permits every ordered N-torsion basis, with every pairing matrix (05a:103–110). Hence transporting it through a q-isogeny is legitimate. For selected target lattice L' and multiplier q^h the opposite lattice is `q^(-h)(L')^dual`; the scaled form remains perfect at q and preserves polarization type elsewhere. The field-level polarization descent and uniqueness match [Edixhoven–van der Geer–Moonen, Proposition 11.25](https://www.math.ru.nl/~bmoonen/BookAV/PolWp.pdf). The relative proof at 05a:448–467 descends the **homomorphism** using `beta=g^dual lambda g`, its vanishing on B'[q^h], and factorization through [q^h]. It does not assume descent of a particular line bundle. The action and marking are uniquely forced by the quotient.

The selected ordinary points at 05a:320–355 are isolated after adjoining graphs of three rational orthogonal projectors. Those projectors fix exactly the negative coordinate line locally, so the enhanced point has algebraic coordinates. After extending the number field and excluding denominators, a completely split good q decomposes its q-divisible group into height-one pieces. Each is étale or multiplicative according to dimension; these reductions are ordinary. Openness and smooth connected fibers give ordinary density on every component. This neither assumes all CM points reduce ordinarily nor assumes the separate Albanese is ordinary. The source also spreads a finite surjective sum of Albanese differences, which provides generation on every retained special fiber (05a:303–318).

At 05b:81–181, lifted ordinary label components are finite flat of rank q. Over a b-dimensional label subspace there are q^b generic graph lifts disjoint from the distinguished line. Their subgroup closures have rank one in each label component and specialize to its reduced point; a subspace containing the distinguished line fills the corresponding rank-q components. Properness extends each generic target in the full tuple model. The isogeny extension has constant degree by the polarization identity, hence is finite flat; its kernel is the closure just counted. Cartier duality transports annihilators under base change. Equal total kernels give equal target tuples, since quotient, action, transported marking, and polarization homomorphism are uniquely determined. Branch multiplicity is retained even when target tuples coincide.

## Hecke normalization and Frobenius polynomial

The active determinant-zero branches remain component-preserving by strong approximation for the simply connected special-unitary group with its noncompact active real factor. This invocation matches [Milne, Theorem 4.16](https://www.jmilne.org/math/xnotes/svi.pdf). A branch representative gamma with active component kg takes `g^(-1)Lambda` back to Lambda. Rational theta covariance consequently makes fixed-input pullback the **inverse** local spherical action (05b-satake:34–82).

The independent child rederived the following count and normalization. If `D_q b_j=q^(3/2)b_(j+1)`, raw minuscule substitutions give

`T1 b0=q^(1/2)((q+1)b0+q^2 b1)`,

`T2 b0=q(b0+(q^2+q)b1)`, and `T3 b0=D_q b0`.

The counts are those of planes or lines containing a fixed nonzero vector in F_q^3. Setting `b1=q^(-3/2)e0 b0` gives `q e1`, `q e2`, and `e3` on `(e0,q^(1/2),q^(-1/2))`. [Gross, equation (3.14)](https://people.math.harvard.edu/~gross/preprints/sat.pdf) gives exactly the raw factors q,q,1. Inversion reciprocates the parameter without dividing by the branch degree.

The bare rational scalar covariance gives `omega^2=zeta product_tau tau(r)^(-3d(tau))`, with only root-of-unity lift phases. The active determinant and projected tensor exponents add to -3, and the compact full summands contribute -3d(tau). With `w=p_c`, `bar(w)=p_1`, the unique contributing representative yields `sum_tau d(tau) nu(sigma tau(r))=-M d(g^(-1))`. Therefore the inverse geometric parameter satisfies `nu(sigma e)=-3v(g)/2`. The constant determinant line is included in this calculation.

The ordinary kernel count at 05b:124–138 gives `D1=X+qY`, `D2=XY+q^2Z`, and `D3=XZ`. X is relative Frobenius on the full tuples: its connected q-torsion kernel, polarization multiplier, and twisted marking all match. Its marking acquires no multiplication-by-q factor. Naturality commutes X with Y and Z. Thus

`X^3-(X+qY)X^2+q(XY+q^2Z)X-q^3XZ=0`.

Applying this equality to actual Albanese differences, ordinary density, and finite-sum generation proves the integral endomorphism identity. It does not rationalize the torsion group of finite-field points. Crystalline pullback retains the polynomial because all the endomorphisms commute and q is prime with residue field F_q.

The central finite-order arguments also check out. T3 is principalized by a norm-one scalar. For C0, if `I bar(I)=(q)` and `I^m=(a)`, write `a bar(a)=q^m u` with u a totally positive F-unit. Then `a^2/u` has the required ideal exponents and norm `q^(2m)`, without requiring a square root of u. Powers fix the marking. Hence for a full parameter `alpha=b(q^(1/2),q^(-1/2),e')`, `b^3 e'` is a root of unity.

The full cubic is `product_j(X-q alpha_j)`. Its three root moduli are `q^(3/2)`, `q^(1/2)`, and q. Degree-one Weil weight selects only `b q^(1/2)`, with slope `1/2-nu(e')/3` in {0,1}. Simultaneous triangularization applies on every generalized character space, so nilpotent Hecke parts do not invalidate root selection.

## Filtered projectors, conjugate ranks, and scalar assembly

The filtered-projector argument at 05c:54–130 is valid with its stated hypotheses. A finite coefficient extension, with Frobenius acting trivially on coefficients, is a direct sum of copies of the original weakly admissible module over Q_q. Both p and 1-p preserve filtration and commute with Frobenius. Weak admissibility gives `tH<=tN` for both; additivity and equality for the whole force equality on each. With only indices 0 and 1, pure slope 0 forces zero F1 and pure slope 1 forces full F1. The source does not use the false general claim that any extreme-slope subspace has pure induced Hodge type. Algebraic Hecke endomorphisms give precisely the needed filtration-preserving projectors (05c:10–48).

For every conjugate character, 05c:281–308 evaluates its separate polynomial projector in the same K-defined operators, over the actual compositum of K and its coefficients. Image and filtration ranks are matrix ranks over that field, preserved by the fixed q-adic embedding and by complex Betti–de Rham comparison. No linear-disjointness hypothesis, independent action on overlapping fields, or geometric conjugation of the variety is assumed. The resulting scalar-conjugate **Betti** spaces on the same variety have type `(1+v(g))/2`.

An algebraic Betti vector in an active space defines a Qbar-linear map from U(v), supported on the identity embedding line. Every scalar conjugate has matching source and target type. The trace-dual descent lemma therefore expresses it as a Qbar combination of rational Hodge maps. Algebraic vectors span the active space after complex extension, including the theta vectors with transcendental coefficients. This establishes the CM-source span (05c:326–389). Finite-family extraction takes a common deeper principal level; different auxiliary primes are allowed and are unnecessary in the final geometric period.

The assembly at 06:10–97 preserves the nonzero endpoint integral under a finite cover, expands finitely many wedges, and selects a nonzero four-class term. The first two are in U(v_i)_1 spans; rational maps commute with scalar complex conjugation, placing the last two in U(v_i)_c spans. The surface criterion at 03:29–124 uses the pushed-forward surface as a functional and four pure algebraic divisor kernels to produce the actual desired degree-four tensor. Its crossing sign is (-1)^6=+1 and its codimension is `(n-2)+4-n=2`. It inserts no unproved higher-degree Hodge projector.

Finally 02:332–479 switches two rows column by column, preserves oddness and total signs, composes pure transition tensors by algebraic polarization contractions, and transfers back to distinct original exterior slots. The contraction coefficient is nonzero by pairing conjugate lines with an ample polarization; its codimension is `p+p+p(s-1)-ps=p`. Scalar descent recovers the original rational cycle span. Repeated field summands and imprimitive types are retained, and s=1 or antipodal switch cases are treated by divisor pairs. The deduction concerns arbitrary CM abelian varieties and their finite products/powers, without claiming generation of the Hodge ring of a fixed power by low-codimension cup products.

## Reconciliation of archived CM reports

After completing the source pass, I read `agent_notes/cm_theta_audit.md`, `cm_arithmetic_falsification.md`, `cm_finite_locus_falsification.md`, and `root_cm_and_deformation_audit.md`.

* The theta report's deferred geometric Hecke/Frobenius and projector boundaries have matching source deductions above. Its common-level and fixed-total-input claims match the actual proof. Its limited original-Weil reconstruction remains a standard imported theorem, not an unrecorded computational certificate.
* The arithmetic report's deferred theta existence/covariance boundary is addressed by the direct theta source pass above. Its finite checks only establish incidence factors and a formal polynomial cancellation; I independently reexecuted `check_field` for q=2,3,5,7,11 without writing any output files, and the values exactly match the saved `hecke_counts.json`. Those computations do not establish moduli, specialization, or Hodge algebraicity.
* The finite-locus report's caution about all GIT/integral-base foundations not being reconstructed is accurate. Its graph-locus representability and relative-Hom citation suggestions are exposition improvements; the source supplies the graph bound, rigidity, and DVR-extension mechanism, and no counterexample or unclosed central proof obligation was identified there.
* The lead report's CM transfer claims agree with the independent derivations here. Its remaining obligation for initial perfect-complex realization through immersed Floer theory and ordinary-category comparison is **outside this CM audit**. This report does not close that separate K3 obligation or treat it as resolved by the favorable CM conclusions.

No pending substantive CM issue was found hidden by the archived reports. The strongest checked result is that the pinned source supplies a coherent complete CM four-factor construction and rational-cycle deduction under its identified standard foundational inputs. The remaining limitations of this review are the absence of a formal verification or a reconstruction of every external foundational theorem, exclusion of section 07's ancillary consequences, and exclusion of the separate universal Kuga–Satake and mixed-K3 analytic/category arguments.
