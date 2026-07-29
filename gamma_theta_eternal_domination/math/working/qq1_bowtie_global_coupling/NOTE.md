# Global transport of the QQ1 completion and bow-tie layers

## Status and scope

Date: 2026-07-28 (PDT)

This is a **proved candidate awaiting hostile review**.  It first proves
a general parameter-three transport lemma and then applies it to the
accepted canonical QQ1 normal form.

The advance is size-independent.  The completion-specific hot cliques
from C-166 are actually subsets of one global clique, and every hot
vertex is retained with every completion.  Together with C-167 and
C-177, this produces two coupled complete retained products:
\(C\times H\) through states \(\{u,d,w\}\), and \(H\times Z\) through
bridges \(\{u,w,z\}\).

The result does **not** eliminate QQ1, force reverse activity on the
original edge \(ux\), prove complete parameter three, or resolve the
gamma--theta conjecture.  No omitted family state is interpreted as a
graph nonedge.

The bounded census below directly audits the global \(C\)-by-\(H\)
transport, the retained \(H\)-by-\(Z\) bridges, and the complete-fan
conclusions for edge cells.  For nonedge cells, the polarized-bow-tie
conclusion is the proved symbolic application of accepted C-177; the
census counts those cells but does not independently re-audit C-177's
activity hypotheses or conclusions.

## 1. A general clique-obstructed transport lemma

Assume

\[
 \gamma(G)=\alpha(G)=\gamma^\infty(G)=3
\tag{1.1}
\]

and let \(\mathcal F\) be any eternal family of dominating triples.
Let \(u,x,r\) be distinct vertices such that

\[
 ux,ur\in E(G),\qquad xr\notin E(G).
\tag{1.2}
\]

Let \(C\) be a nonempty \(G\)-clique contained in

\[
 W_{xr}=\{d\notin\{x,r\}:dx,dr\notin E(G)\}.
\tag{1.3}
\]

For every \(d\in C\), let \(H_d\) be a nonempty subset of \(W_{ud}\)
such that

\[
 K_{d,w}:=\{u,d,w\}\in\mathcal F
 \qquad(w\in H_d).
\tag{1.4}
\]

Put

\[
 H=\bigcup_{d\in C}H_d.
\tag{1.5}
\]

### Theorem 1.1 (global completion transport) — PROVED CANDIDATE

Under (1.1)--(1.5):

1. no state of \(\mathcal F\) contains two distinct vertices of \(C\);
2. the complete Cartesian product is retained:
   \[
     \boxed{\{u,d,w\}\in\mathcal F
       \quad(d\in C,\ w\in H);}
   \tag{1.6}
   \]
3. \(H\) is a \(G\)-clique; and
4. for distinct \(d,d'\in C\), the attack at \(d'\) from
   \(K_{d,w}\) has the unique retained response
   \[
     K_{d,w}\xrightarrow{\,d\to d'\,}K_{d',w}.
   \tag{1.7}
   \]

#### Proof

Take distinct \(d,d'\in C\).  Since \(C\) is a clique, \(dd'\) is an
edge.  Both \(x\) and \(r\) belong to \(W_{dd'}\), while \(xr\) is a
nonedge.  If a retained state contained the pair \(d,d'\), accepted
C-174 would make \(W_{dd'}\) a clique, contradicting \(xr\notin E(G)\).
Thus no retained state contains two vertices of \(C\).

Fix \(w\in H_d\) and \(d'\in C-\{d\}\).  The vertex \(d'\) is
unoccupied in \(K_{d,w}\): a member of \(H_d\) cannot equal a distinct
member of the clique \(C\), because it misses \(d\).  Attack \(d'\).
The guard \(d\) is eligible because \(dd'\) is an edge.  Its successor
is \(K_{d',w}\).  The only other possible successors, arising from
\(u\) or \(w\), contain both \(d,d'\), and the first paragraph proves
that neither can belong to \(\mathcal F\).  Eternal closure therefore
forces the unique retained response (1.7).  The case \(d'=d\) is the
original state.  Varying \(d,d',w\) proves (1.6).

Finally take distinct \(w,y\in H\), and choose \(d\in C\) with
\(y\in H_d\).  By (1.6), the state \(\{u,d,w\}\) is retained.  It must
dominate \(y\), while \(y\) misses both \(u,d\).  Hence \(wy\) is an
edge.  Thus \(H\) is a clique. \(\square\)

The proof excludes the two competing responses in (1.7) by their
**family membership**, using C-174.  It does not infer that either
corresponding move edge is absent.

## 2. Canonical QQ1: one global three-layer skeleton

Use the accepted canonical QQ1 notation:

\[
 T=\{x,p,q\}\in\mathcal K,\qquad
 u\triangleright_{\mathcal K}x,\qquad
 x\not\triangleright_{\mathcal K}u,
\tag{2.1}
\]

where \(\mathcal K\) is the greatest eternal triple-family.  Put

\[
 C=C_{xr},\qquad Z=W_{ux},\qquad
 H_d=W_{ud}\ (d\in C),\qquad H=\bigcup_{d\in C}H_d.
\tag{2.2}
\]

Accepted C-158 makes \(C\) a nonempty clique.  The condition
\(\gamma=3\) makes every \(H_d\) and \(Z\) nonempty.  Accepted C-166
retains every seed state \(\{u,d,w\}\), so Theorem 1.1 applies.

### Corollary 2.1 (global QQ1 completion--hot product) — PROVED CANDIDATE

The sets and states in (2.2) satisfy:

\[
\boxed{
\begin{aligned}
 &H\text{ is a clique},\\
 &\{u,d,w\}\in\mathcal K
       &&(d\in C,\ w\in H),\\
 &\{u,w,z\}\in\mathcal K
       &&(w\in H,\ z\in Z),\\
 &C\cup Z\text{ is a clique}.
\end{aligned}}
\tag{2.3}
\]

Moreover,

\[
 u\text{ misses }H\cup Z,\qquad
 x,r\text{ are complete to }H,\qquad
 x\text{ misses }C\cup Z.
\tag{2.4}
\]

The unions in (2.2) are literal: \(C\cap Z\) is allowed.  In fact,
\(d\in C\cap Z\) exactly when \(ud\) is absent.  The hot set \(H\) is
disjoint from \(C\cup Z\).

#### Proof

The first two lines of (2.3) are Theorem 1.1.  For \(w\in H\), choose
\(d\) with \(w\in W_{ud}\).  Accepted C-167 retains
\(\{u,w,z\}\) for every \(z\in Z\), proving the third line.

Both \(C\) and \(Z\) are cliques.  For \(d\in C\) and \(z\in Z-\{d\}\),
accepted C-166 retains \(A_d=\{u,x,d\}\).  Since \(z\) misses \(u,x\),
domination by \(A_d\) forces \(dz\in E(G)\).  Hence \(C\cup Z\) is a
clique.

Every \(w\in H_d\) misses \(u,d\).  The retained state \(A_d\)
therefore forces \(xw\in E(G)\), while the dominating reverse state
\(\{u,r,d\}\) from C-143 forces \(rw\in E(G)\).  The remaining
adjacencies and disjointness statements follow directly from the
definitions and from the clique \(C\). \(\square\)

## 3. Every hot--central cell has an exact status

### Corollary 3.1 (global polarized/support matrix) — PROVED CANDIDATE

For every \(w\in H\) and \(z\in Z\), exactly one graph case holds.

1. If \(wz\notin E(G)\), then \(w\in P_z=W_{uz}\), and accepted C-177
   supplies the entire polarized bow tie at that cell.  In particular,
   \[
     x\leftrightarrow_{\mathcal K}w,
   \tag{3.1}
   \]
   every \(wh\) with \(h\in Q_z=W_{xz}\) has its retained mixed state,
   and the retained/omitted fan statuses are those of C-177.
2. If \(wz\in E(G)\), then the retained bridge
   \(\{u,w,z\}\) supports the pair \(wz\).  Hence C-174 gives
   \[
     \{w,z,e\}\in\mathcal K\qquad(e\in W_{wz}),
   \tag{3.2}
   \]
   \(W_{wz}\) is a clique, and \(u\in W_{wz}\).

Consequently, the entire bipartite \(H\)-by-\(Z\) adjacency matrix is
coupled:

\[
\boxed{
\begin{array}{c|c}
wz=0&\text{polarized C-177 bow-tie cell and }x\leftrightarrow w,\\
wz=1&\text{supported complete retained \(wz\)-fan containing \(u\).}
\end{array}}
\tag{3.3}
\]

In particular, a row \(w\) containing any zero forces
\(x\leftrightarrow w\); an all-one row consists entirely of supported
fan edges.  Mixed rows may occur, and (3.3) does not force
\(x\triangleright u\).

#### Proof

If \(wz\) is absent, then \(w\) misses both \(u,z\), so \(w\in P_z\)
and C-177 applies.  If \(wz\) is present, the retained bridge from
Corollary 2.1 contains that edge.  Apply C-174; \(u\) misses both
\(w,z\), so \(u\in W_{wz}\). \(\square\)

## 4. Exact controls and audit

The seven-vertex equality graph

```text
FCQe_
```

has exact

\[
(\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3)
\tag{4.1}
\]

and a 12-state greatest triple-family.  With

\[
(u,x,r)=(5,0,2)
\tag{4.2}
\]

it has

\[
C=\{1,4\},\qquad
H_1=\{3\},\qquad H_4=\{3,6\}.
\tag{4.3}
\]

Thus the seed list omits the cross incidence \((1,6)\), while the
theorem forces and the exact kernel contains

\[
\{5,1,6\}\in\mathcal K.
\tag{4.4}
\]

The resulting \(H=\{3,6\}\) is a clique.  This is a nonvacuous exact
control for transport between distinct completion fibers.

The standalone checker also exhausts all 33,864 labeled graphs of
orders three through six.  It finds 2,162 equality graphs and verifies
17,640 instances of Theorem 1.1, including 2,520 with
\(|C|\ge2\) and 2,520 with \(|H|\ge2\).  It checks every attack,
product state, clique conclusion, and collision directly from the
literal greatest fixed point.  A further 10,320 bridge-product
instances check the retained bridges in 12,480 \(H\)-by-\(Z\) cells
and apply the full supported-fan audit to edge cells.  The checker only
counts nonedge cells; their C-177 polarization is not an independent
output of this census.  The control `FCQe_` is a transport control, not
a control for polarized nonedge cells.

Run from the campaign root:

```text
sh math/working/qq1_bowtie_global_coupling/verify_strict.sh
```

## 5. Remaining gate

The completion index \(d\) no longer carries an independent hot clique:
all completion fibers transport into one global clique \(H\).  Every
vertex of that clique is simultaneously coupled to every \(z\in Z\)
by the exact matrix (3.3).

The surviving QQ1 problem is therefore narrower:

1. eliminate the all-supported rows of the \(H\)-by-\(Z\) matrix, or
2. show that the reciprocal edges forced by its zero cells propagate
   back to \(x\triangleright u\).

Neither step is proved here.
