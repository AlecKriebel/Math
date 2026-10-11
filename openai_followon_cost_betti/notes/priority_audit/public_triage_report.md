# Ranked follow-on research paths from OpenAI's October 2026 mathematics release

Date: 2026-10-06 (America/Los_Angeles). Source snapshot: `openai/math` commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`, locally `/Users/alec/Desktop/math`.

This is a research agenda, not a proof announcement. The scan covered the 372-family catalogue (722 manuscripts), with six independent discipline reviews, targeted reading of theorem statements and proof mechanisms, whole-corpus duplicate searches, primary-literature checks, and cross-family adversarial review. It was not a line-by-line audit of every manuscript or a Lean rebuild. The [source README](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/README.md) expressly reports mixed verification status. All implications below assume the exact source theorems survive validation.

Priority balances mathematical impact, how much genuinely remains to be done, and whether the proposed result is already stated in the release. Confidence describes the transfer mechanism, not the probability that all upstream proofs are correct. No exhaustive priority certificate is possible from this rapid scan. The established reductions must be credited; applying them is not inventing a new proof mechanism.

## Recommended order

| Rank | Concrete target | New input | Remaining work | Recommendation |
|---|---|---|---|---|
| 1 | Smooth even log-Minkowski uniqueness in every dimension; full even Lp uniqueness for 0<p<1 | 091 | Short theorem-chain and strictness argument | Launch |
| 2 | Exact hypersingular Riesz constants on all smooth compact surfaces, s>2 | 090 | Periodization/tail estimate, then existing manifold theorem | Launch |
| 3 | Exact pure-loss bosonic dynamic capacity regions; bundled entropy applications | 273 | Insert multimode entropy theorem into published conditional converses | Launch |
| 4 | Fixed-binary-alphabet Sakoda–Sipser lower bounds | 129 | Explicit polynomial-state coding and pullback simulation | Launch |
| 5 | Counterexample to Costa's characteristic-zero polynomial-retract question | 047 | Immediate abstract corollary; extract explicit idempotent polynomial map | Fast corollary note |
| 6 | Deterministic construction and factorization over arbitrary explicit finite fields | 003 + 142 | Classical reductions, bit-complexity bookkeeping, implementation/certificate | Launch as one combined algorithms stream |
| 7 | Strict inequality between equivalence-relation cost and 1+first L2-Betti number | 259 | Immediate invariant calculation; explicit example package | Fast corollary note |
| 8 | Universal rational Hodge theorem for K3 moduli spaces and their mixed products | 032 | Motive decomposition; remove restrictions in existing companion corollary | Useful consolidation, lower novelty |
| 9 | All-dimensional subcritical Lane–Emden universal and Dirichlet estimates | 370 | Apply established Liouville-to-estimates transfer with exact boundary hypotheses | Short PDE application package |

Launch 1–4 first if research capacity is limited. Ranks 5 and 7 can be handled together as short, carefully attributed consequence notes. Rank 6 is a useful separate computational stream. Ranks 8–9 have broad scope but less independent novelty because their conditional transfer mechanisms are already printed.

## 1. Smooth logarithmic Minkowski uniqueness

**Exact target.** For every n≥2 and p∈[0,1), every smooth strictly positive even f on S^(n−1) has a unique smooth origin-symmetric strictly convex solution of

`h^(1−p) det(∇²h + h I) = f`.

For 0<p<1, also establish uniqueness among arbitrary full-dimensional origin-symmetric convex bodies with the same Lp surface-area measure.

**Why this door is open.** Family 091 proves the origin-symmetric logarithmic Brunn–Minkowski inequality, and hence the Lp inequalities. [He–Liu, Theorem 4](https://arxiv.org/html/2510.21530v1), explicitly turns that hypothesis into smooth even uniqueness, including p=0. For general bodies with p>0, use the mixed-volume inequalities in both directions and strictness from Jensen's inequality.

**First deliverable.** A precise theorem combining the new inequality and the existing uniqueness theorem, with a separate short proof for nonsmooth bodies at p>0. Check normalizations and equality conditions. No new central convexity inequality is apparent.

**Boundary.** General nonsmooth uniqueness at p=0 is false: equal-volume boxes with the same coordinate normal directions have the same cone-volume measure. Do not omit smooth positivity at the logarithmic endpoint or origin symmetry anywhere.

**Novelty/trust.** The uniqueness statement was not found in family 091, which states volume and B-conjecture consequences. Its Lean scope covers the log-Brunn–Minkowski input, not this application. Independent review accepted the transfer. [Detailed evidence](agent_notes/geometry_analysis.md), [adversarial audit](agent_notes/geometry_adversarial_audit.md).

## 2. Exact hypersingular Riesz-energy constants

**Exact target.** For the covolume-one triangular lattice Λ and every s>2, determine

`C_(s,2) = ζ_Λ(s) = Σ_(v∈Λ, v≠0) |v|^(−s)`.

For a smooth compact embedded surface M of area A, this gives ordered-pair minimal energy

`E_s(M,N) ~ ζ_Λ(s) A^(−s/2) N^(1+s/2)`.

In particular, the unit two-sphere has coefficient ζ_Λ(s)/(4π)^(s/2).

**Why this door is open.** Family 090 proves triangular-lattice universal optimality for density-one infinite planar configurations. The potential t^(−s/2) is completely monotone. The [Hardin–Saff theorem](https://arxiv.org/abs/math-ph/0311024) transfers the planar constant to manifolds; the lattice value is an explicit [Brauchart–Hardin–Saff conjecture](https://www.math.vanderbilt.edu/saffeb/texts/235.pdf), Conjecture 2.

**First deliverable.** Close the finite-to-infinite bridge: place rescaled N-point square near-minimizers in periodically repeated boxes, separated by ε√N gaps. The inter-box energy per point is O_ε(N^(1−s/2)), hence vanishes. Rescale to density one, apply 090, then take N→∞ and ε→0. Pair this lower bound with the standard lattice upper bound. Root review found no unsupported central conjecture in this route.

**Boundary.** Keep ordered versus unordered pairs and covolume normalization consistent. This determines an energy constant, not microscopic uniqueness or crystallization of every minimizer. Exclude s=2 and unsupported second-order claims for 0<s<2.

**Novelty/trust.** The release already treats infinite-plane energies, renormalized long-range energies and the logarithmic sphere term; this finite hypersingular constant was not found. It is distinct from the already active local planar triangle-program project. [Detailed evidence](agent_notes/geometry_analysis.md).

## 3. Optical communication trade-offs from the entropy photon-number inequality

**Exact first target.** Unconditional classical/quantum/entanglement dynamic capacity and public/private/secret-key dynamic capacity regions for the pure-loss bosonic channel, transmissivity η∈[1/2,1], under a finite mean input photon budget N.

**Why this door is open.** The vacuum-input specialization of family 273 is precisely the strong multimode minimum-output-entropy hypothesis in [Wilde–Hayden–Guha's published converses](https://www.markwilde.com/publications/PhysRevA.86.062306.pdf), Sections III.G–H. Their achievability already exists. For example, the quantum dynamic region is the closure of the union over λ∈[0,1] of

- C+2Q ≤ g(λN)+g(ηN)−g((1−η)λN),
- Q+E ≤ g(ηλN)−g((1−η)λN),
- C+Q+E ≤ g(ηN)−g((1−η)λN),

where g(x)=(x+1)log(x+1)−x log x and the established net-resource conventions are retained.

**First deliverable.** Match energy constraints, code ensembles, tensor powers, entropy units and closures; replace the entropy conjecture in the existing converse. No new capacity formula is being invented.

**Useful bundled targets.** (a) Sharp n-mode additive Gaussian-noise entropy minimization, `S(N_ν^⊗n(ρ))/n ≥ g(g^(−1)(S(ρ)/n)+ν)`, for finite-energy inputs and 0<ν<1, using an energy-controlled thermal-attenuator limit. (b) Common/confidential-message broadcast with arbitrary preshared-key rate in the stronger-Bob regime η≥1/2, under the source's coherent-encoder and strong-secrecy conventions, via [Pereg–Ferrara–Bloch, Theorem 6](https://arxiv.org/abs/2105.04033).

**Boundary.** The independent reviewer found the displayed η<1/2 broadcast formula inconsistent at η=0 with Bob decoding the common message; it is excluded pending correction. An unrestricted-encoder confidential-capacity claim needs its own model audit. Ordinary pure-loss quantum/private capacities and the release's ordinary two-receiver classical broadcast region are not new. General thermal-channel quantum capacities do not follow.

**Novelty/trust.** Published conditional regions plus a new inequality can make a useful unified application paper; searches did not find these trade-off conclusions in the release. Family 273's formal scope covers finite-energy EPnI, not these capacities. [Detailed evidence](agent_notes/physics_operators_topology.md), [independent audit](agent_notes/quantum_adversarial_audit.md).

## 4. Binary-alphabet automata separations

**Exact target.** Explicit binary languages recognized by n-state one-way nondeterministic automata for which every two-way deterministic automaton requires `2^(n^Ω(1))` states. As a companion, audit the analogous fixed-alphabet lower bound for complementing two-way nondeterministic automata.

**Why this door is open.** Family 129 establishes exponential lower bounds for relation-liveness languages over a growing alphabet of binary relations on h points. Encode each relation by its h² adjacency bits. A binary source uses polynomially many states; a two-way binary target pulls back to a relation-alphabet machine with polynomial overhead.

**First deliverable.** Write explicit endmarker-aware compilers and prove the simulations preserve acceptance, stay moves and nonaccepting infinite runs. The independent audit accepts a conservative O(h⁴) source size and O(s h²) target pullback, enough for a stretched-exponential lower bound. Optimize only after the robust superpolynomial theorem is complete.

**Boundary.** Do not claim `2^Ω(n)` after polynomial source expansion, and do not claim L≠NL. Invalid binary encodings must be handled in the source; the pullback only encounters valid codewords.

**Novelty/trust.** The source explicitly limits its headline to growing alphabets. This is a clean removed restriction with a small, checkable construction. [Source and details](agent_notes/computation_combinatorics.md), [independent reduction audit](agent_notes/pde_geometry.md).

## 5. Costa's polynomial-retract question over C

**Exact target.** A nonpolynomial C-algebra A of transcendence degree four that is a retract of C[x₁,…,x₅]. Prefer an explicit idempotent polynomial endomorphism of affine five-space with this image.

**Why this door is open.** Family 047 supplies A[t]≅C[x₁,…,x₅] while A≄C[x₁,…,x₄]. Coefficient inclusion and evaluation at t=0 form a split retraction; conjugate by the supplied stabilization isomorphism. The cancellation/retract relationship is already recorded in [Nagamine, Proposition 1.4](https://arxiv.org/abs/1811.04153).

**First deliverable.** Extract the stabilization maps and compute the five components of the idempotent endomorphism, retaining the upstream obstruction to polynomiality. The existential counterexample is immediate.

**Boundary/novelty.** Ambient dimension five, not four. No new core proof is needed; this merits a precisely attributed consequence note, not an independent-breakthrough claim. No Costa/retract conclusion was found in the source. The listed Lean scope includes the cancellation input. [Details](agent_notes/geometry_analysis.md), [audit](agent_notes/geometry_adversarial_audit.md).

## 6. Deterministic finite-field construction, roots and factorization

**Exact target.** Given an explicitly represented finite field F_(p^m), deterministically factor dense input polynomials in time polynomial in degree, m and log p; construct extension fields of prescribed degree without GRH. Include fixed-r root extraction with the dependence on r stated honestly.

**Why this door is open.** Family 142 supplies deterministic polynomial-time factorization over prime fields. Compute the Berlekamp algebra over F_(p^m), use trace-pairing coordinates to separate its factor components, factor the resulting prime-field polynomials using 142, and split by gcds. [Shoup's irreducible-construction reduction](https://www.shoup.net/papers/detirred.pdf), Theorem 3.1, provides the construction bridge. Family 003 also supplies the weak-GRH-style zero-free input used in [BIMS, Section 6.2](https://arxiv.org/abs/1702.00558) for general nonresidues and root extraction.

**First deliverable.** One precise bit-model theorem and reproducible algorithm, including squarefree decomposition, inseparable pth roots, field representations and output size. State polynomial dependence on r or prescribed degree where required; do not upgrade it to polynomial in log r.

**Novelty/trust.** Classical reductions are the mechanism. The new prime-field input already does most conceptual work. Quadratic nonresidues and square-root extraction are already in the release; exclude them as new claims. The independent reviewer accepted extension-field factorization. [Arithmetic evidence](agent_notes/arithmetic.md), [algorithmic evidence](agent_notes/computation_combinatorics.md).

## 7. Cost is not determined by first L2-Betti number for orbit relations

**Exact target.** An explicit free probability-measure-preserving orbit relation R with β₁^(2)(R)=0 but Cost(R)>1, disproving the relation-level equality Cost(R)=1+β₁^(2)(R).

**Why this door is open.** Family 259 gives one group Γ with free actions Y_M of costs ≤1+99/M and a Bernoulli action X of cost ≥1+η. The cost–Betti inequality forces β₁^(2)(Γ)=0; free-action invariance transfers this to R_X. Γ is infinite, so β₀^(2)=0. [Gaboriau's question and inequality](https://perso.ens-lyon.fr/gaboriau/Travaux-Publi/FAQ.pdf) are the established bridge.

**First deliverable.** Explicit presentation/action reference, invariant calculation and an exact statement of the failed relation-level conjecture. Independent review accepted all hypotheses used here.

**Boundary/novelty.** Infimum-defined GROUP cost remains 1=1+β₁^(2)(Γ); do not claim that equality fails. This is an immediate consequence of the new fixed-price counterexample, with limited independent novelty. [Evidence](agent_notes/algebra_groups_probability.md), [audit](agent_notes/physics_operators_topology.md).

## 8. Hodge for K3 moduli spaces and mixed products

**Exact target.** Rational Hodge in all codimensions for finite products of smooth projective moduli spaces of stable sheaves or eligible twisted Bridgeland-stable objects on projective K3 surfaces, including arbitrary Hilbert schemes S^[n], with different K3 bases allowed.

**Mechanism.** Family 032 supplies Hodge for arbitrary mixed K3 products. [Bülles, Theorem 0.1](https://arxiv.org/abs/1806.08284) makes each moduli-space motive a direct summand of a sum of Tate twists of K3-power motives. Tensor the decompositions and transfer cycles through algebraic correspondences.

**First deliverable.** State the maximum exact universal scope, with smoothness/projectivity/stability hypotheses and mixed-product bookkeeping. Do not assume a universal family when the theorem uses quasi-universal/twisted data.

**Reason for lower rank.** Adversarial whole-corpus checking found essentially the same moduli/self-power transfer in the earlier K3 quadratic-locus companion (paper.tex lines 5214–5255); the subsequent universal Kuga–Satake theorem removes its restriction. Thus universal consolidation and mixed products are useful, but the mechanism is already in the release. Do not claim arbitrary deformations of K3^[n] type, singular moduli, or finite-dimensional Chow motives. [Audit and exact duplicate](agent_notes/geometry_adversarial_audit.md).

## 9. Complete subcritical Lane–Emden a priori estimates

**Exact initial target.** For n≥3, p,q>1 and `1/(p+1)+1/(q+1)>(n−2)/n`, prove universal distance-to-boundary bounds for nonnegative classical solutions of `−Δu=v^p, −Δv=u^q`:

`u(x) ≤ C dist(x,∂Ω)^(−2(p+1)/(pq−1))`,
`v(x) ≤ C dist(x,∂Ω)^(−2(q+1)/(pq−1))`.

Package gradient/exterior bounds and fixed bounded C²-domain Dirichlet a priori estimates, with standard boundary flattening and blow-up made explicit.

**Mechanism.** Family 370 supplies the missing entire Liouville theorem. [Poláčik–Quittner–Souplet, Theorems 4.2–4.3](https://www-users.cse.umn.edu/~polacik/Publications/pqs1.pdf) supply the half-space and universal-bound transfer by doubling and blow-up.

**First deliverable.** Verify the boundary theorem's boundedness/growth and domain assumptions, then state the now-unconditional full subcritical range. Positive smooth coefficient and asymptotically power-law perturbations could add actual application content, but need separate compactness arguments.

**Boundary/novelty.** Exclude the critical hyperbola, p≤1 or q≤1 and parabolic claims. The conditional estimates already exist, so originality lies in the complete range and useful perturbation package. Independent review verified that PQS Theorem 4.2 supplies the needed half-space exclusion; spatially variable coefficients still require a separate adaptation. [Evidence](agent_notes/pde_geometry.md), [independent review](agent_notes/geometry_analysis.md).

## Hold in reserve; do not label straightforward yet

- **Multispecies relativistic Vlasov–Maxwell (362):** potentially the highest physical-impact extension. Start two species with charges ±1, then fixed positive masses/arbitrary charges. The signed cancellation seems geometric, but the species-pair impulse estimate, angular occupation and common momentum bootstrap must be re-established. This is a medium-risk adaptation, not a proved corollary.
- **Weighted nonnegative hafnian FPRAS (113):** unweighted perfect-matching FPRAS is not by itself a bit-complexity theorem for binary-encoded weights. A compact exact weighted-to-unweighted matching gadget remains the explicit gate. Never expand an integer weight into that many edges and call the result polynomial time.
- **Brenier stability for nonuniform log-concave sources (374):** concrete midpoint-density mechanism, but weighted mass differentiation and interpolation still need checking.
- **Smooth projective rational-point undecidability (004):** Poonen's existing reduction supplies a fast corollary; lower incremental novelty than the leading streams.

## Exclusions and validation record

Already present in the release: nonsofic groups, failure of surjunctivity, many UGC/CSP consequences, Vinogradov least quadratic nonresidues, deterministic square roots, sharp effective class-number lower bounds, Euler's idoneal-number list, full BSD for density-one twist families, ordinary pure-loss broadcast capacity, and model-ball spectral inequalities. The local wreath-Hopfian effort is already active.

Unsupported jumps rejected: quasi-RH→RH; rank-zero/one BSD→all ranks; CM Hodge→general Hodge; Nagata→SHGH; Fujita freeness→sharp very ampleness; simplex isotropic constants→KLS; polynomial PEPS existence→efficient ground-state computation; qualitative PDE uniqueness→quantitative stability; one-species Vlasov–Maxwell→all species without checking its key estimate.

Formalization scope was inspected where relevant, not rebuilt. ComparatorChallenges files are statement templates and may intentionally contain `sorry`; they must not be confused with the actual solution library. No proposed follow-on is represented as Lean-verified. No external individuals were contacted, no research stream was launched, no theorem was marked solved, and no DOI release was created.
