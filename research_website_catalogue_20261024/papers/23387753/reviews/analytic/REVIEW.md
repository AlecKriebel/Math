# Independent analytic review — Zenodo 23387753

**Verdict: PASS within the stated mathematical scope.** The principal all-dimensional construction, its uniqueness and quenched bond/site threshold assertions, and the separate planar antecedent deductions are supported. No blocking mathematical defect was identified. This is an independent AI-assisted analytic review, not human peer review, proof-assistant formalization, or certification of bibliographic priority.

Paper: Alec Kriebel, *Finite-energy lattice percolation with internal critical probability one*, version 1.0.0, 15 October 2026. DOI [10.5281/zenodo.23387753](https://doi.org/10.5281/zenodo.23387753). Review completed 2026-10-25 UTC (24 October locally).

## Source identity and complete coverage

- Published five-page PDF: SHA256 `a5c6c86d503729e9f4591fc9aaa42cda9b81d4f78912f67a9a82dcdea993243e`.
- Complete 152-line published `note.tex`: SHA256 `2d4c37189b2e6f7a6faad2fbf3aa43e8d4a06688bbe5de63f7a705e0f65c4e54`.
- Source/verification ZIP: SHA256 `960d76417b4cc13b10be02589810a1cd17ff1183b6d6a3d0b91eddb28a39c2c7`.
- All five PDF pages and the complete mathematical source were read. There is no separate mathematical supplement PDF. Page 4 was additionally rendered and visually inspected, including both planar bounds and the midpoint formula.
- Cached Tectonic reconstruction succeeds and all five extracted page texts equal the published text. The rebuilt PDF is not byte-identical: SHA256 `d19cd0a303b0dcd47fdb952c14d33292629e1f9e97f569c24c15c80dcfc528d4`. See `source_binding.json` and `source_build.log`.
- The archive contains historical proof/review/priority materials. Their review opinions were deliberately not consulted before this verdict and were not used to support it. No sibling opinion was read. The full current written argument stands in `note.tex`; fresh controls were written separately.

Coverage by page: p.1 exact finite-energy and threshold definitions, context and Theorem 1; p.2 general graph kernel, finite-past cuts and Borel–Cantelli; p.3 uniqueness, quenched thinning, measurability, conditional finite energy and lattice input; p.4 dimensional caveat, exact HM projection and both planar thinning arguments; p.5 chronology/priority limits, disclosure and references. All substantive mathematical claims were assessed.

## Exact scope and quantifiers

Theorem 1 is an **existence theorem for each fixed integer d≥2**, on nearest-neighbor edges of Zᵈ. It constructs a law invariant under the full graph automorphism group and mixing under translations. Mixing implies translation ergodicity. Its ordinary finite energy is strict conditional positivity of both edge states given all other output edges, almost surely. A uniform positive bound is not asserted.

Almost surely there is exactly one infinite connected component C, while finite components are allowed. Neither X nor its retained tree is claimed to be connected or everywhere percolating. For almost every realized output X, independent Bernoulli bond thinning with any retention p<1 has no infinite component; at p=1, X percolates. The same conclusions hold for thinning C and for independent site thinning. These are quenched statements about the realized graph, not merely an annealed probability calculation at one chosen p.

Proposition 2 is stronger in its ambient setting: the perturbation works on any countably infinite connected simple bounded-degree graph supplied with a one-ended spanning tree, without requiring invariance of that tree. The extra invariance and mixing conclusions in Theorem 1 come from the chosen lattice input.

The arguments are mathematical deductions. The iid marks and the spanning-tree input are parts of the defined probability law, not empirical assumptions.

## Independent reconstruction of Proposition 2

### Finite pasts, bypass control and summability

A locally finite one-ended tree has a unique infinite ray from each vertex. Removing a tree edge gives one finite and one infinite side. Along the ray from v, the finite sides Sₙ contain v, strictly increase, and exhaust the whole vertex set: the unique ray from any other vertex eventually coalesces with the ray from v. Thus the positive integers sₙ=|Sₙ| are distinct and tend to infinity.

A tree path between endpoints of any ambient edge crossing Sₙ must use its unique tree boundary edge tₙ. Therefore the maximum finite-side size along that path is at least sₙ. The corresponding non-tree insertion probability is at most 2⁻ˢⁿ. The finite degree assumption gives at most Δsₙ ambient crossing edges. These statements apply to every non-tree crossing edge, including a chord whose endpoints are far apart in tree distance. No locality of that tree path is assumed.

Consequently the probability that tₙ is deleted or any non-tree bypass across Sₙ is inserted is bounded by (1+Δsₙ)2⁻ˢⁿ. Summing over the distinct sizes gives 1+2Δ. The first Borel–Cantelli lemma needs no independence of these cut events, which can share many edge coordinates. Eventually the only output boundary edge of Sₙ is the retained tₙ. Intersecting over countably many starting vertices and integrating the conditional probability-one statement over the tree produces one joint full-measure event.

The maximum in the insertion rule is essential to this estimate; replacing it by a smaller local size would not control every cut. The independent negative control below detects precisely that failure.

### Existence and uniqueness of the infinite component

Only finitely many edges are deleted along the ray from any starting vertex, so the retained tree contains an infinite tail. Every retained infinite tree component has a ray, by local finiteness. Rays coalesce in the original one-ended tree, and their sufficiently late retained tails therefore meet. This proves that the retained tree has exactly one infinite component C_R.

For an infinite output component containing v, choose a late Sₙ for which its sole boundary edge is tₙ and the entire remaining original ray tail is retained. The component must leave the finite set Sₙ. It can do so only through tₙ, whose endpoints lie in C_R. Hence it meets C_R. This proves uniqueness in X even though added non-tree edges might join many finite retained-tree pieces.

No amenable-lattice uniqueness theorem or insertion-tolerance uniqueness result is silently used. The argument works in the more general graph setting of Proposition 2.

### Quenched thresholds and exceptional sets

Fix a good pair (T,X). Every infinite connection from v in a thinned graph must traverse every sufficiently late singleton boundary edge tₙ. For any k, the probability that these k distinct, now-fixed edges survive independent bond thinning is pᵏ. Letting k grow gives zero, and a countable union over vertices rules out all infinite components.

The same deterministic collection of cut witnesses applies to every real p<1. This does not require an uncountable intersection of probability-one events indexed by p. On C, the boundary of Sₙ∩C is still exactly {tₙ}, since both endpoints lie in C_R. The site argument uses infinitely many distinct ray vertices forced by these crossings; a subsequence of k distinct such vertices again gives pᵏ. Possible shared endpoints of consecutive edges do not invalidate the argument because the ray has infinitely many distinct vertices.

The endpoint p=1 is covered separately by the retained-tail existence result. Thus the infimum in the definition of the critical parameter is exactly one. Countable graphs with finite degree have finite balls; fixed-parameter connection probabilities are limits of finite-ball expressions. Rational p and countably many vertices make the output threshold event measurable, with monotonicity covering real p. Alternatively, the stated finite-set/singleton-boundary certificate is a countable Borel condition. No selection of a hidden tree from the observed X is needed.

### Finite energy after forgetting the latent tree

Conditionally on T, every edge rate lies strictly between zero and one: each finite side has finite positive size, and each connecting tree path is finite. Realize the law with independent uniform marks. The output sigma-field excluding e is contained in the sigma-field generated by T and every other mark. Independence of the remaining mark and the tower property therefore give the two conditional expectations in equation (5).

If a positive integrable random variable Y had conditional expectation zero on an event A of positive probability in the conditioning sigma-field, then E[Y1_A]=0, contradicting Y>0 almost surely. Applying this to both r_T(e) and 1−r_T(e) establishes strict positivity after conditioning on all other **output** edges. It does not provide a common positive lower bound. Countability gives a common null set, and conditional versions can be changed to 1/2 on excluded conditioning configurations without altering the law.

This is ordinary insertion and deletion tolerance. It does not assume uniform sprinkling, finite-range dependence, a finite coding radius, positive association, or stochastic domination by a fixed positive-density Bernoulli law. The relevant parameters depend on arbitrarily large finite pasts. In particular, one must not apply a uniform-noise domination theorem to these rates.

The allowed finite components matter: finite energy gives positive probability that all finitely many incident edges at a specified vertex are closed, by successive conditioning. Thus an interpretation requiring every vertex to lie in an infinite component would be incompatible with the stated setup. The paper expressly allows finite components.

### Measurability and equivariance

Finite tree paths and finite connected sides can be detected through countably many finite vertex/edge tests. The good-input properties are Borel on the countable edge space. Extending rates by 1/2 off that probability-one domain gives a measurable kernel. Tree paths, finite-side cardinalities and the resulting probabilities commute with graph automorphisms. The construction does not depend on a distinguished root or orientation chosen from coordinate axes.

## Lattice input and mixing

The precise Timár v1 theorem requires an ergodic amenable unimodular random graph with one end and supplies a one-ended factor-of-iid spanning tree. The deterministic rooted lattice meets these hypotheses: its rooted law is deterministic; the mass-transport identity follows from translation and displacement summation; uniformly shifted finite boxes give vanishing relative boundary; and for d≥2 the complement of sufficiently large boxes is connected. The failure of one-endedness in d=1 explains its exclusion.

The factor definition is isomorphism-equivariant and measurable. Independent iid edge marks can be added to the iid vertex field. The joint field is mixing under translations because two fixed finite coordinate sets are disjoint under sufficiently large translations; approximation of arbitrary measurable events by cylinder events extends this to the full sigma-field. A measurable translation-equivariant factor inherits mixing by pulling back events. Thus the absence of a finite coding radius creates no gap in this claim, although it supplies no quantitative mixing rate. Full lattice automorphism invariance is inherited as well.

The Pemantle input is correctly restricted to dimensions 2–4. Above dimension four its limiting uniform spanning forest is disconnected, and paths between some ambient neighboring vertices would be undefined. The main proof uses the connected Timár input instead, so that boundary case is handled.

## Independent reconstruction of the planar antecedent

### Exact midpoint marginal

The published HM Section 2 model embeds primal and dual one-ended USTs on the fine square lattice at scale two. The fine sites corresponding to primal vertices are initially open, dual vertices initially closed, and a crossing midpoint takes the primal-edge state. Its independent flip probability is 2⁻ᵇ⁽ˣ⁾⁻¹, where b counts other finite-past vertices separated from monochromatic infinity by removing the site.

For a midpoint of a tree edge with finite coarse side size s, the finite side of the subdivided monochromatic tree contains s original vertices and s−1 internal midpoints; the removed midpoint is excluded. Hence b=2s−1, and its flip probability is exactly 4⁻ˢ. This gives equation (6) for primal and complementary dual edges. Taking the midpoint coordinates preserves conditional independence. Declaring all coarse vertices present defines a bond law; it is not the induced graph on the post-flip open fine sites. The fixed-phase coarse marginal also removes the need to carry the fine model’s random parity phase into that bond law.

### Fundamental cycles and bounded cuts

On a one-ended tree, a finite simple path consists of two ancestor chains meeting at their common ancestor. Finite-side edge sizes are strictly increasing along each chain, so each size occurs at most twice. For a finite primal tree cut Sₙ, all crossing edges except tₙ have their duals in T*. The finite dual cut is an even graph. In the graph formed by a tree plus tₙ*, its only possible nonempty even edge set is the unique fundamental cycle. Thus all other cut edges correspond to the single dual-tree path between the endpoints of tₙ*; there are no additional even components in a tree.

The expected output boundary size is consequently at most 1+2∑ₘ≥₁4⁻ᵐ=5/3. Conditional Fatou gives a finite liminf almost surely. Therefore some finite integer K bounds infinitely many boundary sizes. Since the Sₙ exhaust the lattice, their boundaries escape every fixed finite edge set, permitting a subsequence of pairwise edge-disjoint bounded boundaries.

After fixing the output, bond thinning removes an entire nonempty such boundary with probability at least (1−p)ᴷ. These events are independent across the selected boundaries. The chance of crossing k boundaries is at most [1−(1−p)ᴷ]ᵏ, tending to zero. An empty boundary already blocks escape. Exhaustion covers every fixed vertex. Summable primal deletions separately preserve infinite ray tails, giving threshold exactly one. The conditional-energy argument applies to the coarse marginal, and UST symmetry gives its full coarse-lattice automorphism invariance.

### Actual post-flip site graph

The same fundamental dual cycle becomes a simple fine-lattice surrounding vertex circuit. It contains one initially open crossing midpoint and otherwise a path in the subdivided dual tree. Finite-past **vertex** counts along a simple path also occur at most twice: each ancestor step strictly increases the past count. Thus the expected number of flipped-open sites on that path is at most 2∑ₘ≥₀2⁻ᵐ⁻¹=2, giving at most three open sites on the full surrounding circuit in expectation.

Those surrounding circuits escape finite fine-lattice sets because their enclosed primal sides exhaust the lattice. Fatou and a subsequence yield vertex-disjoint circuits with bounded numbers of post-flip open sites. Independent site thinning can close all currently open sites on each circuit with a uniformly positive probability for that fixed output and p<1. Nearest-neighbor paths cannot cross a simple fine-lattice circuit without sharing a vertex, so the same obstruction works. The graph has degree at most four. HM Lemma 3.1 therefore transfers site threshold one to bond threshold one for that realized open graph. It does **not** turn a site law into an external finite-energy bond law; the note correctly keeps those operations distinct.

This verifies the extra deduction. It does not establish that HM originally stated it or that the note is the first place it was deduced.

## Primary references checked

Independent acquisition receipts, exact hashes and access failures are in `reference_acquisition.json`; downloaded PDFs/text are ignored cache material.

- [Timár, arXiv:1805.10690v1](https://arxiv.org/pdf/1805.10690v1), Theorem 1, Corollary 2 and the factor definition: confirms the precise hypotheses and equivariant iid input required above.
- [Pemantle, arXiv:math/0404043v1](https://arxiv.org/pdf/math/0404043v1), Theorems 2.3, 4.2 and 4.3: confirms the lattice forest limit, dimensional connectedness split and one-endedness for d≤4. The alternative is not used in high dimensions.
- [Häggström–Mester, published ECP paper, EMIS mirror](https://www.maths.tcd.ie/EMIS/journals/EJP-ECP/article/download/1446/1446-4872-1-PB.pdf), printed pp.43–46: checked finite-energy definitions, the full Section 2 construction and flip rule, complementary UST facts, Lemma 3.1, and the discussion distinguishing the pre-flip fragile model from the later robust construction. Project Euclid’s direct URL returned non-PDF content; the journal PDF from the EMIS mirror was successfully acquired. The post-flip threshold argument is additional reasoning, not an imported HM theorem.
- [Benjamini–Häggström–Schramm, arXiv:math/9906002v1](https://arxiv.org/pdf/math/9906002v1), Question 1.1 and its adjoining definition: confirms that the historical question uses ordinary insertion/deletion tolerance and automorphism invariance, rather than uniform finite energy or everywhere percolation.
- [Benjamini–Tassion, arXiv:1505.06069v1](https://arxiv.org/pdf/1505.06069v1), Question 1 and its definition: confirms the same question is posed in that inspected version. Its uniform-sprinkling results do not apply to the present kernel.
- The cited archived lecture-notes URL was attempted through the web tool but inaccessible. Its exact Open Problem 8.15 locator was therefore not independently confirmed in this review. This is a non-load-bearing historical citation limit: the exact motivating question and energy convention were independently verified in both BHS and BT.

No comprehensive later-literature or first-priority conclusion is inferred from these checks.

## Independent exact controls

`independent_controls.py` contains fresh deterministic checks using integer graph calculations and exact rational arithmetic. No historical verifier is imported.

- All 1,441 labelled trees with 2–6 vertices, rooted at vertex 0 and interpreted as attached there to an infinite ray: 102,507 cut/path incidence checks and 36,894 bypass-probability inequalities pass. Ancestor size strictness was checked on 7,035 chains.
- Edge-size multiplicity at most two passes on 20,796 paths. After subdividing every edge, 7,035 midpoint past counts equal 2s−1; vertex-past multiplicity passes on 76,149 paths. These check the separate bond and site planar estimates.
- All 192 spanning trees of the 3×3 vertex square grid: 1,536 finite primal cuts equal the corresponding complementary-dual fundamental cycles; even-degree cycle checks pass. This is a finite duality control, not a replacement for the infinite planar argument.
- A latent mixture of the three labelled trees on three vertices: all 12 output-condition patterns yield exact conditional probabilities strictly between zero and one, agreeing with the tower calculation. Values range from 5/12 to 7/12 in this finite example; no uniform infinite-law bound is inferred.
- Exact summation with analytic tails verifies ∑(1+Δm)2⁻ᵐ=1+2Δ for several Δ and truncation points. The HM boundary bound equals exactly 5/3.
- A deliberate wrong rule using the minimum path size is rejected on the chain 0–1–2 with chord 0–2: across finite side {1,2}, the correct maximum rule gives 1/4 while the minimum rule gives 1/2, violating the required 1/4 bound.

The tests are checkable support for discrete identities. No finite test establishes the infinite iid-factor theorem, Borel–Cantelli conclusion, mixing limit, or quenched threshold; those were checked by the analytic arguments and exact imported theorem hypotheses above.

## Strongest verified conclusion and exact remaining gap

The full stated existence theorem is supported for every fixed d≥2: an automorphism-invariant, translation-mixing, ordinary-finite-energy bond law almost surely has exactly one infinite component, while both the full graph and that component have quenched internal bond and site critical probabilities equal to one. The general one-ended-tree kernel and both planar HM deductions are also supported.

**No unresolved mathematical gap was identified in those claims.** Remaining scope limits are the inaccessible lecture-notes locator, exhaustive bibliographic priority/current-openness research, independent human review, and formal proof verification. The main PDF’s historical audit/replay descriptions were not independently re-audited and were not relied upon. The paper already disclaims first priority and formal/human verification. No repair, source modification, outreach, website change, spreadsheet edit, Git action, or Zenodo mutation was performed.
