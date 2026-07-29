# A supported asymmetric edge forces a polarized bow tie

## Status and scope

Date: 2026-07-28 (PDT)

Assume

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3
\tag{0.1}
\]

and let \(\mathcal F\) be any eternal family of dominating triples.
This note couples the accepted adjacent-pair dichotomy (C-172) and the
hostile-passed supported-pair fan theorem to a one-sided active edge.

The result is a size-independent normal form.  Every common
nonneighbor of a supported asymmetric edge carries a complete
two-sided bow tie.  One side has omitted central fans, the other has
retained central fans, and every cross edge has a retained central fan.
Applied to canonical QQ1, this structure is forced at every
\(\{u,x\}\)-witness and is coupled exactly to every C-167 hot bridge.

The result does **not** eliminate QQ1, prove symmetry of the activity
relation, complete parameter three, or resolve the gamma--theta
conjecture.  No family omission is interpreted as a graph nonedge.

## 1. Definitions

For distinct vertices \(a,b\), write

\[
 W_{ab}=\{z\notin\{a,b\}:az,bz\notin E(G)\}.
\tag{1.1}
\]

For an edge \(ab\), write

\[
 a\mathrel{\triangleright_{\mathcal F}}b
\tag{1.2}
\]

when an independent triple in \(\mathcal F\), containing \(a\) and
not \(b\), has the retained response obtained by moving \(a\to b\).
Accepted C-108 makes this independent of the chosen independent source
containing \(a\).

Call an edge \(ab\) **supported** when some state of \(\mathcal F\)
contains both \(a,b\).  By the supported-pair fan theorem, a supported
pair has

\[
 \{a,b,z\}\in\mathcal F\qquad(z\in W_{ab}),
\tag{1.3}
\]

and \(W_{ab}\) is a \(G\)-clique.

## 2. Polarized bow-tie theorem

### Theorem 2.1 (supported asymmetric-edge bow tie) — PROVED CANDIDATE

Suppose \(ux\in E(G)\), the pair \(u,x\) is supported, and

\[
 u\mathrel{\triangleright_{\mathcal F}}x,
 \qquad
 x\not\mathrel{\triangleright_{\mathcal F}}u.
\tag{2.1}
\]

For every

\[
 z\in Z:=W_{ux},
\tag{2.2}
\]

put

\[
 P_z=W_{uz},\qquad Q_z=W_{xz}.
\tag{2.3}
\]

Then the following all hold.

1. \(Z,P_z,Q_z\) are nonempty \(G\)-cliques,
   \(P_z\cap Q_z=\varnothing\), and
   \[
     P_z\cup Q_z\text{ is a }G\text{-clique}.
   \tag{2.4}
   \]
2. For every \(g\in P_z\) and \(h\in Q_z\), the graph has the edges
   \[
     xg,\quad uh,\quad gh,
   \tag{2.5}
   \]
   and the family contains
   \[
   \begin{aligned}
     R_z&=\{u,x,z\},&
     S_g&=\{u,z,g\},&
     T_h&=\{x,z,h\},\\
     X_g&=\{x,z,g\},&
     M_{g,h}&=\{z,g,h\}.
   \end{aligned}
   \tag{2.6}
   \]
   Here \(S_g,T_h\) are maximum independent triples.
3. The opposite central state
   \[
     O_h=\{u,z,h\}
   \tag{2.7}
   \]
   is omitted.  More strongly, the entire central fan of the spoke
   \(uh\) is omitted:
   \[
     \{u,h,e\}\notin\mathcal F
     \qquad(e\in W_{uh}).
   \tag{2.8}
   \]
4. Every spoke on either side is reciprocal:
   \[
     u\leftrightarrow_{\mathcal F}h,
     \qquad
     x\leftrightarrow_{\mathcal F}g.
   \tag{2.9}
   \]
5. The edges \(xg\) and \(gh\) lie in the retained-fan branch:
   \[
   \begin{array}{ll}
     \{x,g,e\}\in\mathcal F &(e\in W_{xg}),\\
     \{g,h,e\}\in\mathcal F &(e\in W_{gh}),
   \end{array}
   \tag{2.10}
   \]
   and both \(W_{xg}\) and \(W_{gh}\) are \(G\)-cliques.

Thus a supported one-sided edge cannot be repaired by an unstructured
sequence of fresh witnesses.  Every \(z\in W_{ux}\) forces the
polarized pattern

\[
\boxed{
\begin{array}{c}
 \text{\(uh\): omitted fan and reciprocal}\\
 \text{\(xg\): retained fan and reciprocal}\\
 \text{\(gh\): retained fan}
\end{array}
\qquad(g\in P_z,\ h\in Q_z).}
\tag{2.11}
\]

#### Proof

Because \(\gamma(G)=3\), no pair dominates, so \(Z,P_z,Q_z\) are
nonempty.  The supported-pair theorem applied to \(u,x\) gives
\(R_z\in\mathcal F\) for every \(z\in Z\), and makes \(Z\) a clique.
The sets \(P_z,Q_z\) are cliques because \(\alpha(G)=3\): two
nonadjacent members of either set, together with its defining
independent pair, would form an independent four-set.

The retained state \(R_z\) dominates every \(g\in P_z\).  Since \(u,z\)
miss \(g\), it follows that \(xg\) is an edge.  Symmetrically, every
\(h\in Q_z\) satisfies \(uh\in E(G)\).  A common member of \(P_z,Q_z\)
would miss all three guards of \(R_z\), so the two sets are disjoint.

For \(g\in P_z\), the state \(S_g=\{u,z,g\}\) is a maximum independent
triple and therefore belongs to every eternal triple-family.  Transport
of the active move \(u\to x\) by C-108 gives

\[
 X_g=S_g-u+x=\{x,z,g\}\in\mathcal F.
\tag{2.12}
\]

Now fix \(h\in Q_z\).  The state \(X_g\) must dominate \(h\), while
\(x,z\) both miss \(h\).  Hence \(gh\in E(G)\).  This proves the
complete join in (2.4); its internal clique statements were already
proved.

The state \(T_h=\{x,z,h\}\) is also a maximum independent triple and is
retained.  If \(O_h=T_h-x+u\) were retained, this independent source
would witness \(x\triangleright_{\mathcal F}u\), contrary to (2.1).
Thus \(O_h\) is omitted.

Attack the unoccupied vertex \(h\) from \(S_g\).  The only
graph-eligible guards are \(u,g\): the \(g\)-successor is the omitted
state \(O_h\), while the \(u\)-successor is \(M_{g,h}\).  Eternal
closure therefore forces

\[
 S_g\xrightarrow[\text{attack }h]{u\to h}M_{g,h}
 \in\mathcal F.
\tag{2.13}
\]

The same retained states give all four activities in (2.9):

\[
\begin{array}{c|c|c}
\text{activity}&\text{independent source}&\text{retained successor}\\ \hline
u\to h&S_g&M_{g,h}\\
h\to u&T_h&R_z\\
x\to g&T_h&M_{g,h}\\
g\to x&S_g&R_z.
\end{array}
\tag{2.14}
\]

For \(h\to u\), the competing \(x\to u\) successor is exactly the
omitted state \(O_h\), so the displayed \(h\)-response is forced.

Since \(z\in W_{uh}\) and its central state \(O_h\) is omitted, C-172
puts the whole \(uh\)-fan in the omitted branch, proving (2.8).
Likewise \(z\in W_{xg}\cap W_{gh}\), while \(X_g\) and \(M_{g,h}\)
are retained central states.  The supported-pair fan theorem gives
(2.10) and the two clique conclusions. \(\square\)

Every family nonmembership used above comes from the literal inactivity
assumption in (2.1) or from C-172's membership dichotomy.  No missing
family transition is converted into a graph nonedge.

## 3. Canonical QQ1 consequence

Retain the accepted canonical rank-one QQ1 notation:

\[
 T=\{x,p,q\}\in\mathcal K,\qquad
 u\triangleright x,\qquad x\not\triangleright u,
\tag{3.1}
\]

where \(\mathcal K\) is the greatest eternal family.  For every
\(d\in C_{xr}\), accepted C-166 supplies the retained state

\[
 A_d=\{u,x,d\}\in\mathcal K.
\tag{3.2}
\]

Thus the pair \(u,x\) is supported, and Theorem 2.1 applies
simultaneously to **every** \(z\in W_{ux}\).  This adds a complete
polarized bow tie at each witness to the already accepted QQ1 hot and
cross layers.

Now fix \(w\in W_{ud}\).  Accepted C-167 gives

\[
 D_{w,z}=\{u,w,z\}\in\mathcal K.
\tag{3.3}
\]

Accepted C-166 also gives \(wx\in E(G)\), while every
\(z\in W_{ux}\) misses \(x\).  Hence \(w\ne z\), so the following
edge/nonedge split is literal.

### Corollary 3.1 (exact hot-bridge coupling) — PROVED CANDIDATE

For every \(w\in W_{ud}\) and \(z\in W_{ux}\), exactly one graph case
holds.

1. If \(wz\notin E(G)\), then \(w\in P_z\).  Consequently
   \[
   \begin{gathered}
     wh\in E(G),\qquad \{z,w,h\}\in\mathcal K
       \quad(h\in Q_z),\\
     x\leftrightarrow_{\mathcal K}w,
   \end{gathered}
   \tag{3.4}
   \]
   and the \(xw\)-central fan is retained.
2. If \(wz\in E(G)\), the retained bridge (3.3) supports the edge
   \(wz\).  Moreover \(u\in W_{wz}\), so
   \[
     \{w,z,e\}\in\mathcal K\qquad(e\in W_{wz}),
   \tag{3.5}
   \]
   \(W_{wz}\) is a nonempty \(G\)-clique, and every
   \(e\in W_{wz}-\{u\}\) is adjacent to \(u\).

#### Proof

The first case is Theorem 2.1 with \(g=w\), using
\(wu,wz\notin E(G)\).  In the second case, (3.3) is a retained state
containing the edge \(wz\).  Since \(wu,zu\notin E(G)\), the vertex
\(u\) belongs to \(W_{wz}\).  The supported-pair fan theorem gives
(3.5) and makes \(W_{wz}\) a clique; its members other than \(u\) are
therefore adjacent to \(u\). \(\square\)

This is an exhaustive graph-edge split, not a family-membership split.
It introduces no fresh-witness assumption.

## 4. Exact controls and finite falsifier

The standalone verifier exhausts every labeled graph through order five
and every one-guard eternal subfamily of dominating triples satisfying
\(\gamma=\alpha=3\).  It finds 197 applicable families and 120
supported asymmetric orientations.  Every orientation satisfies
Theorem 2.1.

The equality graph

```text
D]?
```

is \(K_{2,2}\) plus an isolated vertex and has exact

\[
 (\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3).
\tag{4.1}
\]

The specified five-state eternal subfamily

\[
\{014,024,034,124,234\}
\tag{4.2}
\]

has the supported asymmetric edge \(1\triangleright2\),
\(2\not\triangleright1\).  Its unique \(z=4\) has

\[
 P_z=\{0\},\qquad Q_z=\{3\},
\tag{4.3}
\]

and realizes every retained/omitted fan and activity conclusion of
Theorem 2.1.  This proves that the normal form is not vacuous and that
the theorem cannot itself conclude a contradiction for an arbitrary
eternal subfamily.

The accepted order-18 C-169 graph, in its labeled form

```text
QslallyN\~Y^v^|^z~~V|ve~^}G
```

has \((\gamma,i,\alpha,\gamma^\infty,\theta)=(2,3,3,3,3)\).  With
\(u,x,d,w,z=0,1,7,8,9\), its greatest triple-family has size \(473\),
\(W_{ux}=\{z\}\), and

\[
 P_z=\{6\},\qquad Q_z=\{10\}.
\tag{4.4}
\]

It realizes the entire polarized bow tie.  It also has \(wz\in E(G)\),
\(W_{wz}=\{u\}\), so it realizes the second branch of Corollary 3.1
with the smallest possible supported hot fan.  Its \(\gamma=2\)
classification is essential: this is a boundary control, not a
counterexample and not a realization of the theorem's equality
hypothesis.

Run from the campaign root:

```text
sh math/working/qq1_supported_asymmetry_bowtie/verify_strict.sh
```

## 5. Exact remaining gate

The fixed-anchor witness ladder is replaced by a finite object at each
\(z\in W_{ux}\):

\[
 (P_z,Q_z,\text{all mixed retained states},
 \text{polarized fan statuses}).
\tag{5.1}
\]

The C-167 bridge is no longer an isolated retained triple: it either
enters this bow tie on the nonedge branch or itself supports a complete
fan on the edge branch.  What remains is global coupling between the
objects for different \(z\), different completions \(d\), and different
hot witnesses \(w\).  Neither a strict rank decrease nor a dominating
pair has yet been forced.
