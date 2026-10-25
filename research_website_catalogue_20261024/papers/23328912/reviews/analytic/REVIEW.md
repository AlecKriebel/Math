# Independent analytic review — Zenodo 23328912

**Verdict: PASS for the complete stated mathematical result, with the scope and reliance below.** No substantive mathematical defect was found. This is an AI-assisted mathematical review, not external human peer review or a proof-assistant certification. Completion: 100% of this assigned review.

## Exact object and source binding

Reviewed all six pages of *A two-cube cubulation of the AIM free-by-cyclic example*, Alec Kriebel, dated October 12, 2026, Zenodo version 1.0, DOI https://doi.org/10.5281/zenodo.23328912. The standalone published TeX was subsequently read in full and agrees with the mathematical content of the PDF. The three fresh public inputs were independently rehashed, and every one of the 28 extracted regular files was checked byte-for-byte against its ZIP member. Neither archive contains another PDF. Detailed member commitments are in `source-binding.json`.

| Asset | SHA-256 |
|---|---|
| aim_5_2_two_cube_cubulation.pdf | 3dfdfca7c0b9d41c54ed03dc9500afd8d8013fef2ebd589b2806712f84781841 |
| aim_5_2_source.zip | a244ddbbbb0f7ca6d9ca073d21589bef1e9c0a98a404daaca195ee9fc87f6935 |
| aim_5_2_verification.zip | 8ff6e88f6d4a539680667b22931e080365dfd905dd64f795f408e23cc7bb8f01 |

The exact group is

\[
G=\langle a,b,c,t\mid tat^{-1}=a,\ tbt^{-1}=ab,\ tct^{-1}=bcb\rangle.
\]

The final occurrence of (b) is positive. The automorphism has inverse (a\mapsto a, b\mapsto a^{-1}b, c\mapsto b^{-1}acb^{-1}a); substitution in both orders freely gives the three basis letters. The target is the entire marked group (F_3\rtimes_\phi\mathbb Z), not a finite-index subgroup, a quotient, or an unmarked nearby presentation.

The strongest verified claim is exactly Theorem 1: a finite general unit cube complex (Z), of dimension three and cell counts ((1,7,8,2)), is locally CAT(0) and has fundamental group (G). Its universal cover is a CAT(0) cube complex on which the full group (G) acts freely, properly, and cocompactly by cubical isometries. The auxiliary Section 5 deduction from earlier tools also has its stated hypotheses satisfied. Counts apply to the general face-identification quotient before subdivision. No minimum dimension or number of cells, virtual specialness, absolute priority, or historical firstness is established or needed.

## Independence and evidence ordering

I read the actual published PDF and reconstructed the attaching maps, links, group changes, geometric action and auxiliary argument before opening the three supplied helper programs or their driver. `fresh_controls.py` was written and run first; `fresh_controls.json` records 68 successful exact guards and the actual links, triangles and product words. No sibling review findings or dedicated historical assessment bodies were read.

Subsequent necessary helper inspection exposed their inline historical labels, PASS/status strings, claims of independence, names of assessment files, and hashes of those files. The driver reads saved numerical baselines and hashes historical prose; it does not establish the truth of that prose. I did not read the bodies of `BUNDLE_REPORT.md`, `PUBLICATION_ADDENDUM.md`, `ATTEMPT_1.md`, `SOURCE_GATE.md`, historical `RESEARCH_LOG.md`, `AUDIT.md`, or `AUDIT_RESULT.json`. The manuscript's own retrospective audit/disclosure statements were unavoidable manuscript content. These exposures are not independent corroboration and are not used as premises. Raw reference paths/receipts were supplied by the scope family, without mathematical conclusions.

## Reconstruction of the explicit cubical model

### Base complex and involution (pages 2–3)

Use capital letters for inverse oriented edges. The base (K) has squares (xyXY) and (bxBY). Deriving every corner as the pair consisting of inverse incoming and outgoing germs gives four edges joining (x^\pm) to (y^\pm), two joining (b^-) to (x^\pm), and two joining (b^+) to (y^\pm). There are no repetitions or loops. This is the claimed simple bipartite six-vertex, eight-edge graph. Its absence of triangles makes it flag, so (K) is locally CAT(0).

The map (lambda(x)=y,lambda(y)=x,lambda(b)=B) genuinely extends over the squares. The first square boundary maps to its reflected parameterization; the second maps to a rotation of its inverse parameterization. Enumerating the dihedral maps of each four-sided boundary gives unique reflections (j\mapsto -j) and (j\mapsto 1-j), respectively, under the chosen indexing. Both square to the identity and agree with the edge assignments. Thus the extension is a cubical isometric involution, not only an automorphism of the presentation.

The domain (Q) has distinct vertices (A,B,C,D), edges (p:B\to A, q:A\to C, r:D\to C, s:B\to D, d:A\to B, e:C\to A), with labels (x,y,x,y,b,b). Its squares are (pqRS) and (dpEQ), with vertex cycles ((B,A,C,D)) and ((A,B,A,C)). They are closed, and their label words are the two actual base square boundaries.

The complete domain links, retaining both occurrences of (A) in the second square, are

- (A: e^- — p^- — q^+ — d^+);
- (B: d^- — p^+ — s^+);
- (C: r^- — q^- — e^+);
- (D: r^+ — s^-).

Under (j), their vertex sets are, respectively, ({b^-,x^-,y^+,b^+}), ({b^-,x^+,y^+}), ({x^-,y^-,b^+}), and ({x^+,y^-}). Their listed edges are exactly the induced base-link edges on these sets. Each map is injective, and the same assertion after (lambda) follows either directly or from the base-link automorphism. All eight endpoint link maps were checked explicitly. Hence both maps are cubical local isometries. There is no unfilled triangle in a domain link.

The tree (p,q,s) collapses the first square to the relation (r=1) and the second to (d=e). Therefore (pi_1(Q,A)) is infinite cyclic generated by (dp), with images (bx) and (By). In the base group, the homomorphism sending (b\mapsto1) and (x,y\mapsto0) proves (bx) has infinite order; the same holds for (By). Thus neither edge-group map loses a power or a kernel.

### Actual quotient and link multiplicities (pages 3–4)

Take the genuine product (Q\times[0,1]), attaching its two ends by (j) and (lambda j). This produces four distinct vertical edges, one per vertex of (Q), although all endpoints lie at the sole base vertex. The repeated (A) in the second square yields two boundary positions of the same vertical edge in the second cube; this is permitted by the declared general cube-complex convention. It does not identify distinct cube interiors or impose an extra relation.

The cells are exactly one vertex, three base plus four vertical edges, two base plus six product squares, and two product cubes. In particular the number of vertical edges is four, not the number six of domain edges. The Euler characteristic is zero.

The unique vertex link has the six base germs and eight distinct vertical germs (z_v^\pm). Each vertical germ is the apex of the cone over the corresponding full endpoint-link image; no two vertical germs are adjacent. Its actual square-corner occurrences yield 32 distinct edges, not just a set obtained after ignoring multiplicities. Its actual cube-corner occurrences yield 16 distinct nondegenerate triangles. The two (A)-corners of the second square have different base edges, ({d^+,q^+}) and ({p^-,e^-}); consequently the corresponding triangles are different. The first square contributes ({p^-,q^+}). This checks the possible repeated-corner failure directly.

Every triangle has its three actual faces, no simplex is repeated, and the link is a simplicial complex. Every clique with no vertical apex lies in the flag base link. Every other clique contains exactly one apex and has all other vertices in its full base; fullness and the base flag condition fill that clique in the cone. Thus the link is flag by a written argument, with counts ((14,32,16)) and no four-clique as a separate exact control. Deleting either repeated (A)-corner triangle in the fresh controls is detected as a missing flag simplex. The existence of two cubes does not by itself prove flagness; their corner incidences do.

Leary's general-complex Theorem C.9 is applicable to this actual flag simplicial link and gives the local CAT(0) and universal-cover conclusion. His Theorem C.4 supplies the stricter embedded-cube property of the CAT(0) cover; his Corollary C.11 permits a strict quotient after second cubical subdivision. Neither theorem licenses retaining the original cell counts after subdivision, and the manuscript correctly does not do so.

## Exact fundamental group and action (page 4)

For each edge (h:u\to v) of (Q), its product square has word (j(h)z_v\lambda(j(h))^{-1}z_u^{-1}). Deriving these directly gives the six displayed relations, including the positive (b)'s caused by (lambda(b)=b^{-1}). The three-cells do not change the fundamental group.

Put (z=z_A). The (p,q,s) relations solve for

\[
z_B=xzY,\qquad z_C=Yzx,\qquad z_D=YxzYx.
\]

These are generator eliminations with inverses. The (r) relation becomes redundant because (xy=yx). The (d) relation gives (z^{-1}(bx)z=By). The (e) relation gives (z^{-1}(yb)z=xB), the same relation since (yb=bx) and (xB=By). Thus the whole two-skeleton has exactly the presentation

\[
\langle x,y,b,z\mid xy=yx, bxB=y, z^{-1}(bx)z=By\rangle.
\]

The free generator substitutions (t=x, a=xY, c=(zx)^{-1}) have inverse (x=t, y=a^{-1}t, z=c^{-1}t^{-1}), with (b) fixed; both compositions freely reduce to the respective four generators, without using a relation. The first two relations become ([a,t]=1) and (tbt^{-1}=ab). For the third set (u=Bx,v=bx); the base relation gives (By=xB=xuX). Then

\[
z^{-1}vz=xuX
\Longleftrightarrow (zx)u(zx)^{-1}=v
\Longleftrightarrow c^{-1}(b^{-1}t)c=bt
\Longleftrightarrow tc=bcbt.
\]

Every step is reversible. This proves the group is exactly the specified semidirect product, not merely a group mapping onto it. The separate normal-form control evaluates all eight original two-cell words in that exact semidirect product and confirms the inverse monodromy. It also rejects a negative-final-(b) variant. Those computations are corroboration of, not a replacement for, the two-way presentation argument.

The cover has dimension three, unit Euclidean cube shapes and finite links, hence is locally finite and locally compact. Finite dimension excludes infinite ascending cell chains, so its natural length metric is complete (also directly covered by Leary Appendix A/Theorem A.6). The CAT(0) cover is geodesic; the complete locally compact length-space properness theorem makes it proper. The deck action is free and cubical, with the usual covering-space proper discontinuity. For compact-set properness, take compact sets in the proper cover and use finite covering neighborhoods: infinitely many intersecting translates would, after compact subsequences, contradict the evenly covered neighborhoods. The finite quotient makes the action cocompact. Properness is therefore justified, not inferred just from freeness.

## Auxiliary existence proof (page 5)

This part is independently valid at the stated qualitative level; it is unnecessary for the explicit two-cube proof and gives no cell-count bound beyond dimension at most three.

The base group is an HNN extension of the embedded (A_0=\mathbb Z^2), with (bxb^{-1}=y). In its Bass–Serre tree choose the edge from (A_0) to (bA_0), stabilized by (langle y\rangle). For (g=bx), the translates (g^ne) concatenate, their height increasing by one. They form a bi-infinite geodesic axis. The incoming and outgoing edge stabilizers at (A_0) are (langle x\rangle) and (langle y\rangle), whose intersection is trivial in the embedded (mathbb Z^2). Thus two axis vertices have finite (indeed trivial) pointwise stabilizer. The corrected Minasyan–Osin Corollary 4.3 supplies WPD for this loxodromic element; no global acylindricity or finite-extension theorem is assumed.

Dahmani–Guirardel–Osin Corollary 2.9 and the one-element instance of Theorem 6.8 then give a virtually cyclic hyperbolically embedded (E(g)). The height homomorphism proves (g) has infinite order. The finitely generated group (H), infinite-order (g), and virtually cyclic (E(g)) meet Sisto Theorem 1's exact hypotheses. Its Morse conclusion implies word-metric quasiconvexity of (C=langle g\rangle).

The required metric is the edge metric on the Cayley graph (widetilde K^{(1)}), since (K) has one vertex and generators (x,y,b). The lifted two-edge loop reading (bx) contains (C) and stays within one of it. A geodesic between points of this lifted image can be extended by paths of length at most one to endpoints in (C). The extended path is a uniformly quasi-geodesic (for example additive constant four suffices); the Morse property bounds its distance from (C). Thus the actual lifted graph is quasiconvex in precisely the combinatorial metric used in Ben-Zvi–Kropholler–Lyman Theorem 5.1. No conversion from CAT(0)-metric quasiconvexity is smuggled in.

Their Theorem 1.1 and finite-completion Theorem 5.1 produce a finite local-isometry completion with exact fundamental-group image (C). Injectivity preserves the generator (bx), rather than replacing it with a power. The original circle alone is not a local isometry: its intermediate germs (b^-,x^+) bound a base-link edge absent in the circle link. This is independently detected by the fresh control. Completing first and postcomposing with (lambda) gives compatible maps on the same domain.

The product construction over that finite domain has the same full-link-cone argument, so it is a finite locally CAT(0) complex. A local isometry into the two-dimensional (K) has domain dimension at most two; its cylinder has dimension at most three. Van Kampen again gives the same HNN presentation with stable letter along the interval at the basepoint. This proves another proper cocompact action of the full (G). Hagen–Wise Remark 3.7 discusses precisely compact vertex/edge spaces attached by local isometries. Their Corollary 7.2 alone promises a free CAT(0) cubical action; the manuscript correctly does not present that alone as proper cocompact cubulation of this group.

## Primary references and attribution limits

I read the actual relevant statements and nearby definitions/proof passages in the following primary bodies. `primary-bindings.json` records their exact paths, URLs, bytes and freshly verified SHA-256. Standard imported theorems are accepted as published mathematical inputs; I did not independently reprove all 157 pages of DGO or all underlying geometric group theory.

- [Leary, accepted v3](https://arxiv.org/pdf/1009.1540v3): general/strict conventions, Theorem C.4, Theorem C.9, Corollary C.11; Appendix A completeness and Theorem A.6. The distinction is essential for the quotient counts.
- [Ben-Zvi–Kropholler–Lyman, v1](https://arxiv.org/pdf/2011.05374v1): Theorems 1.1 and 5.1; injective-full-link definition and Proposition 2.1. Finite graph and finite base, the prescribed generating set, and exact subgroup image are checked.
- [Minasyan–Osin, corrected v6](https://arxiv.org/pdf/1310.6289v6): Corollary 4.3's tree, axis and finite pointwise-stabilizer hypotheses, not an uncorrected theorem or an unrelated finite-extension claim.
- [Dahmani–Guirardel–Osin, v5](https://arxiv.org/pdf/1111.7048v5): WPD/loxodromic definitions, Corollary 2.9 and Theorem 6.8. The single element case makes pairwise noncommensurability vacuous.
- [Sisto, v1](https://arxiv.org/pdf/1310.7753v1): Morse definition and Theorem 1, including finite generation and infinite order.
- [Hagen–Wise, v3](https://arxiv.org/pdf/1605.07879v3): Remark 3.7 and Corollary 7.2. The latter's free-action conclusion is not enlarged.
- [AIM workshop report](https://aimath.org/pastworkshops/freebycyclicrep.pdf), page 2: the related example uses (b\mapsto aba), unlike the present exact target.
- [Archived original AIM Question 5.2](https://web.archive.org/web/20240828224508id_/http://aimpl.org/freebycyclic/5/): the HTML gives Lyman's question with (a\mapsto a,b\mapsto ab,c\mapsto bcb) and asks for a proper cocompact CAT(0) cubical action. SHA-256 `9dfa1624c5743d114c671ea69201a9ea46fe577e707239e245cc7f22b30b8121`. The fresh live endpoint attempts timed out; this authenticates the historical question, not its current status or continued openness.

The manuscript explicitly credits the earlier tools and explicitly avoids historical-firstness claims. Its retrospective bounded-source-audit statement was not independently reproduced as a comprehensive literature search. Nothing in this review authorizes advertising a new general cubulation theorem, a minimum-size model, or external human validation.

## Reproduction and falsification controls

The fresh script, made before helper inspection, uses only exact integers, finite incidence counters, free reduction and semidirect normal forms. Its 68 guards cover square closure, actual multiplicities, all eight full endpoint links, genuine dihedral involutions, the complete actual 14-vertex link and 16 cube-corner triangles, absence of four-cliques, cell counts, repeated-corner omission controls, nonlocal-isometry of the raw (bx) circle, two-sided monodromy inverse, all original two-cell relators, free inverse changes of generators, and the positive-final-(b) control. The JSON preserves the explicit constructions so its assertions can be independently inspected.

After that independent work, I read all three supplied helper bodies and their complete driver. The dependency-free driver was then executed unmodified from a disposable copy in the ignored review cache, using Python 3.14.6 with isolated/site-free/no-bytecode flags and a working directory outside the bundle. It exited 0 with empty stderr. The source bundle and replay input retained their original hashes.

The driver performed six clean baseline program runs (three programs in normal and optimized modes), deleting saved outputs before each. Geometry and algebra regenerated the exact expected artifact bytes. It then rejected three SHA tamper fixtures and fourteen mutated-program/proof-pin executions (seven mutations in both modes), including duplicate square, nonclosed face, wrong involution sign, omitted cube triangle, wrong vertical sign and wrong inverse monodromy. A relocated full bundle with spaces in its path was run by an optimized driver and repeated six clean program runs. These are 12 successful baseline program executions plus 14 expected failure executions and three integrity rejection controls; they are not 29 independent mathematical proofs. The public geometry's 17 internal negative controls are additional bundled checks, not newly independent discoveries.

`published-replay.stdout.json`, its empty stderr file and `published-replay-receipt.json` preserve the result. The driver's historical proof hashes only bind bytes; they do not endorse historical assessments. The normal-form programs establish the forward mapping; the reversible written derivation above supplies the isomorphism. Finite checks do not prove the global CAT(0), completeness, properness, completion, or historical-priority assertions on their own.

## Exact gaps and disposition

No substantive gap remains in the stated theorem or its auxiliary qualitative deduction, relative to the checked standard theorem imports. No repair was made or proposed. The mathematically supported result is the full explicit general-quotient construction and geometric action, with the stated pre-subdivision counts, and the target-specific existence deduction from prior tools.

Remaining limitations are epistemic and scope limits, not a silently weakened theorem: this is AI-assisted proof review rather than formal certification or external human peer review; imported primary theorems are accepted; no exhaustive novelty or current-open-problem-status audit was performed; and no minimality, virtual specialness or global generalization is claimed. Follow-up questions are not needed for this review and none are proposed.
