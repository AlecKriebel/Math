# Hostile source and proof review of the half-order exclusion

## Verdict

**`ACCEPT_PROVED_CLASSICAL_COROLLARY_NO_NOVELTY_CLAIM`.**

The reviewed bytes are
`math/lemmas/half_order_exclusion.md`, SHA-256
`5d5e054305d97bf8e40f84073abd5236c6d726d66205b5e309ccfe39dd7d5f50`.

There is no mathematical blocker.  The note correctly proves, from the
classical Payan--Xuong/Fink--Jacobson--Kinch--Roberts extremal
characterization, that an isolate-free graph with
\(\gamma(G)=|V(G)|/2\) has \(\gamma(G)=\theta(G)\).  Consequently a connected
\(\gamma\)--\(\theta\) counterexample with common parameter \(k\) has
\[
  k<|V(G)|/2,\qquad\text{and hence}\qquad |V(G)|\geq 2k+1.
\]

The appropriate claim status is `PROVED`, with the classical theorem cited
as an imported published result.  The result must not be advertised as a
new structural theorem: its input is explicitly recalled in the primary
\(\gamma\)--\(\theta\) literature, and the clique-pair corollary is immediate.
Its value here is as a sound campaign reduction and search-lane pruning
rule.

Review date: 2026-07-26 PDT.

## 1. Audit of the classical input

The exact hypotheses in Theorem 1 of the reviewed note are supported.

1. The official Springer record for Fink, Jacobson, Kinch, and Roberts,
   *On graphs having domination number half their order*, confirms the
   authors, journal, volume, pages, year, DOI, and that the article
   characterizes **connected graphs of order \(2n\) with domination number
   \(n\)**:
   <https://doi.org/10.1007/BF01848079>.

2. Lingas, Miotk, Topp, and Żyliński, *Graphs with equal domination and
   covering numbers*, Journal of Combinatorial Optimization **39** (2020),
   55--71, states the connected characterization explicitly: a connected
   even-order graph has domination number half its order if and only if it
   is \(C_4\) or \(F\circ K_1\) for a connected graph \(F\).  It expressly
   attributes the result independently to Payan--Xuong and Fink et al.:
   <https://doi.org/10.1007/s10878-019-00454-6>.

3. The exact componentwise form used in the reviewed note is also printed
   as Theorem 1 in Chellali, Haynes, and Hedetniemi, *Lower bounds on the
   Roman and independent Roman domination numbers*, Applicable Analysis
   and Discrete Mathematics **10** (2016), 65--72:
   <https://doi.org/10.2298/AADM151112023C>.  Its hypotheses and conclusion
   are: even order, no isolated vertices, and every component either
   \(C_4\) or the corona of a connected graph.

4. The same disconnected statement appears as Theorem 2.1 in El-Zahar,
   Khamis, and Nazzal, *On the domination number of the Cartesian product of
   the cycle of length \(n\) and any graph*, Discrete Applied Mathematics
   **155** (2007), 515--522:
   <https://doi.org/10.1016/j.dam.2006.07.003>.

5. Most importantly for prior-art scope, Klostermeyer and Mynhardt,
   *Domination, Eternal Domination, and Clique Covering*, Discussiones
   Mathematicae Graph Theory **35** (2015), 283--300, explicitly says:
   \[
     \gamma(G)=n/2
     \quad\Longleftrightarrow\quad
     \text{each component is a \(4\)-cycle or a corona of a connected
     graph with \(K_1\)}.
   \]
   This occurs in the local primary arXiv source at lines 466--467 and is
   repeated in summary form at lines 955--956.  The local source has
   SHA-256
   `e2c26b432c7b815822ad6c36d43e4fb3a41a1aac8ef4c30f5119a8fe75d33eb5`;
   the published identifier is <https://doi.org/10.7151/dmgt.1799>.

The original Payan--Xuong full text and the theorem body of the original
Fink et al. article were not directly available in the local source cache;
the Springer preview exposes only the latter's abstract.  That access
limitation should remain recorded rather than being disguised as direct
inspection.  It is not a correctness blocker because the precise theorem,
including its hypotheses, is reproduced consistently in several
peer-reviewed published sources and in the primary \(\gamma\)--\(\theta\)
paper.

### Hypothesis-by-hypothesis check

- **Even order:** present in the cited characterization.  In Proposition 4,
  the premise \(\gamma(G)=|V(G)|/2\) already forces \(|V(G)|\) to be even
  because \(\gamma(G)\) is an integer.
- **No isolated vertices:** present and essential.  It is not silently
  dropped in Proposition 4, and connectedness with \(n\geq2\) supplies it
  in Corollary 5.
- **Connected base graph in a corona:** correct.  It describes one
  connected component.  If the base were disconnected, its corona would
  itself split into the coronas of the base components.
- **Component form:** correct.  It is explicitly published as quoted above.
  It also follows from the connected theorem and Ore's bound: additivity
  and \(\gamma(G_j)\leq |V(G_j)|/2\) force equality, and therefore even
  order, in every component.
- **\(C_4\) exception:** correct and necessary; \(C_4\) has no leaves and is
  not a corona \(F\circ K_1\).
- **Small endpoint:** \(F=K_1\) is allowed and gives \(K_2\), correctly
  covering the connected order-two equality case.

The no-isolate hypothesis cannot be weakened away.  For example,
\(K_1\mathbin{\dot\cup}C_5\) has order \(6\) and
\(\gamma=1+2=3=|V|/2\), but
\(\theta=1+3=4\); it is outside the characterization precisely because of
the isolated vertex.

## 2. Independent audit of every deduction

### \(C_4\)

The calculation
\[
  \gamma(C_4)=\alpha(C_4)=\theta(C_4)=2
\]
is correct.  No vertex dominates \(C_4\); two opposite vertices dominate
and form a maximum independent set; and two disjoint edges are a partition
of the vertex set into two cliques.  The lower bound
\(\alpha\leq\theta\) uses the correct vertex-clique-partition convention.

### Coronas

Let \(Q=F\circ K_1\), with support--leaf pairs
\(\{v_j,v'_j\}\), \(1\leq j\leq m\).

- Since \(N[v'_j]=\{v_j,v'_j\}\), every dominating set meets every pair.
  Thus \(\gamma(Q)\geq m\), while all supports dominate, giving
  \(\gamma(Q)=m\).
- The leaves form an independent \(m\)-set.  Each independent set uses at
  most one vertex from every adjacent pair, and the pairs partition all
  vertices.  Hence \(\alpha(Q)=m\).
- The \(m\) support--leaf edges partition \(V(Q)\) into cliques, so
  \(\theta(Q)\leq m\).  The independent leaves force at least \(m\) clique
  parts, so \(\theta(Q)=m\).

This check does not assume that the support vertices are independent and
therefore remains valid for an arbitrary connected base \(F\), including
one containing triangles.

### Proposition 4

Once evenness is inferred from the displayed equality, all hypotheses of
the classical theorem hold.  Each component has
\(\gamma=\theta\) by the preceding two computations.  Domination and
vertex clique-partition number are both additive over components: a
dominating set must dominate each component internally, and no clique can
contain vertices from two different components.  The conclusion
\(\gamma(G)=\theta(G)\) is therefore exact.

### Ore bound and the strict half-order inequality

The invoked Ore bound has the needed hypothesis and can also be checked
directly.  In an isolate-free graph, take any maximal independent set
\(I\).  The set \(I\) dominates by maximality, while \(V-I\) also dominates:
every vertex of \(I\) has a neighbor outside \(I\), and every vertex outside
\(I\) is occupied by that set.  Hence
\[
  \gamma(G)\leq \min\{|I|,|V-I|\}\leq |V|/2.
\]

For a connected graph of order at least two there are no isolates.  If a
counterexample attained equality in Ore's bound, Proposition 4 would give
\(\gamma=\theta\), contradicting the strict clique-cover gap.  Thus
\(k<n/2\).  Because \(n\) and \(k\) are integers,
\[
  2k<n\quad\Longrightarrow\quad n\geq2k+1.
\]
There is no parity gap or off-by-one error.

### Exact order-12 bookkeeping

For \(n=12\), the strict inequality gives \(k<6\).  Combining this with the
accepted minimum-parameter result \(k\geq3\) leaves exactly
\(\{3,4,5\}\).  Accepted campaign claim C-035 excludes the entire
\((n,k)=(12,3)\) slice, including disconnected graphs, and therefore in
particular excludes the connected slice.  The remaining **connected**
order-12 lanes are exactly \(k=4\) and \(k=5\).

The scope paragraph is accurate.  The note does not eliminate either of
those lanes, all order-12 graphs, or a disconnected total-parameter lane
merely by applying the inequality to the total graph.  A disconnected
counterexample only yields a connected counterexample component, to which
the inequality applies using that component's own order and parameter.

## 3. Model and notation audit

The proof is static except for invoking the definition of a
\(\gamma=\gamma^\infty<\theta\) counterexample and the already accepted
component reduction.  It does not use guard transitions and imports no
all-guards-move, total, eviction, or other eternal-domination variant.

The symbol \(\theta\) is used throughout as a partition of the **vertices**
into cliques, equivalently a coloring of the complement.  The support--leaf
edges are disjoint and cover every vertex, so the argument is about a
vertex clique partition, not an edge clique cover.  There is no
\(G\)/\(\overline G\) reversal.

## 4. Prior art and novelty boundary

The structural characterization is already explicit in the 2015
\(\gamma\)--\(\theta\) paper, not merely in unrelated domination
literature.  I did not locate the exact sentence “a counterexample has
\(k<n/2\)” as a separately numbered result there.  Nevertheless, once the
quoted characterization is combined with the evident support--leaf edge
partition, \(\gamma=\theta\) for every half-order extremal graph is an
immediate classical corollary.

Accordingly:

- it is sound to register and use the result as `PROVED`;
- it is useful as an explicit search reduction;
- the order-12 statement that only \(k=4,5\) remain is valid campaign
  bookkeeping using C-035; but
- neither the half-order characterization nor its two-line clique-cover
  consequence should be claimed as a novel publication-level theorem.

No edit to the reviewed note is required for correctness.  If it is moved
into a manuscript, the safest description is “the following classical
characterization immediately implies …”, with the exact no-isolate
hypothesis retained.

