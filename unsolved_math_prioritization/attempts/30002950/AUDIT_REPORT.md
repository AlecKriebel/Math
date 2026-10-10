# Independent audit: nonbasic a-number-one strata

**Problem:** 30002950.

**Decision:** ACCEPT AS PARTIAL, with no necessary mathematical correction.

**Full Chen–Viehmann Conjecture 5.1:** neither proved nor disproved by this work.

**Review date:** 2026-10-10 UTC.

## 1. Precisely what is accepted

For the canonical minimal, slope-adapted reference lattice, and for either coefficient ring and Frobenius specified in the candidate, the following deductions are sound:

1. Every Dieudonne lattice has a unique smallest minimal lattice containing it.
2. If the bi-infinitesimal part is nonzero, the colength in this hull is at most

   C = sum_i (m_i−1)(n_i−1)/2 + sum_{i<j} m_i n_j,

   with the simple factors listed in increasing slope order, including repeated factors separately. Equality holds exactly when the a-number is one.
3. The entire a-number-one locus is a union of J-strata and of J-orbits of strata.
4. When there is only one distinct interior slope, arbitrary slope-zero and slope-one factors do not prevent the published basic single-orbit result from applying. The entirely ordinary case has empty a-number-one locus.

The argument does **not** establish that the union in item 3 consists of one orbit when there are multiple distinct interior slopes. The acceptance is a mathematical review of these restricted claims, not a formal proof certificate, a novelty certification, or a resolution of the original problem.

The audited candidate is identified by:

- PROOF.md, 14,881 bytes, SHA256 `6f1730775744b107fdbc408cae0470ab0d78eca015be45fa5f7e25b3b06cc51e`
- Candidate inventory SHA256 `7eff2a3f3503353f97f4d96f81c585e1a0028501e0b66b70a2458c8583878321`
- Candidate source metadata SHA256 `11938074b98d2c24725c65f48b4089f5102a37db8048a21f339289bff2c6ae03`

## 2. Target and source-scope authentication

Chen–Viehmann Conjecture 5.1 concerns a single J-orbit of **invariant-function strata** containing every lattice of a-number one and no other lattice. Point transitivity, a generic sublocus, and constancy of only one numerical invariant would each be weaker or different assertions. The source's Proposition 5.11 assumes isoclinicity. Section 5 introduces the minimal reference lattice used here, while Remark 2.1 warns that changing the representative b without transporting the reference convention can alter the stratification. These distinctions are preserved in the candidate. See [Chen–Viehmann, Sections 2 and 5](https://arxiv.org/abs/1507.02806v2).

The workshop formulation also covers both the unramified mixed-characteristic and equal-characteristic settings, with q-Frobenius. Its nonbasic assertion is a proposed extension of the basic a-number-one comparison, not a published nonbasic theorem. See [Oberwolfach Report 39/2015, pp. 2297–2299](https://doi.org/10.4171/owr/2015/39).

Viehmann's Theorem 4.11(i)–(ii) and equation (4.21) genuinely concern a bi-infinitesimal isocrystal with possibly several Newton slopes. Section 4.1 orders the distinct slopes before imposing bi-infinitesimality. The formula includes pairs of different slopes and pairs of distinct copies of the same simple slope. Theorem 4.11 is a theorem about a cyclic lattice with a stated leading-coefficient condition. It is not, as written, a two-sided maximal-colength criterion for arbitrary lattices. Similarly, Lemma 4.10 is stated on the a-number-one locus. The candidate correctly supplies the additional arguments instead of silently enlarging either source statement. See [Viehmann, Sections 4.1–4.3](https://arxiv.org/abs/math/0502320).

## 3. Integral ordinary splitting

The splitting asserted in Section 2 is valid. On M/epsilon^r M, images and kernels of sufficiently high iterates of Phi stabilize because the module has finite length and sigma is an automorphism. The stabilized image and kernel form a direct sum. The construction is functorial for maps commuting with Phi, so reduction maps preserve the two factors. Reduction of the stable-image factor is surjective: choose a common sufficiently large iterate on both adjacent quotients and lift its preimage. The same holds for the complementary factor.

Taking inverse limits therefore gives an integral decomposition with Phi invertible on one factor and topologically nilpotent on the other. After inverting epsilon these are the slope-zero and positive-slope summands. V commutes with Phi, so both factors remain V-stable. Applying the same construction to V on the positive-slope part separates slope one from the slopes strictly between zero and one. Thus this is a splitting of the lattice itself, not merely its isocrystal. On the ordinary factors one of Phi and V is surjective, so each contributes zero to the a-number.

This argument uses completeness, finite length, and the invertibility of the coefficient automorphism. It applies equally to Witt vectors with q-Frobenius and to k[[t]]. It does not claim that different *interior* slopes split integrally.

## 4. Hulls of arbitrary lattices and cyclic selection

The operator construction of the hull is sound. On a slope m/h, with ah+bm=1,

    tau = epsilon^(−m) Phi^h,
    pi  = epsilon^a Phi^b,
    pi^h = epsilon tau^b,
    Phi = pi^m tau^a.

These are additive semilinear operators; pi need not be O-linear. This causes no problem: their images of O-submodules are O-submodules, and they commute with each other and with every element of J. Both preserve the canonical reference lattice. Including the slope projections, the generated O-submodule is consequently bounded and finitely generated, and contains the original full-rank lattice. Since tau has determinant valuation zero, inclusion tau P subset P is equality.

The elementary descent argument behind Chen–Viehmann Lemma 5.10 applies to every such stable lattice in an isotypic component, independently of its a-number. One chooses a Frobenius-fixed basis modulo pi and lifts it to tau-fixed vectors. Such lifts exist by successive Frobenius difference equations over the algebraically closed residue field and completeness. Their pi iterates through a full period give an O-basis. On these vectors pi^h equals epsilon and Phi has the required index shift. The resulting O-linear change of basis commutes with Phi. Hence the lattice is a J-translate of the minimal reference. All minimal translates have the same stability properties, proving smallestness and uniqueness. Ordinary components follow from the corresponding slope-zero descent after rescaling Phi where appropriate.

For cyclic selection, normalize the hull to the reference. In a multiplicity-l slope component, the quotient by pi is k^l and tau acts as q^h-Frobenius. If the image of M were contained in a hyperplane defined over F_(q^h), its inverse image would be a proper tau- and pi-stable lattice. Together with the other components this would be a smaller permitted hull. This contradiction proves that each relevant inverse-image hyperplane is proper in M/epsilon M. There are only finitely many such rational hyperplanes, and a finite union of proper subspaces cannot cover a vector space over infinite k.

A vector outside that union has leading coefficients independent over F_(q^h), simultaneously for all slopes. The Moore determinant then spans the quotient under powers of tau. Iterating pi and using pi^h=epsilon tau^b promotes this to full hull equality. Full rank of its Dieudonne module follows from the cyclic colength argument. This avoids the erroneous inference that the source's a-number-one hull lemma already covered arbitrary M.

## 5. Cyclic formula, both characteristics, and both directions

The transfer to q-Frobenius and equal characteristic is accepted on the algebraic proof, not on a presumed geometric equivalence. The companion TRANSFER_DETAILS.md spells out the load-bearing points:

- The correcting monomials can be chosen with bounded difference of exponents. Their increasing weight therefore gives epsilon-adic convergence in the ordinary skew-polynomial ring with complete coefficients; no arbitrary completion is needed.
- Principal-annihilator division uses leading-coefficient cancellation, a strictly improving integer weight, and a bounded range of exponent differences. Witt-vector carries can only increase weight. Equal-characteristic coefficients satisfy the same leading rules, with no carries.
- The cross-slope leading index is m_i n_j for increasing slopes, and every correction term has larger index.
- Eliminating one copy of a repeated slope preserves the appropriate finite-field independence by the q^h-Frobenius difference equation.

These checks recover the cyclic formula without importing display deformation or a dimension theorem into a setting where it was not proved. The natural finite fields are F_(q^h), not F_(p^h) when q differs from p.

The maximality argument then has both needed directions. For arbitrary M choose a cyclic M' inside its interior part with the same hull. Exact additivity of length gives

    C = length(P(M)/M) + length(M/M'),

after suppressing the ordinary factors. Therefore d(M)≤C, and equality forces M=M' on the interior part, hence a=1. Conversely, if a=1, a lift of its quotient generator generates the whole interior Dieudonne module: iteration of M=Dv+(Phi,V)M pushes the remainder into every epsilon-power. The O-submodule Dv is closed because it is a submodule of a finite free module over a complete discrete valuation ring. Applying the cyclic formula gives d=C.

The joint topological nilpotence needed here follows from interior slopes and the commuting relation Phi V=epsilon. The same argument shows that a nonzero cyclic interior lattice has a-number exactly one, rather than merely at most one. The entirely ordinary case must be excluded from the maximality biconditional, as the candidate explicitly does.

## 6. Recovery from the full function and the one-interior-slope case

With the source's relative-position convention, M subset jM0 if and only if all coordinates of f_M(j) are nonnegative. Thus f_M gives the entire set of containing minimal translates and, in particular, its unique smallest member P(M). The sum of the coordinates at a representative for that member is length(P(M)/M). Consequently the accepted criterion is constant on each function stratum. Equivariance of the hull gives constancy on every J-orbit of strata as well. No uniqueness of that orbit follows from this reasoning.

For exactly one interior Newton slope, integral splitting writes both lattices and the reference as three factors, and J is the product of their automorphism groups. Normalize the ordinary factors using their groups and apply the published isoclinic theorem to the interior factor. Relative positions of direct sums are sorted unions of those of the factors. This proves that all a-number-one functions lie in one J-orbit in this special nonbasic class. Saturation excludes other a-numbers from the orbit. No unjustified converse from a sorted union to its individual summands is used.

For the entirely ordinary isocrystal, a=0 for every lattice. The constant-zero function is not any f_M because central multiplication of the argument by epsilon^r shifts every coordinate by −r. It is J-invariant under reindexing. It therefore realizes the literal existential formulation for the empty locus, while not being a nonempty geometric stratum.

## 7. Exact adverse example and independent finite controls

The rank-six lattice in the candidate is correct. Its generating basis has determinant epsilon up to a unit relative to the reference, so its colength is one. The displayed Phi and V iterates recover e1, f2, e2 and f1 because 1−epsilon is invertible, and then recover epsilon e0 and epsilon f0. Thus it is cyclic and stable. Its two projections are the full simple minimal lattices, yet the lattice is glued rather than their direct sum. The direct sum has a-number two, whereas the glued lattice has a-number one. Its formula gives C=1, not zero and not four.

Independent exact controls used arithmetic over GF(16), including q=2 with genuinely different forward and inverse Frobenius maps and q=4, and repeated simple factors. Eight nonconstant-tail cyclic examples of types

    (1,2)+(2,1),
    (2,3)+(3,2),
    (1,2)+(1,2)+(2,1),
    (2,3)+(2,3)

had respective colengths 1, 6, 4 and 8, always a-number one, for both tested q values. The leading-coefficient Moore condition was checked rather than assumed. Tail containment was checked to control truncation. An independent enumeration of all 2,825 F2-subspaces of the rank-six quotient modulo t found 25 stable subspaces; only the displayed glued lattice and the direct sum had full minimal hull. Additional checks tested 1,116,160 correction inequalities and 127 coprime semigroup gap formulas. Deliberately using forward instead of inverse Frobenius, omitting cross terms, or reversing the cross-term order is detected.

The candidate's original diagnostic also replays exactly under its pinned inventory. These checks are adverse controls and reproducibility checks only. They establish neither all possible coefficients nor all relative positions against J, and they give no finite substitute for the universal mixed-characteristic argument.

## 8. Literature limits and disposition

The current primary-source scope checks support the candidate's caution. [Shimada's June 2026 manuscript](https://arxiv.org/abs/2606.03062v1) is about basic strata and explicitly cites the a-number-one orbit statement in the basic case. [Li's June 2026 revision](https://arxiv.org/abs/2605.30929v2) addresses nonbasic reduction-to-Levi morphisms and affine-space fibers. Neither inspected statement supplies the missing equality of invariant-function orbits. Terminology searches in Li's full source found no a-number/a-invariant discussion or Chen–Viehmann citation. This is a bounded literature assessment, not proof that no other solution exists.

No replacement of the candidate's theorem or restriction of its stated partial domain is required. The transfer supplement is explanatory precision, especially about bounded exponent differences and carries. The remaining mathematical task is still the comparison of the **entire** invariant function, up to J-reindexing, for cyclic lattices with at least two different interior slopes. Acceptance must not be promoted from PARTIAL to SOLVED.
