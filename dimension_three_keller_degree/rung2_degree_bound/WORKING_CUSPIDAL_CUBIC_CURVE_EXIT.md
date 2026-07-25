# Working theorem: the transverse cuspidal-cubic leading stratum

**Status:** proved by an exact coefficient calculation, checked by two exact
implementations, and independently adversarially reconstructed from the raw
systems.  This is not peer reviewed.  The source-specific priority search
found no exact prior statement and is not a guarantee of worldwide priority.

**Recorded:** 2026-07-25T03:28:04Z.

**Promoted after audit:** 2026-07-25T04:07:17Z.

## 1. Statement and scope

Let
\[
F=L_0X+H_2+H_3+H_4:\mathbb A^3_{\mathbb C}\longrightarrow
\mathbb A^3_{\mathbb C}
\]
be a total-degree-four Keller map, where \(H_i\) is homogeneous of degree
\(i\).  Suppose that the leading projective image is an irreducible cuspidal
cubic and that the linear fixed divisor of \(H_4\) is transverse to the
minimal source pencil.  Then, after independent linear source and target
changes,
\[
H_4=rA(p,q),\qquad
A=(p^2q,p^3,q^3)^T,
\tag{1}
\]
where \(p,q,r\) are independent linear coordinates.

### Theorem

No Keller map satisfying (1) exists.

This eliminates only the transverse \(h=r\) part of the cuspidal row
\[
(e,a,b,\delta,\nu)=(1,1,3,3,1).
\]
It says nothing about the scalar-aligned locus
\(h\in\langle p,q\rangle\).

The choice of \(A\) is canonical up to projective equivalence.  It is
basepoint-free, is birational because \(A_1/A_2=q/p\) generically, and its
image is
\[
X^3=Y^2Z,
\]
an irreducible cuspidal cubic.  Every irreducible cuspidal plane cubic over
\(\mathbb C\) is projectively equivalent to this one.

## 2. The ramified normal and its syzygies

Put
\[
A_p=(2pq,3p^2,0)^T,\qquad
A_q=(p^2,0,3q^2)^T.
\]
The normal-minor vector has the nonconstant ramification factor
\[
\Delta=A_p\times A_q
=3pN,\qquad
N=(3pq^2,-2q^3,-p^3)^T.
\tag{2}
\]
The reduced normal \(N\) has the Hilbert--Burch syzygies
\[
S=(2q,3p,0)^T,\qquad
T=(p^2,0,3q^2)^T,
\tag{3}
\]
of coefficient degrees one and two.  Indeed
\[
S\times T=3N,\qquad A_p=pS,\qquad A_q=T.
\tag{4}
\]
Since the components of \(N\) have gcd one, (3) generates the full syzygy
module over \(\mathbb C[p,q]\).

For later coefficient bookkeeping, set
\[
\mathcal J(t)=L_0+tJH_2+t^2JH_3+t^3JH_4,\qquad
E_j=[t^j]\det\mathcal J(t).
\tag{5}
\]
The Keller condition makes \(E_j=0\) for every \(j>0\).

## 3. Degree eight

As in the general transverse-cubic calculation,
\[
\operatorname{adj}(JH_4)=\frac r3
(-p,-q,3r)^T\Delta^T.
\tag{6}
\]
Consequently \(E_8=0\), after cancelling the nonzero factors \(r\) and
\(p\), is
\[
N\mathbin{\cdot}\Theta(H_3)=0,\qquad
\Theta=-p\partial_p-q\partial_q+3r\partial_r.
\tag{7}
\]
On a term \(r^jU_{3-j}(p,q)\), the operator \(\Theta\) has the nonzero
eigenvalue \(4j-3\).  Using the two syzygy degrees in (3), the complete
degree-eight solution is therefore
\[
\boxed{
H_3=S(Q+r\ell+\eta r^2)+T(m+\beta r),
}
\tag{8}
\]
where \(Q\) is a binary quadratic, \(\ell,m\) are binary linear forms, and
\(\eta,\beta\in\mathbb C\).

## 4. The \(r=0\) degree-seven obstruction

Write
\[
Q=ap^2+bpq+cq^2,\qquad m=dp+eq,
\]
and put \(V=QS+mT\).  At \(r=0\), the \(H_2\)-term in \(E_7\) vanishes and
the remaining term is \(\det(V_p,V_q,A)\).  Direct expansion gives the
exact square
\[
\boxed{
\det(V_p,V_q,A)
=-18q\bigl(dp^3+(e-a)p^2q-bpq^2-cq^3\bigr)^2.
}
\tag{9}
\]
Thus \(d=b=c=0\) and \(e=a\), so \(V=3aA\).  Renaming the scalar gives
\[
H_3=\lambda A+r\bigl((\alpha p+\gamma q)S+\beta T\bigr)
       +\eta r^2S.
\tag{10}
\]

## 5. The full raw degree-seven certificate

Take the coefficient order
\[
(p^2,pq,pr,q^2,qr,r^2)
\tag{11}
\]
in each of the three components of a general \(H_2\), producing an
eighteen-entry column \(c\).  In the following degree-seven monomial order,
\[
\begin{split}
&(p^6r,p^5qr,p^5r^2,p^4q^2r,p^4qr^2,p^4r^3,
  p^3q^3r,p^3q^2r^2,\\
&\quad p^2q^4r,p^2q^3r^2,p^2q^2r^3,
  pq^5r,pq^4r^2,pq^3r^3,q^5r^2,q^4r^3,q^3r^4),
\end{split}
\tag{12}
\]
the \(H_2\)-coefficient matrix \(M_7\) in \(M_7c=b_7\) has the following
complete list of nonzero entries:
\[
\begin{array}{c|l}
\text{row}&(\text{column},\text{entry})\\ \hline
1&(13,2)\\
2&(14,2)\\
3&(15,-2)\\
4&(1,-6),(16,2)\\
5&(17,-2)\\
6&(18,-6)\\
7&(2,-6),(7,4)\\
8&(3,6)\\
9&(4,-6),(8,4)\\
10&(5,6),(9,-4)\\
11&(6,18)\\
12&(10,4)\\
13&(11,-4)\\
14&(12,-12).
\end{array}
\tag{13}
\]
Rows 15--17 are zero.  Hence
\[
\operatorname{rank}M_7=14,\qquad
\ker M_7^T=\langle e_{15},e_{16},e_{17}\rangle.
\tag{14}
\]
The three corresponding entries of the right-hand side are
\[
-6\gamma^2,\qquad -36\eta\gamma,\qquad -30\eta^2.
\tag{15}
\]
Thus compatibility forces
\[
\gamma=\eta=0.
\tag{16}
\]
Before (16), the generic augmented rank is \(15\); after (16), it is \(14\).
Using \(pS=A_p\) and \(T=A_q\), (10) becomes
\[
\boxed{
H_3=\lambda A+rD A,\qquad
D=\alpha\partial_p+\beta\partial_q.
}
\tag{17}
\]

Solving the same rank-fourteen system gives the full four-parameter family
\[
\boxed{
H_2=\frac13(uA_p+vA_q)+\frac r2D^2A
       +\frac13(wq+kr)S.
}
\tag{18}
\]
No coefficient of a general quadratic \(H_2\) has been normalized away.

## 6. Degree six with arbitrary \(L_0\)

Write the nine entries of \(L_0\) in row-major order.  In the monomial
order
\[
(p^5r,p^4qr,p^4r^2,p^3q^2r,p^2q^3r,p^2q^2r^2,
pq^4r,pq^3r^2),
\tag{19}
\]
the degree-six coefficient matrix has rank eight.  Its rows are
\[
\begin{pmatrix}
0&0&0&0&0&0&1&0&0\\
0&0&0&0&0&0&0&1&0\\
0&0&0&0&0&0&0&0&-3\\
-3&0&0&0&0&0&0&0&0\\
0&-3&0&2&0&0&0&0&0\\
0&0&9&0&0&0&0&0&0\\
0&0&0&0&2&0&0&0&0\\
0&0&0&0&0&-6&0&0&0
\end{pmatrix},
\tag{20}
\]
and the exact right-hand side is
\[
\begin{pmatrix}
0\\
\beta(-3\beta\lambda+2v)\\
-3\beta^3\\
-2(-3\alpha\beta\lambda+\alpha v+\beta u)\\
-3\alpha^2\lambda+2\alpha u-2\beta w\\
3\beta(3\alpha^2+2k)\\
2\alpha w\\
-6\alpha(\alpha^2+k)
\end{pmatrix}.
\tag{21}
\]
Taking the free entry \(\rho=(L_0)_{21}\), with row indices written
one-based, the unique solution for all other entries is
\[
\boxed{
L_0=
\begin{pmatrix}
\frac23(-3\alpha\beta\lambda+\alpha v+\beta u)&
\frac13(3\alpha^2\lambda-2\alpha u+2\beta w+2\rho)&
\frac13\beta(3\alpha^2+2k)\\
\rho&\alpha w&\alpha(\alpha^2+k)\\
0&\beta(-3\beta\lambda+2v)&\beta^3
\end{pmatrix}.
}
\tag{22}
\]
Thus the calculation retains an initially arbitrary nine-entry linear
part; (22) is forced by \(E_6=0\), rather than assumed.

## 7. Degrees five and three

With (17), (18), and (22) imposed, degree five factors as
\[
\boxed{
E_5=-\frac43q(X-kqr)(X+kqr),
}
\tag{23}
\]
where
\[
X=(v-3\beta\lambda)p^2+(3\alpha\lambda-u)pq-wq^2.
\tag{24}
\]
Since \(\mathbb C[p,q,r]\) is a domain, \(E_5=0\) forces
\[
k=w=0,\qquad
u=3\alpha\lambda,\qquad
v=3\beta\lambda.
\tag{25}
\]
After (25), all coefficients \(E_8,\ldots,E_4\) vanish, and
\[
\begin{aligned}
E_3&=-\frac23q^3(\rho-3\alpha^2\lambda)^2,\\
E_2&=-2\beta q^2(\rho-3\alpha^2\lambda)^2,\\
E_1&=-2\beta^2q(\rho-3\alpha^2\lambda)^2,\\
\det L_0=E_0&=-\frac23\beta^3(\rho-3\alpha^2\lambda)^2.
\end{aligned}
\tag{26}
\]
The Keller identity \(E_3=0\) gives
\(\rho=3\alpha^2\lambda\), and then (26) gives
\(\det L_0=0\).  This is impossible because the constant nonzero Jacobian
of \(F\), evaluated at the origin, equals \(\det L_0\).  The theorem
follows.

## 8. Verification boundary and disclosure

`verify_cuspidal_cubic_exit_sympy.py` reconstructs the raw degree-seven
and degree-six matrices, checks their exact ranks and left-kernel
certificates, solves the displayed families, and checks every factor in
(9) and (23)--(26).

`verify_cuspidal_cubic_exit_pari.gp` independently expands the same
determinants in PARI/GP and checks the normal, syzygies, specialized
degree-seven square, parameterized degree-seven and degree-six solutions,
and all final determinant coefficients.

These computations are evidence about the encoded identities only.  They
do not check projective classification, the transverse-coordinate
reduction, or the theorem's scope, and they are not peer review.

The independent audit reconstructed the normalization of every transverse
cuspidal leading map to (1), the ramified normal and complete
Hilbert--Burch module, the degree-eight eigenspace calculation, the
degree-seven square and raw rank-fourteen system, the full four-parameter
quadratic solution, the arbitrary-linear-part degree-six solve, and the
lower factorization.  It also inspected the PARI implementation for
false-pass paths and confirmed that the argument applies exactly to
\(h\notin\langle p,q\rangle\), without touching the scalar-aligned locus.

This proof and its regressions were developed with AI assistance.  The
result has not been peer reviewed.
