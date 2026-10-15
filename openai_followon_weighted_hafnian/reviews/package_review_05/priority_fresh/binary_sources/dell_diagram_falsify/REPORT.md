# Primary-only reconstruction of Dell Figure 3

Prepared 2026-10-07 06:35:24 UTC. This is a bounded primary-source reconstruction, with no verdict about an unseen candidate's novelty.

## Inspected evidence

- **2010:** Holger Dell, Thore Husfeldt, Martin Wahlén, *Exponential Time Complexity of the Permanent and the Tutte Polynomial*, ECCC Report 78 (2010). Actual local PDF `/Users/alec/Documents/Math/openai_followon_weighted_hafnian/reviews/package_review_05/priority_primary/primary_reading/binary_independent/dell2010eccc.pdf`; SHA-256 `c2675fb000d7e87e902ec782cdc7ee7becf18b14cb46cb93534a1f9dddb21ae4`. Directly inspected relevant printed pp. 7–10 and Fig. 3 on p. 8; a whole-document text extraction was also attempted, but truncated and is not a certificate of full reading.
- **2012:** Holger Dell, Thore Husfeldt, Dániel Marx, Nina Taslaman, Martin Wahlén, same title, ECCC Revision 1 of Report 78 (2010), dated June 2012 in the actual PDF. Local PDF `/Users/alec/Documents/Math/openai_followon_weighted_hafnian/reviews/package_review_05/priority_fresh/binary_sources/primary_reading/dell_eccc2012_revision1.pdf`; SHA-256 `1562a744508dc2da2a080d73253e5a70a698544cc28a49053beaa4a6c5a53636`. Directly inspected printed pp. 1–3 and 9–14, including Fig. 3 on p. 12.
- Direct renders of the primary pages are in ignored `primary_reading/`: `dell2010-p8.png`, `dell2012-p12.png`, `dell2010-fig3-right.png`, `dell2012-fig3-right.png`. The last two are 400-dpi crops generated directly from those PDFs.
- Other files read: only `/Users/alec/Documents/Math/AGENTS.md` and `/Users/alec/Documents/Math/openai_followon_weighted_hafnian/research/USER_REQUEST.txt`. No candidate, README, previous review, research note, source summary, receipt, source TeX, or other literature was read.

## Literal sink-loop finding

**There is no sink self-loop in either actual Figure 3 right panel.** The 2012 right panel explicitly draws the terminal vertex circles at u and v; the 2010 right panel labels those interface positions without circles. At v in 2012, incoming arrowheads converge on the plain circle. The curved mark below it is the italic label v. Every genuine loop in the right panel is above an internal chain vertex and has its own curved arc and arrowhead. The left panel likewise acquires explicit terminal circles in the revision; its only loop is at the fresh internal vertex.

This distinction is mathematically material. A hypothetical extra loop at the sink cannot simply be ignored in the cycle-cover application. For the one-vertex input consisting of a loop of weight a, identifying the gadget terminals u=v makes any added sink loop an extra unit-weight cover, changing the answer from a to a+1. The actual primary diagram does not create that issue.

An independent internal subagent subsequently inspected each actual full figure page without reading this report or other-agent artifacts and reached the same literal verdict: terminal circles were added in 2012, but there is no oval loop or loop arrowhead at v. Its bounded task did not reconstruct the full reduction or prove the matching signature.

## Reconstructed graph and paths

Let a>0 have binary expansion a=sum_{i=0}^k a_i 2^i, a_i in {0,1}, a_k=1. Interpret the right panel's top chain as c_0=u, c_1,...,c_k. Its edges are:

1. c_{i-1}->c_i of weight 2, for i=1,...,k;
2. a unit loop c_i->c_i for every i=1,...,k;
3. c_i->v of weight a_i for i=0,...,k, omitting an edge when a_i=0.

There are no other drawn edges or loops. In particular u has no drawn incoming arc and v has no drawn outgoing arc before gluing to the surrounding graph.

The left panel implements each weight-2 arc x->y by x->y, x->h, h->y, plus the unit loop h->h at a fresh h. If the arc is used, the two alternatives are the direct arc (with h on its loop) or the two-arc route through h. If it is unused, h must use its loop. Thus it contributes a factor 2 only in the used state.

After applying that left gadget to every top-chain arc, delete the internal loops temporarily and call the remaining directed graph D. D is a DAG: order u first, then each h_i immediately before c_i, and v last. Every u-v path exits at exactly one c_i. If a_i=1, reaching c_i involves i independently chosen direct-or-via-h routes, hence 2^i paths. Therefore

    #paths_D(u,v) = sum_i a_i 2^i = a.

The graph has 2k internal vertices and 3k+popcount(a) nonloop arcs. Reinstating its 2k internal loops makes the entire diagram a directed graph with loops, rather than literally a DAG; it is the nonloop part D that is acyclic. For a=1, k=0 gives only u->v. For a=0 the replacement is deletion of the original zero-weight arc, rather than a logarithm-of-zero construction.

## Cycle-cover extension and exact interface

The sources define the permanent of a weighted directed graph as the sum of cycle-cover weights; a cycle cover has one incoming and one outgoing selected arc at every vertex (2010 p. 7; 2012 p. 11).

For distinct interface positions u and v, examine covers of the internal gadget vertices while recording whether the gadget supplies an outgoing arc at u and an incoming arc at v. Conservation of internal indegrees and outdegrees forces these two interface indicators to agree. When both are zero, acyclicity of D leaves only the unique selection of every internal loop. When both are one, the nonloop selected edges comprise one u-v path: internal vertices off that path use their loops, and those on it do not. An additional nonloop cycle is excluded by acyclicity. This gives the exact two-state transfer:

    unused arc: 1 extension;
    used arc: a extensions;
    mismatched use of the two interfaces: 0 extensions.

Replacing a directed weighted arc u->v with this gadget, sharing only its interface positions with the background graph, consequently preserves the permanent. If the original arc is a loop, identify u=v after construction: a used path becomes a cycle through that original vertex; the unused state leaves that vertex's two demands to the background. The same a-versus-1 count applies. This reconstructs the equality asserted in both PDFs from the diagram, including the loops that fill unused internal vertices.

## Matching-signature deduction from the diagram

This paragraph is a deduction checked here, not a matching-signature theorem explicitly written in these PDFs. Split every internal vertex q of D into L_q,R_q, add the identity edge L_q-R_q, retain L_u and R_v as terminals, and replace each nonloop directed arc x->y by L_x-R_y. The two bipartition classes have equal size. Removing exactly one terminal therefore yields zero perfect matchings. With both terminals removed, a nonidentity matching would encode a nonloop directed cycle, impossible in D, so the identity matching is unique. With both terminals present, follow the selected nonidentity edges from u: the degree constraints yield a u-v path, and acyclicity precludes any extra nonidentity cycle. Each path completes uniquely by identities elsewhere. Thus the terminal signature is

    (both present, both removed, only L_u removed, only R_v removed) = (a,1,0,0).

Its size is 4k+2 vertices and 5k+popcount(a) edges, including identity edges. The graph is simple because all chain/helper vertices are fresh and the directed nonloop construction has neither duplicate arcs nor loops. This proves the compact terminal construction independently from the displayed binary-sum mechanism; the PDF does not itself state a general undirected nonbipartite weighted-matching or hafnian theorem.

## Exact documentary scope and limitations

- The 2010 proof of Theorem 2(iii), printed p. 8, and 2012 proof of Theorem 1.3(ii), printed p. 12, use the diagram to remove positive/nonunit weights from directed permanent instances. Both explicitly restrict their immediate reduction to weights at most n and nonunit weights on loop edges. Both assert preservation of the permanent and a logarithmic edge-count increase. The surrounding lower-bound chain is signed permanent -> nonnegative bounded-integer permanent -> 0/1 permanent.
- The captions formulate the right diagram for binary a, and the mechanism above works for every positive binary integer a; the bounds a<=n and loop-only placement are the inputs used in those particular hardness proofs. Distinguish that mathematical generality of the depicted gadget from the exact stated application.
- The 2010 next page says its hardness results transfer to perfect-matching counting even for bipartite graphs. The 2012 introduction also relates permanents to perfect matchings and lists their hardness consequences. These passages do not, on their own, supply an approximation algorithm or a weighted sampler.
- Neither inspected passage states the terminal signature (a,1,0,0), the global gluing lemma for general undirected graphs, rational-denominator bit accounting, a hafnian FPRAS, or an approximate weighted sampling analysis. Those would require their own arguments or additional cited sources. Absence from these passages is not a claim about all literature.
- No assertion is made about public-disclosure dates beyond the report/version/date labels visible in these actual PDFs, redistribution rights, or unseen-candidate novelty. No upstream approximation theorem has been inspected in this bounded task.
