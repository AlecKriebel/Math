# Theorem: the marked-critical infinity orbit in line \((2,2)\)

**Status:** exact working theorem, independently hostile-audited.  This is
not peer reviewed, and the source-specific priority search is not a
guarantee of worldwide priority.

**Recorded:** 2026-07-25T05:55:00Z.

**Promoted after hostile audit:** 2026-07-25T06:11:00Z.

## 1. Scope

Let
\[
F=L_0X+H_2+H_3+H_4:\mathbb A^3_{\mathbb C}\to\mathbb A^3_{\mathbb C}
\]
have total degree four and constant nonzero Jacobian.  In the
unique-double-line line-image \((2,2)\) row, consider the marked-critical
orbit
\[
p=x^2,\qquad q=yz,
\]
\[
\boxed{H_4=(p^2,q^2,0)^T,\qquad (H_3)_3=x^3.}             \tag{1}
\]
The double-line value \(p=0\) and the other critical value \(q=0\) of the
outer squaring map are \(0\) and infinity in the pencil coordinate.  Thus
(1) is the branch previously called “marked critical with the other
critical point at infinity.”

### Theorem

No Keller map has leading and cubic-normal data (1).

This theorem concerns only (1).  It does not close every outer-cover chart
in the line-\((2,2)\) row.

## 2. Complete degree-seven form

Put
\[
\delta=z\partial_z-y\partial_y,\qquad
U=(H_3)_1,\quad V=(H_3)_2,\quad W=(H_2)_3.
\]
The degree-seven determinant identity is exactly
\[
E_7=-2x^2q\,\delta(3U-4xW)=0.                             \tag{2}
\]
The cubic kernel of \(\delta\) is
\[
\ker(\delta|\mathbb C[x,y,z]_3)=\langle x^3,xq\rangle.
\]
Consequently
\[
U=\frac43xW+a x^3+A xq,                                  \tag{3}
\]
while \(V\) and \(W\) are arbitrary cubic and quadratic forms.

A target shear removes \(a x^3\).  Target shear in the second component
and affine translations in \(y,z\) remove, respectively, the \(x^3\),
\(y^2z\), and \(yz^2\) coefficients of \(V\).  These are genuine orbit
directions because the relevant leading derivatives are
\(\partial_y(q^2)=2qz\) and \(\partial_z(q^2)=2qy\).
Thus write
\[
\begin{aligned}
W={}&w_0x^2+w_1xy+w_2xz+w_3y^2+w_4yz+w_5z^2,\\
V={}&v_1x^2y+v_2x^2z+v_3xy^2+v_4xyz+v_5xz^2
 +v_6y^3+v_9z^3.
\end{aligned}                                             \tag{4}
\]
No coefficient outside these explicit affine gauges has been discarded.

For completeness, translating the source by \(d\) changes the lower
homogeneous pieces, but the new linear coefficient is \(JF(d)\).  Its
determinant is the same nonzero Keller constant, and the quadratic and
linear coefficients are still completely general when the \(y,z\)
translations are used.

A target shear \(F_1\mapsto F_1+\lambda F_3\) has the exact ledger
\[
\begin{aligned}
U&\mapsto U+\lambda x^3,\\
(H_2)_1&\mapsto(H_2)_1+\lambda W,\\
\operatorname{row}_1(L_0)&\mapsto
\operatorname{row}_1(L_0)+\lambda\operatorname{row}_3(L_0).
\end{aligned}                                             \tag{4a}
\]
The analogous second-component shear changes \(V,(H_2)_2\), and row \(2\).
Both shears have determinant one, so they preserve \(\det L_0\).  Lower
coordinates are relabelled after every such shear.

## 3. Complete degree-six split

Write \(L_0=(\ell_{ij})\), numbered from \(1\), and write
\[
(H_2)_1=u_0x^2+u_1xy+u_2xz+u_3y^2+u_4yz+u_5z^2.
\]
Put
\[
C=A+\frac43w_4.                                           \tag{5}
\]
The raw degree-six identity has the following complete consequences:
\[
\boxed{
w_3=w_5=0,
}                                                         \tag{6}
\]
\[
\boxed{
A(v_1,v_2,v_3,v_5,v_6,v_9)=0,\qquad
Cw_1=Cw_2=0,
}                                                         \tag{7}
\]
and
\[
\boxed{
\begin{aligned}
u_1&=\frac43\ell_{32}+\frac49w_0w_1,&
u_2&=\frac43\ell_{33}+\frac49w_0w_2,\\
u_3&=\frac29w_1^2,&
u_5&=\frac29w_2^2.
\end{aligned}
}                                                         \tag{8}
\]
The coefficients \((u_0,u_4)\), all of \((H_2)_2\), and all entries of
\(L_0\) remain free at this stage.

The supplied exact verifier checks the raw degree-six square coefficients
\[
-\frac{16}{3}w_3^2,\qquad \frac{16}{3}w_5^2,
\]
and the decisive product table after the displayed solve.  The hostile
audit independently substitutes (6)--(8) into every coefficient and
checks the rank-four converse.  Thus the following four cases exhaust the
degree-six variety:
\[
(A,C)\in
(\mathbb C^\times,\mathbb C^\times),\
(\mathbb C^\times,0),\
(0,\mathbb C^\times),\
(0,0).                                                    \tag{9}
\]

Whenever \(w_1=w_2=w_3=w_5=0\), the shear
\(\lambda=-4w_0/3\) removes the tied term \((4/3)w_0x^3\).
In the lower first-component coordinates it sends
\[
\begin{aligned}
u_0&\mapsto u_0-\frac43w_0^2,&
u_4&\mapsto u_4-\frac43w_0w_4,\\
\ell_{1j}&\mapsto\ell_{1j}-\frac43w_0\ell_{3j}.
\end{aligned}                                             \tag{9a}
\]
Every \(u_i,\ell_{ij}\) below is the resulting post-shear coordinate,
relabelled without a prime.

## 4. Case \(A\ne0,\ C\ne0\)

Equation (7) makes
\[
w_1=w_2=0,\qquad V=v_4xq.
\]
After removing the harmless \(x^3\) term from \(U\),
\[
H_3=(Cxq,v_4xq,x^3),\qquad W=w_0p+w_4q.
\]
The degree-five coefficients include
\[
[y^3z^2]E_5=-2C\ell_{32},\qquad
[y^2z^3]E_5=2C\ell_{33}.                                 \tag{10}
\]
They force \(\ell_{32}=\ell_{33}=0\).  The coefficients
\([x^2y^2z]E_5\) and \([x^2yz^2]E_5\) then force
\(\ell_{12}=\ell_{13}=0\).  The first and third rows of \(L_0\) are both
supported in their first entry, so
\[
\det L_0=0.                                               \tag{11}
\]

## 5. Case \(A\ne0,\ C=0\)

Now \(w_4=-3A/4\), while \(w_1,w_2\) initially survive (7).  Degree five
contains
\[
[y^4z]E_5=\frac89w_1^3,\qquad
[yz^4]E_5=-\frac89w_2^3.                                 \tag{12}
\]
Hence \(w_1=w_2=0\).  The same identity gives
\[
\ell_{12}=\frac49w_0\ell_{32},\qquad
\ell_{13}=\frac49w_0\ell_{33}.                            \tag{13}
\]
After its remaining forced coefficients are substituted, degree four has
\[
[y^3z]E_4=-\frac83\ell_{32}^2,\qquad
[yz^3]E_4=\frac83\ell_{33}^2.                             \tag{14}
\]
Thus all four entries in (13)--(14) vanish and again \(\det L_0=0\).

## 6. Case \(A=0,\ C\ne0\)

Here \(w_4=3C/4\) and (7) gives \(w_1=w_2=0\), but the six displayed
noninvariant coefficients of \(V\) remain.  Degree five first forces
\[
v_3=v_5=v_6=v_9=0,\qquad
\ell_{32}=\ell_{33}=0,                                   \tag{15}
\]
and
\[
\ell_{12}=-\frac18C^2v_1,\qquad
\ell_{13}=-\frac18C^2v_2.                                \tag{16}
\]
Put
\[
K=2Cw_0+3u_4.                                             \tag{17}
\]
Here \(u_4\) is the post-shear coefficient from (9a); in the pre-shear
coordinate the same expression is \(3u_4-Cw_0\).
If \(K\ne0\), the coefficients \([x^4y]E_5\) and
\([x^4z]E_5\) kill \(v_1,v_2\), and (16) gives
\(\det L_0=0\).

Suppose \(K=0\).  Degree four gives, for the \(xy,xz,y^2,z^2\)
coefficients \(h_1,h_2,h_3,h_5\) of \((H_2)_2\),
\[
h_1=\frac23v_1w_0,\qquad h_2=\frac23v_2w_0,\qquad
h_3=h_5=0.                                                \tag{18}
\]
The same degree-four identity also imposes the harmless extra products
\[
v_1Q=v_2Q=0,\qquad
Q=9Cv_4+24\ell_{31}-36u_0-32w_0^2.                       \tag{18a}
\]
They only shrink the solution set and are not needed for the exit.
The coefficient \([x^2]E_2\) then becomes
\[
[x^2]E_2=-\frac38C^2(v_1\ell_{23}-v_2\ell_{22}).          \tag{19}
\]
On the other hand, (15)--(16) give the exact polynomial identity
\[
\det L_0=\frac{\ell_{31}}3[x^2]E_2.                       \tag{20}
\]
Thus \(E_2=0\) again forces \(\det L_0=0\), without division by
\(v_1,v_2\), or \(\ell_{31}\).

## 7. Case \(A=C=0\)

Now \(w_4=0\).  The same two cubic coefficients (12) force
\(w_1=w_2=0\).  A target shear removes the remaining
\((4/3)w_0x^3\) from \(U\); it merely reparametrizes the unrestricted
lower first component and first row of \(L_0\).  Degree five then gives
\[
\ell_{12}=-\frac89w_0\ell_{32},\qquad
\ell_{13}=-\frac89w_0\ell_{33},                           \tag{21}
\]
and degree four gives
\[
[y^3z]E_4=-\frac83\ell_{32}^2,\qquad
[yz^3]E_4=\frac83\ell_{33}^2.                             \tag{22}
\]
Equations (21)--(22) make \(\det L_0=0\).

The four cases (9) prove the theorem.

## 8. Verification and disclosure

`verify_line22_marked_critical_infinity_sympy.py` reconstructs the full raw
\(E_7\) kernel, the degree-six square and product table, and the decisive
displayed lower identities through (22).

`verify_line22_marked_critical_infinity_pari.gp`, run through its strict
wrapper, independently expands the raw top identities and all four lower
branches from Jacobian determinants.

The hostile audit's `audit_exact_reconstruct.py` independently checks the
raw ranks and complete gauges, the target-shear ledger, the full
degree-six converse, all four lower branches including (18a), and the
division-free determinant identity (20).  Its fault tests also verify the
Python optimized-mode guard and every strict-PARI-runner outcome.

The exact calculations are evidence about the encoded algebra, not peer
review.  AI systems materially assisted the discovery, case split,
verification code, and exposition.  The hostile audit found no omitted
specialization or scope overreach.
