# Approach 3: an exact classification within parallelograms

## Theorem

For fixed \(0<\alpha<2\), a parallelogram is sliding-stationary for the Riesz energy under area constraint if and only if it is a rhombus. Consequently, when used as its own area-normalized Wulff shape, it remains a global minimizer for all sufficiently small positive γ exactly when it is a rhombus.

The positive conclusion for rhombi is already contained in BCT (2021), Theorem 2.5. The integral calculation below supplies a self-contained strict exclusion of every non-rhombic parallelogram. No priority claim is made.

## Calculation

Let
\[
P=\{sa+tb:0<s,t<1\},\qquad D=|\det(a,b)|>0,
\]
where \(a,b\) are independent vectors. Put \(A=|a|\), \(B=|b|\), and \(p=\alpha/2\). Scaling to area one will not affect equality of side-average potentials.

Opposite sides have identical average potentials by central symmetry. Let \(M_b\) be the average on a side parallel to \(b\), and \(M_a\) the average on a side parallel to \(a\). Direct parametrization and the convolution of two uniform interval measures give
\[
M_b=D\int_0^1\int_{-1}^{1}(1-|t|)|sa+tb|^{-\alpha}\,dt\,ds,
\]
\[
M_a=D\int_0^1\int_{-1}^{1}(1-|s|)|sa+tb|^{-\alpha}\,ds\,dt.
\]
In the second display the inner variable is \(s\), the outer is \(t\). Defining
\[
H(s,t)=|sa+tb|^{-\alpha}+|sa-tb|^{-\alpha},\qquad 0<s,t<1,
\]
we obtain
\[
M_b-M_a=D\int_0^1\int_0^1(s-t)H(s,t)\,ds\,dt
=\frac D2\int_0^1\int_0^1(s-t)[H(s,t)-H(t,s)]\,ds\,dt.
\tag{1}
\]
These integrals are finite for \(\alpha<2\), because the linear maps (s,t)→sa±tb are invertible and the only singularity is at (0,0).

Write \(c=(a\cdot b)/(AB)\in(-1,1)\). The two terms in \(H\) have squared denominators
\[
A^2s^2+B^2t^2\pm2ABcst.
\]
After interchanging \(s,t\), their difference, with either fixed sign, is
\[
(A^2-B^2)(s^2-t^2).
\]
If \(A>B\) and \(s>t\), both denominators for \(H(s,t)\) are strictly larger than those for \(H(t,s)\). Since \(r\mapsto r^{-p}\) is strictly decreasing,
\[
(s-t)[H(s,t)-H(t,s)]<0\quad\text{for }s\ne t.
\]
The same strict sign holds when \(s<t\). Thus (1) is strictly negative. If \(A<B\), it is strictly positive. If \(A=B\), it is identically zero.

There are only two potentially distinct side averages. They are equal exactly when \(A=B\), equivalently when \(P\) is a rhombus. Applying Approach 2 completes the theorem.

## A strict first-order obstruction

For a unit-area rectangle of side lengths \(a\ne b\), the area-preserving path changing the lengths to \(ae^t,be^{-t}\) has
\[
\left.\frac d{dt}V_\alpha(P_t)\right|_{t=0}=2(M_b-M_a)\ne0.
\]
At the rectangle's own crystalline Wulff shape, the anisotropic-perimeter first derivative along this path is zero. Choosing the appropriate sign of \(t\) therefore lowers the full energy for **every** fixed \(\gamma>0\). This is stronger than failure of small-γ global minimality.

## Limit of the approach

The exchange argument uses both the parallelogram parametrization and its two pairs of opposite sides. It does not extend by simply replacing a quadrilateral with a parallelogram. Approach 4 shows that it would be false to infer that all sliding-critical quadrilaterals must be rhombi.
