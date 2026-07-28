# Global critical witnesses in the shortest three-gate obstruction

## Status and scope

Date: 2026-07-28 (PDT)

All statements use the standard one-guard-moves model: attacks are made
only at unoccupied vertices, exactly one adjacent guard moves, and every
retained successor remains in the eternal family.

This note makes one new local advance on the no-full \(k=3\) branch.

1. **PROVED CANDIDATE, pending hostile review:** in the complete shortest
   three-gate geometry, a common complement neighbor of a critical
   cross-gate pair cannot be physical to the missing anchor.  Thus the
   witnesses supplied by \(\gamma(G)=3\) at all three critical pairs are
   forced into the dynamic branch.
2. **PROVED CANDIDATE from accepted C-079/C-082 and \(\gamma=3\),
   pending hostile review:** every such dynamic witness forces a sealed
   positive cap.  Three sealed caps, one for each anchor color, are
   incompatible in the unit-free no-full exact-two-list branch, including
   every possible collision among the caps.
3. **EXACT GAMMA-TWO CONTROL:** a 21-vertex graph realizes all three
   complete gates and all three dynamic critical witnesses simultaneously.
   It has
   \[
      (\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,3).
   \]
   A standalone verifier checks its 843-state eternal family and all
   15,174 attack obligations.  Hence neither the three local witnesses
   nor eternal closure alone finishes the proof; the global
   no-dominating-pair condition must be used again.

This does **not** prove the complete \(k=3\) case and does not resolve the
gamma--theta conjecture.  No literature-priority claim is made.

## 1. Local notation

Let \(\mathcal F\) be an eternal family of triples, let

\[
   S=\{a,b,c\}\in\mathcal F
\]

be independent, and put \(H=\overline G\).  For an outside vertex \(w\),
write

\[
   L(w)=\{h\in S:S-h+w\in\mathcal F\}.
\tag{1.1}
\]

We isolate the two adjacent full gates used by the proof.  Their displayed
vertices are:

\[
\begin{array}{c|l}
\text{symbol}&\text{role}\\ \hline
x&\text{type-\(c\) terminal}\\
u,v&\text{two physical type-\(a\) connector terminals}\\
y&\text{type-\(b\) terminal}\\
s&\text{type-\(b\) cap joining \(x,u\)}\\
t&\text{type-\(c\) cap joining \(v,y\)}\\
o,m&\text{type-\(b\) original port and physicalization midpoint.}
\end{array}
\tag{1.2}
\]

All displayed vertices are distinct.  Assume the response data

\[
\begin{aligned}
  &c\in L(u),\\
  &c\notin L(x)\cup L(t),\\
  &b\notin L(y)\cup L(o)\cup L(m),
\end{aligned}
\tag{1.3}
\]

and the literal complement edges

\[
\begin{aligned}
 &ab,ac,\\
 &bs,xs,us,\\
 &av,uv,vt,yt,\\
 &vo,om,my
\end{aligned}
\qquad\subseteq E(H).
\tag{1.4}
\]

These are a subset of the standard complete three-gate data.  In
particular, \(u-v\) is the length-one type-\(a\) connector, \(s\) is the
preceding cap, and \(v-o-m-y\), together with \(t\), is the next full
tight gate.

The critical cross-gate pair is \(\{x,y\}\).  A **physical critical
witness** is a vertex \(q\), distinct from
\(a,b,c,x,u,v,y,s,t,o,m\), satisfying

\[
   aq,xq,yq\in E(H).
\tag{1.5}
\]

The proof below does not use \(L(q)\).

## 2. A critical witness cannot be physical

### Theorem 2.1 (physical critical-witness exclusion) — PROVED CANDIDATE

Under (1.1)--(1.5), no eternal family \(\mathcal F\) exists.

#### Proof

We repeatedly use the following convention.  A displayed state is
**dead** if some unoccupied attack has no retained one-guard successor.
A state that misses a vertex in \(G\) is dead immediately, because an
attack at that vertex has no adjacent guard.

The response \(c\in L(u)\) gives

\[
   A_0=\{a,b,u\}\in\mathcal F.
\]

Attack \(x\).

- Replacing \(u\) gives \(\{a,b,x\}\), absent because \(c\notin L(x)\).
- Replacing \(a\) gives \(\{b,u,x\}\), which misses \(s\) by
  \(bs,us,xs\in E(H)\).

Closure therefore forces

\[
   A_1=\{a,u,x\}\in\mathcal F.
\tag{2.1}
\]

Attack \(t\) from \(A_1\).

- The state \(\{a,u,t\}\) misses \(v\), by \(av,uv,tv\in E(H)\).
- The state \(\{a,x,t\}\) is dead under an attack at \(b\): the guard at
  \(a\) cannot move because \(ab\in E(H)\), while the other two
  successors are \(\{a,b,t\}\) and \(\{a,b,x\}\), absent by (1.3).

Hence closure forces

\[
   A_2=\{u,x,t\}\in\mathcal F.
\tag{2.2}
\]

We next record a small dead-state ladder.  Any state consisting of \(c\)
and two vertices of \(\{y,o,m\}\) is dead under an attack at \(a\):
the guard at \(c\) cannot move because \(ac\in E(H)\), and the other
successors are direct swaps excluded by
\(b\notin L(y)\cup L(o)\cup L(m)\).  Consequently

\[
   \{y,o,m\}\notin\mathcal F,
\tag{2.3}
\]

because an attack at \(c\) would have only those three dead successor
shapes.

Both \(\{y,t,o\}\) and \(\{u,y,o\}\) are dead under an attack at \(m\).
The guards at \(y,o\) cannot move, by \(ym,om\in E(H)\), and the only
remaining successor shape is (2.3).  Also,

\[
   \{u,t,o\}\notin\mathcal F,
\tag{2.4}
\]

because it misses \(v\), by \(uv,tv,ov\in E(H)\).

It follows that \(\{u,y,t\}\) is dead under an attack at \(o\): its three
successor shapes are exactly

\[
   \{y,t,o\},\qquad \{u,t,o\},\qquad \{u,y,o\},
\]

all excluded above.

Now attack \(y\) from \(A_2\).  The guard at \(t\) cannot move because
\(ty\in E(H)\), and moving \(x\) gives the dead state
\(\{u,y,t\}\).  Closure therefore forces

\[
   A_3=\{x,y,t\}\in\mathcal F.
\tag{2.5}
\]

Finally attack \(a\) from \(A_3\).

- Replacing \(y\) gives \(\{a,x,t\}\), already shown dead.
- Replacing \(t\) gives \(\{a,x,y\}\), which misses \(q\) by (1.5).
- Replacing \(x\) gives \(\{a,y,t\}\).  This state is dead under an
  attack at \(o\): \(\{y,t,o\}\) is dead,
  \(\{a,t,o\}\) misses \(v\), and \(\{a,y,o\}\) is dead under an attack
  at \(c\) using \(ac\in E(H)\) and the absent direct swaps
  \(\{a,c,y\},\{a,c,o\}\).

All possible responses are absent, contradicting
\(A_3\in\mathcal F\).  Every attack used above is at an unoccupied
vertex.  If a move edge not displayed in (1.4) is missing, it only
removes a candidate response and does not affect the forcing argument.
\(\square\)

### Corollary 2.2 (all three critical witnesses are dynamic)

In the canonical shortest complete three-gate geometry of C-104, assume
the unit-free no-full branch and \(\gamma(G)=3\).  Let

\[
  P_a=\{b_0,c_1\},\qquad
  P_b=\{c_0,a_1\},\qquad
  P_c=\{a_0,b_1\}.
\]

Each pair has a common \(H\)-neighbor.  C-104 forces any nondisplayed
neighbor of \(P_a\) to have exact type \(a\), and handles every displayed
collision.  Theorem 2.1 rules out the physical alternative
\(aq_a\in E(H)\); the failed direct incidences of the two adjacent full
gates separately rule out identifying \(q_a\) with either of their
type-\(a\) endpoints.  Therefore

\[
   aq_a\in E(G),\qquad L(q_a)=\{b,c\}.
\tag{2.6}
\]

Cyclically there are witnesses \(q_b,q_c\) with

\[
\begin{array}{c|c|c}
\text{witness}&\text{dynamic anchor edge}&\text{exact list}\\ \hline
q_a&aq_a\in E(G)&\{b,c\}\\
q_b&bq_b\in E(G)&\{a,c\}\\
q_c&cq_c\in E(G)&\{a,b\}.
\end{array}
\tag{2.7}
\]

The three witnesses are distinct because their exact response lists are
different.  This is stronger than applying C-104 to only one selected
critical pair.

## 3. The global cascade and the cross-color contradiction

Fix the dynamic witness \(q_a\).  Since \(\gamma(G)=3\), the pair
\(\{a,q_a\}\) has a common \(H\)-neighbor \(r_a\).  Thus

\[
   ar_a,q_ar_a\in E(H).
\tag{3.1}
\]

The vertex \(r_a\) lies outside \(S\).  It is not \(a\), and it cannot
be \(b\) or \(c\), because \(b,c\in L(q_a)\) force
\(bq_a,cq_a\in E(G)\), contrary to (3.1).

Membership \(a\in L(r_a)\) would force \(ar_a\in E(G)\), so
\(a\notin L(r_a)\).  In the exact two-list branch,

\[
   L(r_a)=\{b,c\}.
\tag{3.2}
\]

Hence \(r_a\) is a physical type-\(a\) representative joined to the
dynamic representative \(q_a\) by one \(H[W_a]\)-edge.

Apply accepted C-082 to this edge.  It supplies an outside common
complement neighbor \(z_a\) with

\[
  q_az_a,r_az_a\in E(H),\qquad a\in L(z_a).
\tag{3.3}
\]

Thus \(\{q_a,r_a,z_a\}\) is an \(H\)-triangle and a retained maximum
independent state.  Accepted C-079 now gives the exact sealing property

\[
   N_H(z_a)\cap P_a^+=\varnothing,
   \qquad
   P_a^+=\{w\notin S:a\in L(w)\}.
\tag{3.4}
\]

Indeed, any \(p\in P_a^+\) adjacent in \(H\) to \(z_a\) would make
\[
  p-z_a-\{q_a,r_a\},\qquad q_ar_a\in E(H),
\]
the forbidden length-one C-079 fan.

Equations (3.1)--(3.4) are the required finite cascade:

\[
 \text{dynamic type-\(a\) witness}
 \longrightarrow
 \text{physical type-\(a\) mate}
 \longrightarrow
 \text{sealed \(a\)-positive cap}.
\tag{3.5}
\]

The same construction applies cyclically to \(q_b,q_c\).  The following
general lemma is the cross-color step.

### Lemma 3.1 (three sealed positives are impossible) — PROVED CANDIDATE

Assume \(\gamma(G)=3\), and assume every outside response list is a
nonempty exact two-subset of \(S=\{a,b,c\}\).  For each
\(i\in\{a,b,c\}\), put

\[
   P_i^+=\{w\notin S:i\in L(w)\}.
\]

There do not exist outside vertices \(z_a,z_b,z_c\), not necessarily
distinct, such that

\[
   i\in L(z_i),
   \qquad
   N_H(z_i)\cap P_i^+=\varnothing
   \quad(i=a,b,c).
\tag{3.6}
\]

#### Proof

First suppose \(z_i\ne z_j\), where
\(\{i,j,k\}=\{a,b,c\}\).  Since \(\gamma(G)=3\), the pair
\(\{z_i,z_j\}\) has a common \(H\)-neighbor \(w\).

If \(w\notin S\), then \(wz_i\in E(H)\) and the sealing condition at
\(z_i\) imply \(i\notin L(w)\).  Similarly \(j\notin L(w)\).
This is impossible because \(L(w)\) is an exact two-subset of a
three-element set.

Thus \(w\in S\).  The anchor \(i\) cannot be \(w\), because
\(i\in L(z_i)\) forces \(iz_i\in E(G)\).  Likewise \(w\ne j\).
Consequently \(w=k\).  The edges

\[
   kz_i,kz_j\in E(H)
\]

imply \(k\notin L(z_i)\cup L(z_j)\), since membership in either response
list would force the corresponding graph edge.  Exact two-list size now
gives

\[
   L(z_i)=L(z_j)=\{i,j\}.
\tag{3.7}
\]

If \(z_a,z_b,z_c\) are pairwise distinct, apply (3.7) first to
\((i,j)=(a,b)\) and then to \((i,j)=(b,c)\).  It gives simultaneously

\[
   L(z_b)=\{a,b\},
   \qquad
   L(z_b)=\{b,c\},
\]

a contradiction.

It remains to audit collisions.  All three vertices cannot coincide,
because their common response list would contain \(a,b,c\), contrary to
exact size two.  Suppose exactly two coincide, say

\[
   z_i=z_j=:z,\qquad z\ne z_k.
\]

Then \(L(z)\) contains \(i,j\), so \(L(z)=\{i,j\}\).  Apply
\(\gamma(G)=3\) to the distinct pair \(\{z,z_k\}\), and let \(w\) be a
common \(H\)-neighbor.  If \(w\notin S\), the two sealing conditions at
the single collided vertex \(z\) force

\[
   i,j\notin L(w),
\]

again impossible for an exact two-list.  If \(w\in S\), anchors \(i,j\)
are blocked by the graph edges forced from \(i,j\in L(z)\), while anchor
\(k\) is blocked by the graph edge forced from \(k\in L(z_k)\).  No
anchor can be \(w\), another contradiction.  This exhausts all collision
patterns. \(\square\)

Closure from \(S\) makes every outside list nonempty.  The unit-free
hypothesis excludes singleton lists, and the no-full hypothesis excludes
three-element lists; hence every outside list has exact size two.  The
proof makes no inference from a missing response to a graph nonedge.

### Theorem 3.2 (canonical complete three-gate exclusion) — PROVED CANDIDATE

In the unit-free no-full exact-two-list branch with \(\gamma(G)=3\), the
canonical shortest complete three-gate odd boundary does not occur.

#### Proof

Corollary 2.2 supplies the three distinct dynamic critical witnesses
\(q_a,q_b,q_c\).  For each \(i\), apply the construction
(3.1)--(3.4) to obtain \(z_i\).  These vertices satisfy (3.6), contradicting
Lemma 3.1. \(\square\)

This theorem excludes the complete three-gate, length-\((1,1,1)\)
canonical geometry.  It does not contract arbitrary subdivisions, exclude
four or more gates, handle a unit or full response list, or prove the
complete \(k=3\) case.

## 4. Exact control and bounded discovery sweeps

The graph

```text
TBn]r]vj]lnZ~^~n~z~^z|~nz~^j~~t~~n^~
```

has order \(21\), size \(174\), and

\[
   (\gamma,i,\alpha,\gamma^\infty,\theta)=(2,2,3,3,3).
\tag{4.1}
\]

It contains all three complete length-\((1,1,1)\) tight gates and three
distinct dynamic critical witnesses of the three forced types.  The
checked eternal family has 843 states; the greatest eternal triple kernel
has 1,237 states.  All 15,174 unoccupied-attack obligations pass.  The
graph has 114 dominating pairs, so it is a sharp control for the need to
use \(\gamma(G)=3\) beyond the three critical pairs.

Two exhaustive pattern probes clarify the role of the full gate data.

\[
\begin{array}{c|c|c}
\text{encoded geometry}&\text{physical/dynamic masks tested}&
  \text{SAT masks}\\ \hline
\text{dead boundaries only, order 15}&8&8\\
\text{three complete gates, order 21}&8&
  \text{all-dynamic only}.
\end{array}
\tag{4.2}
\]

The second UNSAT row is explained by Theorem 2.1, not promoted from the
solver output.  The first row is a bounded control showing that the
original-clause and physicalization data are essential to the theorem.

As additional **OBSERVED** evidence only, the globally constrained
all-two-list formula was UNSAT for the boundary geometry at orders
12 through 18 and for the complete-gate geometry at orders 21 through
23.  These runs have no arbitrary-order coverage theorem and are not
finite exclusion claims.

## 5. Reproduction

From the campaign directory:

```text
python3 -I -B -W error \
  math/working/global_witness_cascade/verify_dynamic_control.py \
  --check math/working/global_witness_cascade/dynamic_three_witness_control.json \
  --output /tmp/dynamic-three-witness-check.json
```

The standalone verifier imports no search or campaign evaluator.  It
checks the graph6 record, all graph parameters in (4.1), the response
lists, the three complete gates, all three dynamic witnesses, every attack
obligation, and the greatest triple-kernel size.

The two pattern tables can be regenerated with:

```text
python3 -I -B -W error \
  math/working/global_witness_cascade/critical_pattern_sweep.py \
  --solver tools/cadical_3_0_1/build/cadical \
  --output /tmp/boundary-patterns.json

python3 -I -B -W error \
  math/working/global_witness_cascade/critical_pattern_sweep.py \
  --full-gates \
  --solver tools/cadical_3_0_1/build/cadical \
  --output /tmp/full-patterns.json
```

Theorem 2.1, Lemma 3.1, and Theorem 3.2 are the mathematical candidates
awaiting hostile review.  The pattern sweeps are proof-discovery and
sharpness controls.
