# Independent adversarial review — Zenodo 23387753

**Verdict: PASS — no substantive mathematical defect found in the published claims as written.**

Reviewed: Alec Kriebel, *Finite-energy lattice percolation with internal critical probability one*, version 1.0.0, dated 15 October 2026. All five published pages and the complete corresponding TeX were read. The proof was assessed independently before inspecting archived computed outputs. No archived reviewer narrative, acceptance opinion or sibling review conclusion was consulted. This is an AI-assisted mathematical review, not external human peer review or formal verification.

## Input binding and scope

- Fresh public PDF: sources/finite-energy-percolation-note.pdf; SHA256 **a5c6c86d503729e9f4591fc9aaa42cda9b81d4f78912f67a9a82dcdea993243e**.
- Fresh verification ZIP: sources/finite-energy-percolation-verification.zip; SHA256 **960d76417b4cc13b10be02589810a1cd17ff1183b6d6a3d0b91eddb28a39c2c7**.
- The ZIP's included note.pdf is byte-identical to the separately acquired public PDF. The package index hash is **acbefb678d34b701ae1df67c6d6896c013b195c08220007d0389fa3aa2feb659**.
- Full paths and acquisition identity are in input_identity.json. All work is confined to this review directory. Local caches are ignored. No outreach, website, spreadsheet, Git or Zenodo mutation was performed.

The main falsification targets were: replacing ordinary finite energy by an unjustified conditional product assertion; unbounded bypass probabilities; applying an independence form of Borel–Cantelli to dependent cuts; confusing a retained ray with uniqueness; proving only an annealed or fixed-parameter threshold statement; silently assuming the UST is connected in high dimensions; insufficient symmetry or ergodicity of the input; and confusing HM's midpoint marginal, pre-flip site model and post-flip site model.

## Strongest verified result and remaining gap

For any countable connected bounded-degree simple graph carrying a one-ended spanning tree, the paper's conditional independent-edge kernel has ordinary finite energy after the tree is forgotten. Almost surely its output has a unique infinite component and both its internal bond and site thresholds equal one, as do those of the whole output graph. Its deterministic proof witness is an exhaustion by finite tree-past sets with eventually singleton output boundaries along each tree ray.

Combined with the precise Timár factor-of-iid input, this proves the stated fully automorphism-invariant, translation-mixing lattice law for every integer dimension at least two. The separate planar HM midpoint projection and post-flip site-threshold deductions are also supported by the written bounded-cutset arguments and the inspected primary construction.

**Exact remaining mathematical gap found: none.** The review does not establish first priority, exhaustive novelty, a uniform finite-energy constant, quantitative mixing, or a finite coding radius. The note expressly avoids those stronger claims.

## Complete proof audit

### 1. Finite pasts, bypass suppression and summability — page 2

Bounded degree makes the graph locally finite. In a one-ended locally finite spanning tree, removing an edge leaves exactly one finite component; otherwise the two infinite components would supply two ends. Along the unique ray from a vertex, these finite sides contain the starting vertex, increase strictly and exhaust the graph. Strict growth follows because the next ray vertex enters the next past. Exhaustion follows because every other vertex's ray eventually coalesces with the first ray.

The unique tree edge crossing the past \(S_n\) is \(t_n\). Every ambient nontree edge crossing that cut has a tree path containing \(t_n\). Therefore the **maximum** finite-past size along that path is at least \(|S_n|\); its insertion probability is at most \(2^{-|S_n|}\). There are at most \(\Delta|S_n|\) crossing edges. The deletion probability of \(t_n\) is exactly \(2^{-|S_n|}\). The union bound is valid even when events share many coordinates.

The sizes along a ray are distinct positive integers, so their bad-event probabilities are summable, bounded by \(\sum_{m\ge1}(1+\Delta m)2^{-m}=1+2\Delta\). The first Borel–Cantelli lemma does not require independence. Its conclusion really is that **both** defects stop: the tree edge is retained and every nontree bypass is absent eventually. Intersecting over the countable vertex set and then integrating over the random input is legitimate.

The bounded-degree and one-ended hypotheses do substantive work. The argument does not extend merely by treating an arbitrary spanning forest as a tree, or by replacing the maximum with an average or minimum. An explicit negative control below detects the minimum substitution.

### 2. Existence and uniqueness — pages 2–3

The eventual-cut statement retains complete infinite tree-ray tails. Thus percolation at retention one is established; it is not inferred only from high edge probabilities. Coalescence of the original tree rays makes all retained infinite tails connect. Any infinite connected component of the retained tree contains a ray by local finiteness, and that ray meets their common retained tail. Hence the retained tree has a unique infinite component.

An infinite output component beginning at any vertex must escape every finite past set. At a sufficiently late singleton cut it must cross the designated tree edge, whose two endpoints already lie on a completely retained tail. Therefore it intersects the retained tree's unique infinite component. This proves uniqueness even though added nontree edges may connect many finite tree fragments. It does not claim the entire output is connected, or that every vertex belongs to the infinite component.

### 3. Internal thinning, all parameters and measurability — page 3

Fix a good realized pair \((T,X)\). Any infinite path from a vertex must cross every sufficiently late singleton boundary. For independent bond retention \(p<1\), it must retain any selected \(k\) of these distinct edge coordinates, whose probability is \(p^k\). Letting \(k\) grow and taking a countable union over vertices excludes every infinite thinned component.

This is a deterministic structural implication that works for every real \(p<1\); it does not require an uncountable intersection of probability-one events over \(p\). The same late edges belong to the unique infinite component \(C\), so the identity for the boundary of \(S_n\cap C\) establishes its threshold as well. For site thinning, the forced ray edges force infinitely many distinct ray vertices to be retained, giving the same obstruction. Finite components of \(X\) cannot become infinite under either deletion operation. At \(p=1\), percolation already holds, making the thresholds exactly one.

Forgetting the hidden tree does not introduce a measurability gap. At rational retention parameters, infinite-connection probabilities are decreasing limits of finite-ball connection probabilities; the resulting graph property is Borel. Monotonicity then supplies all subunit real parameters. The stated graph-only finite-set certificate is another countable Borel description. A measurable choice of a witnessing tree from each output is unnecessary.

### 4. Ordinary finite energy and equivariance — page 3

All conditional output parameters lie strictly between zero and one. Realizing the kernel by independent uniforms makes the sigma-field of other output edges a sub-sigma-field of the input tree and all other uniforms. The tower identity in equation (5) follows, while the omitted edge's uniform remains independent. Thus the conditional probability of either state after observing all other output edges is the conditional expectation of a strictly positive random variable.

Such a conditional expectation cannot vanish on a positive-probability measurable set: integration over that set would contradict strict positivity. This proves both insertion and deletion tolerance almost surely after forgetting the tree. It does **not** provide a common positive lower bound, and none is asserted. On the countable product configuration space, regular conditional versions exist; assigning interior values on exceptional conditioning configurations is harmless.

The finite sides and finite connecting paths have countable measurable descriptions, as does the good one-ended spanning-tree domain. The probability-one extension by rate one-half outside that invariant domain is measurable. Tree paths and finite-side cardinalities are preserved by graph automorphisms, so the conditional kernel commutes with them.

### 5. Lattice input, all automorphisms and mixing — pages 3–4

Timár's exact cited v1 theorem supplies a one-ended **spanning tree**, not a forest, as a factor of iid on an ergodic amenable one-ended unimodular random graph. For the deterministic rooted lattice in dimension at least two, the rooted isomorphism class is deterministic, the mass-transport identity holds by translations, finite-box partitions verify amenability and the lattice has one end. All required hypotheses are satisfied.

The input tree factor and independent iid edge marks form an automorphism-invariant labeled construction. The output kernel is equivariant, so the full graph-automorphism symmetry follows, including reflections and coordinate permutations. The joint independent vertex/edge labeling is mixing under translations. Approximation of measurable events by finite-coordinate events proves mixing even when the factor depends on infinitely many labels; a finite coding radius is not required. The measurable equivariant output inherits mixing and hence translation ergodicity.

The note correctly restricts the older UST alternative to dimensions two through four. Pemantle's high-dimensional limit has multiple components, so paths between all endpoints would not be defined; the paper does not make that substitution.

### 6. Exact HM midpoint marginal — page 4

The primary HM construction fixes a phase, places primal vertices at even/even sites, dual vertices at odd/odd sites and represents bonds by the remaining midpoint sites. Before flipping, the two monochromatic graphs are subdivisions of the primal and complementary dual one-ended trees. At an edge midpoint with a finite coarse side of size \(s\), removing that midpoint cuts off \(s\) coarse vertices and \(s-1\) internal midpoints, giving \(b=2s-1\). HM's flip probability \(2^{-b-1}\) is therefore \(4^{-s}\), exactly as equation (6) states.

Taking just these midpoint coordinates preserves conditional independence. Declaring every coarse vertex present produces a bond law; it is **not** the graph induced by all finally open fine-lattice sites. The fixed phase does not create a parity obstruction for the resulting coarse bond law. Primal UST invariance and equivariance give its full coarse-lattice symmetry. Equation (5)'s conditional-expectation argument proves ordinary finite energy for this marginal.

### 7. Dual paths, Fatou and bounded cutsets — page 4

On a finite simple path in a one-ended tree, finite-past sizes occur at most twice: the path is two strictly increasing ancestor chains meeting at their common ancestor. A finite primal cut has even dual degree. For a finite past of the primal tree, exactly one cut edge is in the primal tree. All other dual cut edges lie in the complementary dual tree. Consequently the cut is exactly the single fundamental cycle formed by adding that one missing dual edge; no additional finite nonempty even component can lie in the dual tree.

Thus all nontree bypasses correspond to one finite dual-tree path. The expected number of retained crossing edges in the HM marginal is at most \(1+2\sum_{m\ge1}4^{-m}=5/3\). Conditional Fatou bounds the expectation of the nonnegative liminf, implying that the liminf is finite almost surely. It does **not** assert eventual uniformly bounded cuts, independence of the original cuts, or singleton cuts for this older rule.

The increasing finite pasts exhaust the lattice, so their boundaries escape every fixed finite edge set. On a good realization, the finite liminf supplies an infinite subsequence with a finite bound \(K\), from which pairwise edge-disjoint boundaries can be selected. An empty boundary already blocks escape from its interior. Otherwise independent thinning deletes each whole boundary with probability at least \((1-p)^K\), independently for the selected disjoint boundaries. The probability of crossing the first \(k\) is at most \([1-(1-p)^K]^k\), which tends to zero. Each fixed vertex is eventually inside all these past sets. This proves the claimed quenched threshold obstruction for the older midpoint marginal.

Percolation of that marginal at retention one follows independently from summable deletions along primal rays. The note only needs the historical bond existence conclusion here; it does not improperly reuse the new rule's eventual singleton-cut property.

### 8. HM post-flip site model — pages 4–5

Subdividing the same dual fundamental cycle in the fine square lattice gives a simple surrounding nearest-neighbor circuit. Exactly one midpoint on it is initially open; the remainder is a finite path in the initially closed subdivided dual tree. For site removal, the number \(b(x)\) of finite descendants strictly increases along an ancestor chain, so on a finite path each value occurs at most twice. The expected number of closed sites flipped open along that path is at most \(2\sum_{m\ge0}2^{-m-1}=2\). Including the exceptional midpoint gives a uniform bound of three on the expected open circuit sites.

Conditional Fatou and the escape of the circuits from every finite vertex set provide infinitely many vertex-disjoint surrounding circuits with a bounded number of finally open sites. Under independent site thinning, simultaneously deleting those finitely many open sites has a probability uniformly bounded away from zero. The disjoint-circuit independence gives the same obstruction. Planar separation forces every infinite nearest-neighbor open path from a fixed site to meet every sufficiently late circuit. This establishes the additional post-flip site-threshold deduction.

HM's Lemma 3.1 converts the internal site threshold-one statement to the internal bond threshold-one statement for the same bounded-degree graph. It does not convert an external site law into an external bond law satisfying finite energy; the note expressly avoids that false inference. The published HM text discusses threshold one for the pre-flip model and presents a different robust, uniform-energy construction later. Those models are not interchangeable, and the reviewed paper distinguishes them correctly.

## Primary sources and historical limits

Successful source PDFs, URLs, hashes and exact inspected passages are recorded in reference_sources.json; cached publications are ignored and not redistributed.

- [Timár, arXiv:1805.10690v1](https://arxiv.org/pdf/1805.10690v1): Theorem 1, Corollary 2 and the FIID definition match the required tree and symmetry input. The claim here uses this exact v1 theorem; no theorem about a mere forest is substituted.
- [Benjamini–Häggström–Schramm, arXiv:math/9906002v1](https://arxiv.org/pdf/math/9906002v1): Question 1.1 and its immediate definitions confirm the exact ordinary-energy, fully invariant bond question. Existence of an infinite component differs from the stronger everywhere-percolating hypothesis used elsewhere in that paper.
- [Benjamini–Tassion, arXiv:1505.06069v1](https://arxiv.org/pdf/1505.06069v1): Question 1 still poses the same question in the cited version. Its sprinkling theorem assumes a different starting condition and does not contradict this construction.
- [Häggström–Mester, published 2009 paper](https://www.maths.tcd.ie/EMIS/journals/EJP-ECP/article/download/1446/1446-4872-1-PB.pdf): Section 2 supplies the actual coordinates and flip rule; Lemma 3.1 supplies the internal bond/site equivalence for bounded-degree graphs. I independently reconstructed the additional bounded-cutset deductions rather than attributing them to a theorem already stated there.
- [Pemantle, arXiv:math/0404043v1](https://arxiv.org/pdf/math/0404043v1): Theorems 2.3, 4.2 and 4.3 support the stated connectedness and one-endedness ranges. The high-dimensional disconnected limit is explicitly excluded.

The exact archived lecture-note URL for the ancillary Open problem 8.15 locator was unavailable through the browser in this review; that pagination was not independently authenticated. This does not affect the mathematical theorem or the exact question independently confirmed in the BHS and BT primary versions. No exhaustive priority audit was attempted. The note's absence of a first-priority claim is appropriate.

## Independent finite controls and published replay

**fresh_controls.py**, with output fresh_controls.json and console log fresh_controls.log, uses only the standard Python library and exact rational arithmetic. It imports no publication checker. It enumerates all **8,476 rooted labeled trees on two through six vertices**, regarding each root as attached to an infinite ray. The finite edge pasts are therefore the exact pasts of a genuine one-ended extension.

The controls test strict ancestor growth; singleton tree cuts; every crossing chord's path and maximum; the exact union bound; HM midpoint counts and rates; edge- and vertex-past multiplicity on arbitrary paths; and the two expected-flip bounds. Further controls enumerate 192 hidden-tree posterior probabilities, check exact geometric-series tails, and enumerate all bond and site thinnings of three redundant diamond blocks connected by bridges. The resulting endpoint-connection probabilities at one-half retention are respectively \(343/16384\) and \(27/4096\), consistent with the required bridge/vertex obstructions.

The negative control replaces the path maximum by its minimum on a four-vertex path with past sizes \(3,2,1\). It gives a bypass probability of one-half across a size-three cut, violating the required one-eighth upper bound. This validates that the control actually distinguishes a tempting incorrect rule. In total the program passes 1,148,399 finite assertions; that number is a count of finite checks, not independent proofs of the infinite theorem.

**planar_controls.py**, with its own JSON and log, samples **120 finite square-grid spanning trees** using a recorded fixed seed. It checks **2,960** dual fundamental-cycle/cut identities and expected-bypass bounds. For **304** cycles avoiding the wired outer face, it explicitly constructs the subdivided fine-lattice circuit and checks simplicity, nearest-neighbor steps, exact enclosed coarse past, and exactly one initially open midpoint. These finite trees are not infinite UST samples; the tests validate finite geometric identities, not infinite-volume probability claims.

The **unmodified published integrity verifier passes in normal and optimized Python modes**, with the external package-index hash above and with its PDF identity independently checked. Outputs are archive_integrity_normal.json and archive_integrity_optimized.json; both stderr files are empty. The commands use Python with -I -S -B, adding -O for the second run, and invoke tmp/package/verify_package.py with the recorded index hash and --full.

The verifier authenticates 108 regular package files, 27 original source files, 15 nested archive members and 11 negative parser/path controls. It explicitly executes **no mathematical proof program**. A historical 21-control checker was not distributed and is not claimed reproduced. This replay establishes byte relationships and reproducibility of the available integrity checks, not Borel–Cantelli, FIID existence, the infinite threshold proof, or priority.

## Disposition

The mathematical gate passes for this version. No repair or deferred substantive defect arose from this review. The written infinite arguments supply the actual proof; the new finite controls and published integrity replay are corroboration.

Public descriptions should retain **ordinary finite energy**, **internal independent thinning**, **every dimension at least two**, and **unrefereed**. They should allow finite components, distinguish the main rule from the older HM deduction, and avoid first-priority, uniform-energy, finite-coding-radius or human-peer-review claims. This review is not itself authorization to publish.
