# Exact fusion of the strengthened faces with the triple-Hodge gap

## Status

This note lifts the sharp rank-two triple-Hodge theorem to an explicit
operator lower bound for the sum of the three strengthened two-pair
faces.

Fix a qutrit code plane \(V\), and write
\[
 H_V=S_V-F_1-F_2-F_3,\qquad
 K_i=H_V+\frac12F_i,\qquad
 K=\sum_iK_i.
\]
The exact fusion theorem is
\[
\boxed{
\begin{aligned}
 \langle z,Kz\rangle-\frac{13}{71}\langle z,S_Vz\rangle
 ={}&
 \frac{255}{142}\sum_i g_i(C_z)
 +\frac{225}{568}\|\Pi_1C_z\|_2^2\\
 &+\frac{10}{71}\Xi(C_z),
\end{aligned}}
\tag{1}
\]
where \(C_z\) is the rank-at-most-two transition associated with
\(z\), \(g_i\) are the three sitewise Haar brackets, and
\[
\boxed{
 \Xi(C)=\|C\|_2^2+6{\cal J}_3(C)
       =(s_1-s_2)^2
        +6\left({\cal J}_3(C)+\frac13s_1s_2\right)
       \geq0.
}
\tag{2}
\]
Every term on the right of (1) is nonnegative.  Consequently
\[
\boxed{
 K(V)\succeq\frac{13}{71}S_V,
 \qquad
 H_V\succeq-\frac9{71}S_V.
}
\tag{3}
\]
Equivalently, in coefficient-matrix variables the same fusion is
\[
\boxed{
 Q_3(C)+\frac{27}{160}\|\Pi_2C\|_2^2
 =
 \frac{51}{160}\sum_i g_i(C)
 +\frac9{128}\|\Pi_1C\|_2^2
 +\frac1{40}\Xi(C).
}
\tag{3a}
\]
Thus the previous estimate
\(Q_3(C)\geq-\|\Pi_2C\|_2^2/4\) improves exactly to
\[
\boxed{
 Q_3(C)\geq-\frac{27}{160}\|\Pi_2C\|_2^2.
}
\tag{3b}
\]
This is the operator form of the explicit generalized-depth bound
\(\delta\leq9/71\), but (1) retains all of the coercive remainder.

The equality set of \(\Xi\) is already on the established
local-support boundary: equality requires equal singular values and
saturation of the sharp triple-Hodge theorem, whose equality
classification is the common-factor orbit.  Thus (1) fuses the
three-face gap with a concrete nonlinear measure which vanishes only
on a sign-safe geometric boundary.

The unrestricted three-copy theorem is now exactly the smaller
inequality
\[
\boxed{
 204\sum_i g_i(C)
 +45\|\Pi_1C\|_2^2
 +16\Xi(C)
 \geq36\,\sigma(C),
}
\tag{4}
\]
where
\[
 \sigma(C)=2Q_3(C)+3\|\Pi_2C\|_2^2.
\]
Equation (4) remains unproved.  It is equivalent to the desired sign,
not a relaxation.

The dependency-free exact checker is
`verification/verify_n3_triple_hodge_face_fusion.py`.

## 1. Face variables

For one transition \(C=C_z\), use the face sums
\[
 R=\sum_i r_i,\qquad T=\sum_i s_i,
\tag{5}
\]
and put
\[
 G=\sum_i g_i=\frac13T,\qquad
 a=\|\Pi_1C\|_2^2,\qquad
 c=\|\Pi_2C\|_2^2.
\tag{6}
\]
The sum of the strengthened-face energies is
\[
\boxed{
 k:=\langle z,Kz\rangle
 =\frac13R+\frac23T
 =\frac13R+2G.
}
\tag{7}
\]
The summed sitewise identity gives
\[
 36Q_3(C)=2R+4T-9c.
\tag{8}
\]
Therefore the Schur energy is
\[
\begin{aligned}
 \sigma
 :=\langle z,S_Vz\rangle
 &=2Q_3(C)+3c\\
 &=\frac13k+\frac52c.
\end{aligned}
\tag{9}
\]
Equivalently,
\[
\boxed{
 c=\frac25\sigma-\frac2{15}k.
}
\tag{10}
\]

## 2. Retaining the exact triple-Hodge slack

Put
\[
 N=\|C\|_2^2,\qquad
 p=s_1(C)s_2(C),\qquad
 \Delta=(s_1(C)-s_2(C))^2,
\tag{11}
\]
so
\[
 N=2p+\Delta.
\tag{12}
\]
Let
\[
 \tau(C)={\cal J}_3(C)+\frac13p.
\tag{13}
\]
The sharp rank-two triple-Hodge theorem is exactly
\[
 \tau(C)\geq0.
\tag{14}
\]

Before its slack is discarded, the conversion to the common face
coordinates is the identity
\[
\boxed{
 320R+28T
 =
 468c+405a+144\Delta+864\tau.
}
\tag{15}
\]
Indeed, the uneliminated form is
\[
 128R+4T+96p-252c-243a=288\tau.
\tag{16}
\]
Substitute
\[
 N=2c+\frac94a+\frac19(T-4R),
\qquad
 2p=N-\Delta,
\]
and multiply by three to obtain (15).

## 3. Exact fusion

Use \(T=3G\) and \(R=3k-6G\) from (7).  The left side of (15) is
\[
 320R+28T=960k-1836G.
\tag{17}
\]
Substitute (10) on the right side of (15):
\[
\begin{aligned}
 960k-1836G
 ={}&
 \frac{936}{5}\sigma-\frac{312}{5}k
 +405a+144\Delta+864\tau.
\end{aligned}
\]
After multiplying by five and collecting \(k\),
\[
\boxed{
 5112k
 =
 936\sigma+9180G+2025a+720\Delta+4320\tau.
}
\tag{18}
\]
Division by \(5112\) gives
\[
 k
 =\frac{13}{71}\sigma
 +\frac{255}{142}G
 +\frac{225}{568}a
 +\frac{10}{71}\Delta
 +\frac{60}{71}\tau.
\tag{19}
\]
Finally,
\[
 \Delta+6\tau
 =\Delta+6{\cal J}_3+2p
 =N+6{\cal J}_3
 =\Xi.
\tag{20}
\]
Combining the last two terms of (19) proves the exact fusion identity
(1).

Because \(G,a,\Xi\geq0\) on rank-at-most-two transitions, (3)
follows.  The affine relation
\[
 K=\frac12S_V+\frac52H_V
\tag{21}
\]
then gives the second operator inequality in (3).

## 4. Equality geometry and common kernels

Equation (2) is itself a sum of two nonnegative quantities:
\[
 \Xi=\Delta+6\tau.
\tag{22}
\]
Therefore
\[
 \Xi=0
 \quad\Longleftrightarrow\quad
 \Delta=0,\quad\tau=0.
\tag{23}
\]
The sharp triple-Hodge equality classification puts the two singular
planes of a nonzero \(\tau=0\) transition in the common-factor orbit.
The additional equation \(\Delta=0\) makes the two singular values
equal.  This orbit has a deficient one-site local support and is
covered by the exact local-support-boundary theorem.  Hence
\[
 \boxed{\Xi(C)=0\quad\Longrightarrow\quad Q_3(C)\geq0.}
\tag{24}
\]

Likewise,
\[
 G=0\quad\Longrightarrow\quad Q_3(C)\geq0.
\tag{25}
\]
Indeed, if \(Q_3(C)<0\), the fixed-left Haar-kernel theorem gives
\(g_i(C)>0\) at every site.

These two safe boundary statements show why equality in the bare
operator bound of (3) is impossible.  If
\[
 k=\frac{13}{71}\sigma,
\]
then (1) forces \(G=a=\Xi=0\).  On the other hand, (21) would give
\[
 Q_3(C)
 =\frac12\langle z,H_Vz\rangle
 =-\frac9{142}\sigma<0,
\]
contradicting either (24) or (25).  Thus, for each fixed code plane,
\[
 K(V)-\frac{13}{71}S_V\succ0.
\tag{26}
\]
The point of (1), beyond this strictness, is that it identifies the
three exact quantities which must provide the additional coercivity.

## 5. The exact remaining fusion inequality

The desired endpoint sign is \(H_V\succeq0\).  By (21), this is
equivalent to
\[
 k\geq\frac12\sigma.
\tag{27}
\]
Subtract \(13\sigma/71\) from both sides and use (1).  Since
\[
 \frac12-\frac{13}{71}=\frac{45}{142},
\]
the result, after multiplying by \(568\) and dividing by five, is
\[
\boxed{
 204G+45a+16\Xi\geq36\sigma.
}
\tag{28}
\]
Using (3a), the equivalent purely sector-normalized form is
\[
\boxed{
 204G+45a+16\Xi\geq108c.
}
\tag{29}
\]
Thus (28), equivalently (29), is equivalent to unrestricted
three-copy positivity.  It
has three useful features:

1. all quantities on the left are exact nonnegative common-code
   invariants;
2. the loci \(G=0\) and \(\Xi=0\) are already sign-safe;
3. known endpoint zero vectors attain equality in (28), so its
   constant cannot be improved.

The unresolved region is therefore the strict interior
\[
 G>0,\qquad \Xi>0,
\]
with genuinely full local support.  A completion must prove the
quantitative lower bound (28), equivalently (29), not merely exclude
a common zero of its three terms.
