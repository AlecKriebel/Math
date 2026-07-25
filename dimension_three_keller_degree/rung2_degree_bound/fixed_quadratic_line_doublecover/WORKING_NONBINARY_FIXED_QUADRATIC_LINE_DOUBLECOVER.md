# Working theorem: the nonbinary fixed-quadratic line double-cover stratum

**Status:** proved by exact determinant elimination, checked by independent
SymPy and PARI/GP implementations, and independently adversarially
reconstructed from the raw systems.  The source-specific priority search
found no exact prior statement and is not a guarantee of worldwide
priority.

**Recorded:** 2026-07-25T04:59:28Z.

**Promoted after audit:** 2026-07-25T05:38:33Z.

This note is not peer reviewed.  Its exact calculations are evidence about
the encoded algebra, not peer review.

## 1. Statement and normalization

Let
\[
F=L_0X+H_2+H_3+H_4:\mathbb A^3_{\mathbb C}\longrightarrow
\mathbb A^3_{\mathbb C}
\]
have total degree four, with \(H_i\) homogeneous of degree \(i\).  Suppose
the projective image of \(H_4\) is a line, its minimal source pencil is
linear, its outer map has degree two, and its fixed divisor has degree two.
This is the taxonomy row
\[
(e,a,b,\delta,\nu)=(2,1,2,1,2).
\tag{1}
\]

Every separable degree-two map \(\mathbb P^1\to\mathbb P^1\) is, under
independent source and target projective changes, the squaring map.  Indeed,
Riemann--Hurwitz gives two distinct simple ramification points; sending
them and their two branch values to \(0,\infty\) gives the normal form
\([p:q]\mapsto[p^2:q^2]\).  Thus
\[
\boxed{H_4=h(p,q,r)(p^2,q^2,0)^T}
\tag{2}
\]
for a nonzero quadratic \(h\).

### Theorem

Assume that the fixed quadratic is nonbinary:
\[
h\notin\mathbb C[p,q].
\tag{3}
\]
If \(F\) is Keller, then \(F\) is a polynomial automorphism.  In
particular, no degree-four Keller counterexample lies in the nonbinary
part of (1).

The binary locus \(h\in\mathbb C[p,q]\) is not treated here.

## 2. The logarithmic derivation

Put \(C=JH_4\) and
\[
k=(ph_r,qh_r,rh_r-4h)^T.
\tag{4}
\]
Directly crossing the two nonzero rows of \(C\) gives
\[
\nabla(hp^2)\times\nabla(hq^2)=-2hpq\,k,
\]
and therefore
\[
\boxed{\operatorname{adj}C=-2hpq\,k e_3^T.}
\tag{5}
\]

Set
\[
\mathcal J(z)=L_0+zJH_2+z^2JH_3+z^3JH_4,\qquad
E_j=[z^j]\det\mathcal J(z).
\tag{6}
\]
The Keller condition says \(E_j=0\) for \(j>0\).

On \(p\ne0\), write
\[
t=q/p,\qquad s=r/p,\qquad h=p^2H(t,s).
\]
For a homogeneous form \(G=p^dg(t,s)\), the derivation in (4) satisfies
\[
\boxed{D_kG=p^{d+1}\bigl(dH_sg-4Hg_s\bigr).}
\tag{7}
\]
Equation \(E_8=0\) is \(D_k(H_3)_3=0\).  At an \(s\)-dependent irreducible
factor \(\phi^m\Vert H\), taking the \(\phi\)-adic residue gives
\[
4v_\phi((H_3)_3)=3m.
\tag{8}
\]
Here \(m\in\{1,2\}\), so (8) is impossible for a nonzero polynomial.
Consequently
\[
\boxed{(H_3)_3=0.}
\tag{9}
\]

Since \(JH_3\) now has zero third row, its mixed contribution to \(E_7\)
vanishes.  The identity \(E_7=0\) becomes \(D_k(H_2)_3=0\), and residues
give
\[
2v_\phi((H_2)_3)=m.
\tag{10}
\]
Unless \(h\) is the square of a nonbinary linear form, (10) forces
\((H_2)_3=0\).  Here the square is global, not merely a square over
\(\mathbb C(t)\).  Indeed, every \(s\)-dependent factor of the quadratic
\(H(t,s)\) must have multiplicity two.  Hence \(H\) has degree two in
\(s\), its discriminant vanishes, and its constant \(s^2\)-coefficient
together with its affine-linear \(s\)-coefficient gives
\[
H=c(s+ut+v)^2,\qquad h=c(r+uq+vp)^2                     \tag{10a}
\]
for constants \(c\ne0,u,v\).

When \((H_2)_3=0\), the third component of \(F\) is a nonzero linear form.
After linear changes, write \(F=(P,Q,r)\).  The pair \((P,Q)\) is a plane
Keller map of degree at most four over \(\mathbb C(r)\).  The established
unconditional plane degree bound, after algebraic base change, makes this
pair birational; the birational Keller theorem then makes \(F\) a
polynomial automorphism.  This exit does not assume the plane Jacobian
Conjecture.

The only remaining case normalizes, while keeping the minimal pencil, to
\[
h=r^2,\qquad
H_4=(p^2r^2,q^2r^2,0)^T.
\tag{11}
\]
The complete quadratic kernel of \(D_k\) is
\[
(H_2)_3=r(\alpha p+\beta q).
\tag{12}
\]
For completeness, these are full-stabilizer orbits.  The leading map in
(11) has the doubled fixed line \(r=0\) and reduced-pencil base point
\([0:0:1]\), so a source stabilizer preserves both.  Compatibility with
the two ramification lines of the squaring cover makes its action on
\(\langle p,q\rangle\) diagonal or anti-diagonal.  Thus the zero pattern
of \((\alpha,\beta)\) is invariant up to exchange.  Consequently the
nonzero forms in (12) have exactly two representatives:
\[
(H_2)_3=pr,\qquad (H_2)_3=(p+q)r.
\tag{13}
\]

The raw coefficient matrices are constant.  In the \(pr\) and
\((p+q)r\) orbits their degree-six ranks/nullities are respectively
\[
(10,13),\qquad(14,9),
\]
while the ensuing degree-five ranks/nullities are
\[
(4,14),\qquad(6,12).
\tag{13a}
\]
The displayed families below have exactly those dimensions and are the
complete affine solution sets.

## 3. The \(pr\) orbit

Write the third row of \(L_0\) as \((a,b,c)\).  The complete degree-six
solution and then the complete degree-five solution are
\[
\begin{aligned}
H_3&=(2pr(ap+bq+cr),\,U,\,0)^T,\\
H_2&=((ap+bq)^2+dpr+eqr+c^2r^2,\,V,\,pr)^T,
\end{aligned}
\tag{14}
\]
where \(U\) and \(V\) are arbitrary cubic and quadratic forms,
respectively.

Put \(K=2bc-e\), and write
\[
U=\sum_{i=0}^9U_iM_i,\qquad
(M_0,\ldots,M_9)
=(p^3,p^2q,pq^2,q^3,p^2r,pqr,q^2r,pr^2,qr^2,r^3).
\]
The degree-four table includes
\[
\begin{array}{c|c@{\qquad}c|c}
p^3r&3KU_0&p^2qr&3KU_1\\
pq^2r&3KU_2&q^3r&3KU_3\\
p^2r^2&KU_4&pr^3&-KU_7\\
r^4&-3KU_9&
\end{array}
\tag{15}
\]
and
\[
\begin{aligned}
[pqr^2]E_4&=2\lambda_{11}+KU_5+4a^2c-2ad,\\
[q^2r^2]E_4&=2\lambda_{12}+KU_6+4abc-2bd,\\
[qr^3]E_4&=-2\lambda_{13}-KU_8-4ac^2+2cd.
\end{aligned}
\tag{16}
\]

If \(K=0\), (16) makes the first row of \(L_0\)
\[
(\lambda_{11},\lambda_{12},\lambda_{13})
=(d-2ac)(a,b,c),
\]
so \(\det L_0=0\).

Assume \(K\ne0\).  Equations (15)--(16) give
\[
\begin{aligned}
U&=qr(Ap+Bq+Cr),\\
(L_0)_{1\bullet}
&=\left(-\frac{AK}{2}-2a^2c+ad,\,
        -\frac{BK}{2}-2abc+bd,\,
        -\frac{CK}{2}-2ac^2+cd\right).
\end{aligned}
\tag{17}
\]
Degree three gives
\[
V=\frac14(Ap+Bq)^2+gpr+jqr+\frac14C^2r^2.
\tag{18}
\]
Its coefficient matrix has constant rank four after the nonzero scalar
factor \(K\) is removed.  The degree-two coefficient matrix has constant
rank three after the same removal, and gives
the following full solution.
If the second row of \(L_0\) is \((m,n,o)\), degree two gives
\[
\begin{aligned}
m&=\frac{-ABC-2ACa+2Aj+4ag}{4},\\
n&=\frac{-2ACb-B^2C+2Bj+4bg}{4},\\
o&=\frac{-2ACc-BC^2+2Cj+4cg}{4}.
\end{aligned}
\tag{19}
\]
Substitution into the determinant gives
\[
\boxed{\det L_0=0.}
\tag{20}
\]
The degree-one identity then vanishes identically, so no lower branch was
discarded.

## 4. The \((p+q)r\) orbit

The complete degree-six solution has
\[
H_3=(-pW+2pr(ap+bq+cr),\,qW,\,0)^T
\tag{21}
\]
with \(W\) an arbitrary quadratic, and again
\((L_0)_{3\bullet}=(a,b,c)\).  The degree-five identity contains three
successive square coefficients.  They force
\[
W=r(Dp+Eq+Tr).
\tag{22}
\]
Put
\[
\alpha=D-2a,\qquad \beta=E-2b,\qquad \gamma=T-2c.
\tag{23}
\]
The complete remaining degree-five solution is
\[
\begin{aligned}
(H_2)_1={}&
\left(\frac{\alpha^2}{4}+X\right)p^2
+\left(\frac{\alpha\beta}{2}+Y\right)pq
+\frac{\beta^2}{4}q^2+Ppr+Qqr+\frac{\gamma^2}{4}r^2,\\
(H_2)_2={}&
\frac{D^2}{4}p^2+\left(\frac{DE}{2}-X\right)pq
+\left(\frac{E^2}{4}-Y\right)q^2
+Rpr+Sqr+\frac{T^2}{4}r^2,\\
(H_2)_3={}&(p+q)r.
\end{aligned}
\tag{24}
\]

Four binary degree-four coefficients reduce exactly to
\[
\boxed{
DX=0,\quad
(\alpha+E)X+DY=0,\quad
\beta X+(\alpha+E)Y=0,\quad
\beta Y=0.
}
\tag{25}
\]
Unless
\[
D=0,\qquad \alpha+E=0,\qquad \beta=0,
\tag{26}
\]
the system (25) forces \(X=Y=0\).  In the exceptional case (26), equivalently
\[
D=0,\qquad a=b,\qquad E=2a,
\tag{27}
\]
the degree-three coefficients include
\[
[p^3]E_3=-2X^2,\qquad [q^3]E_3=-2Y^2,
\]
so \(X=Y=0\) there as well.

With \(X=Y=0\), five remaining degree-four coefficients solve five of the
six entries in the first two rows of \(L_0\).  Their constant solve matrix
has determinant \(-32\).  Reparametrize the remaining affine coordinate
by \(M\), with coefficient \(-4\) on the unsolved entry.  In the
nonexceptional case, the exact degree-three and determinant factors are
\[
[p^2r]E_3=\frac D2M,\qquad
[pqr]E_3=\frac{\alpha+E}{2}M,\qquad
[q^2r]E_3=\frac\beta2M,\qquad
M\mid\det L_0.
\tag{28}
\]
Thus (25) not being exceptional forces \(M=0\) and hence
\(\det L_0=0\).

It remains to check (27).  After the degree-four solve, put
\[
M_*=\lambda_{22}+2a^2c+a^2\gamma-aS.
\tag{29}
\]
Two exact lower coefficients have the form
\[
\begin{aligned}
[pr]E_2&=M_*A,\\
[p]E_1&=M_*(aA-M_*),
\end{aligned}
\qquad
A=4ac+2a\gamma+R-S.
\tag{30}
\]
They imply \(M_*^2=0\), hence \(M_*=0\).  The determinant after the same
degree-four solve is divisible by \(M_*\), so again
\[
\boxed{\det L_0=0.}
\tag{31}
\]
More explicitly, the division-free identity
\[
a[pr]E_2-[p]E_1=M_*^2                                  \tag{32}
\]
and the polynomial divisibility \(M_*\mid\det L_0\) cover every zero
specialization without division.
This finishes both nonzero orbits in (13), and hence the nonbinary theorem.

## 5. Verification boundary and disclosure

Run

```text
/usr/bin/python3 verify_nonbinary_fixed_quadratic_line_sympy.py
./verify_nonbinary_fixed_quadratic_line_pari_strict.sh
```

The accompanying SymPy regression reconstructs (5)--(12), both raw
degree-six kernels, the complete degree-five equations, and every displayed
lower coefficient through (31).  PARI/GP independently expands the general
adjugate and derivation, both normalized lower branches, the exceptional
squares, and the final determinant factors.  It is run through a strict
wrapper that rejects every GP diagnostic and requires a unique pass marker.

The factor-residue argument, the degree-two cover normalization, the two
stabilizer orbits, and the plane birational exit are mathematical inputs,
not consequences of a computer calculation.  This proof and its
regressions were developed with AI assistance.  The independent hostile
audit reconstructed the global square passage, full stabilizer, all four
raw ranks and converses, the \(K\)-specializations, the literal determinant
divisibilities, and (32).  It also confirmed that optimized Python and GP
diagnostic injections fail closed.  The binary fixed-divisor locus remains
open.
