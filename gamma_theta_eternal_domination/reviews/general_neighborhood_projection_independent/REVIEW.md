# Independent hostile review: independent-antineighborhood projection

## Verdict

**ACCEPT — the theorem and both corollaries are proved in the standard
one-guard model.**

No mathematical defect was found.  In particular, the restricted-family
argument has the required quantifier order

\[
 \forall C\in\mathcal E\ \forall r\in V(Q)-C\
 \exists u\in C\cap N_Q(r)
\]

and the successor is obtained by moving exactly that one guard along one edge
to the unoccupied attacked vertex.

The publication/novelty verdict is narrower:

**ACCEPT ONLY AS AN EXPLICIT GENERALIZATION AND FAMILY-level strengthening of
accessible prior work, not as a wholly new antineighborhood idea.**

Taletskii's Lemma 13 already proves the corresponding parameter and
clique-cover conclusion for every independent set in a minimum-order planar
counterexample.  The reviewed theorem removes planarity and
minimum-counterexample hypotheses from the \(\gamma,\alpha,\gamma^\infty\)
projection and explicitly projects every eternal family.  The full
independent-set form is also the convenient iterated form of its
single-vertex case.  These relationships must be cited in any manuscript.
Novelty and priority remain unresolved because the directly relevant 2018
Klostermeyer--Krop--MacGillivray manuscript could not be inspected.

## Frozen review object

- Target:
  `math/lemmas/independent_antineighborhood_projection.md`
- Target SHA-256:
  `543df545dea27669645979ce61451091140d4621f1e11cfdeeaa33437f4b5620`
- Target size: 263 lines, 6,735 bytes
- Repository commit at review time:
  `9df3a414e6ba9f631ff68bff69d5ab0a37048f5e`
- Review date: 2026-07-26
- Model: finite simple graphs; attacks only at unoccupied vertices; exactly one
  adjacent guard moves to the attack; every family state dominates.

The target was not edited during this review.

## Claim-by-claim mathematical audit

### 1. Equality collapse and maximal independent sets

From

\[
 \gamma(G)\leq i(G)\leq\alpha(G)\leq\gamma^\infty(G)
\]

and \(\gamma(G)=\gamma^\infty(G)=k\), all four parameters equal \(k\).
Consequently every maximal independent set of \(G\) has size \(k\).  The
target uses precisely this conclusion and does not infer
\(\gamma=\alpha\) from well-coveredness alone.

### 2. Static projection to \(Q=G-N[A]\)

Let \(A\) be independent, \(|A|=t<k\), and let \(I\) be any maximal
independent set of \(Q\).  Then \(I\cup A\) is independent in \(G\).
It is maximal:

- every vertex in \(N[A]-A\) has a neighbor in \(A\);
- every vertex in \(Q-I\) has a neighbor in \(I\).

Thus \(|I|+t=k\).  This works for every maximal \(I\), so \(Q\) is
well-covered and

\[
 i(Q)=\alpha(Q)=k-t.
\]

Since \(t<k\), this also proves \(Q\ne\varnothing\), without an empty-graph
parameter convention.

The domination argument is exact.  The general bound gives
\(\gamma(Q)\leq i(Q)=k-t\).  If \(B\) dominated \(Q\) with at most
\(k-t-1\) vertices, then \(A\cup B\) would dominate \(G\): \(A\) dominates
\(N[A]\), while \(B\) dominates \(Q\).  Its size would be at most \(k-1\),
contradicting \(\gamma(G)=k\).  Hence

\[
 \gamma(Q)=k-t.
\]

No adjacency between \(Q\) and \(N[A]-A\) is incorrectly excluded or needed.

### 3. Forcing the anchor state in an arbitrary family

The target fixes an **arbitrary** eternal family \(\mathcal D\) of
\(k\)-sets, rather than selecting a favorable strategy.

Choose a maximum independent set \(I\) of \(Q\).  Then \(A\cup I\) is an
independent \(k\)-set.  Every such set belongs to every eternal \(k\)-family:
starting at any family state, attack an unoccupied target vertex.  No guard
already on the independent target can respond, so every legal one-guard
response increases target occupancy by one.  Repetition reaches exactly
\(A\cup I\), with every intermediate state still in the family.

Therefore the restricted slice

\[
 \mathcal E=
 \{D-A:D\in\mathcal D,\ A\subseteq D,\ D-A\subseteq V(Q)\}
\]

is nonempty.  The proof does not assume that every state containing \(A\)
has its other guards in \(Q\); it deliberately selects only the states that
do.  This is the key point that makes simpliciality unnecessary.

### 4. Domination and exact closure of the restricted slice

For \(C\in\mathcal E\), the lifted state is \(D=A\cup C\).  It dominates
\(G\), and no vertex of \(A\) has a neighbor in \(Q\).  Since the restricted
slice has no guard in \(N[A]-A\), it follows directly that \(C\) dominates
\(Q\).

Now fix an arbitrary \(r\in V(Q)-C\).  It is unoccupied in \(D\).
Global family closure supplies

\[
 u\in D\cap N_G(r),\qquad
 D'=(D-\{u\})\cup\{r\}\in\mathcal D.
\]

No member of \(A\) is adjacent to \(r\), by the definition of \(Q\).
Therefore \(u\in C\subseteq Q\).  The successor retains every guard in
\(A\), and all remaining guards outside \(A\) are still in \(Q\).  Hence

\[
 D'-A=(C-\{u\})\cup\{r\}\in\mathcal E.
\]

Both \(u\) and \(r\) lie in the induced graph \(Q\), so the original edge
\(ur\in E(G)\) is also an edge of \(Q\).  Thus exactly one guard moves along
exactly one edge.  The reasoning is pointwise in both \(C\) and \(r\), so
the required universal-universal-existential quantifiers are intact.

It follows that
\(\gamma^\infty(Q)\leq k-t\).  The general lower bound
\(\alpha(Q)\leq\gamma^\infty(Q)\) supplies the reverse inequality.
Therefore

\[
 \gamma(Q)=\alpha(Q)=\gamma^\infty(Q)=k-t,
\]

and the full theorem is valid.

### 5. Minimum-counterexample use of \(\theta\)

For a nonempty \(A\), \(Q\) is nonempty and proper.  The theorem gives
\(\gamma(Q)=\gamma^\infty(Q)=k-t\), while the parameter chain gives
\(\theta(Q)\geq k-t\).  If strict inequality held, \(Q\) itself would be a
smaller counterexample.  Minimum-order minimality therefore gives

\[
 \theta(Q)=k-t.
\]

This step is not circular and does not assume
\(\theta(G)=\theta(Q)+t\).  The target correctly warns that no such general
clique-cover deletion identity is available.

### 6. Complement translation

For \(H=\overline G\), an independent set \(A\) of \(G\) is a clique of
\(H\).  A vertex lies outside \(N_G[A]\) exactly when it is adjacent in
\(H\) to every member of \(A\).  Members of \(A\) are automatically excluded
from the intersection of open neighborhoods because \(H\) has no loops.
Thus

\[
 V(G)-N_G[A]=\bigcap_{a\in A}N_H(a)=N_H(A).
\]

Complementing the induced graph gives

\[
 \alpha(Q)=\omega(H[N_H(A)]),\qquad
 \theta(Q)=\chi(H[N_H(A)]).
\]

The displayed common-neighborhood conclusion

\[
 \chi(H[N_H(A)])=\omega(H[N_H(A)])=k-|A|
\]

is therefore exact.

The listed special cases are also correct:

- a \((k-1)\)-clique has a nonempty independent common neighborhood;
- a \((k-2)\)-clique has a bipartite common neighborhood containing an edge;
- no odd cycle can be complete to a \((k-2)\)-clique.

### 7. The full \(A\)-form is an iteration of the vertex case

The independent-set formulation is useful and its direct family proof is
clean, but it is not logically stronger than the arbitrary-single-vertex
projection.

Write \(A=\{a_1,\ldots,a_t\}\).  After applying the vertex theorem to
\(a_1\), every remaining \(a_j\) lies in \(G-N[a_1]\), because \(A\) is
independent.  Applying the theorem successively gives

\[
 G_j=G-N[\{a_1,\ldots,a_j\}]
\]

and decreases each of \(\gamma,\alpha,\gamma^\infty\) by one.  This reaches
the reviewed theorem after \(t\) steps.  Conversely, \(t=1\) is its vertex
case.

The arbitrary-vertex theorem is genuinely stronger than the earlier
simplicial reduction: for example, every vertex of \(C_4\) is nonsimplicial,
yet \(\gamma(C_4)=\gamma^\infty(C_4)=2\) and deleting any closed
neighborhood leaves \(K_1\), with all projected parameters equal to one.

### 8. Higher-clique complement conditions follow from the vertex condition

For a minimum counterexample, the \(t>1\) complement hierarchy is likewise a
convenient consequence of the \(t=1\) condition plus well-coveredness.

Every clique of \(H\) extends to a maximal clique, and all maximal cliques
have size \(k\).  Thus a \(t\)-clique \(A\) has a common-neighborhood clique
of size \(k-t\).  Fix \(a\in A\).  Inside \(H[N_H(a)]\), the set

\[
 (A-\{a\})\cup N_H(A)
\]

induces the join

\[
 K_{t-1}\vee H[N_H(A)].
\]

The vertex condition
\(\chi(H[N_H(a)])=k-1\) therefore gives

\[
 (t-1)+\chi(H[N_H(A)])\leq k-1.
\]

The common-neighborhood clique gives the reverse lower bound
\(\chi\geq\omega\geq k-t\).  Hence the entire hierarchy follows.  It is a
useful packaged invariant, but not additional pruning beyond the vertex
condition and the already known maximal-clique structure.

## Exact comparison with the \(k=3\) odd-wheel restriction

For \(k=3\), the reviewed complement condition at \(t=1\) says

\[
 \chi(H[N_H(v)])=\omega(H[N_H(v)])=2
\]

for every vertex \(v\): every open neighborhood is bipartite and contains an
edge.

This gives **no genuinely stronger \(k=3\) pruning** than the accepted
odd-wheel theorem plus equality collapse:

1. Since \(\omega(H)=3\), \(H[N_H(v)]\) is triangle-free.
2. If it were nonbipartite, a shortest odd cycle in it would be induced and
   would have length at least five.  Together with \(v\), it would be an
   induced odd wheel.
3. Conversely, an induced odd wheel centered at \(v\) puts an odd cycle in
   \(H[N_H(v)]\).
4. The fact that \(N_H(v)\) contains an edge is already forced because every
   maximal clique of \(H\) is a triangle.

Indeed, the accepted odd-wheel theorem assumes only
\(\gamma^\infty(G)=3\), whereas the reviewed complement corollary also uses
that \(G\) is a minimum counterexample.

For \(t=2\), the common neighborhood of every edge is nonempty because every
edge extends to a maximal triangle; it is independent because an edge among
two common neighbors would create a \(K_4\).  The existing complement
dictionary is stronger still on nonemptiness: \(\gamma(G)=3\) says that
**every pair**, including nonedges of \(H\), has a common neighbor.

Thus the \(k=3\) structural consequence is an alternative derivation and a
useful conceptual bridge, not a new restriction.

## Primary-literature audit and prior-art boundary

### Direct accessible overlap

D. Taletskii, *The Gamma-Theta Conjecture holds for planar graphs*,
arXiv:2412.20120v2 (submitted 2024-12-28, revised 2025-06-28), explicitly
uses the one-guard model.  Its notation is

\[
 G_I=G[V(G)-N[I]].
\]

Lemma 13 states that, for every nonempty independent set \(I\) in a
minimum-order planar counterexample,

\[
 \gamma(G_I)=\theta(G_I)=\gamma(G)-|I|.
\]

The proof also explicitly derives

\[
 \gamma^\infty(G_I)=\gamma(G)-|I|.
\]

Its attack-sequence argument forces at least \(|I|\) guards into \(N[I]\);
its Lemma 7(a) then bounds the eternal number of \(G_I\).  This is an exact
prior planar/minimum-counterexample instance of the reviewed projection's
parameter and \(\theta\) consequences.

The reviewed theorem still strengthens the accessible statement in three
ways:

1. it assumes only \(\gamma(G)=\gamma^\infty(G)\) for its
   \(\gamma,\alpha,\gamma^\infty\), and well-covered conclusions;
2. it has no planarity or counterexample-minimality hypothesis for those
   conclusions; and
3. it projects a restricted slice of **every** eternal family, preserving the
   full online closure quantifiers, rather than proving only the parameter
   inequality through the existence of a suitable minimum eternal state.

However, Taletskii's proof uses no planarity until it invokes minimality for
\(\theta\), so the general parameter statement is a close and natural
extension of the argument already present there.  Any novelty statement must
say this explicitly.

### Known static overlap

The well-covered and independence-number portion is classical.  For example,
B. Randerath and P. D. Vestergaard, *Well-covered graphs and factors*,
Discrete Applied Mathematics 154 (2006), 1416--1428,
DOI `10.1016/j.dam.2005.05.041`, Observation 2, states that if \(G\) is
well-covered and \(I\) is independent, then

\[
 G-N[I]\text{ is well-covered},\qquad
 \alpha(G-N[I])=\alpha(G)-|I|.
\]

That paper cites earlier sources for the observation.  These static
conclusions are not novel ingredients of the reviewed theorem.

### Other one-guard sources checked

The following accessible primary sources were searched by theorem text and
relevant neighborhood terminology:

- Klostermeyer--Mynhardt, *Domination, Eternal Domination, and Clique
  Covering*, DMGT 35 (2015), DOI `10.7151/dmgt.1799`;
- MacGillivray--Mynhardt--Virgile, *Eternal Domination and Clique Covering*,
  EJGTA 10(2) (2022), DOI `10.5614/ejgta.2022.10.2.19`;
- Klostermeyer--MacGillivray, *Eternal Domination: Criticality and
  Reachability*, DMGT 37 (2017), DOI `10.7151/dmgt.1918`;
- Virgile, *Mobile Guards' Strategies for Graph Surveillance and
  Protection*, PhD dissertation, University of Victoria (2024);
- Kimura--Matsumoto--Sato, *Note on the Eternal Domination Number of Planar
  Graphs and Vertex-Critical Graphs*, DML 17 (2026), DOI
  `10.47443/dml.2025.208`.

No source in this list was found to state the reviewed unrestricted
arbitrary-family theorem.

### Unavailable directly relevant source

The 2020 survey chapter cites:

> W. Klostermeyer, E. Krop, and G. MacGillivray, *On graphs with domination
> number equal to eternal domination number*, manuscript, 2018.

No inspectable copy was located.  Its title is directly on the reviewed
hypothesis, and Taletskii cites it for the \(C_4\)-free class theorem.
Accordingly, neither novelty nor priority is certified.

The scope-safe literature conclusion is:

> The reviewed result is a rigorous unrestricted and family-level
> generalization of an antineighborhood parameter reduction already present
> for minimum planar counterexamples in Taletskii's Lemma 13.  No exact
> unrestricted arbitrary-family statement was located in accessible sources.
> Novelty remains unresolved because directly relevant unpublished work is
> unavailable.

## Clean-room exhaustive falsification probe

`probe.py` imports no campaign evaluator.  It independently implements:

- small graph6 decoding;
- exact domination and independence;
- maximal-independent-set well-coveredness;
- exact clique partition;
- the greatest fixed point of dominating configurations in the precise
  one-guard game;
- restriction, projection, and lifting of every tested family response.

Nauty's `geng` is used only to provide one representative of every unlabeled
graph.  The probe exhausted all nonempty unlabeled graphs through order eight:

| Order | Graphs | \(\gamma=\gamma^\infty\) graphs | Independent \(A\) tested | Slice states | Attack obligations |
|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | 0 | 0 | 0 |
| 2 | 2 | 2 | 2 | 2 | 0 |
| 3 | 4 | 3 | 9 | 10 | 2 |
| 4 | 11 | 7 | 39 | 50 | 24 |
| 5 | 34 | 13 | 129 | 187 | 142 |
| 6 | 156 | 40 | 525 | 901 | 991 |
| 7 | 1,044 | 116 | 2,118 | 4,170 | 6,076 |
| 8 | 12,346 | 512 | 11,599 | 26,739 | 48,931 |
| **Total** | **13,598** | **694** | **14,421** | **32,059** | **56,166** |

For every eligible pair \((G,A)\), the probe checked:

- \(G-N[A]\ne\varnothing\);
- \(\gamma=\alpha=\gamma^\infty=k-|A|\);
- every maximal independent set has size \(k-|A|\);
- the restricted slice is nonempty;
- every slice state has the right size and dominates \(Q\);
- every unoccupied attack has a one-edge, one-guard successor in the slice;
- every projected witness lifts to an actual successor in the original
  family;
- the projected family lies in the independently computed greatest kernel of
  \(Q\).

It additionally checked all 5,413 maximum independent target states and the
finite \(\theta(Q)=k-|A|\) equality throughout this counterexample-free
range.  All checks passed.

The finite check uses the greatest eternal family.  It does not enumerate
every closed subfamily; the analytic proof establishes the stronger
arbitrary-family assertion.  There is no counterexample through order eight,
so the minimum-counterexample use of \(\theta\) is not tested nonvacuously.

Reproduction:

```text
python3 reviews/general_neighborhood_projection_independent/probe.py \
  --maximum-order 8
```

Hashes:

- target:
  `543df545dea27669645979ce61451091140d4621f1e11cfdeeaa33437f4b5620`
- probe:
  `4f1c0c959edee7fc246cb124e2362fa0cd3054960b3bfa86a4e428a11f8c5a51`
- result:
  `d7b39d73d79d1e79633793bc4ebcb1656aac0ecd980e4213e877de2c123025fb`
- nauty `geng`:
  `588052a87e5313f331aa145a0a641702b6c13b6e2387dd3c4807bf7f49fdaca1`

An externally timed replay took 1.96 seconds and about 30 MB maximum resident
memory.  Timing is deliberately omitted from the JSON so that repeated runs
produce a byte-identical result.  This was a lightweight laptop-safe job.

## Edge-case and defect ledger

| Attempted failure mode | Result |
|---|---|
| \(k=1\), \(t<k\), nonempty \(A\) | Impossible because no positive \(t<1\); theorem starts with a nonempty \(A\) only in the corollary |
| \(Q=\varnothing\) | Impossible for \(t<k\), since a maximal independent set of \(Q\) would make \(A\) maximal of size \(t<k\) in \(G\) |
| A family state contains \(A\) and a guard in \(N[A]-A\) | Harmless; the restricted slice excludes that state |
| Restricted slice is empty | Impossible because the forced state \(A\cup I\) belongs to every family |
| A guard in \(A\) answers an attack in \(Q\) | Impossible by the definition \(Q=G-N[A]\) |
| Response leaves the restricted slice | Impossible: the responder and attack both lie in \(Q\), and all of \(A\) remains fixed |
| Occupied-vertex attack used | No; attacks are quantified over \(V(Q)-C\) |
| More than one guard moves | No; every successor replaces exactly one named \(u\) by \(r\) |
| Complement uses a closed neighborhood | No; the exact translation is the common **open** neighborhood in \(H\) |
| \(\theta\) inferred without minimality | No; the target explicitly confines it to the minimum-counterexample corollary |
| Full \(A\)-form advertised as independent extra pruning | No; this review records its iterative redundancy beyond \(t=1\) |

| Severity | Count | Disposition |
|---|---:|---|
| Critical mathematical | 0 | None |
| High mathematical | 0 | None |
| Medium mathematical | 0 | None |
| Low mathematical/expository | 0 | None |
| Bibliographic scope correction | 1 | Cite and compare Taletskii Lemma 13 before publication |
| Novelty caution | 1 | Do not claim priority while the 2018 manuscript remains unavailable |

The frozen theorem is mathematically safe to use.  A revised manuscript
version should add the exact Taletskii comparison and describe the result as
an unrestricted, family-level generalization rather than an entirely new
antineighborhood reduction.
