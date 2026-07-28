# Collision and model audit

## General rank-zero restoration row

The independent root \(S=\{u,a,c\}\) makes \(u,a,c\) pairwise distinct and
pairwise nonadjacent in \(G\).  Fullness has \(x\notin S\) and makes \(x\)
adjacent in \(G\) to all three root anchors.

Because \(r\in B=N_{\overline G}(x)\), the vertex \(r\) is outside
\(S\cup\{x\}\): every root anchor is adjacent to \(x\) in \(G\), whereas
\(r\) is not.  The predecessor \(T=\{c,r,q\}\) is a three-set, so
\(q\ne c,r\).  The terminal attack at \(a\) is unoccupied, so
\(q\ne a\).  Lemma 2.1 proves \(q\notin S\), including the only unresolved
collision \(q=u\).  Therefore

\[
 T-S=\{r,q\},\qquad S-T=\{u,a\}
\]

are literal two-sets when arbitrary-state restoration is applied in
Theorem 2.2.

The selected move \(q\to a\) is a physical \(G\)-edge and reaches exactly
\(\{a,c,r\}\).  Since \(ca\notin E(G)\), the only other possible physical
responder is \(r\); its successor, when \(ar\in E(G)\), is exactly
\(\{a,c,q\}\).  No all-guards move or occupied attack is used.

## Shared-secondary witness ladder

A missed witness satisfies

\[
 N_G[w]\cap\{a,c,q\}=\varnothing.
\]

The closed-neighborhood convention forces \(w\notin\{a,c,q\}\).  The proof
splits \(w=u\) before making an attack.  In the other branch,
\(w\ne u\), so \(w\) is unoccupied in \(\{u,c,q\}\).  Its guards \(c,q\)
have no move edge to \(w\); domination and closure therefore force the
single move \(u\to w\).

The resulting state \(\{w,c,q\}\) does not contain \(a\).  Both \(w\) and
\(c\) miss \(a\), while the originally selected terminal move supplies
the edge \(qa\).  Hence the second attack is unoccupied and uniquely moves
\(q\to a\).  The endpoint \(\{w,c,a\}\) is a three-set because
\(w\notin\{a,c\}\).

If \(ar\in E(G)\), the missed witness cannot be \(r\), because \(a\) would
dominate \(r\), and cannot be \(x\), because fullness gives \(ax\in E(G)\).
Without the edge \(ar\), the proof deliberately permits \(w=r\).

## Exact control rows

For `OYifur}UO]}iTij]tpo]v`, the verifier reads all incidences directly
from the decoded graph.

- Root: \(\{0,1,10\}\); full target: \(6\).
- Complement-link vertices: \(B=\{5,7,9,11,13\}\).
- Common retained ban state: \(\{1,5,10\}\).
- Common dominating but nonretained banned state: \(\{1,7,10\}\).

The attacked-secondary row starts at \(\{1,5,7\}\), attacks the unoccupied
vertex \(10\), and has the two physical moves \(7\to10\) and \(5\to10\).
The first enters the retained ban state; the second enters the common
omitted state.

The shared-secondary row starts at \(\{5,7,10\}\), attacks the unoccupied
vertex \(1\), and has the selected edge \(7\to1\).  The physical pair
\(1\,5\) is a graph nonedge, so guard \(5\) cannot move.  This nonedge is
checked from the graph data.  It is **not** inferred from the palette
identity \(Q(5)=\{0,10\}\).

The verifier separately checks that every state used as retained belongs
to the literal greatest family, every retained state dominates, and every
one of its 3,952 attacks has a one-guard response inside the family.
