# Hostile audit: unmarked-double \(\{1,1\}\) component

**Verdict: PASS.**

**Audit completed:** 2026-07-25T19:13:25Z.

The candidate theorem in `../UNMARKED_DOUBLE_K11_EXCLUSION.md` is
correct on its stated exact-\(\gcd=q^2\), \(K\ne0\) locus.  I
independently reconstructed the \(q^2\)-jet normal form, both
Hilbert--Burch columns, the four scaling charts, the exact-gcd
boundary (including both projective endpoints), every contact
elimination, and the zero-contact exit.  I found no hidden division,
missed projective point, sign error, or surviving contact.

Two short exposition improvements are advisable before global
promotion:

1. state explicitly why exact gcd rules out the abstract power-fibre
   exception; and
2. replace the compressed zero-contact reference to a plane map over
   \(\mathbb C(r)\) by the direct degree-\(\le4\) triangular plane
   exit in Section 8 below.

Neither issue changes the theorem.

## 1. Complete \(q^2\)-jet reconstruction

Before normalization, write
\[
\begin{aligned}
A&=a_0p^3+a_1p^2q+a_2pq^2+a_3q^3,\\
B&=b_0p^3+b_1p^2q+b_2pq^2+b_3q^3,\\
R&=c_0p^3+c_1p^2q+c_2pq^2+c_3q^3,
\end{aligned}
\]
with \(P=pA,Q=pB\).  Since \(q=0\) is unmarked, the pencil value
\([A(1,0):B(1,0)]\) is nonzero.  A target change therefore gives
\(a_0=0,b_0=1\).

For
\[
\alpha=J(Q,R),\qquad\beta=-J(P,R),\qquad
\gamma=J(P,Q),
\]
the constant and linear \(q\)-jets are
\[
\begin{array}{c|cc}
&[p^{\deg}]&[p^{\deg-1}q]\\ \hline
\alpha&-3b_1c_0+4c_1&
 b_1c_1-6b_2c_0+8c_2\\
\beta&3a_1c_0&-a_1c_1+6a_2c_0\\
\gamma&-4a_1&-8a_2.
\end{array}
\]
The unit pivots \(-4,-8,4,8\) force, successively,
\[
a_1=a_2=0,\qquad
c_1=\frac34b_1c_0,\qquad
c_2=\left(\frac34b_2-\frac3{32}b_1^2\right)c_0.
\]
Conversely these relations make every displayed jet vanish.  Since
\(J(P,Q)\ne0\), one has \(a_3\ne0\).  Scale \(a_3=1\), then apply
\(Q\mapsto Q-(b_3/a_3)P\) to kill \(b_3\).  This is exactly the
candidate normal form, with
\[
b=b_1,\quad c=b_2,\quad d=c_0,\quad e=c_3.
\]
No division by \(b,c,d,e\), or \(K\), occurred.

## 2. The two columns and the splitting divisor

Let \(F_0=(P,Q,R)^T\), and define \(N,M\) as in the candidate.  Direct
polynomial division by \(q\), before any gcd assumption, shows both
columns are polynomial.  To avoid rational-function cancellation, I
checked the reconstruction in the cross-multiplied form
\[
\begin{aligned}
K(F_0)_p&=-16pN+16qM,\\
K(F_0)_q&=(3b^2q-4bp-8cq)N+4bqM.
\end{aligned}
\]
The determinant of the numerator matrix is
\[
-16Kq^2.
\]
Moreover, if \(\Delta=(\alpha,\beta,\gamma)\), then
\[
16(N\wedge M)=-K\,\frac{\Delta}{q^2}.              \tag{1}
\]
On exact gcd \(q^2\) and \(K\ne0\), the row
\(\Delta/q^2\) is primitive.  Equation (1), together with the
positive-degree entries of \(N,M\), makes this a minimal
Hilbert--Burch matrix.  Both columns have component degrees
\((2,2,1)\), so the splitting is exactly \(\{1,1\}\).  There is no
specialization inside \(K\ne0\) at which a third splitting appears.

The abstract power-fibre exception is also absent.  Such an exception
would give
\[
\lambda P+\mu Q=L^4,\qquad R=L^3.
\]
The left side is divisible by the fixed line \(p\), so \(L\) must be
proportional to \(p\).  Hence \(R\) would be proportional to \(p^3\),
which forces \(e=0\).  But, after division by \(q^2\), setting
\(e=0\) makes all three minors divisible by \(p\).  Exact gcd therefore
forces \(e\ne0\) and rules this out.

## 3. Four scaling charts are exhaustive

Under
\[
p\mapsto\alpha p,\qquad q\mapsto\beta q,
\]
followed by the independent target rescalings which restore the
coefficients of \(pq^3,p^4\), the parameters transform with weights
\[
b\mapsto t b,\qquad c\mapsto t^2c,\qquad
\frac ed\mapsto t^3\frac ed,\qquad t=\frac\beta\alpha.
\]
The third target coordinate has an additional independent nonzero
scale.

Exact gcd gives \(e\ne0\) on every chart.  If \(b=0\), then
\(K=-8c\ne0\) gives \(c\ne0\).  Thus the following disjoint zero
patterns exhaust \(K\ne0\):
\[
\begin{array}{c|c}
(b,d)&\text{normalization}\\ \hline
b d\ne0&b=d=1\\
b\ne0,\ d=0&b=e=1\\
b=0,\ d\ne0&c=d=1\\
b=d=0&c=e=1.
\end{array}
\]
The square-root choice used to normalize \(c\) exists over
\(\mathbb C\); its two choices differ by the residual finite
stabilizer.  No projective parameter point is missing.

## 4. Exact gcd on the generic chart

On \(b=d=1\), divide the three minors by \(q^2\) and denote them
\(\bar\alpha,\bar\beta,\bar\gamma\).  Exact reconstruction gives
\[
\bar\gamma=-4p^2H,\qquad
H=3p^2+2pq+cq^2,\qquad
\bar\beta(0,q)=-3eq^3.                              \tag{2}
\]
Thus \(e=0\) creates the additional factor \(p\), while for
\(e\ne0\) no common factor can be \(p\).  Every remaining common
factor must divide \(H\).

There is no lost point at \(q=0\), since \(H(p,0)=3p^2\).  Hence set
\(q=1\).  The independently computed Sylvester determinant is
\[
\operatorname{Res}_p(\bar\beta(p,1),H(p,1))
=\frac{243}{1024}J(c,e),
\]
with
\[
J=192c^3-48c^2-1024ce-5c+1024e^2+320e.
\]
This also handles the point \(p=0\): when it lies on \(H\) (so
\(c=0\)), equation (2) gives \(\bar\beta(0,1)=-3e\ne0\).

Finally, at any common zero of \(\bar\beta,H\), one has
\(\bar\gamma=0\), and the gradient syzygy
\[
P_p\bar\alpha+Q_p\bar\beta+R_p\bar\gamma=0
\]
forces \(\bar\alpha=0\), because \(P_p=q^3\ne0\) there.  Therefore
\[
\gcd(\alpha,\beta,\gamma)=q^2
\quad\Longleftrightarrow\quad eJ(c,e)\ne0
\]
on the generic \(K\ne0\) chart.

## 5. Generic \(y=0\) contact

For a nonzero contact with \(y=0\), projectivity gives \(x=1\).
The last equation and \(e\ne0\) give
\[
\mu=-\frac c8.
\]
The preceding equation becomes
\[
-\frac38e(16\lambda c-8c-3)=0.
\]
If \(c=0\), this is already a contradiction, so division by \(c\)
in the next line is legitimate:
\[
\lambda=\frac{8c+3}{16c}.
\]
The next equation has the factor \(8c-3=-K\), which is nonzero on
this component, and gives
\[
e=\frac{96c^2-36c+5}{128}.
\]
The remaining equation is
\[
\frac3{16}(4c-1)^2(8c-5)=0,
\]
while the exact-gcd polynomial becomes
\[
J=\frac9{16}(4c-1)^2(8c-5)^2.
\]
Thus every \(y=0\) contact lies on the larger-gcd boundary.  The audit
performed all steps after cross-multiplication and confirmed that no
\(c=0,e=0\), or \(K=0\) point was silently discarded.

## 6. Generic \(y\ne0\) contact

Scale \(y=1\).  The first equation determines \(e\) without division:
\[
e=-\frac{25-144c+192c^2}{512}.
\]
The second is
\[
-\frac{45}{2048}(8c-3)h(c),\qquad
h=64c^2-16c-1.
\]
Since \(K\ne0\), one has \(h=0\).

Reducing the next two raw contact coefficients modulo \(h\) gives the
candidate \(R_2,R_3\) (with respective factors \(9/2048\) and
\(3/8192\)).  Their exact difference is
\[
R_3-5R_2=-2(56c-17)(12x-1),
\]
and
\[
\operatorname{Res}_c(h,56c-17)=128.
\]
Thus \(x=1/12\).

At that value, three remaining equations are precisely the displayed
\(E_0,E_1,E_2\), up to nonzero rational factors.  Their augmented
determinant has remainder
\[
-31850496(79048c-23855)\pmod h,
\]
and
\[
\operatorname{Res}_c(h,79048c-23855)=278656.
\]
Therefore the three linear equations in \(\lambda,\mu\) are
incompatible at both roots of \(h\).  This excludes the entire
\(y\ne0\) chart without selecting a root or dividing by an algebraic
parameter.

The split \(y=0\) versus \(y\ne0\) is projectively exhaustive.  Scaling
\((x,y)\) is legitimate because the curvature is quadratic in the
tangent \(S=xN+yM\), while \((\lambda,\mu)\) may be rescaled by the
same square.

## 7. Boundary charts

I reconstructed the raw curvature on all three remaining charts.

- \(b\ne0,d=0\), with \(b=e=1\): the first equation is
  \(12y^2=0\).  After \(y=0,x=1\), the next pivots give
  \(\lambda=1\) and \(8c+12\lambda-15=0\), hence
  \(c=3/8\) and \(K=0\).
- \(b=0,c\ne0,d\ne0\), with \(c=d=1\): the first equation is
  \((9/2)y^2=0\).  The last three are nonzero multiples of
  \(e\mu,\ \mu+8e\lambda,\ \lambda+4e\).  Since \(e\ne0\), they
  are inconsistent.
- \(b=d=0,c\ne0\), with \(c=e=1\): the first nonzero equation is
  \(30y^2=0\), and after \(y=0,x=1\) a later equation is \(-6=0\).

These contradictions hold on supersets of the exact-gcd opens, so no
additional boundary resultant is needed.

## 8. Zero contact and the exact degree ceiling

When \(x=y=0\), \(E_7\) makes \(U,V,T\) binary.  The remaining \(E_6\)
equation is
\[
\alpha A_r+\beta B_r+\gamma\ell_{33}=0.
\]
After division by the exact gcd \(q^2\), the generator degrees are
\((3,3,4)\).  The coefficient degrees in this equation are
\((1,1,0)\), so its total syzygy degree is \(4\).  Both minimal
\(\{1,1\}\) columns have component degrees \((2,2,1)\), hence total
degree \(5\).  There is no total-degree-four syzygy.  Consequently
\[
A_r=B_r=\ell_{33}=0,
\]
and every nonlinear homogeneous term is binary.

This exit has exact plane degree ceiling **four**.  Multiply on the
target by the inverse linear part.  The map becomes
\[
(p,q,r)\longmapsto
\bigl(p+f(p,q),\,q+g(p,q),\,r+h(p,q)\bigr),
\qquad \max(\deg f,\deg g,\deg h)\le4.
\]
Its first two entries form a plane Keller map of degree at most four
over \(\mathbb C\).  The unconditional plane lower bound (indeed, any
published bound \(>4\)) makes that plane map an automorphism.  The
third entry is then an explicit triangular shear.  This proves
automorphy directly; it neither assumes the plane Jacobian Conjecture
nor needs a delicate descent from \(\mathbb C(r)\).

## 9. Independent exact verification and fault mutations

`verify_unmarked_double_k11_independent.py` is a dependency-free sparse
polynomial implementation over `Fraction`.  It does not import either
CAS used by the candidate.  It reconstructs:

- the six raw \(q^2\)-jet equations;
- polynomiality, cross-multiplied reconstruction, determinant, and
  primitive wedge of \(N,M\);
- the Sylvester resultant defining \(J\), the projective endpoints,
  and the gradient-syzygy implication;
- the raw three-variable curvature and both generic contact charts;
- both nonzero resultants and the augmented determinant; and
- all three boundary charts.

The strict wrapper also reruns under optimized Python; it uses explicit
checks rather than assertions.  Four fault injections are required to
fail:

\[
\begin{array}{c|c}
\text{mutation}&\text{target}\\ \hline
q2\_jet&c_2\text{ coefficient in the normal form}\\
gcd\_J&320e\mapsto321e\text{ in }J\\
contact\_R3&121\mapsto122\text{ in }R_3\\
contact\_E1&-3865\mapsto-3864\text{ in }E_1.
\end{array}
\]

At 2026-07-25T19:13:25Z, both the supplied dual-CAS strict suite and
the independent hostile strict/mutation suite passed.

This audit verifies the stated unmarked-double exact-\(\delta=2\),
\(\{1,1\}\) component only.  It does not enlarge the theorem to other
fixed-linear strata.  Exact computation is evidence about the encoded
algebra, not peer review.
