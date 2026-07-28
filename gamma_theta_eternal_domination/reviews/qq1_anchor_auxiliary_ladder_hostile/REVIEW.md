# Hostile review: QQ1 anchor–auxiliary boundary control

Date: 2026-07-28 PDT

## Verdict

**UNCONDITIONAL PASS.**

Candidate commit `6a69254e` correctly refutes the proposed
anchor–auxiliary shortcut with one fixed order-\(18\) graph.  The graph
has exact parameter vector

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)=(2,3,3,3,3),
\]

realizes every named local QQ1, C-166, and C-167 obligation in the
candidate, has no dominating pair incident with
\(T=\{x,p,q\}\), and nevertheless has exactly thirty dominating pairs
outside \(T\).  It is a \(\gamma=2\) boundary control, not a
counterexample to the gamma–theta conjecture.

Candidate note SHA-256:
`c431772c099e92df63749e4b364a3820403e507bb440bf4c535bd8e4a50e92ee`.

Candidate manifest SHA-256:
`eaa02cbf2abc9249dee09e0bdfb591b9cd5c87a1970c3086aac82f2674ecda68`.

## Independent graph and parameter replay

The clean-room verifier does not import the candidate verifier, a
campaign evaluator, or the discovery encoder.  It uses pinned nauty
`showg` to decode each graph6 record into adjacency sets, represents
guard states as `frozenset` objects, and uses a separately written
synchronous fixed-point loop.

It independently decodes

```text
QslallyN\~Y^v^|^z~~V|ve~^}G
```

and

```text
QpMu]qnvvJb~Tz]mnx~nnZ~|~~W
```

as graphs of order \(18\) and size \(114\).  A color-refinement-guided
exact isomorphism search finds the labeled-to-canonical map

```text
(6,4,0,12,1,2,3,5,7,10,15,11,16,8,17,9,13,14).
```

Pinned nauty 2.9.3 `labelg` sends both records to the stated canonical
record, so canonicalization and idempotence both pass.  The labeled
graph6 and sorted edge-list hashes match the candidate.

Direct subset enumeration gives

- \(\gamma=2\);
- \(i=3\);
- \(\alpha=3\), with exactly thirteen independent triples and no
  independent four-set.

All thirteen independent triples lie in the greatest eternal
three-family.  The displayed three-clique partition is valid, while
\(\alpha=3\) supplies the matching lower bound, so \(\theta=3\).

The literal one-guard kernels have sizes \(0,0,473\) for one, two, and
three guards.  There are \(30\) initial dominating pairs, and all are
deleted in the first synchronous round.  There are \(642\) initial
dominating triples; their deletion-wave sizes are

```text
2, 8, 11, 28, 33, 18, 17, 34, 18.
```

Thus \(\gamma^\infty=3\).

## Rank and activity audit

The review uses the same explicit rank convention as the candidate:
rank one means deletion from the full set of dominating triples in the
first synchronous wave.  For \(B=\{u,p,q\}\), the attack at \(r\) has
all three guards graph-eligible, and the three successors miss exactly
\(x,b,c\), respectively.  Hence \(\rho(B)=1\).  The dominating state
\(O=\{u,r,d\}\) is deleted in the third wave, so \(\rho(O)=3\).

The candidate's displayed \(u\to x\) activity root is literal:

```text
{u,b,w} -> {x,b,w}
```

has retained source and successor.  Exhausting all independent roots
gives two \(u\to x\) roots, and both successors survive.  Conversely,
there are three independent \(x\to u\) roots and all three successors
are omitted.  In particular,

```text
{x,p,q} -> {u,p,q}=B
```

is the displayed reverse failure.  Therefore the one-sided activity
interpretation is correct; it is not inferred merely from an edge or
from a missing response list.

## QQ1, C-166, and C-167 scope

The named QQ1 edges and nonedges all match.  The relevant completion
sets are singletons:

\[
C_{xr}=\{d\},\quad W_{ud}=\{w\},\quad W_{ux}=\{z\},\quad
C_{uw}=\{b\},\quad C_{dw}=\{16\}.
\]

Consequently the universal completion quantifiers in the accepted
C-166/C-167 conclusions collapse to the displayed named states in this
control.  The verifier finds all of

\[
T,U,R,I,A,K,E,F,\{u,x,z\},\{u,w,z\},
\{u,w,b\},\{d,w,16\},\{b,w,16\}
\]

in the literal greatest family, while \(B\) and \(O\) are omitted with
the stated ranks.  The bridge \(\{u,w,z\}\) covers \(b\) through \(z\)
and \(c\) through \(w\).  Since both \(ud\) and \(wz\) are edges, the
cycle

\[
u-d-z-w-x-u
\]

has all five cycle edges and none of its five chords.  All independent
activity roots on the two singleton outer edges \(bd\) and \(16u\)
also survive in both directions.  Thus the candidate's phrase “the
full accepted local QQ1 dynamics” is justified for this fixed graph;
it does not silently replace a universal completion set by one selected
member.

## Anchor protection and witness recycling

Exhaustive pair enumeration reproduces the candidate's complete
thirty-pair list.  Twenty pairs are core–auxiliary and ten are
auxiliary–auxiliary.  None has an endpoint in
\(T=\{x,p,q\}\), while \(\{u,14\}\) is one explicit dominating pair.
This proves directly that protecting every pair touching \(T\) does
not imply \(\gamma=3\).

The six displayed common-nonneighbor identities are exact.  In
particular,

\[
p:11\mapsto16\mapsto11,\qquad
p:14\mapsto17\mapsto14,\qquad
q:5\mapsto15\mapsto5
\]

are literal two-cycles.  They invalidate a descent step that assumes
successive common-nonneighbor witnesses relative to the fixed anchors
must be fresh.  They do not rule out a different global descent using
all non-dominating pairs, and the candidate does not claim otherwise.

## Scope and solver audit

There is no duplicated scope quote in committed Section 6: the first
quote protects only \(p,q\) against auxiliary partners, while the
second protects every pair touching \(T\).  Each occurs exactly once.

`ABLATION_RESULTS.json` labels the unlogged order-\(16\) base and
ablated UNSAT outcomes `OBSERVED_DISCOVERY_ONLY` and expressly claims
no finite or all-order theorem.  The note and manifest repeat that
limitation.  No DRAT, LRAT, FRAT, or other proof log is present, and
none is represented as a certificate.  The order-\(18\) SAT run is
used only as provenance for a graph whose mathematical properties are
recomputed exactly.

The refutation is therefore narrow but rigorous:

- refuted: the named local QQ1/C-166/C-167 obligations plus complete
  pair protection at \(T\) force \(\gamma=3\);
- not refuted: any statement that assumes \(\gamma=3\), equality, or
  full non-domination of every pair;
- not proved: an order-\(16\) or order-\(17\) exclusion, elimination of
  QQ1 under equality, complete \(k=3\), or the universal conjecture.

Reproduce the review from the campaign directory with:

```text
sh reviews/qq1_anchor_auxiliary_ladder_hostile/verify_strict.sh
```
