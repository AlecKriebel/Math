# Hostile review: two-response replication and the order-14 boundary

## Verdict

**PASS.**

The current bytes of the human note prove Lemma 2.1, Corollary 2.3,
Theorem 3.1, and the stated order-\(15\) floor for the **exact**
separated-port pattern.  The argument uses literal closure of a retained
one-guard family and never converts a missing family response into a graph
nonedge.  A clean-room bit-mask verifier independently reconstructs the
14-vertex control and produces a result file byte-for-byte identical to the
source result.

This verdict does **not** promote the corollary to an exclusion of all
14-vertex equality graphs or all 14-vertex response patterns.  Its exact
hypotheses are essential.

## Frozen source bytes reviewed

| artifact | SHA-256 |
|---|---|
| `math/working/separated_core_n14_attack/NOTE.md` | `a619c7acf0dfccbc5767379f68d25f6272d3318db33e433cede39aa70b5ce279` |
| `math/working/separated_core_n14_attack/verify.py` | `482809984835c0f84c275f97fe049171934ab551eff50bf451eaed5cb5edebe2` |
| `math/working/separated_core_n14_attack/result.json` | `f4b1ed7caf63d93798134353233306402202d2ff1439f7eef3f82068e8bfa489` |

The review artifacts are:

| artifact | SHA-256 |
|---|---|
| `reviews/two_response_replication_hostile/independent_check.py` | `b5eb2f7f1c1fada8e765d2799710347211ae46a864bdfb120c5bc81ca847a0fc` |
| `reviews/two_response_replication_hostile/independent_result.json` | `f4b1ed7caf63d93798134353233306402202d2ff1439f7eef3f82068e8bfa489` |

The identical source and independent result hashes are a byte-level
comparison, not merely agreement on the parameter tuple.

## Human-proof reconstruction

Let \(S=\{a,b,c\}\) be an independent retained triple, let \(H=\overline G\),
and let \(Q_S\) and \(A=V(G)-(S\cup Q_S)\) have the meanings in the note.
Because \(\gamma(G)\geq3\), every two-vertex set fails to dominate, hence
every distinct pair has an outside vertex nonadjacent to both in \(G\), or
equivalently a common neighbor in \(H\).  Also,
\(i\in L(t)\) implies \(it\in E(G)\): in \(S-i+t\), the other two anchors
are nonadjacent to the omitted anchor \(i\), so only \(t\) can dominate it.

### Lemma 2.1

1. From the nondominating pair \(\{c,x\}\), choose
   \(y\in N_H(c)\cap N_H(x)\).  Since \(x\in Q_S\), this \(y\) is outside
   \(S\); since \(cy\in E(H)\), it is outside \(Q_S\).  Thus \(y\in A\).

2. The retained states \(D_a=\{b,c,x\}\) and \(D_b=\{a,c,x\}\) dominate
   \(y\).  In both states \(c\) and \(x\) miss \(y\), forcing respectively
   \(by,ay\in E(G)\).  Therefore
   \(N_H(y)\cap S=\{c\}\).

3. From the nondominating pair \(\{c,y\}\), choose
   \(z\in N_H(c)\cap N_H(y)\).  The already established adjacencies
   \(ay,by\in E(G)\), the absence of loops, and \(cQ_S\subseteq E(G)\)
   show that \(z\notin S\cup Q_S\) and \(z\ne y\).  Hence \(z\in A-\{y\}\).
   Since \(S\) dominates and \(cz\in E(H)\), its only possible signatures
   are \(\{c\},\{a,c\},\{b,c\}\).

4. If the signature is \(\{a,c\}\), domination of \(D_b\) forces
   \(xz\in E(G)\).  Attack the unoccupied vertex \(z\) from
   \(D_a=\{b,c,x\}\).  The \(c\)-guard cannot move because \(cz\in E(H)\);
   the \(x\)-move leaves \(\{b,c,z\}\), which misses \(a\); and the
   \(b\)-move leaves \(\{c,x,z\}\), which misses \(y\) because
   \(cy,xy,zy\in E(H)\).  These are all three possible one-guard responses.
   The signature \(\{b,c\}\) is eliminated by the symmetric attack from
   \(D_b\).  Every rejection here is witnessed by an undominated vertex.

5. Thus the signature of \(z\) is \(\{c\}\).  Attack \(z\) from each of
   \(D_a,D_b\).  The \(c\)-guard again cannot move.  Moving the other anchor
   gives \(\{c,x,z\}\), which misses \(y\).  Literal family closure
   therefore forces the \(x\)-guard to move in both attacks.  Consequently
   \(xz\in E(G)\) and both \(S-a+z,S-b+z\) belong to the family.

The attack is legal in each use: \(z\in A\), while \(x\in Q_S\), and
\(z\) is distinct from the anchors.  Exactly one guard moves along one
edge.  The proof establishes the displayed distinctness, signature, and
edge/nonedge claims of (2.2).

### Corollary 2.3

If \(L(t)=\{a,b\}\), positive membership first gives
\(at,bt\in E(G)\).  If \(ct\in E(H)\), then \(t\) itself already has
signature \(\{c\}\).  Otherwise \(t\in Q_S\), so Lemma 2.1 supplies a
vertex \(z\) with \(\{a,b\}\subseteq L(z)\) and \(cz\in E(H)\).  The
positive-membership implication above prevents \(c\in L(z)\), yielding
the exact list.  Thus this corollary infers a missing response only after
an actual graph nonedge has been proved; it does not reverse that
implication.

### Theorem 3.1

Applying Lemma 2.1 to the \(\{a,b\}\) list produces two distinct
signature-\(\{c\}\) vertices.  Its cyclic form applied to the
\(\{b,c\}\) list produces two distinct signature-\(\{a\}\) vertices.
Different signatures make these four vertices pairwise distinct.

For \(\{b,q\}\), choose a common \(H\)-neighbor \(p_q\).  It lies in
\(A\), and domination by \(\{b,c,q\}\) restricts its signature to
\(\{b\}\) or \(\{a,b\}\).  Similarly \(p_v\in A\) has signature
\(\{b\}\) or \(\{b,c\}\).  Both are new relative to the first four.
If they differ, the count is six.  If they coincide at \(p\), the
intersection of the two signature alternatives forces
\(\sigma(p)=\{b\}\).  A common \(H\)-neighbor \(r\) of \(\{b,p\}\) is in
\(A\), has a signature containing \(b\), is distinct from \(p\), and is
distinct from the four pure-\(a\)/pure-\(c\) vertices.  The count is again
six.  This remains valid when \(q=v\).

Therefore \(|A|\geq6\), and the disjoint decomposition
\(V(G)=S\mathbin{\dot\cup}Q_S\mathbin{\dot\cup}A\) gives
\(|V(G)|\geq |Q_S|+9\).

The exact separated-port corollary uses only these checked facts:
the six named old outside vertices lie in \(Q_S\),
\(\{a,b\}\subseteq L(q)\), and
\(\{b,c\}\subseteq L(v_1)\).  Hence \(|Q_S|\geq6\) and the theorem gives
\(n\geq15\).  Fullness of the separate vertex \(x\) is unnecessary.
Without the common reference state, neutrality of both ports, overlapping
positive pairs, or \(\gamma(G)\geq3\), this corollary does not apply.

## Independent finite-control audit

`independent_check.py` imports no source/search/verifier module.  It:

- decodes the short graph6 bit stream into integer adjacency masks;
- exhaustively searches subsets for \(\gamma,\alpha\), and \(i\), using
  maximality directly for \(i\);
- computes \(\theta\) by an anchored dynamic program over partitions into
  cliques of \(G\), and separately validates the supplied four-part
  complement coloring;
- computes the simultaneous greatest fixed point of the exact one-guard
  transition relation, with attacks only on unoccupied vertices and one
  adjacent guard replaced by the attacked vertex;
- reconstructs \(Q_S\), all five displayed signatures, the exact 14-state
  seed/list table, and the four explicit failed attacks.

The independent output is

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,4,4),
\]

with 55 graph edges and 36 complement edges.  There are 200 dominating
triples, deleted in simultaneous rounds \(140,60\).  There are 868
dominating four-sets; 12 are deleted and 856 survive.  Thus the
three-guard kernel is empty and the four-guard kernel is nonempty.

The reconstructed neutral set is exactly
\(\{3,4,5,6,7,8\}\), and the remaining signatures at vertices
\(9,\ldots,13\) are respectively
\(\{b,c\},\{c\},\{a\},\{a,b\},\{b\}\).  All 14 selected seed states
dominate.

For the two attacks displayed in the prose:

- from \(\{0,2,6\}\) at 9, guard 0 is the only anchor/port alternative
  besides guard 6 and leaves vertex 10 undominated; guard 6 leaves vertex
  1 undominated; guard 2 is nonadjacent to 9;
- from \(\{0,2,8\}\) at 12, guard 2 leaves vertex 11 undominated; guard 8
  leaves vertex 1 undominated; guard 0 is nonadjacent to 12.

The other two source-result attack records were also reconstructed
exactly.  This confirms that domination of the selected direct swaps is
strictly weaker than literal one-guard family closure.

## Reproduction

From the repository root:

```text
python3 gamma_theta_eternal_domination/reviews/two_response_replication_hostile/independent_check.py gamma_theta_eternal_domination/reviews/two_response_replication_hostile/independent_result.json
python3 gamma_theta_eternal_domination/reviews/two_response_replication_hostile/independent_check.py gamma_theta_eternal_domination/math/working/separated_core_n14_attack/result.json
python3 gamma_theta_eternal_domination/math/working/separated_core_n14_attack/verify.py --check gamma_theta_eternal_domination/math/working/separated_core_n14_attack/result.json
```

All three commands pass on the reviewed bytes.
