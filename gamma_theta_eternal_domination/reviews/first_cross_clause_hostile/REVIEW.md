# Hostile review: the first positive-length cross clause

## Verdict

**PASS, with strict scope.**

The frozen candidate proves the four parity types of a selected
unit--clause--unit core and proves that its odd--odd type creates two
nonempty, disjoint retained defect ridges.  The argument is valid for an
arbitrary specified one-guard eternal family under the displayed equality
hypotheses.  It does not confuse absence from that family with
nonadjacency in the graph.

This review accepts exactly:

1. the parity classification of the two singleton terminals;
2. the singleton-shared-color description of any intersection of the two
   supporting free components;
3. completeness in \(G\) of the shared anchor to both supporting
   components;
4. the retained common-nonneighbor ridge forced by an odd singleton;
5. disjointness of the two ridges in the odd--odd type; and
6. the stated boundary between a one-edge/one-edge family pattern and the
   exact static induced-\(P_4\) hypothesis required by C-121.

It does **not** accept an exclusion of even arms, anchor-only ridges under
equality, longer or intersecting arms, any arbitrary positive-length
two-unit chain, the complete singleton branch, complete \(k=3\), or the
universal gamma--theta conjecture.

No change to the candidate proof is required.  The phrase “anchor-only
defect ridges are allowed” is accepted only in the candidate's explicit
sense of “not ruled out by this lemma.”  The supplied realization `FDzro`
has \(\gamma=2\), so it does not prove that this escape occurs under
equality.

## Frozen candidate and dependencies

The audited candidate manifest is

```text
math/working/first_cross_clause_attack/MANIFEST.json
SHA-256 2e157de3ce02eda7eee2cff65d2af064eb7b9103a6f2b3d16772ede44d4e86b0
```

All five files listed in it match:

```text
NOTE.md                 d845635c3df454f7809dde5b6dc089e4c9a7076b106cf19c264d62998e311413
RESEARCH_LOG.md         5b1ecb704a6477a5778991bccead97ea70439710e8b27bcefb9c13d202a1d8a2
result.json             35f9745f7b4eacdf3c9b194507fb63ae4be3a60b960183be1e28683ce916738c
search_subfamilies.py   40adb74c37161e7182f44ec34b8fd50f37a24d712b7674934f2da33db77ccb5c
verify.py               183ff12c1c4bc70b2603547ed5f6602d07188424a1a854bdc18345a309d59db8
```

The candidate verifier was replayed and reproduced `result.json` byte for
byte.  That is corroborative only.  The independent checker described
below does not import or execute it.

The exact accepted dependency notes used by the proof were also pinned:

```text
C-120 singleton_fixed_certificates/NOTE.md
25e775574caa48c719e3cf2949fe0ae29c23082b308f2f2002cb1ac2287fa95b

C-124 free_unit_chain_attack/NOTE.md
3dbccd2aa69cfc45b1c5e518e05165594e27f06b1741fcd1ec7a2b8b0d02fb39

C-121 dynamic_gluing_y3/NOTE.md
ff559cb949c5427bc33e75a43deba38a8284e78c380a01bb97488a82a59798f9
```

## Independent mathematical audit

Throughout, \(H=\overline G\),
\(S=\{u,v,w\}\in\mathcal F\) is independent, and

\[
L(q)=\{a\in S:S-a+q\in\mathcal F\}.
\]

The family is not assumed greatest.  The proof uses family-response lists,
except where it explicitly invokes the separate static-list hypothesis of
C-121.

### 1. The four parity types

The port \(x\), with list \(\{v,w\}\), lies in a free component \(K\) of
the frozen-\(u\) bipartite projection.  A singleton marker \(s\in K\)
fixes the component orientation so that \(x\) is assigned \(w\).
C-124 says all singleton markers on the same side demand the same
available anchor and those on the opposite side demand the other anchor.
Therefore

\[
L(s)=\{w\}
\quad\text{at even distance from }x,
\qquad
L(s)=\{v\}
\quad\text{at odd distance.}
\]

The same argument in the frozen-\(v\) projection, whose available colors
are \(u,w\), gives \(\{w\}\) and \(\{u\}\) for the second arm.

The parity is well defined: both endpoints lie in one connected component
of a bipartite graph, so all connecting paths have the same parity.  The
candidate therefore obtains four and only four parity combinations.

### 2. Intersection of the supporting components

If \(r\in K\cap M\), then membership in the frozen-\(u\) vertex set gives
\(u\notin L(r)\), and membership in the frozen-\(v\) vertex set gives
\(v\notin L(r)\).  The list is nonempty, so

\[
L(r)=\{w\}.
\]

Here \(r\) is an outside vertex: a free component cannot contain either
unfrozen anchor of its projection.  Applying C-124 with \(r\) as a
singleton marker puts \(r\) on the \(w\)-side of each selected port.
Thus its parity from both ports is even.  In particular, one physical
vertex cannot serve as both odd terminals.  No assumption about graph
adjacency was inferred from a missing family response.

### 3. The shared anchor is complete to both arms

In the frozen-\(u\) complement projection, \(v\) and \(w\) form the
anchor edge and hence lie in the anchor component.  The component \(K\)
is free, so there is no \(H\)-edge between \(w\) and a vertex of \(K\).
Every such pair is consequently an edge of \(G\).  The frozen-\(v\)
argument gives the same conclusion for \(M\).

This proves

\[
wz\in E(G)\qquad(z\in K\cup M).
\]

The direction of complementation is correct: separation of complement
components produces graph edges, which are the edges legal guard moves
use.

### 4. A singleton's defect ridge

Assume \(L(s)=\{v\}\).  The pair \(\{w,s\}\) cannot dominate because
\(\gamma(G)=3\).  Its missed set is exactly

\[
Z_s=N_H(w)\cap N_H(s),
\]

so \(Z_s\) is nonempty.

The singleton response retains

\[
D_s=S-v+s=\{u,w,s\}.
\]

For \(z=u\), the required state \(\{w,s,z\}\) is already \(D_s\).  For
any other \(z\in Z_s\), the attack at \(z\) from \(D_s\) is unoccupied.
The guards at \(w\) and \(s\) cannot move because both corresponding
pairs are edges of \(H\).  Eternity therefore forces the sole remaining
guard \(u\) to be adjacent to \(z\) and to move:

\[
u\longrightarrow z,
\qquad
\{w,s,z\}\in\mathcal F.
\]

This is a literal one-guard move, not an inference from domination alone.

For distinct \(z,z'\in Z_s\), the retained state
\(\{w,s,z\}\) must dominate \(z'\).  Since \(w\) and \(s\) both miss
\(z'\), it follows that \(zz'\in E(G)\).  Attacking the unoccupied
\(z'\) then uniquely moves \(z\) to \(z'\).  Hence \(G[Z_s]\) is a
clique and all its ridge exchanges are retained.

Finally, for outside \(z\), restoration of the retained state
\(\{w,s,z\}\) must restore the two missing reference positions \(u,v\).
The singleton \(s\) supplies only \(v\), forcing \(u\in L(z)\).
The literal edge \(wz\in E(H)\) independently gives \(w\notin L(z)\).
This last negative assertion is graphical; it does not turn dynamic
family absence into a graph nonedge.

The only possible reference anchor in \(Z_s\) is \(u\): \(w\) is excluded
by the open neighborhood and \(v\) is adjacent in \(G\) to \(s\) because
\(v\in L(s)\).  The reflected assertions for \(Z_t\) are identical.

### 5. Disjointness in the odd--odd type

Odd parity gives

\[
L(s)=\{v\},
\qquad
L(t)=\{u\}.
\]

Suppose \(z\in Z_s\cap Z_t\).  It cannot be an anchor.  The anchor \(u\)
is adjacent in \(G\) to \(t\), the anchor \(v\) is adjacent in \(G\) to
\(s\), and \(w\) lies in neither of its own open neighborhoods.  Thus
\(z\notin S\).

The two applications of the defect-ridge lemma give

\[
u,v\in L(z),
\qquad
w\notin L(z),
\]

so \(L(z)=\{u,v\}\).  Consequently \(s,t,z\) all occur in the
frozen-\(w\) bipartite projection.  The two complement edges

\[
sz,\ tz\in E(H)
\]

form a length-two path, placing \(s\) and \(t\) in one component and on
the same bipartition side.

There are only two component cases:

- In the anchor component, C-120 aligns a singleton-\(v\) marker with the
  \(v\)-side and a singleton-\(u\) marker with the opposite \(u\)-side.
  They cannot be on the same side.
- In a free component, C-124 makes all singleton markers on one side
  demand the same anchor.  The distinct lists \(\{v\}\) and \(\{u\}\)
  again cannot occur on the same side.

This proves \(Z_s\cap Z_t=\varnothing\).

The additional location bound is also exact.  The shared-anchor
completeness proved in Section 3 excludes every vertex of \(K\cup M\)
from either common complement neighborhood.  The only possible anchor in
\(Z_s\) is \(u\), and the only possible anchor in \(Z_t\) is \(v\).

### 6. Exact limits of the result

The candidate correctly stops short of a contradiction.

- **Even arms.**  An even terminal has singleton list \(\{w\}\).  Its
  direct response occupies the other two anchors, and \(w\) is adjacent
  to the marker.  The pair and unique-third-anchor attack used in the odd
  ridge proof are therefore unavailable.  Nothing here eliminates an
  even arm or a coincident even--even pin.
- **Anchor-only ridges.**  The equality hypothesis makes each defect set
  nonempty, but it does not make it external.  The set \(Z_s=\{u\}\)
  already witnesses failure of the pair \(\{w,s\}\), and similarly
  \(Z_t=\{v\}\).  The proof supplies no further vertex in that case.
- **Long or intersecting arms.**  The parity and disjoint-ridge results
  survive, but they do not contract the physical paths or remove chords.
- **Family versus static lists.**  A missing family swap may remain a
  graph-adjacent dominating swap.  It cannot be used as a static
  nonincidence.

If both support paths have one edge, the four **family** lists are

\[
\{v\},\{v,w\},\{u,w\},\{u\},
\]

and the three displayed consecutive pairs are complement edges.  This is
the literal family-list shape of \(Y_3\).  C-121 applies only if:

1. the other three pairs among the four vertices are graph edges, so the
   displayed complement path is induced; and
2. the four **static** lists are exactly the displayed lists.

Neither condition follows from the present candidate.  The scope boundary
in its Section 4 is therefore necessary and correct.

## Independent reconstruction of the controls

`independent_checker.py` imports no candidate or campaign code.  It
decodes and re-encodes each graph6 string, uses frozenset graph data,
computes \(\gamma,i,\alpha\) by complete subset searches, computes
\(\theta\) by a direct clique-partition recursion, and computes
\(\gamma^\infty\) from an explicitly colored configuration digraph with
greatest-fixed-point deletion.

For `FDzro` it independently finds:

```text
(gamma, i, alpha, gamma-infinity, theta) = (2,2,3,3,3)
specified family states = 21
specified unoccupied-attack obligations = 84
greatest triple-family states = 33
```

Every specified state dominates and every unoccupied attack has a
one-edge, one-guard successor in the same family.  At
\(S=\{0,1,2\}\), the family lists are exactly

```text
L(3)={0}, L(4)={0,2}, L(5)={1,2}, L(6)={1}.
```

The complement induced by `3,4,5,6` is exactly the path
`3-4-5-6`; the two free components are `34` in the frozen-1
projection and `56` in the frozen-0 projection; and the defect sets are
exactly `{1}` and `{0}`.  The static lists are strictly larger:

```text
Ls(3)={0,2}, Ls(4)={0,1,2},
Ls(5)={0,1,2}, Ls(6)={1,2}.
```

This control therefore verifies three sharp boundaries at once: the
literal family pattern need not have exact static lists, both defect
ridges can be anchor-only in the local geometry, and the control is not
an equality graph because \(\gamma=2\).

For `FCZbg` the independent search finds:

```text
(gamma, i, alpha, gamma-infinity, theta) = (3,3,3,3,3)
greatest-family stages = 22, 19, 18
final states = 18
unoccupied-attack obligations = 72
```

At \(S=\{3,4,5\}\), it reconstructs

```text
L(0)={3}, L(1)={4,5}, L(2)={4,5}, L(6)={5}.
```

For shared anchor \(4\), the common-nonneighbor sets of pins \(0\) and
\(6\) are respectively `{6}` and `{0}`.  Both forced one-guard moves
lead to the retained exchange state `{0,4,6}`.  This verifies that the
ridge-exchange mechanism itself is compatible with equality.  As the
candidate states, this graph does not realize the complete first-clause
port geometry.

An exact clean-room replay is:

```text
cd gamma_theta_eternal_domination
python3 -I -B -W error \
  reviews/first_cross_clause_hostile/independent_checker.py
```

Its stdout is byte-identical to `independent_result.json`.

## Model and status ledger

Every attack in the universal proof is at an unoccupied vertex.  Every
forced successor replaces exactly one guard, and every move asserted to
exist follows an edge of \(G\).  Every retained configuration is required
to dominate.  Complement edges are used only for nonadjacency,
bipartition, and response-color collisions.  No all-guards-move rule,
occupied-vertex attack, or complement/graph reversal appears.

### PROVED

- Four terminal parity types for the selected first clause.
- Singleton-\(w\) intersection of the two support components.
- Shared-anchor completeness to both support components.
- Nonempty retained defect ridge for each odd singleton terminal.
- \(G\)-clique exchange structure within each ridge.
- Disjointness of the two odd--odd ridges.
- The exact extra hypotheses needed before invoking C-121.

### EXACT CONTROLS

- `FDzro`: literal one-edge/one-edge family obstruction with two
  anchor-only ridges and \(\gamma=2\).
- `FCZbg`: equality graph realizing the retained singleton-ridge exchange
  mechanism, but not the first-clause geometry.

### OBSERVED ONLY

- Any negative output of `search_subfamilies.py`.  It has no coverage
  proof and is not used here.

### OPEN

- Even arms and coincident pins.
- Whether anchor-only odd ridges occur or can be eliminated under the full
  equality first-clause hypotheses.
- Longer, intersecting, or chorded support paths.
- Family-list patterns with enlarged static lists.
- Arbitrary positive-length unit chains and lollipops.
- Residual bicycles and the full-list branch.
- Complete \(k=3\) and the universal gamma--theta conjecture.

The candidate is a valid structural advance, not a theorem resolution or
a finite counterexample-order exclusion.
