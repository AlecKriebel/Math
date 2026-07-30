# Zero rigidity is sufficient for the square-zero theorem

## Status

This note does **not** prove zero rigidity.  It proves that zero
rigidity is sufficient, including the required connectedness of the
full-local-support configuration space.  It also derives the complete
first-order equations for a negative global minimum.  Those equations
apply to a minimum, not to an arbitrary transverse zero of the
determinant.

Let
\[
 {\cal H}=(\mathbb C^3)^{\otimes3},\qquad \dim{\cal H}=27.
\]
For orthogonal isometries \(U,W:\mathbb C^2\to{\cal H}\), let
\[
 H_{ab,cd}
 ={\cal B}_3(|u_a\rangle\langle w_b|,
             |u_c\rangle\langle w_d|).                   \tag{1}
\]
The established sharp rank-one margin implies
\[
 H\succeq0\quad\Longleftrightarrow\quad\det H\geq0.       \tag{2}
\]
For a two-plane \(V\subseteq{\cal H}\), put
\[
 \rho_i^V=\operatorname{Tr}_{\widehat i}P_V.
\]

The remaining qualitative statement is:
\[
\boxed{
 \det H(U,W)=0
 \quad\Longrightarrow\quad
 \prod_{i=1}^3\det\rho_i^U\det\rho_i^W=0.}               \tag{ZR}
\]

## Theorem 1

If (ZR) holds, then
\[
 Q_3(UBW^\dagger)\geq0
 \qquad\text{for every }U^\dagger W=0,\ B\in M_2.        \tag{3}
\]

Thus the full square-zero problem reduces to the equality statement
(ZR); no quantitative product-determinant constant is needed.

## 1. The full-support locus is path connected

We first record the elementary avoidance fact used below.

### Lemma 1

Let \(M\) be a connected smooth real \(m\)-manifold.  For
\(\nu=1,\ldots,N\), let \(P_\nu\) be a compact smooth manifold of
dimension at most \(m-2\), and let
\(f_\nu:P_\nu\to M\) be smooth.  Then
\[
 M\setminus\bigcup_{\nu=1}^N f_\nu(P_\nu)
\]
is path connected whenever it is nonempty.

### Proof

Take two points \(x,y\) in the complement.  A connected manifold is
polygonally path connected in coordinate charts, so choose a smooth
path \(\gamma\) from \(x\) to \(y\).  Since the forbidden union is
compact and misses the endpoints, short initial and final pieces of
\(\gamma\) already avoid it.

On the remaining compact parameter interval choose finitely many
smooth vector fields \(X_1,\ldots,X_q\), supported away from the
endpoints, whose values span the tangent space of \(M\) at every point
of \(\gamma\).  For sufficiently small
\(s=(s_1,\ldots,s_q)\), perturb \(\gamma\) successively by the local
flows of the fields \(s_jX_j\).  This gives a smooth family
\[
 \Gamma(s,t),\qquad \Gamma(0,t)=\gamma(t),
\]
fixed near \(t=0,1\), for which the derivative in the \(s\)-variables
is onto \(T_{\Gamma(s,t)}M\) after, if necessary, adding finitely many
fields supported in smaller parameter intervals.

For one forbidden map \(f:P^k\to M\), consider
\[
 Z=\{(s,t,p):\Gamma(s,t)=f(p)\}.
\]
Because \(\Gamma\) is a submersion in \(s\), the two maps in this
fiber product are transverse.  Hence \(Z\) is locally cut out by
\(m\) independent real equations and has dimension
\[
 \dim Z=q+1+k-m\leq q-1.
\]
The projection of \(Z\) to the \(q\)-dimensional \(s\)-space has
Lebesgue measure zero.  To see this without any dimension theorem,
cover \(Z\) by countably many coordinate boxes on which the projection
is Lipschitz; a bounded subset of \(\mathbb R^{q-1}\) has images
coverable by \(O(\epsilon^{-(q-1)})\) cubes of side \(O(\epsilon)\),
whose total \(q\)-volume tends to zero with \(\epsilon\).

The same conclusion holds for the finite union of forbidden maps.
Choose an arbitrarily small \(s\) outside the union of their projected
collision sets.  Then \(t\mapsto\Gamma(s,t)\) joins \(x\) to \(y\)
and avoids every \(f_\nu(P_\nu)\). \(\square\)

Now let
\[
 {\cal F}
 =\{(U_0,W_0):U_0,W_0\in\operatorname{Gr}(2,27),\
               U_0\perp W_0\}                            \tag{4}
\]
be the space of ordered orthogonal two-planes.  It is the connected
homogeneous manifold
\[
 U(27)/(U(2)\times U(2)\times U(23))
\]
and has real dimension
\[
 2\cdot2(27-2)+2\cdot2(25-2)=100+92=192.                \tag{5}
\]

Fix one site and consider the locus on which \(U_0\) has deficient
local support.  Such a plane has a nonzero local annihilator
\([a]\in\mathbb{CP}^2\) and obeys
\[
 U_0\subseteq a^\perp\otimes\mathbb C^9.                 \tag{6}
\]
The choices have real dimensions at most
\[
\underbrace{4}_{[a]\in\mathbb{CP}^2}
+\underbrace{2\cdot2(18-2)}_{U_0\in\operatorname{Gr}(2,18)}
+\underbrace{2\cdot2(25-2)}_{W_0\in\operatorname{Gr}(2,25)}
=160.                                                     \tag{7}
\]
More precisely, these choices form a compact smooth bundle and map
smoothly onto the deficient locus.  Multiple annihilators only lower
the image dimension.  The same parameterization applies to either
plane and any of the three sites.

Lemma 1, with the six maps furnished by (7), proves:
\[
\boxed{
 {\cal F}_{\rm full}
 =\{(U_0,W_0)\in{\cal F}:
   \det\rho_i^{U_0}\det\rho_i^{W_0}>0\ (i=1,2,3)\}
 \text{ is path connected}.}                             \tag{8}
\]

## 2. Proof of Theorem 1

The established one-sided local-support theorem says that if any one
of the six determinants in (8) vanishes, then
\[
 Q_3(UBW^\dagger)\geq0\quad\text{for every }B.
\]
Equivalently,
\[
 H(U,W)\succeq0                                           \tag{9}
\]
on the deficient boundary.

Assume (ZR).  On the full-support locus (8), \(\det H\) never
vanishes.  Since that locus is path connected, the sign of \(\det H\)
is constant there.  The exact GHZ four-frame
\[
 U=(g_{0,0,0},g_{0,0,1}),\qquad
 W=(g_{1,2,2},g_{2,1,2})
\]
belongs to the locus and has
\[
 H=\frac12I_4.
\]
Therefore \(\det H>0\) throughout the full-support locus.  Equation
(2) gives \(H\succeq0\) there, and (9) handles its complement.  This
proves (3). \(\square\)

## 3. Exact critical equations for a negative minimum

These equations do not prove (ZR), but they give the correct
alternative target if one attacks a negative witness directly.

Normalize \(\|B\|_2=1\) and put
\[
 C=UBW^\dagger,\qquad
 A={\cal L}^{\otimes3}(C),\qquad
 R=I-UU^\dagger-WW^\dagger.                              \tag{10}
\]
Suppose the square-zero functional has a negative global minimum
\[
 \lambda=Q_3(C)<0.                                       \tag{11}
\]
The rank-one margin excludes \(\operatorname{rank}B=1\), so \(B\) is
invertible.  The local-support boundary theorem puts the minimizing
planes in \({\cal F}_{\rm full}\), so all ordinary frame variations
are available.

The differential is
\[
 dQ_3(C)[\dot C]=2\operatorname{Re}\langle A,\dot C\rangle.
                                                               \tag{12}
\]
Variations of \(B\) on its unit sphere give
\[
\boxed{U^\dagger A W=\lambda B.}                         \tag{13}
\]
Indeed the multiplier is \(\lambda\), since taking the inner product
with \(B\) gives
\[
 \langle B,U^\dagger AW\rangle
 =\langle C,A\rangle=Q_3(C)=\lambda.
\]

Independent frame variations into the orthogonal complement give
\[
\boxed{RAW=0,\qquad RA^\dagger U=0.}                     \tag{14}
\]
For example, the \(U\)-gradient is \(AWB^\dagger\); invertibility of
\(B\) removes it from (14).

Finally take the cross rotation
\[
 \dot U=WT,\qquad \dot W=-UT^\dagger,\qquad T\in M_2.
\]
Then
\[
 \dot C=WTBW^\dagger-UBTU^\dagger.
\]
Using both \(T\) and \(iT\) in (12) yields
\[
\boxed{
 W^\dagger A W\,B^\dagger
 =B^\dagger U^\dagger A U.}                              \tag{15}
\]

If
\[
 S=U^\dagger AU,\qquad M=W^\dagger AW,
\]
equations (13)--(15) are equivalently
\[
\boxed{
\begin{aligned}
 AW&=\lambda UB+WM,\\
 A^\dagger U&=\lambda WB^\dagger+US^\dagger,\\
 MB^\dagger&=B^\dagger S.
\end{aligned}}                                            \tag{16}
\]
They retain the square-zero constraint through the common
orthogonal pair \((U,W)\).  They are strictly stronger than treating
the four matrix blocks or the two singular planes independently.

An arbitrary full-support zero of \(\det H\) need not satisfy
(13)--(16): an entangled eigenvalue may cross zero transversely.
Consequently these equations are a direct-negative-witness route,
whereas Theorem 1 requires the genuinely stronger zero-rigidity
statement (ZR).
