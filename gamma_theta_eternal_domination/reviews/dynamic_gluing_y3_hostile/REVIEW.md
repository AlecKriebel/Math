# Hostile review: the dynamic fate of the static \(Y_3\) obstruction

## Verdict

**PASS.**

I found no correction required in
`math/working/dynamic_gluing_y3/NOTE.md` at SHA-256

`ff559cb949c5427bc33e75a43deba38a8284e78c380a01bb97488a82a59798f9`.

The exact accepted scope is:

> Let \(S=\{a,b,c\}\) be an independent state of an arbitrary specified
> one-guard eternal family \(\mathcal F\) of triples, and let
> \(x_0x_1x_2x_3\) be an induced path in \(H=\overline G\).  If the four
> static dominating-swap lists are
> \[
> \{a\},\quad \{a,c\},\quad \{b,c\},\quad \{b\},
> \]
> then the family-response lists are exactly the same.  Under
> \(\gamma(G)=\alpha(G)=\gamma^\infty(G)=3\), the two failed endpoint
> middle-color swaps have nonempty, disjoint defect-witness sets.  Combining
> one witness from each with the five witnesses already separated by C-072
> gives \(|V(G)|\ge14\).

This is a conditional theorem about one exact embedded static \(Y_3\).
It does not exclude such an embedding at order \(14\) or above, prove
\(\mathsf{GL}(3)\), prove the complete parameter-three case, improve the
order frontier for every possible counterexample, or resolve the universal
gamma--theta conjecture.  The candidate states these limits correctly.

## Frozen inputs

| artifact | SHA-256 |
|---|---|
| candidate note | `ff559cb949c5427bc33e75a43deba38a8284e78c380a01bb97488a82a59798f9` |
| candidate checker | `9aa707fc7d29a7c4109c9f7495558ce0258fb291996eed545da48cea599dded1` |
| candidate research log | `763f204c6fb3f49f0f6c8da1a83131e30424465b6fd628c5d18424f79ce5807b` |
| C-067 mixed-\(P_4\) source | `3af645890638f07fa38b294def7967679e280a6447173aa320e8715da714d92c` |
| C-070 witness-saturation source | `079c3ee0e880eb211f7e7460193e9c4c8212d70350965e668eb462f4f0a4db04` |
| C-072 end-witness source | `0c6a3de00f8e4daa53f4602c437ed51a22da911cfdff3f42445550b07e3430bb` |
| ridge-covariance source | `e30a0ac4e028deefbf4c4533646ff934b617d8ff61dce38ec2389a50d622d8e7` |
| independent hostile checker | `6b275d9eff99b83d7ef641fb9ef9025d924aa50f5542a022fd1c01ded5f5c407` |
| hostile checker output | `ecce123e4fa79e2cf4092acd6b75a9b3dceddccaa46ed315a90d27245fd0e994` |

I read the candidate, the three proof-bearing predecessor notes, their
accepted hostile reviews, and the response-covariance source.  The
clean-room checker imports none of them and uses ordinary adjacency
dictionaries and `frozenset` states rather than the candidate's bit masks.

## 1. Static lists and family lists

The two list notions are kept separate correctly.

For \(x\notin S\),

\[
L^{\mathcal F}(x)
=\{u\in S:S-u+x\in\mathcal F\}
\]

records retained family membership, whereas

\[
L^{\rm stat}(x)
=\{u\in S:ux\in E(G),\ S-u+x\text{ dominates }G\}
\]

records every legal dominating direct swap whether or not it is retained.
If \(S-u+x\in\mathcal F\), the state dominates the omitted anchor \(u\).
The two retained anchors are nonadjacent to \(u\), since \(S\) is
independent, so \(xu\in E(G)\).  Family membership also supplies
domination.  Therefore

\[
L^{\mathcal F}(x)\subseteq L^{\rm stat}(x)
\]

exactly as claimed.

Every \(L^{\mathcal F}(x_i)\) is nonempty: \(x_i\) is unoccupied at the
retained state \(S\), and one-guard closure must retain a direct successor.
Consequently the singleton endpoint static lists immediately force

\[
L^{\mathcal F}(x_0)=\{a\},\qquad
L^{\mathcal F}(x_3)=\{b\}.
\]

No step silently turns a negative static-list entry into a graph nonedge.
The four uncertain anchor/path adjacencies used later remain uncertain
throughout the local completion argument.

## 2. Static-to-family rigidity attack audit

The proof that the two internal family lists are full is sound for an
arbitrary specified family.

1. Attack \(x_0\) from \(S\).  The endpoint list forces the retained state
   \[
   A_0=\{b,c,x_0\}.
   \]

2. Attack the unoccupied \(x_1\) from \(A_0\).  The guard \(x_0\) cannot
   move because \(x_0x_1\in E(H)\).  A successor obtained by moving \(b\)
   would be \(\{c,x_0,x_1\}\).  It misses reference anchors \(a,b\), while
   \[
   L^{\mathcal F}(x_0)\cup L^{\mathcal F}(x_1)
   \subseteq\{a,c\},
   \]
   so arbitrary-state restoration rejects it.  Since \(cx_1\in E(G)\)
   from the positive static incidence, closure forces
   \[
   Q_L=\{b,x_0,x_1\}\in\mathcal F.
   \]
   Restoration at \(Q_L\) then forces
   \(c\in L^{\mathcal F}(x_1)\).

3. Reflecting the labels gives
   \(c\in L^{\mathcal F}(x_2)\) and the retained state
   \[
   Q_R=\{a,x_2,x_3\}.
   \]

4. Suppose \(b\notin L^{\mathcal F}(x_2)\), so the list is exactly
   \(\{c\}\).  Attack \(x_0\) from \(Q_R\).  All three graph moves exist:
   \(ax_0\) is a positive static incidence and
   \(x_0x_2,x_0x_3\in E(G)\) by inducedness of the complement path.
   Moving \(x_2\) gives \(\{a,x_0,x_3\}\), whose two outside lists
   \(\{a\},\{b\}\) cannot restore \(c\).  Moving \(x_3\) gives
   \(\{a,x_0,x_2\}\), whose two outside lists
   \(\{a\},\{c\}\) cannot restore \(b\).  Closure therefore forces the
   remaining response \(a\to x_0\), retaining
   \[
   R=\{x_0,x_2,x_3\}.
   \]

5. Attack the unoccupied \(x_1\) from \(R\).  The guards \(x_0,x_2\)
   are nonneighbors of \(x_1\), while \(x_3x_1\in E(G)\).  The unique
   graph successor is \(\{x_0,x_1,x_2\}\).  It misses all three anchors,
   but its outside lists cover only \(\{a,c\}\), contradicting
   restoration.

Thus \(b\in L^{\mathcal F}(x_2)\); reflection gives
\(a\in L^{\mathcal F}(x_1)\).  Every attack above is unoccupied and every
response moves exactly one guard along a graph edge.

As a separate finite stress test, the clean-room checker derived rather
than hard-coded the six genuinely free anchor/path adjacencies and checked
all

\[
64\cdot3\cdot3=576
\]

graph/list subpatterns.  The greatest restoration-compatible local
overapproximation retains \(S\) and all requested direct swaps in only four
completions, and all four have both internal lists full.  This agrees with
the analytic proof; the theorem does not depend on this census.

## 3. Static-defect ridges

C-070 validly supplies

\[
cx_0,cx_3\in E(G).
\]

Since \(c\) is absent from each endpoint static list, the states
\(\{a,b,x_0\}\) and \(\{a,b,x_3\}\) fail domination.  Their missed-vertex
sets are exactly

\[
D_0=N_H(a)\cap N_H(b)\cap N_H(x_0),\qquad
D_3=N_H(a)\cap N_H(b)\cap N_H(x_3),
\]

so both are nonempty.

The common set \(U=N_H(a)\cap N_H(b)\) is a \(G\)-clique: two distinct
nonadjacent vertices of \(U\), together with \(a,b\), would form an
independent four-set.  For every \(d\in U\), the independent triple
\(\{a,b,d\}\) is maximum and therefore lies in every optimal eternal
triple-family.  It is the retained \(c\)-swap at \(S\).  The two graph
nonedges \(da,db\) exclude the other response colors, proving

\[
L^{\mathcal F}(d)=\{c\}.
\]

The retained states \(\{a,b,x_1\}\) and \(\{a,b,x_2\}\) show directly,
or equivalently by the accepted ridge-response covariance between
\(\{a,b,c\}\) and \(\{a,b,d\}\), that

\[
dx_1,dx_2\in E(G).
\]

This use of maximum-independent-state forcing is legitimate because the
hypothesis \(\alpha=\gamma^\infty=3\) makes every eternal family of
triples optimal.

## 4. Complete audit of the double-defect kernel

If \(d\in D_0\cap D_3\), all adjacencies on

\[
\{a,b,c,x_0,x_1,x_2,x_3,d\}
\]

are fixed except

\[
bx_0,\quad bx_1,\quad ax_2,\quad ax_3.
\]

The coverage count is exact:

- three anchor pairs are fixed nonedges;
- the six path pairs are fixed by inducedness of the complement \(P_4\);
- eight of the twelve anchor/path pairs are fixed graph edges by positive
  static incidences and C-070 endpoint saturation;
- the remaining four anchor/path pairs are the four listed above; and
- all seven pairs incident with \(d\) are fixed by
  \(d\in D_0\cap D_3\) and the singleton-\(c\) ridge conclusion.

These categories cover all \(\binom82=28\) pairs, giving exactly
\(2^4=16\) completions.

For each completion the independent checker initialized every displayed
triple that

1. dominates the displayed induced graph, and
2. satisfies the necessary restoration inclusion using the five exact
   displayed family lists.

This is an overapproximation of the intersection of any real family with
the displayed core.  Synchronous greatest-fixed-point deletion removed
the reference state in every completion.  The initial sets had sizes
28--32; \(S\) was deleted in rounds 2--4.  The independently generated
table has SHA-256

`1d693d737414264059c7fba0790ead35be6e2ef686195532ae7c98f7b65c7bc3`.

External vertices cannot repair this contradiction:

- if a real family state is wholly in the core and dominates the whole
  graph, it necessarily dominates every core vertex;
- the global restoration theorem uses the same exact response lists for
  the occupied core vertices, so the state passes the local restoration
  filter;
- an attack at an unoccupied core vertex from a core triple replaces one
  core guard by that core vertex, hence every possible one-guard successor
  is still wholly in the core; and
- adding external family states therefore creates no additional successor
  for any local attack used by the deletion ranks.

By monotonicity, the actual core intersection is contained at every round
in the local active set.  Since the overapproximation deletes \(S\), no
actual family containing \(S\) realizes a double defect.  This proves

\[
D_0\cap D_3=\varnothing.
\]

The further separation from
\(Z=N_H(x_0)\cap N_H(x_3)\) is immediate: a vertex in
\(D_0\cap Z\) also belongs to \(D_3\), and the reflected statement is the
same.

## 5. Collision audit and the order count

The two defect witnesses are genuinely new.

First, every member of \(D_0\) is outside the original seven vertices:
\(a,b,x_0\) are excluded by open-neighborhood membership; \(c\) sees
\(x_0\); \(x_1\) sees \(a\); \(x_2\) sees \(b\); and \(x_3\) sees
\(x_0\).  The reflected ledger proves the same for \(D_3\).

Choose \(d_0\in D_0,d_3\in D_3\).  The local kernel gives
\(d_0\ne d_3\).  Corollary 4.2 separates both from every \(z\in Z\).
Both defects miss \(a,b\), so:

- neither can be \(w\in W\), because C-070 gives both positive response
  colors \(a,b\) at \(w\);
- neither can be \(p\in P_L\), because C-072 gives
  \(b\in L^{\mathcal F}(p)\);
- neither can be \(q\in P_R\), because C-072 gives
  \(a\in L^{\mathcal F}(q)\); and
- neither can be \(y\in Y_w\), because C-070 gives
  \(ya,yb\in E(G)\).

Positive family-response colors imply the corresponding graph edges by
the independent-reference-state argument in Section 1, so these are real
collision exclusions, not list-label assertions.

I rechecked accepted C-072 at source SHA-256
`0c6a3de00f8e4daa53f4602c437ed51a22da911cfdff3f42445550b07e3430bb`.
It proves that one may choose

\[
w\in W,\quad z\in Z,\quad p\in P_L,\quad q\in P_R,\quad y\in Y_w
\]

as five mutually distinct vertices external to the original seven.
The two defect vertices are distinct from those five and from the original
seven.  Therefore the candidate's count is exactly

\[
7+5+2=14.
\]

No stronger global order bound follows: a counterexample need not realize
this particular static \(Y_3\).

## 6. Independent controls and graph6 audit

The clean-room checker validated the ordinary graph6 convention against
the known labeled path `Ch`, decoded each control, and re-encoded it
byte-for-byte.

For `FDzro` it independently:

- reconstructed a seven-vertex, thirteen-edge graph;
- removed exactly the forbidden direct swaps and computed the greatest
  allowed one-guard kernel, obtaining a 21-state family containing \(S\);
- checked all \(21(7-3)=84\) unoccupied attacks;
- required every response to replace exactly one occupied guard, traverse
  a graph edge, and remain in the same family;
- recovered family lists
  \[
  \{0\},\{0,2\},\{1,2\},\{1\};
  \]
- recovered the strictly larger static lists
  \[
  \{0,2\},\{0,1,2\},\{0,1,2\},\{1,2\};
  \]
- and obtained
  \[
  (\gamma,\alpha,\gamma^\infty,\theta)=(2,3,3,3)
  \]
  using exhaustive subsets, a separate unrestricted eternal kernel, and
  direct complement coloring.

The full response-obligation ledger has SHA-256
`b2bd047ea9391b839932908354d4b03a193a31346fa5fa165e34cd102c81faaa`.
This confirms the candidate's sharp gamma-two boundary and also confirms
that a family-list \(Y_3\) need not be a static-list \(Y_3\).

For the ten-vertex control, the checker round-tripped

```text
G = IzM]XTR`W
H = ICp`eik]_
```

and verified that the two decoded graphs are exact complements, with
25 and 20 edges respectively.  Independent exhaustive evaluation gave

\[
(\gamma,\alpha,\gamma^\infty,\theta)=(3,3,4,4).
\]

It also found no \(K_4\) in \(H\), verified every induced vertex link in
\(H\) bipartite, and found a common \(H\)-neighbor for every vertex pair.
All 77 dominating triples were deleted by the ordinary one-guard kernel in
synchronous round sizes

\[
10,\ 20,\ 40,\ 7.
\]

The seven independent triples had deletion-rank multiset

\[
3,3,4,4,4,4,4.
\]

An unrestricted eternal four-family of 197 states supplies the positive
\(\gamma^\infty=4\) witness.

## 7. Exact nonclaims

This review does not accept any of the following:

1. an arbitrary-order exclusion of the static \(Y_3\);
2. a proof of \(\mathsf{GL}(3)\) or of the complete \(k=3\) conjecture;
3. a universal counterexample-order floor of fourteen;
4. an exclusion of longer unit chains, lollipops, bicycles, full lists, or
   higher-parameter \(Y_k\) obstructions;
5. a claim that family and static response lists coincide in general; or
6. a resolution of the gamma--theta conjecture.

Within the stated conditional scope, the analytic proof, finite local
kernel, C-072 combination, two controls, graph/complement convention, and
order count all pass adversarial review.
