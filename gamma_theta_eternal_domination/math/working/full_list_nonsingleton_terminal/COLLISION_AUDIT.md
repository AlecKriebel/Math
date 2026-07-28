# Collision and occupancy audit

Date: 2026-07-28 (PDT)

This audit supports `CANDIDATE.md`.  It separates the identifications
excluded by the symbolic row argument from the stronger distinctness
realized by the exact finite control.

## 1. One symbolic nonroot-corridor row

Use the notation of Lemma 2.1:

\[
 S=\{u,v,t\},\qquad
 T=\{v,t,q\},\qquad
 E=\{v,t,r\},\qquad
 A_v=\{t,q,r\}.
\]

The roles have the following forced occupancy relations.

- \(u,v,t\) are pairwise distinct because \(S\) is a triple.
- \(x\notin S\) by the full-target setup.
- \(r\notin S\cup\{x\}\).  The terminal state has three occupants, and
  \(r\in B=N_H(x)\), whereas every root color is adjacent to the full
  target.
- \(q\notin S\cup\{x,r\}\).  The predecessor and one-swap transition have
  three distinct occupants, and a nonroot corridor has \(q\notin B\)
  while \(r\in B\).
- The C-149 quartet \(\{x,u,q,r\}\) has exactly one missing graph edge,
  namely \(xr\).  In particular, \(xq,uq,ur,qr\in E(G)\).
- A secondary color \(v\in Q(r)\setminus\{u\}\) is occupied in \(T\);
  \(vr\in E(G)\), so \(v\to r\) is a legal alternate response.
- A missed witness \(w_v\) for \(A_v\) is not in \(A_v\).  It is not
  \(v\), because \(vr\in E(G)\); not \(u\), because \(uq\in E(G)\);
  and not \(x\), because \(xq\in E(G)\).  Hence

  \[
  w_v\notin S\cup\{x,q,r\}.
  \]

- Since \(T\) dominates and \(T\setminus A_v=\{v\}\), the missed witness
  satisfies \(vw_v\in E(G)\).

If both anchors in \(S-u\) are secondary colors, their row-wise witnesses
are distinct: the witness assigned to \(v\) is nonadjacent to \(t\),
whereas the witness assigned to \(t\) is adjacent to \(t\).

Nothing here excludes a witness for one color from coinciding with a
witness, mover, or terminal belonging to a different color.  The
candidate makes no cross-row distinctness claim.

## 2. Direct-root row

For a direct-root terminal, the rank-zero predecessor is \(S\), the
attacked vertex \(r\) is unoccupied, and the guard at \(u\) gives the
banned successor \(S-u+r\).

If \(v\in Q(r)\setminus\{u\}\), then \(v\) is a distinct occupied guard
and \(v\to r\) gives \(S-v+r\).  This triple still contains \(u\), so it
cannot equal any ban state \(S-u+z\).  Its occupancy alone therefore
prevents the secondary response from being silently classified as
banned.

## 3. Exact-control roles

For the graph6 control

```text
OQifur}UO]}iTij]tpo}v
```

the named roles are:

| role | color \(0\) | color \(1\) | color \(10\) |
|---|---:|---:|---:|
| color | 0 | 1 | 10 |
| target | 6 | 6 | 6 |
| mover \(q\) | 14 | 3 | 12 |
| terminal \(r\) | 11 | 7 | 5 |
| secondary color | 1 | 10 | 0 |
| rank-zero missed witness | 8 | not applicable | 4 |

The root \(\{0,1,10\}\), target \(6\), mover set
\(\{14,3,12\}\), terminal set \(\{11,7,5\}\), and rank-zero
witness set \(\{8,4\}\) comprise twelve pairwise-distinct vertices.
The three diamonds necessarily share the target, but their colors,
movers, and terminals are distinct.

The verifier checks all of the following from the decoded graph rather
than trusting this table:

- distinctness within every state and one-swap transition;
- disjointness of root, target, movers, terminals, and the two named
  rank-zero witnesses;
- exact predecessor and terminal occupancies;
- the legal target-to-mover approach and mover-to-terminal entry;
- the legal secondary-color response;
- the unique missing edge in each four-vertex diamond;
- exact missed-vertex sets \(\{8\}\) and \(\{4\}\);
- ban membership of each terminal and nonmembership of each secondary
  response; and
- survival of the color-\(1\) secondary response versus nondomination of
  the other two.

The safe color also has a different legal nondominating response
\(\{3,7,10\}\), which misses vertex \(2\).  This extra vertex is not used
as a named witness in the symbolic doubleton argument, because that
argument selects the response made by the secondary palette color \(10\).
