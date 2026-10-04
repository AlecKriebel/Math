# Independent adversarial audit: low-exponent supersolvability

Target: **30004609 / OWR-4990374-015**, queue rank 644.  
Audit date: **2026-10-04 UTC**.  
Verdict: **PASS within the stated characteristic-zero scope**.

The frozen candidate supplies a complete proof of the source conjecture, including arbitrary rank, products, and essentialization. I found no mathematical error or missing substantive argument. This is an independent mathematical audit judgment, not a formal proof-assistant certificate, journal acceptance, or certification of novelty. The result should retain the distinction between a reviewed candidate and an established published theorem.

## 1. Exact inputs and scope

The reviewed proof has SHA-256 `73716fdb49896b2443ada06ed707dba1e0d08f304d9e563cf251c949d8752798` and 13,674 bytes. All eight author files were read and matched against the frozen author manifest. The 19,956-byte author ZIP has SHA-256 `96abc4bb5ffa7810753f88875f5e414c07a844e40f301b28fe627cd568b43746`; its exact member set and every member's bytes agree with that manifest. The manifest itself has SHA-256 `009ab1bc105e881dbebb014056e2f8621ffb4f991847fcd1ea283f8daf07c32f`.

The source statement was checked directly against Tohaneanu's contribution in [Oberwolfach Report 5/2021](https://ems.press/content/serial-article-files/46883), printed pp. 283–286. Page 283 fixes characteristic zero; p. 284 states the target. I text-inspected the relevant passage and independently rendered and visually inspected printed p. 284. The selected numeric catalogue record was also read privately and matches that target. Direct catalogue retrieval was unavailable; no successful live catalogue read is claimed.

The candidate's nonzero-exponent formulation legitimately includes nonessential arrangements. It concerns finite sets of distinct central hyperplanes, not multiarrangements. No all-characteristics claim is audited or inferred. The empty rank-zero case is vacuous, and rank-one factors are immediate.

## 2. Established inputs and the historical correction

The proof uses Terao factorization, freeness implying formality, and standard product/essentialization facts. These are correctly stated and applied. The source report itself records the relevant factorization and product facts. The precise meaning of formality and its implication from freeness are independently confirmed in Möller–Mücksch–Röhrle, [On Formality and Combinatorial Formality for hyperplane arrangements](https://arxiv.org/pdf/2202.09104v2), pp. 1–3, which explicitly attributes freeness-to-formality to Yuzvinsky, Corollary 2.5. Direct retrieval of the original AMS article failed, so I do not claim to have inspected its original proof.

I independently checked the [v4 withdrawal record](https://arxiv.org/abs/1707.07091v4). The January 2022 notice questions completeness of two hand enumerations and rejects an inference in Proposition 4.8(a). The frozen candidate does not use these affected results. Its proof neither assumes inductive freeness nor assumes that arbitrary deletions preserve freeness. The supplied withdrawal example has been checked as free and supersolvable; its deletion really has two factors of sizes four and three, explaining the historical failed inference without refuting the conjecture.

## 3. Adversarial proof review

### 3.1 Reduction to one exponent 1

Choose independent defining forms as coordinates. A degree-one logarithmic derivation must send each coordinate to a scalar multiple of itself. Every other defining form is an eigenvector of this diagonal map. If the map is nonscalar, its different eigenspaces partition all defining forms into complementary normal subspaces. This is a genuine product decomposition over the original field, with no algebraic-closure assumption needed. Conversely, each product factor supplies an independent Euler derivation. Essentiality excludes degree zero. The asserted irreducible exponent lists and the values `n=2r-1` or `n=2r` therefore follow.

### 3.2 Connectedness is justified by formality

Let the incidence graph have components with element sets `E_i`. Every local relation is confined to one such component. As local relations span the full relation space, projection of any relation onto `K^{E_i}` is again a relation. Suppose vectors in the component normal spans sum to zero; express them using their respective defining forms. Projecting the resulting relation shows each component vector is zero. The normal spans therefore form a direct sum. More than one component contradicts irreducibility. Isolated elements are covered by the same argument. This is not an unsupported inference from geometric connectedness.

### 3.3 Rank-two multiplicity bound

After choosing two independent normal forms as `x,y`, every further member of that rank-two flat can be scaled to `x+c_i y`, with distinct nonzero `c_i`. For a homogeneous logarithmic derivation of degree `delta`, write its first two coefficients as `xP,yQ`. Tangency makes each `x+c_i y` divide `P-Q`: this follows by reduction modulo that linear factor and its coprimeness with `x`. If `m-2>delta-1`, then `P=Q`. If the flat has more than `d+1` members, this applies to every basis derivation of degree at most `d`; the first two matrix rows are proportional over the rational-function field. A free basis cannot have zero determinant. The bound is valid.

### 3.4 Counts and the unique possible four-point line

The pair-count identity is correct because a rank-two flat with `m` elements contributes `binom(m,2)` pairs and `m-1` to `b_2`. With exponents `(1,2,...,2)`, factorization gives `u=r-1`; with `(1,2,...,2,3)`, it gives `u+3v=r+1` and `n=2r`.

Crucially, local relation spaces are permitted to overlap linearly in their sum; the proof only uses the valid upper bound on the dimension of that sum. Formality yields

`r = dim R <= u+2v = r+1-v`,

so `v<=1`. There is no equality assumption hidden here. Together with connectedness, the all-2 case and the one-four-point-line case have exactly one fewer edge than vertices and hence are trees. In the remaining case, the incidence graph has cycle rank three and there are `r+1` triple-relation vectors spanning an `r`-dimensional space.

### 3.5 Minimal dependence really forces the K4 support

Take a minimal dependent family of `t` triple relations. Every relation coefficient in its dependence is nonzero, and every coordinate within any triple relation is nonzero because the represented points are distinct. Therefore every supported element occurs at least twice. If the union has `s` elements, `s<=3t/2`.

The support incidence graph is connected: otherwise the zero sum would split into nonzero dependences on disjoint supports, contrary to minimality. Its cycle rank is `2t-s+1`, which is at most three since its cycle space injects into that of the entire graph. Thus `s>=2t-2` and `t<=4`. Each triple's three elements must be covered by distinct other triples because different complete rank-two lines meet in at most one element. Hence `t>=4`. Equality forces exactly four triples, six elements, degree two at every element, and one distinct intersection for each pair of triples. This is precisely the subdivided K4 incidence support.

This is an all-ranks inequality argument. The finite enumeration of four-triple families is unnecessary for its validity. There is no assumption that every abstract support is realizable or that incidence automatically supplies a dependence: the dependence was extracted from the actual relation vectors first.

### 3.6 No additional cycles or non-tree attachments remain

The core already has the full cycle rank of the connected graph. Collapse the core to a single vertex and discard its internal edges; the remaining quotient is connected and has cycle rank zero. Thus it is a tree. An external path meeting the core twice or an external cycle would contradict that count. Core line vertices already have their full three incidences inside the core, so external attachments are at element vertices. This excludes arbitrary additional cyclic configurations in higher rank.

### 3.7 Terminal-pencil removal is a valid formal reduction

Let `L={a,p_1,...,p_{m-1}}` be terminal and retain `a`. Put `S` equal to the sum of local relation spaces of the other lines. Those are supported entirely on the retained elements. Formality gives `R=R_L+S`. Since a relation supported both on `L` and on the retained elements would be supported on the single nonzero form `a`, the intersection is zero. Intersecting the decomposition with the retained coordinate space gives `R'=S`; consequently the retained configuration is formal and has rank one less.

No removed form can belong to its retained normal span `W`. Otherwise its relation to the retained forms, after the above decomposition, would produce a nonzero relation supported on `a` and that removed form, which are independent. Thus `W` is a represented hyperplane flat, the pencil plane `U` intersects it in `Ka`, and every removed normal lies in `U` outside `W`.

This proof uses formality exactly where necessary. An independently constructed nonformal six-point control in the audit diagnostics has a terminal triple but removal does not lower rank. It is rejected by the candidate's hypotheses, demonstrating that the argument has not silently replaced formality by incidence alone.

### 3.8 The modularity and chain-extension step is global

For any subspace `F` generated by a subset of the arrangement's forms, let `S_F` be the span of the chosen forms in `W`. If the subset contains no outside form, the conclusion is immediate. If it contains exactly one outside form, that form has nonzero image in the one-dimensional quotient by `W`, so `F intersect W = S_F`. If it contains at least two outside forms, those distinct forms span `U`, giving

`F intersect W = S_F + Ka`.

In each case the intersection is spanned by represented forms. This proves modularity of `W` against every flat, not only rank-two flats. The represented-subspace criterion follows directly from the modular rank equality and the vector-space dimension formula.

If `C` is modular in the lattice inside `W`, then for every global flat `F`, the intersection `W intersect F` is a represented flat in `W`, and `C intersect F=C intersect(W intersect F)` is represented. Hence `C` is modular globally. Appending the full normal space to a modular chain in `W` is legitimate. No incorrect general assertion that all modular elements of every restriction remain modular is being used; the containing hyperplane is itself modular.

### 3.9 Pruning and the rank-three endpoint

A line vertex farthest from the root in any attached tree has its two outward element vertices as leaves. Pruning preserves precisely the relation generation needed to repeat the argument; freeness of the intermediate deletions is unnecessary. Tree cases terminate at rank-two pencils.

In the cyclic case, pruning leaves the six-element core. Its four triple relations have rank three, since they form a minimal dependence; formality after pruning then makes the normal rank three. Fix one of the core triples. Every other triple meets it in a represented point. A rank-two flat of size two corresponds to two disjoint indexing K4 edges, and exactly one of these meets the fixed indexing vertex. Thus this flat also meets the chosen triple plane in a represented point. Rank-zero, rank-one, and full-rank flats pose no additional condition. The triple plane is modular; a point on it completes a modular chain. The reverse pencil extensions and product/essentialization reductions finish the full theorem.

## 4. Independent computational checks

The author's entire checker ran under Python 3.12.14 and SymPy 1.14.0. Its output is **byte-for-byte identical** to the frozen `RESULTS.json`. This includes all eleven fixtures, the withdrawal Saito basis and 32 tangency checks, 1,716 six-point subsets, and 4,845 four-triple families.

I also wrote a separate checker without importing or calling the author's mathematical routines. It uses SymPy's exact linear algebra and independently enumerates the flats of five configurations. It checks:

- the rank-two arithmetic symbolically in an indeterminate rank;
- a parameterized K4 core whose four relation vectors have rank three and every three are independent;
- a four-point-pencil attachment with nonunit coefficients;
- a K4 attachment with nonunit coefficients;
- a nonformal negative control where terminal incidence alone fails;
- the non-Fano boundary, including a newly calculated explicit Saito certificate with degrees `(1,3,3)`, determinant exactly its defining product, and all 21 tangency conditions.

All checks passed. The independent non-Fano certificate closes a small diagnostic limitation of the author suite: the latter directly proves freeness for the withdrawal example but does not itself compute a freeness certificate for the non-Fano fixture. This was not a gap in the theorem, whose boundary observation is also independently standard.

## 5. Corrections, novelty, and limits

There are **no required mathematical corrections**. Optional clarifications are listed in `CORRECTIONS.md`; none changes the proof or its verdict. The author's artifacts remain unchanged.

A separate, bounded search for the exact title, one-3 formulations, formality/incidence formulations, and subsequent work found no inspected all-ranks resolution or identical argument. The author's current research page lists the Oberwolfach extended abstract. A potentially misleading search result about a conjecture solved by Abe was checked in [Burity–Tohaneanu v3](https://arxiv.org/html/2005.14367v3); that passage concerns a different line-arrangement realizability conjecture, not this all-ranks problem. This is useful disambiguation, not a novelty certificate.

The mathematical PASS does not certify publication priority, a complete literature search, arbitrary characteristic, multiarrangements, or a proof-assistant formalization. No remote writes, third-party communications, or modifications of the frozen inputs were performed. The portable audit bundle contains original analysis, verification code/results, and the exact author packet; it excludes scholarly PDFs/full text, dataset records/corpora, and private coordination material.
