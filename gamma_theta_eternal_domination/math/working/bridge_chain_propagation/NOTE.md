# The anchor-only bridge is side-pure and turns at its next forced ridge

## Status and exact scope

Date: 2026-07-28 (PDT)

All statements use the standard one-guard-moves eternal-domination model:
attacks are made only at unoccupied vertices, exactly one adjacent guard
moves, and every retained successor remains in the specified eternal
family.

This note continues the hostile-passed C-129 first-cross-clause theorem and
the hostile-passed anchor-only bridge theorem.  Let

\[
 S=\{u,v,w\}\in\mathcal F
\]

be independent.  In the odd--odd first-clause geometry, the terminal
singletons and clause ports satisfy

\[
 L(s)=\{v\},\quad L(x)=\{v,w\},\quad
 L(y)=\{u,w\},\quad L(t)=\{u\}.
\tag{0.1}
\]

The port \(x\) and marker \(s\) lie in a free component \(K\) of the
frozen-\(u\) complement projection, at odd distance.  Similarly \(y,t\)
lie at odd distance in a free component \(M\) of the frozen-\(v\)
projection.  In the simultaneous anchor-only defect case, the accepted
bridge theorem supplies

\[
 W=N_{\overline G}(s)\cap N_{\overline G}(t)\ne\varnothing,
\tag{0.2}
\]

with every \(\{s,t,z\}\), \(z\in W\), retained and

\[
 L(z)\in\bigl\{\{w\},\{u,w\},\{v,w\}\bigr\}.
\tag{0.3}
\]

The new conclusions are:

1. **PROVED: bridge-side purity.**  Every bridge vertex is forced to the
   shared color \(w\) by the two selected unit orientations.  If the
   bipartition sides containing \(s,t\) are \(K_0,M_0\), then
   \[
   N_{\overline G}(z)\cap K\subseteq K_0,\qquad
   N_{\overline G}(z)\cap M\subseteq M_0
   \quad(z\in W).
   \tag{0.4}
   \]
   In particular every bridge vertex is adjacent in \(G\) to both original
   ports \(x,y\).
2. **PROVED: an active next clause cannot return to an original
   component.**  If \(L(z)=\{u,w\}\), then a complement edge from \(z\)
   to a type-\(u\) port \(r\), \(L(r)=\{v,w\}\), can carry the active
   collision color \(w\).  If \(r\in K\), however, (0.4) puts \(r\) on
   the \(v\)-colored marker side, so the clause is already satisfied.
   A genuinely new propagated unit must enter a different free component
   of the frozen-\(u\) projection.  The reflected statement holds for a
   \(\{v,w\}\)-bridge and \(M\).
3. **PROVED: two-list bridges force a turning ridge.**  For
   \(L(z)=\{u,w\}\), put
   \[
   R_z=N_{\overline G}(w)\cap N_{\overline G}(z).
   \tag{0.5}
   \]
   Either \(R_z=\varnothing\), in which case \(\{w,z\}\) is a dominating
   pair, or \(R_z\) is a \(G\)-clique with every state
   \(\{w,z,q\}\), \(q\in R_z\), retained and all ridge exchanges forced.
   The only possible anchor is \(v\), and every outside member has exact
   list
   \[
   L(q)=\{v\}\quad\text{or}\quad L(q)=\{u,v\}.
   \tag{0.6}
   \]
   Under \(\gamma(G)=3\), the dominating-pair alternative is impossible,
   so the ridge is nonempty.  The \(\{v,w\}\)-bridge statement is obtained
   by exchanging \(u,v\).
4. **EXACT SHARPNESS CONTROLS.**  Equality graphs `FCXfO` and `HEhbtjK`
   realize the two external alternatives in (0.6), respectively.  Both
   have
   \[
   (\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3).
   \]

The forced ridge does not continue the active shared-\(w\) implication.
For a singleton \(q\), the endpoint lists are disjoint.  For
\(L(q)=\{u,v\}\), the edge \(zq\) is a collision clause in color \(u\),
but the bridge orientation assigns \(z=w\), so that clause is inactive.

This is a propagation gate, not an exclusion of the first clause.  An
active shared-\(w\) clause may still leave a two-list bridge for a fresh
projection component.  No arbitrary unit-chain, lollipop, bicycle,
complete \(k=3\) theorem, or universal gamma--theta resolution is claimed.

No literature-priority claim is made.

## 1. Frozen-component notation

Put \(H=\overline G\).  Write the bipartitions of the two supporting
components as

\[
 K=K_0\mathbin{\dot\cup}K_1,\qquad
 M=M_0\mathbin{\dot\cup}M_1,
\tag{1.1}
\]

where

\[
 s\in K_0,\qquad t\in M_0.
\tag{1.2}
\]

The support paths from \(s\) to \(x\) and from \(t\) to \(y\) are odd, so

\[
 x\in K_1,\qquad y\in M_1.
\tag{1.3}
\]

Accepted free-component polarization gives the selected local colors

\[
\begin{array}{c|cc}
 &0\text{-side}&1\text{-side}\\ \hline
K&v&w\\
M&u&w.
\end{array}
\tag{1.4}
\]

These are component orientations forced by the singleton markers.  They
do not presuppose that the entire response 2-CNF is colorable.

The accepted bridge-location theorem gives

\[
\begin{aligned}
 W_w&=\{z\in W:L(z)=\{w\}\}\subseteq K\cap M,\\
 W_{uw}&=\{z\in W:L(z)=\{u,w\}\}\subseteq M-K,\\
 W_{vw}&=\{z\in W:L(z)=\{v,w\}\}\subseteq K-M.
\end{aligned}
\tag{1.5}
\]

Because every bridge vertex is adjacent in \(H\) to both \(s\) and \(t\),
equations (1.4)--(1.5) show:

- a vertex of \(W_w\) lies in \(K_1\cap M_1\);
- a vertex of \(W_{uw}\) lies in \(M_1\); and
- a vertex of \(W_{vw}\) lies in \(K_1\).

Thus every bridge vertex receives the shared color \(w\) wherever its
list and component membership make a local orientation choice.

## 2. The bridge sees only marker sides in the complement

### Theorem 2.1 (bridge-side purity)

For every \(z\in W\),

\[
 \boxed{
 N_H(z)\cap K\subseteq K_0,\qquad
 N_H(z)\cap M\subseteq M_0.
 }
\tag{2.1}
\]

Consequently

\[
 zq\in E(G)
 \quad
 \bigl(z\in W,\ q\in(K_1\cup M_1)-\{z\}\bigr).
\tag{2.2}
\]

In particular,

\[
 zx,zy\in E(G)\qquad(z\in W).
\tag{2.3}
\]

#### Proof

Apply the accepted C-079 side-purity theorem with:

\[
 a=u,\qquad p=t,\qquad q=z,
\]

and with the \(u\)-omitting component \(K\).  The positive-response
hypothesis holds because \(u\in L(t)\), and the required physical edge is

\[
 tz\in E(H)
\]

from the definition of \(W\).  Hence all complement neighbors of \(z\)
inside \(K\) lie on one bipartition side.  But

\[
 sz\in E(H),\qquad s\in K_0,
\]

so that one side must be \(K_0\).

The reflected application uses

\[
 a=v,\qquad p=s,\qquad q=z,
\]

and the component \(M\).  Here \(v\in L(s)\) and \(sz\in E(H)\), while
\(tz\in E(H)\) identifies the permitted side as \(M_0\).  This proves
(2.1).  For every distinct \(q\in K_1\cup M_1\), the complement of
(2.1) gives (2.2).

It remains to check that a bridge vertex cannot itself be one of the two
ports before applying (2.2).  If \(z=x\), then the literal clause edge
\(xy\in E(H)\) makes \(y\in N_H(z)\cap M_1\), contradicting the
\(M\)-side assertion in (2.1).  Symmetrically, if \(z=y\), then
\(x\in N_H(z)\cap K_1\), contradicting the \(K\)-side assertion.  Thus
\(z\ne x,y\), and (1.3) together with (2.2) gives (2.3). \(\square\)

No family omission was converted into a graph nonedge.  Every edge used to
invoke side-purity is a literal edge of \(H\).

### Corollary 2.2 (where an active next clause can go)

Let \(z\in W_{uw}\), and suppose

\[
 zr\in E(H),\qquad L(r)=\{v,w\}.
\tag{2.4}
\]

The edge \(zr\) is a cross-type response clause whose only collision color
is \(w\).  If \(r\in K\), then \(r\in K_0\), and the orientation forced by
\(s\) assigns

\[
 z=w,\qquad r=v.
\tag{2.5}
\]

Thus the clause is already satisfied.  Any occurrence of (2.4) that
propagates the forced bridge literal into a genuinely new Boolean variable
uses a free component of the frozen-\(u\) projection different from \(K\).

The symmetric statement holds for \(z\in W_{vw}\), a type-\(v\) port
\(r\) with list \(\{u,w\}\), and the original component \(M\).

#### Proof

Theorem 2.1 puts every \(H\)-neighbor of \(z\) in \(K\) on \(K_0\).
Equation (1.4) gives (2.5).  Exact-two vertices belong to free components
of their omitted-color projections, by the accepted anchor-fixed
certificate theorem, so an endpoint outside \(K\) really does use a
different free component. \(\square\)

This is the exact sense in which the bridge cannot simply feed the same
false shared-color collision back through either original unit component.
It does not prohibit a separated-port continuation through a fresh
component.

## 3. A two-list bridge has its own retained defect ridge

The next lemma does not require the whole first-clause geometry.  It is
stated separately so that its hypotheses are explicit.

### Theorem 3.1 (turning ridge or dominating pair)

Assume

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3,
\]

every outside response list is nonempty and proper, and

\[
 L(z)=\{u,w\}.
\tag{3.1}
\]

Put

\[
 R_z=N_H(w)\cap N_H(z).
\tag{3.2}
\]

Then \(R_z\ne\varnothing\).  More precisely:

1. \(G[R_z]\) is a clique;
2. for every \(q\in R_z\),
   \[
   \{w,z,q\}\in\mathcal F;
   \tag{3.3}
   \]
3. for distinct \(q,q'\in R_z\), the attack at \(q'\) from
   \(\{w,z,q\}\) uniquely moves \(q\to q'\);
4. the only possible anchor in \(R_z\) is \(v\); and
5. every \(q\in R_z-S\) has
   \[
   L(q)=\{v\}\quad\text{or}\quad L(q)=\{u,v\}.
   \tag{3.4}
   \]

Without the assumption \(\gamma(G)=3\), the exact alternative is:

\[
 R_z=\varnothing
 \quad\Longleftrightarrow\quad
 \{w,z\}\text{ dominates }G.
\tag{3.5}
\]

For \(L(z)=\{v,w\}\), interchange \(u,v\): the only possible anchor is
\(u\), and every outside ridge list is \(\{u\}\) or \(\{u,v\}\).

#### Proof

Equation (3.5) is the definition of domination in complement language.
Since \(\gamma(G)=3\), the pair \(\{w,z\}\) cannot dominate, proving
nonemptiness.

The direct response \(u\in L(z)\) retains

\[
 S-u+z=\{v,w,z\}\in\mathcal F.
\tag{3.6}
\]

The anchor \(v\), if it belongs to \(R_z\), already gives (3.3) through
(3.6).  No other anchor can lie in the ridge: \(w\) is excluded by the
open neighborhood, while \(uz\in E(G)\) follows from \(u\in L(z)\).

Now take \(q\in R_z-\{v\}\).  It is outside \(S\).  Attack the unoccupied
vertex \(q\) from (3.6).  The guards at \(w,z\) cannot move because

\[
 wq,zq\in E(H).
\]

Eternal closure therefore forces the only remaining guard:

\[
 v\longrightarrow q,\qquad
 \{w,z,q\}\in\mathcal F.
\tag{3.7}
\]

Apply arbitrary-state restoration to (3.7).  Relative to \(S\), the
missing anchors are \(u,v\).  The list \(L(z)=\{u,w\}\) restores \(u\),
so \(v\in L(q)\).  The literal edge \(wq\in E(H)\) gives
\(w\notin L(q)\).  A nonempty proper subset of \(S\) with these two
properties is exactly one of the lists in (3.4).

Finally take distinct \(q,q'\in R_z\).  The retained state
\(\{w,z,q\}\) must dominate \(q'\).  Both \(w,z\) miss \(q'\), so
\(qq'\in E(G)\).  At an attack on \(q'\), the first two guards still
have no move edge, hence \(q\to q'\) is the unique response.  This proves
the clique and exchange assertions. \(\square\)

### Corollary 3.2 (the forced ridge turns the collision color)

Let \(z\in W_{uw}\).  Its unit orientation is \(z=w\).
For an outside \(q\in R_z\):

- if \(L(q)=\{v\}\), the lists of \(z,q\) are disjoint; and
- if \(L(q)=\{u,v\}\), the complement edge \(zq\) has collision color
  \(u\), not \(w\).

Thus every gamma-forced edge from \(z\) into its turning ridge is safe
under the selected bridge orientation.  It does not itself constitute the
active next shared-\(w\) clause.

## 4. Exact equality controls

The theorem permits both external list alternatives in (3.4), even under
full parameter equality.

### 4.1 External singleton

For

```text
FCXfO
```

the greatest eternal family has 18 triples.  At

\[
 S=\{0,1,2\},\qquad (u,v,w,z,q)=(1,0,2,4,3),
\]

one has

\[
 L(z)=\{1,2\},\qquad L(q)=\{0\},
\]

and

\[
 N_H(2)\cap N_H(4)=\{0,3\}.
\]

### 4.2 External exact two-list

For

```text
HEhbtjK
```

the greatest eternal family has 48 triples.  At

\[
 S=\{0,1,2\},\qquad (u,v,w,z,q)=(1,0,2,5,3),
\]

one has

\[
 L(z)=\{1,2\},\qquad L(q)=\{0,1\},
\]

and again

\[
 N_H(2)\cap N_H(z)=\{0,3\}.
\]

The standalone verifier checks all graph parameters, every unoccupied
attack obligation, the exact response lists, the full two-vertex ridge,
and both directed ridge exchanges.  In both controls,

\[
 \boxed{(\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3).}
\]

These controls establish sharpness only for Theorem 3.1.  They are
colorable equality graphs and do not claim to realize the full C-129
anchor-only first-clause geometry.

## 5. Remaining gap

The simultaneous anchor-only escape is now constrained as follows.

1. Its entire bridge ridge carries the shared color \(w\).
2. Every bridge vertex is \(G\)-adjacent to every distinct vertex of the
   two original opposite/unit-port sides, and in particular to both
   original ports.
3. An active next shared-\(w\) clause cannot return through either original
   component; it must enter a fresh free component.
4. Every two-list bridge has a nonempty retained turning ridge, but every
   forced turning edge is inactive under the bridge orientation.

The unresolved case is therefore a genuinely separated continuation:
an active clause from a two-list bridge into a fresh component, followed
by a connector to another physical port.  Proving that such fresh
continuations cannot form a finite lollipop/bicycle, or that one creates a
dominating pair, remains open.
