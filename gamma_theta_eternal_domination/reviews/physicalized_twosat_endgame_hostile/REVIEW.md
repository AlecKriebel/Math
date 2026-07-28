# Hostile review: physical response literals and nonphysical clauses

## Verdict

**PASS.**

The current bytes of the source note prove Theorem 2.1 and Corollary 2.2
from the accepted two-response replication lemma.  The complement path has
the stated even parity, so the two port events are literally the same
Boolean event.  The proof does not move the complement edge that supports a
cross clause.

A clean-room bit-mask verifier independently reconstructs the 13-vertex
control from both its graph6 record and its word description.  It confirms
the exact parameter tuple, family, lists, full induced projection, and
failed clause transport.  No self-witness, hidden full list, odd projection
edge, or overlooked physical representative was found.

This verdict validates a boundary result, not the gamma--theta conjecture:
the control is three-clique-coverable and its response 2-CNF is colorable.

## Frozen source bytes reviewed

| artifact | SHA-256 |
|---|---|
| `math/working/physicalized_twosat_endgame/NOTE.md` | `3a357c3c7ece9a0cf33f7b555cae21e629a19b9e2d86e6ebe6f5798b4f08e7df` |
| `math/working/physicalized_twosat_endgame/verify.py` | `f0d99b27605f63e243e8cddba036575e9fc0a7d000718fcfde09d33f58cbbc8d` |
| `math/working/physicalized_twosat_endgame/result.json` | `9095bf44af7a0a8d8b93dd0bde9544a5e91a04710ea6fc5d7b2d7dda18645956` |

The accepted prerequisite used for the nontrivial case is Lemma 2.1 of
`math/working/separated_core_n14_attack/NOTE.md`, whose reviewed source hash
is `a619c7acf0dfccbc5767379f68d25f6272d3318db33e433cede39aa70b5ce279`.

## Human-proof audit

Let \(S=\{a,b,c\}\) be an independent member of an eternal triple-family,
assume \(\gamma(G)\geq3\), and let \(L(t)=\{a,b\}\).  A positive response
membership forces its corresponding graph edge: the other two independent
anchors cannot dominate the omitted anchor.  Hence \(at,bt\in E(G)\).

If \(ct\in E(H)\), taking \(r=t\) proves the first case directly.  If
\(ct\in E(G)\), then \(t\) is \(G\)-complete to \(S\), so the accepted
pure omitted-color pair lemma applies to \(t\).  It supplies distinct
vertices \(y,r\) with

\[
ty,yr,cy,cr\in E(H),\qquad tr\in E(G),\qquad a,b\in L(r).
\]

The actual nonedge \(cr\in E(H)\), rather than a missing family response,
excludes \(c\) from \(L(r)\), so \(L(r)=\{a,b\}\).  Similarly
\(c\notin L(y)\).  Thus \(t,y,r\in W_c\), and \(t-y-r\) is a length-two
path in the bipartite graph \(B_c\).  Its endpoints are in one component
and on the same side.  All vertices used are distinct for the reasons
recorded in the replication lemma; no loop or occupied attack is hidden in
the application.

For a fixed component coordinate, the event that a two-list port \(x\)
takes color \(w\) is

\[
z_{c,K}=\pi_c(x)\mathbin{\oplus}\iota_c(w).
\]

The even path gives \(\pi_c(t)=\pi_c(r)\), hence
\(P(t,w)=P(r,w)\) as identical equations in the same component variable.
Substitution in a 2-CNF clause is therefore exact.  This conclusion says
nothing about whether the supporting edge \(rq\) lies in \(H\), and the
source note correctly keeps that incidence statement separate.

## Independent finite-control audit

`independent_check.py` imports no source or campaign module.  It:

- decodes `LFzJbZYhdrDZdM` directly into integer adjacency masks and
  independently reconstructs the same graph from the two-coordinate words
  and three exceptional edges;
- exhaustively computes \(\gamma,i,\alpha,\theta\), and separately computes
  the simultaneous greatest one-guard fixed point;
- rebuilds both transversal families with bit masks and checks all 1,420
  legal unoccupied attacks;
- reconstructs every response list from family membership;
- colors every component of the **full** induced graph
  \(B_c=H[\{a,b\}\cup W_c]\) and explicitly checks every induced
  complement edge crosses the bipartition;
- transcribes and checks all 78 entries of the human common-\(H\)-neighbor
  table, including that no witness is one of the pair endpoints; and
- enumerates every exact-\(\{a,b\}\) physical vertex, then filters by
  component, parity, and preservation of the \(qv\) complement edge.

The independently obtained values are

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3).
\]

There are 144 dominating triples.  Two are deleted in the first
simultaneous kernel round, and the 142 survivors are **exactly** the
supplied family.  The two coordinate families have 80 states each, their
union has 142 states, and its serialized hash is

```text
9e49fca49aceff56168e0aef5cd825b5a55ec73a901985daec7bc03a9022e4aa
```

The response lists outside \(S\) are

```text
3:ab  4:bc  5:ab  6:bc  7:bc  8:ab  9:ac  10:ac  11:c  12:a
```

so there are no hidden full lists.  The complete projection is

```text
V(B_c) = {0,1,3,5,8,12}
E(B_c) = {01, 1-12, 35, 58}.
```

Its port component is the path \(q-z-r=3-5-8\).  The physical exact
\(\{a,b\}\) vertices are exactly \(z=5\) and \(r=8\); \(z\) has opposite
parity from \(q\), while \(r\) has the same parity.  Therefore \(r\) is
the unique same-event physical representative.  Exhaustive filtering gives
no same-event physical representative adjacent to \(v\) in \(H\):

```text
qv in H;  physical(ab) = {z,r};  same-sign = {r};
same-sign preserving qv = empty;  rv in G.
```

The concise source `result.json` is a semantic summary rather than the
verifier's complete printed object; every one of its fields agrees with the
independent reconstruction.

## Reproduction

From the campaign directory:

```text
python3 -I -B -W error \
  reviews/physicalized_twosat_endgame_hostile/independent_check.py \
  > reviews/physicalized_twosat_endgame_hostile/independent_result.json

python3 -I -B -W error \
  reviews/physicalized_twosat_endgame_hostile/independent_check.py \
  reviews/physicalized_twosat_endgame_hostile/independent_result.json

python3 -I -B -W error \
  math/working/physicalized_twosat_endgame/verify.py
```

All commands pass on the frozen source bytes above.
