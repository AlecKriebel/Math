# Research log: family mixed-\(P_4\) endpoint-rank recurrence

Date: 2026-07-28 (PDT)

## Scope

Work in the literal greatest eternal triple-family under

\[
\gamma(G)=\alpha(G)=\gamma^\infty(G)=3
\]

and the exact family-response mixed-\(P_4\) lists

\[
\{a\},\quad\{a,c\},\quad\{b,c\},\quad\{b\}
\]

at an independent root \(S=\{a,b,c\}\).  Accepted C-151 makes the two
omitted \(c\)-swaps \(Q_0=\{a,b,x_0\}\) and
\(Q_3=\{a,b,x_3\}\) dominating positive-finite-rank states.

Never infer a graph nonedge from an omitted family response.

## 2026-07-28 12:32 PDT — dependency audit

- Read the accepted C-108 source and hostile review in full.
- Read the accepted C-143 source and hostile review in full.
- Read the accepted C-145 source and hostile review in full.
- Read the accepted C-146 source and hostile review in full.
- Read the accepted C-148 source and hostile review in full.
- Read the final accepted C-151 hostile review.  The recurrence is bound
  to source SHA-256
  `115df65cbeb4e9dffccaad93adc78e7c22d698a5036f431ec2e57ba67598a3d1`
  and review-manifest SHA-256
  `9172dc9ce7f31d798118f99b9c9ebc376e410e5c9b7d7e3cdfaa4c574f3d9c80`.
- Rechecked the exact target in `family_mixed_p4_lift/NOTE.md` Section 4.
- The C-146 single-hit mechanism applies to an endpoint row even without
  assuming a reverse active orientation: the finite-horizon transport
  theorem itself is unconditional.  C-143 is not needed for that
  transport because the transported mixed-\(P_4\) pattern supplies either
  a positive-rank endpoint or the C-148 rank-zero defect alternative.

## 2026-07-28 12:32 PDT — first proved recurrence step

- Let \(Q_i=S-c+x_i\) have positive finite rank \(h\), and let \(r\)
  delete it at round \(h\).
- If \(r\) has exactly one neighbor in \(S\), that neighbor cannot be
  \(c\): domination of \(Q_i\) would force \(rx_i\), and then the
  \(x_i\to r\) successor is the maximum independent state
  \(S-c+r\), which survives.
- Hence the unique root neighbor is \(g\in\{a,b\}\).  Then
  \(S'=S-g+r\) is an independent ridge neighbor of \(S\).  C-108
  transports the two shared response roles, and C-064 Theorem 3.1
  transports the exchanged roles.  Explicitly, their direct successor is
  the common state \(S-g+x_j=S'-r+x_j\).  If retained, it must dominate
  the opposite exchanged vertex: independence of \(S'\) forces
  \(rx_j\in E(G)\), and independence of \(S\) forces
  \(gx_j\in E(G)\).  Thus the entire exact mixed-\(P_4\) list system
  transports under \(g\leftrightarrow r\).
- The legal deleting successor
  \[
  Q_i-g+r=S'-c+x_i
  \]
  is the corresponding endpoint row.  Its rank is \(<h\), and C-146's
  unit ridge Lipschitz bound makes its rank exactly \(h-1\).
- If \(h-1=0\), accepted C-151 Lemma 1.1 identifies this as the
  family-list form of the C-148 endpoint domination-defect core.  If
  \(h-1>0\), it is a strictly lower positive-rank copy.
- Therefore every failure of the proposed recurrence is forced into the
  genuine multi-hit branch \(|N(r)\cap S|\ge2\).
- Named-collision and occupancy audit: a single-hit target cannot be a
  path vertex because each path vertex has at least two root neighbors.
  The target \(c\) cannot delete an endpoint row at any rank because
  endpoint saturation permits the surviving response \(x_i\to c\) back
  to \(S\).
- Iterating the single-hit step strictly decreases the positive integer
  rank.  Accepted C-148 excludes the rank-zero terminal defect, so every
  realization must reach a transported row with a multi-hit deleting
  attack after finitely many root-ridge transports.

## Current boundary

The multi-hit branch is not yet resolved.  A complete exact-list audit
now gives:

- no root vertex can be a deleting target;
- a named path target either has a surviving legal response or is the
  opposite endpoint and gives an immediate lower-rank endpoint row;
- every unresolved target is therefore fresh;
- after endpoint-adapted relabeling
  \(S=\{c,\ell,m\}\), \(Q=\{u,\ell,m\}\),
  \(L_S(u)=\{\ell\}\), the fresh multi-hit branch has eight bookkeeping
  cells according to its root neighborhood and the edge \(ur\);
- the cell \(N(r)\cap S=\{c,\ell\},ur\notin E(G)\) is impossible;
- the reflected cell
  \(N(r)\cap S=\{c,m\},ur\notin E(G)\) has a unique successor of exact
  rank \(h-1\) and forces \(\ell\leftrightarrow u\), but that successor
  is not an endpoint row because \(cr\in E(G)\);
- both \(ur\)-present two-hit-\(c\) cells force a singleton list at \(r\)
  and a reciprocal active edge; and
- in the \(\{\ell,m\}\)-collision cells, a singleton list at \(r\)
  forces its responder reciprocal with \(r\).

The remaining multi-hit cells do not yet yield a lower-rank exact-list
endpoint copy, a C-148 defect, or a dominating pair.  Omitted roles at
\(r\) remain family nonmembership statements only.

## 2026-07-28 — bounded discovery replay

- Replayed the accepted C-151 SAT generator at orders \(7,\ldots,11\).
  CaDiCaL returned `UNSAT` with formula sizes
  \(581/1414\), \(1092/2702\), \(1884/4726\), \(3045/7723\), and
  \(4675/11963\) variables/clauses.
- Combined with C-151's recorded orders \(12,\ldots,22\), the discovery
  range now covers every order \(7,\ldots,22\).
- This remains **OBSERVED** only.  No proof certificate or independent
  encoding audit is packaged, and none of these rows is used above.

## 2026-07-28 13:05 PDT — hostile proof-binding revision

- Read the exact hostile review of the frozen recurrence candidate.
  It found no substantive mathematical counterexample and requested only
  dependency and proof bindings.
- Read accepted C-064 and its hostile review in full.  Bound source
  SHA-256
  `e30a0ac4e028deefbf4c4533646ff934b617d8ff61dce38ec2389a50d622d8e7`
  and review SHA-256
  `bc5011d85d333fb66fce3ea563e4cc80cf016090cc3427e44187b2e40fb5f9f8`.
  Lemma 2.1 now invokes C-064 Theorem 3.1 and records the opposite-vertex
  domination argument forcing both exchanged move edges.
- Read accepted C-058 and its hostile review in full.  Bound source
  SHA-256
  `71384d66373ab4cbffa7ced60973971cf39b72a0315eac31ad522abd1afa2f47`
  and review SHA-256
  `4369b3b85912e3e9a534ea2a63c9cc12ab06cb701cd2227ea77c912665c51d45`.
  The named-target audit now identifies C-058 Theorem 3.1 and explicitly
  uses the family-state construction in its restoration proof.
- The rank-zero terminal now cites accepted C-151 Lemma 1.1 as the exact
  family-response-list one-defect form of the C-148 kernel.
- No theorem was broadened or weakened; the full eight-cell recurrence
  remains open.
