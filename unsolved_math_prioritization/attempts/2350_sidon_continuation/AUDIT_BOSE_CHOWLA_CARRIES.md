# Independent audit: canonical Bose–Chowla carry obstruction

Date: 12 October 2026. Scope: Erdős 864 / problem 2350 / row 1741, construction-specific partial theorem. This audit does not establish the interval conjecture, an extremal constant of √(2/3), or novelty. No remote or repository mutation was performed.

## Verdict

ACCEPT the theorem and its 29/30 retained-size consequence in `BOSE_CHOWLA_CARRY_PROOF.md`, after a minor topology/exposition clarification. The original frozen argument contains no identified algebraic, character-sum, or incidence error changing the theorem. Its continuity-set passage should explicitly use the relative topology on its supporting subgroup H. The corrected proof does so. No theorem constant or domain has changed.

The external input remains the standard Riemann hypothesis for polynomial Dirichlet L-functions. This is an unconditional established theorem used as an input, not an assumption of an unproved number-theoretic hypothesis. This audit does not prove that external theorem.

## Provenance and independence

The supplied manifest SHA-256 is `4088f2b016f57293f67daa0a97bf33e706c2c8da7ed8f30d6fe9f204eb1d1d9d`. Its ten file entries were independently checked for both byte count and SHA-256. A byte-identical copy of the complete input packet is preserved in the original frozen input identified in INPUT_PINS.json. The original proof has SHA-256 `d6568efa627e1904813fe5509806c1f408f76e7dec53ce97b8c3fc06e97737b3` and 14,185 bytes.

The new `independent_check.py` was written from scratch. The author's program and its reported output were not imported, executed, or used to generate the independent results. Algebraic checks use direct field multiplication and cubic enumeration, then compare the rational parametrization. Exact lifts are enumerated separately. Fourier computations are floating-point diagnostics, explicitly distinguished from the analytic proof.

## Analytic audit

### 1. Strong Sidonicity

After cancellation of λ², pair-product equality gives the sum and product of the two base-field coordinates. Equal monic quadratics give equality of unordered pairs, including the repeated-root case. This yields strong modular Sidonicity. An integer or same-coset half-integer pair-sum equality reduces to the same modular equality, so both canonical lifts inherit strong Sidonicity. Distinct nonzero ordered differences therefore have at most one representation.

### 2. Parametrization and degenerate slices

Write M=μ(θ+b)=uθ+v. Its product with θ+a is Uθ+V with U=ua+v and V=va+uδ. The θ coefficient after multiplication by θ+c is Uc+V, so the claimed c=(1−V)/U and d=Uδ+Vc are correct when U is nonzero.

When U is zero, V cannot also vanish because both multiplied factors are nonzero. V=1 produces exactly p choices c=d; V≠1 produces none. Moreover U=0,V=1 is equivalent to 1/M−θ belonging to F. Subtracting its conjugate yields N(M)=−u with the correct minus sign. The polynomial N(μ)(b²−δ)+u(b) has degree two and nonzero leading coefficient, hence at most two roots, also over odd nonprime finite fields. u(b) vanishes at most once; if u=0 then v≠0.

The exact slice sizes are p when u=0, p−1 for an ordinary u≠0 slice, and 2p−1 for a degenerate slice. Consequently Σ_b|n_b−p|≤3p and |Ωμ|=p²+O(p), uniformly in every μ≠0. All multiplicities are retained.

### 3. Rational factor and every CRT degeneracy

Direct expansion gives θ+c=−conj(M)(a−r)/(ua+v), where r=θ+1/conj(M). The condition r∈F is exactly the same N(M)=−u equation. The only possible common irreducible quadratic with θ is obtained when r=θ or −θ; r=θ is impossible, and r=−θ is equivalent to M=1/(2θ), occurring for at most one b. Thus at most three b-slices are omitted, each having at most 2p−1 points.

Outside those slices the roots θ and −r define distinct irreducible quadratics. If u≠0, the denominator factor is T−v/u: evaluating T+a at v/u gives a+v/u, whose zero is the forbidden a=−v/u. This sign is correct. Its character is the inverse of γ restricted to F*, with the scalar γ(u) inverse removed separately. Including this factor even when its local character is principal correctly assigns zero to the omitted pole. It is coprime to both quadratics. For u=0 the nonzero denominator is a scalar and the modulus degree drops to four.

For every pair (α,γ) other than (1,1), at least one quadratic local character is nonprincipal. The evaluation map at its degree-two root identifies that residue field with K. Chinese remaindering permits its unit coordinate to vary independently of the other quadratic and the optional linear coordinate. No cancellation between characters on distinct factors is possible. Therefore the composite character is nonprincipal for every such pair, including characters trivial on F* and low-order characters. There is no unexamined “generic character” hypothesis.

### 4. External RH input and full nonresonant bound

Independently inspected source: Swastik Kopparty, *The zeta function, L-functions, and irreducible polynomials*, Rutgers finite-fields notes, edition 13 October 2013, https://www.math.toronto.edu/swastik/courses/rutgers/finitefields-F13/zeta.pdf . The local seven-page PDF is 224,728 bytes, SHA-256 `19d2dea263d6545454da0dbc69b2fc76450500da33e3e5aa4e3b890c0ab59c45`.

The public PDF was independently opened. Its general-modulus definition and polynomial degree lemma were checked, along with Theorem 4 and its general inverse-root consequence; rendered pages 4–5 were visually inspected. The coefficient illustration later specializes to an irreducible modulus, but the preceding degree and root statements do not. Their combination bounds the degree-one coefficient by (D−1)√p for every nonprincipal character modulo the squarefree degree-at-most-five modulus here. Primitivity and oddness are unnecessary; imprimitive/trivial-root factors fit the same bound. Only this standard consequence is used, not the source's unrelated asymptotic formulas.

Thus every nonexcluded slice in the α-or-γ nonprincipal case is bounded by 4√p. The three omitted slices contribute at most 6p, giving an estimate stronger than the stated 4p√p+12p. If α=γ=1 but β≠1, the exact slice-size estimate and the irreducible quadratic instance of RH give p√p+3p. The only remaining tuples are α=β=γ=1, which yield precisely the stated scalar multiple of |Ωμ|. All four-character tuples have been covered.

### 5. Half-integer congruence and generator uniformity

Writing an integer residue as t and a representative as t+ε gives the congruence t_a+t_b+t_c−t_d+2ε=0 mod q. Translating this multiplicatively gives μ=λ²g^(2ε), including μ=λ²g for ε=1/2. This uses only the integer exponent 2ε=1 and never divides by 2 in Z/q. Arbitrary μ, rather than only squares, was correctly included in the preceding proof.

For fixed Fourier frequency n, resonance means q divides each n_i+n_4 for i≤3. Once q exceeds these fixed absolute values, this is equivalent to the integer equalities n_1=n_2=n_3=−n_4. On resonant frequencies the phase is exactly one because the counted coordinates lie in H. The nonresonant bound is independent of λ, g, μ and character order. Changing the primitive generator accounts for every unit dilation, while λ accounts for every translate.

### 6. Uniform weak convergence and the clarification

The measures are positive, have uniformly bounded mass tending to one, and are all supported on the same closed subgroup H. Ambient character restrictions separate points of H and are dense in C(H). Fixed-frequency uniform bounds therefore give uniform convergence for every fixed continuous function on H; finite approximation involves no parameter-dependent choice of test function.

The carry regions are continuity sets in H's relative topology. Their ambient boundaries in the four-torus would contain all of H, so a literal ambient continuity-set invocation would not suffice. The corrected proof explicitly works on H and states the relative boundary condition. This is a clarification of the natural supporting-space argument, with no additional estimate required.

Under the parametrization by independent first three coordinates, the regions have the Irwin–Hall masses 1/6, 2/3, 1/6. Coordinate seams and the planes where their sum is integral have three-dimensional Lebesgue measure zero. Continuous upper/lower approximation on H gives the asserted uniform little-oh error.

### 7. Endpoints and incidence

For the integer convention, at most one seed point moves from residue representative 0 to q. In a prescribed source role it participates in at most (p−1)+p=2p−1 congruent ordered quadruples: the zero-difference case can occur for at most one second-source choice. In a target role, pair-sum Sidonicity gives at most 2p. The union bound 8p is therefore safe, including repetitions. The half-integer representatives have no seam. Positivity and the maximum q give −q<x+y+z−w<3q, so only carries 0,1,2 occur.

For the deletion consequence, source a fixed in a genuine equality a+y+z=w gives a nonzero positive difference w−z=a+y. There is at most one ordered representation for each y, hence at most p equations per source role. With a fixed target, choosing the first source leaves at most two ordered pair-sum representations, hence at most 2p. The per-point union bound is 5p even with repetitions. Removing r points destroys at most 5pr ordered equations, so r≥C0/(5p)=(1/30−o(1))p. No dependence on the deleted subset's geometry is used.

## Independent finite verification

One explicitly constructed quadratic extension was used at each base-field order 3, 5, 7, 9, 11, 13, 17. The order-nine base field was genuinely constructed as F3[z]/(z²+1), not simulated by arithmetic modulo 9.

- All 736 nonzero μ parameters across those fields were checked.
- Direct multiplication examined 2,021,760 ordered source triples and recovered the complete solution variety for each μ.
- The rational parametrization, both exceptional equations, minimal-polynomial collisions, exact slice sizes, all stated uniform degeneracy counts, and strong Sidonicity passed.
- All 46,604,128 reduced nonprincipal global Fourier tuples were numerically checked for orders at most 9. The reduction covers all four-character tuples up to the exact unit scalar.
- All 78,337,174 nonprincipal local character pairs on nonexcluded slices were numerically checked for orders at most 13, using the sharper degree-four/degree-five RH bounds. The largest observed bound ratio was approximately 0.961260.
- Every translation and every unit dilation, with both lift conventions, was checked for field orders at most 11; 12 selected affine choices were checked at orders 13 and 17. Total: 14,832 lifts.
- Each lift's modular variety, allowed carries, exact source/target incidence bounds, and endpoint bound passed.
- All 12,800 subset/lift combinations for orders 3 and 5 verified exact deletion coverage.

Some small-field seeds have C0=0. That is compatible with the asymptotic theorem and is a reason not to turn this audit into a finite-p positivity claim. No effective threshold, best error term, sharp deletion constant, or finite-field asymptotic inference is asserted by the computations.

## Accepted scope and exclusions

Accepted: canonical length-q integer and single-coset half-integer lifts of full affine Bose–Chowla p-sets, with q=p²−1, uniformly over their translations and unit dilations, as odd field order tends to infinity; plus the resulting obstruction to retaining more than (29/30+o(1))p points in a triple-sum-free subset.

Not accepted or claimed: Erdős 864; the √(2/3) interval bound; arbitrary Sidon sets; arbitrary/noncanonical or longer lifts; mixed lattice cosets; an explicit finite threshold; novelty; permission to publish source PDFs or private coordination material.

## Public edition notice

The preceding text is the complete accepted historical proof or audit, with only the locator edits recorded in [EDITION_MAP.md](EDITION_MAP.md). Statements about accompanying diagnostic programs, original input records, or the absence of publication describe the original research or review stage. This prose-only edition distributes no executable program, detailed diagnostic collection, source PDF or image, or private record. Original and accepted file identities are recorded in [INPUT_PINS.json](INPUT_PINS.json); public-file identities are recorded in [MANIFEST.json](MANIFEST.json). [VERIFICATION.json](VERIFICATION.json) distinguishes exact finite checks, floating-point diagnostics, and integrity checks. This notice changes no mathematical argument, verdict, or hypothesis.
