# Independent audit of the Häggström-Mester implication

Audit date: 15 October 2026 UTC. Scope: PR838 / problem 10000036, d=2 antecedent mechanism only. The original effort count remains 3/5. This audit is not a new target proof-search attempt. No sibling classical-audit verdict was read before or during this audit.

## Decision

**Mathematical PASS, with source and model distinctions.** The exact post-flip Section 2 site model in Häggström-Mester (HM) has internal site and bond critical probability one for its open graph, almost surely; the same holds for its closed graph. The bounded-cycle argument below supplies a complete deduction. It is additional reasoning in this audit, not a theorem that the inspected paper prints.

A direct bond construction on the original coarse square lattice also passes. The **exact fixed-phase midpoint marginal** of HM has tree deletion and complementary-dual insertion rates **4^{-s}**, not 2^{-s}. The proposed rates 2^{-s} give a second valid adaptation. Both bond laws have full lattice-automorphism invariance, translation mixing, ordinary conditional finite energy, a unique infinite component, and quenched internal critical probability one. The site-to-bond critical-value lemma alone does not establish an external bond finite-energy law.

This is substantial d=2 antecedent evidence. It does **not** establish that a solution to the exact question was previously published, recognized, or claimed. It does not establish the d>=3 conclusion of the submitted construction. The original all-dimensional proof is not being rejected on mathematical grounds here.

## Exact source and what is printed

The controlling source is [HM, Electronic Communications in Probability 14 (2009), 42-54](https://www.maths.tcd.ie/EMIS/journals/EJP-ECP/article/download/1446/1446-4872-1-PB.pdf), SHA-256 `ddbf7afb7874e41839426dc0158d473ae369ae593334f77021dbdef26f2c0c1d`, 165957 bytes. It differs from the root's arXiv PDF. Relevant complete pages were extracted and visually inspected, with pins in SOURCE_READING_LEDGER.json.

HM printed pp44-45 specify a primal UST and its one-ended complementary dual, a subdivided site picture, a uniform parity shift, and independent flips of probability 2^{-b(x)-1}. Here b(x) counts other vertices separated from infinity by removing x. Proposition 2.1 asserts coexistence and finite energy. Printed p45 states Lemma 3.1, the equivalence of site and bond thresholds being below one on bounded-degree graphs. Printed p46 asserts threshold one for the **pre-flip** model; it does not assert it for the post-flip model. Printed p43 recalls the invariant finite-energy uniqueness theorem.

The subsequent arguments in this report are audit deductions. In particular, neither the post-flip cycle estimate nor the midpoint bond construction is attributed as a printed HM theorem.

## A deterministic planar lemma

Use the standard planar embedding of G=Z^2 and its dual G*. Let T be a one-ended spanning tree of G such that the complementary dual edge set T* is also a one-ended spanning tree. These hypotheses hold almost surely for the planar UST used by HM.

Take t in T. Its dual t* is absent from T*. The endpoints of t* are joined by a unique finite simple path P* in T*. Consequently C*=P* union {t*} is a finite simple cycle in the square dual lattice, and its embedding is a Jordan curve.

Every dual edge of C* except t* crosses an edge outside T. The only T-edge crossing C* is t. The inside contains a finite nonempty set A of primal vertices, and the outside contains infinitely many. Since T is connected and only t crosses the curve, the T-subgraphs on each side are connected: any additional T-component on a side would have no possible route to the other side or to its side's component incident to t. Thus A is exactly the finite component S_T(t) of T-t. A primal edge crosses C* precisely when its dual is an edge of C*, so

    {e*: e in delta_G S_T(t)} = C* = P* union {t*}.

This proof also excludes self-touching or multiple-boundary objections. It starts with a simple fundamental cycle in the dual tree instead of presupposing that an arbitrary finite set has a simple boundary. It uses dual connectedness essentially.

Fix a primal vertex o and follow its unique infinite T-ray. Write t_n for the successive ray edges and A_n=S_T(t_n). Then A_n strictly increase. They exhaust all primal vertices: the unique ray from every vertex eventually merges with the ray from o, and its finite connecting path is on the finite side of a sufficiently late ray edge. Hence every finite primal box is contained in all sufficiently late A_n.

The cycles C_n*=delta_G A_n, viewed dually, escape every compact set. For a fixed dual vertex, all primal vertices in its adjacent faces eventually lie in A_n, so it eventually has no incident boundary edge. The same applies to every finite set of dual vertices or edges. After HM's factor-two scaling, the circuits also escape every finite set of sites. Their interiors eventually contain every site. The cycles need not be disjoint initially; escape and exhaustion allow a disjoint subsequence.

## Multiplicity of finite past sizes

For a locally finite one-ended tree H and vertex x, let D(x) be x together with all its finite descendants toward the unique end, so b(x)=|D(x)|-1. If y is a child of x, then D(y) is a proper subset of D(x), and b(y)<b(x).

Any finite simple H-path is the union of two chains directed toward their first common ancestor. Along each chain b strictly increases. Give the common ancestor to just one chain. Each integer therefore appears at most twice among the b-values on the path. The same argument applies to edge finite-side sizes s_H(h), by associating an edge with its child endpoint. The argument includes leaves with b=0, ancestor-descendant paths, and paths of length zero. It applies unchanged after subdividing all edges.

This is a deterministic statement, not a UST correlation or geometry estimate. Branches off the path only increase the descendant counts and do not undermine strict increase along either arm.

## Post-flip site cutsets

Condition first on the good tree pair and on HM's phase. In the factor-two site picture, the cycle C_n* is a nearest-neighbor site circuit. Its dual-tree part is a simple path in the subdivided dual tree and is initially closed. The sole remaining site is the midpoint crossing t_n, which is initially open. Thus there is exactly one initially open site on the circuit.

Let Z_n count finally open sites on that circuit after HM's flips. Multiplicity of b along the initially closed path gives

    E[Z_n | T, phase]
      <= 1 + 2 sum_{m=0}^infinity 2^{-m-1}
      = 3.

The bridge site contributes at most one regardless of its own flip. No independence between different cycle counts is required. Conditional Fatou gives

    E[liminf_n Z_n | T, phase] <= 3,

so the liminf is finite almost surely. Therefore, for almost every final configuration and its tree witness, some finite integer K bounds Z_n for infinitely many n.

Choose such cycles recursively so each is outside a box containing all earlier circuits. They are pairwise site-disjoint and still surround every fixed site eventually. Their finally open portions S_j are pairwise disjoint vertex separators of the final open graph and satisfy |S_j|<=K. Every infinite nearest-neighbor path from a site in an interior must meet the corresponding S_j. Opening sites elsewhere cannot circumvent the Jordan curve without meeting a circuit vertex; both the circuit and the final paths lie in the same square-lattice embedding.

Now fix that final graph and witness, then fix any p<1. Independent Bernoulli-p site thinning must retain at least one site of every sufficiently late S_j for any fixed vertex to connect to infinity. If K=0, an empty separator already prevents escape. If K>=1, independence of thinning on the disjoint S_j gives, for any r such necessary separators,

    P_p(vertex connects to infinity)
      <= [1-(1-p)^K]^r -> 0.

Every fixed vertex is inside all sufficiently late circuits. A countable union over vertices proves absence of every infinite thinned component. This argument works for **every p<1 on the same deterministic good graph**; it does not make an unjustified intersection of uncountably many annealed null events. The tree is an existence witness for a graph property. Forgetting the tree does not change that property or the subsequent product thinning measure.

HM's eventually unflipped primal ray tail ensures that the final open graph percolates at p=1. Thus its internal site threshold is exactly one. Its degree is at most four, so HM Lemma 3.1, contraposed, makes its internal bond threshold one. Exchanging primal and dual and open and closed proves the corresponding closed-graph assertions.

## External bond construction and the exact rate correction

The preceding threshold conversion keeps the same graph. It does not turn an external site law into an external bond law with finite energy: setting an edge open exactly when its two endpoint sites are open can have single-edge states forced by other edge states.

A direct construction avoids this issue. For a midpoint x of a subdivided tree edge h with finite original vertex side of size s, the finite component after removing x contains s original vertices and s-1 other midpoints. Therefore

    b(x)=2s-1,   2^{-b(x)-1}=4^{-s}.

Consequently the midpoint coordinates of HM's construction **conditioned to a fixed phase**, read as edges of the coarse primal lattice and with all coarse vertices kept present, have the following conditional edge law:

    r_T(e)=1-4^{-s_T(e)}                 when e in T,
    r_T(e)=4^{-s_{T*}(e*)}              when e outside T.

The midpoint flips are conditionally independent. Vertex-site flips are discarded. This identifies the exact fixed-phase midpoint distribution; it does not assert that this bond graph equals HM's final open site graph or is recoverable from that graph without its latent phase.

The parent's proposed rates replace 4 by 2. For either a=4 or a=2, write the deletion/insertion rates a^{-s}. Then the number W_n of open bond edges through delta_G A_n satisfies

    E[W_n | T] <= 1 + 2 sum_{m>=1} a^{-m},

which is 5/3 for a=4 and 3 for a=2. Here the non-tree cut edges correspond exactly to the dual-tree path P_n*, whose finite edge-side sizes have multiplicity at most two. Fatou again gives infinitely many bounded open edge cutsets. Since the A_n exhaust the lattice, their boundaries escape each fixed finite edge set, allowing a pairwise edge-disjoint subsequence. Independent bond thinning has the identical product obstruction, now on edges. Thus quenched bond p_c=1; site thinning also fails by selecting disjoint finite endpoint neighborhoods of sufficiently separated cuts.

The deletion probabilities along every primal ray are summable, because its positive finite-side sizes strictly increase. The first Borel-Cantelli lemma gives an eventually fully retained primal ray tail, proving percolation. The conditional probabilities r_T(e) lie strictly between zero and one. After forgetting T,

    P(e open | all other final edges)=E[r_T(e) | all other final edges],

and both this quantity and its complement are positive almost surely. This proves ordinary finite energy. Small latent probabilities alone do not prove that the marginal law lacks uniform finite energy; no such marginal nonuniformity claim is needed here.

The bond rule is intrinsic in the embedded primal/dual pair. Every lattice automorphism carries dual faces, crossing pairs, and finite-side sizes to their images, so the rule is fully equivariant. The UST law is fully invariant, by exhaustion independence and the symmetries of finite approximations. Its translation mixing follows from its tail triviality, also explicitly used in Pemantle's proof of Theorem 4.3 (arXiv version, printed p21). The independent edge-mark extension is mixing; the bond field is a measurable equivariant factor, so it is mixing as well. No locality or finitary coding is required. Finally the invariant finite-energy uniqueness theorem applies on the square lattice, giving exactly one infinite component. Restricting the thinning extinction result to this component gives p_c(C)=1.

## The phase is a real mixing distinction

The random parity shift in HM's site law cannot be ignored when claiming mixing. In fact that site law is not translation mixing. Conditioned on any fixed phase it is mixing under even translations, since it is a factor of the UST and independent site marks. At an original primal vertex its conditional open mean is strictly greater than 1/2: the flip probability is at most 1/2 and is strictly smaller with positive probability. Positivity follows because, by transitivity, a fixed tree vertex has positive probability of having a child; otherwise every vertex would almost surely be a leaf, contradicting connected infinitude. At an original dual vertex the conditional open mean is strictly less than 1/2 by the same argument.

Let m_R be the conditional open mean at a fixed site given phase R. These means are not all equal. Conditional mixing under displacements (2n,0) implies that the limiting covariance of the two site indicators is Var(m_R)>0. Thus the parity mixture fails mixing. The intrinsic bond construction has no random phase and passes the required mixing test. Full site-law lattice invariance still follows from its uniform phase and the UST symmetries.

## Priority weight and remaining gap

The planar audit has no remaining mathematical gap under the cited standard UST and invariant finite-energy uniqueness inputs. It finds no counterexample to the proposed bounded-cycle implication. The corrections are about the exact rate and model categories, not failure of the threshold argument.

The inspected HM paper does not print this post-flip deduction or claim to solve the exact internal-threshold question. [Benjamini-Tassion's 2015 arXiv version, Question 1 on p3](https://arxiv.org/pdf/1505.06069v1) still poses the invariant ordinary finite-energy bond question. That is evidence against casually describing HM as a recognized prior solution; it is not a mathematical disproof of the deduction above.

Safe attribution is: the d=2 conclusion follows by the supplied planar argument from HM's published tree-flip construction, and a direct bond version is obtained from its midpoint coordinates (exactly with rates 4^{-s}). The same planar argument validates the changed rates 2^{-s}. Calling this a **previously published exact solution** is unsupported by the inspected sources. Calling the d=2 construction or mechanism wholly novel is also unsafe after this audit. The submitted maximum-along-primal-path rule and its all-dimensional extension require their own sharply delimited novelty assessment. No conclusion about priority for d>=3 is supplied here.

All work stayed in this audit folder; source reads outside it were read-only. No Git operation, remote mutation, publication, release, external communication, or cross-chat communication was performed. Internal parent messages reported the two model distinctions promptly. Raw PDFs, source extracts, and renderings are excluded by the local deny-by-default .gitignore. The public manifest covers only authored audit artifacts.
