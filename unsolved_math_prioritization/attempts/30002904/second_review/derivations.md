# Independent continuous SL3 derivations

These calculations establish the second review's accepted mathematical claims. They concern normalized Haar measure in ordinary operator balls in SL3(R) only. All thresholds s are fixed and nonnegative, and X>1. No lattice-counting input is used.

## 1 Radial coordinates from the group differential

Let D=diag(exp(a),exp(b),exp(c)), where a>=b>=c and a+b+c=0. Consider g=kDℓ, with k,ℓ in SO3(R). At k=ℓ=I, left-trivializing the differential of this map gives

\[
D^{-1}(d g)=D^{-1}U D+D^{-1}dD+V,
\]

where U,V are skew-symmetric. For each i<j, the two independent coefficients of U and V map to the (i,j),(j,i) matrix entries with coefficient matrix

\[
\begin{pmatrix}
 e^{t_j-t_i}&1\\
 -e^{t_i-t_j}&-1
\end{pmatrix}.
\]

Its determinant is 2sinh(t_i-t_j). The diagonal directions contribute a fixed nonzero determinant in coordinates (a,b), with c=-a-b. On the regular ordered chamber the remaining compact ambiguity is finite and constant. Thus, after the compact variables are integrated out, the Haar density is a constant C>0 times

\[
J(a,b)=\sinh(a-b)\sinh(2a+b)\sinh(a+2b)
\]

with respect to da db. Repeated singular values form the chamber boundary and do not change the integrals. The precise value of C is immaterial because every numerator and denominator below uses the same Haar measure and same coordinate normalization.

The ordinary operator norm is exp(a); therefore its radius-X ball is given by a<=L=log X and -a/2<=b<=a. The determinant constraint implies a>=0. In particular, there is no independent box cutoff on the smaller singular values.

## 2 A unit-square proof with an elementary limiting density

Define

\[
t=e^a/X,\qquad r=e^{2(b-a)}.
\]

Then

\[
\sigma_1=Xt,\qquad \sigma_2=Xt\sqrt r,
\qquad \sigma_3=X^{-2}t^{-2}r^{-1/2}.
\]

The condition sigma2>=sigma3 is exactly X³t³r>=1. Together with sigma1>=sigma2 and sigma1<=X, this gives

\[
D_X=\{(t,r):X^{-1}\le t\le1,
\ X^{-3}t^{-3}\le r\le1\}.
\]

The coordinate Jacobian is

\[
\left|\frac{\partial(a,b)}{\partial(t,r)}\right|
=\left|\det\begin{pmatrix}1/t&0\\1/t&1/(2r)\end{pmatrix}\right|
=\frac1{2tr}.
\]

Writing each sinh difference as half the difference of the corresponding singular-value ratio and its reciprocal gives the exact scaled density

\[
X^{-6}J(a,b)\,da\,db
=F_X(t,r)\,dt\,dr,
\]

where, on D_X,

\[
F_X(t,r)=\frac{t^5(1-r)}{16}
\left(1-X^{-6}t^{-6}r^{-1}\right)
\left(1-X^{-6}t^{-6}r^{-2}\right).
\tag{1}
\]

Extend F_X by zero to [0,1]². In D_X we have X^(-6)t^(-6)<=r² and 0<r<=1. Both factors in parentheses consequently belong to [0,1], so

\[
0\le F_X(t,r)\le F(t,r)=t^5(1-r)/16.
\]

For every fixed t,r in (0,1), the point eventually lies in D_X and both factors tend to one. Since

\[
\int_0^1\!\int_0^1F(t,r)\,dr\,dt
=\frac1{16}\cdot\frac16\cdot\frac12
=\frac1{192},
\tag{2}
\]

dominated convergence proves that the unnormalized radial ball mass is asymptotic to X^6/192. The factor C is restored only if an absolute Haar normalization is desired.

The top gap d=a-b is at least s precisely when r<=z=exp(-2s). Applying the same dominated-convergence argument with that indicator and dividing by (2) gives

\[
\lim_{X\to\infty}\Pr(d\ge s)
=\frac{\int_0^1\int_0^z t^5(1-r)/16\,dr\,dt}{1/192}
=2z-z^2=2e^{-2s}-e^{-4s}.
\tag{3}
\]

Equivalently, the limiting normalized density of (t,r) is 12t^5(1-r), and the r marginal is 2(1-r) on [0,1]. The associated gap density is 4(exp(-2d)-exp(-4d)) on [0,infinity). This supplies an independent derivation without discarding a chamber constraint or approximating a determinant by an unnormalized leading exponential.

## 3 Exact finite-radius tail and its verification

Use the simple-root gaps p=a-b and q=b-c. They satisfy

\[
a=(2p+q)/3,\qquad b=(-p+q)/3,\qquad c=-(p+2q)/3,
\]

with absolute Jacobian 1/3. The exact radial region is p,q>=0 and 2p+q<=3L. For 0<=s<=3L/2 let

\[
I(L,s)=\frac13\int_s^{3L/2}\int_0^{3L-2p}
\sinh p\sinh q\sinh(p+q)\,dq\,dp.
\tag{4}
\]

For larger s the mass is zero. The identity

\[
4\sinh p\sinh q\sinh(p+q)
=\sinh(2p+2q)-\sinh(2p)-\sinh(2q)
\]

gives the inner integral, including its 1/3 Jacobian, as

\[
H_L(p)=\frac{
\cosh(6L-2p)-\cosh(6L-4p)-\cosh(2p)+1}{24}
-\frac{(3L-2p)\sinh(2p)}{12}.
\tag{5}
\]

Define

\[
\begin{aligned}
Q(L,s)={}&\frac{\sinh(6L-2s)}{48}
-\frac{\sinh(6L-4s)}{96}
-\frac{\sinh(3L)}{12}
+\frac{\sinh(2s)}{16}\\
&+\frac{(3L-2s)(2\cosh(2s)+1)}{48}.
\end{aligned}
\tag{6}
\]

Differentiating (6) with respect to s gives -H_L(s), and Q(L,3L/2)=0. The fundamental theorem of calculus therefore proves I(L,s)=Q(L,s). This is a complete elementary verification of the first auditor's expression; agreement of software output is not needed for the implication.

At s=0 it gives

\[
I(L,0)=\frac{\sinh(6L)}{96}-\frac{\sinh(3L)}{12}+\frac{3L}{16}.
\tag{7}
\]

At fixed s, divide (6) by exp(6L). Only the first two terms remain in the limit, and their combined coefficient is (2exp(-2s)-exp(-4s))/192. Dividing by (7) recovers (3). The exact formula vanishes at the largest possible gap, and the integral (4) guarantees nonnegativity throughout its stated domain.

## 4 Inverse-bounded mass in different coordinates

Let v=-c=log(||g^(-1)||op). Since b=v-a, the chamber inequalities become

\[
a/2\le v\le2a.
\]

The coordinate map (a,v)->(a,b) has determinant one. The simultaneous norm conditions are 0<=a,v<=L, giving a symmetric quadrilateral. Its radial integrand is

\[
J_*(a,v)=\sinh(2a-v)\sinh(a+v)\sinh(2v-a).
\]

Consequently

\[
K(L)=\int_0^{L/2}\int_{a/2}^{2a}J_*(a,v)\,dv\,da
+\int_{L/2}^L\int_{a/2}^LJ_*(a,v)\,dv\,da.
\tag{8}
\]

An antiderivative in v is

\[
H(a,v)=\frac{\cosh(2a+2v)}8
+\frac{\cosh(4a-2v)}8
-\frac{\cosh(4v-2a)}{16}.
\]

This follows either by direct differentiation or the same three-sinh identity. There is a particularly short independent evaluation of (8). The two moving square faces contribute symmetrically, while the chamber edges are fixed. Therefore, for L>0,

\[
\begin{aligned}
K'(L)&=2\int_{L/2}^LJ_*(L,v)\,dv\\
&=2[H(L,L)-H(L,L/2)]\\
&=\frac{\cosh(4L)}4-\frac{\cosh(3L)}2
+\frac{\cosh(2L)}8+\frac18.
\end{aligned}
\]

Together with K(0)=0, integration proves

\[
K(L)=\frac{\sinh(4L)}{16}-\frac{\sinh(3L)}6
+\frac{\sinh(2L)}{16}+\frac L8.
\tag{9}
\]

This checks the first audit's inverse-ball formula by a different polygon decomposition and an independent boundary-derivative computation.

## 5 Independent corner proof of the inverse-ball coefficient

For a second verification of the asymptotic in (9), put alpha=L-a and beta=L-v. The simultaneous norm region becomes

\[
\alpha,\beta\ge0,\quad \alpha,\beta\le L,
\quad L-2\alpha+\beta\ge0,
\quad L+\alpha-2\beta\ge0.
\]

Extend its scaled density by zero to the nonnegative quadrant. Within the region, all three sinh arguments are nonnegative, so

\[
\begin{aligned}
0&\le e^{-4L}J_*(L-\alpha,L-\beta)\\
&\le\frac18e^{-2\alpha-2\beta}.
\end{aligned}
\]

For each fixed alpha,beta the region eventually includes that point, the three arguments tend to infinity, and the scaled density tends to the displayed upper bound. Its integral over the quadrant is

\[
\frac18\left(\int_0^\infty e^{-2\alpha}d\alpha\right)^2
=\frac1{32}.
\]

Thus K(L)~exp(4L)/32 directly by dominated convergence. Combining this with I(L,0)~exp(6L)/192 yields

\[
\frac{m(\{g:\|g\|_{op}\le X,\ \|g^{-1}\|_{op}\le X\})}
{m(\{g:\|g\|_{op}\le X\})}
=\frac{K(\log X)}{I(\log X,0)}\sim6X^{-2}.
\]

The extra inverse condition cuts out a different dominant part of the radial chamber. It is not a constant change of norm and cannot be silently added to the ordinary-ball model. This conclusion and its constant are continuous Haar statements only.

## 6 Exact numerical-bound contradiction

Substitute s=2log(eta) into (3). For every eta>1,

\[
2\eta^{-4}-\eta^{-8}-\eta^{-4}
=\eta^{-8}(\eta^4-1)>0.
\]

For eta=5 this is the exact comparison

\[
1249/390625>625/390625.
\]

Both numerator and denominator of the finite-radius normalized ratio have positive leading multiples of X^6. Their individual limits diverge, whereas their ratio has the finite positive limit (3). This distinction is necessary when interpreting the separately placed limits in the source statement.

The corrected dimension-three limit remains strictly below one for eta>1, since

\[
2\eta^{-4}-\eta^{-8}=1-(1-\eta^{-4})^2.
\]

The result therefore corrects the precise numerical upper bound without contradicting that qualitative feature. It does not address the higher-dimensional discrete problem, any transfer theorem, or a different thinness result in the inverse-bounded model.
