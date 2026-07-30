# A full-support flag--Bell pencil falsifies reciprocal log convexity

## Status

This note proves two exact results about the proposed square-zero
determinant inequality
\[
 \det G(U,W)\ \stackrel{?}{\geq}\
 \frac{3^{18}}{2^{22}}
 \prod_{i=1}^3\det\rho_i^U\det\rho_i^W.                 \tag{1}
\]

1.  Inequality (1) holds strictly on an explicit two-parameter,
    full-local-support flag--Bell pencil.  The sharp ratio within this
    pencil is an explicitly defined algebraic number
    \[
       \gamma_*=1.04708022452666\ldots>1.                \tag{2}
    \]
    This pencil reproduces the geometry of the closest non-GHZ
    numerical obstruction found in the determinant searches.

2.  The logarithm of the ratio in (1) is **not** convex on all
    reciprocal positive-filter orbits.  At the exact rational point
    \(x=1/10,\ y=1/100\), a determinant-one reciprocal local filter
    has curvature
    \[
     -\frac{9845853439120560320}
             {427988320182198573561}<0.                 \tag{3}
    \]
    All six one-site plane marginals are positive definite there.
    Thus global reciprocal-filter log convexity cannot prove (1).

The failure is specific to the logarithm.  On this entire pencil the
unlogged determinant ratio is strictly convex along the same
reciprocal-filter direction.  At the point in (3), the unlogged ratio
and the normalized determinant defect both have positive curvature.
Consequently this is an exact counterexample to an intermediate proof
mechanism, **not** a negative square-zero matrix and not a
counterexample to (1).

The dependency-free exact checker is
`verification/verify_n3_squarezero_filter_nonconvexity.py`.  It
reconstructs the physical endpoint Gram over
\(\mathbb Q(\omega)[x,y]\), rather than assuming the displayed
formula.

## 1. The physical pencil

Put \(\omega=e^{2\pi i/3}\), and on physical sites \(1,3\) define the
qutrit Bell basis
\[
 |\Phi_{r,s}\rangle
 =\frac1{\sqrt3}\sum_{j=0}^2
   \omega^{sj}|j\rangle_1|j+r\rangle_3,
 \qquad r,s\in\mathbb Z_3.                              \tag{4}
\]
Site \(2\) is a three-valued flag.  For \(x,y>0\), set
\[
\begin{aligned}
 u_0&=|0\rangle_2|\Phi_{0,0}\rangle_{13},\\
 u_1&=\frac{
       x|1\rangle_2|\Phi_{2,1}\rangle_{13}
        +|2\rangle_2|\Phi_{0,0}\rangle_{13}}
       {\sqrt{1+x^2}},\\
 w_0&=|0\rangle_2|\Phi_{1,1}\rangle_{13},\\
 w_1&=\frac{
       y|1\rangle_2|\Phi_{0,2}\rangle_{13}
        +|2\rangle_2|\Phi_{1,1}\rangle_{13}}
       {\sqrt{1+y^2}}.
\end{aligned}                                            \tag{5}
\]
The Bell labels paired at each flag are distinct.  Hence the four
vectors in (5) are orthonormal.  In particular
\[
 U=(u_0,u_1),\qquad W=(w_0,w_1),\qquad U^\dagger W=0.    \tag{6}
\]

Let
\[
 E_{ab}=|u_a\rangle\langle w_b|,\qquad
 G_{ab,cd}=
 \langle E_{ab},L^{\otimes3}(E_{cd})\rangle_{\rm HS},
 \quad L(A)=A-\tfrac12\operatorname{Tr}(A)I_3.           \tag{7}
\]
Indices are ordered \(00,01,10,11\).

For the contraction it is convenient to omit the denominators
\(\sqrt{1+x^2}\) and \(\sqrt{1+y^2}\) from the second columns.  The
resulting logical Gram is
\[
 \widetilde G=
 \begin{pmatrix}
 \frac13&0&0&-\frac{xy+4}{12}\\
 0&\frac{2(y^2+1)}3&0&0\\
 0&0&\frac{2(x^2+1)}3&0\\
 -\frac{xy+4}{12}&0&0&
 \frac{2x^2y^2+4x^2-xy+4y^2+2}{6}
 \end{pmatrix}.                                         \tag{8}
\]
This follows by direct partial-trace contraction.  The exact checker
constructs all four \(27\times27\) transition matrices and verifies
(8) coefficient by coefficient in
\(\mathbb Q(\omega)[x,y]\).

Put
\[
 A=1+x^2,\qquad B=1+y^2,\qquad
 D=\operatorname{diag}
 \left(1,B^{-1/2},A^{-1/2},(AB)^{-1/2}\right).           \tag{9}
\]
Normalization of the two second columns gives
\[
 G=D\widetilde GD.                                      \tag{10}
\]
Taking the determinant in (8) yields
\[
\begin{aligned}
 P(x,y)&=15x^2y^2+32x^2-16xy+32y^2,\\
 \det\widetilde G&=\frac{AB}{324}P(x,y),\\
 \boxed{\quad
 \det G=\frac{P(x,y)}{324AB}.
 \quad}                                                  \tag{11}
\end{aligned}
\]

## 2. Every local marginal has full rank

Every qutrit Bell state has one-site marginal \(I_3/3\).  Orthogonal
flag values eliminate cross terms on sites \(1,3\); orthogonal Bell
labels eliminate the flag cross terms on site \(2\).  Therefore
\[
\begin{aligned}
 \rho_1^U=\rho_3^U=\rho_1^W=\rho_3^W&=\frac23I_3,\\
 \rho_2^U&=
 \operatorname{diag}\left(1,\frac{x^2}{1+x^2},
                             \frac1{1+x^2}\right),\\
 \rho_2^W&=
 \operatorname{diag}\left(1,\frac{y^2}{1+y^2},
                             \frac1{1+y^2}\right).
\end{aligned}                                            \tag{12}
\]
Thus all six marginals are positive definite for \(x,y>0\), and
\[
 \prod_i\det\rho_i^U\det\rho_i^W
 =
 \left(\frac8{27}\right)^4
 \frac{x^2y^2}{A^2B^2}.                                 \tag{13}
\]

Combining (11)--(13), the ratio of the two sides of (1) is
\[
 \boxed{\quad
 {\cal R}(x,y)
 =\frac{256\,AB\,P(x,y)}{59049\,x^2y^2}.
 \quad}                                                  \tag{14}
\]
This also verifies the normalization \(3^{18}/2^{22}\): if all six
marginals are \(2I_3/3\), their determinant product is
\(2^{18}/3^{18}\), so the proposed right side is \(1/16\).

## 3. Exact product-bound theorem on the pencil

Let
\[
 z=xy>0,\qquad s=x^2+y^2\geq2z.                         \tag{15}
\]
Then
\[
 P=15z^2-16z+32s,\qquad AB=1+z^2+s.                    \tag{16}
\]
Both factors are positive and increasing in \(s\) on \(s\geq2z\).
It follows that
\[
 ABP\geq(1+z)^2(15z^2+48z).                            \tag{17}
\]
Hence \({\cal R}(x,y)\geq1\) follows from
\[
 F(z):=
 256(15z+48)(1+z)^2-59049z>0.                          \tag{18}
\]
Expanding,
\[
 F(z)=3840z^3+19968z^2-30633z+12288.                   \tag{19}
\]
There is a short rational positivity certificate.  Put
\(r=13/20\).  For \(z=r+t,\ t\geq0\),
\[
 F(r+t)
 =3840t^3+27456t^2+\frac{963}{5}t
  +\frac{186759}{100}>0.                                \tag{20}
\]
For \(z=r-t,\ 0\leq t\leq r\),
\[
\begin{aligned}
 F(r-t)
 &=t^2(27456-3840t)
   +\frac{186759}{100}-\frac{963}{5}t\\
 &\geq\frac{8712}{5}>0.                                 \tag{21}
\end{aligned}
\]
This proves (1), strictly, for every member of (5).

The sharp ratio inside the pencil is also exact.  Equality in (17)
requires \(x=y=\sqrt z\).  On this line,
\[
 {\cal R}
 =\frac{256}{59049}
 \left(15z^2+78z+111+\frac{48}{z}\right).               \tag{22}
\]
The bracket is strictly convex.  Its unique minimum occurs at the
positive root \(z_*\) of
\[
 5z_*^3+13z_*^2-8=0.                                   \tag{23}
\]
Therefore
\[
 \boxed{\quad
 \gamma_*=
 \frac{256}{59049}
 \left(15z_*^2+78z_*+111+\frac{48}{z_*}\right)
 =1.04708022452666\ldots .
 \quad}                                                  \tag{24}
\]
The corresponding normalized flag weight is
\[
 \frac{z_*}{1+z_*}=0.410607747859283\ldots,              \tag{25}
\]
which is the weight repeatedly seen in the near-active flag--Bell
optimization.  Thus this numerical attractor has an exact algebraic
explanation and a certified \(4.7\%\) determinant margin.

## 4. Reciprocal filtering and negative log curvature

On flag site \(2\), apply
\[
 T_t=\operatorname{diag}(1,e^t,e^{-t})
 \quad\hbox{to }U,\qquad
 T_t^{-1}\quad\hbox{to }W,                              \tag{26}
\]
and whiten the two logical columns on each side.  Positivity of
\(T_t\) and reciprocity preserve \(U^\dagger W=0\).  Within (5), the
result is exactly
\[
 x_t=xe^{2t},\qquad y_t=ye^{-2t}.                        \tag{27}
\]
Thus
\[
 z_t=x_ty_t=z,\qquad
 s_t=x^2e^{4t}+y^2e^{-4t}.                              \tag{28}
\]
Up to a constant independent of \(t\), (14) becomes
\[
 {\cal R}(t)
 =
 \frac{256}{59049z^2}
 \underbrace{(15z^2-16z+32s_t)}_{p_t}
 \underbrace{(1+z^2+s_t)}_{q_t}.                        \tag{29}
\]

Take
\[
 x=\frac1{10},\qquad y=\frac1{100}.                     \tag{30}
\]
Then
\[
\begin{aligned}
 z&=\frac1{1000},&
 s_0&=\frac{101}{10000},\\
 \dot s_0&=\frac{99}{2500},&
 \ddot s_0&=\frac{101}{625},\\
 p_0&=\frac{61443}{200000},&
 q_0&=\frac{1010101}{1000000}.
\end{aligned}                                            \tag{31}
\]
Twice differentiating the logarithm of (29) gives
\[
 \left.\frac{d^2}{dt^2}\log{\cal R}(t)\right|_{t=0}
 =
 32\frac{\ddot s_0p_0-32\dot s_0^2}{p_0^2}
 +\frac{\ddot s_0q_0-\dot s_0^2}{q_0^2}.                \tag{32}
\]
Exact substitution yields
\[
 \boxed{\quad
 \left.(\log{\cal R})''\right|_{0}
 =
 -\frac{9845853439120560320}
        {427988320182198573561}<0.
 \quad}                                                  \tag{33}
\]
At this point the two nontrivial marginal determinants are
\[
 \det\rho_2^U=\frac{100}{10201},\qquad
 \det\rho_2^W=\frac{10000}{100020001},                  \tag{34}
\]
so (33) is an interior full-support obstruction, not a singular
boundary artifact.

The determinant inequality itself is very far from failing:
\[
 {\cal R}\left(\frac1{10},\frac1{100}\right)
 =\frac{27583838108}{20503125}
 =1345.3479949\ldots>1.                                 \tag{35}
\]

## 5. What survives the obstruction

The unlogged ratio has a better curvature identity.  From (29),
\[
 {\cal R}''
 =\frac{256}{59049z^2}
 \left[
 64(\dot s)^2+(32q+p)\ddot s
 \right].                                               \tag{36}
\]
Since
\[
 32q+p
 =32+47z^2-16z+64s
 \geq32+47z^2+112z>0,                                  \tag{37}
\]
and \(\ddot s>0\), the unlogged ratio is strictly convex along every
reciprocal-filter path (26) in this pencil.  At (30),
\[
 {\cal R}''
 =\frac{859750796032}{36905625}>0.                      \tag{38}
\]
The normalized defect
\[
 \det G-\frac{3^{18}}{2^{22}}
 \prod_i\det\rho_i^U\det\rho_i^W
\]
also has positive curvature at (30), namely
\[
 \frac{1294370873331706238711800}
      {84322645437596652728132481}>0.                   \tag{39}
\]
Equation (39) is only a pointwise check; no global convexity of the
normalized defect is claimed.

The exact conclusion is therefore:

* a proof based on a globally positive Hessian of the **logarithmic**
  determinant ratio is impossible;
* the unlogged ratio remains a viable convex quantity and survives
  this exact hostile pencil;
* reciprocal filtering removes the imbalance \(x/y\), but preserves
  the orbit invariant \(z=xy\); the residual algebraic inequality in
  \(z\), not filter balancing alone, supplies the strict margin.

The last point is the structural lesson for the unrestricted
determinant problem.  Any global filter argument must retain and
control the invariants of reciprocal-filter orbits after balancing.
