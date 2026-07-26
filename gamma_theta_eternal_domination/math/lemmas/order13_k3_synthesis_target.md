# Exact coverage and CNF semantics for the order-13, parameter-three target

## Status and claim boundary

The mathematical statements in this note are **proved relative to the
accepted campaign inputs listed below**.  In particular, the note proves an
exact four-branch cover and a graph-to-CNF/CNF-to-graph equivalence for the
proposed order-13, parameter-three formulas.

This note does not by itself assert that any order-13 formula has been
generated correctly or is satisfiable or unsatisfiable.  Exact source bytes,
generated CNF bytes, proof certificates, and independent replay are separate
implementation and certificate obligations.  A separately frozen A/B audit
now accepts deterministic constructor bytes for all four templates; the
abstract equivalence here is independent of that implementation.  The
companion direct proof in `order13_k3_hole11_exclusion.md` has passed
independent hostile review in `reviews/order13_k3_math_hostile/`.

Every dynamic statement uses the standard one-guard-moves model.  Attacks
occur only at unoccupied vertices.  A response removes exactly one guard,
moves it along one edge of \(G\) to the attacked vertex, and leaves a
dominating configuration in the same family.

The accepted inputs are:

1. the parameter chain
   \[
   \gamma(G)\leq i(G)\leq\alpha(G)\leq
   \gamma^\infty(G)\leq\theta(G);
   \]
2. additivity over components and the connected-counterexample reduction;
3. C-050: relative to the published through-order-11 result used there,
   there is no counterexample of order at most \(12\);
4. the Strong Perfect Graph Theorem;
5. C-014: if \(\gamma^\infty(G)=3\), then
   \(\overline G\) contains no induced odd wheel;
6. C-017: when
   \(\alpha(G)=\gamma^\infty(G)=3\), an imperfect
   \(\overline G\) contains an induced odd hole; equivalently, the possible
   induced \(\overline{C_7}\) obstruction is excluded in the one-guard
   model; and
7. the accepted maximum-independent-state lemma: every independent
   \(k\)-set belongs to every eternal family of \(k\)-sets.

C-052 already records the resulting order-13 parameter range and the
four-template conclusion.  Sections 1--3 below reconstruct its
parameter-three coverage argument explicitly so that the CNF realization
does not use C-052 as an unexplained black box.

## 1. The exact target and complement dictionary

Let \(G\) be an order-13, parameter-three counterexample:

\[
 |V(G)|=13,\qquad
 \gamma(G)=\gamma^\infty(G)=3<\theta(G).
\tag{1.1}
\]

The parameter chain collapses between its equal endpoints:

\[
 \gamma(G)=i(G)=\alpha(G)=\gamma^\infty(G)=3.
\tag{1.2}
\]

Put \(H=\overline G\).  Then

\[
 \omega(H)=\alpha(G)=3,\qquad
 \chi(H)=\theta(G)>3.
\tag{1.3}
\]

In particular, (1.2), not well-coveredness by itself, supplies the essential
equality \(\gamma(G)=\alpha(G)=3\).  Equality \(i(G)=\alpha(G)\) does imply
that \(G\) is well-covered, but well-coveredness is only a consequence here,
not a substitute for the equalities in (1.2).

### Lemma 1 (pair/common-neighbor dictionary)

No two-set dominates \(G\) if and only if every pair of vertices in \(H\)
has an external common \(H\)-neighbor.

#### Proof

Fix distinct vertices \(a,b\).  The pair \(\{a,b\}\) fails to dominate
\(G\) exactly when there is a vertex
\(x\notin\{a,b\}\) adjacent in \(G\) to neither \(a\) nor \(b\).  This is
equivalent to

\[
 ax,bx\in E(H).
\]

The witness is external automatically: the two occupied vertices dominate
themselves under closed-neighborhood domination.  Applying the equivalence
to every pair proves the statement. \(\square\)

Since \(\gamma(G)=3\), Lemma 1 applies to the target.

### Lemma 2 (connectedness at order 13)

Relative to C-050, every graph satisfying (1.1) is connected.

#### Proof

Suppose \(G\) has components \(G_1,\ldots,G_s\), where \(s>1\).  Additivity
gives

\[
\gamma(G)=\sum_j\gamma(G_j),\qquad
\gamma^\infty(G)=\sum_j\gamma^\infty(G_j),\qquad
\theta(G)=\sum_j\theta(G_j).
\]

For every component,
\(\gamma(G_j)\leq\gamma^\infty(G_j)\).  Equality of the first two sums
therefore forces
\(\gamma(G_j)=\gamma^\infty(G_j)\) for every \(j\).  The strict inequality
\(\theta(G)>\gamma(G)\) forces
\(\theta(G_j)>\gamma(G_j)\) for at least one \(j\).  That component is a
counterexample of order at most \(12\), contrary to C-050. \(\square\)

The formula below nevertheless encodes connectedness directly.  This makes a
satisfying assignment decode to a connected target without asking the
checker to import C-050.

## 2. Exhaustive odd-hole cover

### Theorem 3 (four overlapping templates)

If \(G\) satisfies (1.1), then \(H=\overline G\) contains a hub-free induced
cycle

\[
 C_\ell\quad\text{for some}\quad
 \ell\in L:=\{5,7,9,11\}.
\tag{2.1}
\]

Here hub-free means that no vertex outside the selected cycle is adjacent in
\(H\) to every vertex of the cycle.

#### Proof

By (1.3), \(H\) is imperfect.  The Strong Perfect Graph Theorem supplies an
induced odd hole or odd antihole.  An odd antihole on \(2q+1\) vertices has
clique number \(q\).  Since \(\omega(H)=3\), only \(q=2,3\) are possible.
The five-vertex odd antihole is \(C_5\), already an odd hole.  The remaining
case is an induced \(\overline{C_7}\), excluded by C-017 because
\(\alpha(G)=\gamma^\infty(G)=3\).  Thus \(H\) contains an induced odd hole.

By C-014 that hole is hub-free: a vertex complete to its rim would form an
induced odd wheel.

It remains to bound its length.  Let \(C\) be the selected odd hole.  By
Lemma 1, the endpoints of every rim edge have a common \(H\)-neighbor.  No
rim vertex is adjacent to both endpoints of a rim edge in an induced cycle
of length at least five, so every such common neighbor lies outside \(C\).
There is therefore at least one outside vertex.  If there were exactly one,
that vertex would have to be adjacent to both endpoints of every rim edge,
and hence to every rim vertex.  It would be a hub, a contradiction.  Thus at
least two vertices lie outside \(C\), and

\[
 |C|\leq 13-2=11.
\]

The possible odd-hole lengths at least five are exactly those in (2.1).
\(\square\)

The four cases form an **exhaustive union, not a partition**.  The same graph
may contain induced holes of several listed lengths, several holes of the
same length, or several admissible choices of a distinguished rim edge and
common neighbor.  No disjointness is needed: excluding every branch would
exclude their union.

The companion near-spanning-hole theorem proves that an equality graph with
common parameter three cannot have only two vertices outside an induced odd
hole.  Once that theorem is accepted, the \(C_{11}\) member of this
four-template cover is empty and the live union reduces to \(C_5,C_7,C_9\).
The four-template statement remains the exact accepted C-052 cover and is
recorded here because it is the starting point of the audit.

## 3. Sound template relabeling and the fixed independent triple

Fix \(\ell\in L\) and a hub-free induced \(C_\ell\) in \(H\).  Choose either
orientation and any starting rim edge, and label the rim cyclically

\[
 R_\ell=\{0,1,\ldots,\ell-1\},
\]

with \(01\) the chosen rim edge.  Thus the only \(H\)-edges internal to
\(R_\ell\) are

\[
 j(j+1)\quad(0\leq j<\ell),
\]

where indices are read modulo \(\ell\).

Lemma 1 gives a common \(H\)-neighbor of \(0\) and \(1\).  No rim vertex can
be that common neighbor, so choose one outside the rim and label it

\[
 z=\ell.
\]

Label the remaining \(12-\ell\) vertices arbitrarily.  We then have

\[
 01,0z,1z\in E(H).
\tag{3.1}
\]

Consequently,

\[
 A_\ell=\{0,1,z\}
\tag{3.2}
\]

is a triangle of \(H\), equivalently an independent triple of \(G\).  By
\(\alpha(G)=3\), it is maximum.  It is also maximal and hence dominates
\(G\).

This is the only fixed independent triple used by the proposed template
formula.  It is not an unrelated anchor imposed in addition to the fixed
hole.  Simultaneously fixing a selected hole on one set of labels and an
arbitrary maximum independent set on unrelated labels would require an
incidence theorem that is not available and would be unsound.  The triangle
in (3.2) is safe precisely because the pair/common-neighbor condition
constructs it from the chosen rim edge.

For completeness, the maximum-independent-state argument is short.  Let
\(\mathcal D\) be any eternal family of triples and let \(A\) be any
independent triple.  Starting from a member of \(\mathcal D\), repeatedly
attack an unoccupied vertex of \(A\).  A guard already on \(A\) cannot
respond, because \(A\) is independent.  Each response therefore increases
the number of guards on \(A\) by one.  Closure keeps every successor in
\(\mathcal D\), and after finitely many attacks the state is exactly \(A\).
Hence every independent triple, including \(A_\ell\), belongs to every
eternal family of triples.

Hub-freeness of the selected hole becomes

\[
 \text{for every }x\notin R_\ell,\quad
 \bigvee_{v\in R_\ell} xv\notin E(H).
\tag{3.3}
\]

Equations (3.1)--(3.3), the induced-cycle adjacencies, and arbitrary labels
on the remaining vertices are the complete template relabeling.  No
automorphism of \(G\) is assumed.

## 4. The abstract order-13 CNF

This section defines the formula whose implementation is to be checked.  It
does not bind any current source file or generated byte string.

Fix \(\ell\in L\), let \(V=\{0,\ldots,12\}\), and put \(z=\ell\).  Let
\(F^{13}_\ell\) have the following variables.

1. For every unordered pair \(u<v\), an edge variable \(e_{uv}\), true
   exactly when \(uv\in E(H)\).
2. For every unordered pair \(a<b\) and every
   \(x\in V-\{a,b\}\), a witness variable \(w_{ab,x}\).  A true witness
   certifies that \(x\) is a common \(H\)-neighbor of \(a,b\).
3. For every triple \(D\in\binom V3\), a family variable \(f_D\).  It is
   true exactly when \(D\) is selected as a state of the eternal family.
4. For every \(D\in\binom V3\), every unoccupied attack
   \(r\in V-D\), and every guard \(u\in D\), a response variable
   \(m_{D,r,u}\).  A true response variable denotes the one-guard move from
   \(u\) to \(r\).

There are exactly

\[
\binom{13}{2}=78
\]

edge variables,

\[
\binom{13}{2}\cdot11=858
\]

witness variables,

\[
\binom{13}{3}=286
\]

family variables, and

\[
\binom{13}{3}\cdot10\cdot3=8{,}580
\]

move variables, for \(9{,}802\) variables in total.

Write \(e_{uv}=e_{vu}\) when displaying clauses.  The base formula consists
of the following clauses.

### 4.1 Clique number and pair witnesses

For every four-set \(Q\subseteq V\), include

\[
 \bigvee_{\{u,v\}\in\binom Q2}\neg e_{uv}.
\tag{4.1}
\]

These clauses say \(\omega(H)\leq3\).

For every pair \(a<b\), include

\[
 \bigvee_{x\in V-\{a,b\}} w_{ab,x},
\tag{4.2}
\]

and, for every eligible \(x\), include

\[
 \neg w_{ab,x}\vee e_{ax},
 \qquad
 \neg w_{ab,x}\vee e_{bx}.
\tag{4.3}
\]

The witness variables are implications, not biconditionals.  Clauses
(4.2)--(4.3) nevertheless assert exactly the needed existential fact: every
pair has at least one external common \(H\)-neighbor.

### 4.2 The labeled hub-free hole

For each pair \(u<v\) in \(R_\ell\), include the unit \(e_{uv}\) if \(u,v\)
are consecutive on the cyclic rim, and include \(\neg e_{uv}\) otherwise.
For every \(x\in V-R_\ell\), include

\[
 \bigvee_{v\in R_\ell}\neg e_{xv}.
\tag{4.4}
\]

Finally include the two units

\[
 e_{0z},\qquad e_{1z}.
\tag{4.5}
\]

These clauses assert exactly an induced \(C_\ell\), no external hub for that
selected hole, and the distinguished common neighbor in Section 3.

### 4.3 Connectedness of \(G\)

For every nonempty proper \(S\subset V\) with \(0\in S\), include

\[
 \bigvee_{\substack{u\in S\\v\in V-S}}\neg e_{uv}.
\tag{4.6}
\]

Each negative \(H\)-edge literal is a positive \(G\)-edge.  Thus (4.6) says
that every proper cut has a crossing edge in \(G\), exactly characterizing
connectedness of \(G\), not connectedness of \(H\).

### 4.4 Dominating family and one-guard responses

For every triple \(D\) and every \(x\notin D\), include

\[
 \neg f_D\ \vee\ \bigvee_{u\in D}\neg e_{xu}.
\tag{4.7}
\]

If \(D\) is selected, some \(u\in D\) is adjacent to \(x\) in \(G\), so
\(D\) dominates \(G\).  No clause is needed for \(x\in D\), because
domination uses closed neighborhoods.

Include the nonempty-family clause

\[
 \bigvee_{D\in\binom V3} f_D.
\tag{4.8}
\]

For every \(D\), every \(r\notin D\), and every \(u\in D\), let

\[
 D-u+r=(D-\{u\})\cup\{r\}.
\]

Include

\[
 \neg f_D\ \vee\ \bigvee_{u\in D}m_{D,r,u},
\tag{4.9}
\]

\[
 \neg m_{D,r,u}\vee\neg e_{ur},
\tag{4.10}
\]

and

\[
 \neg m_{D,r,u}\vee f_{D-u+r}.
\tag{4.11}
\]

The index restriction \(r\notin D\) is the unoccupied-attack rule.
Equation (4.10) says \(ur\in E(G)\).  The successor in (4.11) removes one
guard and inserts the attacked vertex; because \(r\notin D\), it is again a
three-set.  Equation (4.7), applied to the selected successor, ensures that
the resulting configuration dominates.

No at-most-one clause on the three response variables is needed.  Several
true response variables represent several alternative legal one-guard
responses, not a simultaneous motion of several guards.  To decode a
strategy, choose any one true response variable promised by (4.9).

For every triple \(D=\{a,b,c\}\), also include the redundant strengthening

\[
 \neg e_{ab}\vee\neg e_{ac}\vee\neg e_{bc}\vee f_D.
\tag{4.12}
\]

This says every triangle of \(H\), equivalently every independent triple of
\(G\), is selected.  Section 3's maximum-independent-state argument proves
that (4.12) is sound for every target graph and every eternal family of
triples.  It is not being assumed as a converse characterization of eternal
domination.

### 4.5 Complete complement-coloring bank

A coloring row is a map

\[
 c:V\longrightarrow\{0,1,2\}.
\]

It is *first-use canonical* when its color names are \(0,1,2\) in order of
first occurrence.  Let \(B_\ell\) contain exactly the first-use canonical
rows proper on all forced-positive template edges: the rim edges and
\(01,0z,1z\), with \(01\) already a rim edge.  Forced-negative template
edges impose no condition on a coloring row.

For each \(c\in B_\ell\), append

\[
 C_c=
 \bigvee_{\substack{u<v\\c(u)=c(v)}}e_{uv}.
\tag{4.13}
\]

For a fixed row \(c\), clause \(C_c\) is false exactly when every color
class is independent in \(H\), that is, exactly when \(c\) is a proper
three-coloring of \(H\).

The forced triangle \(\{0,1,z\}\) uses all three colors.  The action of the
six color-name permutations is therefore free, and first-use
canonicalization chooses exactly one representative of every admissible
color partition.  Hence, for every graph extending the template,

\[
 H\models\bigwedge_{c\in B_\ell} C_c
 \quad\Longleftrightarrow\quad
 \chi(H)>3.
\tag{4.14}
\]

This canonicalization is only a quotient by the names of colors.  It is not
a vertex-symmetry assumption about \(H\).

The chromatic polynomial of an odd cycle gives

\[
 |B_\ell|
 =\frac{(2^\ell-2)3^{12-\ell}}{3!}.
\tag{4.15}
\]

Thus the exact expected bank sizes are:

| branch | \(|B_\ell|\) |
|---|---:|
| `hole5` | 10,935 |
| `hole7` | 5,103 |
| `hole9` | 2,295 |
| `hole11` | 1,023 |

### 4.6 Combinatorial clause census

The clause categories above give the following counts before the coloring
bank:

| category | clauses |
|---|---:|
| no \(K_4\), (4.1) | 715 |
| pair witnesses, (4.2)--(4.3) | 1,794 |
| template, (4.4)--(4.5) and rim units | \(\binom{\ell}{2}+15-\ell\) |
| connected cuts, (4.6) | 4,095 |
| selected-state domination, (4.7) | 2,860 |
| family nonempty, (4.8) | 1 |
| response existence, (4.9) | 2,860 |
| move implications, (4.10)--(4.11) | 17,160 |
| triangle-to-family, (4.12) | 286 |

Consequently:

| branch | base clauses | bank clauses | full clauses |
|---|---:|---:|---:|
| `hole5` | 29,791 | 10,935 | 40,726 |
| `hole7` | 29,800 | 5,103 | 34,903 |
| `hole9` | 29,813 | 2,295 | 32,108 |
| `hole11` | 29,830 | 1,023 | 30,853 |

These are mathematical counts for the clause scheme, not an implementation
binding.  A production constructor must reproduce them and must still be
checked at the clause-multiset and byte levels.

## 5. Exact semantic equivalence

### Theorem 4 (one template is encoded exactly)

For each \(\ell\in L\), the abstract formula \(F^{13}_\ell\) is satisfiable
if and only if there is a labeled graph \(G\) on \(V=\{0,\ldots,12\}\) such
that:

1. \(G\) is connected;
2. \(\gamma(G)=\alpha(G)=\gamma^\infty(G)=3<\theta(G)\);
3. \(H=\overline G\) has the hub-free induced \(C_\ell\) on
   \(0,\ldots,\ell-1\); and
4. vertex \(z=\ell\) is a common \(H\)-neighbor of rim-edge endpoints
   \(0,1\).

The equality \(i(G)=3\) and well-coveredness then follow from the accepted
parameter chain.

#### Proof: graph and strategy imply a satisfying assignment

Assume a labeled graph with properties 1--4.  Set

\[
 e_{uv}=1\quad\Longleftrightarrow\quad uv\in E(H).
\]

Because \(\gamma(G)=3\), Lemma 1 supplies an external common
\(H\)-neighbor for every pair.  Choose one for each pair, set its witness
variable true, and set the unused witness variables false.  Clauses
(4.2)--(4.3) hold.  Since
\(\alpha(G)=\omega(H)=3\), the no-\(K_4\) clauses hold.  Properties 3--4
give all template clauses, and connectedness gives every cut clause (4.6).

Choose an eternal family \(\mathcal D\) of triples witnessing
\(\gamma^\infty(G)=3\), and set

\[
 f_D=1\quad\Longleftrightarrow\quad D\in\mathcal D.
\]

Every selected state dominates, so (4.7) holds, and the family is nonempty,
so (4.8) holds.  For every \(D\in\mathcal D\) and every unoccupied
\(r\notin D\), choose one guard \(u(D,r)\) supplied by eternal closure.  Set
that response variable true and set the other response variables for
\((D,r)\) false.  Set all response variables from unselected source states
false.  The chosen move traverses a \(G\)-edge and its successor belongs to
\(\mathcal D\), proving (4.9)--(4.11).

Every \(H\)-triangle is an independent triple of \(G\).  Since
\(\alpha(G)=3\), the maximum-independent-state argument in Section 3 puts
it in \(\mathcal D\), proving (4.12).

Finally,
\(\theta(G)=\chi(H)>3\).  By (4.14), every complete-bank clause holds.
Thus all variables have been assigned and \(F^{13}_\ell\) is satisfied.

#### Proof: a satisfying assignment implies a graph and strategy

Conversely, let an assignment satisfy \(F^{13}_\ell\).  Define \(H\) from
the true edge variables and let \(G=\overline H\).

The no-\(K_4\) clauses give \(\omega(H)\leq3\), while the forced triangle
\(\{0,1,z\}\) gives \(\omega(H)\geq3\).  Therefore

\[
 \alpha(G)=\omega(H)=3.
\tag{5.1}
\]

Clauses (4.2)--(4.3) give every pair an external common \(H\)-neighbor.
Lemma 1 says that no pair dominates \(G\), so

\[
 \gamma(G)\geq3.
\tag{5.2}
\]

Let

\[
 \mathcal D=\{D:f_D=1\}.
\]

It is nonempty by (4.8), and (4.7) says every member dominates \(G\).  For
each \(D\in\mathcal D\) and each \(r\notin D\), choose one true response
variable from (4.9).  Clauses (4.10)--(4.11) say that its guard moves along
one \(G\)-edge and that the resulting triple belongs to \(\mathcal D\).
Thus \(\mathcal D\) is an eternal dominating family of triples in exactly
the one-guard, unoccupied-attack model.  Hence

\[
 \gamma(G)\leq\gamma^\infty(G)\leq3.
\tag{5.3}
\]

Together, (5.2)--(5.3) give

\[
 \gamma(G)=\gamma^\infty(G)=3.
\tag{5.4}
\]

Equation (5.1) supplies the required equality with \(\alpha(G)\); it is not
being inferred from well-coveredness.

The complete bank and (4.14) give

\[
 \theta(G)=\chi(H)>3.
\tag{5.5}
\]

The cut clauses make \(G\) connected, and the template units and hub clauses
give properties 3--4.  This proves every claimed property of the decoded
graph. \(\square\)

## 6. Global order-13, parameter-three coverage

### Theorem 5 (every target satisfies at least one branch)

Relative to C-050, every order-13 counterexample with common parameter three
can be relabeled to give a satisfying assignment of

\[
 F^{13}_5,\quad F^{13}_7,\quad F^{13}_9,
 \quad\text{or}\quad F^{13}_{11}.
\tag{6.1}
\]

#### Proof

Lemma 2 makes the target connected.  Theorem 3 supplies a hub-free induced
\(C_\ell\) for some \(\ell\in L\).  Relabel the chosen cycle, rim edge,
external common neighbor, and remaining vertices exactly as in Section 3.
The relabeled graph satisfies the four semantic properties in Theorem 4, so
Theorem 4 constructs a satisfying assignment of \(F^{13}_\ell\). \(\square\)

Therefore independently checked UNSAT certificates for all four exact
formulas would prove that no order-13, parameter-three counterexample exists.
Because the branches overlap, no inclusion--exclusion calculation and no
unique-template assignment is required.

The direct theorem in `order13_k3_hole11_exclusion.md` proves more strongly
that \(F^{13}_{11}\) has no graph-semantic model, without invoking a SAT
run.  Combining it with Theorem 5 leaves only

\[
 F^{13}_5,\qquad F^{13}_7,\qquad F^{13}_9
\]

as live computational branches.

## 7. Symmetry audit

The abstract formulas above use only two kinds of safe normalization.

1. **Template relabeling.**  A chosen hole is oriented and labeled, one rim
   edge is named \(01\), one of its guaranteed external common neighbors is
   named \(z=\ell\), and all remaining labels are arbitrary.  This is an
   existence-preserving relabeling of the whole graph and every auxiliary
   variable.
2. **Color-name canonicalization.**  The coloring bank retains one
   first-use representative per permutation of the three color names.
   This acts on color rows only and loses no coloring partition.

The proposed formulas contain **no** free-vertex signature sorting, residual
rim-reflection condition, DoubleLex condition, or separately anchored
independent triple.  None of those constraints is covered by Theorems 4--5.
If a production formula adds one, it requires a separate full-variable
covariance/equisatisfiability proof for that exact order-13 formula,
including its complete coloring bank.  A heuristic breaker may instead be
used to find candidates, but it cannot support a certified negative result.

## 8. Hostile model checklist

The following dictionary is mandatory when reviewing an implementation.

| Mathematical requirement | Exact CNF mechanism |
|---|---|
| \(H=\overline G\), not \(G\) | \(e_{uv}=1\) means an \(H\)-edge; every \(G\)-edge is \(\neg e_{uv}\) |
| \(\alpha(G)=3\) | no \(K_4\) in \(H\), plus forced \(H\)-triangle \(\{0,1,z\}\) |
| \(\gamma(G)\geq3\) | every \(H\)-pair has an external common neighbor, so no two-set dominates \(G\) |
| \(\gamma(G)\leq3\) | the nonempty selected family contains a dominating triple |
| unoccupied attacks only | response clauses exist only for \(r\notin D\) |
| exactly one guard moves | each response successor is \(D-u+r\) for one \(u\in D\) |
| move along a \(G\)-edge | \(m_{D,r,u}\Rightarrow\neg e_{ur}\) |
| resulting state remains legal | \(m_{D,r,u}\Rightarrow f_{D-u+r}\), and every selected state satisfies the domination clauses |
| one-guard eternal closure | \(\forall D\) selected, \(\forall r\notin D\), at least one response variable is true |
| connectedness of \(G\) | every proper cut has a crossing negative \(H\)-edge |
| \(\theta(G)>3\) | the complete bank forbids every three-coloring of \(H\), since \(\theta(G)=\chi(H)\) |
| \(\gamma=\alpha\), not merely well-coveredness | independently derived as \(\gamma=3\) and \(\alpha=3\) |
| fixed independent triple | only \(\{0,1,z\}\), derived from the chosen rim edge and its guaranteed common neighbor |
| hub-free selected hole | every external vertex has at least one missing \(H\)-edge to the rim |

In particular, allowing several true \(m_{D,r,u}\) variables does not encode
an all-guards move.  They are alternative existential witnesses; a decoded
response chooses one of them.

## 9. Remaining gaps and circularity audit

1. **Implementation is separately bound.**  A deterministic order-13
   constructor and independent clause/byte reconstruction are accepted in
   `reviews/order13_k3_constructor_acceptance/`.  This note remains the
   abstract semantic proof.  Solver execution, proof conversion, certificate
   checking, and accepted exclusions for the live branches remain separate
   obligations.
2. **No certificate-backed order-13 exclusion yet.**  Formula counts and a
   proofless exploratory UNSAT response are not certificates.  The
   `hole11` branch is removed by a separate human proof, not by that solver
   response; the remaining three branches have no accepted exclusion.
3. **Only the \(k=3\) slice is covered.**  C-052 leaves
   \(k\in\{3,4,5\}\) at order 13.  Even certified exclusion of all four
   formulas in (6.1) would leave the \(k=4\) and \(k=5\) slices open and
   would not by itself raise the global counterexample lower bound to 14.
4. **C-050 is a relative input.**  The connectedness conclusion and
   “minimum order” language inherit C-050's explicit dependence on the
   published through-order-11 result.  This note does not replace that
   source audit.
5. **No circular use of the conjecture.**  The strict inequality
   \(\theta(G)>3\) is a counterexample hypothesis and is encoded independently
   by complement coloring.  It is not deduced from the conjecture.  The
   realization proof uses no SAT/UNSAT outcome.
6. **No circular use of C-052.**  C-052 records the cover, but Theorem 3
   exposes the proof path through imperfection, SPGT, C-014, C-017, and the
   pair/common-neighbor condition.  The CNF equivalence is proved separately
   in Theorem 4.
7. **Well-coveredness is not a search surrogate.**  It follows only after
   the formula has forced
   \(\gamma=\alpha=\gamma^\infty=3\).  Replacing those constraints by
   well-coveredness would enlarge the target unsafely.
8. **Extra symmetry is outside scope.**  Combining a fixed hole with an
   unrelated fixed anchor, or appending an unaudited signature, reflection,
   or DoubleLex breaker, would create an unproved coverage gap.

Subject to the accepted inputs, there is no mathematical coverage gap in the
four-template union for the order-13, parameter-three slice.  Subject also to
acceptance of the companion near-spanning-hole theorem, the live union is the
three templates \(C_5,C_7,C_9\).  The remaining obligations are
implementation equivalence, exact certificate production and replay for
those branches, and the separate \(k=4,5\) slices.
