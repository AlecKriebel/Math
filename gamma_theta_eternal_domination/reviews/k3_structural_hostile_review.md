# Hostile review of the day-one \(k=3\) structural restrictions

**Review date:** 2026-07-25 14:33 PDT  
**Files reviewed:**

- `math/lemmas/k3_structural_day1.md`
  (`sha256:15a5033356d6a93b8f23011e28e6b6556b85af9f3bc32b145ceb5382655a5d88`)
- `src/search/k3_wheel_probe.py`
  (`sha256:fa438e526d8a459d4cb361de4e2e8aa44d907095ea3365f82ace7083d60b9a74`)

**Independent review artifact:**

- `reviews/k3_structural_hostile_probe.py`
  (`sha256:8150d6cfa6f6b45440fc1f6f0fff9e499a25c7e9cd0bf8a08b5cd11fb4109aa9`)

## Verdict

**ACCEPT all four mathematical statements without correction.** Lemma 1,
Theorem 2, Lemma 3, and Theorem 4 are valid under the campaign's exact
one-guard-moves definition: attacks are only at unoccupied vertices and one
guard traverses one edge. The odd-wheel obstruction and the order-12
template split may be promoted to `PROVED`.

**ACCEPT the three finite counts as `OBSERVED`.** An independent
definition-level program reproduced the reported \(0,5,78\) static counts
and \(0,2,47\) odd-wheel rejection counts for orders \(6,7,8\). It also
checked the obstruction on every connected unlabeled odd-wheel host through
order eight and found no size-three eternal family.

No critical, high, or medium-severity defect was found. There is one
low-severity methodology limitation in the observational probe: verifier B
is called only after verifier A passes a graph through the static prefilter.
This does not affect the theorem proofs or the reproduced counts, but it
means the checked-in program is not a symmetric differential test on all
input graphs.

## 1. Exact-model audit

The relevant closure condition is

\[
 \forall D\in\mathcal F\ \forall r\notin D\ \exists u\in D\cap N_G(r):
 (D-\{u\})\cup\{r\}\in\mathcal F.
\]

The arguments never attack an occupied vertex. The \(W_5\) argument
considers the unoccupied rim vertex \(v_3\), and it examines exactly the
three possible old guard positions. The hub is not adjacent to the attack
in \(G\), while the two legal moves each move one guard along one edge and
produce a nondominating state. There is no simultaneous movement or
all-guards convention hidden in any statement.

The independent probe constructed the complement of \(W_5\) directly and
obtained the only legal candidate successors:

\[
\begin{array}{c|c|c}
\text{moved guard}&\text{successor}&\text{dominates }G\\
\hline
v_0&\{c,v_1,v_3\}&\text{no}\\
v_1&\{c,v_0,v_3\}&\text{no}.
\end{array}
\]

The guard at \(c\) has no edge to \(v_3\) in \(G\). This is exactly the
claimed local certificate.

## 2. Lemma 1: automatic static constraints

If every pair in \(H\) has a common neighbor, every edge belongs to a
triangle. Under \(\omega(H)=3\), a clique of size two therefore cannot be
maximal. A maximal singleton would be an isolated vertex, but an isolated
vertex cannot share a common neighbor with another vertex; another vertex
exists because \(\omega(H)=3\). Hence every maximal clique is a triangle.

The same common-neighbor property puts every nonadjacent pair at distance
two, so the diameter is at most two. If a vertex \(v\) had unique neighbor
\(u\), a common neighbor of \(u,v\) would be a vertex distinct from both
endpoints (neighborhoods are open in a simple graph) and a second neighbor
of \(v\). Thus \(\delta(H)\geq2\).

As a finite check independent of either campaign verifier, all unlabeled
graphs through order eight satisfying the two premises were enumerated.
The numbers at orders \(3,\ldots,8\) were respectively

\[
 1,\ 1,\ 4,\ 12,\ 53,\ 317.
\]

Every one had all maximal cliques of size three, minimum degree at least two,
and diameter at most two.

## 3. Theorem 2: complement and monotonicity arithmetic

On the wheel vertex set,

\[
 \overline{K_1\vee C_{2q+1}}
 =K_1\mathbin{\dot\cup}\overline{C_{2q+1}}.
\]

This is an induced equality: edges to vertices outside the selected set are
irrelevant. Proposition 5 and Lemma 9 of `math/reductions.md` then give

\[
 \gamma^\infty\!\left(
 K_1\mathbin{\dot\cup}\overline{C_{2q+1}}\right)
 =1+3=4.
\]

The induced-subgraph inequality is used in the correct direction. Lemma 8
proves
\(\gamma^\infty(G[W])\leq\gamma^\infty(G)\), hence an induced subgraph
requiring four guards forces the host to require at least four guards.
Its maximum-intersection projection proof remains valid under unoccupied
attacks: if the responding guard were outside the induced vertex set, the
number of guards inside would increase beyond its chosen maximum.

The independent oracle checked the base complements of odd wheels with rim
lengths \(5,7,9,11\), at total orders \(6,8,10,12\). In every case it found

\[
 \gamma=3,\qquad \gamma^\infty=4,
\]

by literal fixed-point deletion over dominating configurations. It also
scanned all connected unlabeled graphs at orders \(6,7,8\). There were
respectively \(0,7,382\) graphs whose complement contained an induced odd
wheel, and no one of these graphs admitted a closed family of dominating
three-sets.

## 4. Lemma 3: forced state and failed swaps

The wheel triangle \(S=\{c,v_0,v_1\}\) in \(H\) is an independent
three-set in \(G\). Under \(\alpha(G)=3\), it is maximum, so the
independent-set forcing lemma puts it in every eternal three-family. The
attack at \(v_3\) is unoccupied.

Complement adjacency gives:

- \(cv_3\in E(H)\), so \(c\) cannot move to \(v_3\) in \(G\);
- \(v_0v_3,v_1v_3\notin E(H)\), so these are the only legal one-edge moves;
- \(v_2\) is adjacent in \(H\) to all of
  \(\{c,v_1,v_3\}\), so the first successor does not dominate \(v_2\) in
  \(G\);
- \(v_4\) is adjacent in \(H\) to all of
  \(\{c,v_0,v_3\}\), so the second successor does not dominate \(v_4\) in
  \(G\).

The fact that the wheel is induced is sufficient for both failed-domination
witnesses. Adjacencies from wheel vertices to vertices outside the wheel
cannot make \(v_2\) or \(v_4\) adjacent to one of the three occupied wheel
vertices.

## 5. Theorem 4: SPGT split and order twelve

For a parameter-three counterexample,
\[
 \omega(H)=\alpha(G)=3<\theta(G)=\chi(H).
\]
Thus \(H\) itself violates perfection, and SPGT supplies an induced odd
hole or odd antihole.

For an odd antihole on \(2q+1\) vertices,
\[
 \omega(\overline{C_{2q+1}})=\alpha(C_{2q+1})=q.
\]
The ambient bound \(\omega(H)=3\) leaves only \(q=2,3\), hence lengths five
and seven. The length-five antihole is isomorphic to \(C_5\) and belongs to
the odd-hole branch; \(\overline{C_7}\) is the only additional template.

Every induced odd hole in \(H\) is hub-free: an external vertex complete to
the rim would induce an odd wheel, contradicting Theorem 2. The proof that a
hole has at least two external vertices is also sound. Adjacent rim vertices
have no common neighbor on an induced cycle of length at least five. The
pair-common-neighbor condition therefore assigns each rim edge an external
common neighbor. If there were only one external vertex, it would be
adjacent to both endpoints of every rim edge and hence to every rim vertex,
making it a forbidden hub.

Consequently an odd hole at order twelve has length at most ten. The only
odd lengths at least five are \(5,7,9\). The four proposed branches
\[
 C_5,\quad C_7,\quad C_9,\quad\overline{C_7}
\]
are exhaustive but need not be disjoint, exactly as stated. No symmetry
assumption or unstated connectedness premise is used in this case split.

## 6. Probe audit and reproduced measurements

Both checked-in wheel recognizers implement the exact induced-wheel
predicate. For a proposed rim they require induced degree two at every rim
vertex and connectedness, which characterizes a single cycle; they then
require a vertex outside the rim adjacent to every rim vertex. The loop
`range(5, graph.n, 2)` is correct because a hub must remain outside the rim,
so a rim cannot use all vertices.

The independent probe does not import either verifier, graph
representation, invariant routine, eternal transition routine, or wheel
recognizer. It reproduced:

| order | connected unlabeled | static prefilter | odd-wheel rejections |
|---:|---:|---:|---:|
| 6 | 112 | 0 | 0 |
| 7 | 853 | 5 | 2 |
| 8 | 11,117 | 78 | 47 |

Only length-five wheels occur among the reported static targets, with counts
\(2\) and \(47\) at orders seven and eight. The independent oracle also
found zero eternal-three graphs in each static-prefilter row, agreeing with
the checked-in probe.

### Low severity P1: verifier B is downstream of verifier A's filter

At lines 145--149 of `k3_wheel_probe.py`, verifier A computes the prefilter
and rejected graphs are skipped. Verifier B is invoked only at lines
152--170 for a graph already accepted by A. Therefore the program confirms
that A and B agree on every reported target, but it would not detect a
hypothetical false negative in A's prefilter.

This is not a mathematical gap: the counts are explicitly labeled
observations, verifier A has separate exhaustive audits, and the independent
review program reproduced the universe without either implementation. It is
also consistent with the function docstring, which promises to cross-check
every graph that *passes* the prefilter. If this probe is later upgraded
from a measurement to a finite certificate, compute the three B invariants
before the `continue` and require agreement on every generated graph.

## Promotion decision

- Promote Lemma 1, Theorem 2, Lemma 3, and Theorem 4 to **`PROVED`**.
- Retain the order \(6\)--\(8\) table as **`OBSERVED`**, not
  `CERTIFIED-FINITE`.
- The low-severity asymmetric-filter limitation does not require a source
  change for the current observational use.

