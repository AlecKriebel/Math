# Independent adversarial audit: KOU-21.136 / catalogue 2645 / queue rank 475

Audit date: 2026-10-03 UTC. Audited object: the frozen 13-file `frozen_original/` package.

## Verdict

**PASS as a five-attempt, unresolved partial-results package. HOLD any claim of a general solution.**

No substantive mathematical error or publication-blocking gap was found in the restricted claims. The proofs establish the stated soluble-by-torsion theorem, normalizer obstruction, and countably based local reduction. They do not establish the unrestricted torsion conjecture. All ten finite controls pass independently. No correction to an original mathematical argument is required; two small wording clarifications are listed below.

This audit neither claims novelty nor certifies that a bounded literature search exhausts the literature. It performs no sixth proof attempt. Original attempts and the frozen package were not modified by the review.

## 1. Object integrity and scope

- The manifest SHA-256 is exactly `45c9e39e4f717e5930b287908cfd4bb5e3386cf374d26355d12143301e301f37`.
- All 12 listed files match their byte counts and SHA-256 hashes. Together with the manifest, the directory contains exactly the advertised 13 files.
- The five original files in `attempts/` match their frozen release counterparts byte for byte.
- This mathematical audit verifies the frozen package bytes; remote publication verification is separate.
- README, audit scope, research log, status, and all five attempts consistently disclaim a general resolution and novelty. The finite calculations are explicitly supplementary.
- The supplied Notebook page image visibly identifies 21.136 as this torsion question and separately identifies 21.137 as an unrelated question. The catalogue snapshot agrees. There is no imported resolution of 21.137.

## 2. Attempt 1: inheritance and countably based reduction — PASS

### Continuous images

For a continuous surjection G to Q, choose one lift of a representative of every infinite-order Q-class. A finite-order lift could not have infinite-order image. Conjugate lifts would have conjugate images. This injects the selected Q-class index set into the infinite-order G-class index set, so the claimed cardinal inequality is valid.

### Open subgroups

Fix a G-class meeting H and choose a representative in H. Decomposing G into cosets r_i H expresses the G-orbit as a union of at most [G:H] H-orbits. An H-orbit either lies entirely in H or avoids H. Thus its intersection with H has at most [G:H] H-classes. Multiplication by a fixed finite number preserves the strict inequality with continuum, including when continuum is singular; no continuum-hypothesis assumption is present. Arbitrary closed subgroups are correctly excluded.

### Factorial-power construction

Infinite order guarantees g^(n!) is nonidentity for every n, so an open normal V_n avoiding it exists. The descending finite intersections N_n give a closed normal K. The induced map G/K into the countable product of G/N_n is injective and has compact, hence closed, image. This gives a compact metrizable, second-countable quotient. If gK had order m, then g^(n!) would be in K for every n at least m, contradicting K contained in V_n. An infinite-order pro-p element remains pro-p under a continuous quotient and remains infinite-order by this argument.

### Literature input and finite-generation boundary

Wilson's Theorem A requires topological finite generation. His Lemma 4.2 does not; it supplies finite prime support using Herfort. The source phrases support through nontrivial p-elements, equivalent here to primes in finite quotient orders by profinite Sylow theory. Every topologically finitely generated continuous image is therefore finite. Nothing transfers this theorem to an arbitrary closed subgroup. The package correctly preserves that boundary.

## 3. Attempt 2: exact generator fusion — PASS, including p=2

For A isomorphic to Z_p, each topological generator a^v determines A uniquely as its closed generated subgroup. Any ambient conjugator between a^v and a^w therefore normalizes A. Conversely the normalizer's induced unit action realizes precisely these conjugacies. Since the unit group is abelian, its orbits on itself are exactly cosets of U; the number is [Z_p^times:U], with no additional fusion overlooked.

The normalizer is closed: preservation of a closed subgroup under both conjugation and inverse conjugation is a closed condition. Its conjugation action on A is continuous, visible by evaluating at a. Hence U is compact and closed. The quotient of the compact metrizable unit group by closed U is a compact metrizable group. If infinite it has no isolated points, and a nested binary clopen construction gives at least continuum points; metrizability gives at most continuum. Consequently fewer than continuum cosets forces finite index and U open.

For odd p, an open U contains a principal-unit group 1+p^k Z_p with k at least 1. At p=2 choose k at least 2. These groups are infinite, torsion-free, and isomorphic to additive Z_p. Thus U contains continuum infinite-order elements. If the normalizer were open, inheritance first to the normalizer and then to its quotient U would contradict U's abelian singleton conjugacy classes. Infinite-index closed normalizers are not covered by that inference. This is the precise distinction the package uses.

## 4. Attempt 3: abelian kernel and finite derived length — PASS

The local procyclic reduction is independent of the global finite-prime input. A procyclic profinite B is the product of its procyclic Sylow factors. Infinitely many nontrivial factors give continuum elements with distinct infinite prime supports: choose a generator on each selected coordinate and identity elsewhere. Infinite support makes each selected element infinite-order, and conjugation preserves supernatural order. If only finitely many factors occur and B is infinite, one is infinite procyclic pro-p, hence Z_p.

Now let B be closed, normal, and abelian, with G/B torsion. For A isomorphic to Z_p inside B and n in its normalizer, there is an integer m=m(n)>0 with n^m in B. Abelianity of B makes n^m centralize A. Therefore every induced unit has finite order. No common m is required.

The torsion units form a finite subgroup. Indeed a finite-index principal-unit subgroup is torsion-free, using 1+pZ_p for odd p and 1+4Z_2 for p=2. The valuation calculation in the attempt is valid in both stated ranges. Because the full unit group is abelian, its torsion subgroup injects into the finite principal-unit quotient. A torsion U is therefore finite, contrary to Attempt 2's forced openness and infinitude. Thus B is torsion; combining the finite order of gB with that of a suitable power in B proves every g has finite order.

The derived-series induction preserves all hypotheses. The last nontrivial closed derived term is closed, characteristic in S, normal in G, and abelian. Quotienting reduces the finite derived length, preserves P, and leaves the same torsion terminal quotient. Induction followed by the abelian-kernel proposition proves the theorem. A core of an open soluble subgroup is still open, normal, and soluble. This validates the virtually soluble consequence under the ordinary finite-derived-length meaning of soluble. It supplies no induction through unbounded prosoluble derived length.

## 5. Attempt 4: affine example and finite controls — PASS

Independently composing affine maps gives

    (a,v)(b,u)(a,v)^(-1) = (vb+(1-u)a,u).

For u=1, multiplication by units is transitive exactly on each finite nonzero p-adic valuation, so the translation subgroup meets countably many ambient infinite-order classes. It has continuum internal classes. This illustrates fusion without claiming a counterexample to inheritance from a group satisfying P.

The multiplier projection is an abelian quotient. Distinct nonidentity principal units yield continuum pairwise nonconjugate infinite-order complement elements. This defeats the proposed infinite affine example. A torsion complement has torsion unit image, necessarily finite, and leaves continuum generator classes instead.

Over R=Z/p^n Z, set d=min(v_p(1-u),n). Translation moves b by the ideal p^d R, and unit action on R/p^d R has one orbit at each valuation below d, plus zero. Hence there are d+1 classes for this multiplier. Independently summing d over units gives

    sum_u d(u) = sum_{j=1}^n #{u : u=1 mod p^j}
               = sum_{j=1}^n p^(n-j).

This yields the stated total and the translation sizes, including p=2,n=1.

### Independent computational evidence

The author's script was loaded with `runpy` and its `run()` called, avoiding its file-writing main block. Its return value equals the frozen JSON exactly. Separately, each affine element was realized as an actual permutation of R. Conjugacy was enumerated using permutation composition and inverse permutations, not the pair multiplication/inversion functions in the package. Each class was then compared against the formula, multiplier counts, and translation valuation sizes. An additional full commuting-pair count verified `number of commuting ordered pairs = |G| k(G)`.

| p | n | order | classes | commuting ordered pairs |
|---|---|---|---|---|
| 2 | 1 | 2 | 2 | 4 |
| 2 | 2 | 8 | 5 | 40 |
| 2 | 3 | 32 | 11 | 352 |
| 2 | 4 | 128 | 23 | 2944 |
| 2 | 5 | 512 | 47 | 24064 |
| 3 | 1 | 6 | 3 | 18 |
| 3 | 2 | 54 | 10 | 540 |
| 3 | 3 | 486 | 31 | 15066 |
| 5 | 1 | 20 | 5 | 100 |
| 5 | 2 | 500 | 26 | 13000 |

All checks passed. None establishes an infinite profinite assertion by finite approximation.

## 6. Attempt 5: class-space topology and local reduction — PASS

### Quotient class space

For descending open normals N_n with trivial intersection, maps into the finite conjugacy-class sets are continuous. Their joint image X is compact, metrizable, and zero-dimensional. If two elements have identical images, their finite-level conjugator sets are nonempty closed nested subsets of compact G. Their intersection gives an actual conjugator. Thus the fibers are exactly G-classes. The map is also a topological quotient because it is a continuous surjection from compact G to Hausdorff X. Independently, the full conjugacy relation is closed as the image of compact G times G under (g,t) mapping to (g,tgt^(-1)). There is no separation or closed-relation hypothesis missing.

### Bounded-order sets and perfect-set argument

T_m is closed as a power-map fiber and is conjugacy invariant. Its image F_m is compact and closed in X. Thus q^(-1)(F_m)=T_m, and the increasing union of F_m is precisely the finite-order class locus. E is G_delta.

The removal of points with a countable E-neighborhood removes only countably many points: each such point belongs to a countable E-intersection with one member of a countable base. If E is uncountable, every clopen parent meeting E uncountably contains at least two retained points. Around them one can choose disjoint small clopen children inside the parent and outside the next F_m. All children still meet E uncountably. Compactness and shrinking diameters give one point per binary branch, and closed children chosen outside F_m keep each limit out of every F_m. This gives continuum distinct E-points. Hence P forces E at most countable, without CH.

### Complete metric and Baire step

The displayed metric is valid. Each reciprocal distance to a nonempty closed F_m is finite and continuous on E. The weighted truncated differences form a metric contribution with summable bound. Finite-coordinate continuity and a uniformly small tail show the same topology as the original metric. A Cauchy sequence is Cauchy in the original complete metric, and each reciprocal-distance coordinate is an ordinary real Cauchy sequence: truncation at 1 causes no problem for sufficiently small tolerances. These coordinates are bounded, so the original limit cannot enter any F_m. It lies in E, and the same finite-head/tail argument gives convergence in the new metric.

A nonempty countable completely metrizable E cannot consist exclusively of nowhere-dense singletons. Some infinite-order class is relatively isolated. A finite cylinder isolating it can be refined to the single conjugacy-class condition at N_n because the basis is descending. The coset N_n x lies in the inverse image of that cylinder. Thus its infinite-order locus is nonempty and contained in the one global class x^G. Relative isolation is not promoted to openness of x^G.

### Exclusion of an open infinite-order class

If an open normal coset Ny is contained in x^G, conjugate y to x, retaining N by normality. For every open normal L contained in N, the class of xL has at least |N/L| points. The finite centralizer therefore has order at most [G:N], so xL has order at most that same fixed bound. Consequently x^([G:N]!) lies in every such L, whose intersection is trivial. This contradicts infinite order. No countability assumption is required here.

Each class is closed and hence an infinite-order class is nowhere dense. In the special coset N_n x its complement is open dense and torsion. A compact open coset inside any nonempty open part of that complement is covered by the closed T_m; Baire supplies a smaller open set, and then a smaller open coset, of bounded exponent. This is an assertion about that smaller coset, not a claim that a neighborhood of the exceptional class is torsion.

## 7. Exact remaining gaps and disposition

The unresolved steps are real and are accurately disclosed:

1. P has not been established for arbitrary closed subgroups, in particular the necessarily infinite-index normalizers in Attempt 2.
2. The induced unit quotient of such a normalizer is not thereby a continuous quotient of G. Openness of U does not make the normalizer open.
3. No argument excludes an open coset whose nonempty infinite-order locus lies in one global conjugacy class. Excluding an entire open infinite-order class is strictly weaker.
4. Dense torsion and bounded-exponent subcosets do not dispose of the exceptional infinite-order locus.
5. The soluble-kernel induction terminates only for finite derived length.

There is no claimed repair of these gaps. They require additional mathematics; filling them would be further research, not audit cleanup.

## 8. Exact minor clarifications and source handling

These nonblocking editorial items have been applied to the current attempts and recorded in CHANGE_MAP.json; the audited originals remain unchanged in frozen_original/:

- Attempt 1, section 1: replace “right cosets r_i H” by “left cosets r_i H” or simply “cosets r_i H.” The orbit formula and the bound are already correct.
- Attempt 5, section 4: make the initial phrase explicitly “an open coset Ny, with N open normal in G.” Any nonempty open subset contains such a coset, so this only spells out an already available choice.

Wilson's displayed Corollary 3.1 omits finite generation; the surrounding text and Theorem C require it. The infinite exponent-p product of copies of C_p refutes the unrestricted finiteness wording. The package handles the omission correctly. The locally supplied published PDF/text and page image were examined, and the primary arXiv version was fetched independently: https://arxiv.org/abs/2209.14753 and https://arxiv.org/pdf/2209.14753 . Fresh access to the Cambridge and Notebook PDF URLs failed in this audit, so their local supplied primary snapshots, not a fresh successful download, support the relevant checks.

The author-hosted Barnea–Camina–Ershov–Lewis paper was fetched independently. Its invariant counts cyclic/procyclic subgroup coverings, including the affine example, rather than infinite-order element classes. Its use as a distinct, nonresolving nearby source is accurate: https://m-ershov.github.io/Research/ncc_final2025.pdf .

The frozen references to independent review being pending describe the pre-audit snapshot. Any later publication metadata may link this separate audit without changing the preserved attempts or portraying a general solution. Independent review does not establish a general solution; final publication and remote-state verification are separate.
