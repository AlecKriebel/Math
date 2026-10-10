# Second independent mathematical audit: internal threshold one

Problem 10000036 / AMR-099-0036, rank 875. Review date: 6 October 2026.

## Verdict

**ACCEPT for mathematical correctness within the manuscript's stated scope.** No mathematical repair is necessary. The audited construction answers the weak finite-energy existence question affirmatively for every fixed integer d >= 2. Its law is invariant under all lattice automorphisms and mixing under translations; it has one infinite cluster almost surely, and that cluster has quenched Bernoulli bond critical probability one. The internal site-thinning assertion also follows. Neither uniform finite energy nor finitary coding is established or required.

This is an independent written proof audit, not a formal proof-assistant verification or an assertion of novelty, priority, or current community acceptance. The assessment was reached without consulting another auditor's conclusions. The external input is an established one-ended spanning-tree theorem. All subsequent arguments have been checked directly below.

## 1. Audited bytes and scope

The immutable author archive has 13,793 bytes and SHA-256

`266debc377c66c6813e9db2b6abc704454ead9cdec47024f5d15338329b2fe05`.

Its external manifest has 1,268 bytes and SHA-256

`80ae7742dec006af9feb3de07722ce520ecb2a1393809ff86e19d798b85b56c2`.

Before mathematical inspection, both pins were matched, the six-member archive inventory was inspected, and every member's byte count and SHA-256 was matched against the external inventory. The members are APPROACHES.md, AUDIT_GUIDE.md, MANIFEST.json, PROOF.md, SOURCES.json, and STATUS.md. No executable mathematical checker is present. PROOF.md has 16,299 bytes and SHA-256

`c31b7a1cd6a3af04807b20d58f23d79f9d07cf4eb87df26187498f3260f9891d`.

The full supplied catalog, problem collection, and research-report collection were parsed as data and their complete-file pins checked. The matching record identifies rank 875 and the stated problem number; the earlier report is search triage rather than a mathematical proof attempt. The catalog question has no explicit all-dimensions quantifier. The manuscript's conclusion for every d >= 2 is its own stronger, explicitly stated scope. No raw catalog records or research reports are reproduced in this audit packet. Three substantive approaches are recorded, within the five-approach limit; this review adds no new research approach.

Benjamini's Saint-Flour notes, printed/PDF page 61, identify the intended existence problem as Open problem 8.15. The current direct notes URL did not open successfully; the pinned archived PDF and its rendered page were inspected. The live catalog webpage likewise did not open, so no live status confirmation is claimed. [S]

The earlier BHS Question 1.1 specifies full lattice-automorphism invariance and defines finite energy through positivity of both single-edge conditional probabilities. BT Question 1 repeats this convention. These statements concern bond configurations and do not demand uniform conditional bounds. This removes the main possible scope mismatch. [BHS, BT]

## 2. Independent deterministic reconstruction

Let G=(V,E) be an infinite connected graph with countable vertex set and degree bounded by Delta, and let T be a connected spanning tree with exactly one end. Only these assumptions are needed until the lattice-symmetry step.

### 2.1 Finite sides and ray geometry

Deleting a tree edge t leaves exactly two components. They cannot both be finite because T is infinite. They cannot both be infinite: each would contain a ray by local finiteness, and the two rays would determine different ends. Thus there is a unique finite side S(t), with positive finite size s(t).

From any v there is a unique infinite simple T-ray. Existence follows from local finiteness; two different rays from the same vertex in a tree would never merge again and would give different ends. Write its consecutive edges t_0,t_1,... and put S_n=S(t_n), s_n=s(t_n). The starting vertex belongs to every S_n. Removing the next edge leaves S_n and the intervening next ray vertex on its finite side, so S_n is strictly contained in S_(n+1). Therefore s_n are strictly increasing positive integers. In particular, for nonnegative a_m,

    sum_n a_(s_n) <= sum_(m>=1) a_m.

This is stronger than merely knowing s_n tends to infinity; the stronger assertion is precisely what makes the proposed summability bound valid. Different starting rays in a one-ended tree eventually coalesce. For completeness, the S_n actually exhaust V: the ray from any other vertex eventually merges with this ray, so that vertex is on the finite side of every sufficiently late t_n. Exhaustion is available, although the thinning proof needs only that each S_n is finite and contains v.

For an ambient edge e={x,y} outside T, connectedness of the spanning tree supplies a finite unique path P_T(x,y). Set

    M(e) = max {s(t): t belongs to P_T(x,y)}.

If e crosses S(t), then x and y are on opposite sides of T\{t}; hence P_T(x,y) contains t and M(e)>=s(t). Finally, at most Delta*s(t) ambient edges leave S(t), by counting degrees at vertices in S(t). All these are deterministic statements; no geometric regularity, volume-growth property, or independence is being smuggled into them.

### 2.2 Definition and measurability of the random graph

Conditionally on T, choose independent edge uniforms U_e. Include a tree edge t with probability 1-2^(-s(t)); include a non-tree edge e with probability 2^(-M(e)). Every coordinate parameter is strictly between zero and one.

The finite side of a fixed tree edge is measurable. For any fixed candidate finite set A, deciding that A is the relevant component requires checking connectedness inside A and the finitely many incident boundary edges. Taking a countable union over finite A yields measurability of s(t). A path between specified endpoints is identified by a countable union over finite candidate paths, giving measurable M(e). The event that T is a connected, acyclic, one-ended spanning subgraph is Borel: connectivity, acyclicity and the finite-side characterization above each admit countable descriptions. Assigning the constant parameter 1/2 on the exceptional set therefore gives a globally measurable kernel.

Automorphisms transport finite components and tree paths to their counterparts without changing cardinalities. Thus all parameters transform equivariantly. No origin, direction, enumeration, or arbitrary selected infinite ray is used in defining the process. An enumeration used to formalize countable probability spaces changes no output law.

### 2.3 The indispensable bypass estimate

Fix a good deterministic T and a vertex v. At the n-th ray cut, let B_n denote the event that either t_n is deleted or some non-tree edge crossing S_n is inserted. Conditional on T, the union bound gives

    P(B_n | T) <= 2^(-s_n) + Delta*s_n*2^(-s_n).

Summing over n and using the strict size increase gives

    sum_n P(B_n | T) <= sum_(m>=1) (1+Delta*m)*2^(-m)
                       = 1+2*Delta < infinity.

Crucially, an inserted edge may cross several of these cuts, so the events B_n need not be independent. Only the first Borel-Cantelli lemma is used, for which summability is sufficient. It follows that, almost surely in the conditional edge-mark law, there is an N_v after which every t_n is retained and every competing crossing edge is absent. Consequently

    boundary_X(S_n) = {t_n} for every n>=N_v.

Deletion of other tree edges does not affect this boundary calculation: only t_n ever crossed this particular tree cut. The finite side need not remain connected in X. Separating a finite set from its complement depends on its boundary, not on its internal connectedness.

There are countably many vertices. Intersect the conditional full-probability events over all v, and then integrate over the random T. This yields one full-probability event for the pair (T,X) on which the retained-tail and singleton-boundary statements hold at every vertex. No intersection over an uncountable family of trees is needed.

### 2.4 Existence and uniqueness of the infinite component

The graph R formed by retained tree edges has a retained infinite ray tail and therefore an infinite component. Every two retained tails coalesce inside T; their common sufficiently late tail is still retained. If R had another infinite component, local finiteness would produce an infinite R-ray in it. That ray is the unique T-ray from its initial vertex, and hence it would meet the same common retained-tail component. Therefore R has a unique infinite component C_R.

An infinite component of X must contain an infinite simple ray. If v lies in such a component, that ray must exit every finite S_n containing v. For n>=N_v it must cross t_n, the sole X-edge leaving S_n. Both endpoints of t_n belong to the retained tail and thus to C_R. Hence every infinite X-component contains C_R, proving existence and uniqueness of the infinite X-component C.

This argument also explicitly excludes an infinite component assembled solely by inserted edges joining finite components of R. Such a proposed component would still have to cross the same singleton boundaries and reach C_R. A uniqueness theorem for general invariant percolation is unnecessary.

### 2.5 Quenched threshold, all vertices, and all parameters

Fix a pair (T,X) in the good event. For a fixed vertex v and p<1, independent Bernoulli-p bond thinning of this now deterministic X can connect v to infinity only if every distinct t_n with n>=N_v survives. The first k of these edges are independent thinning coordinates, so

    P_p^X(v has an infinite thinned component) <= p^k.

Letting k increase gives zero. A countable union over vertices excludes any infinite thinned component. The same deterministic witness works separately for every real p<1; there is no exchange of an uncountable intersection with a probability-one statement. If a simultaneous monotone coupling is desired, applying the conclusion to rational p<1 and using monotonicity yields it as well.

The conclusion is genuinely quenched. Its randomness is only the independent thinning after X is fixed. The input tree serves as a witness, not as part of the thinning environment that must be resampled. The property of X is measurable: for fixed rational p and v, the conditional percolation probability is the limit of measurable finite-radius connection probabilities. Thus the full joint-probability conclusion transfers to the X marginal without a hidden projection-measurability assumption.

At p=1 the unique infinite cluster C exists. Hence p_c(X)=1. Restricting to C gives the same obstruction because each sufficiently late cut edge is in C and is the only C-edge crossing S_n intersect C. Therefore p_c(C)=1. Independent site thinning is also blocked, since every path to infinity must retain infinitely many distinct ray vertices. This last observation concerns internal thinning of a bond-generated graph; it does not claim that an external site process has been constructed.

### 2.6 Finite energy of the observable marginal

Let F_e be the sigma-field generated by all output edge states except e, and let r_T(e) be the parameter above. The collection (T, (U_f)_(f!=e)) is independent of U_e. Since F_e is contained in its sigma-field,

    P(X_e=1 | T,F_e) = r_T(e).

Applying conditional expectation once more yields

    P(X_e=1 | F_e) = E[r_T(e) | F_e],
    P(X_e=0 | F_e) = E[1-r_T(e) | F_e].

If Y is strictly positive almost surely, its conditional expectation given any sigma-field is strictly positive almost surely: on the measurable set where the conditional expectation vanishes, the integral of Y vanishes, which forces that set to have probability zero. Apply this with Y=r_T(e) and with Y=1-r_T(e). Both output states have positive conditional probability. Countability of E permits the assertions for all edges simultaneously outside one null set. Versions can be set to 1/2 on null conditioning configurations if needed.

This argument addresses the marginal law, rather than stopping at finite energy conditional on the hidden tree. Even if other output edges reveal much of T, they cannot reveal the unused independent coordinate U_e. Conversely, arbitrarily small tree-conditioned parameters alone would not prove that marginal conditional probabilities lack a uniform bound. The manuscript correctly avoids that unsupported converse assertion.

## 3. The lattice input and exact symmetry claims

Timár's Theorem 1 gives a one-ended spanning tree that is a factor of iid on an ergodic, amenable, one-ended unimodular random graph. His factor definition uses Borel maps equivariant under rooted isomorphisms, and Corollary 2 explicitly confirms the invariant-tree conclusion for the quasi-transitive setting. The source is a connected spanning-tree theorem, not merely a forest theorem. The arXiv primary text and rendered first two pages were inspected; the arXiv record identifies its publication in ECP 24 (2019), paper 72. [T]

For every d>=2 the rooted nearest-neighbor lattice is deterministic and therefore ergodic as a rooted graph law. Its translation action yields the mass-transport identity by summing over displacement vectors, so it is unimodular. Cubes have boundary-to-volume ratio tending to zero, which verifies amenability. Removing a finite set leaves one infinite component: outside a sufficiently large cube the lattice is connected when d>=2. Thus all hypotheses apply.

The isomorphism-equivariant factor on this fixed graph gives the required full automorphism invariance, including rotations and reflections. Adjoining independent edge marks preserves this invariance, and the kernel was already checked equivariant. There is no illicit randomization by a nonexistent uniform distribution on all lattice translates.

For translation mixing, the joint label-and-mark field is a product process. Approximate two measurable events by finite-coordinate events; sufficiently distant translates have disjoint supports and are independent. Letting the approximation errors go to zero proves mixing of the product field. Taking preimages under the measurable equivariant construction proves mixing of X. This proof needs no finitary coding radius. The manuscript does not assert a finitary factor, and none should be added merely because each individual tree path and finite past is finite: discovering those objects from the original iid labels need not have a proven finite stopping radius.

Pemantle's Theorems 2.3 and 4.3 independently provide the older one-ended UST input in dimensions 2, 3, and 4. Exhaustion-independence makes its law invariant under every automorphism by transporting finite approximants. The high-dimensional uniform spanning forest cannot be used as this construction's input because endpoints in different components have no tree path. The principal all-dimensional and mixing assertions are instead supported by Timár's factor input. [P]

## 4. Adversarial failure modes resolved

- **Infinite finite-side sizes:** excluded by local finiteness and one-endedness for every tree edge.
- **Only increasing distances rather than sizes:** the proof uses strict nesting of finite sides, which gives distinct integer sizes.
- **A hidden bypass using many inserted edges:** any exiting path has a first edge crossing the finite-set boundary; all competing crossing edges are absent.
- **One inserted edge influencing many cuts:** allowed; summability and first Borel-Cantelli do not require independence of cut events.
- **New infinite components made from finite retained pieces:** excluded by the singleton-boundary argument connecting any infinite X-component to C_R.
- **Only a rootwise conclusion:** countable intersections and unions cover every vertex and every component.
- **An annealed threshold mistaken for a quenched one:** the thinning calculation fixes the complete realized graph and its witness before introducing thinning randomness.
- **Uncountably many p-values:** a deterministic family of singleton cuts gives the p^k bound for all p<1 on the same good graph.
- **Finite energy only before forgetting T:** the conditional-expectation calculation proves it after marginalization.
- **Finite energy interpreted uniformly:** the source uses positivity, and the accepted theorem is explicitly limited to that convention.
- **Unverified finitary or quantitative mixing claims:** neither is required or asserted; only ordinary translation mixing is proved.
- **Uniform sprinkling used implicitly:** no fixed-density sprinkling is used; the insertion parameters depend on the original tree geometry.

The argument does not claim every vertex lies in the infinite cluster. Finite components are allowed and are consistent with the source question. It does not establish positive association, finite dependence, or robustness under thinning; the last of these is deliberately disproved for the constructed graph.

## 5. Antecedent and bounded literature check

Häggström–Mester Section 2 already uses summable flips based on finite past sizes to preserve ray tails and obtain weak finite energy in a site-coexistence example. Its Section 3 threshold-one observation concerns the unflipped X-hat, not the finite-energy X-bar. That displayed observation is therefore not itself a stated solution of the present bond question. The inspected proposition also does not supply the present all-bypass cut estimate. Credit for the summable perturbation mechanism is necessary and is already present. No claim is made that an additional argument could not extract related consequences from that earlier model. [HM]

The present manuscript supplies the separate no-bypass estimate through the maximum finite-past size along each non-tree edge's connecting tree path. Its mathematical correctness does not rely on a literature-status assumption. Bounded searches of the exact question, the BT question, finite energy with critical probability one, and one-ended-tree perturbations located no exact prior resolution. This is insufficient to decide novelty or priority. In particular, one must not equate a valid affirmative proof with a verified first solution of a still-open problem.

BT's fixed-density sprinkling theorem is not contradicted: the process here deletes tree edges and uses tree-dependent insertion probabilities. There is no assertion that the retained tree subgraph percolates at every vertex, and no decomposition into the theorem's required everywhere-percolating core plus independent fixed-density sprinkling has been supplied. [BT]

## 6. Acceptance boundary and disposition

The original proof is accepted unchanged. No patched derivative is needed. The author archive remains untouched and its original candidate-status wording is preserved as historical provenance; this separate report records the later acceptance decision. The conclusion remains an authored mathematical result supported by a written audit, not a computation, simulation, automated proof certificate, or newly verified publication-status claim.

Only authored audit text, a separate acceptance report, and verification/public-source metadata are included in the review archive. Third-party source PDFs, extracted source text, images, raw dataset records, and private coordination material are excluded. No publication or external upload was performed by this review.

## Public references

[S] I. Benjamini, Coarse Geometry and Randomness, Open problem 8.15, p. 61. https://www.wisdom.weizmann.ac.il/~itai/stflouraug24.pdf#page=61

[BHS] I. Benjamini, O. Häggström and O. Schramm, On the effect of adding epsilon-Bernoulli percolation to everywhere percolating subgraphs of Z^d, Journal of Mathematical Physics 41 (2000), 1294–1297. https://arxiv.org/abs/math/9906002

[BT] I. Benjamini and V. Tassion, Homogenization via sprinkling, Annales de l'Institut Henri Poincaré, Probabilités et Statistiques 53 (2017), 997–1005. https://doi.org/10.1214/16-AIHP746 ; https://arxiv.org/abs/1505.06069

[HM] O. Häggström and P. Mester, Some two-dimensional finite energy percolation processes, Electronic Communications in Probability 14 (2009), 42–54. https://doi.org/10.1214/ECP.v14-1446 ; https://arxiv.org/abs/1011.2872

[P] R. Pemantle, Choosing a spanning tree for the integer lattice uniformly, Annals of Probability 19 (1991), 1559–1574. https://arxiv.org/abs/math/0404043

[T] A. Timár, One-ended spanning trees in amenable unimodular graphs, Electronic Communications in Probability 24 (2019), paper 72. https://doi.org/10.1214/19-ECP274 ; https://arxiv.org/abs/1805.10690
