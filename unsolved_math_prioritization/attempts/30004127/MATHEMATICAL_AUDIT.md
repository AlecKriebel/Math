# Independent audit of the vertex distribution testing separation

## Verdict

ACCEPT AS COMPLETE for the quantified negative answer to problem 30004127 / OWR-16931-012 established in Theorem 1 of the pinned manuscript. I found no mathematical gap after an independent adversarial review of the full argument, its access-model quantifiers, its source alignment, and its final wheel-blowup addition.

This verdict means that the submitted argument establishes the stated separation under the original vertex-distribution-free graph-testing model. It is an independent mathematical audit, not a claim of peer-reviewed acceptance, priority, or exhaustive literature novelty. Finite checks below are supplementary controls; they are not the basis for the infinite-family theorem.

Distributed manuscript: [PROOF.md](PROOF.md), 25,005 bytes, SHA-256 `1483bcaa29473616799fa9c04937e55fc249bd27e293c45d580af236d38709f3`. The complete accepted mathematical content is preserved; edition changes reconcile status and publication references only. The original audit evaluated the frozen manuscript independently rather than importing author test results as mathematical validation. [ACCEPTANCE.json](ACCEPTANCE.json) binds the exact distributed proof and audit bytes.

The audited result concerns the single fixed property P consisting of K4-free graphs that become 3-colorable after deletion of at most one vertex. It proves a polynomial standard-model canonical sample upper bound and a superpolynomial unrestricted VDF total-oracle lower bound, with a separate superpolynomial sample lower bound when adjacency queries use sampled labels. This is sufficient to refute every universal polynomial comparison of the relevant complexities.

## Original problem and model alignment

I independently retrieved the complete primary PDFs, compared their bytes with the available primary copies, inspected extracted text, and visually inspected the relevant rendered source pages. The historical retrieval metadata, public URLs, hashes, sizes, and inspection details are preserved in [SOURCE_METADATA.json](SOURCE_METADATA.json). No source document or source-text extract is included in this audit package.

The original question is Problem 5 in Lior Gishboliner's contribution, joint work with Asaf Shapira, to Oberwolfach Report 19/2019, publisher PDF page 27, printed page 1139. The precise later version is Problem 5.6 in Gishboliner and Shapira, *Testing Graphs against an Unknown Distribution*, arXiv:1905.09903v5, PDF page 22. Both ask for comparison with the standard model for properties satisfying both heredity and extendability. The candidate preserves both hypotheses and provides a fixed property, rather than a parameter-dependent collection of properties. [Original report](https://ems.press/content/serial-article-files/46798), [later primary manuscript](https://arxiv.org/abs/1905.09903v5).

On page 2 of v5, weighted distance sums D(x)D(y) once per unordered changed pair. The standard distance is changed-edge count divided by n squared. The graph size is not supplied, the vertex distribution is unknown, and success probability is at least two thirds. The opening model definition counts the total number of sampling and edge-query calls. Proposition 5.7 subsequently states a canonical sampled-vertex bound, whose full induced-graph inspection can have quadratic adjacency cost. The candidate explicitly tracks these different meanings and proves enough for both relevant comparisons.

The candidate does not establish a sample-only lower bound for a tester permitted arbitrarily many free queries to arbitrary known vertex names. That would be false in its strengthened known-name model, where the entire graph could be queried without sampling. Its theorem instead states the valid total-cost lower bound, plus the sampled-label version. This distinction is substantive and is handled correctly.

Footnotes 23 and 24 of v5, visually checked on PDF pages 20 and 23, require a proximity relaxation such as epsilon to epsilon/2 when arbitrary irrational weights are included in the blowup transfer. The candidate uses positive rational weights and does not invoke that transfer. Its polynomial upper bound is uniform over small epsilon, so fixed constant rescaling cannot rescue a polynomial comparison. Goldreich's manuscript uses an ordered-pair adjacency-predicate normalization, which is a factor of two different; no numerical constant in the proof is imported from that source.

## Independent mathematical verification

### The property and its computational meaning

Every 3-colorable graph belongs to P. An induced subgraph of a graph that is 3-colorable after deleting one vertex retains that feature: delete the same vertex when present and delete none otherwise. K4-freeness is hereditary. Adding an isolated vertex and deleting edges preserve both conditions. Thus P is hereditary, extendable in the primary source's exact sense, and edge-monotone.

Membership is decidable by testing K4-freeness and enumerating the possible exceptional vertex and colorings. The tester claims oracle complexity rather than polynomial running time, so exponential finite membership computation is allowed. Probability distributions on vertices require a nonempty vertex set; the empty graph belongs to P and creates no contrary input instance.

### The all-size colorability sampling lemma

I checked the proposed list-coloring argument directly, without using the Alon–Krivelevich theorem as a black box. For every proper partial coloring on S, let U be the uncolored vertices with no permissible color. For each remaining vertex v choose a color minimizing the number delta(v) of potential same-color neighbors among remaining nonempty lists. This produces a full coloring after assigning U arbitrarily. Its monochromatic edges number at most n|U| plus the sum of delta(v). This is an upper bound even though some edges are counted twice. Deleting those edges gives a legal 3-coloring, hence epsilon-farness implies the displayed repair inequality.

If W is the set with delta(v) at least epsilon n/2, the inequality forces |U union W| at least epsilon n/2. Coloring any v in W with any allowed color removes that color from at least delta(v) other nonempty lists. The sum of all list sizes therefore decreases by at least epsilon n/2. This potential begins at 3n, so a feasible path cannot have more than 6/epsilon such steps.

The possible dependency between different coloring-tree nodes is harmless. For each fixed ternary-tree address of depth j, its partial coloring depends only on the previous j sample blocks. The next block is independent. The conditional miss probability is at most exp(-epsilon l/2). Summing these conditional probabilities over fewer than 3^h addresses yields the claimed 1/12 failure bound. No independence between nodes is assumed. If the whole sampled induced graph were 3-colorable, its coloring would select a feasible child at every visited node; every chosen vertex lies outside that branch's S. Repeated sample labels therefore do not break this implication.

The choices h=floor(6/epsilon)+1, l=ceil((2/epsilon)log(12 times 3^h)), and r=hl make the potential and union-bound inequalities strict enough. They imply r=O(epsilon^-3). There is no lower bound on n anywhere in this proof. This closes the small-input qualification that would arise from simply quoting an asymptotic sampling theorem.

### The polynomial classical tester

An epsilon-far graph for P is epsilon-far for 3-colorability, since 3-colorable graphs form a subset of P. For n at least N=12r squared, two independent r-sample blocks are separately non-3-colorable except with probability at most 1/12 each. Their underlying vertex sets intersect with probability at most r squared divided by n, also at most 1/12. On the complementary event, deleting any one vertex leaves one of two disjoint non-3-colorable witnesses intact. The sampled graph is therefore outside the one-exceptional-vertex property, hence outside P.

For n below N, M=ceil(N log(3N)) uniform samples collect every vertex with probability at least two thirds. The inequality n exp(-M/n) at most N exp(-M/N) is valid because the function t exp(-M/t) increases for positive t. Complete collection exposes the input graph itself, which is outside P. The same fixed M is used regardless of the unknown n, and M is at least 2r. Heredity gives perfect completeness.

Thus the announced vertex-sample cost O(epsilon^-6 log(1/epsilon)) and quadratic adjacency cost follow. Using proximity 1/8 for larger requested epsilon is valid. No hard-instance distribution is being substituted for the uniform sampling distribution in this upper bound.

### Exact weighted distance and arbitrary repairs

The apex has mass one half and each tail vertex mass 1/(2n). A tail-edge edit costs 1/(4n squared); an apex-edge deletion costs 1/(4n).

For a 3-colorable tail H, deleting a smallest triangle edge-hitting set gives a triangle-free, still 3-colorable tail. Its universal-apex join is K4-free, and deleting the apex leaves a 3-colorable graph. This proves the upper bound of one quarter of the tail's ordinary triangle-freeness distance.

For the converse, take any repaired graph F in P, allowing edge additions. Let S be the tail vertices whose apex edge was removed. The remaining apex-neighbor set must induce a triangle-free graph in F, because any triangle there would produce a K4 with the apex. Use this part of F as a repaired tail and isolate S. Edits off S are bounded by F's tail-edit count, while deletion of original edges incident to S costs at most n|S|. On dividing by n squared, this is at most four times F's total weighted cost. This establishes the reverse inequality without assuming that an optimal repair is deletion-only.

For the later edge-disjoint-triangle tails, the ordinary triangle distance is exactly the number of retained full triangles divided by n squared: every original triangle needs an original edge removed, distinct triangles have disjoint edges, and one removal per triangle suffices. Edge additions cannot avoid that necessity.

### Explicit arithmetic host

With B=2^d, there are B^d digit vectors and at most d(B-1)^2+1 possible squared norms. A largest equal-norm class has at least B^d/(dB squared) vectors, enough for the stated K. Base 2B encoding with a constant shift gives distinct integers in the required range. In a progression equation the shifts cancel and every digit on either side is below the base, so there is no carry. Equal norms and the midpoint equation force equal vectors by the squared-distance identity. The argument covers all chosen K encodings.

For the host triangles indexed by (x,a), each edge determines its index uniquely, including the YZ edge where a=z-y and x=2y-z. Any host triangle has three part differences a,b,2c with a,b,c in A, so a+b=2c and hence all three differences agree. There are consequently exactly T=mK triangles, all edge-disjoint, on n=6m vertices. No unlisted triangle can survive in a sampled subgraph. Both the sphere method and the arithmetic host are fully proved, so failure to retrieve an original historical article does not leave a theorem dependency.

### Parity distributions and farness

The even- and odd-parity distributions on three edge bits have identical distributions on every proper coordinate subset. The choices on designated triangles are independent, and triangle edge sets do not overlap. GOOD never retains a full designated triangle and is therefore always a yes instance. BAD retains each full triangle independently with probability one quarter. No extra triangles arise because the host has none.

The exponential-moment argument yields Pr[Z<T/8] at most exp(-T/32). The manuscript's elementary bound log 2 at most 3/4 is adequate. Combining with the distance identity makes all BAD instances with Z at least T/8 epsilon_d-far for epsilon_d=T/(32n squared). Crucially, the proof does not condition the hard distribution on farness before applying indistinguishability; it uses the unconditional BAD distribution and then loses only the explicit exceptional probability. This avoids a conditioning error.

### Adaptive named-query exposure

This is the most important adversarial check. A sample call and an edge-query endpoint can expose a new tail label. Giving the entire induced graph on all exposed labels only strengthens the algorithm. Queries involving the apex and knowledge of n and D cannot reveal the parity choice: these data are identical in both worlds.

Condition on the exact host images already assigned to exposed names as well as the transcript. All observations concern only those assigned names. The unused-name portion of the secret random bijection remains uniform and independent of all pattern restrictions already observed. Therefore an adaptively selected unused name has a uniform unused host image. Its name may be a complicated function of the transcript; the conditional exchangeability statement still applies. Tail sampling chooses a uniformly random name independently of the graph, and repetitions reveal no new host image. Two new query endpoints can be exposed sequentially, which only helps the strengthened algorithm.

Couple common algorithm coins, sampled names, and fresh host images. Until an entire designated triangle is exposed, every inspected portion of each triangle's pattern has at most two coordinates, so its conditional law can be coupled identically. Independence across designated triangles handles simultaneous observations. When one exposure completes a triangle, stop before returning the potentially different full-pattern information. Before this stopping event the algorithm's choices coincide in both worlds.

A variable-length fresh-image sequence can be padded to the deterministic exposure budget by the same uniform-without-replacement rule. The unconditional padded prefix is uniform: conditional uniformity of the next image given every earlier image and transcript proves this inductively. Conditioning on prior nonfailure would not by itself give an unconditional uniform set, but the manuscript does not make that invalid inference. The full sequential experiment, or a single-world continuation after the stopping time, supplies the required prefix distribution.

A fixed designated triangle is contained in this k-prefix with probability (k)_3/(n)_3. The union bound over T triangles therefore bounds coupling failure and total variation. For k at least n the trivial bound is sufficient; the coarse 2Tk cubed/n cubed bound is consistent in that case. The denominator estimate for n at least 6 is valid, and actual hosts have much larger n.

The two-thirds success guarantee applies separately to every fixed labeled weighted input, so averaging over the two hard distributions and private randomness is legitimate. GOOD rejection is at most one third, whereas unconditional BAD rejection is at least two thirds times (1-p). This gives a rejection-probability gap of at least one sixth for the stated parameters. No deterministic-tester restriction or unproved one-sided canonicalization theorem is used.

### Quantitative comparison and quantifiers

Each execution with at most s sample calls and e edge calls exposes at most s+2e names. Therefore the gap forces s+2e at least (n cubed/(12T))^(1/3). If the split varies by execution but total calls are always at most Q, use a deterministic exposure budget 2Q directly. This gives Q at least (n cubed/(96T))^(1/3), which is at least m^(1/3) since K at most m. In the sampled-label-only model the same reasoning uses k=s, independent of the number of free pair queries.

The floor in K causes no difficulty: for d at least 4 the unfloored quantity exceeds one, so it loses at most a factor of two. The two displayed epsilon_d bounds imply log(1/epsilon_d)=Theta(d), while log(m^(1/3))=(log 2)d(d+1)/3. The lower bound is thus exp(c log squared(1/epsilon_d)) for one absolute positive c and sufficiently large d. A subsequence of this growth suffices to refute any fixed polynomial bound valid for all small epsilon. The standard upper bound remains polynomial after any fixed constant proximity rescaling.

The property is fixed, the input graph and rational weights vary, the lower bound is worst-case oracle cost, and the upper bound handles every eligible finite size. No runtime bound, arbitrary-free-query sample lower bound, or universal single-forbidden-graph claim is silently substituted.

### Direct non-blowup-avoidability witness

I independently checked the final Section 8 addition against the definition on page 22 of v5, including the page 20 convention that edges inside blowup classes may be arbitrary.

Let W be the universal-apex join of a 5-cycle. W is K4-free, becomes 3-colorable after deleting its center, and is itself 4-chromatic, since the odd cycle needs three colors and the center needs another. Every vertex of W lies in a triangle. Blow every vertex into a class of size two. If one class has its internal edge, take its two vertices and one representative from each of two adjacent neighbor classes; these four vertices induce a K4. If no class has an internal edge, deleting any one vertex leaves each class nonempty. A transversal then induces W, so the remaining graph is still not 3-colorable. Every allowed blowup is outside P.

If P were blowup-avoidable, its definition would furnish a blowup of W without any minimal forbidden induced graph using two vertices of a class. Any forbidden induced graph in that blowup would therefore be transversal, and would project to a forbidden induced subgraph of W, impossible because W belongs to the hereditary property P. Thus this direct witness really refutes blowup-avoidability. It does not rely circularly on the separation or Proposition 5.7. The source's partial positive result is therefore inapplicable for an independently established reason.

## Independent finite controls

The historical finite checker was authored independently for this audit, without importing candidate code or earlier checker logic. Its substantive checks used explicit exceptions rather than optimization-removable assertions. Normal and optimized outputs agreed byte for byte. Programs and raw outputs are excluded from this proof-only edition; these historical checks supplement the complete analytic proof and are not required to establish its theorem.

- Structural checks covered 1,032 member graphs of order at most five, 4,809 single-edge deletions, 5,071 single-vertex deletions, isolated extensions, and all 64 internal-edge choices of the doubled wheel.
- Weighted-distance checks covered all 74 3-colorable labeled tails of orders one through four. They compared 60,876 possible same-vertex-set repairs, including additions, and found the exact identity in all cases; 23 tails had positive triangle distance.
- List-coloring controls checked 9,283 proper partial colorings on all four-vertex graphs and 24,876 feasible potential transitions. The repair bound, heavy-set implication, and potential decrease all passed.
- Arithmetic controls exhaustively constructed two reduced-parameter hosts with 72 and 1,296 triangles, checked edge uniqueness and absence of extra triangles, enumerated all 65,536 vectors for the actual d=4 sphere parameters and checked a 64-element AP-free encoding, and checked exact integer/rational parameter inequalities for d=4 through 100.
- Parity controls compared all seven proper coordinate subsets. Exact transcript enumeration used two edge-disjoint triangles sharing a vertex, all 120 secret permutations, and all 16 patterns per world. It tested adaptive name choices with and without early stopping at exposure budgets two through five. Every total-variation value obeyed the claimed union bound. For three exposures without early stopping the bound was attained: both were 1/5.
- Mathematical negative controls detected all intended failures: replacing disjoint coloring witnesses with one overlapping witness, lowering the apex mass while retaining the same distance identity, omitting K4-freeness, permitting a three-term progression in the host set, and corrupting the parity marginal distribution.

These checks are useful at catching indexing, normalization, and access-model mistakes. Their finite scope does not prove concentration, asymptotics, or the all-instance adaptive coupling; those were verified analytically above.

## Literature and source limitations

The independently inspected primary v5 still poses Problem 5.6 and proves only the stated restricted positive comparison in Proposition 5.7. The Alon–Krivelevich manuscript explicitly treats its main bounds asymptotically in n; the candidate correctly supplies a separate all-size proof. Goldreich's sampled-label reduction and one-sided conversion are contextual and are not hidden dependencies.

A bounded current search for the exact model combined with separation, superpolynomial, colorability, and Problem 5.6 did not identify a later resolution. I also inspected the introduction and related-work distinction of Yumou Fei's 2026 manuscript *Testing Properties of Edge Distributions*, arXiv:2603.22702v2: it studies a different edge-distribution model and does not supply the claimed VDF-versus-standard separation in the inspected material. This is a scope check, not an exhaustive review of that paper or proof that no prior result exists. [2026 contextual manuscript](https://arxiv.org/abs/2603.22702v2).

No new mathematical theorem is accepted merely because a scholarly source or an author checker says so. The separation's proof obligations are all discharged within the audited manuscript. Historical construction credits and contextual papers are appropriately distinguished from indispensable imported results.

## Release boundary

The audit endorses the exact stated theorem and complete manuscript. This proof-only edition contains the full authored proof, full substantive audit, acceptance, status, source review and public verification metadata. Programs, raw outputs, generated certificates, datasets, copied third-party source documents/text/images and private coordination material are excluded. No theorem claim requires omitted code or data. Edition preparation rechecked frozen input bytes and publication integrity without rerunning historical mathematical computations or performing new source retrieval, source-text inspection or literature search. Any later mathematical change requires a fresh audit and new pins. This AI-assisted manuscript and audit are unrefereed; acceptance is not external human peer review, journal acceptance, proof-assistant certification or a novelty claim.
