# Target-response propagation across independent states

## Status and scope

Date: 2026-07-28 (PDT)

This note uses the standard one-guard-moves eternal-domination model.
Attacks are made only at unoccupied vertices, exactly one adjacent guard
moves, and every retained state dominates.

The results below apply to every guard number \(k\).  They strengthen the
parameter-three vertex-star and facet-color propagation theorem C-106, but
they do not force the final global color intersection and do not resolve
the gamma--theta conjecture.

No literature-priority claim is made.

## Theorem (general vertex-star propagation)

Let \(\mathcal F\) be an eternal family of dominating \(k\)-sets in a
finite simple graph \(G\).  Let \(x\in V(G)\), and let \(T,T'\in\mathcal F\)
be independent \(k\)-sets avoiding \(x\).  If

\[
 v\in T\cap T',
\tag{1}
\]

then

\[
\boxed{
 vx\in E(G),\ T-v+x\in\mathcal F
 \quad\Longleftrightarrow\quad
 vx\in E(G),\ T'-v+x\in\mathcal F.
}
\tag{2}
\]

Thus, for a fixed target \(x\), whether the guard at a shared vertex \(v\)
can answer is independent of which retained independent \(k\)-state
containing \(v\) is used.

### Proof

By symmetry it is enough to prove the forward implication.  Assume

\[
 vx\in E(G),\qquad
 D_0=T-v+x\in\mathcal F.
\tag{3}
\]

Put

\[
 A=(T\cap T')-\{v\},\qquad
 O=T-T',\qquad
 B=T'-T.
\tag{4}
\]

Because \(T\) and \(T'\) have the same size,

\[
 |O|=|B|=:m.
\tag{5}
\]

Order the vertices of \(B\) as

\[
 B=\{b_1,\ldots,b_m\}.
\]

Starting from \(D_0\), attack \(b_1,b_2,\ldots,b_m\) in that order.  We
prove inductively that after the first \(j\) attacks there is a retained
state

\[
 D_j=\{x\}\cup A\cup\{b_1,\ldots,b_j\}\cup O_j,
\tag{6}
\]

where \(O_j\subseteq O\) and

\[
 |O_j|=m-j.
\tag{7}
\]

For \(j=0\), equations (4)--(5) turn (3) into (6).

Suppose \(D_{j-1}\) has been retained and attack the unoccupied vertex
\(b_j\).  Every guard in

\[
 A\cup\{b_1,\ldots,b_{j-1}\}
\tag{8}
\]

is nonadjacent to \(b_j\) in \(G\), because all those vertices and
\(b_j\) belong to the independent set \(T'\).  None of those guards can
answer.

If the guard at \(x\) moved to \(b_j\), the resulting \(k\)-set would be
contained in

\[
 (T\cup T')-\{v\}.
\tag{9}
\]

Every vertex in (9) is nonadjacent to \(v\) in \(G\): vertices of \(T\)
are nonadjacent to \(v\) because \(T\) is independent, and vertices of
\(T'\) are nonadjacent to \(v\) because \(T'\) is independent.  Hence an
\(x\)-move would produce a state that does not dominate \(v\), so that
successor cannot belong to \(\mathcal F\).

Eternal closure must therefore move one guard from \(O_{j-1}\) to
\(b_j\).  Removing that mover defines

\[
 O_j\subset O_{j-1},\qquad |O_j|=|O_{j-1}|-1,
\]

and gives the retained state (6).  This completes the induction.

At \(j=m\), equation (7) gives \(O_m=\varnothing\), while (4) gives

\[
 A\cup B=T'-\{v\}.
\]

Therefore

\[
 D_m=T'-v+x\in\mathcal F.
\tag{10}
\]

The graph edge \(vx\) was already part of (3), so (10) proves the forward
implication in (2).  Interchanging \(T\) and \(T'\) proves the reverse
implication. \(\square\)

## Corollary under equality

Suppose

\[
 \alpha(G)=\gamma^\infty(G)=k
\]

and \(\mathcal F\) is any eternal \(k\)-family.  Every independent
\(k\)-set belongs to \(\mathcal F\).  For a fixed target \(x\), define

\[
 A_x=
 \{v\ne x:
   v\text{ lies in an independent }k\text{-set }T\text{ avoiding }x,
   \ vx\in E(G),\ T-v+x\in\mathcal F\}.
\tag{11}
\]

The theorem makes \(A_x\) well-defined independently of \(T\).  Moreover,
for every independent \(k\)-set \(T\) avoiding \(x\),

\[
 \varnothing\ne T\cap A_x
 =
 \{v\in T:T-v+x\in\mathcal F\}.
\tag{12}
\]

For the displayed equality, membership of \(T-v+x\) in \(\mathcal F\)
already forces \(vx\in E(G)\): the retained successor must dominate \(v\),
while every vertex of \(T-\{v\}\) is nonadjacent to \(v\).  The
nonemptiness is exactly the required response to the unoccupied attack at
\(x\) from \(T\).

This produces a global, family-relative transversal of the maximum
independent sets avoiding each target.  The theorem does not assert that
\(A_x\) is a clique, a color class, a minimum transversal, or independent
of the chosen eternal family.

## Responder colors on \(k\)-facets

Retain the equality setup of the corollary.  Put

\[
 H'=\overline{G-x}
\]

and suppose \(H'\) has a proper \(k\)-coloring

\[
 \kappa:V(G)-\{x\}\longrightarrow\{1,\ldots,k\}.
\tag{13}
\]

Let \(\Gamma_x\) be the graph whose vertices are the independent
\(k\)-sets avoiding \(x\), with two sets adjacent when they share
\(k-1\) vertices.

### Theorem (componentwise responder-color propagation)

For a component \(C\) of \(\Gamma_x\), define using any \(T\in C\)

\[
 A_C^\kappa=\kappa(T\cap A_x).
\tag{14}
\]

Then \(A_C^\kappa\) is independent of the choice of \(T\in C\), and

\[
 \varnothing\ne A_C^\kappa\subseteq\{1,\ldots,k\}.
\tag{15}
\]

If a vertex

\[
 r\in N_{\overline G}(x)
\]

belongs to the support of \(C\), then

\[
 \kappa(r)\notin A_C^\kappa.
\tag{16}
\]

#### Proof

It is enough to compare adjacent facets

\[
 T=U\cup\{p\},\qquad
 T'=U\cup\{q\},\qquad |U|=k-1.
\]

The general vertex-star theorem makes active status of every member of
\(U\) independent of the chosen facet.  The two exchanged successors are
literally the same set:

\[
 T-p+x=U\cup\{x\}=T'-q+x.
\tag{17}
\]

If (17) belongs to \(\mathcal F\), its domination of \(p\) and \(q\)
forces both \(px,qx\in E(G)\), because every member of \(U\) is
nonadjacent in \(G\) to each exchanged vertex.  Hence \(p\in A_x\) if and
only if \(q\in A_x\).

Every independent \(k\)-set is a \(k\)-clique of \(H'\), so its vertices
use all \(k\) colors under \(\kappa\).  The shared set \(U\) uses
\(k-1\) colors, and \(p,q\) use the same remaining color.  Thus (14) is
invariant along a ridge step.  Connectivity gives well-definedness, and
(12) gives nonemptiness.

Finally, \(r\in N_{\overline G}(x)\) cannot lie in \(A_x\).  In any facet
of \(C\) containing \(r\), it is the unique vertex of color
\(\kappa(r)\).  That color is therefore absent from (14), proving
(16). \(\square\)

### Theorem (exact inactive-set color identity)

Put

\[
 R_x=V(G-x)\setminus A_x
\tag{17a}
\]

and write \(\operatorname{supp}(C)\) for the union of the facets in a
ridge component \(C\).  Then

\[
 \boxed{
 A_C^\kappa
 =
 \{1,\ldots,k\}\setminus
 \kappa\bigl(R_x\cap\operatorname{supp}(C)\bigr).
 }
\tag{17b}
\]

If every vertex of \(G-x\) lies in an independent \(k\)-set, then

\[
 \boxed{
 \bigcap_C A_C^\kappa
 =
 \{1,\ldots,k\}\setminus\kappa(R_x).
 }
\tag{17c}
\]

Consequently, a common responder color exists exactly when the chosen
deletion coloring uses at most \(k-1\) colors on \(R_x\).

#### Proof

Fix a component \(C\) and a color \(c\).  If
\(c\in A_C^\kappa\), then in every facet of \(C\) the unique
\(c\)-colored vertex is active.  Hence no support vertex of color \(c\)
belongs to \(R_x\).

Conversely, if color \(c\) is absent from
\(R_x\cap\operatorname{supp}(C)\), the unique \(c\)-colored vertex of
any facet in \(C\) is active.  Thus \(c\in A_C^\kappa\), proving (17b).

When the component supports cover every deletion vertex, intersecting
(17b) over all components gives (17c).  Its final assertion is immediate.
\(\square\)

Every \(k\)-clique of \(H'\) is an independent \(k\)-set of \(G-x\) and
therefore meets \(A_x\) by (12).  Hence

\[
 \omega(H'[R_x])\le k-1.
\tag{17d}
\]

For \(k=3\), this is the triangle-free inactive-set consequence.

### Theorem (common responder color extends the target)

Assume additionally that

\[
 \gamma(G-x)=\alpha(G-x)=\gamma^\infty(G-x)=k.
\tag{18}
\]

If

\[
 w\in\bigcap_C A_C^\kappa,
\tag{19}
\]

then giving \(x\) color \(w\) extends \(\kappa\) to a proper
\(k\)-coloring of \(\overline G\).  Consequently

\[
 \theta(G)=k.
\tag{20}
\]

#### Proof

The parameter chain and (18) imply that \(G-x\) is well-covered.  Every
deletion vertex therefore lies in an independent \(k\)-set: extend the
vertex to a maximal independent set, whose size is \(k\).

Let \(v\) be any deletion vertex of color \(w\), and choose an independent
\(k\)-set \(T\) containing it.  In the ridge component of \(T\), equation
(19) says that the unique \(w\)-colored member \(v\) of \(T\) lies in
\(A_x\).  Hence \(vx\in E(G)\), or equivalently
\(vx\notin E(\overline G)\).  No \(w\)-colored vertex is a complement
neighbor of \(x\), so color \(w\) extends over \(x\).

The coloring gives \(\theta(G)\le k\), while
\(\alpha(G)=k\le\theta(G)\), proving (20). \(\square\)

### Corollary (general critical full-target obstruction)

Suppose

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=k<\theta(G),
\tag{21}
\]

\[
 \gamma(G-x)=\alpha(G-x)=\gamma^\infty(G-x)=\theta(G-x)=k,
\tag{22}
\]

and \(x\) has a full response at some independent \(k\)-state \(S\).
Then, for every proper \(k\)-coloring \(\kappa\) of
\(\overline{G-x}\):

1. the ridge component \(C_0\) containing \(S\) satisfies
   \[
   A_{C_0}^\kappa=\{1,\ldots,k\};
   \]
2. the support of \(C_0\) is disjoint from
   \(N_{\overline G}(x)\);
3. every other component has a nonempty responder-color set; and
4. the total intersection of all component responder-color sets is empty.

In particular, \(\Gamma_x\) has at least three components.

#### Proof

Fullness makes every vertex of \(S\) active.  The componentwise theorem
therefore gives all \(k\) colors on \(C_0\), and (16) excludes complement
neighbors of \(x\) from its support.  Every component set is nonempty by
(15).  A nonempty total intersection would invoke the extension theorem
and contradict (21), so the total intersection is empty.  With one
component it would contain all \(k\) colors; with exactly two it would be
the nonempty set belonging to the one nonroot component.  Hence at least
three components are necessary. \(\square\)

For \(k=3\), these are the responder-color conclusions of C-106.  The
argument above shows that their dependence on three colors was inessential.

## Exact boundary

The proof uses both independence hypotheses.  They ensure, respectively,
that every old or new non-\(x\) guard is nonadjacent to the omitted vertex
\(v\), and that guards already placed in the target state \(T'\) cannot
answer later attacks.  No conclusion is claimed for arbitrary retained
dominating states.

The result does not turn the transversal (12) into a \(k\)-clique
partition.  Even in the critical deletion branch, it proves only that a
common responder color would extend and that a counterexample needs at
least three incompatible ridge components.  It does not prove that the
required common color exists.
