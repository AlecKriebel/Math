# A certified dynamic exclusion of an inactive induced \(C_5\)

## Status and scope

Date: 2026-07-28 (PDT)

This note uses the standard **one-guard-moves** eternal-domination model:
attacks occur only at unoccupied vertices, exactly one adjacent guard moves,
and every retained successor dominates.

The main result is a certificate-backed local theorem candidate.  The
generator and a separately written reconstruction/replay checker both pass;
external hostile review by a different research agent is still pending, so
the campaign claim registry should not promote it before that audit.  Subject
to that review, it proves that the inactive graph in the parameter-three
target-response setup has no induced \(C_5\).  It does **not** yet rule out
inactive induced odd cycles of length at least seven, force the inactive graph
to be bipartite, prove the complete \(k=3\) case, or resolve the
gamma--theta conjecture.

No literature-priority claim is made.

## 1. The local dynamic lemma

Let \(G\) be a finite graph, let \(\mathcal F\) be a one-guard eternal
family of dominating triples, and put \(H=\overline G\).  Fix a target
\(x\).  Let

\[
 C=r_0r_1r_2r_3r_4r_0
\tag{1.1}
\]

be an induced \(C_5\) of \(H-x\), with indices read modulo five.  For each
rim edge, suppose there is a vertex

\[
 p_i\notin V(C)\cup\{x\}
\tag{1.2}
\]

such that

\[
 T_i=\{r_i,r_{i+1},p_i\}
\tag{1.3}
\]

is an independent triple of \(G\) belonging to \(\mathcal F\).  The
witnesses \(p_i\) need not be distinct.

Assume that neither rim endpoint can answer the attack at \(x\) from its
named witness state:

\[
 T_i-r_i+x\notin\mathcal F,
 \qquad
 T_i-r_{i+1}+x\notin\mathcal F
 \quad(0\le i<5).
\tag{1.4}
\]

### Certified local lemma

The configuration (1.1)--(1.4) does not exist.

This statement is deliberately local.  It assumes neither
\(\gamma(G)=3\), nor \(\alpha(G)=3\), nor a clique-cover gap, nor a full
response at another state.  The only family states required initially are
the five named triples in (1.3).

## 2. Finite proof and exact coverage

The proof is a complete finite case split on equality among the five
witnesses \(p_0,\ldots,p_4\).

Every equality pattern has a unique restricted-growth string of length
five.  There are

\[
 B_5=52
\tag{2.1}
\]

such strings.  For one pattern, form the finite template whose vertices are

\[
 \{r_0,\ldots,r_4\}
 \cup\{\text{distinct witness blocks}\}
 \cup\{x\}.
\tag{2.2}
\]

The template order ranges from seven to eleven.  Introduce:

- one variable \(h_{uv}\) for each possible edge of \(H\);
- one variable \(f_D\) for membership of each template triple
  \(D\) in \(\mathcal F\);
- one variable \(m_{D,y,u}\) saying that the guard at \(u\in D\)
  answers the unoccupied attack at \(y\notin D\).

The CNF contains exactly the following clauses.

1. **Domination.**  If \(f_D\) is true, no outside template vertex has
   \(H\)-edges to all three members of \(D\).
2. **One-guard closure.**  If \(f_D\) is true and \(y\notin D\), at least
   one current guard \(u\in D\) is selected; that selection forces
   \(uy\notin E(H)\) and
   \[
      f_{D-u+y}.
   \]
3. **Induced rim.**  The ten pairs on the rim are fixed to be exactly the
   five edges of \(C_5\).
4. **Witness states.**  Each \(p_i\) is joined in \(H\) to
   \(r_i,r_{i+1}\), and \(f_{T_i}\) is true.
5. **Inactivity.**  The ten successor variables in (1.4) are false.

There are no clauses imposing a domination number, independence-number
bound, coloring, full target, connectedness, global common-neighbor
condition, response at occupied vertices, or all-guards movement.

Why is the finite template a sound relaxation of an arbitrary larger graph?
Restrict the real graph to (2.2) and interpret \(f_D\) by literal membership
in the real family.  A real retained state dominates every template vertex.
For an attack at a template vertex, the moving guard and attacked vertex
both lie in the template, so the successor does too.  Hence the restricted
assignment satisfies all five clause groups.  Behavior at vertices outside
the template is simply omitted, which can only make the formula weaker.

All 52 formulas are UNSAT.  Each has a DRAT proof independently replayed by
`drat-trim`.  A clean-room checker independently reconstructs every DIMACS
byte, verifies the complete restricted-growth-string list, checks every
artifact hash, and replays every proof.

The bundle summary is:

\[
\begin{array}{c|c}
\text{witness-block template order}&\text{number of cases}\\ \hline
7&1\\
8&15\\
9&25\\
10&10\\
11&1
\end{array}
\]

with 215,100 reconstructed input clauses and 276,375 total proof bytes.
The manifest SHA-256 is

```text
3260bd78dd4a8726b2b16f92fcc3dfafc8309531133c3ae34f0f0d3ba24193d7
```

Reproduction:

```text
python3 -I -B -W error \
  math/working/inactive_odd_cycle_attack/independent_check.py
```

The output ends with

```text
"partition_count": 52
"all_instance_bytes_match": true
"all_drat_proofs_verified": true
```

This proves the local lemma.

## 3. Consequence for the active/inactive target split

Assume

\[
 \alpha(G)=\gamma^\infty(G)=3,
\tag{3.1}
\]

let \(\mathcal F\) be any eternal triple-family, and fix \(x\).  Let
\(A_x\) be the family-relative active set from C-108 and put

\[
 R_x=V(G-x)\setminus A_x.
\tag{3.2}
\]

Assume also

\[
 \gamma(G-x)\ge3.
\tag{3.3}
\]

### Corollary

\[
 \boxed{\overline{G-x}[R_x]\text{ has no induced }C_5.}
\tag{3.4}
\]

### Proof

Suppose \(r_0,\ldots,r_4\) induce a \(C_5\) in
\(\overline{G-x}[R_x]\).  For every rim edge \(r_ir_{i+1}\), condition
(3.3) says that the pair \(\{r_i,r_{i+1}\}\) does not dominate \(G-x\).
Thus some deletion vertex \(p_i\) is nonadjacent in \(G\) to both rim
endpoints.  Equivalently,

\[
 \{r_i,r_{i+1},p_i\}
\]

is a triangle of \(\overline{G-x}\).  No \(p_i\) lies on the induced
\(C_5\), because two consecutive vertices of an induced \(C_5\) have no
common neighbor on that cycle; and \(p_i\ne x\) by construction.

The displayed triple is an independent triple of \(G\).  By (3.1) it is
maximum, so the maximum-independent-state forcing theorem puts it in every
eternal triple-family, including \(\mathcal F\).  Both rim endpoints lie
in \(R_x\).  C-108's vertex-star propagation therefore says that neither
endpoint successor at \(x\) belongs to \(\mathcal F\).  The five triples
and their ten absent successors satisfy (1.1)--(1.4), contrary to the local
lemma. \(\square\)

In the equality-critical deletion branch of C-108, (3.3) holds with
equality.  Since C-108 already proves that
\(\overline{G-x}[R_x]\) is triangle-free, any remaining non-bipartite
inactive graph has a shortest odd cycle that is induced.  The new result
raises its possible length:

\[
 \boxed{\text{every remaining inactive odd-cycle obstruction has length
 at least seven}.}
\tag{3.5}
\]

## 4. Exact parity control

The result cannot be strengthened to “the inactive graph is acyclic.”
The 16-vertex graph

```text
OQifur}UO]}iTij]tpo}v
```

has

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3).
\]

For target \(x=15\), its greatest eternal triple-kernel has 304 states,
the root \(\{5,6,7\}\) has a full response, and the inactive set is

\[
 \{0,1,2,3,8,11\}.
\]

The inactive complement induced edges are

\[
 01,\ 12,\ 23,\ 30,\ 8\,11,
\]

so \(0,1,2,3\) induce a genuine \(C_4\).  The deletion graph also has all
five parameters equal to three.  The standalone verifier recomputes all
parameters, the greatest kernel, the active set, and the induced cycle:

```text
python3 -I -B -W error \
  math/working/inactive_odd_cycle_attack/verify_c4_control.py
```

Its result file has SHA-256

```text
a4c9197db6add4d817ff4118d9af07672ca1284bbcb07d4aef6cbe1ec76d55e1
```

This is a positive equality control, not a counterexample to the
gamma--theta conjecture.

## 5. Remaining gap

The next exact target is the analogue of the local lemma for induced
\(C_{2q+1}\) with \(q\ge3\).  The \(C_5\) proof does not provide a
length-independent attack argument: directly enumerating witness
identifications grows by the Bell numbers.  Until a general shortening or
projection mechanism is proved, (3.5), not bipartiteness of the full
inactive graph, is the rigorous conclusion.
