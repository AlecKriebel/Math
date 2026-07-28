# Hostile review: physical response ports and bicycle shortening

Date: 2026-07-28 (PDT)

## Verdict

**PASS, unconditional relative to the named accepted dependencies.**

On the frozen candidate bytes, the same-type-mate lemma, universal
side-purity theorem, transversal completion theorem, signed-coloring
equivalence, shortest-unbalanced-cycle theorem, and five-skeleton
classification are correct.  No hidden use of an absent family response
as a graph nonedge was found.

The accepted conclusion is deliberately limited:

\[
 \text{an inconsistent exact-two-list \(k=3\) system}
 \Longrightarrow
 \text{one of five short signed type skeletons}.
\]

The candidate does not exclude those five skeletons.  It therefore does
not finish the exact-two-list branch, prove the complete \(k=3\) case, or
resolve the gamma--theta conjecture.

## Frozen byte binding

The independently checked candidate bytes are:

| candidate artifact | SHA-256 |
|---|---|
| `math/working/physicality_bicycle_endgame/NOTE.md` | `b282d96e1582ff9100bbdf6a81d9f1b29d2d76a3565e4a0d3cfbbb08886d0d91` |
| `math/working/physicality_bicycle_endgame/MANIFEST.json` | `039637c213d3236fa630df0223f3ef320f150b571c4fa15049ee034384317873` |
| `math/working/physicality_bicycle_endgame/RESEARCH_LOG.md` | `89d0434a31f23c3dd82efd90797a4101111f604a4ea00b0e03b3a907f5a4c396` |
| `math/working/physicality_bicycle_endgame/controls.json` | `f8f2e087b57590fb09fafd679fd75aba8a786fff14fca3729cf9b30f16220489` |
| `math/working/physicality_bicycle_endgame/search_static.py` | `f3c95be6ccd830750f29591928e4ad628ee053636637ca276215cb9755d048c3` |
| `math/working/physicality_bicycle_endgame/verify.py` | `6dc1d0bd32d601a99b58f1049f4367e3181dbef0f46130c92d683f79111323b3` |

The prerequisite statements were reread rather than inferred from the
claims ledger:

| dependency | SHA-256 |
|---|---|
| C-111 physicality, `math/working/dynamic_type_sparsity/NOTE.md` | `f3309daa2497a10c978fac28286959d6ec2fb52e8438c727cdf2eafce89aa1a7` |
| C-079 odd fan, `math/working/k3_long_bicycle_connectors/NOTE.md` | `d3a23bb0171a047a85f2a05c5ccb5faeef0c0c7ceb6d7bb139c6a7a86b8b1f10` |
| C-079 side-purity consequence, `math/working/k3_side_purity_cap_cycle/NOTE.md` | `64312289f6d3d87a4c302692c92901caeb9788b16354493e07be01920549f11b` |
| frozen projection, `math/working/k3_cross_state_attack.md` | `3e87ca4e7c04987c2f56576c4e8b0f28113e254fdb1a024b4da7a3e0d6bf4c68` |
| maximum-independent-state forcing | `08cfa394f5fb1778beac62d752ec2700027ac7710071ed635d9e914f71133e8e` |

## Hypothesis audit

Let \(\mathcal F\) be an eternal family of triples containing the
independent state \(S=\{a,b,c\}\), assume \(\gamma(G)=3\), and assume that
every outside response list has size exactly two.  The candidate sometimes
writes the full equality

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3.
\]

This is not an extra hidden assumption.  The independent triple gives
\(\alpha(G)\geq3\), the specified eternal triple-family gives
\(\gamma^\infty(G)\leq3\), and the accepted chain
\(\alpha\leq\gamma^\infty\) forces both values to be three.

C-111 then gives the exact physical identity

\[
 L(x)=N_G(x)\cap S.
\]

Thus a type-\(t\) vertex is joined in \(H=\overline G\) to exactly anchor
\(t\).  This identity, and not mere omission from a family list, is what
supports every anchor incidence used below.

For a fixed \(t\), the accepted frozen projection on

\[
 (S-\{t\})\cup W_t
\]

has complement bipartite.  Its anchor edge is disconnected from \(W_t\):
every vertex of \(W_t\) is adjacent in \(G\) to both other anchors.
Therefore each \(H[W_t]\) is bipartite exactly as used in the candidate.

## Same-type mate and universal side-purity

Take \(q\in W_t\).  The pair \(\{t,q\}\) does not dominate because
\(\gamma(G)=3\), so it has a common \(H\)-neighbor \(p\) outside the pair.
Neither other anchor can be \(p\), since both are adjacent to \(q\) in
\(G\).  Hence \(p\notin S\).  The literal edge \(tp\in E(H)\) and C-111
give \(t\notin L(p)\), so \(p\in W_t\).  The mate is distinct from \(q\)
and satisfies \(pq\in E(H)\).  Lemma 2.1 is valid.

Now fix a component \(K\) of \(H[W_t]\) and an arbitrary outside vertex
\(q\).

- If \(q\in W_t\), it is either outside \(K\), with no neighbor in \(K\),
  or inside \(K\), where bipartiteness places all its neighbors on the
  opposite side.
- If \(q\in W_r\) for \(r\ne t\), its same-type mate \(p\in W_r\) has
  \(t\in L(p)\) and \(pq\in E(H)\).  The accepted C-079 side-purity
  theorem applies with \(p\) as the required \(t\)-positive neighbor.

All quantifiers and distinctness requirements of the imported theorem
match.  Thus every outside vertex has a side-pure neighborhood in every
type component.

## Transversal completion

Let \(xy\in E(H)\) with distinct types \(r\) and \(s\), and let \(t\) be
the third type.  Since \(\gamma(G)=3\), the pair \(\{x,y\}\) has a common
complement neighbor \(z\).

No anchor is common:

- anchor \(r\) is an \(H\)-neighbor of \(x\) but a \(G\)-neighbor of \(y\);
- anchor \(s\) is a \(G\)-neighbor of \(x\) but an \(H\)-neighbor of \(y\);
- anchor \(t\) is a \(G\)-neighbor of both.

Thus \(z\) is outside.  If \(z\) had type \(r\), the edge \(xz\) would put
\(x,z\) on opposite sides of one component of \(H[W_r]\), while \(y\)
sees both in \(H\), contradicting universal side-purity.  Type \(s\) is
symmetric.  Therefore every such common neighbor has type \(t\), and in
particular at least one literal transversal triangle \(xyz\) exists.

The proof establishes the stronger “every common neighbor” wording, not
only existence.  It also uses the original edge \(xy\); no representative
substitution or unsupported clause-edge transport occurs.

## Exact signed-coloring dictionary

Fix the anchor colors \(0,1,2\) cyclically.  A type-\(t\) outside vertex
has exactly the two colors \(t-1,t+1\); call their choices chirality
\(0,1\).

- On a same-type edge, proper coloring is exactly opposite chirality.
- On a cross-type edge, transversal completion produces a triangle with
  one vertex of each type.  Its only two allowed proper colorings give
  equal chirality at all three vertices.

Conversely, opposite chirality on a same-type edge gives the two distinct
allowed colors, while equal chirality at two different types always gives
distinct colors.  Anchor spokes are proper because C-111 says that a
type-\(t\) vertex is adjacent in \(H\) to exactly anchor \(t\).

Hence proper three-colorings extending the anchor triangle are in
bijection with solutions of

\[
 \chi(x)\oplus\chi(y)
 =
 \begin{cases}
 1,&\tau(x)=\tau(y),\\
 0,&\tau(x)\ne\tau(y).
 \end{cases}
\]

The clean-room checker also tested this equivalence independently on all
\(2^9=512\) allowed assignments of each control, with zero mismatches.

## Shortest-cycle proof

An inconsistent signed system has a simple unbalanced cycle.  Choose one
of minimum length \(C\).  Any chord splits \(C\) into two shorter cycles;
the chord is counted twice in the xor of their parities, so exactly one
would be unbalanced.  Therefore \(C\) is chordless.

The typed-pair selection for \(|C|\geq6\) is complete.

1. For length six, if every opposite pair has the same type, the type
   word repeats after three positions.  Each same-type status is then
   repeated in an opposite edge, so the parity is even.
2. For length at least seven, suppose every pair whose two cyclic
   distances are at least three has the same type.  In particular,
   \(\tau(x_i)=\tau(x_{i+3})=\tau(x_{i+4})\) for every \(i\).  Consecutive
   vertices therefore all have one type.  Such a cycle lies in a
   bipartite \(H[W_t]\), so it cannot be unbalanced.

Thus an unbalanced \(C\) has distinct-type vertices \(x,y\) with both
cyclic distances at least three.  Their two arcs have length at most
\(|C|-3\).  The non-dominating pair condition supplies a two-edge
complement path \(R=xzy\) with \(z\) outside \(S\).

The delicate point is why \(z\notin V(C)\).  If \(z\) were on the
chordless cycle, each of \(xz,yz\) would have to be a cycle edge;
otherwise it would be a chord.  Then one \(x\)-\(y\) arc would have length
two through \(z\), contradicting the choice of \(x,y\).  Hence both
unions of \(R\) with a cycle arc are simple shorter cycles.  Their signed
parities xor to the parity of \(C\), because the two edges of \(R\) occur
twice.  One is a shorter unbalanced cycle, a contradiction.

This proves the length-at-most-five conclusion.  As extra falsification,
the independent checker enumerated all 796,797 type words of lengths
six through twelve.  Among 395,643 unbalanced words, 395,634 have the
required distinct-type pair and the remaining nine are the three
constant words at each odd length, precisely the cases forbidden by
projection bipartiteness.

## Canonical words and residual scope

Independent enumeration under all type permutations, rotations, and
reversals gives:

\[
\begin{array}{c|l}
3&000,\ 001\\
4&0012\\
5&00000,\ 00001,\ 00011,\ 00101,\ 00102,\ 00121.
\end{array}
\]

The exclusions are exact:

- `000` and `00000` are odd cycles in one bipartite type projection;
- in `001`, the distinct-type vertex sees both sides of the displayed
  same-type edge;
- in `00001`, the distinct-type vertex sees the two ends of an odd
  three-edge path in one type component.

Universal side-purity excludes the latter two.  The exact residual list is

\[
 0012,\qquad00011,\qquad00101,\qquad00102,\qquad00121.
\]

No witness-collision claim is needed for this classification, and no
residual skeleton is declared impossible.

## Clean-room control audit

`independent_check.py` imports no campaign evaluator, does not read the
candidate `controls.json`, and independently implements short graph6
decoding and re-encoding, complement construction, exhaustive domination
and independence, maximal-independent domination, exact coloring,
greatest-fixed-point eternal kernels, response lists, type projections,
side-purity, transversal completion, signed cycles, and word orbits.

For

```text
KBjB\z[^||Z[
```

it reconstructs a 12-vertex graph with 42 edges and complement with 24
edges, and obtains

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,4).
\]

There are exactly 9 dominating pairs and 163 dominating triples.  All 163
triples survive the greatest-fixed-point deletion and satisfy all 1,467
unoccupied-attack obligations.  The retained-response count histogram is

\[
 1:798,\qquad2:561,\qquad3:108.
\]

The nine root lists are exactly the displayed physical two-lists.  All
projection components are bipartite and universally side-pure, every cross
edge has a third-type transversal witness, and the shortest unbalanced
cycle has length six.

For

```text
KBjB\j[Z||ZW
```

it reconstructs 39 graph edges and 27 complement edges, and obtains

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,4,4).
\]

There are no dominating pairs and exactly 136 dominating triples.  The
triple kernel deletes in simultaneous rounds

\[
 34,\ 56,\ 46
\]

and is empty; the four-guard kernel has 459 states.  All direct root swaps
give the displayed exact physical two-lists, every port has a same-type
mate, all type projections are bipartite and universally side-pure, and
every cross edge has only third-type outside common witnesses.  The
complement is exactly four-chromatic and its shortest unbalanced cycle has
length five.

The two controls therefore have the advertised sharp boundary:
the first has complete triple closure but \(\gamma=2\), while the second
has \(\gamma=3\) and all static conclusions but no eternal triple-family.

## Adversarial conclusions

The following possible failure modes were specifically checked and did not
occur:

- an anchor masquerading as a common-neighbor witness;
- failure to prove a same-type mate is outside \(S\);
- invoking side-purity without a distinct positive neighbor;
- treating response omission as physical nonadjacency before applying
  C-111;
- replacing a cross-clause edge by a representative edge;
- deriving two-sided parity from one binary clause instead of the full
  transversal triangle;
- allowing the gamma-supplied shortcut vertex to lie on the chosen cycle;
- overlooking the length-six period-three case;
- omitting a type-word orbit or eliminating one without either
  bipartiteness or side-purity; or
- importing all-guards-move dynamics into either exact kernel.

No correction or qualification beyond the candidate's own stated scope is
required.

## Reproduction

From the campaign root, run:

```text
python3 -I -B -W error \
  reviews/physicality_bicycle_hostile/independent_check.py
```

On the reviewed bytes, the SHA-256 of stdout is

```text
73fa79bf8c1f64b3b6d8a1b8675099731f3be737ee45b7618485e418545fcce3
```

The checker SHA-256 is

```text
436352c146f80758d892edf5af706d4d196970f789503bdf461bac012a1d79de
```
