# Disjoint second-layer witnesses at a full response

## Status and scope

Date: 2026-07-27 (PDT)

This note strengthens the static five-vertex witness bound in
`math/working/full_response_witness_bound/NOTE.md` by using one literal
one-guard closure obligation.  It is a conditional theorem about a full
response at an independent family state.  It is not a global
counterexample-order exclusion.

Throughout, \(H=\overline G\).

## 1. Setup

Let

\[
S=\{a,b,c\}
\]

be an independent member of an eternal dominating family \(\mathcal F\) of
three-vertex configurations.  Let \(x\notin S\) have a full response at
\(S\): \(x\) is adjacent in \(G\) to every member of \(S\), and

\[
D_i=(S-\{i\})\cup\{x\}\in\mathcal F
\qquad(i\in S).
\tag{1.1}
\]

Assume \(\gamma(G)\geq3\).  For each \(i\in S\), choose a witness

\[
u_i\in N_H(x)\cap N_H(i)
\tag{1.2}
\]

to the failure of the pair \(\{x,i\}\) to dominate.  Since every state
\(D_j\) dominates, the usual spoke argument gives

\[
N_H(u_i)\cap S=\{i\}.
\tag{1.3}
\]

In particular, \(u_a,u_b,u_c\) are distinct.

Define the nonempty second-layer witness sets

\[
Z_i=N_H(i)\cap N_H(u_i).
\tag{1.4}
\]

They are nonempty because the pair \(\{i,u_i\}\) does not dominate.
More generally, write

\[
A_i=N_H(x)\cap N_H(i),\qquad
Y_{i,p}=N_H(i)\cap N_H(p)\quad(p\in A_i).
\tag{1.5}
\]

Every \(A_i\) and \(Y_{i,p}\) is nonempty.  The chosen \(u_i\) belongs to
\(A_i\), and \(Z_i=Y_{i,u_i}\).

## 2. Disjointness theorem

### Theorem 2.1

For distinct \(i,j\in S\), every \(p\in A_i\), and every \(q\in A_j\),

\[
Y_{i,p}\cap Y_{j,q}=\varnothing.
\tag{2.1}
\]

In particular, \(Z_a,Z_b,Z_c\) are pairwise disjoint.

#### Proof

Suppose instead that \(z\in Y_{i,p}\cap Y_{j,q}\), and write \(h\) for
the third member of \(S\).

First, \(z\notin\{x,j,h\}\).  Indeed, \(xi\in E(G)\), so
\(x\notin Y_{i,p}\).
The same argument as (1.3), applied to any \(p\in A_i\), gives
\(N_H(p)\cap S=\{i\}\).  Hence if \(z\in S\), that equality and the
absence of loops rule out \(z\in N_H(p)\cap N_H(i)\).  Thus \(z\) is an
unoccupied legal attack target at the family state

\[
D_i=\{x,j,h\}.
\]

There are only three possible responding guards.

1. The guard at \(j\) cannot move to \(z\), because
   \(z\in Y_{j,q}\subseteq N_H(j)\), so \(jz\notin E(G)\).
2. If the guard at \(h\) moves, the successor is \(\{x,j,z\}\).
   This set does not dominate \(q\), because

   \[
   q\in N_H(x)\cap N_H(j)\cap N_H(z).
   \]

3. If the guard at \(x\) moves, the successor is \(\{j,h,z\}\).
   This set does not dominate \(i\), because \(S\) is independent in
   \(G\) and \(z\in Y_{i,p}\subseteq N_H(i)\).

Consequently the attack at \(z\) has no legal response whose successor
dominates \(G\), contradicting the closure of \(\mathcal F\).  Hence the
sets are pairwise disjoint. \(\square\)

The proof allows arbitrary additional edges.  In particular, it never
turns absence of a family response into a graph nonedge.

## 3. Forced cross responses

The same attack has a useful positive form.

### Theorem 3.1

Fix \(j\in S\), \(q\in A_j\), and \(y\in Y_{j,q}\).  Then

\[
xy\in E(G),\qquad
N_H(y)\cap S=\{j\},
\tag{3.1}
\]

and, for each \(i\in S-\{j\}\),

\[
(S-\{i\})\cup\{y\}\in\mathcal F.
\tag{3.2}
\]

Thus the family-response list of \(y\) at \(S\) contains both colors in
\(S-\{j\}\), while the missing color \(j\) is a genuine graph nonedge.

#### Proof

Fix \(i\in S-\{j\}\), and let \(h\) be the third anchor.  Attack \(y\)
from \(D_i=\{x,j,h\}\).  The guard at \(j\) cannot move because
\(jy\in E(H)\).  Moving \(h\), if its edge to \(y\) exists in \(G\),
would leave \(\{x,j,y\}\), which misses \(q\).  Closure therefore
forces the guard at \(x\) to move.  Hence \(xy\in E(G)\),
\(\{j,h,y\}=(S-\{i\})\cup\{y\}\) belongs to \(\mathcal F\), and this
successor dominates.

In particular it dominates the omitted anchor \(i\).  Both \(j\) and \(h\)
are adjacent to \(i\) in \(H\), so necessarily \(iy\in E(G)\).  Applying
this argument to both choices of \(i\neq j\) proves (3.1) and (3.2).
\(\square\)

For chosen \(u_j\in A_j\) and \(z_j\in Y_{j,u_j}\), the vertices
\(\{j,u_j,z_j\}\) form a triangle in \(H\), whereas \(x\) is adjacent in
\(H\) to \(u_j\) and nonadjacent in \(H\) to \(j,z_j\).  This rigid
four-triangle skeleton is likely the useful normal
form for the remaining order-\(13\) full-response slice.

## 4. Counting consequence

Let

\[
Q_S=\{q\in V(G)-S:q\text{ is adjacent in }G\text{ to every member of }S\}.
\tag{3.1}
\]

As in the five-vertex witness proof, no \(u_i\) or member of \(Z_i\) lies
in \(S\cup Q_S\), and no member of any \(Z_i\) is one of
\(u_a,u_b,u_c\).  Choosing \(z_i\in Z_i\), Theorem 2.1 therefore gives six
distinct vertices

\[
u_a,u_b,u_c,z_a,z_b,z_c
\in V(G)-(S\cup Q_S).
\]

### Corollary 4.1 (six-vertex witness bound)

Under the setup of Section 1,

\[
\left|V(G)-(S\cup Q_S)\right|\geq6,
\qquad
|V(G)|\geq |Q_S|+9.
\tag{3.2}
\]

### Corollary 4.2 (exact separated-port floor)

In the exact nine-vertex separated-port core, the six outside core
vertices \(x,r,s,q,v_0,v_1\) are all members of \(Q_S\).  Therefore any
equality realization with a full response at \(x\) has

\[
|V(G)|\geq 6+9=15.
\tag{3.3}
\]

This supersedes the order-\(14\) floor obtained from the static
five-vertex bound for this exact pattern.  It does not exclude other
full-response patterns at order \(13\) or \(14\), and it does not raise the
campaign's global certified frontier.

## 5. Discovery provenance

Theorem 2.1 was read from the 14-clause cores of the `partition` and
`overlap` tight-pattern probes in
`math/working/order13_single_full_squeeze/`.  In the labels used there,
closure of the state \(\{1,2,3\}\) against attack \(7\) is impossible:
guard \(1\) cannot move; moving guard \(2\) leaves a state missed by spoke
\(5\); and moving guard \(3\) leaves a state missed by anchor \(0\).

The theorem and its corollaries above are human proofs.  The machine cores
are discovery provenance, not premises.
