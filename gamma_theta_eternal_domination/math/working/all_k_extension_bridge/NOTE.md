# The all-\(k\) inactive-link extension bridge

## Status and exact boundary

Date: 2026-07-28 (PDT)

This note uses the standard one-guard-moves eternal-domination model.
Attacks occur only at unoccupied vertices, exactly one adjacent guard
moves, and every retained successor dominates.

The outcome is a new all-parameter local consequence of the accepted
frozen-color projection and target-response propagation theorems:

1. **PROVED:** in a minimum counterexample, every target-inactive vertex
   \(r\) forces not only its complement link, but its link together with
   the target \(x\), to be exactly \((k-1)\)-colorable;
2. **PROVED:** when \(rx\in E(G)\), this is a genuine strengthening of the
   ordinary face-link theorem, because \(x\notin N_{\overline G}(r)\);
3. **AUDITED:** these local \((k-1)\)-colorings do not presently glue into
   the single deletion coloring required by C-108;
4. **EXACT POSITIVE CONTROL:** even in an equality graph, for the greatest
   eternal family and a genuine full target, one cannot fix an arbitrary
   deletion coloring: half of the deletion colorings of the accepted
   order-12 control use all three colors on the inactive set.

This does not prove the gamma--theta conjecture, the complete \(k=3\)
case, or the critical full-target branch.  No literature-priority claim is
made.

The accepted inputs read in full were:

- `math/lemmas/general_target_response_propagation.md` (C-108);
- `math/working/k3_cross_state_attack.md` (the all-\(k\) frozen-color
  projection);
- `math/lemmas/independent_antineighborhood_projection.md` (C-051);
- `math/working/full_target_facet_propagation/NOTE.md`; and
- `math/working/inactive_set_coloring_bridge/NOTE.md` (C-109).

## 1. Setup

Let \(G\) be a minimum-order counterexample with

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=k<\theta(G),
 \qquad H=\overline G,
\tag{1.1}
\]

and let \(\mathcal F\) be an eternal family of \(k\)-sets.
Fix a target \(x\).

Let \(T\) be an independent \(k\)-set avoiding \(x\), and let \(r\in T\).
For \(y\notin T\), write

\[
 L_T^{\mathcal F}(y)
 =
 \{u\in T:uy\in E(G),\ T-u+y\in\mathcal F\}.
\tag{1.2}
\]

Define the \(r\)-omission set and its frozen projection by

\[
 W_{T,r}
 =
 \{y\notin T:r\notin L_T^{\mathcal F}(y)\},
\tag{1.3}
\]

\[
 Q_{T,r}
 =
 G[(T-\{r\})\cup W_{T,r}].
\tag{1.4}
\]

C-108 says that, for the fixed target \(x\), whether \(r\) belongs to
\(L_T^{\mathcal F}(x)\) is independent of the maximum independent
\(k\)-state \(T\) containing \(r\).  Call \(r\) **inactive at \(x\)** when

\[
 r\notin L_T^{\mathcal F}(x).
\tag{1.5}
\]

In the equality-critical deletion branch, \(G-x\) is well-covered with
independence number \(k\), so every deletion vertex occurs in such a
state \(T\).

## 2. Inactive-link suspension theorem

### Theorem 2.1 — PROVED

Under (1.1), let \(r\) be inactive at \(x\) and let \(T\) be any maximum
independent \(k\)-set avoiding \(x\) and containing \(r\).  Then

\[
 \boxed{
 \chi\!\left(
   H[\{x\}\cup N_H(r)]
 \right)
 =
 \omega\!\left(
   H[\{x\}\cup N_H(r)]
 \right)
 =
 k-1.
 }
\tag{2.1}
\]

Moreover, the larger frozen projection itself satisfies

\[
 \gamma(Q_{T,r})
 =
 \alpha(Q_{T,r})
 =
 \gamma^\infty(Q_{T,r})
 =
 \theta(Q_{T,r})
 =
 k-1.
\tag{2.2}
\]

#### Proof

Inactivity (1.5) says exactly that

\[
 x\in W_{T,r}.
\tag{2.3}
\]

Now take any \(z\in N_H(r)\).  If \(z\in T-\{r\}\), then \(z\) belongs to
the first set in (1.4).  Otherwise \(z\notin T\), and

\[
 rz\in E(H)
 \quad\Longleftrightarrow\quad
 rz\notin E(G).
\]

The guard at \(r\) therefore cannot answer an attack at \(z\), so
\(r\notin L_T^{\mathcal F}(z)\) and \(z\in W_{T,r}\).  Together with
(2.3), this proves

\[
 \{x\}\cup N_H(r)\subseteq V(Q_{T,r}).
\tag{2.4}
\]

The accepted frozen-color projection theorem, applied with reference
state \(T\) and frozen guard \(r\), gives

\[
 \gamma(Q_{T,r})
 =
 \alpha(Q_{T,r})
 =
 \gamma^\infty(Q_{T,r})
 =
 k-1.
\tag{2.5}
\]

The graph \(Q_{T,r}\) is a proper induced subgraph of \(G\), because it
does not contain \(r\).  If its clique-cover number exceeded \(k-1\),
then (2.5) would make it a smaller counterexample, contrary to the
minimum-order choice of \(G\).  Hence

\[
 \theta(Q_{T,r})=k-1,
\]

which proves (2.2).

Taking complements inside the common induced vertex set, a
\((k-1)\)-clique partition of \(Q_{T,r}\) is a proper
\((k-1)\)-coloring of

\[
 H[V(Q_{T,r})].
\]

Equation (2.4) restricts that coloring to
\(H[\{x\}\cup N_H(r)]\), proving the upper bound in (2.1).
Finally, \(T-\{r\}\subseteq N_H(r)\) is a \((k-1)\)-clique of \(H\).
Thus the chromatic and clique numbers in (2.1) are both exactly
\(k-1\). \(\square\)

### What is genuinely added

If \(rx\in E(H)\), then \(x\in N_H(r)\), and (2.1) reduces to the
accepted minimum-counterexample face-link equality C-051.

The new case is dynamic inactivity:

\[
 rx\in E(G)
 \quad\text{but}\quad
 T-r+x\notin\mathcal F.
\tag{2.6}
\]

Then \(x\notin N_H(r)\), yet adjoining \(x\) to the entire complement
link still does not raise its chromatic number.  This conclusion uses the
multi-step eternal family through the frozen projection; it is not a
static consequence of the graph edge \(rx\).

For \(k=3\), (2.1) says

\[
 H[\{x\}\cup N_H(r)]\text{ is bipartite}.
\tag{2.7}
\]

Consequently, in every connected component of \(H[N_H(r)]\), all
neighbors of \(x\) lie on one bipartition side.  If \(x\) met both sides,
an odd path between the two sides together with its two incident
\(x\)-edges would form an odd cycle, contradicting (2.7).  This recovers
the relevant side-purity phenomenon directly from the all-\(k\)
projection.

## 3. Why this does not complete the induction

In the equality-critical deletion branch, put

\[
 R_x=V(G-x)\setminus A_x,
\]

where \(A_x\) is the C-108 active set.  C-108 proves that a common
responder color exists exactly when one can choose a proper \(k\)-coloring
\(\kappa\) of \(H-x\) with

\[
 |\kappa(R_x)|\le k-1.
\tag{3.1}
\]

Theorem 2.1 supplies a \((k-1)\)-coloring around **each individual**
\(r\in R_x\), namely on

\[
 H[\{x\}\cup N_H(r)].
\]

It does not supply one coloring on the union of those vertex sets, and
the accepted theorems do not synchronize the independent color
permutations on their overlaps.  In particular:

1. the frozen projected family need not be the greatest eternal family of
   the projected graph;
2. an arbitrary clique partition of the projection gives only static
   response compatibility, not membership in the original family; and
3. local \((k-1)\)-colorability of all these suspensions does not imply
   that \(H[R_x]\) is \((k-1)\)-colorable, much less that its coloring
   extends through all of \(H-x\).

Thus combining C-108, C-051, and the frozen-color projection exhausts the
local induction hypothesis but leaves a genuine global precoloring/gluing
problem.  Declaring the local colorings compatible would assume the
missing bridge.

## 4. Exact equality control: the deletion coloring cannot be arbitrary

The accepted labeled graph

```text
Ksv`f\knJVis
```

has

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3).
\]

For

\[
 S=\{1,2,3\},\qquad x=0,
\]

the greatest eternal triple-family has 127 states and

\[
 L_S(x)=S.
\]

The C-108 active and inactive sets are

\[
 A_x=\{1,2,3,4,5,7,9\},
\qquad
 R_x=\{6,8,10,11\}.
\tag{4.1}
\]

The standalone checker exhausts all 12 proper three-colorings of
\(\overline{G-x}\):

- six use exactly two colors on \(R_x\);
- six use all three colors on \(R_x\);
- each of the three colors is the omitted color in exactly two of the
  successful colorings.

Therefore even exact equality, the greatest eternal family, and a genuine
full target do **not** permit the proof to begin with an arbitrary deletion
coloring.  A real coloring-selection mechanism is required.

This control lies in the sharp domination-drop branch

\[
 \gamma(G-x)=2,\qquad
 \alpha(G-x)=\gamma^\infty(G-x)=\theta(G-x)=3.
\]

It therefore does not refute the desired existence statement in the
equality-critical deletion branch.  It only refutes the stronger
“every deletion coloring works” shortcut.

Reproduction:

```text
python3 -I -B -W error \
  math/working/all_k_extension_bridge/verify_positive_control.py
```

## 5. Bounded normalized control search

`search_k3_control.py` asks for a stronger control in the
equality-critical deletion branch.  It encodes:

- exact \(\gamma=\alpha=\gamma^\infty=\theta=3\) for \(G\);
- exact \(\gamma=\alpha=\gamma^\infty=\theta=3\) for \(G-x\);
- a specified eternal family with a full root response at \(x\);
- one proper three-coloring of \(\overline G\); and
- a second proper coloring of \(\overline{G-x}\) using all three colors on
  three physical complement neighbors of \(x\).

CaDiCaL 3.0.1 returned UNSAT for the normalized formulas at every order
from 9 through 14.  The order-14 formula has 14,498 variables and 37,104
clauses.  These are **OBSERVED discovery runs only**: no proof logs,
independent reconstruction, or coverage audit were produced, so no finite
theorem is claimed.

The ablation that removes the second coloring and its three blockers also
returned UNSAT through order 12.  This merely says that the fixed positive
critical-full control was not found in that bounded search; it is not a
universal structural theorem.

## 6. Conclusion

The accepted all-\(k\) machinery does advance one layer further:

\[
 \boxed{
 r\in R_x
 \quad\Longrightarrow\quad
 \chi\bigl(H[\{x\}\cup N_H(r)]\bigr)=k-1
 }
\]

inside a minimum counterexample.

It does not force a common responder color.  The remaining bridge is now
precisely a compatibility theorem for these locally balanced suspensions,
or an attack argument showing that a minimal obstruction to their global
gluing cannot survive.  Without such a new compatibility mechanism, the
attempted universal induction stops here rather than resolving the
conjecture.
