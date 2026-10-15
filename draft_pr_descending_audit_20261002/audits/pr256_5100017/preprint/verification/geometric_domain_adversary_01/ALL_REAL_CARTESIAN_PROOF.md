# An independent all-real Cartesian moment proof

This derivation independently checks the submitted explicit centroid by expanding Cartesian projections. It applies to every real strict confocal elliptic pair with a least even poristic period N; it does not enumerate or sample N. The geometric group, normal-angle, positivity, four-period, and domain arguments are supplied in `GEOMETRIC_DOMAIN_REPORT.md`. Every local polynomial identity below is checked exactly in `real_cartesian_certificate.py`; the script starts from Cartesian projections and does not import submitted algebra or checkers.

## Geometric inputs and a circle identity

Let the consecutive outward unit normals be `n_i=(c,s)`, `n_j=(u,w)`, with support numbers h,k. Put

\[
 K=cw-su,\quad C=cu+sw,\quad
 \xi_i=c^2-s^2,\quad \eta_i=2cs,\quad
 \xi_j=u^2-w^2,\quad \eta_j=2uw.
\]

For `d≠0`, set D=F/d. The ellipse support formula and chord tangency give

\[
 c^2+s^2=u^2+w^2=1,\qquad
 h^2=H+e\xi_i,\quad k^2=H+e\xi_j,\quad
 hk=(D+e)cu+(D-e)sw.                                      \tag{A}
\]

These are the only support constraints needed in the subsequent coefficient expansion. For clarity, the tangency input follows by writing consecutive boundary parameters as `u_0,u_0+2q`, where `0<q<pi/2`, and using

\[
 \sin^2q=\lambda\left(\frac{\cos^2(u_0+q)}{a^2}
                        +\frac{\sin^2(u_0+q)}{b^2}\right).
\]

Collecting the cosine and sine products gives `d hk=F C+ed(cu-sw)`, which is (A). Its squared-support compatibility reduces exactly to

\[
 0=H^2-e^2-(D^2-e^2)C^2+e(H-D)(\xi_i+\xi_j).                \tag{B}
\]

Write `Z_i=(xi_i,eta_i)`, so the doubled normals are unit vectors. Their cross and dot products are

\[
 [Z_i,Z_j]=2KC,\qquad Z_i\cdot Z_j=2C^2-1.
\]

The strict-domain positivity `F+ed>0`, `F-ed>0` makes `D^2-e^2>0`. Consequently (B) implies

\[
 Z_i\cdot Z_j=u_*+v(\xi_i+\xi_j),\quad
 u_*=\frac{2(H^2-e^2)}{D^2-e^2}-1,\quad
 v=\frac{2e(H-D)}{D^2-e^2}
   =\frac{-4e\lambda d}{F^2-e^2d^2}.                       \tag{C}
\]

No sign inference or billiard reconstruction is made by squaring: (B) is only a necessary relation for the already constructed physical billiard.

For any unit complex vectors Z,W,

\[
 [Z,W](Z+W)=-i(1+Z\cdot W)(W-Z).                           \tag{D}
\]

This is an identity without division, hence remains valid for diameters, coincident doubled normals, and self-intersecting ordered polygons. On summing (D) using (C), the constant terms telescope. Its imaginary coordinate contains the sum of `xi_j^2-xi_i^2` and vanishes. Its real coordinate is

\[
 v\sum_i(\xi_i+\xi_j)(\eta_j-\eta_i)
 =v\sum_i[Z_i,Z_j],
\]

because the difference of `xi_j eta_j` and `xi_i eta_i` telescopes. Define

\[
 S_Z=\frac12\sum_i[Z_i,Z_j]=\sum_i K_iC_i.
\]

The real and imaginary coordinates of the resulting first-circle-moment identity therefore give

\[
 \sum_iK_iC_i(\xi_i+\xi_j)=vS_Z,\qquad
 \sum_iK_iC_i(\eta_i+\eta_j)=0.                            \tag{E}
\]

All sums are in trajectory order. Neither simplicity nor nonzero S_Z was required to prove (E).

## Pairing and the direct area expansion

For a fixed Cartesian point `M=(x,y)`, direct orthogonal projection to the tangent line gives

\[
 Q_i=(hc+x s^2-ycs,\ hs-xcs+y c^2),
\]
\[
 Q_j=(ku+x w^2-yuw,\ kw-xuw+y u^2).                         \tag{F}
\]

The opposite edge replaces h,k by -h,-k but keeps c²,s²,cs,u²,w²,uw. The cyclic sum includes both antipodal edges. Thus it equals the sum of the average of each edge polynomial with its antipodal copy; no extra factor of two is inserted. This average removes the linear area terms and the constant/quadratic first-moment terms.

For the paired-average area edge `A_ij=[Q_i,Q_j]/2`, its surviving monomial coefficients reduce to

\[
 [1]A_{ij}=\frac D2KC+\frac e2(uw-cs),
\]
\[
 [x^2]A_{ij}=\frac14KC+\frac14(cs-uw),\qquad
 [y^2]A_{ij}=\frac14KC-\frac14(cs-uw),
\]
\[
 [xy]A_{ij}=\frac14(\xi_j-\xi_i).
\]

The terms after KC all telescope. Hence

\[
 S(M)=S_Z\left(\frac D2+\frac{x^2+y^2}{4}\right),\qquad
 S(0)=\frac D2S_Z.                                        \tag{G}
\]

As proved geometrically, `S(0)>0`; therefore `S_Z≠0` for d≠0. Equation (G), `F>0`, and D=F/d yield precisely the submitted area identity and its entire exceptional locus.

## Direct first-moment expansion with explicit telescoping terms

Let

\[
 T(M)=\sum_i[Q_i,Q_j](Q_i+Q_j).
\]

In the following tables, each listed edge coefficient is exactly its cyclic part plus `f(c,s)-f(u,w)`. The identities require only (A), are polynomial in real variables, and hold regardless of polygon simplicity. They can be verified by expanding (F) and replacing h²,k²,hk as in (A); `real_cartesian_certificate.py` does this and checks the residual modulo the two unit-normal equations. Each listed potential is explicitly a function of only one normal, so its cyclic sum vanishes.

Put `Xi=xi_i+xi_j` and `Yi=eta_i+eta_j` only within these tables.

| Coordinate and monomial | Cyclic part | Potential f(c,s) |
|---|---|---|
| Tx, x | `KC[(D-H-3e/2)-(D+e/2)Xi]` | `-e cs(1+2s²)/2` |
| Tx, y | `KC(-D+e/2)Yi` | `e c²s²` |
| Ty, x | `KC(-D-e/2)Yi` | `e c²s²` |
| Ty, y | `KC[(D-H+3e/2)+(D-e/2)Xi]` | `e cs(2s²-3)/2` |

| Coordinate and monomial | Cyclic part | Potential f(c,s) |
|---|---|---|
| Tx, x³ | `KC(3-Xi)/4` | `cs(1+2s²)/4` |
| Tx, x²y | `-KCYi/4` | `s²(3s²-1)/2` |
| Tx, xy² | `KC(3-Xi)/4` | `cs(1-6s²)/4` |
| Tx, y³ | `-KCYi/4` | `c²s²/2` |
| Ty, x³ | `-KCYi/4` | `-c²s²/2` |
| Ty, x²y | `KC(3+Xi)/4` | `cs(5-6s²)/4` |
| Ty, xy² | `-KCYi/4` | `s²(5-3s²)/2` |
| Ty, y³ | `KC(3+Xi)/4` | `cs(2s²-3)/4` |

Every constant and degree-two first-moment coefficient is zero by antipodal pairing. Summing the table and using (E) gives the full signed moment, valid for arbitrary real x,y:

\[
 T_x=S_Z x\left[D-H-\frac{3e}{2}-v\left(D+\frac e2\right)
                    +\frac{3-v}{4}(x^2+y^2)\right],        \tag{H}
\]
\[
 T_y=S_Z y\left[D-H+\frac{3e}{2}+v\left(D-\frac e2\right)
                    +\frac{3+v}{4}(x^2+y^2)\right].        \tag{I}
\]

These are exact cyclic identities for all real admissible supports/normals, not empirical fitted polynomials. In particular they also apply where S(M)=0; only the quotient below excludes that set.

## Quotient, all-real domain, and the four-period boundary

Whenever `2D+x²+y²≠0`, divide (H) and (I) by `6S(M)` from (G). Put `z=x+iy`. Combining the two real quotients yields

\[
 C'_2(M)=\frac z2-
 \frac{z(D+2H+ev)+\overline z(2Dv+3e+v|z|^2/2)}
 {3(2D+|z|^2)}.                                           \tag{J}
\]

This last conversion is also checked as an exact rational identity in the certificate. Multiplying the fraction numerator and denominator by d gives submitted formula (2). Thus all dependence on the orbit phase cancels for every real strict confocal elliptic pair of least even period and every M with nonzero signed area.

At d=0 the substitution D=F/d is deliberately unused. Geometrically each normal advances by pi/2, giving least period four and a rectangular outer polygon. Conversely, for least period four, antipodes and the consecutive support identities give `2dh_0h_1=0`, hence d=0. In a side frame of that rectangle the pedal vertices are `(A,y),(x,B),(-A,y),(x,-B)`. Direct shoelace gives `S=2AB` and `T=4AB(x,y)`, so `C'_2=M/3`. As v=0 at d=0, submitted formula (2) has that same value and no zero denominator.

The geometric normal positivity supplies `S(0)>0`. From the exact area identity, the centroid exists for every M when d>=0; for d<0 it exists exactly off the fixed circle `|M|²=-2F/d`. Every simple even family has d>=0 by the geometric report's half-orbit argument and repaired four-period converse. There is no need to take an endpoint or to rely on numerical limiting behavior. Hyperbolic/degenerate caustics and padded odd least-period orbits are outside this theorem's stated assumptions.
