# Independent mathematical audit: internal critical probability one

Problem 10000036 / AMR-099-0036, rank 875. Audit date: 6 October 2026.

## Outcome

**Accepted for the exact theorem in the frozen PROOF.md.** No mathematical defect or necessary correction was found. For every integer d >= 2, the manuscript constructs an automorphism-invariant, translation-mixing bond law on the nearest-neighbor lattice Z^d with ordinary finite energy, exactly one infinite component C almost surely, and quenched internal Bernoulli bond thresholds p_c(X) = p_c(C) = 1. The additional assertion about the internal site threshold also passes.

This is an acceptance of the mathematical argument using its cited established spanning-tree input. It is not a claim of novelty, priority, journal acceptance, or verification of every statement in the cited papers. It does not resolve a stronger uniform finite-energy problem. The full-dimensional claim is supported by Timar's one-ended spanning-tree theorem, not by substituting a disconnected uniform spanning forest into the construction.

## 1. Frozen object and identity checks

The externally supplied archive and manifest were checked before reading archive members. All byte counts and SHA-256 digests matched; the archive had exactly the six expected ordinary text members and no executable or copied source document.

| Object | Bytes | SHA-256 |
|---|---:|---|
| Author archive | 13,793 | 266debc377c66c6813e9db2b6abc704454ead9cdec47024f5d15338329b2fe05 |
| External manifest | 1,268 | 80ae7742dec006af9feb3de07722ce520ecb2a1393809ff86e19d798b85b56c2 |
| PROOF.md | 16,299 | c31b7a1cd6a3af04807b20d58f23d79f9d07cf4eb87df26187498f3260f9891d |
| APPROACHES.md | 3,435 | 3fc8a1e278c0971f609e75b949e5cfc18e0291a6e4020d84cadc033ebcabe232 |
| AUDIT_GUIDE.md | 2,770 | de81702da9f776c83b4a7d50001e574b275a255e73e7f6b01af753506731faaa |
| SOURCES.json | 4,902 | 0a21a34203d8a75e7703b6af9a1d5d20f7fb598adcaefdbcb3920f480bdc8733 |
| STATUS.md | 2,477 | f2e702022e56e609fcbce4fd960ca8c28baf87a268c3d84dede509b50c065ad4 |
| MANIFEST.json | 1,031 | 48c6bb8b5d12915f266966e414b2fa8c0248d4f1ad7f25db5b4964855b255de5 |

All six members were read in full. The original archive and members were left unchanged. Hashing verifies identity only; it is not mathematical certification. No mathematical executable, simulation, finite-size inference, or proof-assistant certificate is asserted.

All six cached public-source PDFs listed in the author's SOURCES.json were located and independently matched to its byte counts and SHA-256 digests. The older Haggstrom-Mester arXiv copy was available in a separate cache. Each had a PDF header. This verifies the metadata against the available bytes; it does not assert a new download of those documents. SOURCE_VERIFICATION.json records only the public metadata and inspection results. No source bytes or extracted source text are included in the audit deliverables.

The complete problem descriptor and complete paired status report were separately checked against their supplied full-corpus pins before inspection. The relevant statement digest is 30364c04ff997a39f54d48433189503018af46561dbaf907c3029002745aff4c (196 UTF-8 bytes). The complete descriptor/report pair, serialized as a two-element array with sorted keys and standard Python JSON defaults, has digest 0f157faedf19230d980dca9da4b20d61008e0e2536d8c4eb785f4027df3d1778 (3,430 bytes). No descriptor or dataset contents are reproduced here.

## 2. Source scope and the spanning-tree input

The scope was checked against the complete descriptor, the Saint-Flour problem listing, and the surrounding definitions of Benjamini and Tassion's Question 1. The latter explicitly uses positivity of both single-edge conditional probabilities given all the other edges. Thus the manuscript's ordinary finite-energy condition matches the target; a uniform lower bound is not an omitted hypothesis. The graph model is a bond subgraph. [Benjamini and Tassion, Section 1.2](https://arxiv.org/pdf/1505.06069)

The Saint-Flour source identifies the item as Open Problem 8.15 on page 61. Its question does not add an explicit universal dimension quantifier in that sentence. The complete descriptor and paired report likewise add no hidden uniform-energy or site-model condition. The candidate nevertheless proves every d >= 2, removing that possible scope ambiguity. The direct author-hosted PDF opening failed during this audit; the indexed primary-source passage and a fresh rendering of page 61 from the hash-matched archived PDF were inspected instead. [Benjamini, Coarse Geometry and Randomness](https://www.wisdom.weizmann.ac.il/~itai/stflouraug24.pdf#page=61)

Timar's Theorem 1 in the cited arXiv version provides a one-ended factor-of-iid spanning tree for an ergodic amenable unimodular random graph having one end. Corollary 2 and the adjoining factor definition were independently inspected, both through the public PDF text and fresh renderings of pages 1-2 from the hash-matched PDF. This is a connected spanning tree, and the factor is measurable and isomorphism-equivariant. [Timar, Theorem 1 and Corollary 2](https://arxiv.org/pdf/1805.10690)

The application to the deterministic rooted nearest-neighbor Z^d is valid: it is a unimodular Cayley graph, is amenable by the box boundary/volume estimate, and has one end for d >= 2. Its deterministic rooted isomorphism class is ergodic. Isomorphism-equivariance gives the needed invariance under the entire lattice automorphism group. No choice of an axis or origin is retained in the construction.

The lower-dimensional alternative is valid as well. Pemantle's exhaustion limit and one-end theorem give a one-ended uniform spanning tree in dimensions 2, 3, and 4. Its symmetry follows from exhaustion-independence and the symmetry of finite uniform spanning-tree laws. The manuscript correctly refuses to use the higher-dimensional disconnected forest as the same input. [Pemantle, Theorems 2.3 and 4.3](https://arxiv.org/pdf/math/0404043)

## 3. Adversarial checks of the construction

### 3.1 Finite sides, paths, and measurability: pass

In a locally finite one-ended spanning tree, removing an edge leaves exactly one finite component. Two infinite components would supply two disjoint rays and hence two ends; two finite components would make the whole tree finite. The finite-side size s(t) is therefore a positive integer for every tree edge.

A fixed pair of vertices has a unique finite tree path. Consequently the maximum M(e) over the finitely many s(t) values on that path is finite and positive for each non-tree edge. There is no undefined maximum over an infinite path.

For any fixed finite set S, the assertion that S is a component after removing a given edge is measurable using its internal connectivity and its finite edge boundary. Taking a countable union over finite sets gives the size function. Finite paths can similarly be enumerated. The null-set extension of the kernel is valid and invariant because being a one-ended spanning tree is invariant.

### 3.2 Rates and hidden-tree conditioning: pass

All conditional-on-tree edge probabilities are strictly between zero and one. After fixing T, the output edge X_e uses only its own independent mark U_e. Other output coordinates, even taken all together, are measurable from T and the other marks. Thus conditioning on T and every other output coordinate does not expose U_e.

The tower identity in Section 7 is therefore correct. The conditional expectation of an almost-surely positive integrable random variable is almost surely positive. Applying this separately to r_T(e) and 1-r_T(e) proves both insertion and deletion tolerance for the marginal law of X. Countably many edges allow a common exceptional null set.

This argument also proves positivity of every prescribed pattern on any fixed finite edge set, conditional on its complement: given T the corresponding finite product is strictly positive, and then the same conditional-expectation argument applies. There is no loss of ordinary finite energy when the auxiliary tree is forgotten.

The manuscript appropriately does not claim either a uniform marginal bound or failure of such a bound merely from the conditional-on-tree rates.

### 3.3 Every bypass is controlled: pass

For the finite side S_T(t), the only crossing tree edge is t. If a non-tree edge e has endpoints on opposite sides, its unique tree path must include t. Thus M(e) >= s(t), and its insertion probability is at most 2^(-s(t)). This statement concerns every possible lattice edge crossing the cut, not just edges near a chosen ray or edges exposed at an earlier stage.

The number of possible crossing edges is at most Delta s(t). On Z^d, Delta = 2d. The finite side need not remain connected after perturbation; the boundary estimate and the separating role of the entire vertex set remain valid.

### 3.4 Summability and simultaneous quantifiers: pass

Along the unique ray from a vertex v, the finite sides are strictly nested. The next ray vertex belongs to the next finite side but not the preceding one. Hence their sizes are distinct positive integers, which is stronger than merely tending to infinity.

The total expected number of exceptional cuts, conditional on any admissible T, is bounded by

sum over m >= 1 of (1 + Delta m) 2^(-m) = 1 + 2 Delta.

The first Borel-Cantelli lemma therefore applies without any independence between exceptional-cut events. Its conclusion is that all sufficiently late cuts along this ray simultaneously have their tree edge retained and every possible non-tree bypass absent.

There are countably many starting vertices. Taking that countable intersection, then integrating over T, gives one full-probability joint event valid for every vertex. No intersection over uncountably many trees or retention parameters is being smuggled into the proof.

### 3.5 The final cutsets are genuine: pass

At each sufficiently late cut, the retained crossing tree edge exists in X and no other crossing edge exists in X. Thus the boundary is exactly the singleton claimed in Section 4. Deletions elsewhere cannot create a crossing. This excludes the common error of establishing a cutset only in the original tree rather than in the final percolation graph.

### 3.6 Percolation and uniqueness: pass

The eventual retained tail of any one tree ray is infinite, so X percolates. Any two rays in a one-ended tree coalesce. Their eventual retained tails thus belong to the same retained-tree component. Conversely every infinite retained-tree component contains a ray, so this component is unique.

For any v in an infinite X-component, an infinite simple path from v must exit each of the finite sides containing v. At a sufficiently late cut it can exit only across the retained ray edge, whose endpoints lie in the retained-tree infinite component. Hence every infinite X-component meets that one component. This proves uniqueness directly for the final graph, including possible paths created solely by many inserted edges.

### 3.7 Quenched thresholds, all components, and all parameters: pass

Fix a good pair (T,X). For any vertex v, independent bond thinning with retention p < 1 can leave v in an infinite component only if it keeps every edge in the fixed infinite list of distinct singleton boundaries. The probability of keeping its first k entries is p^k, which tends to zero. A countable union over vertices excludes every infinite thinned component.

The reasoning is deterministic in the good witnessed graph and applies to each p < 1. It does not infer an uncountable family of quenched conclusions from separate annealed probability-one events. Equivalently, one could first use rational p and monotonicity, but that repair is unnecessary here.

At p = 1, X percolates. Restricting the same cuts to its unique infinite component gives the same conclusion for that component. Thus both critical probabilities equal one under the definition in the manuscript. The additional internal site-thinning statement is also valid because an infinite path must retain the infinitely many distinct ray vertices; the same finite-product bound applies. The external process remains a bond law.

### 3.8 Full automorphism invariance and mixing: pass

Finite-component sizes and finite paths commute with graph automorphisms. The perturbation therefore preserves every symmetry of the input law. Independent identically distributed edge marks also have the full symmetry, including reflections and coordinate permutations.

For the all-dimensional input, T is a measurable equivariant factor of independent vertex labels. Together with the independent edge marks these form a translation-mixing product field: finite cylinder events become independent under sufficiently large translations, and arbitrary events are approximated in measure by cylinders. Equivariant factors inherit this property. The manuscript consequently proves mixing of X, rather than incorrectly inferring it from an arbitrary invariant mixture of tree laws.

## 4. Prior work, source limitations, and scope discipline

Haggstrom and Mester's Section 2 was independently inspected. It already uses a one-ended uniform spanning tree and geometry-dependent summable flips to preserve infinite clusters while obtaining ordinary finite energy. Their later discussion separates that mechanism from robustness under fixed-density thinning. This is a close antecedent and is correctly credited. The inspected proposition does not itself state the max-path suppression rule or certify the critical threshold of the perturbed process used here. [Haggstrom and Mester, Sections 2-3](https://www.maths.tcd.ie/EMIS/journals/EJP-ECP/article/download/1446/1446-4872-1-PB.pdf)

The manuscript's insertion probabilities depend on T and vanish along relevant large cuts; its tree edges can also be removed. It is not the fixed-density independent sprinkling over an everywhere-percolating subgraph covered by Benjamini and Tassion's theorem. Therefore that theorem does not contradict the proposed example. [Benjamini and Tassion, Theorem 1](https://arxiv.org/pdf/1505.06069)

Independent bounded searches covered the exact finite-energy question, internal critical probability one, one-ended spanning-tree perturbations, and references to the Benjamini-Tassion question. No exact earlier resolution was located. That is a bounded search outcome only. It cannot establish that the result is novel, and it does not update the publication status of the old open-problem source by itself.

The three documented approaches were read. The fixed-density obstruction and the non-invariant axis example are correctly delimited, and the third approach supplies the complete candidate. No fourth approach or additional construction was needed for this audit.

## 5. Final disposition

Accept the frozen proof for its stated ordinary finite-energy bond theorem, for every d >= 2, including translation mixing, uniqueness, and quenched threshold one for both the graph and its infinite component. Accept the internal site-threshold remark as well. No correction patch or derivative proof is required. Preserve the frozen original and attach this audit and the separate acceptance report without replacing the author's historical pending-review status inside that original.

Mathematical acceptance does not imply uniform finite energy, priority, peer review, or permission for any unrelated external action.
