# Working theorem: the conic double-cover row

**Status:** proved by a complete exact branch reduction, checked by
independent SymPy and PARI/GP implementations, and independently
adversarially reconstructed from the raw systems.  This is not peer
reviewed.  The source-specific priority search found no exact prior
statement and is not a guarantee of worldwide priority.

**Recorded:** 2026-07-25T04:50:23Z.

**Promoted after audit:** 2026-07-25T05:19:48Z.

> **AI-assistance and verification disclosure.**  The derivation,
> branch analysis, verifier, and exposition were produced with AI
> assistance under human direction.  The exact script reconstructs the raw
> coefficient operators and checks the stated ranks, kernels,
> compatibilities, gauges, and lower-degree identities.  Those checks are
> evidence for the encoded algebra only: they are not independent peer
> review, do not certify the geometric reduction by themselves, and do not
> establish a priority claim.

## 1. Statement

Let
\[
F=L_0X+H_2+H_3+H_4:\mathbb A^3_{\mathbb C}\longrightarrow
\mathbb A^3_{\mathbb C}
\]
have total degree four, with \(H_i\) homogeneous of degree \(i\).  Suppose
the projective leading image is a conic and its parametrization has generic
degree two.  Equivalently, this is the taxonomy row
\[
\boxed{(e,a,b,\delta,\nu)=(0,1,4,2,2).}
\tag{1}
\]

### Theorem

If \(F\) is Keller, then \(F\) is a polynomial automorphism.  Hence this
entire conic double-cover row contains no degree-four Keller
counterexample.

The only external input in the final automorphism branches is the banked
degree-at-most-four plane Keller theorem.

## 2. Why one leading form is exhaustive

After a target change, the leading form is
\[
H_4=\operatorname{Ver}(B_0(x,y),B_1(x,y)),
\qquad
\operatorname{Ver}(s,t)=(s^2,st,t^2),
\tag{2}
\]
where \(B_0,B_1\) are coprime binary quadratics and
\([B_0:B_1]:\mathbb P^1\to\mathbb P^1\) has degree two.

A degree-two map of projective lines has two distinct ramification points
and two distinct branch values.  Send the ramification points to
\([1:0],[0:1]\) and the branch values to the same two points.  The zero and
pole divisors are then twice those points, so, after rescaling,
\[
[B_0:B_1]=[x^2:y^2].
\]
Consequently independent linear source and target changes put every member
of (1) into
\[
\boxed{H_4=(x^4,x^2y^2,y^4)^T.}
\tag{3}
\]
Conversely, (3) is the Veronese conic composed with the degree-two map
\([x:y]\mapsto[x^2:y^2]\), so it lies in (1).  Thus (3) is an if-and-only-if
normal form and no relative-position modulus occurs at leading degree.

Write \(E_j\) for the coefficient of \(t^j\) in
\[
\det\bigl(L_0+tJH_2+t^2JH_3+t^3JH_4\bigr).
\tag{4}
\]
For a Keller map, \(E_1,\ldots,E_8\) vanish and
\(\det L_0\ne0\).

## 3. The complete degree-eight kernel

The two nonzero columns of \(JH_4\) have cross product
\[
\Delta
=8xy(y^4,-2x^2y^2,x^4)^T,
\qquad
\operatorname{adj}(JH_4)=e_z\Delta^T.
\tag{5}
\]
Hence
\[
E_8=\Delta\cdot\partial_zH_3.
\tag{6}
\]

On a completely general \(30\)-coefficient cubic vector, (6) has rank
\(16\).  Its \(14\)-dimensional kernel is exactly
\[
\boxed{
H_3=C_3(x,y)+z
\begin{pmatrix}
2ax^2\\ ay^2+bx^2\\2by^2
\end{pmatrix},
}
\tag{7}
\]
where \(C_3\) is an arbitrary binary cubic vector and \(a,b\in\mathbb C\).
Indeed, the degree-two syzygies of
\((y^4,-2x^2y^2,x^4)\) are precisely
\[
\left(2ax^2,\ ay^2+bx^2,\ 2by^2\right).
\]
From this point onward, \(a,b\) denote the two scalars in (7), not the
degree entries in the taxonomy tuple (1).

Index the coefficients of \(C_3\), component by component and starting at
zero, by
\[
C_{3,i}=c_{4i}x^3+c_{4i+1}x^2y+c_{4i+2}xy^2+c_{4i+3}y^3.
\tag{8}
\]

## 4. Degree seven: rank, compatibilities, and full solution

Write \(B_2(x,y)\) for an arbitrary binary quadratic vector.  The
degree-seven operator on the eighteen coefficients of \(H_2\) has rank
nine.  Two endpoint coefficients contain no \(H_2\) variable:
\[
[x^7]E_7=-4bc_9,\qquad
[y^7]E_7=-4ac_2.
\tag{9}
\]
These are the complete compatibility equations,
\[
\boxed{bc_9=0,\qquad ac_2=0.}
\tag{10}
\]

When (10) holds, the full solution is
\[
H_2=B_2(x,y)+z
\begin{pmatrix}
\frac{3ac_0-2ac_6+2bc_2}{2}x+
 \frac{2ac_1+3bc_3}{2}y\\[1mm]
\frac{-ac_{10}+6ac_4+4bc_6}{4}x+
 \frac{4ac_5-bc_1+6bc_7}{4}y\\[1mm]
\frac{3ac_8+2bc_{10}}{2}x+
 \frac{2ac_9+3bc_{11}-2bc_5}{2}y
\end{pmatrix}
+z^2
\begin{pmatrix}a^2\\ab\\b^2\end{pmatrix}.
\tag{11}
\]
Direct substitution leaves exactly
\(-4bc_9x^7-4ac_2y^7\), which is also a division-free check of
exhaustiveness.

The stabilizer of (3) contains
\[
x=\alpha X,\quad y=\beta Y,\quad z=\gamma Z,
\qquad
\operatorname{diag}(\alpha^{-4},(\alpha\beta)^{-2},\beta^{-4})
\tag{12}
\]
on the target.  It sends
\[
a\longmapsto \frac{\gamma a}{\alpha^2},
\qquad
b\longmapsto \frac{\gamma b}{\beta^2}.
\tag{13}
\]
Over \(\mathbb C\), the zero pattern of \((a,b)\) therefore gives exactly
three cases:
\[
(0,0),\qquad (1,1),\qquad(1,0),
\tag{14}
\]
plus the source-target involution
\[
(x,y;H_1,H_2,H_3)\longleftrightarrow(y,x;H_3,H_2,H_1),
\tag{15}
\]
which exchanges \((1,0)\) and \((0,1)\).

This list is not merely a convenient set of representatives.  Any source
automorphism preserving (3) must preserve or exchange the two ramification
lines \(x=0,y=0\); on the minimal pencil it is therefore diagonal or the
swap.  The complementary coordinate may be scaled and sheared by \(x,y\).
Those operations rescale, exchange, or leave unchanged the two entries
\(a,b\), and cannot change their zero pattern.  Hence (14)--(15) are the
complete stabilizer-orbit alternatives.

## 5. The zero orbit is plane plus shear

If \(a=b=0\), equations (7) and (11) say that every nonlinear homogeneous
part depends only on \(x,y\).  Put \(A=L_0e_z\).  If \(F\) is Keller, then
\(A\ne0\).  A target change sends \(A\) to the third coordinate, after
which
\[
F(x,y,z)=\bigl(G_1(x,y),G_2(x,y),\lambda z+h(x,y)\bigr),
\qquad \lambda\ne0.
\tag{16}
\]
The plane map \(G\) is Keller and has degree at most four, so it is an
automorphism.  Equation (16) is then an automorphism.

## 6. Both \(a\) and \(b\) nonzero

Normalize \(a=b=1\).  Equations (10) first give \(c_2=c_9=0\).
After substituting (11), the degree-six coefficient has thirteen monomial
rows and rank six in the nine binary-quadratic and nine linear-part
variables.  Six rows contain no such variable:
\[
\begin{array}{c|c}
\text{monomial}&\text{coefficient in }E_6\\ \hline
x^5z&6(-c_{11}+2c_5)\\
x^4yz&-6c_8\\
x^3y^2z&-6(c_1-2c_7)\\
x^2y^3z&6(-c_{10}+2c_4)\\
xy^4z&-6c_3\\
y^5z&-6(c_0-2c_6).
\end{array}
\tag{17}
\]
The seventh cokernel expression is three times
\[
\begin{aligned}
R={}&c_0c_1+2c_1c_4-2c_1c_6+c_1c_8-c_{10}c_{11}
-c_{10}c_3+2c_{10}c_5-2c_{10}c_7.
\end{aligned}
\tag{18}
\]
It introduces no new branch, because the exact ideal certificate is
\[
\begin{aligned}
R={}&c_1(c_0-2c_6)-c_1(c_{10}-2c_4)+c_1c_8\\
&-c_{10}(c_{11}-2c_5)-c_{10}c_3+c_{10}(c_1-2c_7).
\end{aligned}
\tag{19}
\]
Thus (17) is the complete compatibility locus.
Conversely, substituting the six equalities in (17) annihilates every
left-cokernel row of the \(13\times18\) system, so the degree-six equations
are solvable at every point of that locus; there is no suppressed
rank-specialization branch.

On that locus,
\[
C_3=
\begin{pmatrix}
2c_6x^3+2c_7x^2y\\
c_4x^3+c_5x^2y+c_6xy^2+c_7y^3\\
2c_4xy^2+2c_5y^3
\end{pmatrix}.
\tag{20}
\]
Translate \(x,y\) by \(\xi,\eta\), and apply the source shear
\(z\mapsto z+\mu x+\nu y\).  The four parameters in (20) change by
\[
\begin{aligned}
c_4&\mapsto c_4+\mu,&
c_5&\mapsto c_5+\nu+2\eta,\\
c_6&\mapsto c_6+\mu+2\xi,&
c_7&\mapsto c_7+\nu.
\end{aligned}
\tag{21}
\]
The division-free choice
\[
\mu=-c_4,\quad \nu=-c_7,\quad
\xi=\frac{c_4-c_6}{2},\quad
\eta=\frac{c_7-c_5}{2}
\tag{22}
\]
kills all of \(C_3\).  Affine source translation is harmless: translate the
target afterward to restore zero constant term.  Since a Keller determinant
is constant, the new linear part remains invertible.

The canonical form is now
\[
H_3=z(2x^2,x^2+y^2,2y^2)^T,\qquad
H_2=B_2(x,y)+z^2(1,1,1)^T.
\tag{23}
\]
The complete rank-six degree-six solve is
\[
B_2=ux^2+vy^2,\qquad L_0e_z=u+v,
\tag{24}
\]
with \(u,v\in\mathbb C^3\) arbitrary.  In particular, all three \(xy\)
coefficients vanish.

Write \(\ell_{ij}\) for the entry of \(L_0\) in target row \(i\) and source
column \(j\), with columns ordered \(x,y,z\).  After (24), the entire
degree-five coefficient is
\[
\boxed{
E_5=-4\ell_{32}x^5-4\ell_{31}x^4y
+8\ell_{22}x^3y^2+8\ell_{21}x^2y^3
-4\ell_{12}xy^4-4\ell_{11}y^5.
}
\tag{25}
\]
Therefore the first two columns of \(L_0\) vanish.  This gives
\(\det L_0=0\), contrary to the Keller condition.

## 7. Exactly one of \(a,b\) nonzero

By (15), take \(a=1,b=0\).  Equation (10) gives \(c_2=0\).  The raw
degree-six system has ten monomial rows and rank six.  Its four cokernel
conditions are
\[
\boxed{
c_8=0,\qquad c_{10}=2c_4,\qquad c_0=2c_6,\qquad c_{10}c_9=0.
}
\tag{26}
\]
For example, the corresponding coefficients are
\[
[x^4yz]E_6=-6c_8,\quad
[x^2y^3z]E_6=6(-c_{10}+2c_4),\quad
[y^5z]E_6=-6(c_0-2c_6),\quad
[x^6]E_6=c_{10}c_9.
\tag{27}
\]

The same translations and \(z\)-shears kill \(c_6,c_7,c_5\).  The five
invariants left on an affine slice are
\[
S=c_1-2c_7,\quad D=c_3,\quad P=c_4,\quad
M=c_9,\quad N=c_{11}-2c_5.
\tag{28}
\]
Explicitly, the relevant action is
\[
\begin{aligned}
c_6&\mapsto c_6+\mu+2\xi,&
c_1&\mapsto c_1+2\nu,\\
c_7&\mapsto c_7+\nu,&
c_5&\mapsto c_5+2\eta,&
c_{11}&\mapsto c_{11}+4\eta.
\end{aligned}
\]
Taking \(\xi=-c_6/2,\mu=0,\nu=-c_7,\eta=-c_5/2\)
gives the claimed slice and leaves exactly the five quantities in (28).
Equations (26) give the single residual equation
\[
\boxed{PM=0,}
\tag{29}
\]
and every orbit has a representative
\[
C_3=
\begin{pmatrix}
Sx^2y+Dy^3\\
Px^3\\
Mx^2y+2Pxy^2+Ny^3
\end{pmatrix}.
\tag{30}
\]
This slice retains all normal-form moduli; no scaling or division has been
used in (28)--(30).

Conversely, substituting (30) into the raw degree-six system gives (31)--(33)
with six freely chosen parameters and arbitrary first two columns of
\(L_0\).  Since the raw system has rank six, this is its full solution, not
only a family of solutions.  Thus \(PM=0\) is necessary and sufficient for
degree-six solvability on the slice, including the intersection \(P=M=0\).

For arbitrary constants \(q_0,q_2,q_3,q_5,q_6,q_8\), the complete
degree-six solution is
\[
\begin{aligned}
H_2={}&
\begin{pmatrix}
q_0x^2+\frac32DPxy+q_2y^2\\
q_3x^2-\frac14PSxy+q_5y^2\\
q_6x^2+\frac32NPxy+q_8y^2
\end{pmatrix}\\
&+z(Sy,Px,My)^T+z^2(1,0,0)^T,
\end{aligned}
\tag{31}
\]
\[
\boxed{L_0e_z=(q_0,q_3,q_6-P^2)^T.}
\tag{32}
\]
Before imposing (29), direct substitution gives the compact certificate
\[
\boxed{E_6=2MPx^6.}
\tag{33}
\]

### 7.1 The branch \(P\ne0\)

Here (29) gives \(M=0\).  With (31)--(32), the entire degree-five
coefficient is
\[
\begin{aligned}
E_5={}&3NP^2x^5
+\frac{-MPS+8Pq_8-8\ell_{31}}2x^4y
+6MPx^4z\\
&+3P^2Sx^3y^2
-\frac{3DMP+16Pq_5-16\ell_{21}}2x^2y^3\\
&+3DP^2xy^4+(-PS^2+4Pq_2-4\ell_{11})y^5.
\end{aligned}
\tag{34}
\]
Since \(P\ne0\), its separated coefficients force
\[
M=N=S=D=0,\qquad
(\ell_{11},\ell_{21},\ell_{31})=P(q_2,q_5,q_8).
\tag{35}
\]
After (35), degree four is exactly
\[
\boxed{
E_4=2P\ell_{32}x^4-4P\ell_{22}x^2y^2
+2P\ell_{12}y^4.
}
\tag{36}
\]
Thus the second column of \(L_0\) vanishes and again
\(\det L_0=0\).

### 7.2 The branch \(P=0\)

Setting \(P=0\) in (34) gives
\[
\boxed{
E_5=-4\ell_{31}x^4y+8\ell_{21}x^2y^3-4\ell_{11}y^5.
}
\tag{37}
\]
Thus the first column of \(L_0\) vanishes and \(\det L_0=0\).  This is
already a direct contradiction to the Keller condition.

As an independent structural check, this branch retains arbitrary
\(S,D,M,N\).  Set
\[
U=z+x^2,
\tag{38}
\]
which is a polynomial source automorphism.  Let
\[
A=L_0e_x,\qquad B=L_0e_y,\qquad C=L_0e_z=(q_0,q_3,q_6)^T.
\]
Substituting \(z=U-x^2\) into the complete map, with no lower identity
discarded, gives
\[
\boxed{
\begin{aligned}
F={}&Ax+By+CU\\
&+\begin{pmatrix}
U^2+SyU+Dy^3+q_2y^2\\
Uy^2+q_5y^2\\
y^4+MyU+Ny^3+q_8y^2
\end{pmatrix}.
\end{aligned}}
\tag{39}
\]
All nonlinear terms in (39) depend only on \(y,U\).  If \(F\) were Keller,
then \(A\ne0\).  Send \(A\) to the first target direction and project to
the other two target coordinates.  The projected map
\[
G:\mathbb A^2_{y,U}\longrightarrow\mathbb A^2
\]
is Keller and has degree at most four.  The plane theorem makes \(G\) an
automorphism, while the first component of (39) is a shear in \(x\).
This recovers the same exclusion structurally, although the direct
singular-linear-part obstruction (37) is stronger.

## 8. Exhaustion

The branches and their endpoints are:
\[
\begin{array}{c|c|c}
(a,b)&\text{lower branch}&\text{conclusion}\\ \hline
(0,0)&\text{none}&\text{plane plus shear}\\
(1,1)&\text{unique affine orbit after }E_6&\det L_0=0\\
(1,0)&P\ne0&\det L_0=0\\
(1,0)&P=0&\det L_0=0\\
(0,1)&\text{involution of the previous two}&\text{same conclusions}.
\end{array}
\tag{40}
\]
The leading degree-two cover has no modulus, (14) exhausts the stabilizer
zero patterns, (28)--(30) retain every lower relative-position modulus,
and the split (29) includes their intersection.  Thus no normal-form
modulus or specialization is omitted.

## 9. Exact verification

Run

```text
/usr/bin/python3 verify_conic_double_cover_exit_sympy.py
```

The script checks:

1. the adjugate (5), rank-\(16\) degree-eight operator, and the full
   \(14\)-parameter kernel (7);
2. all eleven degree-seven monomial coefficients, rank nine, (10), and
   the complete solution (11);
3. the \(13\times18\), rank-six two-nonzero degree-six system, all seven
   cokernel expressions, certificate (19), and gauge (22);
4. the canonical degree-six solve (24) and the complete certificate (25);
5. the \(10\times18\), rank-six one-nonzero system and all four
   compatibilities (26);
6. the complete five-modulus slice (30), solutions (31)--(33), the full
   degree-five expression (34), and degree-four certificate (36);
7. the direct \(P=0\) exit (37) and exact coordinate factorization (39);
   and
8. the source-target involution (15).

The independent PARI/GP audit in
`audit_conic_double_cover_hostile/audit_conic_double_cover_pari.gp`
reconstructs the raw ranks, gauges, branch solutions, lower exits, and
involution by a separate exact implementation.  Run it through
`audit_conic_double_cover_hostile/audit_conic_double_cover_pari_strict.sh`;
the wrapper rejects diagnostics, extra output, and nonzero exit status.
The hostile audit also reconstructed the geometric normalization,
stabilizer quotient, all specialization endpoints, and both plane exits.
No omitted branch or failing equation was found.
