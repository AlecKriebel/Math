# Hostile review: three-gate forced-witness package

Date: 2026-07-28 PDT

## Verdict

**UNCONDITIONAL PASS** for the claims expressly marked `PROVED` and for the
exact gamma-dropped control.

I reconstructed both halves of Theorem 2.1 from the one-guard definition,
checked the displayed-witness collision lemma after requiring its addition,
and independently recomputed the control graph.  I found no invalid attack,
unexamined successor, complement confusion, or inference of a graph nonedge
from a missing family response.

This verdict does **not** promote the experimental parity table, prove an
arbitrary odd-cycle shortening theorem, prove the full no-full branch, prove
the universal parameter-three case, or resolve the gamma--theta conjecture.
The package itself now states all of those limitations.

The exact reviewed source hashes are:

| file | SHA-256 |
|---|---|
| `NOTE.md` | `7d01124894ecc7d0745ab2f7b61ac3aa55ecda04dba82a464163d589d4a1f68e` |
| `verify.py` | `f030dbf6f287ee3e4d3b736760bd620bf7c417805d0804e9d575a58df1d31a19` |
| `result.json` | `fc4f1a4f462456704649e7b3ce778f07bc2e2c7107d391be2db60925cc432937` |
| `RESEARCH_LOG.md` | `57cad33d430242edce832e4cc4973752fbd49f349882a0ca52d002e7b2ec2a25` |

The independent checker is
`independent_check.py`, SHA-256
`2c32675bac64f430a9a4841b832c37e16dc14cfecdf7feb98fbe5c1b7fe61ff0`.
Its frozen output is `evidence.json`, SHA-256
`7d44239fede08812411ba1d22dcd9becef1984934adf80394e840591074ffd44`.

## 1. Semantic preliminaries

The response list is

\[
L(x)=\{u\in S:S-u+x\in\mathcal F\}.
\]

The note uses the two implications in the correct directions:

- \(u\in L(x)\) means that the direct-swap state is retained.  That state
  must dominate the omitted anchor \(u\); because the other two anchors are
  \(G\)-nonadjacent to \(u\), this forces \(ux\in E(G)\).
- \(u\notin L(x)\) means only that the direct-swap state is absent from
  \(\mathcal F\).  The proofs never turn this omission into \(ux\in E(H)\).

Every nondominating state is legitimately absent because every member of an
eternal family is required to dominate.  Every "dead under an attack"
argument is also legitimate: if the state were retained, closure would
require one retained successor reached by moving exactly one adjacent
guard.

## 2. Theorem 2.1, first inclusion

Assume \(b\notin L(q)\), so \(\{a,c,q\}\notin\mathcal F\).
The retained state \(D=\{a,c,c_0\}\) is justified by
\(b\in L(c_0)\).

Attack the unoccupied vertex \(q\) from \(D\).

1. Replacing \(c_0\) produces the assumed-absent state
   \(\{a,c,q\}\).
2. Replacing \(a\) produces \(\{c,c_0,q\}\), which misses \(c_1\)
   because \(cc_1,c_0c_1,qc_1\in E(H)\).
3. Therefore closure can only be satisfied by replacing \(c\), forcing
   \(A=\{a,c_0,q\}\in\mathcal F\).  Closure also supplies the needed move
   edge; the proof does not assume it.

Attack the unoccupied vertex \(b_1\) from \(A\).  Its three successor
shapes are exhausted as follows.

- \(\{a,c_0,b_1\}\) misses \(a_\ast\).
- \(\{a,b_1,q\}\) is dead under the unoccupied attack at \(c\):
  \(a\) cannot move because \(ac\in E(H)\), while the other two successor
  shapes are \(\{a,c,q\}\) and \(S-b+b_1\), both absent.
- If \(\{c_0,b_1,q\}\) were retained, attack the unoccupied \(b_0\).
  The guards \(b_1,q\) cannot move because
  \(b_0b_1,qb_0\in E(H)\), so the only possible shape is
  \(U=\{b_0,b_1,q\}\).  From \(U\), attack the unoccupied \(c\).
  Its three possible shapes are
  \(\{c,b_1,q\}\), \(\{c,b_0,q\}\), and
  \(\{c,b_0,b_1\}\).  In each, an attack at the unoccupied anchor \(a\)
  has no response: the guard \(c\) cannot move, and the remaining
  successors are the assumed-absent \(\{a,c,q\}\) or the absent
  type-\(b\) direct swaps.  Hence all three shapes, then \(U\), then
  \(\{c_0,b_1,q\}\), are absent.

Thus the attack at \(b_1\) from retained \(A\) has no response, a
contradiction.  This proves \(b\in L(q)\).

The symbolic replay in the independent checker inspected eight attack
nodes and all 24 guard-replacement shapes.  Six shapes were illegal by an
explicit \(H\)-edge, seventeen ended in a proved-absent state, and the one
remaining shape was the uniquely forced state.

## 3. Theorem 2.1, reflected inclusion

Assume \(c\notin L(q)\), so \(\{a,b,q\}\) is absent.
The retained state \(D'=\{a,b,b_1\}\) is justified by
\(c\in L(b_1)\).

Attack \(q\).  Replacing \(b_1\) gives the assumed-absent state;
\(\{b,b_1,q\}\) misses \(b_0\); hence closure forces
\(A'=\{a,b_1,q\}\).

Attack the unoccupied \(c_0\) from \(A'\).

- \(\{a,b_1,c_0\}\) misses \(a_\ast\).
- \(\{a,c_0,q\}\) is dead under attack at \(b\), using
  \(ab\in E(H)\), the assumed-absent state, and the absent type-\(c\)
  direct swap.
- From a hypothetically retained \(\{b_1,c_0,q\}\), attack \(c_1\).
  The guards \(c_0,q\) cannot move, so the only possible shape is
  \(\{c_0,c_1,q\}\).  Attack \(b\) there.  Its three possible shapes are
  each dead under attack at \(a\), using \(ab\in E(H)\), the
  assumed-absent state, and the two absent type-\(c\) direct swaps.

All three responses from \(A'\) are therefore absent, proving
\(c\in L(q)\).  The independent symbolic replay again checked eight attack
nodes and all 24 replacement shapes with the same disposition counts.

In both halves:

- every attacked vertex is unoccupied;
- the distinctness of \(q\) from the fixed auxiliary vertices is used;
- each candidate replaces exactly one guard;
- an unknown move edge is never assumed present or absent; and
- every nondomination claim is witnessed by three explicit \(H\)-edges.

The cyclic rotation

\[
a\mapsto b\mapsto c\mapsto a,\qquad
a_i\mapsto b_i\mapsto c_i\mapsto a_i,\qquad
a_\ast\mapsto b_\ast\mapsto c_\ast\mapsto a_\ast
\]

preserves the displayed geometry and rotates
\(P_a,P_b,P_c\).  The checker verifies this incidence invariance directly,
so the cyclic versions do not hide an orientation mismatch.

## 4. Lemma 2.2 and displayed-witness collisions

The first reviewed draft required \(q\) to be distinct from all twelve
displayed vertices but then informally invoked \(\gamma(G)\geq3\), which
only guarantees some common \(H\)-neighbor of a critical pair.  I treated
that as a blocker until the current Lemma 2.2 supplied the missing collision
audit.  The revision is correct.

For \(P_a=\{b_0,c_1\}\), all twelve displayed candidates are covered:

- \(b_0,c_1\) themselves cannot be witnesses in a simple graph.
- No anchor works.  List membership gives
  \(ab_0,cb_0,ac_1,bc_1\in E(G)\), eliminating \(a,b,c\).
- The type-\(a\) vertices \(a_0,a_1,a_\ast\) already have their physical
  \(H\)-incidence to \(a\).  If one is common to \(b_0,c_1\), it is
  already a literal cap.
- The labels \(b_\ast,c_\ast\) do not occur in the fixed auxiliary roles
  of either Theorem 2.1 attack tree.  If either were a common neighbor,
  the same trees would force the missing list color and contradict its
  displayed type.
- \(b_1\) and \(c_0\) are the only genuine collisions.

For the \(b_1\) collision, suppose \(b_1c_1\in E(H)\).  From retained
\(\{a,c,c_0\}\), attack the unoccupied \(b_\ast\).  The direct type-\(b\)
swap is absent and \(\{c,c_0,b_\ast\}\) misses \(c_1\), so closure forces
\(\{a,c_0,b_\ast\}\).  Attack the unoccupied \(b_1\):

- \(\{a,c_0,b_1\}\) misses \(a_\ast\);
- \(\{a,b_1,b_\ast\}\) is dead under attack at \(c\), using the two
  absent type-\(b\) direct swaps; and
- \(\{c_0,b_1,b_\ast\}\) misses \(c_1\), where the three required
  complement edges are \(c_0c_1,b_1c_1,b_\ast c_1\).

This is a contradiction.

The actual reflection for the \(c_0\) collision is

\[
b\leftrightarrow c,\quad
a_0\leftrightarrow a_1,\quad
b_0\leftrightarrow c_1,\quad
b_1\leftrightarrow c_0,\quad
b_\ast\leftrightarrow c_\ast,
\]

with \(a,a_\ast\) fixed.  Explicitly, if \(c_0b_0\in E(H)\), start at
\(\{a,b,b_1\}\), attack \(c_\ast\), force
\(\{a,b_1,c_\ast\}\), and attack \(c_0\).  The three shapes respectively
miss \(a_\ast\), are dead under attack at \(b\), and miss \(b_0\).
The independent checker replays both collision trees: each has three attack
nodes, nine candidate shapes, and three explicit nondomination witnesses.

This closes the finite collision gap and validates the cyclic collision
versions.  It does not supply the still-missing well-founded descent through
dynamic physicalization, which the note correctly leaves open.

## 5. Independent control-graph reconstruction

The review checker uses integer adjacency masks and imports no campaign
module.  It decodes and re-encodes the graph6 record independently from the
explicit complement edge table.  It obtains:

\[
|V|=12,\qquad |E(G)|=45,\qquad G\text{ connected},
\]

and

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,3).
\]

The checks behind those values are:

- exhaustive subset tests for \(\gamma,i,\alpha\);
- the triangle \(012\) in \(H\) for \(\theta\geq3\), together with an
  independently checked proper 3-coloring of \(H\) for \(\theta\leq3\);
- a reverse-obligation queue computation of the greatest eternal families,
  structurally separate from the source verifier's repeated
  simultaneous-deletion loop.

The independent greatest-family sizes are

\[
|\mathcal K_1|=0,\qquad |\mathcal K_2|=0,\qquad |\mathcal K_3|=181.
\]

For all 181 retained triples, the checker replays all
\(181(12-3)=1629\) unoccupied attacks and finds 2,934 retained legal
one-guard responses.  It reproduces both frozen source hashes:

```text
greatest triple family:
4e9e5e160535c2bd14d2a47a14ed78c02627f347bf5579981716275b66e7b350

complete response table:
8be2fad3ee18ad777df90b69f487cfdfa72a8414ce504195e12b63c772b834b4
```

It also reconstructs all nine exact response lists.  Each of the three
boundary states has exactly its displayed cap as the sole undominated
vertex:

| boundary | undominated vertex |
|---|---:|
| \(\{b,a_0,c_1\}=\{1,3,6\}\) | \(b_\ast=9\) |
| \(\{c,a_1,b_0\}=\{2,4,7\}\) | \(c_\ast=10\) |
| \(\{a,b_1,c_0\}=\{0,5,8\}\) | \(a_\ast=11\) |

Finally, each critical pair \(\{4,6\},\{5,7\},\{3,8\}\) dominates \(G\)
and has no common \(H\)-neighbor.  This verifies the claimed sharpness:
the control realizes the odd boundary cycle only because
\(\gamma(G)=2\), while the witness step needs the no-dominating-pair
consequence of \(\gamma(G)\geq3\).

Both source and independent verifiers passed under
`PYTHONHASHSEED=0,1,17,8675309`.

## 6. Reproduction

From `gamma_theta_eternal_domination/`:

```text
python3 -I -B -W error \
  math/working/three_gate_odd_holonomy/verify.py \
  --check math/working/three_gate_odd_holonomy/result.json

python3 -I -B -W error \
  reviews/three_gate_odd_holonomy_hostile/independent_check.py \
  --check reviews/three_gate_odd_holonomy_hostile/evidence.json
```

Both commands return `PASS`.
