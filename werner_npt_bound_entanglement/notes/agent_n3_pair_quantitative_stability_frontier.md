# Quantitative stability at the rank-one pair-sector frontier

## Status

This note isolates the exact quantitative estimate needed to upgrade
the sharp rank-one theorem to the strengthened pair-sector theorem.  It
also proves:

1. exact quadratic normal stability at generic points of both
   classified rank-one equality components;
2. an exact quartic obstruction at a singular intersection of those
   components;
3. a global compactness theorem excluding a whole neighborhood of the
   rank-one boundary from any counterexample to the original
   pair-sector Ky--Fan inequality.

It does **not** prove the sharp global stability estimate.  In
particular, the generic Hessian estimates cannot simply be made
uniform because the equality variety is singular where its two
components meet.

The independent exact checker is
`verification/verify_n3_pair_quantitative_stability_frontier.py`.

## 1. The exact global stability target

Let \(D\) be a qutrit pair-sector operator, normalized by
\[
 \|D\|_2=1,
\]
and let
\[
 d_1\ge d_2\ge\cdots
\]
be its singular values.  Define the sharp rank-one slack
\[
 \varepsilon=\frac49-d_1^2\ge0.                         \tag{1}
\]
In the balanced branch \(d_2\ge d_1/2\), the strengthened pair-sector
theorem is
\[
 3(d_1^2-d_1d_2+d_2^2)\le1.                            \tag{2}
\]
Substituting
\[
 1=\frac94(d_1^2+\varepsilon)
\]
gives the identity
\[
\boxed{
1-3(d_1^2-d_1d_2+d_2^2)
=\frac34\left(3\varepsilon-(2d_2-d_1)^2\right).}        \tag{3}
\]
Thus the complete balanced branch is exactly equivalent to the sharp
stability inequality
\[
\boxed{(2d_2-d_1)^2\le3\varepsilon.}                   \tag{4}
\]

If
\[
 \frac{d_2}{d_1}=\frac12+t,\qquad t\ge0,
\]
then (4) is equivalently
\[
\boxed{
\varepsilon\ge
\frac{16t^2}{27+36t^2}.}                               \tag{5}
\]
This is the precise modulus a global argument must prove.  Merely
showing \(d_2\to d_1/2\) as \(\varepsilon\to0\) is insufficient; the
required rate is square-root with the sharp coefficient in (4).

## 2. The rank-one slack as a polynomial SOS

For arbitrary \(x,y\in(\mathbb C^3)^{\otimes3}\), set
\[
 E(x,y)=\Pi _2(|x\rangle\langle y|)
\]
and define the homogeneous slack
\[
 \Delta(x,y)
 =4\|x\|^2\|y\|^2-9\|E(x,y)\|_2^2.                    \tag{6}
\]
Let \(F_i\) swap the \(i\)-th factors of two replicas.  The exact
rank-one SOS is
\[
\begin{aligned}
\Delta(x,y)
={}&\sum_{i<j}
\langle x\otimes y|(I-F_i)(I-F_j)|x\otimes y\rangle\\
&+\langle x\otimes y|
(I-F_1)(I-F_2)(I-F_3)|x\otimes y\rangle.               \tag{7}
\end{aligned}
\]

At an equality pair \((x_0,y_0)\), put
\[
 x=x_0+t\xi,\qquad y=y_0+t\eta.
\]
Since every square in (7) vanishes at \(t=0\), the quadratic
coefficient is
\[
\begin{aligned}
{\cal H}_{x_0,y_0}(\xi,\eta)
={}&\frac14\sum_{i<j}
\left\|(I-F_i)(I-F_j)
(\xi\otimes y_0+x_0\otimes\eta)\right\|^2\\
&+\frac18
\left\|\prod_{i=1}^3(I-F_i)
(\xi\otimes y_0+x_0\otimes\eta)\right\|^2.             \tag{8}
\end{aligned}
\]
This is a positive semidefinite Hermitian Gram form over the
\(54\)-dimensional complex variation space.

## 3. Generic product--tangent stability

Consider the exact equality pair
\[
\begin{aligned}
x_{\rm p}&=|000\rangle,\\
y_{\rm p}&=|000\rangle+|100\rangle+|010\rangle+|001\rangle.
\end{aligned}                                          \tag{9}
\]
This is a generic point of the product--tangent component: the tangent
vector has nonzero variation at every local site and has no common
local factor with \(x_{\rm p}\).

### Proposition 3.1

The Gram form (8) at (9) has
\[
\boxed{\operatorname{rank}{\cal H}_{\rm p}=40,\qquad
\dim\ker{\cal H}_{\rm p}=14.}                          \tag{10}
\]
Moreover,
\[
\boxed{
{\cal H}_{\rm p}(\xi,\eta)
\ge\frac12
\operatorname{dist}\!\left((\xi,\eta),
\ker{\cal H}_{\rm p}\right)^2.}                        \tag{11}
\]

#### Proof

Multiply the matrix of (8) by \(8\); call the resulting integral Gram
matrix \(G_{\rm p}\).  Exact row reduction gives nullity \(14\).
Its characteristic polynomial is
\[
\begin{aligned}
\chi_{\rm p}(\lambda)
={}&\lambda^{14}(\lambda-32)^3(\lambda-8)^2
(\lambda^2-160\lambda+4032)\\
&\cdot(\lambda^2-40\lambda+192)^3\\
&\cdot(\lambda^3-168\lambda^2+6272\lambda-38400)\\
&\cdot(\lambda^4-200\lambda^3+11520\lambda^2
        -215552\lambda+942080)^3\\
&\cdot(\lambda^4-200\lambda^3+12032\lambda^2
        -264704\lambda+1781760)^3.                    \tag{12}
\end{aligned}
\]
The matrix is a Gram matrix and hence positive semidefinite.  Exact
Sturm counting applied to (12) gives fourteen roots in \([0,4]\), all
at zero.  Thus every nonzero eigenvalue of \(G_{\rm p}\) is strictly
larger than \(4\).  Dividing by \(8\) proves (10)--(11). \(\square\)

The affine cone of product vectors has complex dimension
\[
 3+3+3-2=7.
\]
Its tangent fiber also has dimension \(7\), so the classified
product--tangent incidence variety has dimension \(14\).  Hence the
kernel in (10) is exactly its tangent space.  The equality component
is smooth at (9), and the ordinary implicit-function and Taylor
estimates imply: for every \(c<1/2\), in a sufficiently small
neighborhood of (9),
\[
 \Delta(x,y)\ge
 c\,\operatorname{dist}\bigl((x,y),{\cal E}_{\rm p}\bigr)^2,   \tag{13}
\]
where \({\cal E}_{\rm p}\) is the product--tangent equality component.

## 4. Generic common-factor stability

Now take
\[
\begin{aligned}
x_{\rm b}&=|000\rangle+2|011\rangle,\\
y_{\rm b}&=|000\rangle+|001\rangle+|010\rangle-2|011\rangle.
\end{aligned}                                          \tag{14}
\]
The vectors share their first local factor.  Their two-site
coefficient matrices are
\[
 X=\begin{pmatrix}1&0\\0&2\end{pmatrix},\qquad
 Y=\begin{pmatrix}1&1\\1&-2\end{pmatrix},              \tag{15}
\]
and
\[
 \operatorname{Tr}(X^{-1}Y)=1-1=0.
\]
Thus (14) is a generic point of the common-factor equality component.

### Proposition 4.1

At (14),
\[
\boxed{\operatorname{rank}{\cal H}_{\rm b}=41,\qquad
\dim\ker{\cal H}_{\rm b}=13,}                          \tag{16}
\]
and
\[
\boxed{
{\cal H}_{\rm b}(\xi,\eta)
\ge2\,
\operatorname{dist}\!\left((\xi,\eta),
\ker{\cal H}_{\rm b}\right)^2.}                        \tag{17}
\]

#### Proof

Let \(G_{\rm b}=8{\cal H}_{\rm b}\).  Exact row reduction gives
nullity \(13\), and
\[
\begin{aligned}
\chi_{\rm b}(\lambda)
={}&\lambda^{13}(\lambda-232)^2(\lambda-152)^2
(\lambda-96)(\lambda^2-96\lambda+1664)^5\\
&\cdot(\lambda^4-480\lambda^3+77952\lambda^2
        -4938240\lambda+94416896)^4\\
&\cdot(\lambda^5-480\lambda^4+75456\lambda^3
        -4900864\lambda^2+129196032\lambda
        -1132462080)^2.                               \tag{18}
\end{aligned}
\]
Exact Sturm counting gives thirteen roots in \([0,16]\), all at
zero.  Since \(G_{\rm b}\) is positive semidefinite, every nonzero
eigenvalue is strictly larger than \(16\).  Division by \(8\) proves
(16)--(17). \(\square\)

The component dimension is also \(13\).  Indeed:

* the common local line contributes \(\dim\mathbb P^2=2\);
* the two common two-dimensional row and column supports contribute
  \(2+2\);
* the invertible \(X\) contributes \(4\);
* \(Y\), subject to its one polarized-determinant equation,
  contributes \(3\).

Thus the kernel in (16) is exactly the tangent space to the classified
common-factor component.  As above, for every \(c<2\), there is a
neighborhood of (14) on which
\[
 \Delta(x,y)\ge
 c\,\operatorname{dist}\bigl((x,y),{\cal E}_{\rm b}\bigr)^2.   \tag{19}
\]

Equations (13) and (19), combined with the previously proved uniform
boundary certificate \(s_2(E)\le2/9\), give a local square-root
modulus
\[
 s_2(E(x,y))\le\frac29+C\sqrt{\Delta(x,y)}              \tag{20}
\]
near every generic point of either component.  The constant \(C\)
can be chosen locally, but the present argument does not give the
sharp global coefficient required by (4).

## 5. Exact quartic obstruction at a singular intersection

The two equality components meet at
\[
 x_0=|000\rangle,\qquad y_0=|100\rangle.                \tag{21}
\]
This point is itself spectrally sharp.  Directly,
\[
 E(x_0,y_0)
 =|0\rangle\langle1|\otimes
 \left(q\otimes p+p\otimes q\right),                   \tag{22}
\]
where
\[
 p=\frac13I,\qquad q=|0\rangle\langle0|-\frac13I.
\]
Hence
\[
 s_1(E)=\frac49,\qquad s_2(E)=\frac29.                 \tag{23}
\]

At (21), the Hessian (8) has
\[
 \operatorname{rank}{\cal H}_{0}=36,\qquad
 \dim\ker{\cal H}_{0}=18,                              \tag{24}
\]
larger than at either generic component.  This is not a harmless
coordinate artifact.  Consider the exact curve
\[
\begin{aligned}
x(t)&=|000\rangle+t|101\rangle,\\
y(t)&=|100\rangle+t|010\rangle.                        \tag{25}
\end{aligned}
\]
Its velocity belongs to \(\ker{\cal H}_0\), but for \(t\ne0\) the
pair is not on either equality component.  Direct substitution in
the SOS (7) gives
\[
\boxed{\Delta(x(t),y(t))=4t^4.}                        \tag{26}
\]
After normalizing both vectors, this becomes
\[
\boxed{
\Delta\!\left(
\frac{x(t)}{\sqrt{1+t^2}},
\frac{y(t)}{\sqrt{1+t^2}}
\right)
=\frac{4t^4}{(1+t^2)^2}.}                              \tag{27}
\]

Thus the first nonzero slack at this sharp intersection is quartic.
The generic normal Hessians in Sections 3--4 cannot be patched into a
uniform proof without additional compatibility information at their
intersections.  Equation (27) does not disprove a distance-to-the-full-
equality-variety error bound—the nearest equality point may itself
move at order \(t^2\)—but it proves that the Hessian at a fixed
intersection is insufficient.

## 6. A global compactness exclusion for the original pair theorem

Although the sharp rate (4) remains open, the equality classification
has an immediate global consequence.

### Theorem 6.1

There exists \(\varepsilon_0>0\) such that every pair-sector operator
\(D\) with
\[
 \|D\|_2=1,\qquad
 d_1(D)^2\ge\frac49-\varepsilon_0                      \tag{28}
\]
satisfies
\[
 \boxed{d_1(D)^2+d_2(D)^2<\frac23.}                    \tag{29}
\]
Consequently, any counterexample to the original pair-sector Ky--Fan
inequality must remain a positive distance away from the sharp
rank-one boundary.

#### Proof

Suppose first that \(d_1(D)^2=4/9\).  Let \(x,y\) be a top singular
pair and put
\[
 E=\Pi _2(|x\rangle\langle y|).
\]
Then
\[
\frac23=d_1(D)
=\langle D,E\rangle
\le\|D\|_2\|E\|_2
\le\frac23.                                            \tag{30}
\]
Both inequalities are equalities.  Hence \(\|E\|_2=2/3\) and
\[
 D=e^{i\theta}\frac32E.                                \tag{31}
\]
The complete equality-locus spectral theorem gives
\[
 s_2(E)\le\frac29.
\]
Therefore
\[
 d_2(D)\le\frac13,\qquad
 d_1(D)^2+d_2(D)^2\le\frac59.                          \tag{32}
\]

If the theorem were false, there would be a sequence of unit
pair-sector operators \(D_m\) such that
\[
 d_1(D_m)^2\longrightarrow\frac49,\qquad
 d_1(D_m)^2+d_2(D_m)^2\ge\frac23.
\]
The unit sphere in the finite-dimensional pair-sector space is
compact, so a subsequence converges to a unit \(D_\infty\).  Singular
values are continuous, and \(D_\infty\) would simultaneously satisfy
\[
 d_1(D_\infty)^2=\frac49,\qquad
 d_1(D_\infty)^2+d_2(D_\infty)^2\ge\frac23,
\]
contradicting (32). \(\square\)

The gap at exact saturation is \(2/3-5/9=1/9\), but the proof above
does not produce a numerical value for \(\varepsilon_0\).  Producing
one requires a uniform algebraic treatment of the quartic
intersection geometry exposed by (27).

## 7. Remaining lemma

The next exact target is no longer qualitative.  It is precisely:
\[
\boxed{
(2d_2(D)-d_1(D))_+^2
\le3\left(\frac49\|D\|_2^2-d_1(D)^2\right)
\quad(D\in\operatorname{Ran}\Pi _2).}                  \tag{33}
\]
For unit \(D\), this is (4).  A successful proof may be sought by:

1. deriving a matrix certificate for
   \(E(x,y)^\dagger E(x,y)\) with an error controlled by the SOS
   \(\Delta(x,y)\);
2. treating the two generic components with the quadratic bounds
   (11), (17);
3. adding explicit quartic compatibility certificates at their
   intersections, beginning with (25)--(27).

Compactness alone cannot supply the sharp coefficient in (33).
