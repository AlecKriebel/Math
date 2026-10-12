> Editorial scope: This is the complete authored text of the accepted third-round source document, with operational identities and reproduction directions editorially removed or relabeled. Mathematical arguments and finite-scope counts are preserved. References to candidate status, packet contents, or narrower review scope record the original stage; the final combined decision is in [ACCEPTANCE_REPORT.md](ACCEPTANCE_REPORT.md). This public edition contains prose and public verification metadata only. It contains no programs, raw certificates, dataset contents, source documents, or runnable bundle. Original and distributed identities are different; [PUBLIC_MANIFEST.json](PUBLIC_MANIFEST.json) identifies only the files actually distributed.

# Mixed signed list dependency and application audit

12 October 2026 UTC. Scope: the signed reductions in Section 2 and positive boundary theorem in Section 3 of the third-continuation mixed prescribed Clebsch-class candidate for problem 3209, queue row 1752.

## Verdict and exact scope

**PASS for the inspected external statements, conventions, and their use in the mixed boundary theorem.** The argument correctly uses non-symmetric four-color lists at boundary entities, eight-color lists elsewhere, and a maximum auxiliary degree of four at every boundary entity. No missing case was found in the end-block argument or its return to the cube.

The original mathematical report was inspected against its exact frozen identity, which is retained outside this edition. Its final dependency set is Theorem 2.1(a),(c),(e) and Lemma 2.4. The author’s packet manifest was externally pinned to identify the candidate packet; that original identity is retained outside this edition and does not expand this audit into acceptance of every listed artifact. Sections 2–3 and the dependency simplification were reread before sign-off.

The signed list results remain explicit external mathematical assumptions. This audit reads their primary source and checks the candidate's application; it does not independently re-prove the source theorem. It also does not accept all of the candidate's obstruction proofs, programs, maximum-cut enumerations, witness computations, or provenance statements. A separate full-packet audit is needed for those claims. Neither this audit nor the positive theorem resolves the Weak pentagon conjecture or every globally maximum prescribed cut. No novelty or exhaustive literature claim is made.

No candidate file was edited. No remote state was changed. Source PDF, extracted source text, and source-page images are excluded from the public audit artifacts.

## Primary source and dependency contract

Thomas Schweser and Michael Stiebitz, [Degree choosable signed graphs, arXiv:1507.04569v1](https://arxiv.org/abs/1507.04569v1), submitted 16 July 2015. The [21-page primary PDF](https://arxiv.org/pdf/1507.04569v1) has 202,056 bytes and SHA-256 `727b9d254300f36b91c7ff2e02e1538c259ff0075316da2dfffb454ee2da960e`.

The relevant source contract, paraphrased: graphs are finite loopless multigraphs, degree counts multiplicity, colors are integers, and signed coloring forbids c(u)=sigma(uv)c(v). Lists need not be symmetric. An uncolorable pair is connected, has lists at least as large as vertex degrees, and has no list coloring. Theorem 2.1(a),(e), pp. 7–8, forces equality and brick blocks. Theorem 2.1(c), p. 8, propagates lists across each edge of an uncolorable block by its sign. Lemma 2.4, pp. 13–14, decomposes an uncolorable pair into uncolorable block-list pairs whose incident block lists unite to the original list. Switching reverses cut signs and negates switched lists and colors.

All 21 pages of the primary PDF were read in extracted text. Pages 8, 12, and 13 were also rendered and visually inspected. Theorem 2.1's proof and Lemma 2.4's proof were read. Lemma 2.2(b) was also inspected as background; its proof is expressly left to the reader in the source. The final candidate does not rely on Lemma 2.2: Theorem 2.1(c) already gives the needed doubled-brick contradiction. The audit uses v1's numbering; the journal full text was not inspected. the retained public-source inspection metadata records the public inspection and retrieval metadata.

## Application checks

### The auxiliary graph and its degree convention

Let G be finite, simple, triangle-free, and subcubic, with matching cut complement M. Exactly one M-edge rs lies in Y. An auxiliary entity is one X-edge of M or one unmatched X-vertex. Only ordinary vertices y in Y outside {r,s} generate neighbor-pair constraints.

If two distinct X-neighbors of such a y were the same entity, they would be the endpoints of an M-edge and form a triangle with y. Thus the constructed signed graph F has no loops. At a degree-three y the three neighbor entities are distinct.

Multiplying the signed coloring inequality by epsilon_x gives exactly the prohibition on antipodal cube images. Same-sign parallel copies impose the same inequality and can be deduplicated. Opposite-sign parallel copies impose two different inequalities and must both be retained. Their contributions both count toward degree. Deduplication never removes the last copy of a generated signed constraint. All subsequent degree and cycle arguments use this multigraph convention.

### Boundary prescriptions really are four-element lists

Write R=N_B(r), T=N_B(s). Triangle-freeness gives R intersect T empty, and neither set contains both endpoints of an X-demand. If both endpoints of one entity appear in R union T, they therefore appear one in each set. Their epsilon signs are opposite and their t signs are opposite, so t_x epsilon_x agrees for both prescriptions. A boundary entity consequently receives exactly D or -D, where D={1,2,3,4}; it never receives an unexamined intersection or an empty list. Every other entity receives C=D union -D.

The lists are subsets of the ordinary integers. D and -D are disjoint, nonempty, and non-symmetric. Zero is absent. No symmetric-list hypothesis is being silently imposed on the four-color lists. The endpoint degrees of rs give at most four boundary incidences and hence at most four boundary entities, although the final local end-block proof does not rely on that count.

### Switching and palette relabeling

Changing the chosen orientation of an entity by a sign q_P transforms its incident edge signs to q_P sigma(PQ) q_Q, its list to q_P L(P), and its color to q_P c_P. This preserves both admissible colors and every inequality. In particular, switching a boundary entity exchanges D with -D; one cannot switch only the graph while keeping its four-color list fixed. The candidate does not make that mistake. Cycle products are preserved by switching, since each vertex factor occurs twice.

For the alternative full-palette reduction, independently exchanging +i with -i for each absolute color i is a bijection psi of C satisfying psi(-a)=-psi(a). Hence c_P=sigma c_Q holds exactly when psi(c_P)=sigma psi(c_Q). If the transformed boundary roles contain no opposite pair, these independent exchanges put every occurring role in D simultaneously. Repeated roles and absent absolute colors cause no problem. Two roles of one entity have the same a-sign, so a same-entity added condition only forbids a nonzero color from equaling its own negative and can be omitted. This validates the equivalence claimed in Proposition 2.2; it does not grant a degree-eight theorem for F-plus.

### Exact equivalence with the prescribed cube extension

In the forward direction, entity lists supply adjacency to fixed antipodal odd images h and h+J for r and s. Other Y-vertices have at most three X-neighbors, and all pairs of their images avoid antipodes by the signed constraints. The elementary cube lemma therefore supplies an image for each ordinary Y-vertex independently. There are no other Y-demands, so this independence introduces no unsatisfied coupling.

For the reverse direction, along each G-edge the parity difference between a prescribed cube map and the specified cut parity is constant: both change on B-edges, and neither changes on M-edges. A componentwise translation makes all X-images even. In the component containing rs, f(r) and h are now odd, so their difference is even; a further even translation normalizes f(r) to h without disturbing the X parity. It also normalizes f(s) to h+J. The inverse of theta and the entity signs then recover the stated lists and signed inequalities. Other G-components have no boundary constraints. This handles disconnected graphs and isolated vertices as well.

### Every vertex satisfies the degree-list hypothesis

For an entity P define the pre-deduplication count

T(P)=sum over x in P, y in N_B(x) outside {r,s} of (d_B(y)-1).

There are no generated loops, so this counts all incident constraint copies. Thus d_F(P) is at most T(P). If k is the entity's number of incidences with {r,s}, the subcubic and matching hypotheses give T(P) at most 2(3-k) for a singleton and 2(4-k) for a pair. These are upper bounds even when different incidences generate the same signed edge.

An unconstrained entity has an eight-element list and degree at most eight. The theorem expressly assumes boundary degree at most four, matching its four-element list. Thus each uncolorable connected component K satisfies the external degree-list hypothesis. Theorem 2.1(a) forces d_K(P)=|L(P)|, and componenthood gives d_K(P)=d_F(P). Every vertex of K consequently has degree four or eight. Degree four means boundary; degree eight means an unconstrained pair because an unconstrained singleton has degree at most six. An isolated vertex cannot belong to such a K.

### Block palettes and cut vertices

Apply Lemma 2.4 to (K,L) before invoking properties of an uncolorable block. It supplies lists L_Q on each block Q. At a vertex in only one block, L_Q(P)=L(P). At a cut vertex that equality is generally false; only the union over its incident blocks is guaranteed.

The block lists are in fact pairwise disjoint at each vertex. Theorem 2.1(a) applied to K and to each (Q,L_Q), together with the partition of incident edges among blocks, gives

|L(P)|=d_K(P)=sum over incident Q of d_Q(P)=sum over incident Q of |L_Q(P)|.

Since their union is L(P), equality of finite cardinalities rules out overlap. This justifies the palette-splitting interpretation without assuming that any one block receives all of C at a cut vertex. The candidate uses inherited original lists only at non-cut vertices, exactly where it may.

### End blocks of degree eight

Choose an end block Q, or K itself if there is just one block. A non-cut vertex of Q has its full K-degree in Q. Since Q is a regular brick, its degree is four or eight. If Q has degree eight and has a cut vertex, that vertex has eight incident edges within Q and at least one outside Q, contradicting the global degree bound eight. Therefore K=Q is a single eight-regular brick. Only balanced K9 and signed 2K5 have this degree.

Every entity is then an unconstrained pair. Equality in d_F(P) at most T(P) at most eight forces both represented X-vertices to have exactly two ordinary Y-incidences, every adjacent ordinary y to have B-degree three, and no incident same-sign duplicate deletion. In particular there are no incidences to r or s. If y is adjacent to the represented set, its generated signed edges keep all three neighbor entities in K, even after deduplication. This verifies the required component closure.

For three neighbors x,z,w of such a y, the generated triangle has sign product

(-epsilon_x epsilon_z)(-epsilon_z epsilon_w)(-epsilon_w epsilon_x)=-1.

In a supposed balanced K9 the relevant edges are the unique edges on those pairs, so this contradicts balance, in any switching representative. In a supposed 2K5 there are five pairs and ten represented X-vertices. Their ordinary B-degree is two, so there are twenty incidences. Closure says every adjacent ordinary Y-vertex has all three neighbors among those ten vertices, giving 20=3|N_B(X_K)|, impossible. This count is in the original bipartite cut graph, not in F.

### End blocks of degree four

Every non-cut vertex P of such a Q is boundary, so L_Q(P)=L(P) is D or -D. In either doubled degree-four brick type, 2K3 or a doubled odd cycle, choose a neighbor P-prime of a non-cut vertex P. The two parallel edges have opposite signs. Theorem 2.1(c) applied to (Q,L_Q) therefore gives L_Q(P)=L_Q(P-prime) and L_Q(P)=-L_Q(P-prime). Thus L_Q(P) is symmetric, contradicting D or -D. This directly excludes the doubled types without using Lemma 2.2 or assuming anything about the original list at P-prime. The remaining degree-four brick is a balanced K5. Cycle bricks of degree two and bridges of degree one cannot occur as the chosen end block because a non-cut vertex would then have K-degree one or two.

Let P be a non-cut vertex of this putative K5. Since P is boundary, a paired P has at most three ordinary Y-incidences and a singleton P has at most two. If every ordinary Y-neighbor had degree at most two, each incidence would contribute at most one auxiliary constraint, giving d_F(P) at most three. Its actual degree is four. Hence at least one adjacent ordinary y has degree three.

Its three distinct neighbor entities generate a negative-product triangle. Both generated edges at P survive same-sign deduplication. All edges incident with the non-cut P belong to Q. The two other triangle vertices consequently belong to Q as well, and the third generated edge closes a cycle in the same block. Equivalently, adding an edge between vertices of a block cannot put that edge into a separate block. An opposite-sign parallel copy would likewise belong to this same block; it cannot be hidden outside Q. Thus Q contains the negative-product triangle, contradicting its balance.

This local exclusion is valid without counting how many boundary entities different end blocks consume. It also avoids any assumption that the palette at the possible cut vertex equals its original eight-color list.

## Boundary sharpness check and stopping point

An independent reconstruction of F from the authored 18-vertex graph gives five entity degrees (5,5,5,5,8), with the first four entities boundary and each receiving four colors. the original boundary-degree receipt pins that graph input and records this limited check. The independent the original boundary-degree checker reproduces the same JSON under normal Python, -O, and -OO. It is not a second verification of UNSAT or maximum cuts.

Those four entities violate the degree-list hypothesis. The positive proof therefore makes no assertion about that example. It cannot be extended to degree five at those four boundary vertices by this theorem. Claims about more general deficient-list patterns, the 4+1 distribution, or globally maximum cuts need additional arguments.

## Source notation observations

The primary v1 contains minor notation slips already relevant to careful reading: the edge-sign map's displayed domain on p. 2, L(v) instead of L(u) in the p. 7 deletion formula, and a missing adjacency qualifier in Theorem 2.1(b). In Lemma 2.4's induction paragraph on p. 13, the block-family subscript in the formula for L2 must refer to G2 rather than G1. Its surrounding induction, lemma statement, and palette-union conclusion are unambiguous. None of these slips is imported into the candidate's argument.

The short bound |C_i| at most d_Gi(v) in that proof is a legitimate contrapositive use of Theorem 2.1(a): all other vertices already meet their degree bounds; if |C_i| were larger, the uncolorable pair would contradict exactness. This does not assume degree feasibility at v before it is established.

## Final conclusion

The checked mixed reduction and positive boundary argument are valid assuming the cited external signed degree-list results. The new clauses were inspected directly in the full primary source, not inferred from the earlier one-sided audit. The candidate respects the distinction between original lists and block palettes, keeps opposite-sign multiplicity, and establishes the component closure and negative-cycle exclusions needed for its end-block argument. No independent reproof of the external theorem or acceptance of unreviewed packet claims is asserted.
