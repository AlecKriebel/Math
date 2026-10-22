# Independent probability and input audit

PR838 / problem 10000036 / frozen head `ed2de7249953ba0c1afad253adca9b820d7297c5`.

## Decision and scope

**PASS for the assigned mathematical family, without a required proof repair.** Sections 3, 7, and 8 of the frozen author proof supply a measurable conditional product kernel, ordinary finite energy after the auxiliary tree is forgotten, full lattice-automorphism invariance, and translation mixing for every integer d>=2. Their interfaces with the one-ended-tree hypothesis and the subsequent cut argument are consistent.

This is a family-level verification, not an independent verdict on the entire PR. The original effort remains 3/5. No new central proof search, priority audit, preprint, queue/service change, Git/index/branch change, or outreach was performed. The other fresh audit results were not read.

**Source-access limit:** the exact Timár arXiv v1 theorem and factor definition were independently retrieved and inspected, including the more formal definition referred to by that paper. The publisher's version-of-record routes returned security-challenge HTML, and a normal browser visit visibly required hCaptcha. No CAPTCHA interaction was attempted. The 12-page published body was not obtained. Accordingly this report does not assert that every sentence or proof in the 10-page arXiv copy agrees with the final publication. This access limit does not contradict the precise existence theorem explicitly used in the frozen proof. A final-source comparison remains the exact source-verification gap; there is no identified mathematical gap in this assigned family.

## Independence and frozen identity

The complete private queue-show record, its prior triage report, SOURCE_MANIFEST.json, and the entire frozen author PROOF.md were read. The independent reconstruction was saved in INDEPENDENT_RECONSTRUCTION.md before the two historical audit reports were consulted. Those reports were read afterward only for comparison. No substantive conclusion from another fresh audit was consumed.

The checked author proof has 16299 bytes and SHA-256 `c31b7a1cd6a3af04807b20d58f23d79f9d07cf4eb87df26187498f3260f9891d`; this agrees with the frozen manifest. Timár and Pemantle were independently downloaded with explicit v1 URLs; both byte counts and SHA-256 values agree with the author's pins. Hash agreement establishes identity, not truth. SOURCE_READING.json records exact versions, hashes, retrieval limits, and reading/visual extents. Raw source bytes, extracts, and renders remain private and ignored.

## 1. Measurable product kernel

Work on the countable product space Ω_T={0,1}^E, where E is the nearest-neighbor edge set. Let A be the set of connected acyclic spanning trees with exactly one end. This is Borel. Connectivity is a countable intersection of countable unions of finite-path events, and acyclicity excludes countably many finite cycles. For a locally finite infinite tree, one-endedness is equivalent to saying that every present edge leaves a finite component when removed. For each specified edge and candidate finite component S, that component event can be checked using finitely many internal and boundary edge statuses. A countable union over S and countable intersection over edges completes a Borel description of A.

For fixed t and finite S with exactly one endpoint of t, the event that S is a component of T−t is a finite-edge event. On A there is exactly one such finite side. Thus the positive finite integer s_T(t) is measurable on {T∈A:t∈T}. For a fixed external edge e, the unique T-path between its endpoints is one of countably many finite simple candidate paths. Each candidate-path event is a finite cylinder event on A, and on that event M_T(e) is a finite maximum of the measurable sizes along the path. Hence M_T(e) is measurable.

Define the displayed rates on A and set all rates to 1/2 off A. The extension is Borel. Each rate lies in (0,1). The coordinate map

    Φ(T,U)_e = 1{U_e < r_T(e)}

is measurable. For every finite F⊂E and a∈{0,1}^F its conditional law is

    K(T,{x_F=a}) = ∏_{e∈F} r_T(e)^{a_e}(1−r_T(e))^{1−a_e}.

This is a consistent conditional product distribution; the independent-uniform construction realizes it. Measurability of K(T,B) for every product-Borel B follows from the finite cylinders by the monotone-class theorem. There is no unmentioned measurable-selection problem for the paths, components, or kernel.

The finite-path and finite-size assertions use connected spanning trees. A disconnected forest would leave M_T(e) undefined for ambient edges whose endpoints lie in different components. This is why the high-dimensional input distinction is substantive.

## 2. Conditional finite energy after marginalizing the tree

Fix e. Write

    H_e = σ(T,U_f:f≠e),
    G_e = σ(T,X_f:f≠e),
    F_e = σ(X_f:f≠e).

Then F_e⊂G_e⊂H_e. The independent mark U_e is independent of H_e; r_T(e) is σ(T)-measurable. Therefore

    E[X_e | H_e] = r_T(e),
    E[X_e | G_e] = r_T(e),
    E[X_e | F_e] = E[r_T(e) | F_e].

The middle identity is a direct tower-property consequence and justifies the manuscript's conditioning on both T and all other output edges. Arbitrarily much information about T revealed by those edges cannot reveal the unused mark U_e. Similarly,

    E[1−X_e | F_e] = E[1−r_T(e) | F_e].

For any integrable Y>0 almost surely and any sigma-field F, put B={E[Y|F]=0}. Then E[1_B Y]=E[1_B E[Y|F]]=0, so positivity of Y forces P(B)=0. Apply this with Y=r_T(e) and Y=1−r_T(e). Both conditional state probabilities are positive almost surely, proving

    0 < P(X_e=1 | F_e) < 1 almost surely.

The outside configuration space {0,1}^{E\{e}} is standard Borel, so the conditional probability has a Borel representative q_e of that outside configuration. The set where this representative fails to belong to(0,1) has outside marginal probability 0; redefining it there to 1/2 preserves the conditional-probability identity. E is countable, so the identities and positivity assertions for every e hold simultaneously off a single null set. These modifications are assertions about versions, not positive-mass changes to the law.

Ordinary finite energy is exactly what this reasoning proves. It does not produce a deterministic ε > 0 bounding all conditional probabilities away from 0 and 1. Nor does smallness of some tree-conditioned rates prove failure of uniform finite energy for the observable marginal. The manuscript correctly asserts neither unsupported statement. The U_e<r convention is harmless at endpoints because uniform marks have no atoms there.

## 3. Actual tree theorem and lattice hypotheses

The independently retrieved [Timár arXiv v1](https://arxiv.org/pdf/1805.10690v1), Theorem 1 on PDF page 1, states the existence of a one-ended spanning tree as a factor of independent vertex labels for an ergodic amenable unimodular random graph that has one end almost surely. It is a connected spanning-tree assertion. Corollary 2 on page2 gives the corresponding invariant-tree characterization for quasi-transitive unimodular graphs. The adjacent factor definition requires a Borel construction from independent Lebesgue vertex labels, equivariant under rooted isomorphisms.

To check the last convention rather than infer it from a bibliographic title, this audit also inspected Definition 6 on page 6 of [the primary paper Timár explicitly refers to](https://arxiv.org/pdf/1712.08210v1). Its measurable vertex-decoration rule quantifies over every graph isomorphism; one uses the same rule at each vertex. Consequently the rooted formulation describes a coherent graph decoration and does not retain a distinguished origin. Applied to the uncolored lattice graph, it respects its full automorphism group. A Cayley diagram with fixed colors/orientations would have a smaller automorphism group, but no such extra input is used here.

All theorem hypotheses hold for the deterministic rooted nearest-neighbor lattice for each d >= 2:

- It is a connected countable simple graph with degree 2d.
- Its rooted isomorphism class is deterministic, so its law is ergodic.
- For any nonnegative invariant mass transport f, translation by −x gives f(G,0,x)=f(G,−x,0). Summing over x proves unimodularity.
- Boxes have boundary-to-volume ratio tending to 0. More explicitly for invariant amenability, partition into side-N lattice cubes with a uniform residue shift in(Z/NZ)^d. The associated cut-edge process has finite components and expected removed degree 2d/N at the root. The partition law is translation invariant; averaging over the finite lattice symmetries if needed gives full invariance without changing the bound. This supplies an invariant finite-component approximation, so the appropriate random-graph amenability is satisfied.
- Removing any finite set leaves one infinite component, because the exterior of a sufficiently large box is connected for d >= 2. Thus the lattice has one end. The d=1 boundary fails this hypothesis and is not claimed.

The checked theorem does not require a finite coding radius. It requires ordinary measurable factor structure, which is enough below. The cited Timár and Pemantle results are used as established mathematical inputs. No independent complete re-proof of either paper is claimed; the audit checks actual statements, hypotheses, conventions, and applicability against the exact construction.

## 4. Full symmetry and translation mixing

For every automorphism g and every good T,

    S_{gT}(gt)=gS_T(t),
    s_{gT}(gt)=s_T(t),
    P_{gT}(ge)=gP_T(e).

Therefore r_{gT}(ge)=r_T(e). The fallback on A-complement also commutes with g. The kernel map obeys Φ(gT,gU)=gΦ(T,U). Since Timár's tree is an isomorphism-equivariant factor of vertex IID labels and the edge uniforms are independent IID, their joint input law is invariant under all lattice automorphisms. The output law has that same full symmetry, including coordinate permutations and reflections. No global random coordinate frame or retained axis is required.

For mixing, the base coordinates are indexed by V disjoint-union E. If finite coordinate supports I,J are fixed, then I and a sufficiently distant translate z+J are disjoint. Their sigma-fields are independent. For arbitrary input events A,B, choose finite-coordinate approximants A₀,B₀ with small symmetric-difference probabilities. For all sufficiently large |z|,

    |P(A∩τ_zB)−P(A)P(B)|
      ≤ 2P(A△A₀)+2P(B△B₀).

The errors tend to0, proving translation mixing of the joint vertex/edge IID field. The preimages of output events under the measurable translation-equivariant map X=Φ(F(L),U) satisfy the same formula. Hence X is translation mixing and therefore ergodic. A generic invariant mixture of tree laws would not support this inference; the actual factor input does. No finitary or quantitative mixing claim is added.

## 5. Pemantle alternative and dimension boundary

The checked [Pemantle arXiv v1](https://arxiv.org/pdf/math/0404043v1) defines subgraphs as bond configurations and finite uniform spanning-tree approximants. Theorem 2.3, PDF pages 6–8, gives the exhaustion-independent weak limit. Transporting finite approximants by an arbitrary lattice automorphism and using exhaustion-independence yields full automorphism invariance, even though the printed theorem explicitly names translations. Theorem 4.2 on page 18 gives connectedness for d=3,4 and infinitely many components for d >= 5; its proof separately explains d=2 connectedness. Theorem 4.3 on pages 21–23 states one-endedness in the lower-dimensional tree case.

Thus the alternative input is valid for 2 <= d <= 4. The higher-dimensional uniform spanning forest is not a spanning tree, irrespective of how many ends each individual component has. It cannot be inserted into the path formula on the whole lattice. The author makes exactly this distinction and uses Timár for the all-dimension factor construction. Pemantle is not being used as a substitute proof of the all-dimension mixing assertion.

## 6. Interfaces, failure checks, and exact remaining limit

The kernel supplies conditional independence of distinct edge marks after T is fixed, and all rates are positive. Subsequent summability arguments need only those rates and the deterministic one-ended-tree geometry. They do not require uniform energy or a geometric regularity theorem about the chosen tree. Full invariance and mixing depend on the input factor, while the conditional-energy calculation is valid for any law supported on good one-ended spanning trees. These hypotheses are used in the correct places.

The attempted falsifications were: nonmeasurable component/path choices; a non-Borel exceptional-input extension; revealing U_e through all other output edges; a positive variable acquiring zero conditional expectation on positive mass; incompatible all-edge exceptional sets; an unjustified uniform-energy assertion; an origin-only or Cayley-diagram-only factor; an invariant but nonmixing hidden mixture; misuse of a disconnected forest; and failure of amenability/ergodicity/one-endedness for the deterministic lattice. Each is excluded by the arguments above.

No required correction was found for this family. The exact uncompleted source task is comparison against the inaccessible final Timár publication body. This report accepts the precise arXiv theorem as the cited mathematical input and labels that publication-body limit explicitly. It does not certify priority, current literature completeness, source-side open status, or the rest of the PR. No mathematical replacement route was developed.
