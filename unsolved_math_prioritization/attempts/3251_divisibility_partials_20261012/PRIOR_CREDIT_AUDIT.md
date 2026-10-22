# Hu–Xu–Zhuang: exact scope and elementary dependency audit

Checked 12 October 2026. This is an authored mathematical audit, not a reproduction of the source manuscript. No journal-publication or novelty claim is made.

## Primary source and inspection

Qiming Hu, Baogang Xu, Miaoxia Zhuang, *Some properties of minimally nonperfectly divisible graphs*, arXiv:2603.01967v2.

- Versioned record: https://arxiv.org/abs/2603.01967v2
- Versioned full text: https://arxiv.org/html/2603.01967v2
- Versioned PDF: https://arxiv.org/pdf/2603.01967v2
- arXiv DOI: https://doi.org/10.48550/arXiv.2603.01967
- First submission: 2 March 2026, 15:16:09 UTC.
- Inspected revision: 5 March 2026, 15:51:48 UTC.
- The unversioned arXiv landing page still identifies v2 as latest on the inspection date.
- The primary record does not display a journal reference, journal DOI, or acceptance statement. Treat this as an arXiv preprint; a bounded title/author/publication search did not verify a later publication. Search-engine crawl dates are not manuscript dates.
- Retrieved PDF: 13 pages, 328,752 bytes; SHA-256 `331c5cec46144d6b58c307bbb4d429518eb2b9c42ae856b49a2a7da853c3d4f7`.
- Inspection: all of Section 4, relevant Section 3 arguments (Theorem 3.1, Lemmas 3.2–3.4), and the stated scope and argument outline of Theorem 1.4. Printed PDF page 11 was visually checked against the extracted text. This is not a full proof audit of Sections 2–3 or a comparison with v1.

## Exact overlap and boundary

The relevant 2-divisibility statements are all on printed page 11, Section 4. Put k=omega(G).

1. Theorem 4.1 gives four necessary conditions for a minimally non-2-divisible graph (MN2D): no nonempty basin; every vertex lies in a maximum clique and has a neighbor outside that clique; |N(X)| >= k-omega(X) for every nonempty X; and minimum degree at least 2k-2.
2. The paragraph after Theorem 4.1 gives omega(G1)=omega(G2)=k for the two pieces of a clique-cutset decomposition.
3. Lemma 4.1 says every pair of side divisions disagrees somewhere on the shared clique.
4. Lemma 4.2 says side divisions can be chosen so that every disagreement vertex is blocked from changing color on either side by a maximum clique.

Theorem 4.1 is stated as an adaptation of Section 3 without a separate proof. Lemma 4.1 has a short proof. Lemma 4.2 refers to the proof of Lemma 3.4. Their elementary content is reconstructed and checked below.

Theorem 1.4, by contrast, excludes clique cutsets for **minimally nonperfectly divisible** graphs under the extra condition of being claw-free or 2P3-free. It is not an MN2D theorem. Theorem 4.2 concerns triangle-free MNPD graphs and 4-criticality, also a different property.

None of these statements proves unrestricted MN2D clique-cutset exclusion or the odd-hole-free 2-divisibility conjecture. They do establish directly relevant prior art for no-basin, minimum-degree, two-piece maximum-clique, trace-incompatibility, and single-vertex blocking reductions. Independently reconstructed proofs should be described as such, without a novelty claim for these statements.

## Definitions and preliminary reduction

A 2-division of an edge-containing graph H is a partition into two sets, each inducing clique number less than omega(H). Hereditary 2-divisibility requires such a division for every induced subgraph with an edge. Edgeless induced subgraphs are exempt. MN2D means non-2-divisible with every proper induced subgraph 2-divisible.

An MN2D graph G itself has no 2-division: otherwise its proper induced subgraphs and G would all meet the definition. Its clique number k is at least two. Every proper induced subgraph H admits a partition with both clique numbers less than k: if H has an edge, use its 2-division and omega(H)<=k; if H is edgeless, put its vertices on one side, which has clique number at most one.

These observations handle all edge exceptions in the arguments below.

## Independent reconstruction of Theorem 4.1

For X contained in V(G), let N(X) be the neighbors outside X and N[X]=X union N(X). A basin means omega(G[N[X]])<k.

**No basin.** If nonempty X were a basin, X could not be all of V(G). Partition G-X into A,B with both clique numbers below k as above. Every clique of G[A union X] is either contained in A or, if it meets X, contained in N[X]. Thus omega(G[A union X])<k, while omega(G[B])<k. This divides G, a contradiction.

**Two disjoint neighborhood cliques.** Fix v and partition G-v into A,B with both clique numbers below k. Adding v to either side must fail, since otherwise G is divided. Consequently A cap N(v) and B cap N(v) each contain a (k-1)-clique. These two cliques are disjoint. Hence degree(v)>=2k-2. Together with v, either is a maximum clique K; a vertex in the other clique is a neighbor of v outside K. This proves Theorem 4.1(2) and (4), and spells out the stronger paired-clique witness behind its degree bound.

**Set neighborhood inequality.** No basin gives omega(G[N[X]])=k for nonempty X. A maximum clique in N[X] has at most omega(G[X]) vertices in X and at most omega(G[N(X)]) vertices outside. Therefore k<=omega(X)+omega(N(X))<=omega(X)+|N(X)|.

These proofs use induced-subgraph minimality and elementary clique containment. They use neither odd-hole-freeness, perfect-graph theory, nor the conjectured clique-cutset exclusion.

## Independent reconstruction of the clique-cutset consequences

Let S be a clique cutset, V(G)\S=V1 disjoint-union V2 with both parts nonempty and anticomplete, and Gi=G[S union Vi].

**Both pieces retain k.** Since N[Vi] is contained in S union Vi, omega(Gi)<k would make Vi a basin. Hence omega(G1)=omega(G2)=k. Both pieces are proper and therefore admit divisions.

**Agreement glues.** Choose side divisions (Ai,Bi). If their vertex colors agree on S, then A=A1 union A2 and B=B1 union B2 form a partition. A clique cannot meet both V1 and V2, because these sets are anticomplete. Consequently every clique on either global color side lies in one side piece, and both global clique numbers are below k. This contradicts indivisibility. Thus every pair of traces disagrees somewhere, proving Lemma 4.1. Anticompleteness, not merely the fact that the overlap is a clique, is the clique-containment justification in this step.

**Minimum disagreement forces both recolorings to fail.** Of all ordered pairs of side divisions choose one minimizing the number of differently colored vertices of S. Its disagreement set is nonempty by Lemma 4.1. For x in S cap A1 cap B2, if B1 union {x} contained no k-clique, moving x from A1 to B1 would give another valid division of G1: its old A-side only shrinks. The move would reduce the disagreement count by one. Therefore omega(B1 union {x})=k. The same argument moving x in the other piece gives omega(A2 union {x})=k. Interchanging the labels proves the two conclusions for x in S cap A2 cap B1. This is Lemma 4.2.

Since the original receiving side has clique number below k, each newly created k-clique includes x. Removing x leaves a (k-1)-clique in its receiving-color neighborhood. This is the precise forcing witness. The argument supplies no guarantee that sequences of recolorings can achieve agreement, and no contradiction to odd-hole-freeness by itself.

## Use in the current mathematical frontier

Credit this source when presenting any of the overlapping necessary conditions. A strengthened statement, such as a new trace-extension result or an additional lower bound, requires its own proof and a precise comparison with these conditions. The presence of published or posted necessary conditions is not evidence that the open gluing step has been completed.

The manuscript's perfect-divisibility material cannot be substituted for the 2-divisibility arguments above: perfect divisibility requires one side to be perfect and only the other side to lower clique number. For instance, C5 is perfectly divisible but is not 2-divisible.

