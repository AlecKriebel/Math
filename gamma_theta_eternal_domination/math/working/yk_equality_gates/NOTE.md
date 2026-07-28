# Two exact gates in the all-parameter \(Y_k\) realization

## Status and scope

Date: 2026-07-28 (PDT)

This note continues C-125--C-126.  It assumes the exact static
\(Y_k=K_{k-3}\vee P_4\) notation from C-125 and studies the two hypotheses
which were left open there:

1. whether the installed singleton clique must be clean; and
2. whether endpoint static defects must survive the clean projection.

The main new conclusion is a stronger clean-branch order floor which does
**not** assume static-defect survival:

\[
\boxed{
 k\geq5,\quad
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=k,\quad
 \text{clean exact static }Y_k
 \quad\Longrightarrow\quad
 |V(G)|\geq 2k+9.
}
\tag{0.1}
\]

The proof is human and length-independent.  It combines:

- a mandatory directed cycle of dirty singleton-to-\(D\) incidences;
- two external closed-private buffers forced by that cycle;
- the equality-three projection and the order-twelve dynamic witness
  system of C-072; and
- one original endpoint static-defect vertex, counted whether or not it
  survives the projection.

Thus projected static-defect survival is not needed for the order count.
The note does **not** prove that defects always survive.

There is also a sharp structural answer at the first gate:

\[
\boxed{\text{A clean exact static }Y_4\text{ cannot occur.}}
\tag{0.2}
\]

More generally, every singleton vertex necessarily has a wrong-role
neighbor among the original anchors.  In the base-clean branch these
neighbors lie in \(D\), so \(k\geq5\) and a directed contamination cycle
is unavoidable.

A dirty base incidence, when it occurs, installs a closed-private buffer
and a retained shifted three-guard carrier.  The direct response lists at
that carrier are nonempty subsets of the \(Y_3\) caps, and the endpoint
lists are exact.  If the shifted carrier is independent from the installed
singletons, the whole exact dynamic \(Y_3\) pattern follows.  Without that
extra independence, however, the initially claimed exactness is not
proved: hostile review found a finite \(Z\)-fixed symbolic model in which
all established caps, graph incidences, restoration conditions, and
one-guard obligations hold while a middle role is absent.  Section 5
records the corrected theorem and the sharp proof-method falsifier.

No counterexample, all-order \(Y_k\) exclusion, proof of
\(\mathsf{GL}(k)\), or resolution of the gamma--theta conjecture is
claimed.

## 1. Exact setup

Let \(\mathcal F\) be an eternal family of dominating \(k\)-sets in
\(G\), let

\[
 S=B\mathbin{\dot\cup}D,\qquad
 B=\{a,b,c\},\qquad |D|=k-3
\tag{1.1}
\]

be an independent retained state, and put \(H=\overline G\).  There are
vertices

\[
 Z=\{z_d:d\in D\},\qquad
 X=\{x_0,x_1,x_2,x_3\}
\tag{1.2}
\]

such that \(H[Z\cup X]=K_{k-3}\vee P_4\), with path
\(x_0x_1x_2x_3\), and

\[
 L_S^{\rm stat}(z_d)=\{d\}\qquad(d\in D),
\tag{1.3}
\]

\[
\begin{array}{c|cccc}
v&x_0&x_1&x_2&x_3\\ \hline
L_S^{\rm stat}(v)&
D\cup\{a\}&D\cup\{a,c\}&D\cup\{b,c\}&D\cup\{b\}.
\end{array}
\tag{1.4}
\]

Put

\[
A_0=\{a\},\quad A_1=\{a,c\},\quad
A_2=\{b,c\},\quad A_3=\{b\}.
\tag{1.5}
\]

C-125 proves:

- every partial singleton replacement is retained;
- in particular
  \[
  T=B\cup Z\in\mathcal F;
  \tag{1.6}
  \]
- \(L_S^{\mathcal F}(z_d)=\{d\}\); and
- \(L_S^{\mathcal F}(x_i)\cap B=A_i\).

For \(u\in S\), write

\[
 P_S(u)=\{p:N_G[p]\cap S=\{u\}\}
\tag{1.7}
\]

for its closed-private block relative to \(S\).

The installation is **base-clean** (called simply clean in C-125) when

\[
 E_G(B,Z)=\varnothing.
\tag{1.8}
\]

In that case

\[
 J=G[\{v\notin Z:E_G(v,Z)=\varnothing\}]
\tag{1.9}
\]

is the clean equality-three projection of C-125.

## 2. Every singleton is necessarily contaminated

For \(d\in D\), define

\[
 A(d)=N_G(z_d)\cap(S-\{d\}).
\tag{2.1}
\]

### Lemma 2.1 (mandatory singleton contamination) — PROVED

For every \(d\in D\),

\[
\boxed{A(d)\ne\varnothing.}
\tag{2.2}
\]

For every \(u\in A(d)\), there is a vertex

\[
\boxed{
 p\in P_S(u)\cap N_H(z_d).
}
\tag{2.3}
\]

#### Proof

Fix \(i\in\{0,1,2,3\}\).  Since \(d\in L_S^{\rm stat}(x_i)\), the state

\[
 S-d+x_i
\tag{2.4}
\]

dominates \(G\).  The vertex \(z_d\) is not in that state, and
\(z_dx_i\notin E(G)\) because \(H[Z\cup X]\) is a join.  Therefore some
member of \(S-\{d\}\) is adjacent to \(z_d\), proving (2.2).

Now let \(u\in A(d)\).  The edge \(uz_d\) is present, but
\(u\notin L_S^{\rm stat}(z_d)=\{d\}\).  Hence \(S-u+z_d\) fails to
dominate.  Let \(p\) be a missed vertex.  It is nonadjacent to
\(z_d\) and to every member of \(S-\{u\}\).  Since \(S\) dominates,
\(p\) is adjacent to \(u\).  Thus
\(N_G[p]\cap S=\{u\}\) and \(pz_d\in E(H)\), proving (2.3).
\(\square\)

The first conclusion is easy to overlook: the positive \(d\)-role at
every path vertex and the graph nonedge \(z_dx_i\) force \(z_d\) to be
dominated by a *different original anchor* after \(d\) moves.

### Corollary 2.2 (the clean branch starts at \(k=5\)) — PROVED

If the installation is base-clean, then

\[
 A(d)\subseteq D-\{d\}\qquad(d\in D).
\tag{2.5}
\]

Consequently:

1. no clean exact static \(Y_4\) exists; and
2. for \(k\geq5\), the directed graph on \(D\) with arc
   \(d\to e\) whenever \(z_de\in E(G)\) has minimum outdegree at least
   one and hence contains a directed cycle of length at least two.

#### Proof

Base-cleanliness excludes \(B\) from \(A(d)\), and \(d\notin A(d)\) by
definition, giving (2.5).  If \(|D|=1\), (2.5) contradicts Lemma 2.1.
If \(|D|\geq2\), every vertex of the displayed finite loopless digraph
has positive outdegree, so following outgoing arcs eventually produces a
directed cycle. \(\square\)

This does not prove that equality forces cleanliness.  In fact, at
\(k=4\) any exact realization would necessarily use a dirty
singleton-to-base edge.

## 3. A clean contamination cycle forces external buffers

### Lemma 3.1 (cycle buffers lie outside the clean projection) — PROVED

Assume the installation is base-clean.  Let

\[
 d_0\to d_1\to\cdots\to d_{\ell-1}\to d_0
\tag{3.1}
\]

be a simple directed cycle in the contamination digraph.  For each
\(j\), with indices modulo \(\ell\), choose by Lemma 2.1

\[
 p_j\in P_S(d_{j+1})\cap N_H(z_{d_j}).
\tag{3.2}
\]

Then:

1. the vertices \(p_0,\ldots,p_{\ell-1}\) are pairwise distinct;
2. none belongs to \(S\cup Z\cup X\); and
3. every \(p_j\) has a graph neighbor in \(Z\), and therefore
   \[
   p_j\notin V(J).
   \tag{3.3}
   \]

In particular, there are at least two distinct vertices outside
\(J\cup D\cup Z\).

#### Proof

Closed-private blocks of different anchors are disjoint.  The heads
\(d_{j+1}\) on a simple directed cycle are distinct, proving (1).

A vertex in \(S\) cannot be a missed vertex in the proof of Lemma 2.1;
more directly, \(p_j=d_{j+1}\) would be adjacent to \(z_{d_j}\), contrary
to (3.2), while every other member of \(S\) is excluded by
\(P_S(d_{j+1})\).

No path vertex lies in \(P_S(d_{j+1})\): by (1.4), every \(x_i\) is
adjacent to every member of \(D\), and the clean branch has
\(|D|\geq2\).

Suppose \(p_j=z_f\).  Since \(z_f\) is adjacent to its anchor \(f\),
closed privacy forces \(f=d_{j+1}\).  But Lemma 2.1 and
base-cleanliness give \(z_f\) another neighbor in \(D-\{f\}\), again
contradicting \(z_f\in P_S(f)\).  This proves (2).

Finally, the retained state \(T=B\cup Z\) dominates \(p_j\).  The vertex
\(p_j\) is nonadjacent to all of \(B\), because it is private to an
anchor in \(D\).  It is not occupied in \(T\), by (2).  Hence some member
of \(Z\) is adjacent to \(p_j\).  This excludes \(p_j\) from the common
antineighborhood \(J\) and proves (3). \(\square\)

Thus the very graph edges which permit a base-clean installation force
two new vertices beyond the \(D\cup Z\) vertices already excluded from
the equality-three projection.

## 4. Endpoint defects count even when projection repairs them

Assume from now on

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=k
\tag{4.1}
\]

and base-cleanliness.  C-125 gives

\[
 \gamma(J)=\alpha(J)=\gamma^\infty(J)=3
\tag{4.2}
\]

and an eternal triple-family \(\mathcal P\) on \(J\) whose family lists
at \(B=\{a,b,c\}\) on \(x_0x_1x_2x_3\) are exactly

\[
 \{a\},\quad\{a,c\},\quad\{b,c\},\quad\{b\}.
\tag{4.3}
\]

C-070 applied inside \(J\) gives

\[
 cx_0,cx_3\in E(G).
\tag{4.4}
\]

The original static lists (1.4) omit \(c\) at both endpoints.  Therefore
the two original swaps \(S-c+x_0\) and \(S-c+x_3\) fail to dominate
\(G\).  Define their nonempty defect sets

\[
 E_0=N_H(S-\{c\})\cap N_H(x_0),
\qquad
 E_3=N_H(S-\{c\})\cap N_H(x_3).
\tag{4.5}
\]

Every member of \(E_0\cup E_3\) belongs to \(P_S(c)\).

### Lemma 4.1 (survive-or-count dichotomy) — PROVED

Let \(q\in E_0\) (and symmetrically for \(E_3\)).

- If \(q\in V(J)\), then \(q\) is a projected endpoint static defect and
  is distinct from all twelve vertices in the separated C-072 witness
  system.
- If \(q\notin V(J)\), then \(q\) is adjacent to a member of \(Z\) and is
  a new vertex outside
  \[
  J\cup D\cup Z\cup\{p_0,\ldots,p_{\ell-1}\},
  \tag{4.6}
  \]
  where the \(p_j\) are the cycle buffers from Lemma 3.1.

Thus an original endpoint defect contributes at least one further vertex
whether or not the clean projection repairs its static role.

#### Proof

The failed state \(S-c+x_0\) contains every member of \(D\) and the
anchors \(a,b\).  A missed vertex \(q\) is therefore external to that
state, is nonadjacent to \(D\cup\{a,b,x_0\}\), and, since \(S\)
dominates, is adjacent to \(c\).  Hence \(q\in P_S(c)\).

Suppose first that \(q\in J\).  Then \(\{a,b,x_0\}\) fails to dominate
\(J\), so \(q\) is a genuine endpoint defect in the equality-three
projection.

C-072 supplies, beyond \(B\cup X\), five mutually separated witnesses
which may be denoted

\[
 w,\quad z,\quad p_L,\quad p_R,\quad y.
\tag{4.7}
\]

Its accepted incidence ledger gives positive \(a,b\)-roles at \(w\), a
positive \(b\)-role at \(p_L\), a positive \(a\)-role at \(p_R\), and
graph edges from \(y\) to both \(a,b\).  The vertex \(q\), being private
to \(c\), has neither graph edge to \(a\) nor to \(b\), so it is distinct
from \(w,p_L,p_R,y\).

The remaining witness \(z\) belongs to
\(N_H(x_0)\cap N_H(x_3)\).  If \(q=z\), then \(q\) is simultaneously an
endpoint defect at \(x_0\) and \(x_3\).  The local double-defect kernel
lemma of C-121 applies using only (4.2)--(4.4) and rules this out.  Thus
\(q\) is also distinct from \(z\), and it is visibly outside the
seven-vertex reference/path core.  This proves the first alternative.

Suppose instead that \(q\notin J\).  By the definition of \(J\), \(q\)
has a graph neighbor in \(Z\).  It is not in \(D\), since \(D\) was
occupied in the failed state.  It is not in \(Z\), because every \(z_d\)
is adjacent to the occupied anchor \(d\) and hence is not missed.  It is
outside \(J\) by assumption.  Finally,

\[
 q\in P_S(c),\qquad
 p_j\in P_S(d_{j+1}),
\tag{4.8}
\]

and closed-private blocks of distinct anchors are disjoint.  Hence \(q\)
is distinct from all cycle buffers.  This proves the second
alternative. \(\square\)

This lemma records exactly what a projected repair means: it does not
erase the original defect vertex; it moves that vertex outside the clean
projection by an edge to the installed singleton clique.

### Theorem 4.2 (unconditional clean \(Y_k\) floor) — PROVED

If \(k\geq5\), (4.1) and a base-clean exact static \(Y_k\) realization
imply

\[
\boxed{|V(G)|\geq2k+9.}
\tag{4.9}
\]

#### Proof

C-072 applied to the clean equality-three projection gives

\[
 |V(J)|\geq12.
\tag{4.10}
\]

Every member of \(D\) is outside \(J\), because it is adjacent to its
installed singleton, and \(Z\) is excluded by definition.  Hence
\(D\cup Z\) contributes

\[
 2(k-3)
\tag{4.11}
\]

vertices outside \(J\).

Lemma 3.1 contributes at least two further, distinct cycle buffers
outside \(J\cup D\cup Z\).  Lemma 4.1 contributes one original endpoint
defect distinct from all vertices counted so far.  Therefore

\[
 |V(G)|
 \geq 12+2(k-3)+2+1
 =2k+9.
\]
\(\square\)

The stronger hypothesis (5.3) in C-125 is therefore unnecessary for an
order improvement.  The mechanism is different: two vertices come from
the mandatory contamination cycle, and the endpoint defect is counted on
whichever side of the projection it lies.

### Corollary 4.3 (exact remaining one-vertex collision) — PROVED

If \(E_0\cup E_3\) contains two distinct vertices, then the proof above
gives

\[
 |V(G)|\geq2k+10.
\tag{4.12}
\]

The only way the endpoint-defect contribution can remain one is that

\[
 E_0=E_3=\{q\}
\quad\text{for the selected minimal union, with}\quad
 q\notin J.
\tag{4.13}
\]

In particular, the common defect is adjacent to \(Z\).  A common defect
inside \(J\) is excluded by C-121's double-defect kernel.

This isolates the sharp residual obstruction to gaining the second
endpoint vertex.  It does not assert that (4.13) exists.

## 5. What a dirty base incidence actually creates

The clean branch is now quantitatively stronger, but equality has not
been shown to force it.  Hostile review found that the first version of
this section overclaimed exact response-list transport at a
nonindependent shifted carrier.  The corrected statement is the
following.

### Lemma 5.1 (private-buffer carrier, corrected) — PROVED

Do not assume base-cleanliness.  Suppose

\[
 u\in B,\qquad uz_d\in E(G)
\tag{5.1}
\]

for some \(d\in D\).  Choose by Lemma 2.1

\[
 p\in P_S(u)\cap N_H(z_d).
\tag{5.2}
\]

Let \(\rho:B\to C=(B-\{u\})\cup\{p\}\) replace \(u\) by \(p\) and fix
the other two base anchors, and put

\[
 U=Z\cup C.
\tag{5.3}
\]

Then:

1. \(U\in\mathcal F\);
2. for the legal retained response set
   \[
   R_i=\{v\in C:vx_i\in E(G),\ U-v+x_i\in\mathcal F\},
   \tag{5.4}
   \]
   one has
   \[
   \varnothing\ne R_i\subseteq\rho(A_i)
   \qquad(0\leq i\leq3);
   \tag{5.5}
   \]
3. every member of \(\rho(A_i)\) is graph-adjacent to \(x_i\);
4. the endpoint caps are exact:
   \[
   R_0=\{\rho(a)\},\qquad R_3=\{\rho(b)\};
   \tag{5.6}
   \]
5. if \(E_G(C,Z)=\varnothing\), equivalently if \(U\) is independent,
   then
   \[
   R_i=\rho(A_i)\qquad(0\leq i\leq3).
   \tag{5.7}
   \]

#### Proof

Since \(p\in P_S(u)\), attacking \(p\) from \(S\) uniquely moves \(u\).
Thus

\[
 S-u+p\in\mathcal F,\qquad
 L_S^{\mathcal F}(p)=\{u\}.
\tag{5.8}
\]

Now attack \(p\) from the installed state \(T=B\cup Z\).  No base guard
other than \(u\) is adjacent to \(p\).  If a singleton guard \(z_e\)
moved, the successor's outside positions relative to \(S\) would be
\((Z-\{z_e\})\cup\{p\}\).  Their original family lists cover only

\[
 (D-\{e\})\cup\{u\},
\tag{5.9}
\]

while the successor misses every member of \(D\), including \(e\).
This violates restoration relative to \(S\).  Hence \(u\) is the unique
possible retained responder and \(U\in\mathcal F\).

Attack \(x_i\) from \(U\).  No member of \(Z\) is adjacent to \(x_i\).
If \(v\in B-\{u\}\) responds, restoration relative to \(S\) requires
\(v\in A_i\): the installed singleton lists cover \(D\), the buffer
\(p\) covers \(u\), and only the original base portion \(A_i\) of the
\(x_i\)-list can cover the newly missing \(v\).  If \(p\) responds, the
same argument requires \(u\in A_i\).  Closure makes the response set
nonempty, proving (5.5), and the singleton endpoint caps give (5.6).

If \(v\in A_i-\{u\}\), then \(vx_i\in E(G)\) because \(v\) is a
positive original static role.  If \(u\in A_i\), the dominating state
\(S-u+x_i\) must dominate \(p\).  The buffer \(p\) is nonadjacent to
every member of \(S-\{u\}\), so necessarily \(px_i\in E(G)\).  This
proves the graph-incidence assertion.

Finally suppose \(E_G(C,Z)=\varnothing\).  Then \(U\) is independent.
Freeze \(Z\) in its common graph antineighborhood.  The \(Z\)-fixed
portion of \(\mathcal F\) is an eternal triple-family containing \(C\);
the path attacks have the nonempty family-list caps (5.5).  Arbitrary-state
restoration relative to the independent triple \(C\), followed by the
same path attack used in the family-cap version of C-121, forces first
the two middle-color roles and then the remaining two middle roles.
Thus all caps are attained, proving (5.7). \(\square\)

### 5.1 Why the nonindependent extension is invalid

When \(E_G(C,Z)\ne\varnothing\), restoration relative to the original
independent state \(S\) still constrains which original colors occur in
\(L_S^{\mathcal F}(x_i)\).  It does **not** imply that the corresponding
direct successor \(U-\rho(v)+x_i\) belongs to \(\mathcal F\).  This is
the exact point at which the first version incorrectly repeated the
C-121 proof.

The hostile review gives a finite symbolic control.  Take

\[
 Z=\{z_0,z_1\},\qquad C=\{p,b,c\},\qquad
 X=\{x_0,x_1,x_2,x_3\},
\]

and the graph edges

\[
\begin{split}
 &z_1p,\\
 &px_0,px_1,\\
 &bx_1,bx_2,bx_3,\\
 &cx_0,cx_1,cx_2,cx_3,\\
 &x_0x_2,x_0x_3,x_1x_3.
\end{split}
\tag{5.10}
\]

All other pairs are nonedges.  Thus \(Z\) and \(C\) are separately
independent, \(Z\) is anticomplete to \(X\), \(X\) is an induced
complement \(P_4\), but \(U=Z\cup C\) is nonindependent through \(z_1p\).

Assign the abstract original-palette lists

\[
\{d_0\},\quad\{d_1\},\quad\{a\}
\]

to \(z_0,z_1,p\), respectively, and assign

\[
D\cup\{a\},\quad D\cup\{a,c\},\quad
D\cup\{b,c\},\quad D\cup\{b\}
\tag{5.11}
\]

to the four path vertices.  Among the dominating five-sets satisfying
the resulting restoration inclusions, delete the direct state
\(U-c+x_1\) and take the greatest one-guard kernel.  The kernel has
34 states, contains \(U\), and satisfies all \(34(9-5)=136\)
unoccupied-attack obligations.  Its direct response lists at \(U\) are

\[
\{p\},\quad\{p\},\quad\{b,c\},\quad\{b\}.
\tag{5.12}
\]

Every role in the intended caps is a graph incidence, but the \(c\)-role
at \(x_1\) is absent.  The independent hostile checker reconstructs this
kernel rather than trusting a listed family.

This control refutes the inference from caps, graph incidences,
restoration, and closure to exact shifted lists when \(U\) is
nonindependent.  It is not asserted to realize the entire original
static \(Y_k\) setup in one graph, so it does not refute a possible
stronger equality-specific dirty-carrier theorem.  That theorem remains
open.

## 6. Consolidated gate verdict

The two gates now have the following exact status.

### Cleanliness gate

- Every singleton \(z_d\) necessarily has a wrong-role neighbor in
  \(S-\{d\}\).
- At \(k=4\), that neighbor must be a base anchor, so the clean branch is
  impossible.
- In a base-clean realization with \(k\geq5\), the wrong-role neighbors
  form a directed graph on \(D\) with a directed cycle.  That cycle
  forces at least two distinct external buffers outside the clean
  projection.
- A dirty base edge forces the shifted exact dynamic carrier of
  Lemma 5.1 only when the shifted carrier remains independent of \(Z\).
  In general it forces a retained carrier with nonempty \(Y_3\) caps and
  exact endpoints, but the full shifted-list conclusion is not proved.
  The symbolic control in Section 5.1 refutes the earlier proof-method
  inference.

### Static-defect-survival gate

- Equality has not been proved to make every original defect survive.
- Survival is no longer needed for the order floor: a surviving witness
  is a new vertex inside \(J\), while a repaired witness is a new vertex
  outside \(J\).
- Together with the contamination-cycle buffers, this improves C-125's
  clean bound from \(2k+6\) (or conditionally \(2k+8\)) to the
  unconditional \(2k+9\) bound for \(k\geq5\).
- The only endpoint collision preventing \(2k+10\) is a common repaired
  endpoint defect outside \(J\).

These are pattern theorems.  They do not establish a global
counterexample-order frontier because an arbitrary counterexample has not
been shown to contain an exact static \(Y_k\).
