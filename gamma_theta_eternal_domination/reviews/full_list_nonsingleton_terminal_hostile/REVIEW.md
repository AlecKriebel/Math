# Hostile review: nonsingleton full-list terminals

## Verdict

**UNCONDITIONAL PASS ON COMMIT `8a77c68c`.**

The reviewed candidate is
`math/working/full_list_nonsingleton_terminal/CANDIDATE.md` at SHA-256

`0497d07b8cf2bf1f5e3572f35d400d954745abae4490e6cac707f15cbcaeb22c`.

I find Lemma 2.1 and Corollary 2.2 sound at their stated rank-zero,
row-wise scopes.  A clean-room implementation also confirms every numerical
and incidence assertion used in Proposition 3.1.  The exact control really has
only two empty restricted kernels; it is therefore a sharp boundary example,
not an instance of the unresolved all-three-empty branch.

This result does **not** prove that any color-restricted kernel survives, does
not handle a terminal entry made from positive deletion rank, does not
eliminate anchor restoration, and does not prove the complete \(k=3\) case or
the gamma--theta conjecture.

## 1. Frozen candidate and dependency audit

The candidate tree at review time is byte-for-byte the tree added by commit
`8a77c68c`.  Its own manifest hashes all match:

| artifact | SHA-256 |
|---|---|
| candidate note | `0497d07b8cf2bf1f5e3572f35d400d954745abae4490e6cac707f15cbcaeb22c` |
| collision audit | `24a7fcf9ee9f0bd4a4a24e7a1105fa6ef152e5bfa82c004f5f6b9c1204446eba` |
| candidate verifier | `3001b7f7b922cf91ad9ad4780b32d7f38acc4b673263ee7583869589709d6fc8` |
| candidate manifest | `0829cde87d15e7634f747d0c7f1af75c66bf51f8ef8828b0d27b31a4c2b8acc9` |
| C-149 source note | `a3a2fc44befb4084b783b73afe108e81af8b7ac3f20b0d34d00bfc35d1f4e62d` |
| C-154 context note | `0d6eb44fa2807cd34e441c31364149577cccf39f28b426a5d81b7cc78c9d1253` |

The candidate verifier emits the frozen stdout SHA-256
`ca0b15eb32c5db9e47c8fca23af2c2d614a1f87626bf59bee585a2e294378b11`.

## 2. Exact C-149 semantics and rank convention

The proof uses the accepted C-149 objects without changing their meaning.

- \(\mathcal F^\star\) is the literal greatest unrestricted eternal family of
  dominating triples.
- For fixed root \(S\), full target \(x\), and color \(u\),
  \(B=N_{\overline G}(x)\) and
  \(\mathcal B_u(x)=\{S-u+z:z\in B\}\).
- The restricted deletion starts from **all** dominating triples outside
  \(\mathcal B_u(x)\), not merely from
  \(\mathcal F^\star-\mathcal B_u(x)\).
- Rank zero means deletion in the first synchronous round.  Thus a
  deletion-witness attack at a rank-zero state has no dominating successor
  outside the ban.  This is exactly the implication used in Lemma 2.1.
- C-149 supplies a retained decreasing-rank trace into the ban when the
  restricted kernel is empty, but it does not say that the last predecessor
  has rank zero.  The candidate states this limitation explicitly.

Because \(x\) is full at \(S\), every root color is adjacent to \(x\) in
\(G\), so \(B\cap S=\varnothing\).  Consequently each terminal
\(r\in B\) is outside \(S\), and a state that still contains \(u\) cannot
silently equal a member of \(\mathcal B_u(x)\).

C-149's terminal split is also preserved exactly.  In a corridor the attacked
vertex is the terminal \(r\), the predecessor is
\((S-u)+q\), and \(q\to r\).  The case \(q=u\) is direct-root.  Otherwise
\(q\notin S\cup B\cup\{x\}\), and the four vertices
\(\{x,u,q,r\}\) induce \(K_4-xr\).  Anchor restoration remains a separate,
unhandled gate.

## 3. Lemma 2.1(1): direct-root audit

The predecessor is \(S\), the attacked vertex \(r\) is unoccupied, and the
selected \(u\to r\) successor is banned.  Suppose a second color
\(v\in Q(r)-\{u\}\) existed.  The definition of \(Q\) gives both the move
edge \(vr\) and the retained, hence dominating, state \(S-v+r\).

That state is outside the \(u\)-ban: it contains \(u\), whereas every ban
state omits \(u\), since \(B\cap S=\varnothing\).  It would therefore be a
first-round response to the same attack.  This contradicts that \(r\) is the
deletion-witness attack at a rank-zero predecessor.  The previously proved
positive incidence \(u\in Q(r)\) then yields \(Q(r)=\{u\}\).

No family nonmembership is converted into a graph nonedge.

## 4. Lemma 2.1(2): nonroot audit

Write \(S=\{u,v,t\}\),
\[
T=\{v,t,q\},\qquad E=\{v,t,r\}.
\]
For a secondary color \(v\in Q(r)-\{u\}\), the edge \(vr\) makes the
alternate response
\[
A_v=\{t,q,r\}
\]
legal at the same attack on \(r\).

The ban-membership argument is exact.  Every \(u\)-ban state contains both
anchors \(v,t\), while \(A_v\) omits \(v\); the C-149 occupancy conditions
ensure that no set collision can restore it.  Hence \(A_v\) is outside the
ban.  If it dominated, it would belong to the initial restricted universe and
would answer the deletion-witness attack.  Rank zero therefore forces
\(A_v\) to be nondominating.

For any vertex \(w_v\) missed by \(A_v\), domination by \(T\) leaves only
the omitted guard \(v\) as a possible dominator.  The possibility
\(w_v=v\) is excluded because \(r\in A_v\) and \(vr\in E(G)\); therefore
\(vw_v\in E(G)\).  The remaining collision exclusions are complete:

- \(t,q,r\in A_v\), so none can be missed;
- \(u\) is adjacent to \(q\in A_v\);
- \(x\) is adjacent to \(q\in A_v\); and
- \(v\) is adjacent to \(r\in A_v\).

Thus \(w_v\notin S\cup\{x,q,r\}\).  If both anchors are secondary colors,
every witness for \(v\) is nonadjacent to \(t\), while every witness for
\(t\) is adjacent to \(t\); their witness sets are disjoint, so distinct
witnesses exist.  No cross-row distinctness follows, and none is claimed.

## 5. Corollary 2.2 quantifiers

The corollary is conditional on selecting one trace per color **such that**
each selected final predecessor has rank zero.  It does not assert that
kernel annihilation guarantees such a choice.  Under that condition:

1. nonsingleton terminal palettes exclude direct-root entries row by row;
2. anchor-restoration entries are still possible; and
3. only after the additional assumption that all three entries are nonroot
   corridors does every row acquire the private witness from Lemma 2.1(2).

This is the strongest conclusion justified by the proof.  The candidate's
OPEN list correctly leaves positive-rank entries, anchor restoration,
cross-row witness identifications, and the all-three-empty contradiction
unresolved.

## 6. Independent exact replay of Proposition 3.1

`independent_replay.py` imports no campaign module and uses packed integer
configurations, a fresh graph6 decoder, exhaustive domination and independence
searches, an independently written coloring backtracker, and a direct
synchronous one-guard greatest-fixed-point deletion.

It reconstructs the graph

`OQifur}UO]}iTij]tpo}v`

and obtains:

| quantity | clean-room result |
|---|---:|
| order, size | \(16,71\) |
| \((\gamma,\alpha,\gamma^\infty,\theta)\) | \((3,3,3,3)\) |
| dominating triples | \(304\) |
| literal greatest eternal triple family | \(304\) |
| physical link \(B\) | \(\{5,7,9,11,13\}\) |
| \(H[B]\)-edges | \(57,59,11\,13\) |

The lower bound \(\theta\ge3\) also follows independently from
\(\alpha=3\), while the replay supplies an explicit 3-coloring of
\(\overline G\).

For root \(\{0,1,10\}\) and target \(6\), the target palette is all three
colors.  The restricted peelings are:

| color | initial states | deletion rounds | kernel | selected-start rank |
|---:|---:|---|---:|---:|
| \(0\) | 301 | \(26,81,132,62\) | 0 | 1 |
| \(1\) | 301 | \(28,74,49\) | 150 | survives |
| \(10\) | 300 | \(29,81,128,62\) | 0 | 1 |

The three displayed terminal palettes are exactly
\[
Q(11)=\{0,1\},\quad Q(7)=\{1,10\},\quad Q(5)=\{0,10\}.
\]
For colors \(0\) and \(10\), the named predecessors have rank zero, the
secondary responses miss exactly vertices \(8\) and \(4\), and the only
dominating retained response to the terminal attack is the banned corridor
move.  For color \(1\), the named predecessor survives and the secondary
state \(\{0,3,7\}\) is in the 150-state kernel.  Every named diamond,
move edge, ban membership, palette, missed set, and all twelve claimed
occupancy distinctions were recomputed.

The color-1 row is geometric boundary data, not a C-149 annihilation terminal.
The candidate says so explicitly.  Therefore Proposition 3.1 correctly
refutes only a rank-free/static elimination of cyclic doubleton corridor
geometry.

The independent stdout SHA-256 is
`2aadb3446aad5074588631eeca448bc50d6c746232cdd749166c77e37f2596e1`.

## 7. Adversarial local countermodel search

`search_local_countermodels.py` exhausts arbitrary graph completions of the
named roles while deliberately weakening greatest-family membership to mere
domination.  This makes the local search stronger for falsification than the
stated lemma.

- Among all 8,192 seven-vertex direct-root completions, 1,768 have the local
  rank-zero corridor premises.  None has a dominating unbanned secondary
  response.
- Among all 1,024 seven-vertex nonroot completions, 240 have the local
  rank-zero premises and 16 have a secondary incidence.  Every alternate is
  nondominating and every missed witness has the claimed location and
  adjacency.
- Among all 131,072 eight-vertex nonroot completions, 28,288 have the local
  rank-zero premises and 3,264 have secondary incidences.  This includes 64
  rows with both secondary colors.  There are no nondomination failures,
  witness-collision failures, or intersections between the two secondary
  witness sets.

The exact equality/full-target subfilter happens to be empty at these small
orders, so it is not used as evidence.  The nonvacuous weakened local sweeps
test the proof mechanism; the separate order-16 replay supplies the exact
equality control.

The local-search stdout SHA-256 is
`1c2fd5a8673256a1a0db81197fbee864a43f90d61fc3cb48cf42a03be1177a0d`.

## 8. Reproduction

From the repository root:

```text
gamma_theta_eternal_domination/reviews/full_list_nonsingleton_terminal_hostile/verify_strict.sh
```

The strict runner freezes the candidate and C-149 source bytes, replays both
the candidate and independent control implementations, reruns the exhaustive
local search, and checks every expected output hash.

