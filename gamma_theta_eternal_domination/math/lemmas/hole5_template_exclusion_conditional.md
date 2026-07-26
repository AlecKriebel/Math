# Conditional coverage theorem for the order-12 hub-free \(C_5\) template

## Status and claim boundary

The realization and symmetry-coverage theorem below is **proved**. It says
that a connected order-12, parameter-three counterexample whose complement
contains a hub-free induced \(C_5\) must produce a satisfying assignment of
the exact retained complete-bank `hole5` formula and of its accepted
symmetry-strengthened versions.

The following separate premise is deliberately **unfilled**:

> **UNFILLED CERTIFICATE PREMISE.** The exact strengthened `hole5` CNF has
> been proved UNSAT by an accepted, independently checked certificate.

Accordingly, this note makes no `hole5` exclusion, no order-12 slice claim,
and no conjecture-resolution claim. If the premise is established later, the
final conditional corollary identifies exactly what it would imply.

All eternal domination statements use the one-guard-moves model: attacks are
only at unoccupied vertices, and exactly one guard moves along one edge to
the attacked vertex.

## 1. Exact formulas

Let \(G\) be a graph on 12 vertices and put \(H=\overline G\). A Boolean
edge variable \(e_{uv}\), \(u<v\), is true exactly when \(uv\in E(H)\).

Let \(F_5\) denote the exact retained complete-bank CNF at
`results/synthesis_k3_template_bank_packages/hole5/instance.cnf`. Its binding
is:

| quantity | value |
|---|---:|
| variables | 6,886 |
| clauses | 23,653 |
| literals | 188,959 |
| bytes | 742,899 |
| SHA-256 | `76bf36ecb663cd37272acded2208206fdba6aa571dd5f2e757cc132bd533e0b7` |

The corresponding coloring bank has 3,645 rows and SHA-256
`b3c24db61e7a33c3d8803e2bbadcdda92b950fb04445e59e7930330e92b74a00`.
The package manifest has SHA-256
`99a56197074ad3373691578527e41baff4d76eb1e86141366c4edf8bc5871402`.

The 6,886 variables have four roles:

\[
\binom{12}{2}=66\quad e\text{-variables},
\]
\[
\binom{12}{2}\cdot10=660\quad w\text{-variables},
\]
\[
\binom{12}{3}=220\quad f\text{-variables},
\]
and
\[
\binom{12}{3}\cdot9\cdot3=5{,}940\quad m\text{-variables}.
\]

Here \(w_{ab,c}\) certifies that \(c\) is a common \(H\)-neighbor of
\(a,b\), \(f_D\) selects a three-guard configuration, and \(m_{D,r,u}\)
selects the response that moves the guard at \(u\in D\) to the unoccupied
attacked vertex \(r\notin D\).

The 20,008-clause base is followed by the 3,645 complete-bank clauses. The
base consists exactly of:

1. one no-\(K_4\) clause for every four-set;
2. common-neighbor existence and witness-implication clauses for every pair;
3. the induced, hub-free `hole5` template and its distinguished common
   neighbor;
4. one connectedness clause for each proper cut whose side containing
   vertex \(0\) is specified;
5. domination clauses for selected triples;
6. one nonempty-family clause;
7. one-guard response, legal-edge, and successor-family clauses; and
8. the redundant but sound clauses forcing every \(H\)-triangle into the
   selected family.

Let \(S\) be the accepted predicate sorting the six core signatures of
vertices \(6,\ldots,11\). The exact \(F_5\land S\) byte construction has
6,886 variables, 23,968 clauses, 192,169 literals, 754,323 bytes, and
SHA-256
`c6a0811c718ff8e9352f253e4ce225ce2826def9c3e4a9cd55f0b0152703d104`.

Finally let
\[
T:\quad e_{25}\le e_{45},
\]
encoded by the single clause \((-24,39)\). The exact
\(F_5\land S\land T\) byte construction has 6,886 variables, 23,969
clauses, 192,171 literals, 754,332 bytes, and SHA-256
`441e54c28fdf6005f0f17fb951bf37c7ff46e222f3e605b7e715fabeec8f64d4`.

## 2. Counterexample hypotheses and the complement dictionary

Call \(G\) a *connected order-12 parameter-three counterexample* when
\[
|V(G)|=12,\qquad G\text{ is connected},\qquad
\gamma(G)=\gamma^\infty(G)=3<\theta(G).
\tag{2.1}
\]

The parameter chain
\[
\gamma(G)\le i(G)\le\alpha(G)\le\gamma^\infty(G)\le\theta(G)
\]
collapses between its equal endpoints in (2.1), giving
\[
\alpha(G)=3.
\tag{2.2}
\]
For \(H=\overline G\), complementation therefore gives
\[
\omega(H)=\alpha(G)=3,\qquad
\chi(H)=\theta(G)>3.
\tag{2.3}
\]

A pair \(\{a,b\}\) dominates \(G\) exactly when it has no common neighbor
in \(H\): a vertex \(c\notin\{a,b\}\) is undominated by the pair in \(G\)
exactly when \(ac,bc\in E(H)\). Since \(\gamma(G)=3\), no pair dominates,
so
\[
\text{every pair of vertices of }H\text{ has a common }H\text{-neighbor}.
\tag{2.4}
\]

Let \(\mathcal D\) be an eternal family witnessing
\(\gamma^\infty(G)=3\). By definition, \(\mathcal D\) is a nonempty family
of dominating triples such that, for every \(D\in\mathcal D\) and every
unoccupied attacked vertex \(r\notin D\), some \(u\in D\) satisfies
\[
ur\in E(G),\qquad
(D-\{u\})\cup\{r\}\in\mathcal D.
\tag{2.5}
\]
This is an existential choice of one responding guard for each pair
\((D,r)\); it is not an all-guards move.

Every triangle of \(H\) is an independent triple of \(G\). By (2.2) it is a
maximum independent set. Starting from any configuration of \(\mathcal D\)
and attacking its currently unoccupied vertices one at a time forces all
three guards onto that independent triple: a responding guard cannot leave
another vertex of the independent set. Hence
\[
\text{every triangle of }H\text{ belongs to }\mathcal D.
\tag{2.6}
\]

## 3. Sound relabeling into the `hole5` template

Assume additionally that \(H\) contains a hub-free induced \(C_5\). Choose
an orientation and label its vertices
\[
0,1,2,3,4
\]
cyclically. Thus its only \(H\)-edges among the rim vertices are
\[
01,12,23,34,40.
\tag{3.1}
\]

By (2.4), the rim-edge endpoints \(0,1\) have a common \(H\)-neighbor.
No vertex of the induced \(C_5\) is adjacent to both endpoints of the rim
edge \(01\), so this common neighbor lies outside the rim. Label one such
vertex \(5\). Then
\[
e_{05}=e_{15}=1.
\tag{3.2}
\]
Label the remaining six vertices arbitrarily as \(6,\ldots,11\).

Hub-freeness says that every vertex \(x\in\{5,\ldots,11\}\) misses at least
one rim vertex in \(H\), exactly satisfying the template clause
\[
\bigvee_{v=0}^{4}\neg e_{xv}.
\tag{3.3}
\]
Equations (3.1)--(3.3) are precisely the frozen `hole5` template. No graph
symmetry is assumed: this is a relabeling of a selected induced cycle, one
of its rim edges, and a certified external common neighbor.

The general structural template theorem says that an order-12
parameter-three counterexample has a hub-free induced odd hole of length
5, 7, or 9, or an induced \(\overline{C_7}\). The present theorem covers
only the \(C_5\) branch. It does not assert that every counterexample belongs
to that branch.

## 4. Realizing every base variable

Define a Boolean assignment \(A\) to all 6,886 variables.

### 4.1 Graph and common-neighbor variables

Set
\[
A(e_{uv})=1\quad\Longleftrightarrow\quad uv\in E(H).
\tag{4.1}
\]
For every pair \(a,b\), choose one common neighbor \(c(a,b)\) supplied by
(2.4). Set \(w_{ab,c(a,b)}=1\) and all other \(w_{ab,c}=0\).

The no-\(K_4\) clauses hold because \(\omega(H)=3\). Each witness-existence
clause contains the chosen true variable. Its two implications are true
because \(ac(a,b),bc(a,b)\in E(H)\); every implication from a false witness
is vacuous.

The template clauses hold by Section 3. For every nonempty proper cut with
specified side containing vertex \(0\), connectedness of \(G\) supplies a
crossing \(G\)-edge. That pair is an \(H\)-nonedge, so the corresponding
negative edge literal satisfies the encoded cut clause.

### 4.2 Family and move variables

Set
\[
A(f_D)=1\quad\Longleftrightarrow\quad D\in\mathcal D.
\tag{4.2}
\]
For every \(D\in\mathcal D\) and \(r\notin D\), choose one guard
\(u(D,r)\) satisfying (2.5), set \(m_{D,r,u(D,r)}=1\), and set the other two
response variables for \((D,r)\) to zero. Set every move variable whose
source triple is not in \(\mathcal D\) to zero.

Now check each family clause.

- The family-nonempty clause holds because \(\mathcal D\ne\varnothing\).
- If \(f_D=0\), every domination and response clause for \(D\) is satisfied
  by \(\neg f_D\).
- If \(f_D=1\) and \(x\notin D\), domination of \(D\) in \(G\) gives some
  \(d\in D\) with \(xd\in E(G)\). Thus \(e_{xd}=0\), so the corresponding
  negative edge literal satisfies the domination clause.
- For selected \(D\) and unoccupied attack \(r\), the chosen move variable
  satisfies the response disjunction. Since \(u(D,r)r\in E(G)\), it is a
  nonedge of \(H\), so the legal-move implication
  \(m_{D,r,u}\Rightarrow\neg e_{ur}\) holds. The successor implication holds
  because (2.5) puts the successor in \(\mathcal D\).
- Every false move variable satisfies both of its implication clauses
  vacuously.
- If a triple is a triangle of \(H\), (2.6) makes its family variable true.
  If it is not a triangle, at least one of the three negative edge literals
  satisfies the redundant triangle-to-family clause.

Thus \(A\) satisfies every one of the 20,008 base clauses. The construction
uses exactly the required quantifier order
\[
\forall D\in\mathcal D\ \forall r\notin D\ \exists u\in D,
\]
and every true move variable represents exactly one guard traversing one
edge of \(G\).

## 5. The complete coloring bank

The forced positive template edges are the five rim edges together with
\(05\) and \(15\), so \(0,1,5\) form a triangle in \(H\). The complete bank
contains exactly one first-use canonical representative of every
three-color partition proper on these forced edges. Its exact size is
\[
\frac{(2^5-2)3^6}{3!}=3,645.
\]

For a bank row \(c=(c_0,\ldots,c_{11})\), its clause is
\[
C_c=\bigvee_{\substack{u<v\\c_u=c_v}}e_{uv}.
\tag{5.1}
\]
Clause \(C_c\) is false exactly when every color class is independent in
\(H\), namely when \(c\) is a proper three-coloring of \(H\).

Conversely, any proper coloring of a graph extending the template is proper
on the forced edges. Renaming its colors by first occurrence produces its
unique bank representative without changing its color classes. Therefore,
relative to the template,
\[
\bigwedge_{c\in B_5}C_c
\quad\Longleftrightarrow\quad
\chi(H)>3.
\tag{5.2}
\]

Equation (2.3) gives \(\chi(H)>3\), so the edge assignment (4.1) satisfies
all 3,645 bank clauses. Combined with Section 4, this proves that \(A\)
satisfies the exact retained \(F_5\).

## 6. Realization and symmetry-coverage theorem

**Theorem 1 (conditional `hole5` realization).** Let \(G\) be a connected
order-12 graph satisfying
\[
\gamma(G)=\gamma^\infty(G)=3<\theta(G).
\]
If \(H=\overline G\) contains a hub-free induced \(C_5\), then some labeling
of \(G\), together with explicit assignments to the common-neighbor,
family, and move variables, satisfies the exact retained formula \(F_5\).

Moreover, there are orbit-equivalent assignments satisfying
\[
F_5\land S
\qquad\text{and}\qquad
F_5\land S\land T.
\]

**Proof.** Sections 2--5 construct and verify the satisfying assignment of
\(F_5\).

For \(S\), permutations of vertices \(6,\ldots,11\) fixing
\(0,\ldots,5\) act on all graph, witness, family, and move variables and
preserve the complete formula. Sort the six outer core-signatures
lexicographically and apply the corresponding full variable relabeling.
The result satisfies \(F_5\land S\).

For \(T\), use the residual rim reflection
\[
\rho=(0\ 1)(2\ 4),
\]
fixing \(3,5,6,\ldots,11\). It preserves \(F_5\) and swaps \(e_{25}\) with
\(e_{45}\). If \(T\) fails, apply \(\rho\); the image satisfies \(T\).
Then sort the outer signatures. Every outer permutation fixes
\(e_{25},e_{45}\), so sorting preserves \(T\) and yields
\(F_5\land S\land T\). \(\square\)

The symmetry clauses are not logical consequences of \(F_5\); the theorem
uses equisatisfiability through full-variable orbit representatives.

## 7. Explicitly conditional exclusion corollary

**Corollary 2 (certificate gate, not presently activated).** If an accepted
independent checker verifies a sound UNSAT certificate for the exact
byte-bound formula \(F_5\land S\), or for the exact byte-bound formula
\(F_5\land S\land T\), then no connected order-12 parameter-three
counterexample can have a hub-free induced \(C_5\) in its complement.

**Proof.** Such a counterexample would satisfy the corresponding formula by
Theorem 1, contradicting certified unsatisfiability. \(\square\)

**Current status of the premise in this note:** unfilled. The conditional
corollary must not be promoted to an exclusion until the exact formula,
proof, checker, coverage, and successful replay are separately bound and
accepted.
