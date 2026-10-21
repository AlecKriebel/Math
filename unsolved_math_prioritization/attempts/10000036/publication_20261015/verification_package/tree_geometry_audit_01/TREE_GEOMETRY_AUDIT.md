# Adversarial tree-geometry audit: PR 838 / problem 10000036

## Verdict and exact boundary

**PASS for the deterministic and quenched arguments in frozen author PROOF.md Sections 2–6. No substantive defect and no necessary repair were found.** The measure-theoretic expansions below make two abbreviated passages explicit; they do not alter the kernel or supply a missing central construction.

Frozen PR head: `ed2de7249953ba0c1afad253adca9b820d7297c5`. Frozen proof: `source/author/PROOF.md`, 16,299 bytes, SHA-256 `c31b7a1cd6a3af04807b20d58f23d79f9d07cf4eb87df26187498f3260f9891d`. All 27 supplied source-file hashes match SOURCE_MANIFEST.json; this is an identity check, not a proof certificate.

This family verifies the following conditional theorem: if G is countably infinite, connected, simple, has maximum degree Δ<∞, and T is a one-ended spanning tree, then the stated independent-edge kernel conditional on T almost surely produces X with one infinite component C, and the quenched internal Bernoulli bond and site critical probabilities of X and C are one. The result holds for every deterministic admissible T and hence for any random T supported on admissible trees.

This family does **not** independently certify the primary-literature interpretation of finite energy, the spanning-tree existence/factor theorem in Section 8, current literature or novelty, or the marginal finite-energy calculation in Section 7. Their validity is not inferred from the historical acceptances. Lattice dimensions and symmetry/mixing depend on those separate-family inputs. The source problem and complete prior triage report were read; the latter is not a proof premise.

## Independence and method

The independent reconstruction was saved before either historical independent report was opened. Its fixed SHA-256 is recorded in the log and ledger. The later historical reports agree with the reconstruction but contribute no indispensable premise to this audit. No fresh sibling-family conclusions were read. No proof search beyond reconstructing/checking the submitted mechanism was initiated. Original effort remains 3/5; this audit adds no substantive attempt turn. No simulation, finite-volume inference, external outreach, publication, Git mutation, queue mutation, or service mutation occurred.

Success criterion: reconstruct every deterministic implication, identify a counterexample or unsupported inference if one exists, settle quantifier/measurability issues, and establish the exact scope that survives. The checkable artifact is the analytical proof below. No finite computation would certify its infinite-volume conclusions, and none is needed to test the identified failure modes.

## 1. Finite sides, unique rays, and path maxima

For t∈T, T−t has exactly two components. They cannot both be finite, since T is infinite. They cannot both be infinite: a locally finite infinite connected graph has a ray, so each would contain a ray; in a tree these rays are separated by t and represent different ends. Therefore exactly one component is finite. Call its nonempty vertex set S(t) and size s(t)∈{1,2,...}. Its T-boundary is exactly {t}.

There is one infinite simple T-ray from each vertex v. Existence follows by the elementary finite-branching argument: in the infinite tree rooted at v, one child has infinitely many descendants, and recursively one can choose such a child. If two rays from v first diverged, a tree would prevent their reunion; their divergent tails would give two ends. Write the unique ray v=v_0,v_1,... and its edges t_n={v_n,v_{n+1}}.

The finite side S_n=S(t_n) contains v_0,...,v_n; v_{n+1} lies on its infinite side. The two endpoints of every earlier ray edge lie on the finite side of t_{n+1}. Any vertex x∈S_n is connected to v_n without using t_n, and then to v_{n+1} using t_n without using t_{n+1}. Thus x lies in the component of v_{n+1} in T−t_{n+1}; this component is finite because the other one contains the infinite remaining ray. Hence S_n⊊S_{n+1}, with v_{n+1} witnessing strictness. The s_n are distinct increasing positive integers and s_n≥n+1. Therefore for every nonnegative sequence a_m,

    ∑_{n≥0} a_{s_n} ≤ ∑_{m≥1} a_m.

The strict increase matters. Merely s_n→∞ would not by itself justify this comparison with unit multiplicities.

For an ambient non-tree edge e={x,y}, connectedness of T gives a unique finite path P_T(e); simplicity ensures x≠y and the path is nonempty. Its finitely many finite positive sizes have finite positive maximum M(e). If e crosses S(t), then x and y are in different components of T−t, so P_T(e) uses t. Thus M(e)≥s(t). Every possible bypass of this finite-set cut is controlled, even if one bypass crosses many cuts.

Finally, counting incidences at vertices of S(t) gives |∂_G S(t)|≤Δs(t). No shape, diameter, isoperimetric, or growth property of the finite side is required. The global degree bound is used here and must not be silently weakened to local finiteness alone.

## 2. Measurable kernel and witness event

For a fixed finite candidate F and fixed edge t, the assertion that F is a component of an endpoint in T−t is determined by finitely many coordinates: internal T-connectivity of F after deleting t and absence of T−t boundary edges. The boundary is finite by local finiteness. There are countably many finite F, so S(t) and s(t), on their stated domain, are measurable. For fixed x,y, enumerate finite simple paths from x to y; in a tree exactly one is present. The path and its finite maximum M(e) are consequently measurable. The one-ended spanning-tree domain is Borel: connectivity and acyclicity have countable descriptions, and for every present edge one component of its removal is finite, a countable union of the finite-component tests above. Assigning rate 1/2 off this domain is measurable.

The proof's rate formulas therefore define a genuine coordinatewise measurable kernel. For any good T, each rate is strictly between zero and one. Its dependence on the whole tree causes no problem in this conditional argument.

One can also describe the full good witness event without assuming a measurable global choice of rays. Enumerate ambient edges. For fixed v,t, let B(v,t) mean: t∈T, v∈S(t), and either X_t=0 or some X-open non-tree edge crosses S(t). This is measurable by the countable finite-set description of S(t). The edges t with v∈S(t) are exactly the edges of the unique ray from v: removing t separates v from the unique end exactly in that case. Hence the statement that only finitely many B(v,t) occur is measurable, since an edge enumeration expresses it as a countable union of countable intersections. Intersect over countably many v. This is the joint good event used below. Alternatively, the ray's next edge can be measurably identified as the unique incident edge whose opposite component is infinite.

## 3. Summability and the all-vertex order

Fix a deterministic good T and v. Let D_n mean deletion of t_n, and A_n mean insertion of at least one non-tree ambient edge crossing S_n. Under the conditional kernel,

    P_T(D_n)=2^{−s_n},
    P_T(A_n)≤∑_{e∈∂_G S_n, e∉T}2^{−M(e)}≤Δs_n2^{−s_n}.

By the union bound and the distinct-size comparison,

    ∑_n P_T(D_n∪A_n)
      ≤∑_{m≥1}(1+Δm)2^{−m}=1+2Δ<∞.

The first Borel–Cantelli conclusion can be checked directly: P_T(∪_{n≥N}(D_n∪A_n))≤∑_{n≥N}P_T(D_n∪A_n)→0. Therefore with conditional probability one there exists finite N_v such that for every n≥N_v,

    X_{t_n}=1 and ∂_X S_n={t_n}.

No independence between A_n, D_n, or unions at different n has been used. A single inserted edge may affect several cuts. Only the later independent Bernoulli thinning uses independence of its own coordinates.

For fixed T, the vertex set is countable, so intersection over v retains conditional probability one. The measurable event from Section 2 has probability one for every deterministic good T, so integration against any random good-tree law gives joint probability one. This does not involve an intersection of probability-one events indexed by all trees. On the resulting single event, the retained-tail and singleton-boundary conclusions hold simultaneously for every vertex.

## 4. The retained tree and the unique final infinite component

For each v, all t_n for n≥N_v are open, giving an infinite ray tail in R=T∩X. Distinct T-rays coalesce. Indeed, the finite T-path joining their starting points together with two tails that never meet would yield two ends; once two simple rays in a tree meet on their route toward the single end, they cannot split again. Their sufficiently late retained tails therefore share infinitely many edges.

Choose one such tail and call its R-component C_R. All eventual retained tails lie in C_R. Every infinite R-component contains a ray by local finiteness. That ray is a T-ray and therefore equals the unique T-ray from its initial vertex; its eventual tail lies in C_R. Thus every infinite R-component is C_R, and C_R is infinite.

Now let v lie in an infinite X-component. For any n≥N_v, finite S_n contains v, so some finite X-path from v exits S_n (one can also take an infinite X-ray). Its first exit edge must be t_n, the only X-boundary edge. Since t_n and all following ray edges are open, **both endpoints of t_n lie in C_R**. Therefore the infinite X-component of v contains C_R. As C_R itself is infinite, X has exactly one infinite component C, the X-component containing C_R.

This excludes a proposed infinite component assembled from infinitely many finite retained-tree components using added edges: its own path out of S_n must reach C_R across t_n. Finite components of X are allowed. It is not claimed that the original vertex v is connected to its retained ray tail unless v lies in the infinite component.

## 5. Quenched bond/site thresholds and restriction to C

Fix any one good pair (T,X), with no randomness remaining in that pair. Fix v and any p∈[0,1). In Bernoulli-p bond thinning of this deterministic X, if v has an infinite component then an infinite thinned ray exits every finite S_n containing v. Hence it must use every distinct t_n with n≥N_v. For each k≥1,

    P_p^X(v lies in an infinite thinned component)
       ≤P_p^X(t_{N_v},...,t_{N_v+k−1} all retained)=p^k.

Taking k→∞ gives zero, including p=0. Countable union over all v excludes any infinite thinned component. Every p<1 is handled by the same deterministic witnessed graph and the same derivation. The full-probability event for (T,X) does not depend on p; there is no uncountable null-set interchange.

At p=1, X has C. Thus its critical parameter under the manuscript's positive-probability definition is exactly one. For v∈C, t_n lies in C because both endpoints lie in C_R⊂C, and

    ∂_C(S_n∩C)={t_n}.

The set S_n∩C is finite and contains v, even when S_n has become disconnected in X. Every C-edge leaving it is an X-edge leaving S_n, and the latter boundary is the singleton; conversely t_n is present in C and crosses it. Thus the very same quenched argument proves p_c(C)=1. In fact removing t_n separates the nonempty finite component S_n∩C from the infinite side within C, so these are genuine bridges of C.

For site thinning, an infinite site-open ray from v must traverse each t_n and retain the infinitely many distinct vertices v_{N_v},v_{N_v+1},.... The first k selected vertices are independent site coordinates and give the same p^k upper bound. This proves internal site threshold one for both X and C. Under the convention conditioning on the starting vertex being occupied, division by p for p>0 leaves the limiting zero unchanged; p=0 has no occupied infinite component.

## 6. Graph-property passage without a hidden projection assumption

The statement “a property of X alone” is mathematically valid here; it need not rely on the general projection of the good-pair event being Borel. There are two direct ways to formalize it.

First, define Q(X) by: for every v and k≥1, there are finite vertex sets F_1,...,F_k containing v and pairwise distinct edges e_1,...,e_k with ∂_X F_i={e_i}. There are countably many candidate finite certificates. Each fixed certificate is determined by the finite ambient boundaries, so Q is Borel. Every good pair produces Q via any k sufficiently late S_n. If v survives bond thinning to infinity, it must retain all k of the certificate edges, giving the p^k bound directly from Q. No witness tree needs to be recovered from X.

Second, for fixed rational p∈[0,1) and fixed v, let q_{p,n}(X) be the bond- or site-thinning probability that v connects beyond the ambient radius-n ball centered at v. The ball and its incident boundary are finite, so q_{p,n} is a finite-coordinate measurable function of X. The decreasing limit θ_{p,v}(X)=lim_n q_{p,n}(X) is the probability that v lies in an infinite thinned component; local finiteness justifies this equivalence by the finite-branching ray argument. Therefore

    ∩_{p∈Q∩[0,1)} ∩_{v∈V} {θ^bond_{p,v}(X)=θ^site_{p,v}(X)=0}

is Borel. Monotonicity extends this property from rational p to all real p<1. Existence of an infinite component is Borel by the same finite-radius tests. Uniqueness is Borel because two infinite components exist exactly when there are vertices u,v that both pass all radius tests but have no finite X-path joining them, another countable description. Intersecting these Borel properties gives a graph-only measurable event B containing the X-output of every good pair. Since the joint good event has probability one, the marginal law satisfies P(X∈B)=1. This settles the marginal quenched assertion for both bond and site percolation.

The manuscript's short witness passage is thus sound. Adding this paragraph would be an optional expository clarification, not a mathematical repair.

## 7. Adversarial boundary-case register

| Failure mode tested | Result and reason |
|---|---|
| Finite T, disconnected forest, or two-ended tree | Outside the hypotheses; finite sides or connecting paths can fail. These cannot be substituted as input. |
| G locally finite but without a global degree bound | Not certified by this estimate; Δs is essential as written. The actual lattice meets the bound. |
| S(t) has size one; U equals a rate | Rates remain strictly between zero and one. Uniform endpoint/equality events have probability zero. |
| Side sizes skip many integers | Harmless: the nonnegative-series comparison only improves. Repetition is ruled out by strict nesting. |
| G=T, so there are no non-tree edges | The A_n events are empty and the deletion/tail proof still works. |
| Very large or nonlocal finite sides | No shape/diameter assumption is used. Boundary count is by degree. |
| One inserted edge crosses many nested cuts | Max-path domination holds for each crossed cut; no cross-cut independence is assumed. |
| A path bypasses a cut using many added edges | Any exiting path has a first ambient boundary edge; all competing boundary edges are absent. |
| S_n disconnected after deletions | Only its vertex-set boundary is used. Internal connectivity is unnecessary. |
| v lies in a finite X-component | Its thinning claim is trivial; its eventual retained tail still lies elsewhere in C_R. |
| New infinite component built from finite R-pieces | It must exit S_n through t_n and join C_R. |
| Different starting vertices need different N_v | Allowed. Countably many vertices permit one simultaneous full-probability event. |
| Need all p on one realized graph | The deterministic certificate and p^k argument work for all p<1; the Borel formulation uses rational p and monotonicity. |
| p=0; p=1 | At zero all thinnings fail to percolate. At one the existing infinite C survives. |
| Cut edges leave C or finite-side pieces are lost | Both endpoints lie in C_R; ∂_C(S_n∩C)={t_n}. |
| Need a measurable T selected from X | Unnecessary; Q and B are directly Borel in X. |

## 8. Disposition, repairability, and remaining gap

No defect was identified in the assigned family. No modified kernel, quantitative estimate, added theorem, or proof-attempt turn is required. The optional exact clarifications are: state the countable description of the joint witness event in Section 4, and replace the bare graph-property sentence in Section 6 with either of the Borel formulations in Section 6 of this report. These clarify already valid implications.

The strongest verified result is the conditional theorem stated at the beginning, including all vertices, every thinning p<1, uniqueness of C, and both bond/site thresholds of X and C. Its exact remaining gap **within this family is none**. Application to the full original invariant finite-energy question still requires the separate source-scope, spanning-tree-input, symmetry/mixing, marginal-energy, and priority checks; this report does not pre-judge them. No promotion or publication is authorized or performed by this audit.
