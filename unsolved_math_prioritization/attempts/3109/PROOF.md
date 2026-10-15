# Petersen fragments refute the proposed oddness bound

## Result and attribution

For every odd integer \(n\ge 3\), there is a connected simple bridgeless cubic graph \(G_n\) with \(10n\) vertices such that every cycle in every 2-factor is odd and
\[
\omega(G_n)=n+1.
\]
Thus \(G_3\), with 30 vertices and oddness 4, refutes the bound 2.

Here a 2-factor is a spanning subgraph of degree 2 at every vertex, and oddness is the minimum number of odd cycles among all 2-factors. The target is the conjecture on the [Open Problem Garden page](https://www.openproblemgarden.org/op/odd_cycles_and_low_oddness), whose hypotheses require a bridgeless cubic graph. The page does not impose 3-edge-connectivity.

The construction and two-case analysis belong to the Anonymous comments of [29 June 2010](https://www.openproblemgarden.org/op/odd_cycles_and_low_oddness#comment-6751) and [2 July 2010](https://www.openproblemgarden.org/op/odd_cycles_and_low_oddness#comment-6753). The proof below reconstructs them with all necessary local facts and witnesses. No claim of novelty or journal publication is made.

## Petersen graph facts

Write the vertices of the Petersen graph \(P\) as \(a_j,b_j\), with \(j\) taken modulo 5. Its edges are
\[
a_ja_{j+1},\qquad b_jb_{j+2},\qquad a_jb_j.
\]
The edges of the last kind are called spokes. This definition gives a connected simple cubic graph on ten vertices.

The girth is 5. Indeed, without spokes a cycle is one of the two displayed 5-cycles. A cycle crosses between the two vertex classes an even number of times. If it has two spokes and length at most 4, the other two edges would have to join the same pair of indices in the outer and inner cycles. This is impossible, since their index differences would have to be both \(\pm1\) and \(\pm2\) modulo 5. Four or more spokes require a nonspoke edge between every two successive spokes, giving length at least 8.

There is no edge cut of size 1 or 2 in \(P\). Otherwise let \(S\) be a smaller nonempty side of such a cut, let \(s=|S|\le5\), and let \(b=|\delta(S)|\le2\). Cubicity gives
\[
3s=2|E(P[S])|+b.
\]
For \(s\le4\), girth 5 makes the induced graph a forest; hence \(3s\le2(s-1)+b\), or \(s\le b-2\le0\), a contradiction. For \(s=5\), the induced graph has at most five edges: any cycle spans these five vertices, and adding a chord to that 5-cycle produces a shorter cycle. Consequently \(b\ge15-10=5\), again a contradiction.

It follows that \(P-e\) is connected and bridgeless for every edge \(e\). Disconnection would make \(e\) a bridge of \(P\). A bridge \(f\) after deleting \(e\) would provide a cut of \(P\) contained in \(\{e,f\}\), contrary to the preceding paragraph.

Every 2-factor of \(P\) consists of two 5-cycles. To prove this without invoking a classification theorem, complement a 2-factor to obtain a perfect matching \(M\). If \(k\) spokes belong to \(M\), the other \(5-k\) outer vertices pair among themselves, so \(k\) is odd. The possibilities are 1, 3, and 5. With three spokes, the two unmatched indices would have to differ by \(\pm1\) for the outer matching and \(\pm2\) for the inner matching, which is impossible. With five spokes, the complement is the two original 5-cycles.

With one spoke, rotate indices so it is \(a_0b_0\). Removing its endpoints leaves a path on four outer vertices and a path on four inner vertices. Each has a unique perfect matching. Thus
\[
M=\{a_0b_0,a_1a_2,a_3a_4,b_2b_4,b_1b_3\}.
\]
Its complement consists of
\[
(a_0,a_1,b_1,b_4,a_4),\qquad
(a_2,a_3,b_3,b_0,b_2),
\]
where cycle notation closes the last vertex back to the first. Rotating these cycles proves the assertion for all five one-spoke choices. This also enumerates all six perfect matchings of \(P\).

Fix \(e=a_0b_0\). A 2-factor avoiding \(e\) is the union of the outer and inner 5-cycles. A 2-factor containing \(e\) is
\[
(a_1,a_2,b_2,b_0,a_0),\qquad
(a_3,a_4,b_4,b_1,b_3).
\]
Deleting \(e\) from this latter factor leaves a path from \(a_0\) to \(b_0\) on five vertices and a disjoint 5-cycle. Both local states therefore exist.

## Constructing the graph

Take disjoint copies \(P_i\) of \(P\), indexed by \(i\in\mathbb Z/n\mathbb Z\). In block \(i\), delete the edge \(x_iy_i\) corresponding to \(a_0b_0\), and denote the resulting graph by \(H_i\). Add the links
\[
\ell_i=y_ix_{i+1}.
\]
For \(n\ge3\), these links join distinct blocks without loops or parallel edges. Every vertex has degree 3: only \(x_i,y_i\) lost an edge, and each receives one link. The connected blocks form a cyclic chain, so the whole graph is connected and has \(10n\) vertices.

Every internal edge of a block lies on a cycle in that block because \(H_i\) is bridgeless. To check the links, choose any simple \(x_i\)-to-\(y_i\) path in each connected block. These paths and all the links form one cycle, since the blocks are disjoint and cyclically joined. Hence each link also lies on a cycle. Thus \(G_n\) is bridgeless.

## Classifying every 2-factor

Let \(F\) be any 2-factor of \(G_n\). The boundary of block \(H_i\) is precisely \(\{\ell_{i-1},\ell_i\}\). An even-degree subgraph meets every edge cut evenly, since
\[
\sum_{v\in S}\deg_F(v)=2|E(F[S])|+|E(F)\cap\delta(S)|.
\]
Therefore \(F\) uses either both boundary links of a block or neither. Around the cycle of blocks, this forces all link indicators to agree.

If no links are used, the restriction to each block is a 2-factor of \(P_i\) avoiding the deleted edge. The Petersen classification shows that it consists of two 5-cycles. Thus \(F\) consists of \(2n\) cycles of length 5.

If all links are used, the restriction to block \(i\) has degree 1 at \(x_i,y_i\) and degree 2 elsewhere. Adding \(x_iy_i\) yields a 2-factor of \(P_i\). The Petersen classification now implies that the restriction consists of one 5-cycle and one five-vertex path joining the two terminals. The \(n\) paths, together with the \(n\) links, make one cycle of length \(5n\). Thus \(F\) consists of \(n\) cycles of length 5 and one cycle of length \(5n\). The assertion that the links share a single cycle follows here from the local path description; parity alone was only used to force their simultaneous presence.

Both global cases occur by using the respective explicit local witnesses in every block. When \(n\) is odd, all cycle lengths in both cases are odd. Consequently
\[
\omega(G_n)=\min\{2n,n+1\}=n+1.
\]
This proves the result for every odd \(n\ge3\).

## Scope

The two links bounding a block form a 2-edge-cut. The construction therefore says nothing about a strengthened conjecture requiring 3-edge-connectivity. It establishes a counterexample of order 30, without claiming that 30 is the smallest possible counterexample order. The mathematical proof is independent of a computer enumeration.
