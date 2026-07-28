# Future-stable colors: forced responses and a cumulative-kernel reduction

## Status and exact scope

Date: 2026-07-28 (PDT)

This is a **candidate theorem package awaiting hostile review**.  It uses
the standard one-guard-moves model: attacks are made only at unoccupied
vertices, exactly one adjacent guard moves, and every retained state
dominates.

The package proves two reductions.

1. In the parameter-three equality setting, a color-restricted kernel is
   safe exactly when it is nonempty.  Thus the two named state-membership
   tests in the earlier definition are redundant.
2. All full-list vertices at one independent root can be treated at once.
   A single greatest kernel with the **union** of all chosen color bans
   prevents the state-reintroduction defect of sequential recomputation.
   Once such a cumulative kernel survives, the remaining extension
   question is exactly the accepted proper-list 2-SAT problem on the
   non-full vertices.

The package does **not** prove that any one color-restricted kernel is
nonempty, does not prove that any surviving kernel has a satisfiable
2-CNF, does not complete the \(k=3\) case, and does not resolve the
gamma--theta conjecture.

The accepted inputs are:

- maximum independent triples belong to every eternal triple-family
  (C-010);
- the frozen-color projection theorem (C-063);
- \(\alpha=\gamma^\infty=2\Longrightarrow\theta=2\) (C-006); and
- the exact no-full-list projection-gluing 2-SAT theorem used in C-063
  and the full-list slice.

No literature-priority claim is made.

## 1. Setup

Let
\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3,\qquad H=\overline G,
\tag{1.1}
\]
and let \(\mathcal F^\star\) be the literal greatest eternal family of
dominating triples.  Fix an independent triple
\[
 S=\{s_0,s_1,s_2\}.
\tag{1.2}
\]
For an eternal triple-family \(\mathcal E\), write
\[
 L_S^{\mathcal E}(z)=
 \{u\in S:uz\in E(G),\ S-u+z\in\mathcal E\}.
\tag{1.3}
\]

Fix \(x\notin S\), put
\[
 B_x=N_H(x),
\tag{1.4}
\]
and, for \(u\in S\), define the root-swap ban
\[
 \mathcal B_u(x)=
 \{S-u+b:b\in B_x\}.
\tag{1.5}
\]

## 2. Avoiding one root-swap ban forces the chosen response

### Theorem 2.1 (ban-avoidance forcing) — PROVED

Let \(\mathcal E\) be any nonempty eternal family of dominating triples
in a graph satisfying (1.1).  If
\[
 \mathcal E\cap\mathcal B_u(x)=\varnothing,
\tag{2.1}
\]
then
\[
 \boxed{u\in L_S^{\mathcal E}(x).}
\tag{2.2}
\]

The theorem does not require \(\mathcal E\) to be greatest and does not
assume that \(x\) is full in \(\mathcal F^\star\).

#### Proof

Every independent triple belongs to every eternal triple-family, so
\(S\in\mathcal E\).

Suppose, for a contradiction, that \(u\notin L_S^{\mathcal E}(x)\).
First,
\[
 u\notin B_x.
\tag{2.3}
\]
Indeed, if \(u\in B_x\), then
\(S=S-u+u\in\mathcal B_u(x)\), whereas every independent triple,
including \(S\), belongs to \(\mathcal E\).  This contradicts (2.1).

For every \(b\in B_x-S\), condition (2.1) also gives
\[
 u\notin L_S^{\mathcal E}(b).
\tag{2.4}
\]
Indeed, the only possible \(u\)-successor from \(S\) at \(b\) is the
banned state \(S-u+b\).

Let
\[
W_u=\{z\notin S:u\notin L_S^{\mathcal E}(z)\}
\]
and form the accepted frozen-\(u\) projection
\[
 Q_u=G[(S-\{u\})\cup W_u].
\tag{2.5}
\]
The assumed failure at \(x\) puts \(x\) in \(W_u\).  If
\(b\in B_x-S\), then (2.4) puts \(b\) in \(W_u\); if
\(b\in B_x\cap(S-\{u\})\), it is already a base vertex of \(Q_u\).
Together with (2.3), these observations give
\[
 \{x\}\cup B_x\subseteq V(Q_u).
\tag{2.6}
\]
The frozen-color projection theorem gives
\[
 \alpha(Q_u)=\gamma^\infty(Q_u)=2.
\]
The accepted parameter-two theorem therefore gives
\(\theta(Q_u)=2\).  Equivalently,
\[
 H[V(Q_u)]\text{ is bipartite}.
\tag{2.7}
\]

It remains to exhibit a triangle in (2.7).  The set \(B_x\) is nonempty,
since otherwise \(x\) dominates \(G\).  Choose \(b\in B_x\).  The pair
\(\{x,b\}\) does not dominate \(G\), because \(\gamma(G)=3\).  Hence
there is a vertex \(c\) adjacent in \(H\) to both \(x\) and \(b\).
Then \(c\in B_x\), and
\[
 xb,xc,bc\in E(H).
\]
Thus \(H[\{x,b,c\}]\) is a triangle contained in \(H[V(Q_u)]\), contrary
to (2.7).  This proves (2.2). \(\square\)

The proof isolates the exact use of \(\gamma=3\): it makes every vertex
of \(H[B_x]\) nonisolated.  More generally, the same proof works whenever
\(H[B_x]\) contains an edge.

## 3. The safe-color test is exactly kernel nonemptiness

Assume now that \(x\) is full at \(S\) in \(\mathcal F^\star\):
\[
 L_S^{\mathcal F^\star}(x)=S.
\tag{3.1}
\]
For \(u\in S\), let \(\mathcal K_u(x)\) be the greatest eternal family
among all dominating triples outside \(\mathcal B_u(x)\).  As in the
earlier safe-kernel note, call \(u\) safe when
\[
 S,\ S-u+x\in\mathcal K_u(x).
\tag{3.2}
\]

### Corollary 3.1 (nonempty if and only if safe) — PROVED

\[
 \boxed{
 u\text{ is safe at }(S,x)
 \quad\Longleftrightarrow\quad
 \mathcal K_u(x)\ne\varnothing.
 }
\tag{3.3}
\]

#### Proof

The forward implication is immediate.  Conversely, a nonempty
\(\mathcal K_u(x)\) is an eternal triple-family avoiding
\(\mathcal B_u(x)\).  Theorem 2.1 gives
\[
 u\in L_S^{\mathcal K_u(x)}(x),
\]
which includes both the move edge and the state
\(S-u+x\in\mathcal K_u(x)\).  The independent-state theorem also gives
\(S\in\mathcal K_u(x)\). \(\square\)

Thus the still-open single-incidence safe-color lemma is precisely
\[
 \boxed{\text{at least one of }
 \mathcal K_{s_0}(x),\mathcal K_{s_1}(x),\mathcal K_{s_2}(x)
 \text{ is nonempty}.}
\tag{3.4}
\]
No existence assertion is proved here.

There is also a useful local consequence.  If \(\mathcal K_u(x)\) is
nonempty, then its frozen-\(u\) omission projection contains
\((S-\{u\})\cup B_x\) but not \(x\).  It has equality parameter two and
clique-cover number two.  Hence the surviving kernel supplies one
globally consistent two-color orientation of the physical link with
color \(u\) absent from \(B_x\).  This remains only a local coloring
statement.

## 4. One cumulative kernel for the entire full core

Define the full greatest-family core at \(S\) by
\[
 X=F_3^\star(S)=
 \{x\notin S:L_S^{\mathcal F^\star}(x)=S\}.
\tag{4.1}
\]
Let
\[
 f:X\longrightarrow S
\tag{4.2}
\]
be a proposed anchored color assignment.  Define its cumulative ban
\[
 \mathcal B_f=
 \bigcup_{x\in X}
 \{S-f(x)+b:b\in N_H(x)\},
\tag{4.3}
\]
and let \(\mathcal K_f\) be the greatest eternal family among all
dominating triples outside \(\mathcal B_f\).

### Proposition 4.1 (all selected responses are forced) — PROVED

If \(\mathcal K_f\ne\varnothing\), then, simultaneously for every
\(x\in X\),
\[
 f(x)\in L_S^{\mathcal K_f}(x),
\tag{4.4}
\]
and for every \(b\in N_H(x)\),
\[
 f(x)\notin L_S^{\mathcal K_f}(b).
\tag{4.5}
\]

#### Proof

The cumulative ban contains the individual ban
\(\mathcal B_{f(x)}(x)\).  Apply Theorem 2.1 to the nonempty family
\(\mathcal K_f\) to obtain (4.4).  Equation (4.5) is immediate because
its only possible successor is a state in \(\mathcal B_f\). \(\square\)

This is why one cumulative kernel is preferable to sequentially
recomputing three separate kernels: every earlier ban remains literally
present, so no forbidden state can be reintroduced.

Put
\[
 Y=V(G)-(S\cup X).
\tag{4.6}
\]
If \(\mathcal K_f\ne\varnothing\), then every list
\(L_S^{\mathcal K_f}(y)\), \(y\in Y\), is nonempty.  It has size at most
two, because \(\mathcal K_f\subseteq\mathcal F^\star\) and \(y\notin X\).
Give the vertices the color domains
\[
 D_f(s)=\{s\}\ (s\in S),\qquad
 D_f(x)=\{f(x)\}\ (x\in X),\qquad
 D_f(y)=L_S^{\mathcal K_f}(y)\ (y\in Y).
\tag{4.7}
\]
Every domain has size one or two.  Let
\[
 \Phi_f
\tag{4.8}
\]
be the ordinary exact list-coloring 2-CNF: a two-element domain gets one
Boolean variable, singleton domains are fixed, and for every edge of
\(H\) and every color common to its endpoint domains, add the clause
forbidding both endpoints from taking that color.  This formula is
satisfiable exactly when \(H\) has a proper coloring from the domains
in (4.7).

### Theorem 4.2 (exact cumulative-kernel characterization) — PROVED

Under (1.1),
\[
 \boxed{
 \theta(G)=3
 }
\]
if and only if there is an assignment \(f:X\to S\) such that:

1. \(f\) is a proper coloring of \(H[X]\);
2. \(\mathcal K_f\ne\varnothing\); and
3. the exact 2-CNF \(\Phi_f\) is satisfiable.

#### Proof

First assume the three conditions.  A satisfying assignment of
\(\Phi_f\) is, by its literal clauses, a proper three-coloring of \(H\).
Thus \(\theta(G)=3\).  Equations (4.4)--(4.5) explain why the prescribed
full-core colors are family-compatible and why no same-color
\(X\)--\(Y\) edge can occur, but exactness here is simply the direct
2-CNF encoding.

Conversely, suppose \(\theta(G)=3\), and fix a proper three-coloring
\(\kappa\) of \(H\), relabeled so that \(\kappa(s)=s\) for \(s\in S\).
Set \(f=\kappa|_X\).  It is proper on \(H[X]\).

The family of all triples having one vertex of each \(\kappa\)-color is
an eternal triple-family.  If \(b\in N_H(x)\), then
\(\kappa(b)\ne\kappa(x)=f(x)\), so
\[
 S-f(x)+b
\]
is not a color transversal.  The clique-fiber family therefore avoids
every state in \(\mathcal B_f\), and hence is contained in
\(\mathcal K_f\).  In particular, \(\mathcal K_f\ne\varnothing\).

For every \(y\in Y\), the transversal
\[
 S-\kappa(y)+y
\]
belongs to the clique-fiber family and therefore to \(\mathcal K_f\).
Thus \(\kappa(y)\in L_S^{\mathcal K_f}(y)\).  The restriction of
\(\kappa\) therefore respects every domain in (4.7), so it satisfies the
exact list-coloring 2-CNF \(\Phi_f\). \(\square\)

Theorem 4.2 is an exact reformulation, not a proof that the right-hand
side occurs under equality.  It separates the remaining obstruction into
two independently checkable failures:

\[
\boxed{
\begin{array}{l}
\textbf{kernel annihilation: }\mathcal K_f=\varnothing
\text{ for every proper }f;\\[2mm]
\textbf{Boolean obstruction: }\mathcal K_f\ne\varnothing
\text{ but every surviving }\Phi_f\text{ is unsatisfiable.}
\end{array}}
\tag{4.9}
\]

In the single-full case \(X=\{x\}\), the first branch is exactly the
failure of all three safe colors.  In the second branch, the full-target
augmentation has disappeared into the cumulative ban: a minimal
unsatisfiable core of \(\Phi_f\) is an ordinary minimal unsatisfiable
2-CNF (hence has the accepted two-unit-chain, one-unit-lollipop, or
unit-free-bicycle form).

## 5. A retained terminal-entry normal form when a kernel is empty

This section records a fully finite consequence of kernel annihilation.
It does not eliminate that branch.

Fix \(u\in S\), abbreviate \(A=S-\{u\}\), and suppose
\(\mathcal K_u(x)=\varnothing\).  Start the usual simultaneous deletion
process with all dominating triples outside \(\mathcal B_u(x)\), and give
each deleted state its finite deletion rank.

### Proposition 5.1 (retained descent to a ban) — PROVED

From every state
\[
 D\in\mathcal F^\star-\mathcal B_u(x)
\]
there is a finite legal one-guard response trace, all of whose preterminal
states lie in \(\mathcal F^\star-\mathcal B_u(x)\) and have strictly
decreasing restricted deletion rank, whose final state lies in
\(\mathcal F^\star\cap\mathcal B_u(x)\).

In particular, this applies to \(S-u+x\).

#### Proof

At a state of finite rank, choose an attack witnessing its deletion.
Closure of \(\mathcal F^\star\) supplies a retained response.  If its
successor is not banned, then it was absent from the deletion stage at
which the current state failed, so it has strictly smaller rank.  Continue.
Finite descent ends with a retained banned successor. \(\square\)

### Proposition 5.2 (the only two terminal-entry gates) — PROVED

Let the final move in Proposition 5.1 enter
\[
 A\cup\{b\},\qquad b\in B_x.
\tag{5.1}
\]
Exactly one of the following forms occurs.

1. **Corridor entry.**  The attack is at \(b\), the predecessor is
   \[
   A\cup\{q\},\qquad q\notin B_x,
   \]
   and the move is \(q\to b\).
   If \(q=u\), this is a direct \(u\)-response from the root \(S\).
   Otherwise \(q\notin S\cup B_x\cup\{x\}\), and
   \[
   G[\{x,u,q,b\}]\cong K_4-xb;
   \tag{5.2}
   \]
   that is, these four vertices induce a diamond whose missing edge is
   \(xb\).
2. **Anchor-restoration entry.**  The attack is at one member \(a\in A\).
   Writing \(A=\{a,c\}\), the predecessor is
   \[
   \{c,b,q\},
   \]
   and the selected retained move is \(q\to a\).

#### Proof

The attacked vertex belongs to the successor (5.1) but not to the
predecessor.  If it is \(b\), removing the moving guard from the
predecessor must leave exactly \(A\), giving form 1.  The predecessor is
not banned, so \(q\notin B_x\).

If the attacked vertex is not \(b\), it must be one of the two members of
\(A\).  Removing that attacked anchor from (5.1) and restoring the mover
gives exactly form 2.  These cases exhaust the three vertices of (5.1).

For the non-root corridor, the move gives \(qb\in E(G)\), while
\(q\notin B_x\) gives \(qx\in E(G)\), and fullness gives
\(ux\in E(G)\).  The retained predecessor \(A+q\) must dominate the
omitted anchor \(u\); the two anchors in \(A\) miss \(u\), so
\(qu\in E(G)\).  Similarly, the retained successor \(A+b\) forces
\(bu\in E(G)\).  Finally \(b\in B_x\) gives \(bx\notin E(G)\).
The four vertices are distinct (the mover cannot be \(x\), which has no
edge to \(b\)), proving (5.2). \(\square\)

Thus a hypothetical equality counterexample with one full target and no
safe color must carry three finite retained descent traces, one for each
color, ending only in direct-root/corridor diamonds or
anchor-restoration gates.  Ruling out those three interlocking traces is
the narrow kernel-annihilation problem left by this package.

## 6. Exact controls and audit boundary

The ordinary-frozenset checker in this directory reproduces:

- the order-12 equality control ``Ksv`f\knJVis``, root
  \(\{1,2,3\}\), whose full core is \(\{0\}\): two cumulative kernels are
  empty, while color \(3\) leaves a 64-state kernel and a satisfiable
  residual coloring problem;
- MMV-001 ``IEhbtj{ro``, root \(\{0,1,2\}\), whose single full target
  has all three kernels empty and \(\gamma=2\);
- MMV-021 ``JEhbtj{rv~?``, root \(\{0,1,2\}\), where target \(10\) has
  an individually surviving restricted kernel but the two-vertex full
  core has no surviving cumulative assignment; and
- all 581 full incidences in the fixed 55-graph
  \(\alpha=\gamma^\infty=3<\theta\) catalog: every unsafe color has an
  empty restricted kernel.

The gamma-two controls are not counterexamples to Theorem 2.1 because its
\(\gamma=3\) hypothesis is absent.  MMV-021 also shows why an individual
safe color must not be advertised as a coloring theorem.

An exploratory scan of all 12,113 connected unlabeled graphs through
order eight found 8,344 full greatest-family incidences and 25,032
color tests in the wider \(\alpha=\gamma^\infty=3\) class.  Of these,
25,026 restricted kernels were nonempty and all contained the forced
response; the remaining six were empty.  This last scan is
**OBSERVED** only and is not used in any proof.

## 7. Exact remaining target

The equality safe-color lemma remains open.  In the terminology proved
here, its single-target form is exactly:

> among three root-swap bans, at least one leaves a nonempty eternal
> kernel.

Even after that statement, a universal proof still needs to eliminate the
ordinary no-full 2-SAT obstruction in every surviving cumulative kernel.
The present package makes those two gaps disjoint and prevents sequential
kernel recomputation from obscuring either one.
