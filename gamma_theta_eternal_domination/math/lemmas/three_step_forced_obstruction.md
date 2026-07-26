# Recursive online failure certificates and the third-ply forced-state obstruction

## Status and scope

This note continues the online transition-kernel notation proved in
`math/lemmas/two_step_transition_kernel.md`.  The recursive certificates below
are elementary dual witnesses for finite kernel membership and nonmembership.
No claim is made that the general finite-horizon formulation is new.

The contribution delimited here is:

1. a direct recursive certificate for failure at any online horizon, checkable
   without computing the greatest fixed point;
2. its specialization to a third-ply obstruction at a forced maximum
   independent state; and
3. a certificate-backed measurement on the 526 recorded edge-toggle
   near-misses that survived the earlier two-ply obstruction.

All attacks are at unoccupied vertices.  Every response moves exactly one
guard along exactly one edge to the attacked vertex.

## 1. Kernel notation

Fix a finite simple graph \(G\) and a guard count \(k\).  Let
\(\mathcal C_k\) be the family of dominating \(k\)-subsets of \(V(G)\).  For
\(\mathcal X\subseteq\mathcal C_k\), set

\[
 \Phi(\mathcal X)=
 \left\{D\in\mathcal C_k:
 \begin{array}{l}
 \text{for every }r\in V(G)-D\text{ there is }u\in D\cap N(r)\\
 \text{such that }D-u+r\in\mathcal X
 \end{array}
 \right\},
\]

where \(D-u+r=(D-\{u\})\cup\{r\}\).  Put

\[
 \mathcal K_0=\mathcal C_k,\qquad
 \mathcal K_{h+1}=\Phi(\mathcal K_h).
\]

Thus \(D\in\mathcal K_h\) means that the defender has an online strategy
which keeps every configuration dominating for the next \(h\) attacks.  The
stable value of the descending chain \((\mathcal K_h)\) is the greatest
eternal \(k\)-family.

## 2. Recursive failure and survival certificates

An **\(h\)-failure certificate rooted at \(D\)** is defined recursively.

- A terminal certificate names a vertex \(x\) with
  \(N[x]\cap D=\varnothing\).  It is valid at every horizon \(h\geq0\).
- A nonterminal certificate, allowed when \(h\geq1\), names an unoccupied
  attack \(r\notin D\) and, for every \(u\in D\cap N(r)\), contains an
  \((h-1)\)-failure certificate rooted at \(D-u+r\).

The universal branching over all adjacent occupied guards is essential.  In
particular, a missing response branch is not a certificate.

Dually, an **\(h\)-survival certificate rooted at \(D\)** requires \(D\) to
dominate and is defined as follows.

- At horizon zero there are no branches.
- At horizon \(h\geq1\), for every unoccupied attack \(r\notin D\), it names
  one guard \(u\in D\cap N(r)\) and contains an \((h-1)\)-survival
  certificate rooted at \(D-u+r\).

The attack choices in a failure tree and the guard choices in a survival tree
may depend on the entire preceding path.  These are therefore online,
alternating-quantifier certificates.

**Lemma 1 (soundness and completeness).**  For every \(k\)-set \(D\) and
every \(h\geq0\):

1. an \(h\)-failure certificate rooted at \(D\) exists if and only if
   \(D\notin\mathcal K_h\); and
2. an \(h\)-survival certificate rooted at \(D\) exists if and only if
   \(D\in\mathcal K_h\).

**Proof.**  Induct on \(h\).  At \(h=0\), membership in
\(\mathcal K_0\) is exactly domination, so the two terminal definitions give
both assertions.

Suppose \(h\geq1\).  A non-dominating \(D\) is outside
\(\mathcal K_h\subseteq\mathcal K_0\), and a named undominated vertex
certifies this directly.  If \(D\) dominates, then

\[
 D\notin\mathcal K_h
 \quad\Longleftrightarrow\quad
 \text{there is }r\notin D\text{ such that }
 D-u+r\notin\mathcal K_{h-1}
 \text{ for every }u\in D\cap N(r).
\]

By induction, the right side is equivalent to the recursive failure
certificate definition.

Likewise,

\[
 D\in\mathcal K_h
 \quad\Longleftrightarrow\quad
 D\text{ dominates and, for every }r\notin D,\text{ some }
 u\in D\cap N(r)
 \text{ has }D-u+r\in\mathcal K_{h-1}.
\]

Applying the induction hypothesis to each chosen successor gives exactly a
survival certificate. \(\square\)

This lemma makes both certificate types independently checkable by elementary
adjacency, occupancy, cardinality, and domination tests.  No fixed-point
iteration is required by the checker.

## 3. The forced-state obstruction

Every maximum independent set of size \(k\) belongs to every eternal
dominating family of size \(k\): starting from any family state, repeatedly
attack unoccupied vertices of the independent set.  Independence prevents a
guard already on that set from responding, so every attack increases its
occupancy by one.

**Theorem 2 (finite-horizon forced-state obstruction).**  Suppose
\(\alpha(G)=k\).  If some maximum independent \(k\)-set \(S\) has an
\(h\)-failure certificate for some finite \(h\), then

\[
 \gamma^\infty(G)\geq k+1.
\]

**Proof.**  If an eternal \(k\)-family existed, it would contain \(S\).
Every eternal family is contained in every finite kernel
\(\mathcal K_h\), whereas Lemma 1 gives \(S\notin\mathcal K_h\), a
contradiction.  The general lower bound
\(\alpha(G)\leq\gamma^\infty(G)\) and integrality finish the proof.
\(\square\)

At horizon three, the theorem has the explicit adversarial form

\[
 \exists r_1\ \forall u_1\ \exists r_2(u_1)\ \forall u_2\
 \exists r_3(u_1,u_2)\ \forall u_3,
\]

where every \(r_j\) is an unoccupied attack, every quantified \(u_j\) ranges
over all guards adjacent to that attack, and every surviving depth-three
branch ends in a named non-dominating configuration.  A branch may terminate
earlier if a response is already non-dominating.  This is the
**third-ply forced-state obstruction**.  It strictly contains the two-ply
condition: failure at horizon three can occur even when the same forced state
survives horizon two.

## 4. Certificate-backed strictness on \(C_{15}\)

Label \(C_{15}\) cyclically by \(0,1,\ldots,14\), put \(k=7\), and let

\[
 S=\{0,2,4,6,8,10,12\}.
\]

The usual cycle bound gives \(\alpha(C_{15})=7\).  Direct kernel sizes are

\[
 |\mathcal K_0|=765,\qquad
 |\mathcal K_1|=120,\qquad
 |\mathcal K_2|=15,\qquad
 |\mathcal K_3|=0.
\]

The 15 maximum independent sets are the rotations of \(S\); all survive
through \(\mathcal K_2\) and none survives \(\mathcal K_3\).  The artifact
`certificates/c15_k2_not_k3.json` contains:

- a 73-node, 64-leaf survival tree proving \(S\in\mathcal K_2\); and
- an 8-node, 4-leaf failure tree proving \(S\notin\mathcal K_3\).

The small failure tree is readable directly.  Attack \(1\) from \(S\).

- If \(0\to1\), vertex \(14\) is undominated.
- If \(2\to1\), attack \(7\).
  - If \(6\to7\), attack \(3\).  The only response is \(4\to3\), after
    which vertex \(5\) is undominated.
  - If \(8\to7\), attack \(11\).
    - After \(10\to11\), vertex \(9\) is undominated.
    - After \(12\to11\), vertex \(13\) is undominated.

Every listed move is along a cycle edge, the attacks are unoccupied, and the
branches exhaust the guards adjacent to the attack.  The larger positive
tree records one legal response to every first and second attack and is
replayed by the direct checker.  Consequently the horizon-three obstruction
is genuinely stronger than the horizon-two obstruction.

## 5. Measurement on the 526 two-ply survivors

The deterministic standard-library program
`src/search/three_step_kernel.py` independently parsed the graph6 records,
recomputed \(\alpha=3\), enumerated every dominating triple, and computed the
online kernels.  For all 526 selected graphs it also compared the exact
deletion rank of every dominating triple with the previously recorded
third-audit trace.  All 64,893 configuration ranks agreed.

The source population is deliberately narrow: these are the 526 canonical
records among the 8,587 stored edge-toggle near-misses with
\(\gamma=\alpha=3\) and \(\gamma^\infty=\theta=4\) that survived
\(\mathcal K_2\).  It is not the set of all graphs of orders 11 or 12.

For a forced triple, its deletion rank is the least \(h\) for which it is
absent from \(\mathcal K_h\).  The measured distributions were:

| statistic | distribution |
|---|---|
| earliest forced-triple rank per graph | \(3:518,\ 5:7,\ 6:1\) |
| latest forced-triple rank per graph | \(3:225,\ 4:291,\ 5:2,\ 6:7,\ 7:1\) |
| all 6,375 forced triples | \(3:5283,\ 4:1012,\ 5:19,\ 6:55,\ 7:6\) |
| first empty full-kernel level | \(3:185,\ 4:331,\ 5:2,\ 6:7,\ 7:1\) |

Thus a third-ply certificate at one forced triple eliminates 518 of the 526
two-ply survivors, about \(98.5\%\).  The generator wrote and then reparsed
518 recursive certificates.  Their aggregate size is 5,540 nodes and 3,174
terminal leaves; the largest individual certificate has 17 nodes.

Eight graphs survive both \(\mathcal K_3\) and \(\mathcal K_4\).  Seven
first lose a forced triple at \(\mathcal K_5\), and the last first loses one
at \(\mathcal K_6\):

```text
graph6          n   m   earliest forced rank   full empty depth
J@l|bfNuVK_    11  32             5                    6
K]?H[|]nj}\k   12  39             5                    6
KoDbMyz}@}ju   12  38             5                    6
KoYu~_VMyzLf   12  39             5                    6
Kp]e~_VDyZlf   12  39             5                    6
Krqb}iw[W^`~   12  39             5                    6
KrrDthx\_^`~   12  39             5                    6
Kun_w{vRrblV   12  40             6                    7
```

The deepest graph, `Kun_w{vRrblV`, has kernel sizes

\[
147,\ 143,\ 136,\ 128,\ 119,\ 93,\ 28,\ 0
\]

from \(\mathcal K_0\) through \(\mathcal K_7\).

The complete measurement is in
`results/three_step_kernel_measurement.json`; the 518 certificate rows are
in `certificates/k3_three_step_edge_toggle.ndjson`.  The certificate stream
is bound to the source and input ledger by SHA-256 hashes, has a
row-stream digest in its trailer, and is reparsed and checked after atomic
write.

## 6. What this does and does not prove

Theorem 2 is universal and exact.  Each accepted recursive certificate
rigorously proves that its named forced state cannot belong to an eternal
family of the stated size.

The population counts are certificate-backed finite measurements on a
derived search family.  They are useful evidence that one additional online
ply is a very high-yield filter, but they do not constitute exhaustive
verification at order 11 or 12, do not raise the known global order bound,
and do not resolve the \(\gamma\)--\(\theta\) conjecture.  The eight deeper
graphs are retained as the next structural targets rather than reported as
counterexamples.
