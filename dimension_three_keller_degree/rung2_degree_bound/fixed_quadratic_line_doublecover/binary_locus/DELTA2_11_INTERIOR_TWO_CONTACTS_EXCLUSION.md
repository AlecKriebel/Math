# Provisional exclusion of the squarefree-interior two-contact
\(\delta=2,\{1,1\}\) row

**Status:** exact SymPy and independent PARI/GP replays pass; hostile
mathematical audit is pending.

**First recorded release (UTC):** 2026-07-25T19:02:24Z.

This work is not peer reviewed.  Exact checks are evidence about the
encoded algebra, not peer review.

## Theorem

Put
\[
L=p-wq,\qquad M=wp-q,\qquad h=LM,\qquad u=w^2.
\]
Up to exchanging \(p,q\), scaling the cubic, and the residual
stabilizer described below, the two-ramification-contact contribution
is
\[
\begin{aligned}
R={}&4wa\,p^3-3(1+u)a\,p^2q\\
   &\quad-3(1+u)pq^2+4wq^3.                    \tag{1}
\end{aligned}
\]
There is no Keller counterexample in this leaf on the exact open
\[
w(u-1)E_LE_M\kappa_-\kappa_+\ne0,              \tag{2}
\]
where
\[
\begin{aligned}
E_L&=aw^3-3aw-3u+1,\\
E_M&=-3au+a+w^3-3w,\\
\kappa_-&=u-4w+1,\qquad
\kappa_+=u+4w+1.                               \tag{3}
\end{aligned}
\]
The factors \(E_L,E_M\) are the two fixed-root incidence boundaries.
The factors \(\kappa_\pm\) are the two exceptional \(\kappa=16\)
\(\{2,0\}\) mutations already treated separately.

The normalization in (1) loses no endpoint.  Before scaling, write the
two coefficients as \(A,D\).  The involution \(p\leftrightarrow q\)
swaps \(A,D\); hence an endpoint with \(D=0,A\ne0\) moves into the
\(D\ne0\) chart.  The case \(A=D=0\) is not an exact-\(\delta=2\)
two-contact cubic.

## Stabilizer and the cross-ratio modulus

The four marked points on the binary line are the ramification pair
\(\{0,\infty\}\) and the fixed pair \(\{w,w^{-1}\}\).  Thus the
ordered cross-ratio is \(u=w^2\), while the unordered configuration
identifies \(u\) with \(u^{-1}\).  The normal form has the exact
redundancies
\[
\begin{array}{c|c}
p\leftrightarrow q&a\leftrightarrow a^{-1}\\
w\leftrightarrow w^{-1}&a\mapsto a\\
p\mapsto-p\ \text{and a common target sign}&(w,a)\mapsto(-w,-a).
\end{array}                                    \tag{4}
\]
In particular, \(w\) is not an artificial free coefficient: it
records the cross-ratio, up to the finite identifications in (4).
The reciprocal factors below respect these symmetries.

On (2), direct bracket computation gives
\[
\gcd([Q,R],-[P,R],[P,Q])=pq,\qquad
P=hp^2,\quad Q=hq^2.                            \tag{5}
\]

## The generic contact chart

Let \(M_7\) be the coefficient matrix of
\[
[Q,R]U-[P,R]V+[P,Q]W=0,\qquad
\deg(U,V,W)=(2,2,1).                            \tag{6}
\]
It has rank six.  In the chart used for its two-dimensional kernel,
the internal denominator is
\[
\begin{aligned}
B={}&16w(u+1)^3(a^2+1)\\
   &\quad+a(3u^4+108u^3-46u^2+108u+3).         \tag{7}
\end{aligned}
\]
Lift a tangent \(sN_1+tN_2\) to the \(E_6\) contact map in
\[
(X,Y,Z,x_5,y_5)=(s^2,st,t^2,x_5,y_5).
\]
After removing the nonzero common factor
\[
\mathcal B=
\frac{1024w^2(u+1)\kappa_-\kappa_+}{3B^3},     \tag{8}
\]
the six maximal minors have the form
\[
\begin{aligned}
m_0&=\mathcal B K_1Q_0,\\
m_i&=-\mathcal B w^2K_1K_2Q_i\quad(1\le i\le4),\\
m_5&=\mathcal B K_2Q_5,                         \tag{9}
\end{aligned}
\]
where
\[
K_1=ab+c,\qquad K_2=ac+b,                       \tag{10}
\]
\[
b=-4w(9u^2+2u+9),\qquad
c=7u^3-27u^2-27u+7.                            \tag{11}
\]
The \(Q_i\) are literal primitive residual minors stored in the
verification programs.

There are three possible mechanisms for all minors in (9) to vanish.

### Both linear factors vanish

Exact elimination gives
\[
\operatorname{Res}_a(K_1,K_2)=-S_-(w)S_+(w),   \tag{12}
\]
where
\[
\begin{aligned}
S_-(w)&=7w^6-36w^5-27w^4-8w^3-27w^2-36w+7,\\
S_+(w)&=7w^6+36w^5-27w^4+8w^3-27w^2+36w+7.
\end{aligned}                                  \tag{13}
\]
Both sextics are primitive and irreducible over \(\mathbb Q\).
They correspond respectively to \(a=1\) and \(a=-1\).  Fresh
row reductions over
\(\mathbb Q[w]/(S_\pm)\) give contact rank four, but the unique
kernel is non-Veronese.  Both branches are therefore excluded by
\(E_6\).

### Exactly one linear factor vanishes

The two symmetric resultants are
\[
\begin{aligned}
\operatorname{Res}_a(K_1,Q_5)
=\operatorname{Res}_a(K_2,Q_0)
={}&-6w^2(w-1)^2(w+1)^2(u+1)^3\\
&\cdot G(w)^2H(w)^2,                           \tag{14}
\end{aligned}
\]
where
\[
\begin{aligned}
G(w)&=7w^8-156w^6+66w^4-12w^2+15,\\
H(w)&=15w^8-12w^6+66w^4-156w^2+7.
\end{aligned}
\]
On \(K_1=0\), so that \(a=-c/b\), one has the exact identities
\[
E_L=\frac{G(w)}
 {4(3u-4w+3)(3u+4w+3)},\qquad
E_M=\frac{H(w)}
 {4w(3u-4w+3)(3u+4w+3)}.                       \tag{15}
\]
Thus every octic root in (14) is an incidence boundary, not a
discarded denominator and not an exact-open survivor.

### Neither linear factor vanishes

The gcd of the five pairwise \(a\)-resultants of the \(Q_i\) is
\[
w^6(w-1)^8(w+1)^8(u+1)^5
\kappa_-^4\kappa_+^4(5u^2-6u+5)^2.             \tag{16}
\]
At \(u=-1\), the common polynomial in \(a\) is \(a^2+1\).
Its two roots are \(a=\pm w\); one makes \(E_L=0\), and the other
makes \(E_M=0\).  At
\[
5u^2-6u+5=0,                                   \tag{17}
\]
the common polynomial is
\[
10a^2+(-5w^3+11w)a+10.                         \tag{18}
\]
Modulo (17), its roots are
\[
a_1=\frac{3u-5}{4w},\qquad
a_2=\frac{3-5u}{4w},
\]
and satisfy \(E_M(a_1)=0\), \(E_L(a_2)=0\).
Consequently (16) yields no exact-open survivor.

## The alternate \(B=0\) chart

The generic basis must not be specialized at \(B=0\).  A fresh
six-by-six \(E_7\) pivot has determinant
\[
10368w^3(w-1)^2(w+1)^2(u+1)E_L^2E_M^2.         \tag{19}
\]
It is valid away from \(u=-1\).  Reducing the six contact minors
modulo \(B\), and eliminating \(a\), gives
\[
59049w\kappa_-^2\kappa_+^2
\cdot(5u^2-6u+5)^2P_{16}(w),                   \tag{20}
\]
where
\[
\begin{aligned}
P_{16}(w)={}&385w^{16}+9992w^{14}-23012w^{12}
 +53560w^{10}-24250w^8\\
&+53560w^6-23012w^4+9992w^2+385.               \tag{21}
\end{aligned}
\]
The PARI replay, which clears the alternate-basis denominators before
elimination, obtains the same factors together with
\(8192(u+1)^{11}\); the extra factor is precisely the singular chart
\(u=-1\), treated afresh below.

The quartic factor in (20) is again the routed boundary (17).
The polynomial \(P_{16}\) is primitive and irreducible over
\(\mathbb Q\).  On its only possible common-minor branch,
\[
\begin{aligned}
a={-w\over14417920}\big(&2626085w^{14}+67753107w^{12}
-167139687w^{10}\\
&+396647791w^8-228766929w^6+398117721w^4\\
&-168036781w^2+83754213\big).                  \tag{22}
\end{aligned}
\]
A fresh computation over
\(\mathbb Q[w]/(P_{16})\) gives contact rank five, excluding this
projection artifact.

## The isolated \(u=-1,a=0\) point

At \(u=-1\), equation \(B=0\) forces \(a=0\).  This point remains on
the exact open.  Here
\[
h=w(p^2+q^2),\qquad R=4wq^3,\qquad w^2=-1.      \tag{23}
\]
A fresh \(E_7\) basis gives contact rank three.  The restriction of
the Veronese equation \(Y^2-XZ\) to its two-dimensional kernel is,
in the recorded basis, \(-36t^2\).  Hence there is a unique
projective Veronese lift:
\[
(N_1,N_2,N_3)=(2p^2+q^2,q^2,0),\qquad
(x_5,y_5)=(-w,0).                               \tag{24}
\]
The top-only \(E_5\) coefficient vanishes, so no conclusion is drawn
until every lower coefficient is restored.

Write the free binary-cubic coefficients as \(u_i,v_i\), the
binary-quadratic coefficients as \(x_i,y_i,t_i\), and the linear
part as \(L_0=(\ell_{ij})_{0\le i,j\le2}\).
The full \(E_6\) solve has rank six.  After it, the \(r\)-coefficient
of \(E_5\) is
\[
18q^2\{p^2(u_2+2v_0-v_2)+q^2(-u_0+2u_2+v_0)\}. \tag{25}
\]
Thus
\[
u_0=2u_2+v_0,\qquad v_2=u_2+2v_0.              \tag{26}
\]
The constant part of \(E_5\) has a rank-three selected matrix.  Its
first compatibility equation is \(12v_0^2=0\), hence \(v_0=0\).
The remaining equations then force
\[
\begin{aligned}
u_0&=2u_2,&v_2&=u_2,\\
x_1&=-wu_1u_2,&y_1&=-wu_2v_1,\\
\ell_{02}&=u_2^2-wx_0,&
\ell_{12}&=-wy_0,&
\ell_{20}&=-wt_0u_2.                           \tag{27}
\end{aligned}
\]
The \(E_4\) identity fixes
\[
\ell_{10}=-wu_2y_0,\qquad
\ell_{00}=u_2^3-wu_2x_0.                       \tag{28}
\]
The \(E_6\) solve also gives \(\ell_{22}=-wt_0\).  Consequently
\[
\begin{pmatrix}\ell_{00}\\\ell_{10}\\\ell_{20}\end{pmatrix}
=u_2
\begin{pmatrix}\ell_{02}\\\ell_{12}\\\ell_{22}\end{pmatrix}.       \tag{29}
\]
After (27)--(28), the identities \(E_3,E_2,E_1\) vanish
identically, but (29) gives
\[
\det L_0=0.                                     \tag{30}
\]
The constant Jacobian coefficient is therefore zero, contradicting
the Keller condition.  This excludes the final exact-open point.

## Scope and verification

The theorem is confined to the squarefree-interior fixed divisor with
two ramification contacts in the exact-\(\delta=2,\{1,1\}\) row.
Incidence boundaries are routed to \(\delta\ge3\), and
\(\kappa_\pm=0\) is routed to the already separated \(\{2,0\}\)
analysis.

The strict replay is
`verify_delta2_11_interior_two_contacts_strict.sh`.  It runs:

- an exact SymPy reconstruction of both contact charts, all
  resultants, exact algebraic-field pivots, and the full lower chain;
- an independent PARI/GP reconstruction using separately scaled
  tangent bases, fresh polynomial-modulus pivots, and an independent
  full-lower determinant expansion.

The note and programs were prepared with AI assistance.  They are not
peer reviewed, and the exact checks certify only the algebra encoded
in the scripts.
