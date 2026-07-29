# Exact sixth-order theorem on the two 27-dimensional boundary components

## 1. Statement

Work at
\[
C_0=|000\rangle\langle110|+|001\rangle\langle111|
\]
in the polar Stiefel chart used in
`agent_n3_boundary_effective_quartic_sos.md`.  Number the four linear
components of the effective-quartic zero set as in the exact
zero-decomposition certificate.  Components \(L_2,L_3\) are the two
27-dimensional components.  They are exchanged by swapping the first
two physical sites, so it is enough to analyze \(L_2\).

In the component basis \(c_0,\ldots,c_{26}\), put
\[
\begin{aligned}
 z&=(c_{14}+c_{15})+i(c_{16}-c_{17}),\\
 w&=(w_0,\ldots,w_5)
   =(c_4+c_5,c_6-c_7,c_8,c_9,c_{10},c_{11}),\\
 d&=c_{18}+ic_{19}.
\end{aligned}
\tag{1}
\]
The remaining fifteen real coordinates are tangent to local-unitary,
local-plane, or phase orbits and do not enter the invariant secondary
minimum.

Define three complex numbers
\[
 \xi=w_0+iw_1,\qquad
 \beta=w_2+iw_3,\qquad
 \chi=w_4+iw_5
\tag{2}
\]
and
\[
\begin{aligned}
 t&=\frac54\left(|\xi|^2+2|\beta|^2+2|\chi|^2\right),\\
 \eta&=\frac14\xi^2+\beta\chi,\\
 \Delta&=t^2-|\eta|^2.
\end{aligned}
\tag{3}
\]

Let \(\sigma_6\) denote the order-six Lyapunov--Schmidt minimum after
the 149 positive Hessian directions, the 28 directions normal to
\(L_2\) in the primary kernel, and all permitted order-three
corrections have been minimized exactly.

**Theorem.**  If \(w\ne0\), then
\[
\boxed{
\sigma_6(z,w,d)
=
\frac{4t}{25\Delta}
\left[
(3t^2-5|\eta|^2)|z|^2|d|^2
+2t\,\operatorname{Re}(\eta z^2d^2)
\right].
}
\tag{4}
\]
The continuous value at \(w=0\) is zero.  Moreover
\[
 \sigma_6(z,w,d)\ge0,
\tag{5}
\]
and equality holds exactly when
\[
 z=0,\qquad w=0,\qquad\text{or}\qquad d=0.
\tag{6}
\]
The same theorem holds on \(L_3\) after interchanging physical sites
one and two.

Thus neither 27-dimensional component has a negative sixth-order
continuation.  The sets \(z=0\) and \(w=0\) are the already known
intersections with \(L_1\) and \(L_0\), respectively.  The set \(d=0\)
is a new 25-dimensional sixth-order-flat branch.  Section 6 proves
that this entire branch also integrates to an exact-zero family, so
there is no order-eight obstruction on it.

## 2. Intrinsic meaning of the quotient variables

After quotienting local-plane motions, the first-order frames stay in
three qubit supports.  The internal block in the left frame is a
complex \(2\times2\) matrix \(B\), and the corresponding block in the
right frame is its qubit spin flip.  The two real combinations
\[
 c_4-c_5,\qquad c_6+c_7
\]
are precisely the scalar part of \(B\).  They are induced by an
infinitesimal local unitary and can be removed.  The six coordinates
\(w\) in (1) are the traceless part of \(B\).

The four coordinates \(c_0,\ldots,c_3\), the eight coordinates
\(c_{12},c_{13},c_{20},\ldots,c_{25}\), and \(c_{26}\) are,
respectively, common local-plane motions and a phase motion.  Since
\(Q_3\) is invariant under local isometries and scalar phase, they do
not affect the invariant Lyapunov--Schmidt coefficient.  This explains
the exact reduction from 27 to
\[
 2+6+2=10
\]
real first-order coordinates.

## 3. Exact two-dimensional Schur core

The direct Gaussian-rational expansion initially gives a quadratic
order-six minimization in 177 correction variables.  The 149
order-three positive-Hessian variables form a constant diagonal block
and can be completed square by square.  Of the remaining 28
normal-kernel variables, the twelve genuinely qutrit directions have
zero linear term and are uncoupled from the active block.  Completing
the other fourteen squares leaves two real variables \(h\in\mathbb
R^2\).

By the phase covariance
\[
 (z,d)\longmapsto(e^{i\theta}z,e^{-i\theta}d)
\tag{7}
\]
and homogeneity, it is enough to set \(z=1\).  Write
\[
 \eta=x+iy.
\tag{8}
\]
The exact remaining form is
\[
 h^{\mathsf T}Kh+h^{\mathsf T}L d_{\mathbb R}
  +d_{\mathbb R}^{\mathsf T}C d_{\mathbb R},
\qquad
d_{\mathbb R}=(\operatorname{Re}d,\operatorname{Im}d)^{\mathsf T},
\tag{9}
\]
where
\[
\begin{aligned}
 K&=\frac12
 \begin{pmatrix}t+x&y\\y&t-x\end{pmatrix},\\
 L&=
 \begin{pmatrix}
 x+t/5&-y\\
 y&x-t/5
 \end{pmatrix},\\
 C&=JKJ,\qquad J=\operatorname{diag}(1,-1).
\end{aligned}
\tag{10}
\]
All entries in (10) are quadratic polynomials in the six real
coordinates \(w\).  In the original real coordinates they are
\[
\begin{aligned}
t&=\frac54(w_0^2+w_1^2+2w_2^2+2w_3^2+2w_4^2+2w_5^2),\\
x&=\frac14(w_0^2-w_1^2+4w_2w_4-4w_3w_5),\\
y&=\frac12w_0w_1+w_2w_5+w_3w_4.
\end{aligned}
\tag{11}
\]
Equations (9)--(11) are obtained by direct completion of rational
squares; no numerical optimizer is used.

The determinant is
\[
 \det K=\frac14(t^2-x^2-y^2)=\frac{\Delta}{4}.
\tag{12}
\]
For \(w\ne0\), \(K\) is positive definite by the estimate in the next
section.  Minimizing (9) in \(h\) gives
\[
 H=C-\frac14L^{\mathsf T}K^{-1}L.
\tag{13}
\]
A two-by-two multiplication yields
\[
H=\frac{4t}{25\Delta}
\begin{pmatrix}
3t^2+2tx-5|\eta|^2&-2ty\\
-2ty&3t^2-2tx-5|\eta|^2
\end{pmatrix}.
\tag{14}
\]
Consequently
\[
d_{\mathbb R}^{\mathsf T}Hd_{\mathbb R}
=\frac{4t}{25\Delta}
\left[
(3t^2-5|\eta|^2)|d|^2
+2t\operatorname{Re}(\eta d^2)
\right].
\tag{15}
\]
Restoring \(z\) through (7) and homogeneity replaces \(d\) by \(zd\),
which is exactly (4).

## 4. Positivity and equality

The key estimate is elementary but sharp:
\[
\begin{aligned}
|\eta|
&\le\frac14|\xi|^2+|\beta||\chi|\\
&\le\frac14|\xi|^2+\frac12(|\beta|^2+|\chi|^2)
=\frac15t.
\end{aligned}
\tag{16}
\]
In particular, if \(w\ne0\), then \(t>0\) and
\[
\Delta\ge\frac{24}{25}t^2>0.
\tag{17}
\]
Using
\[
\operatorname{Re}(\eta z^2d^2)
\ge-|\eta||z|^2|d|^2
\tag{18}
\]
in (4), and writing \(u=|\eta|/t\le1/5\), gives
\[
\begin{aligned}
&(3t^2-5|\eta|^2)|z|^2|d|^2
+2t\operatorname{Re}(\eta z^2d^2)\\
&\qquad\ge
t^2(3-2u-5u^2)|z|^2|d|^2\\
&\qquad=
t^2(3-5u)(1+u)|z|^2|d|^2>0
\end{aligned}
\tag{19}
\]
whenever \(z,w,d\) are all nonzero.  This proves (5) and the equality
classification (6).

Equivalently, the eigenvalue ratio of the core \(K\) is at most
\[
\frac{t+|\eta|}{t-|\eta|}\le\frac32,
\tag{20}
\]
whereas positivity of the final Schur complement would only require
that ratio to be at most \(4\).  The certificate therefore has a
substantial exact margin off the three zero branches.

## 5. Verification

The discovery/derivation program
`discovery/analyze_n3_boundary_l2_reduced_form.py` starts from the exact
polar-chart contraction of \(Q_3\), eliminates the 149 and then the
fourteen correction directions with rational arithmetic, and checks
the matrices \(K,L,C\).

The small verifier
`verification/verify_n3_boundary_l2_secondary_core.py` checks the
closed two-by-two identities, the determinant, the Schur complement,
the invariant formula, and exact sample comparisons against the full
177-variable elimination.

The independent symbolic verifier
`verification/verify_n3_boundary_l2_d0_exact_family.py` checks the
adjugate, Gram-product, Cayley--Hamilton, and fully-traceless-block
identities used for the exact \(d=0\) family.

## 6. Exact integration of the \(d=0\) branch

The remaining sixth-order zero branch is not a new higher-order
obstruction.  It is tangent to the following exact-zero family.

In the canonical gauge used in (1), associate to \(w\) the matrix
\[
B=
\begin{pmatrix}
-w_0+iw_1&w_2-iw_3\\
w_4-iw_5&0
\end{pmatrix}.
\tag{21}
\]
Put
\[
D=B-(\operatorname{Tr}B)I=-\operatorname{adj}B,
\qquad A=D^\dagger.
\tag{22}
\]
For a real path parameter \(s\), define unnormalized two-frames
\[
\begin{aligned}
\widetilde U(s)
&=\left(|0\rangle+\frac{s\overline z}{2}|1\rangle\right)_1
\otimes
\left(|0\rangle_2\otimes I_2+s|1\rangle_2\otimes B\right),\\
\widetilde V(s)
&=\left(\frac{sz}{2}|0\rangle+|1\rangle\right)_1
\otimes
\left(s|0\rangle_2\otimes A+|1\rangle_2\otimes I_2\right).
\end{aligned}
\tag{23}
\]
Here an expression such as
\(|0\rangle_2\otimes I_2+s|1\rangle_2\otimes B\) is a map from the
logical qubit to physical sites two and three.  Polar-normalize the
frames:
\[
U=\widetilde U(\widetilde U^\dagger\widetilde U)^{-1/2},
\qquad
V=\widetilde V(\widetilde V^\dagger\widetilde V)^{-1/2}.
\tag{24}
\]
Then \(U,V\) are isometries, \(C(s)=UV^\dagger\) is a rank-two partial
isometry, and
\[
Q_3(C(s))=0
\qquad\text{for every real }s.
\tag{25}
\]
Its derivative at \(s=0\) is precisely the canonical \(L_2\) direction
with coordinates \((z,w,d=0)\).  Applying the fifteen local-plane,
local-unitary, and phase symmetries gives every \(d=0\) direction in
\(L_2\).

To prove (25), set \(M=B^\dagger B\).  From (22),
\[
A^\dagger A=DD^\dagger=\operatorname{adj}(B^\dagger B)
=\operatorname{adj}M.
\tag{26}
\]
For every \(2\times2\) matrix \(M\),
\[
M+\operatorname{adj}M=(\operatorname{Tr}M)I,
\qquad
M\operatorname{adj}M=(\det M)I.
\tag{27}
\]
Consequently
\[
(I+s^2M)(I+s^2\operatorname{adj}M)
=
\left(1+s^2\operatorname{Tr}M+s^4\det M\right)I.
\tag{28}
\]
The two factors are commuting positive matrices.  Their inverse square
roots therefore multiply to a scalar.  The two site-one vectors in
(23) also have the same squared norm
\(1+s^2|z|^2/4\).  It follows that, up to a positive scalar,
\[
C(s)=|a(s)\rangle\langle b(s)|_1\otimes E_{23}(s),
\tag{29}
\]
where the four site-two blocks of \(E_{23}\) are
\[
E_{00}=sD,\qquad
E_{01}=I,\qquad
E_{10}=s^2BD,\qquad
E_{11}=sB.
\tag{30}
\]
Cayley--Hamilton gives
\[
D-B=-(\operatorname{Tr}B)I,\qquad
BD=-(\det B)I.
\tag{31}
\]
Thus the off-diagonal block \(E_{01}\), the off-diagonal block
\(E_{10}\), and the difference of the diagonal blocks
\(E_{00}-E_{11}\) are all scalar matrices on site three.  Equivalently,
\[
(L_2\otimes L_2)(E_{23})=0.
\tag{32}
\]
Hence \(Q_2(E_{23})=0\), and tensor factorization gives (25).

The exact continuation program
`discovery/analyze_n3_boundary_l2_d0_continuation.py` independently
solves the 177-variable secondary system and obtains zero Taylor
coefficients through order twelve.  The calculation is only an audit:
equations (21)--(32) prove vanishing to every order.

## 7. Consequence for the canonical boundary point

All zeros of the exact sixth-order form now have geometric
integrations:

1. \(z=0\) lies in the spin-flip exact-zero family tangent to \(L_1\);
2. \(w=0\) lies in the factorized exact-zero family tangent to \(L_0\);
3. \(d=0\) lies in the adjugate two-copy exact-zero family (23).

Away from this union, the sixth-order coefficient is strictly positive.
This completes the componentwise formal obstruction analysis through
the first nonzero reduced order on both \(L_2,L_3\).  It is still a
local theorem at \(C_0\), not by itself the unrestricted three-copy
positivity theorem.

## 8. Uniformity audit: sectorial positivity, not yet a full neighborhood

The proof gives a useful quantitative strengthening.  From
\(|\eta|/t\le1/5\), (19), and \(\Delta\le t^2\),
\[
\begin{aligned}
\sigma_6
&\ge
\frac{48t^3}{125\Delta}|z|^2|d|^2\\
&\ge
\frac{48t}{125}|z|^2|d|^2\\
&\ge
\boxed{\frac{12}{25}\,
|z|^2\|w\|_{\mathbb R^6}^2|d|^2}.
\end{aligned}
\tag{33}
\]
Consequently, on every compact subset of the projectivized component
that stays a positive distance from
\[
\{z=0\}\cup\{w=0\}\cup\{d=0\},
\tag{34}
\]
the sixth-order Lyapunov--Schmidt minimum has a uniform positive gap.
The analytic Taylor remainder is then uniformly dominated for a
sufficiently small chart radius.  This proves genuine local
nonnegativity in every such closed conic sector.

It does **not** yet prove that one whole neighborhood of \(C_0\) is
nonnegative.  The reason is precise: the lower bound (33) degenerates
quadratically at each exact-zero branch.  For example, a sequence in
which \(d\) tends to zero at the same time as the chart radius moves
the first possible comparison from order six to order eight or
higher.  The exact family (23) proves that the center value at \(d=0\)
is zero, but it does not by itself give a uniform positive normal-form
estimate for perturbations transverse to that family.  The issue is
especially delicate where two or three exact-zero families intersect.

A full neighborhood theorem therefore requires one additional,
strictly smaller local result:

> Construct tubular coordinates around the union of the three
> exact-zero families and prove that the reduced functional is bounded
> below by a positive quadratic form in the transverse coordinates,
> with constants compatible at all pairwise and triple intersections.

Equivalently, one can perform a finite blow-up of the three factors in
(33) and prove nonnegativity on every exceptional chart.  Neither this
uniform tubular estimate nor the equivalent blow-up analysis is
claimed here.  Thus the exact result is a componentwise sixth-order
theorem plus all-order integration of its zero directions, not yet an
actual full-neighborhood theorem.
