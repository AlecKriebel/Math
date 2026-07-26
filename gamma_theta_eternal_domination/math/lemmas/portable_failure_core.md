# Portable independent-root failure cores

## Status and scope

This note restores the full independent-set forcing statement already proved
in `math/lemmas/maximum_independent_states.md` (Claim C-010), which was
restated with unnecessarily narrow hypotheses in
`math/lemmas/three_step_forced_obstruction.md`.  It then packages finite
failure certificates as portable induced obstruction cores.  This packaging
is consistent with, and at the parameter level is implied by, the full
induced-subgraph monotonicity theorem in `math/reductions.md`, Lemma 8
(Claim C-005).  No new monotonicity theorem is claimed here.

The results in Sections 2--5 are self-contained statements for the standard
one-guard-moves eternal domination model:

- attacks are made only at unoccupied vertices;
- exactly one guard moves;
- the move follows one edge to the attacked vertex; and
- every configuration retained by an eternal family dominates the graph.

The proof does not use the \(\gamma\)--\(\theta\) conjecture.

The finite statements about the two named graphs in Section 6 are separate
from the universal theorems.  Their ranked attack DAGs and induced embeddings
are direct finite certificates in
`certificates/portable_failure_cores.json`.  The broader one-vertex-extension
enumeration is explicitly classified as `OBSERVED`, not as a theorem or a
resolution of the conjecture.

## 1. Finite-horizon notation

Let \(G\) be a finite simple graph and fix \(k\geq1\).  Write
\(\mathcal C_k(G)\) for the dominating \(k\)-subsets of \(V(G)\).  For
\(\mathcal X\subseteq\mathcal C_k(G)\), put

\[
 \Phi_G(\mathcal X)=
 \left\{D\in\mathcal C_k(G):
 \begin{array}{l}
 \text{for every }r\in V(G)-D\text{ there is }u\in D\cap N_G(r)\\
 \text{such that }D-u+r\in\mathcal X
 \end{array}
 \right\}.
\]

Define

\[
 \mathcal K_0(G,k)=\mathcal C_k(G),\qquad
 \mathcal K_{h+1}(G,k)=\Phi_G(\mathcal K_h(G,k)).
\]

Thus \(D\in\mathcal K_h(G,k)\) exactly when the defender can keep every
configuration dominating for the next \(h\) online attacks.  Because the
configuration set is finite, the descending chain stabilizes at the greatest
eternal \(k\)-family.

The recursive failure certificates of
`math/lemmas/three_step_forced_obstruction.md` prove
\(D\notin\mathcal K_h(G,k)\): a nonterminal node gives one unoccupied attack
and has one child for every adjacent occupied guard; a terminal node gives an
undominated vertex.

## 2. Every independent \(k\)-set is forced

The word "maximum" in the restricted restatement in
`math/lemmas/three_step_forced_obstruction.md` is unnecessary.  The following
is Claim C-010, repeated here so the portable-certificate argument is
self-contained.

**Lemma 1 (independent-set forcing).**  If \(\mathcal F\) is an eternal
dominating family of \(k\)-sets in \(G\), then every independent set
\(S\subseteq V(G)\) of cardinality \(k\) belongs to \(\mathcal F\).

**Proof.**  Choose any \(D\in\mathcal F\).  If \(D\ne S\), attack a vertex
\(s\in S-D\).  This attack is unoccupied.  No guard in \(D\cap S\) is
adjacent to \(s\), since \(S\) is independent.  Hence every legal responding
guard lies in \(D-S\), and the successor

\[
 D'=D-u+s
\]

satisfies \(|D'\cap S|=|D\cap S|+1\).  Closure of \(\mathcal F\) supplies
such a successor in \(\mathcal F\).  Repeating at most
\(k-|D\cap S|\) times reaches \(S\), so \(S\in\mathcal F\). \(\square\)

This proof uses all three model details that are easy to conflate: the attack
is unoccupied, one guard moves, and the response guard must be adjacent to the
attacked vertex.

**Corollary 2 (strengthened finite-horizon obstruction).**  Let \(S\) be any
independent \(k\)-set in \(G\).  If

\[
 S\notin\mathcal K_h(G,k)
\]

for some finite \(h\), then

\[
 \gamma^\infty(G)\geq k+1.
\]

**Proof.**  A putative eternal \(k\)-family would contain \(S\) by Lemma 1
and would be contained in every finite kernel, contradicting
\(S\notin\mathcal K_h(G,k)\).  Also \(\alpha(G)\geq k\), so the standard
bound \(\alpha(G)\leq\gamma^\infty(G)\) excludes every guard count below
\(k\).  Integrality gives the result. \(\square\)

Unlike the restricted formulation in the three-step note, Corollary 2 does
not assume that \(S\) is maximum or that \(\alpha(G)=k\).  This generality was
already present in `math/lemmas/maximum_independent_states.md`.

## 3. Portability to induced supergraphs

**Theorem 3 (portable independent-root obstruction).**  Let \(H=G[W]\) be
an induced subgraph of \(G\).  Let \(S\subseteq W\) be an independent
\(k\)-set.  If

\[
 S\notin\mathcal K_h(H,k)
\]

for some finite \(h\), then

\[
 \gamma^\infty(G)\geq k+1.
\]

**Proof.**  Suppose that \(G\) has an eternal \(k\)-family
\(\mathcal F\).  By Lemma 1, \(S\in\mathcal F\).

Starting from \(S\), follow an \(h\)-failure certificate in \(H\).  Every
configuration \(D\) in this play is a \(k\)-subset of \(W\), and every named
attack \(r\) lies in \(W-D\).  If \(D\) fails to dominate some vertex of
\(G\), then \(D\notin\mathcal F\), which is already a contradiction.
Otherwise the eternal-family condition supplies a response guard
\(u\in D\cap N_G(r)\).  Since \(D\cup\{r\}\subseteq W\) and \(H\) is
induced,

\[
 D\cap N_G(r)=D\cap N_H(r).
\]

Thus \(u\) is one of the response guards exhaustively represented in the
\(H\)-certificate, and the successor \(D-u+r\) remains a subset of \(W\).

Eventually the certificate reaches a state \(D\subseteq W\) and a witness
\(x\in W\) with \(N_H[x]\cap D=\varnothing\).  Inducedness and
\(D\subseteq W\) give \(N_G[x]\cap D=\varnothing\), so \(D\) does not
dominate \(G\), again contradicting \(D\in\mathcal F\).  Therefore no eternal
\(k\)-family exists in \(G\).  The independent \(k\)-set \(S\) implies
\(\alpha(G)\geq k\), and \(\alpha\leq\gamma^\infty\) excludes fewer guards.
\(\square\)

Inducedness is essential to the proof: for a non-induced subgraph, an edge
omitted from \(H\) could introduce an additional responding guard in \(G\)
or could dominate a terminal witness.

At the level of the inequality alone, Theorem 3 also follows from
Corollary 2 applied in \(H\) and the previously proved monotonicity

\[
 \gamma^\infty(H)\leq\gamma^\infty(G)
\]

for induced \(H\) (Claim C-005).  The direct proof above is recorded because
it transports the actual finite attack certificate, preserves its horizon,
and identifies exactly when an outside vertex lets a branch terminate even
earlier.

**Corollary 4 (alpha-tight obstruction core).**  If \(H\) is induced in
\(G\),

\[
 \alpha(H)=k
 \quad\text{and}\quad
 \gamma^\infty(H)>k,
\]

then \(\gamma^\infty(G)>k\).

**Proof.**  Choose a maximum independent \(k\)-set \(S\) of \(H\).  The
greatest eternal \(k\)-family of \(H\) is empty.  Since the finite kernel
chain stabilizes, \(S\notin\mathcal K_h(H,k)\) for some finite \(h\).
Apply Theorem 3. \(\square\)

Consequently, for fixed \(k\), every alpha-tight graph \(H\) with
\(\gamma^\infty(H)>k\) is a forbidden induced subgraph for graphs having an
eternal \(k\)-family.  This is a certificate-oriented specialization of the
already established general induced-subgraph monotonicity theorem.

## 4. The certificate support is a portable core

**Corollary 5 (support reduction).**  Let \(T\) be a finite failure
certificate in \(G\) rooted at an independent \(k\)-set \(S\).  Let \(W_T\)
contain every vertex that occurs

1. in a configuration of \(T\);
2. as an attacked vertex of \(T\); or
3. as a terminal undominated witness of \(T\).

Then \(S\) has a failure certificate in the induced subgraph \(G[W_T]\).
Hence every graph containing \(G[W_T]\) as an induced subgraph has eternal
domination number at least \(k+1\).

**Proof.**  Every configuration, attack, responding guard, and terminal
witness in \(T\) belongs to \(W_T\).  Passing to the induced subgraph
preserves all adjacencies among these vertices.  A nonterminal configuration
that dominates \(G\) dominates \(G[W_T]\); its adjacent occupied responders
are unchanged.  Each terminal witness remains undominated.  Thus the same
tree is valid in \(G[W_T]\).  The final statement is Theorem 3. \(\square\)

This gives a sound graph-only learning rule: once a search obtains an
independent-root failure certificate, its induced support can be stored as a
portable obstruction rather than rediscovering the same game-tree failure in
every supergraph.

## 5. Ranked attack DAG certificates

Recursive trees duplicate a subtree whenever two response histories reach the
same configuration.  The following equivalent certificate shares those
subtrees.

A **ranked attack DAG** for guard count \(k\) consists of:

- a finite nonempty set \(\mathcal P\) of dominating \(k\)-sets;
- a positive integer rank \(\rho(D)\) for each \(D\in\mathcal P\);
- an unoccupied attack \(a(D)\notin D\) for each \(D\in\mathcal P\); and
- for every \(u\in D\cap N(a(D))\), either
  - a named vertex undominated by \(D-u+a(D)\), or
  - a successor \(D-u+a(D)\in\mathcal P\) with strictly smaller rank.

**Lemma 6 (ranked-DAG soundness).**  If an independent \(k\)-set
\(S\in\mathcal P\), then \(\gamma^\infty(G)\geq k+1\).

**Proof.**  Lemma 1 forces \(S\) into every putative eternal \(k\)-family.
At a state \(D\in\mathcal P\), attack \(a(D)\).  Every possible response
either immediately yields a non-dominating configuration or strictly lowers
the positive integer rank.  An infinite legal defense would therefore
produce an infinite strictly descending sequence of positive integers,
which is impossible.  Thus no eternal \(k\)-family exists.  As before,
\alpha(G)\geq k\) excludes fewer guards. \(\square\)

Unrolling the rank descent gives an ordinary recursive failure certificate.
Conversely, any finite recursive failure tree can first be viewed as an
occurrence-labelled acyclic attack graph.  To obtain a ranked DAG in the
present state-indexed sense, normalize each reachable dominating
configuration by its exact greatest-fixed-point deletion rank and select a
witnessing attack whose dominating successors have strictly smaller exact
ranks; only then merge repeated configurations.  Blindly merging occurrences
at different remaining horizons is not justified.  Thus the DAG form is a
certificate compression, not a different game model.

Theorem 3 applies verbatim to a ranked attack DAG in an induced subgraph.

## 6. Two portable three-guard cores in the measured deep tail

Define

```text
J = J@l|bfNuVK_     (order 11, size 32)
Q = Kun_w{vRrblV    (order 12, size 40).
```

The direct certificate file records independent-root ranked attack DAGs with:

| core | root | root rank | attack states | distinct terminal states | tree nodes after unrolling |
|---|---:|---:|---:|---:|---:|
| \(J\) | \(\{1,4,6\}\) | 5 | 8 | 9 | 19 |
| \(Q\) | \(\{1,2,6\}\) | 6 | 9 | 11 | 27 |

The certified three-guard kernel profiles are

\[
\begin{aligned}
J &: 110,105,100,88,64,10,0,\\
Q &: 147,143,136,128,119,93,28,0.
\end{aligned}
\]

Both have \(\gamma=\alpha=3\), empty greatest three-guard kernel, and a
nonempty greatest four-guard kernel.  Hence
\(\gamma^\infty(J)=\gamma^\infty(Q)=4\).

Six explicit maps in the certificate show that the other six order-12 graphs
in the previously measured eight-row \(K_3/K_4\) tail contain \(J\) as an
induced subgraph.  Together with \(J\) itself and \(Q\), Theorem 3 compresses
all eight failures to two portable obstruction cores.

The deterministic checker also scans the fixed 526-row population from
`results/three_step_kernel_measurement.json` and
`certificates/k3_three_step_edge_toggle.ndjson`.  Its exact-isomorphism
replay certifies that 37 of those 526 graphs contain induced \(J\): 30 have
earliest forced rank 3 and the seven \(J\)-core rows have earliest forced
rank 5.  The only other row whose earliest forced rank exceeds 3 is \(Q\),
at rank 6.  This is a `CERTIFIED-FINITE` statement about that fixed derived
population, not about all graphs of order 11 or 12.

Finally, the generator enumerates all \(2^{11}-1=2047\) nonempty
neighborhoods for one new vertex over the fixed labeled graph \(J\).  Pinned
`labelg` canonicalization reports 623 unmarked isomorphism keys.  Among the
89 reported classes with \(\gamma=\alpha=3\), the distribution of the
earliest forced independent-triple rank is

\[
 1:12,\qquad 2:32,\qquad 3:36,\qquad 4:3,\qquad 5:6.
\]

The six rank-5 keys are exactly the six induced supergraphs certified above.
Five add a true twin, one for each vertex orbit of \(J\); the sixth is a
near-twin extension.  This 623-class statement is retained as `OBSERVED`:
the checker reconstructs all labeled origins, replays `labelg`, verifies
every parameter and kernel value, and checks every raw-to-key isomorphism,
but it does not independently derive a canonical normal form or prove that
two distinct reported keys are nonisomorphic.

## 7. Consequence for search

At guard count three, any graph containing \(J\) or \(Q\) as an induced
subgraph can be rejected before a full eternal-family computation.  For a
specific embedding \(\varphi:V(H)\hookrightarrow V(G)\), a synthesis solver
may soundly add the induced-copy blocking clause

\[
 \bigvee_{uv\in E(H)}\neg e_{\varphi(u)\varphi(v)}
 \;\vee\!
 \bigvee_{uv\notin E(H)}e_{\varphi(u)\varphi(v)}.
\]

The clause says that at least one adjacency on the proposed induced copy must
change.  It is sound because Theorem 3 rules out every graph containing that
copy, independently of vertices outside the image.

These two forbidden cores and the finite measurements do not resolve the
\(\gamma\)--\(\theta\) conjecture and do not raise the exhaustive global
order bound.  They provide a reusable structural reduction and a compact
explanation of the deepest failures in one recorded near-miss population.

## 8. Reproduction

From the campaign root, generate the deterministic certificate, measurement,
and extension table with

```text
PYTHONPATH=src PYTHONWARNINGS=error \
python3 -m search.portable_failure_core generate
```

Then replay every direct certificate, both ordinary-set kernel profiles, all
526 induced-\(J\) occurrence checks, all 2,047 extension origins, every
raw-to-key isomorphism, and all recorded extension parameters with

```text
PYTHONPATH=src PYTHONWARNINGS=error \
python3 -m search.portable_failure_core audit
```

The audit is deterministic and rejects malformed schemas, stale source or
input hashes, non-exhaustive response lists, occupied attacks, illegal moves,
invalid terminal witnesses, nondecreasing ranks, bad induced embeddings,
omitted source-population rows, and extension-table changes.
