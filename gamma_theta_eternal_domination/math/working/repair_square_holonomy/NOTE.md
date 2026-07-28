# Fixed-pivot repair iteration and its exact holonomy boundary

## Status and scope

Date: 2026-07-28 (PDT)

This note assumes

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3
\tag{0.1}
\]

and writes \(\mathcal K\) for the literal greatest eternal family of
dominating triples in the standard one-guard-moves model.  The notation

\[
 u\mathrel{\triangleright}x
\tag{0.2}
\]

has its accepted C-108 meaning: a guard at \(u\) can answer an attack at
\(x\) from one, equivalently every, maximum independent triple containing
\(u\), with the successor retained in \(\mathcal K\).

The accepted C-145 repair-square theorem is the starting dependency.  This
note does not re-prove that theorem.  It proves a new finite-iteration
consequence:

> A one-sided active edge separates its endpoints in the complement link of
> every common nonneighbor.  In the two resulting bipartite link components,
> all synchronized repair iterations have an exact checkerboard
> orientation.

It also proves that the omitted-corner deletion rank is conserved when the
repair square flips to the opposite asymmetric edge.  Hence neither a
directed repair-cycle argument nor deletion-rank monotonicity closes the
remaining reciprocity gap.  The exact order-15 control
`NslalntvXzn^{~n||^w` attains the sharp rank change \(1\to3\) between two
reverse endpoints of the same active orientation.  That graph has
\(\gamma=2\), so it is a boundary control, not a counterexample to (0.1).

Nothing here proves complete \(k=3\), the gamma--theta conjecture, or
greatest-family reciprocity.

## 1. Dependencies and notation

Put

\[
 H=\overline G.
\tag{1.1}
\]

For \(w\in V(G)\), its **complement link** is

\[
 L_w=H[N_H(w)].
\tag{1.2}
\]

Thus an edge \(ab\) of \(L_w\) is exactly a maximum independent triple
\(\{w,a,b\}\) of \(G\).

We use the following accepted inputs.

1. C-010: every maximum independent triple belongs to every eternal
   triple-family.
2. C-051: the independent antineighborhood of one vertex in an equality
   graph has equality parameter two.
3. The accepted \(\alpha=2\) theorem: equality parameter two forces clique
   cover number two.
4. C-108: activity of a fixed physical responder is independent of the
   maximum independent triple containing it.
5. C-143: every complementary reverse endpoint of an active edge
   dominates.
6. C-145: a one-sided active edge and two independent completions over a
   common nonneighbor produce the five-state repair square and the
   opposite one-sided active edge.
7. C-146: finite deletion rank is Lipschitz within one fixed vertex star.

For a triple \(D\), write \(\rho(D)=0\) when \(D\) is non-dominating,
\(\rho(D)=h\) when it is deleted in round \(h\) of the descending greatest
kernel, and \(\rho(D)=\infty\) when \(D\in\mathcal K\).

### Lemma 1.1 (the physical link is bipartite and isolate-free) — PROVED

For every \(w\), the graph \(L_w\) is bipartite and has no isolated
vertices.

#### Proof

Apply C-051 to the independent singleton \(\{w\}\).  The projected graph

\[
 Q=G-N_G[w]=G[N_H(w)]
\tag{1.3}
\]

satisfies

\[
 \gamma(Q)=\alpha(Q)=\gamma^\infty(Q)=2.
\tag{1.4}
\]

The accepted \(\alpha=2\) theorem gives \(\theta(Q)=2\).  Since
\(\overline Q=L_w\), the link is bipartite.

Now take \(v\in N_H(w)\).  The pair \(\{w,v\}\) is independent in \(G\).
Because \(i(G)=\alpha(G)=3\), it extends to an independent triple
\(\{w,v,t\}\).  Equivalently, \(vt\in E(L_w)\).  Thus \(v\) is not
isolated. \(\square\)

## 2. Fixed-pivot component separation

Assume

\[
 u\mathrel{\triangleright}x,
 \qquad
 x\not\mathrel{\triangleright}u.
\tag{2.1}
\]

The pair \(\{u,x\}\) does not dominate, because \(\gamma(G)=3\).  Hence

\[
 W=N_H(u)\cap N_H(x)\ne\varnothing.
\tag{2.2}
\]

Fix an arbitrary \(w\in W\).  Both \(u\) and \(x\) are vertices of
\(L_w\), while \(ux\notin E(H)\) because activity requires
\(ux\in E(G)\).

### Theorem 2.1 (fixed-pivot component separation) — PROVED

The vertices \(u\) and \(x\) lie in distinct connected components of
\(L_w\).

#### Proof

Suppose instead that

\[
 v_0=u,v_1,\ldots,v_d=x
\tag{2.3}
\]

is a path in \(L_w\).  Since \(ux\notin E(H)\), one has \(d\ge2\).

If \(d=2\), then both

\[
 \{u,w,v_1\},\qquad \{x,w,v_1\}
\tag{2.4}
\]

are maximum independent triples and hence retained.  From the second
state, an attack at \(u\) can only move the guard at \(x\): the other two
guards are \(H\)-adjacent, and therefore \(G\)-nonadjacent, to \(u\).
The successor is the first state.  Thus
\(x\mathrel{\triangleright}u\), contrary to (2.1).

If \(d\ge3\), use the two endpoint edges of (2.3) as the C-145
completions:

\[
 S=\{u,w,v_1\},
 \qquad
 T=\{x,w,v_{d-1}\}.
\tag{2.5}
\]

C-145 produces the opposite one-sided active edge

\[
 v_{d-1}\mathrel{\triangleright}v_1,
 \qquad
 v_1\not\mathrel{\triangleright}v_{d-1}.
\tag{2.6}
\]

The subpath

\[
 v_1,v_2,\ldots,v_{d-1}
\tag{2.7}
\]

has length \(d-2\) in the same link.  Repeating the argument decreases
the displayed path length by two.  It eventually reaches length two,
which was just excluded, or length one.  Length one is also impossible:
an active orientation requires a \(G\)-edge, whereas a link edge is an
\(H\)-edge.  This contradiction proves the theorem. \(\square\)

The proof is a genuinely finite repair iteration.  No compactness,
limiting family, or assumed path-independence is used.

### Corollary 2.2 (connected-link reciprocity test) — PROVED

If \(u,x\) have a common \(H\)-neighbor \(w\) for which \(L_w\) connects
\(u\) to \(x\), then

\[
 u\mathrel{\triangleright}x
 \quad\Longrightarrow\quad
 x\mathrel{\triangleright}u.
\tag{2.8}
\]

In particular, if every complement link \(L_w\) is connected, the active
relation is symmetric.

This is only a reciprocity test.  Active-edge symmetry by itself is not
the missing global three-coloring theorem.

## 3. Checkerboard propagation across the separated components

Let \(C\) and \(D\) be the components of \(L_w\) containing \(u\) and
\(x\), respectively.  By Theorem 2.1, \(C\ne D\).  By Lemma 1.1 choose
bipartitions

\[
 C=C_0\mathbin{\dot\cup}C_1,\qquad
 D=D_0\mathbin{\dot\cup}D_1,
\qquad
 u\in C_0,\quad x\in D_0.
\tag{3.1}
\]

### Lemma 3.1 (synchronized-walk repair law) — PROVED

Let

\[
 u=u_0,u_1,\ldots,u_\ell
\quad\text{and}\quad
 x=x_0,x_1,\ldots,x_\ell
\tag{3.2}
\]

be walks of the same length in \(C\) and \(D\).  Then

\[
\begin{array}{ll}
 \ell\text{ even}:&
 u_\ell\mathrel{\triangleright}x_\ell,\quad
 x_\ell\not\mathrel{\triangleright}u_\ell,\\[1mm]
 \ell\text{ odd}:&
 x_\ell\mathrel{\triangleright}u_\ell,\quad
 u_\ell\not\mathrel{\triangleright}x_\ell.
\end{array}
\tag{3.3}
\]

#### Proof

For one step, the independent completions

\[
 \{u_0,w,u_1\},
 \qquad
 \{x_0,w,x_1\}
\tag{3.4}
\]

and C-145 turn
\(u_0\mathrel{\triangleright}x_0\) into
\(x_1\mathrel{\triangleright}u_1\), with the reverse orientation absent.
Apply the same argument repeatedly.  Each repair swaps the order of the
two endpoint walks, giving exactly the parity rule (3.3).  The endpoints
always lie in distinct link components, so they are distinct and joined
in \(G\), as required. \(\square\)

### Theorem 3.2 (componentwise checkerboard orientation) — PROVED

For all \(c_i\in C_i\) and \(d_i\in D_i\),

\[
\boxed{
\begin{array}{lll}
 c_0\mathrel{\triangleright}d_0,
 &\qquad&
 d_0\not\mathrel{\triangleright}c_0,\\[1mm]
 d_1\mathrel{\triangleright}c_1,
 &&
 c_1\not\mathrel{\triangleright}d_1.
\end{array}}
\tag{3.5}
\]

#### Proof

Choose paths from \(u\) to \(c_i\) in \(C\) and from \(x\) to \(d_i\) in
\(D\).  Their lengths have the same parity \(i\).  Lemma 1.1 gives an
edge in each component, so the shorter path can be padded by two-step
backtracks until the two lengths agree.  Lemma 3.1 now gives (3.5).
\(\square\)

Thus one asymmetric edge does not merely create one opposite asymmetric
edge.  It polarizes two entire link components.  This is the strongest
fixed-pivot conclusion available from finite repair iteration.

## 4. Why finite repair cycles do not contradict C-064

Take any neighbors

\[
 a\in N_{L_w}(u),\qquad z\in N_{L_w}(x).
\tag{4.1}
\]

C-145 gives

\[
 u\mathrel{\triangleright}x
 \longmapsto
 z\mathrel{\triangleright}a.
\tag{4.2}
\]

For the new orientation, use the same pivot \(w\) and the backtracking
neighbors

\[
 x\in N_{L_w}(z),\qquad u\in N_{L_w}(a).
\tag{4.3}
\]

The next repair gives

\[
 z\mathrel{\triangleright}a
 \longmapsto
 u\mathrel{\triangleright}x.
\tag{4.4}
\]

Hence the repair operation always has a literal two-step return.  This is
a cycle in the space of oriented pairs, not a directed two-cycle
\(u\leftrightarrow x\) in the active relation.

C-064 gives no contradiction from the displayed fixed-pivot data alone.
The mixed repair states contain
the \(G\)-edges \(xa\), \(uz\), \(ux\), or \(az\), so the repair square is
not a loop of independent ridge states.  C-064 applies only along
independent ridge paths.  Within one component of \(L_w\), such paths
transport response incidence consistently; there is no ridge path from
\(C\) to \(D\) among the independent facets containing \(w\).  On the
immediate backtrack, the canonical transpositions cancel.  More generally,
C-064 requires the permutation of a closed ridge path to preserve response
incidence, not to be the identity.

Thus no contradiction follows by applying C-064 to the local repair cycle.
It remains **OPEN** whether a global independent ridge path that leaves the
star of \(w\), together with the full \(\gamma=3\) condition, supplies a new
constraint.  A future holonomy argument would have to specify and prove
such a coupling between distinct link components.

## 5. Corner-rank conservation

Retain the completions (4.1), and write the C-145 states as

\[
\begin{array}{lll}
 S=\{u,w,a\},&
 T=\{x,w,z\},&
 O=\{u,w,z\}.
\end{array}
\tag{5.1}
\]

The state \(O\) is the omitted reverse endpoint for the original
orientation:

\[
 O=T-x+u.
\tag{5.2}
\]

The opposite orientation is

\[
 z\mathrel{\triangleright}a,
\qquad
 a\not\mathrel{\triangleright}z,
\tag{5.3}
\]

and the very same state is its omitted reverse endpoint:

\[
 O=S-a+z.
\tag{5.4}
\]

### Theorem 5.1 (repair preserves the tracked corner rank) — PROVED

The rank \(\rho(O)\) is positive and finite, and it is exactly the same
reverse-endpoint rank for both asymmetric orientations (2.1) and (5.3).

If \(J\) is any maximum independent triple containing \(x\), and

\[
 B_J=J-x+u,
\tag{5.5}
\]

then

\[
 \boxed{
 |\rho(B_J)-\rho(O)|
 \le |J-T|
 \le2.
 }
\tag{5.6}
\]

#### Proof

C-143 says that \(O\) dominates.  C-108 and either inactive reverse
orientation in (2.1) or (5.3) say that \(O\notin\mathcal K\).  Thus its
rank is positive and finite.  Equations (5.2) and (5.4) prove literal
rank conservation: there is only one state \(O\), not two states whose
ranks must be compared.

For (5.6), apply the C-146 star-Lipschitz theorem to the independent
triples \(J,T\), with fixed responder \(x\) and fixed target \(u\).
Both triples contain \(x\), so they differ in at most their other two
vertices. \(\square\)

This theorem rules out rank monotonicity as an automatic repair invariant.
The tracked corner rank is conserved around (4.2)--(4.4), while changing
the independent endpoint of one fixed orientation can move the rank up or
down by two.

## 6. Exact sharp boundary

The standalone graph checker in this directory verifies the graph

```text
NslalntvXzn^{~n||^w
```

without importing the search encoder.  It recomputes

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(2,3,3,3,3),
\tag{6.1}
\]

the 285-state greatest triple family, and the following named data:

\[
\begin{gathered}
 u=0,\quad x=1,\quad w=10,\quad a=6,\quad z=13,\\
 L_w=H[\{0,1,6,13\}]=2K_2
 \quad\text{with components }\{0,6\},\{1,13\},\\
 0\mathrel{\triangleright}1,\quad
 1\not\mathrel{\triangleright}0,\quad
 13\mathrel{\triangleright}6,\quad
 6\not\mathrel{\triangleright}13.
\end{gathered}
\tag{6.2}
\]

The canonical QQ1 reverse endpoint

\[
 \{0,2,3\}
\tag{6.3}
\]

has rank one.  The repaired corner

\[
 O=\{0,10,13\}
\tag{6.4}
\]

has rank three.  It is simultaneously the reverse endpoint

\[
 \{1,10,13\}-1+0
 =
 \{0,6,10\}-6+13.
\tag{6.5}
\]

Thus the upper bound two in (5.6) is attained, and the repair iteration
returns after two steps while preserving the rank-three corner.

This graph also has 23 dominating pairs.  It therefore fails the full
\(\gamma=3\) hypothesis even though the selected pair \(\{u,x\}\) itself
does not dominate.  It proves only the following sharp boundary:

\[
\boxed{
\begin{array}{c}
\alpha=\gamma^\infty=3,\ \{u,x\}\text{ non-dominating, C-064, and the}\\
\text{literal greatest family do not force repair-rank descent.}\\
\text{Any further contradiction must use global }\gamma=3
\text{ beyond the selected pair.}
\end{array}}
\tag{6.6}
\]

Separately, `verify_abstract.py` exhausts every labeled isolate-free
bipartite link graph through order six.  Across 66,968 oriented nonedge
roots it independently checks the repair closure used in Theorems 2.1 and
3.2: all 60,044 same-component roots become inconsistent, while all 6,924
separated-component roots remain consistent and contain every forced
checkerboard orientation.  This is a finite bookkeeping audit, not the
all-order proof; the proof is the path induction in Sections 2--3.

Global \(\gamma=3\) still does not force link connectivity.  The exact
equality graph \(G=\overline{L(K_{3,3})}\) has

\[
 \gamma=i=\alpha=\gamma^\infty=\theta=3,
\tag{6.7}
\]

while every vertex link in \(H=L(K_{3,3})\) is \(2K_2\).  That graph has
no claimed asymmetric active edge; it is only the sharp reason that
Theorem 2.1 cannot be finished by asserting that equality links are
connected.

## 7. Exact remaining gate

The fixed-pivot iteration is now complete:

1. a same-component path gives a finite contradiction;
2. distinct components acquire the checkerboard orientation (3.5);
3. repair has an unavoidable two-step return;
4. C-064 does not couple the separated components from the displayed
   fixed-pivot data alone; a global path leaving the star remains open; and
5. deletion rank is conserved on the tracked omitted corner and can rise
   by the sharp C-146 allowance when the endpoint triple changes.

The next genuinely new step must therefore use the global common-neighbor
condition

\[
 \gamma(G)=3
\quad\Longleftrightarrow\quad
 \text{every vertex pair of }H\text{ has a common }H\text{-neighbor}
\tag{7.1}
\]

to couple the different components of \(L_w\), or show that the
checkerboard polarization forces a dominating pair.  Re-running the
fixed-pivot repair square, invoking C-064 alone, or minimizing the same
corner rank cannot supply that step.
