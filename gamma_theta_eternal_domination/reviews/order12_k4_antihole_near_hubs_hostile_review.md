# Hostile review: anti-\(C_7\) near-hub alignment and cap

**Verdict:** `ACCEPT_PROVED_LOCAL_LEMMAS_WITHOUT_SCOPE_INFLATION`.

This accepts Theorem 1, Corollary 3, and Theorem 4 of the frozen note as
mathematical consequences of their stated hypotheses and previously accepted
inputs.  It does not exclude the full induced-\(\overline{C_7}\) template,
certify an order-12 slice, establish novelty, or resolve the
\(\gamma\)–\(\theta\) conjecture.

## Frozen scope

| artifact | SHA-256 |
|---|---|
| `math/lemmas/order12_k4_antihole_near_hubs.md` | `5db7b3970794ca3dd16fd612ae2d1b2111a68596a34ccd304c7a30fd1371688e` |
| author regression probe | `850e7973b5863b7beb8d6562149f4c08adf7a36af9df8bba22a99fd6c14fe0c2` |
| independent hostile probe | `138a86a4c154b109eae4996f5030392d1d1f73814f7f307dd4b3229cbe30e381` |

The accepted note differs from its frozen predecessor
`39182554433e413741f15d7c70e89d07389c8d1ebd658ab74c39bc596fc825c5`
only in its status label and in the requested explicit transition from the
displayed independent four-set to
\(\gamma^\infty(J)=4\) and hence to an eternal family of four-sets.  Reversing
exactly those two edits reconstructs the predecessor byte-for-byte.

The imported mathematical dependencies were also checked at their current
accepted hashes: `math/reductions.md` at `d2c899b6...`,
`order12_k4_hub_constraints.md` at `aab7cc33...`, and
`order12_k4_synthesis_target.md` at `5421357c...`, together with their
existing hostile reviews.

## Definition-level audit

Lemma 2 uses only attacks at unoccupied vertices and one move along one edge.
When an unoccupied vertex of an independent set is attacked, no guard already
on that independent set can answer, so the number of guards on it increases
by one.  This proves both the forcing of every independent \(k\)-set into
every eternal \(k\)-family and the lower bound
\(\alpha\leq\gamma^\infty\).  No all-guards move is present.

The invoked induced-subgraph inequality has the correct direction:
\[
\gamma^\infty(G[W])\leq\gamma^\infty(G).
\]
Its accepted maximum-occupancy projection proof applies to the nine-vertex
induced graph used here.

## Theorem 1

If \(xy\) is absent, the four cyclic-distance rows in the note give a stable
three-set on the \(C_7\) avoiding the one or two attachment vertices.  Adding
\(x,y\) gives an independent five-set, contradicting
\(\gamma^\infty(J)\leq4\).  The distance rows cover all possibilities up to
rotation and reflection.

If \(xy\) is present but the two spokes differ, the three attack-table rows
cover cyclic distances \(1,2,3\).  In each row:

1. the displayed \(D\) is an independent dominating four-set and is therefore
   forced into every eternal four-family;
2. every first-response guard is enumerated;
3. exactly one first successor dominates; and
4. every response to the displayed second unoccupied attack is
   nondominating.

The accepted editorial revision now makes the formerly implicit transition
explicit: the displayed independent four-set gives
\(\gamma^\infty(J)\geq4\), while induced-subgraph monotonicity gives the
reverse inequality.  Thus an eternal family of exactly four-sets exists
under the contradiction hypothesis.  This is not an additional assumption
or a proof gap.

For sharpness, when the spokes agree and \(xy\) is present,
\(\{a,x,y\}\) and three edges covering the path \(C_7-a\) form a four-clique
partition.  Conversely, \(x\) plus a stable three-set of that six-vertex path
is independent.  Hence the induced nine-vertex graph has
\(\gamma^\infty=4\).

## Complement translation and Theorem 4

Complementation is translated correctly.  An \(H\)-vertex adjacent to six
antihole vertices has one neighbor on the corresponding induced cycle in
\(G\).  Theorem 1 therefore makes any two near-hubs nonadjacent in \(H\) and
aligns their unique \(H\)-nonneighbor.

For a common gap labelled \(0\), none of
\[
\{0,1,4\},\quad\{0,2,5\},\quad\{0,3,6\}
\]
has an internal common neighbor in the induced antihole: the corresponding
closed \(C_7\)-neighborhood unions each cover all seven rim vertices.  Every
aligned near-hub also misses all three triples because each contains the
common gap.

With five near-hubs, P3 immediately fails.  With exactly four, the sole
remaining outside vertex must witness every one of the three triples.  Their
union is the whole rim, so this vertex is a forbidden outside hub.  The
conclusion “at most three” is therefore sound.  Order 12 is used exactly to
leave five outside vertices; P3 and the previously accepted no-hub theorem
are the only ambient target inputs.  Connectedness is harmlessly retained as
a standing hypothesis but is not used.

## Independent finite falsification attempts

The independent hostile probe uses explicit `frozenset` configurations and
an explicit colored configuration graph; it imports no campaign evaluator.
It:

- checked all 98 ordered labelled two-spoke graphs, obtaining
  \(\gamma^\infty=4\) in exactly the seven aligned-edge cases and \(5\) in
  the other 91;
- found a stable rim triple after every one of the 49 ordered deleted pairs;
- checked every legal response in all three attack-table rows;
- checked all seven aligned gaps, all 889 four-near-hub/nonhub remaining
  incidence patterns, and all seven five-near-hub cases, with no no-hub P3
  survivor; and
- independently replayed the unchanged frozen author-probe source against the
  accepted note, rebinding only its expected note digest in memory.

The hostile probe exited zero in 0.522 seconds with empty stderr.  These
finite checks are regression evidence; the proof audit above supports the
mathematical verdict.

## Claim boundary

The accepted result is the local branch restriction:

> In the order-12 parameter-four target, an induced
> \(\overline{C_7}\) in \(H=\overline G\) has at most three outside vertices
> adjacent to exactly six rim vertices.

It is a proved necessary condition relative to the already accepted P3,
no-hub, and one-guard monotonicity inputs.  It is not a finite nonexistence
certificate and has not been literature-audited for novelty.
