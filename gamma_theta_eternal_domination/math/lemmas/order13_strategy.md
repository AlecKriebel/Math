# Exact strategy for the order-13 frontier

## Status and scope

This is a bounded search-design note, not a finite exclusion theorem.  Its
parameter reduction is a consequence of accepted claims C-003, C-006,
C-036, C-049, and C-050.  Formula counts below are exact combinatorial
counts for the stated proposed encodings, but no order-13 encoder has yet
received the graph-to-CNF and implementation audits required for a claim.

Every dynamic statement uses the standard one-guard model: an attack is at
an unoccupied vertex, and exactly one adjacent guard moves to it.

The recommended first lane is the complete parameter-three slice.  It has
an exact four-template cover, reuses the most mature campaign machinery,
and has formulas an order of magnitude smaller than the proposed
parameter-five target.  A 30-second proofless pilot on its `hole11` branch
returned UNSAT in 0.0202 seconds, making that branch the first
certificate-production candidate.  This pilot is explicitly not a result.

## 1. Exact parameter range

### Proposition 1

Relative to C-050, any counterexample of order \(13\) is a
minimum-order counterexample, is connected, and has common parameter

\[
 k=\gamma=\alpha=\gamma^\infty\in\{3,4,5\}.
\tag{1.1}
\]

#### Proof

C-050 excludes every smaller order, so an order-13 counterexample is
minimum.  Component additivity then forces it to be connected: otherwise
one of its proper components would be a smaller counterexample.

C-006 gives \(k\geq3\).  C-036 gives

\[
 13\geq 2k+1,
\]

so initially \(k\leq6\).  C-049 applies to this minimum counterexample and
gives

\[
 13\geq \left\lceil\frac{5k}{2}\right\rceil.
\]

The value \(k=6\) would require \(13\geq15\), so \(k\leq5\).  This leaves
exactly (1.1). \(\square\)

The conclusion inherits C-050's explicit published lower-order premise.  A
future order-13 frontier would be a certified extension of that premise,
not a campaign-only enumeration through order 13.

## 2. Exact local constraints from C-051

Let \(G\) be a hypothetical order-13 counterexample and put
\(H=\overline G\).  For every \(t\)-clique \(A\) of \(H\), \(1\leq t<k\),
C-051 gives

\[
 \chi(H[N_H(A)])=\omega(H[N_H(A)])=k-t.
\tag{2.1}
\]

The common neighborhood is nonempty.  The complete list by parameter is:

| \(k\) | \(t=1\) | \(t=2\) | \(t=3\) | \(t=4\) |
|---:|---|---|---|---|
| 3 | \(\chi=\omega=2\) | \(\chi=\omega=1\) | -- | -- |
| 4 | \(\chi=\omega=3\) | \(\chi=\omega=2\) | \(\chi=\omega=1\) | -- |
| 5 | \(\chi=\omega=4\) | \(\chi=\omega=3\) | \(\chi=\omega=2\) | \(\chi=\omega=1\) |

Here `1` means a nonempty independent common neighborhood, while `2`
means a bipartite common neighborhood containing an edge.  In particular:

- every clique of size less than \(k\) extends to a \(K_k\);
- no odd cycle of \(H\) is complete to a \((k-2)\)-clique;
- for \(k=3\), every open neighborhood of \(H\) is bipartite.

These are sound hard filters.  The stronger projected conclusion
\(\gamma=\alpha=\gamma^\infty=k-t\) on \(G-N_G[A]\) is also available,
although (2.1) is the cheapest graph-only form.

C-048 independently supplies the hard conditions that \(G\) has no
simplicial vertex, \(\delta(G)\geq2\), and the neighbors of every
degree-two vertex are nonadjacent.

The following are only heuristics unless separately proved: preference for
near-regular graphs, density windows learned from order 12, prioritizing
vertex-transitive hosts, or assuming that equality is nearly attained in
the McCuaig--Shepherd bound.

## 3. Parameter three: recommended first lane

### 3.1 Exact template cover

For \(k=3\), \(H\) has \(\omega(H)=3<\chi(H)\).  The Strong Perfect Graph
Theorem supplies an odd hole or odd antihole.  An odd antihole
\(\overline{C_{2q+1}}\) has clique number \(q\), so only
\(C_5\) and \(\overline{C_7}\) can occur.  The accepted one-guard
antihole theorem C-017 excludes \(\overline{C_7}\).

Thus \(H\) has an odd hole.  C-051 makes it hub-free.  A spanning
induced \(C_{13}\) would have clique number two, contrary to
\(\omega(H)=3\).  Therefore the following four overlapping templates are
complete:

\[
 C_5,\qquad C_7,\qquad C_9,\qquad C_{11}.
\tag{3.1}
\]

For each hole, a rim edge has an external common neighbor by the accepted
pair-common-neighbor characterization.  Consequently one may relabel the
rim as \(0,\ldots,\ell-1\) and one common neighbor of rim edge \(01\) as
vertex \(\ell\).  This is the same orbit-complete labeling mechanism used
at order 12.  It does not simultaneously fix an unrelated anchor.

### 3.2 Pilot formula census

A read-only runtime parameterization of the accepted order-12 core to
\(n=13\), with a complete first-use-canonical coloring bank, produced the
following exploratory bytes:

| branch | variables | base clauses | coloring rows | full clauses | full literals | bytes |
|---|---:|---:|---:|---:|---:|---:|
| `hole5` | 9,802 | 29,791 | 10,935 | 40,726 | 493,820 | 1,805,539 |
| `hole7` | 9,802 | 29,800 | 5,103 | 34,903 | 349,248 | 1,372,338 |
| `hole9` | 9,802 | 29,813 | 2,295 | 32,108 | 281,028 | 1,168,197 |
| `hole11` | 9,802 | 29,830 | 1,023 | 30,853 | 250,664 | 1,076,723 |

The exact exploratory hashes and claim boundary are in
`results/logs/order13_strategy_k3_template_pilot.json`.

The existing free-vertex signature breaker also has a clean proposed
generalization.  Sort vertices outside the fixed rim plus its named common
neighbor by their signatures to that fixed core.  Its additional census is:

| branch | core bits | free vertices | adjacent comparators | clauses | literals |
|---|---:|---:|---:|---:|---:|
| `hole5` | 6 | 7 | 6 | 378 | 3,852 |
| `hole7` | 8 | 5 | 4 | 1,020 | 14,344 |
| `hole9` | 10 | 3 | 2 | 2,046 | 36,868 |
| `hole11` | 12 | 1 | 0 | 0 | 0 |

This breaker is not yet a hard constraint.  It first needs a written
covariance proof and a clean-room truth-table and clause-multiset audit for
the order-13 formula.  The residual rim reflection used at order 12 may
likewise be used only after a new exact action proof.

### 3.3 Concrete bounded experiment

The exact exploratory `hole11` bytes had SHA-256

```text
1ab880e6d2cf9014e70362437b530c8d534fe57db7620029d06bc3ed9afee901
```

CaDiCaL 3.0.1, seed zero, with a 30-second internal limit and no proof
request, returned UNSAT in 0.0202 seconds with 5.92 MiB maximum RSS.

This establishes only that proof production is likely cheap.  It does not
establish formula coverage or UNSAT: the formula was generated by an
unaudited runtime parameterization, and no proof was retained or checked.
The historical exploratory ledger also failed to retain the exact solver
argument vector, CPU time, or stdout/stderr transcript.  Those missing
fields have not been reconstructed.  The corrected ledger records this
protocol defect explicitly, and no production job may repeat it.

### 3.4 Production order

The bounded order is:

1. prove and independently audit (3.1) and the order-13 constructor;
2. reconstruct all four formulas independently and freeze hashes;
3. produce and check an LRAT for `hole11`;
4. proceed in order `hole9`, `hole7`, `hole5`;
5. if a branch becomes hard, partition only that branch by an exhaustive
   Boolean prefix of the lexicographically minimum free-vertex signature.

The four templates may overlap.  Disjointness is unnecessary for an UNSAT
cover: the mathematical theorem proves every target lies in their union,
and every member of the union is excluded when all four branches are
certified.  A coverage manifest must nevertheless list all four branches
and their exact formula and proof hashes.

## 4. Generic anchored synthesis sizes

For comparison, consider the direct complement encoding used for C-037,
generalized to \((n,k)=(13,k)\):

- one \(H\)-edge variable per pair;
- one external common-neighbor witness for every \((k-1)\)-set;
- one family variable per \(k\)-set;
- one move variable per state, unoccupied attack, and possible guard;
- no \(K_{k+1}\), an anchored \(K_k\), connectedness of \(G\), exact
  one-guard family clauses, and independent-state forcing;
- all \(k^{13-k}\) anchor-normalized color clauses;
- row and column lexicographic breakers.

The exact combinatorial census is:

| \(k\) | states | move variables | all variables | base clauses | color clauses | full DoubleLex clauses | full DoubleLex literals |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 286 | 8,580 | 9,802 | 29,774 | 59,049 | 90,932 | 1,740,356 |
| 4 | 715 | 25,740 | 29,393 | 79,320 | 262,144 | 343,117 | 5,109,628 |
| 5 | 1,287 | 51,480 | 59,280 | 157,116 | 390,625 | 548,978 | 5,916,975 |

These counts exclude any C-051 redundant strengthening.  Formula size is
not a solver-time estimate, but it makes the parameter-three template lane
the clear first laptop target.

## 5. Parameter four: second computational lane

The order-12 `src/synthesis_k4/encoding.py` construction is mathematically
generic in the order in most of its loops, but its constants, schemas,
hashes, generator, candidate checker, DoubleLex appender, and production
runner are deliberately frozen to \(n=12\).  They must not be monkeypatched
for a decisive result.

A new order-13 module should reproduce the 29,393-variable census above.
The C-045 orbit-minimum proof should generalize to nine outer rows and four
anchor columns, but this requires a new full-formula covariance audit,
including any C-051 clauses.

The exact C-051 static strengthenings are:

\[
\begin{aligned}
\chi(H[N_H(v)])&=\omega(H[N_H(v)])=3,\\
\chi(H[N_H(u)\cap N_H(v)])&=
\omega(H[N_H(u)\cap N_H(v)])=2
\quad(uv\in E(H)).
\end{aligned}
\]

The second line says every edge-common-neighborhood is bipartite and
contains an edge.  Conditional local color variables can encode this
without enumerating graphs.  Such clauses are hard filters only after an
independent semantic proof and small-order exhaustive differential test.

The accepted large-hole argument based on the three-set common-neighbor
property is order-independent: an induced odd hole needs at least four
outside vertices.  Hence an order-13 target has an SPGT obstruction among

\[
 C_5,\ C_7,\ C_9,\ \overline{C_7}.
\]

An \(\overline{C_9}\) obstruction is impossible because it induces
\(C_9\) in \(G\), whose one-guard eternal domination number is five.
These templates are useful for structural analysis, but fixing both one
template and an anchored \(K_4\) on arbitrary labels is unsound.  The
whole anchored formula avoids that incidence problem.

If the whole DoubleLex formula is not decided in a 60-second proofless
pilot, partition by the first sorted outer row.  Column order and no
\(K_5\) leave exactly

```text
0000  0001  0011  0111
```

as four disjoint, exhaustive cubes of the strengthened formula.  A further
split must use explicit binary edge-variable cubes or a proved stabilizer
action; heuristic canonical labels cannot support a negative claim.

## 6. Parameter five: structural-first lane

There is no existing parameter-five synthesis module.  The direct formula
is still laptop-sized as an input, but it has 59,280 variables, 1,287
family states, and 51,480 move variables.  It should follow the
parameter-three and parameter-four gates rather than be the first
production run.

C-051 has its strongest hierarchy here:

- every vertex neighborhood of \(H\) has \(\chi=\omega=4\);
- every edge-common-neighborhood has \(\chi=\omega=3\);
- every triangle-common-neighborhood is bipartite and contains an edge;
- every \(K_4\) has a nonempty independent common neighborhood.

Before constructing the full formula, the proof lane should audit whether
known near-extremal refinements of the McCuaig--Shepherd domination bound,
combined with no simplicial vertices and this hierarchy, exclude
\((13,5)\) analytically.  This is a research direction, not a current
filter.

If synthesis is needed, use an anchored \(K_5\), complete five-color bank,
and a newly proved DoubleLex action.  The first sorted outer row then has
exactly five possible cubes:

```text
00000  00001  00011  00111  01111
```

They are the initial resumable partition.  Local C-051 coloring witnesses
should be added only as audited redundant constraints.  The construction
and the independent candidate verifier must share no transition core.

## 7. Resource and evidence gates

No production solve begins until all earlier gates for that lane pass.

### Gate A: mathematical coverage

- a self-contained graph-to-CNF theorem;
- a proof of every relabeling and symmetry restriction;
- for \(k=3\), the four-template union (3.1);
- for a partition, a machine-readable proof that cubes are exhaustive and
  pairwise disjoint;
- an adversarial one-guard and complement-coloring audit.

### Gate B: independent construction

- deterministic constructor and exact manifest;
- byte-identical clean-room reconstruction;
- exhaustive comparator truth tables;
- brute-force differential tests on small orders;
- deliberate rejection tests for occupied attacks, multiple-guard moves,
  missing domination, and coloring \(G\) instead of \(H\).

### Gate C: bounded exploration

- one solver process only;
- 30--60 seconds, deterministic seed, no proof;
- monitor RSS and stop at 2 GiB;
- classify every outcome as exploratory;
- on SAT, immediately freeze the graph and family and invoke two
  independent semantic verifiers.

### Gate D: certificate production

- run one branch or cube at a time;
- require at least 4 GiB available memory and 8 GiB free-disk reserve;
- cap solver RSS at 2 GiB and raw proof output at 2 GiB per attempt;
- checkpoint before launch and after every child process;
- preserve raw binary DRAT, normalize fail-closed, run warning-fatal
  forward and backward checks, produce LRAT, and replay with a separately
  pinned checker;
- if projected proof volume exceeds the cap, stop and refine the Boolean
  partition rather than relaxing resource safeguards.

An UNSAT solver exit or a timeout is not evidence.  A SAT model is not a
counterexample until a standalone verifier checks \(\gamma=k\), the exact
one-guard family, and \(\theta>k\).  A complete negative slice requires the
coverage theorem, case manifest, every checked proof, and an independent
coverage audit.

## 8. Portfolio recommendation

For the next bounded sprint:

1. **70%:** formalize and certify the four order-13 \(k=3\) templates,
   beginning with `hole11`;
2. **20%:** generalize and independently reconstruct the whole anchored
   \(k=4\) DoubleLex formula, but do not start production until the \(k=3\)
   gate is stable;
3. **10%:** structural work on the \(k=5\) C-051 hierarchy and
   near-\(2n/5\) domination case.

Rebalance after the first two certified \(k=3\) branches.  If either branch
is SAT, counterexample verification becomes the sole priority.  If
`hole11` and `hole9` are certified cheaply, continue the template lane.  If
a branch exceeds a 60-second proofless pilot or a projected 2 GiB proof,
partition it before spending additional laptop time.
