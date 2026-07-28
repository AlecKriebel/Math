# Exact errata history for the initial frozen candidate

The initial hostile verdict was `REVISE_LOCAL_ERRATA`.  The replacements
below were sufficient; no other mathematical change was found necessary.
They are all present in the final confirmed `NOTE.md`, SHA-256
`acfbc262877c08f9e4b38aa38931c3b95699b50073aa9a67d8ac3f80ba9ba3fd`.
The final verdict is `PASS`.

## 1. State the multi-hit hypothesis in Section 2

Immediately after the heading

> `## 2. The exact six-case table`

insert:

> Assume in this section that \(r\) is a multi-hit deleting attack:
> \[
>   |N(r)\cap T|\ge2.
> \]
> By C-146 this assumption is automatic when \(h=1\), and also when
> \(B\) has globally minimum rank among all complementary reverse
> endpoints.

Replace

> The following table is exhaustive.

by

> Under this additional multi-hit hypothesis, the following table is
> exhaustive.

This preserves the all-rank XQ0 and XQ1 conclusions: those conclusions
need only their named row, not rank one or global rank minimality.

## 2. Repair the completion-set definition

Replace equation (4.2) by

\[
 C_{xr}
 =
 \{c\in V(G)-\{x,r\}:cx,cr\notin E(G)\}.
\tag{4.2}
\]

The rest of Theorem 4.1 and its proof then read literally as written.

## 3. Make the private-witness self-collision explicit

Replace the first paragraph of the proof of Lemma 3.1 by:

> Choose a vertex \(y_g\) missed by the non-dominating state
> \(C_g=B-g+r\).  It misses \(r\) and every member of \(B-\{g\}\).
> Because \(g\in N(r)\), one has \(gr\in E(G)\); since
> \(y_gr\notin E(G)\), it follows that \(y_g\ne g\).  Nor can \(y_g\)
> equal a member of \(B-\{g\}\), since those vertices are occupied in
> \(C_g\).  Thus \(y_g\notin B\).  Since \(B\) dominates \(y_g\) and
> \(y_g\) has no neighbor in \(B-\{g\}\), necessarily
> \(gy_g\in E(G)\), proving (3.1).  For \(g\ne g'\), the vertex \(y_g\)
> is adjacent to \(g\), while \(y_{g'}\) is nonadjacent to \(g\), so
> the witnesses are distinct.

This is a clarification of a fact already forced by the displayed
hypotheses, not a new hypothesis.
