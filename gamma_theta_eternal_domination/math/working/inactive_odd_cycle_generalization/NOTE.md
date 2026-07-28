# A certified dynamic exclusion of an inactive induced \(C_7\)

## Status and scope

Date: 2026-07-28 (PDT)

All statements use the standard one-guard-moves eternal-domination model:
attacks occur only at unoccupied vertices, exactly one adjacent guard moves,
and every retained successor dominates.

The main result of this directory is a **certificate-backed finite theorem
candidate, ready for hostile review**:

> The local inactive-rim configuration already excluded for \(C_5\) cannot
> occur on an induced \(C_7\), for any equality pattern among its seven
> edge witnesses.

The 877 witness partitions reduce to 93 orbits under the dihedral group of
the seven-cycle.  Every representative formula has a checked DRAT proof,
and a separately written checker reconstructs all formulas, verifies the
complete orbit coverage, and replays all proofs.

This result does **not** exclude inactive odd cycles of length at least nine,
prove that the inactive graph is bipartite, prove the complete \(k=3\) case,
or resolve the gamma--theta conjecture.  No literature-priority claim is
made.

## 1. The local \(C_7\) theorem

Let \(G\) be a finite graph, let \(\mathcal F\) be a one-guard eternal
family of dominating triples, and put \(H=\overline G\).  Fix a target
\(x\).  Suppose

\[
 C=r_0r_1\cdots r_6r_0
\tag{1.1}
\]

is an induced \(C_7\) of \(H-x\).  For each rim edge, suppose there is a
vertex

\[
 p_i\notin V(C)\cup\{x\}
\tag{1.2}
\]

such that

\[
 T_i=\{r_i,r_{i+1},p_i\}\in\mathcal F
\tag{1.3}
\]

and \(T_i\) is independent in \(G\).  Indices are read modulo seven.  The
witnesses \(p_i\) need not be distinct.

Assume that neither rim endpoint can answer the attack at \(x\) from its
named witness state:

\[
 T_i-r_i+x\notin\mathcal F,
 \qquad
 T_i-r_{i+1}+x\notin\mathcal F
 \quad(0\le i<7).
\tag{1.4}
\]

### Certified local theorem candidate

The configuration (1.1)--(1.4) does not exist.

The theorem is deliberately local.  It assumes neither
\(\gamma(G)=3\), nor \(\alpha(G)=3\), nor a clique-cover gap, nor
connectedness.  Only the seven named family states are initially forced.

## 2. Complete dihedral certificate

Equality among \(p_0,\ldots,p_6\) is represented by a restricted-growth
string of length seven.  There are

\[
 B_7=877
\tag{2.1}
\]

such strings.  A rotation or reflection of the rim sends one witness
partition to another and induces a literal relabeling isomorphism of the
corresponding formula.  Canonicalizing under

\[
 D_7=\langle\text{cyclic shift},\text{reversal}\rangle
\tag{2.2}
\]

leaves 93 representatives.  Their orbit-size distribution is

\[
\begin{array}{c|ccc}
\text{orbit size}&1&7&14\\ \hline
\text{number of orbits}&2&57&34.
\end{array}
\tag{2.3}
\]

For one representative, the finite template consists of the seven rim
vertices, one vertex per witness block, and \(x\).  It therefore has order
between nine and fifteen.  The CNF uses:

- a variable \(h_{uv}\) for every edge of \(H\);
- a variable \(f_D\) for every template triple \(D\);
- a variable \(m_{D,y,u}\) saying that the guard at \(u\in D\) answers
  the unoccupied attack at \(y\notin D\).

Its clauses impose exactly:

1. domination of every retained state;
2. literal one-guard closure at every unoccupied template attack;
3. the induced \(C_7\) rim;
4. the witness spokes and named states in (1.2)--(1.3); and
5. the fourteen absent successors in (1.4).

No clause imposes a domination number, an independence-number bound,
colorability, connectedness, planarity, or any all-guards move.

The restriction from an arbitrary larger graph to a template is sound.  A
real retained triple dominates every template vertex.  An attack at a
template vertex and its responding guard both lie in the template, so its
successor also lies there.  Attacks outside the template are omitted, which
only weakens the formula.

All 93 representative formulas are UNSAT.  Their checked bundle contains:

\[
\begin{array}{c|rrrrrrr}
\text{template order}&9&10&11&12&13&14&15\\ \hline
\text{representatives}&1&8&31&33&16&3&1.
\end{array}
\tag{2.4}
\]

The clean-room audit reconstructed 1,418,936 input clauses and replayed
1,739,039 proof bytes.  The certificate manifest SHA-256 is

```text
d5187e0a35595865f79063b02f74e6fa819aa5b0fe0b78c2c09bbdb15d148ee4
```

and the independent audit-result SHA-256 is

```text
37450e8a8f5b56e2023ee924fd2fa9263b1fe10ad675049ccedc1885e42eb29b
```

Reproduction:

```text
python3 -I -B -W error \
  math/working/inactive_odd_cycle_generalization/independent_check.py
```

The output asserts all of the following:

```text
"partition_count": 877
"representative_count": 93
"all_instance_bytes_match": true
"all_drat_proofs_verified": true
```

This proves the local theorem once the bundle survives hostile review.

## 3. Consequence for the active/inactive target split

Assume

\[
 \alpha(G)=\gamma^\infty(G)=3,
\tag{3.1}
\]

let \(\mathcal F\) be any eternal triple-family, and fix \(x\).  Let
\(A_x\) be the C-108 active set and put

\[
 R_x=V(G-x)\setminus A_x.
\tag{3.2}
\]

Assume also

\[
 \gamma(G-x)\ge3.
\tag{3.3}
\]

### Corollary candidate

\[
 \boxed{\overline{G-x}[R_x]\text{ has no induced }C_7.}
\tag{3.4}
\]

### Proof

Suppose \(r_0,\ldots,r_6\) induce a \(C_7\) in
\(\overline{G-x}[R_x]\).  For every rim edge, (3.3) says that
\(\{r_i,r_{i+1}\}\) does not dominate \(G-x\).  Hence some deletion vertex
\(p_i\) is nonadjacent in \(G\) to both endpoints.  No \(p_i\) is a rim
vertex, because consecutive vertices of an induced cycle of length at least
four have no common neighbor on that cycle.

Thus \(\{r_i,r_{i+1},p_i\}\) is an independent triple of \(G\).  By (3.1)
it is maximum, so maximum-independent-state forcing puts it in
\(\mathcal F\).  Both endpoints lie in \(R_x\).  C-108 therefore makes
both endpoint successors at \(x\) absent.  These states satisfy
(1.1)--(1.4), contradicting the local theorem. \(\square\)

In the equality-critical deletion branch, C-108 already makes
\(\overline{G-x}[R_x]\) triangle-free, and the accepted \(C_5\) certificate
excludes an induced five-cycle.  The new result raises the surviving
inactive odd-hole threshold to

\[
 \boxed{\text{length at least nine}.}
\tag{3.5}
\]

## 4. A human mechanism that survives all lengths

The following propagation lemma is independent of the finite certificate
and explains one of the recurring attack patterns.

### Lemma 4.1 (private-star propagation)

Let \(E,T\in\mathcal F\) be \(k\)-states containing \(v\), where \(T\) is
independent, \(x\notin E\cup T\), and

\[
 v\text{ is nonadjacent in }G\text{ to every member of }E-\{v\}.
\tag{4.1}
\]

If \(x\notin E\), \(vx\in E(G)\), and

\[
 E-v+x\in\mathcal F,
\tag{4.2}
\]

then

\[
 T-v+x\in\mathcal F.
\tag{4.3}
\]

#### Proof

Put

\[
 A=(E\cap T)-\{v\},\quad O=E-T,\quad B=T-E.
\]

Then \(|O|=|B|\).  Start from \(E-v+x\) and attack the members of \(B\)
in any order.  At each step, the already restored members of \(T-\{v\}\)
cannot answer the next attack because \(T\) is independent.

The guard at \(x\) also cannot answer.  Such a successor would be contained
in \((E\cup T)-\{v\}\), every member of which is nonadjacent to \(v\) by
(4.1) and independence of \(T\).  It would therefore fail to dominate
\(v\).  Consequently, each attack removes one guard from \(O\).  After all
members of \(B\) are restored, the retained state is exactly
\(T-v+x\). \(\square\)

### Corollary 4.2 (distance-two exclusion)

Suppose \(v\) lies in an independent \(k\)-state \(T\) avoiding \(x\),
\(T-v+x\notin\mathcal F\), \(av,bv\in E(H)\), and \(a,b,x\) are distinct
from \(v\).  Then

\[
 \{a,b,x\}\notin\mathcal F.
\tag{4.4}
\]

Indeed, if \(\{a,b,x\}\) were retained, attack \(v\).  Neither \(a\) nor
\(b\) can move, so closure forces \(x\to v\), producing
\(\{a,b,v\}\in\mathcal F\).  Now \(v\) satisfies (4.1), and Lemma 4.1
would propagate the retained successor back to \(T\), contradicting the
assumed inactivity of \(v\) at \(x\).  In the equality-critical target
setup, this applies to every named rim vertex in \(R_x\).

For an inactive rim path, every edge state

\[
 \{r_i,r_{i+1},x\}
\tag{4.5}
\]

is retained: attack \(x\) from the named witness state, where both rim
responses are absent.  Corollary 4.2 simultaneously forbids

\[
 \{r_i,r_{i+2},x\}.
\tag{4.6}
\]

Thus the family already assigns the correct first two alternating parities
along every inactive path.  The unresolved human step is to propagate this
alternation through arbitrary path length without replacing a missing
family response by a graph nonedge.

## 5. Exact parity boundary and the remaining target

The local theorem is genuinely parity-sensitive.  For every even
\(m\ge4\), take \(H\) to consist of:

- an induced rim \(C_m=r_0\ldots r_{m-1}r_0\);
- distinct vertices \(p_i\), each adjacent in \(H\) exactly to
  \(r_i,r_{i+1}\); and
- an isolated target \(x\).

In \(G=\overline H\), the three sets

\[
 \{r_i:i\text{ even}\},\qquad
 \{r_i:i\text{ odd}\},\qquad
 \{p_0,\ldots,p_{m-1},x\}
\tag{5.1}
\]

are cliques.  The product family with one guard in each clique is eternal.
Every named witness state belongs to it, and an attack at \(x\) from that
state can be answered only by the witness guard while remaining in the
product family.  Hence the even analogue of (1.1)--(1.4) exists for every
even length.

Discovery calculations support a stronger path-parity statement:

> **Open path-parity target.**  Along every inactive witnessed path,
> \(\{r_0,r_j,x\}\in\mathcal F\) exactly when \(j\) is odd.

The certified \(C_7\) theorem is consistent with this target.  One
all-distinct-witness \(C_9\) formula also returned UNSAT, but the other
21,146 witness partitions were not covered and no proof package was made.
That run is OBSERVED only and is not a \(C_9\) theorem.

The next proof task is therefore a length-independent attack induction for
the path-parity target.  If that induction succeeds, every inactive odd
cycle is excluded at once, closing the full-target \(k=3\) coloring branch.
