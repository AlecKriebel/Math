# Exact mixed-divisor \(\{1,1\}\) exclusion in the fixed-linear row

**Candidate checkpoint:** 2026-07-25T16:05:16Z  
**Status:** complete primary proof with exact dual-CAS checks; independent
hostile audit pending; not peer reviewed.

## 1. Statement

Let
\[
H_4=(P,Q,0)=(pA(p,q),pB(p,q),0),\qquad R=(H_3)_3,
\]
and put
\[
\alpha=J(Q,R),\qquad \beta=-J(P,R),\qquad
\gamma=J(P,Q).
\]
Suppose
\[
\gcd(\alpha,\beta,\gamma)\sim pq,                 \tag{1}
\]
where \(p=0\) is the marked fixed divisor and \(q=0\) is a distinct
unmarked divisor.

The common-root equations give
\[
\begin{aligned}
A&=q^2(a_2p+a_3q),\\
B&=p^3+b_1p^2q+b_2pq^2+b_3q^3,\\
R&=p\left(c_0p^2+\frac34b_1c_0pq+c_2q^2\right),
\qquad c_2\ne0.                                   \tag{2}
\end{aligned}
\]

**Candidate theorem.**  No quartic Keller counterexample satisfying
(1)--(2) lies on \(b_1\ne0\).  This is exactly the mixed-divisor
Hilbert--Burch component with splitting
\[
\{k_1,k_2\}=\{1,1\}.
\]

Together with `../delta2_mixed_k20/MIXED_K20_EXCLUSION.md`, this
provisionally excludes the entire exact mixed divisor \(g\sim pq\).
It does not exclude double-unmarked or two-unmarked divisors of degree
two.

## 2. The two tangent columns

Scale \(b_1=c_2=1\).  Define
\[
\begin{aligned}
N_p&=\frac1p(P_q,Q_q,R_q)^T,\\
N_q&=\frac1q\left(
(\partial_q-\tfrac14\partial_p)P,\,
(\partial_q-\tfrac14\partial_p)Q,\,
(\partial_q-\tfrac14\partial_p)R
\right)^T.                                        \tag{3}
\end{aligned}
\]
Both are polynomial syzygies of
\((\alpha,\beta,\gamma)\), and
\[
\begin{pmatrix}P_p&P_q\\Q_p&Q_q\\R_p&R_q\end{pmatrix}
=
\begin{pmatrix}N_p&N_q\end{pmatrix}
\begin{pmatrix}4p&p\\-4q&0\end{pmatrix},\qquad
\det\begin{pmatrix}4p&p\\-4q&0\end{pmatrix}=4pq.  \tag{4}
\]
On the exact stratum (1), (4) is a Hilbert--Burch basis with splitting
\(\{1,1\}\).

The degree-seven transverse dependence therefore has the form
\[
S=xN_p+yN_q.                                      \tag{5}
\]
The highest \(r\)-coefficient of \(E_6\), modulo the span of
\(\alpha,\beta\), gives five homogeneous contact equations in
\[
(x^2,xy,y^2,\lambda,\mu),                         \tag{6}
\]
where \(-\lambda r^2/2,-\mu r^2/2\) are the top \(r^2\)-terms in the
first two components of \(H_2\).

## 3. Exhaustive residual charts

At \(p=0\), coprimality gives \((a_3,b_3)\ne(0,0)\).  A target shear
and diagonal source/target scalings give two charts.

### 3.1 The chart \(a_3=0\)

Normalize
\[
A=pq^2,\qquad B=p^3+p^2q+q^3,\qquad
R=p(cp^2+\tfrac34cpq+q^2).                        \tag{7}
\]
The first contact coefficient is
\[
-\frac38y^2(49c-16).                              \tag{8}
\]
On \(y=0\), projectivize with \(x=1\); the five equations generate the
unit ideal.  At \(c=16/49\), the lifted contact matrix has rank four
and kernel
\[
\left(
-\frac6{419},-\frac{141}{838},\frac4{419},
-\frac{35}{419},1
\right).                                          \tag{9}
\]
It is not a Veronese point because
\[
\left(-\frac{141}{838}\right)^2
-\left(-\frac6{419}\right)\left(\frac4{419}\right)
=\frac{19977}{702244}\ne0.                        \tag{10}
\]
Thus this chart has no nonzero contact.

### 3.2 The chart \(a_3\ne0\)

Normalize
\[
\begin{aligned}
A&=q^2(ap+q),\\
B&=p^3+p^2q+bpq^2,\\
R&=p(cp^2+\tfrac34cpq+q^2).                       \tag{11}
\end{aligned}
\]

#### The projective chart \(y=0\)

Put \(x=1\).  Eliminating \(\mu,\lambda,a\) gives exactly
\[
(6bc-72b+7)(9bc^2-48bc-6c+16)=0.                 \tag{12}
\]
The apparent extra factor \(b=0\) in the raw resultant is impossible
already in the fourth contact equation.

The first component of (12) is
\[
\begin{aligned}
b&=\frac7{6(12-c)},&
a&=\frac{9(c-8)(c-4)}{2(c-12)},\\
\lambda&=-\frac{9c(c-4)}{c-12},&
\mu&=\frac7{c-12}.
\end{aligned}                                     \tag{13}
\]
All three original minors then contain, beyond \(pq\), the line
\[
3(c-8)p-q.                                        \tag{14}
\]

The second component is
\[
\begin{aligned}
b&=\frac{2(3c-8)}{3c(3c-16)},\\
a&=\frac{9c(3c^2-128)}
        {8(3c-16)(3c-8)},\\
\lambda&=-\frac{9c(3c^2-64c+128)}
              {4(3c-16)(3c-8)},\\
\mu&=-\frac{4(3c-8)}{c(3c-16)}.
\end{aligned}                                     \tag{15}
\]
All three minors contain \(pq\) times the nonzero quadratic
\[
\begin{aligned}
G_2={}&27c^3p^2+144c^2pq-1152cp^2-864cpq\\
     &+48cq^2-128q^2.                             \tag{16}
\end{aligned}
\]
The only nonautomatic denominator endpoint in (15),
\((c,b)=(8/3,0)\), has inconsistent contact equations.  Thus every
\(y=0\) contact leaves exact \(\delta=2\).

#### The chart \(y\ne0\)

Set \(y=1\).  The first contact equation is
\[
H:=ac-16a-48bc+6c+64=0.                           \tag{17}
\]
First take \(c\ne16\) and solve
\[
a=\frac{48bc-6c-64}{c-16}.                        \tag{18}
\]
Put
\[
\begin{aligned}
D={}&24bc-3c-32,\\
G={}&15bc^3-288bc^2+1536bc-2048b\\
   &\quad-8c^2+176c-768,\\
V={}&408b^2c^2-6528b^2c+27648b^2\\
   &\quad-171bc^2+2768bc-12032b\\
   &\quad+18c^2-296c+1328.                        \tag{19}
\end{aligned}
\]
The four-by-four lifted contact pivot has determinant
\[
-\frac{D^2G}{16(c-16)^2}.                         \tag{20}
\]

Both pivot divisors lie outside the exact stratum.  On \(D=0\), all
three minors contain \(pq^2\).  On \(G=0\), all contain \(pqL_G\), where
\[
L_G=(15c^2-192c+512)p+(4c-64)q.                   \tag{21}
\]
There is no lost denominator in this statement:
\[
\operatorname{Res}_c(
15c^3-288c^2+1536c-2048,\,
8c^2-176c+768)=2^{23}5^2.                         \tag{22}
\]

On the exact open, the unique lifted kernel, normalized by \(y^2=1\),
has
\[
\begin{aligned}
x^2_{\rm lift}&=\frac{3(4b-1)(c-16)}{16D},\\
x&=\frac{3(24b-5)(c-8)}{4D},\\
\lambda&=\frac{(24b-5)
(84bc^2-576bc-33c^2+464c-1536)}
{4(c-16)D},\\
\mu&=\frac{b(42bc-288b-9c+64)}{4D}.
\end{aligned}                                     \tag{23}
\]
The Veronese condition is exactly
\[
x^2-x^2_{\rm lift}=\frac{3V}{4D^2},               \tag{24}
\]
so a genuine contact requires \(V=0\).

## 4. The top-only \(E_5\) obstruction

Let \(\Phi(p,q)\) be the coefficient of \(r^2\) in \(E_5\) after
substituting (18), (23):
\[
\Phi=C_0p^3+C_1p^2q+C_2pq^2+C_3q^3.              \tag{25}
\]
Multilinearity of the determinant shows that this \(r^2\)-coefficient
is independent of every binary integration constant in \(H_3,H_2\),
every \(r\)-linear lower term in \(H_2\), and the full linear part.
The verification suite repeats this check with all such coefficients
symbolic.

Let \(\widetilde C_i\in\mathbb Z[b,c]\) be the primitive numerator of
\(C_i\).  Exact elimination gives
\[
\begin{aligned}
\operatorname{Res}_b(V,\widetilde C_0)
={}&2687385600(c-16)^6(c-8)^6\\
&\quad\cdot(57c^2-960c+4096),\\
\operatorname{Res}_b(V,\widetilde C_1)
={}&2902376448(c-16)^8(c-8)^6\\
&\quad\cdot(11925c^4-398990c^3+5022128c^2\\
&\qquad\qquad-28184576c+59506688).
\end{aligned}                                     \tag{26}
\]
The two residual factors are coprime; their resultant is
\[
20654497726464=2^{32}\cdot3\cdot7\cdot229.        \tag{27}
\]
Hence \(V=C_0=C_1=0\) forces \(c=8\) or \(c=16\).

At \(c=8\),
\[
V=16(4b-1)(24b-7).                                \tag{28}
\]
The root \(b=1/4\) lies on \(G=0\), and \(b=7/24\) lies on \(D=0\);
both already have larger gcd.

It remains to treat \(c=16\) without dividing by \(c-16\).  Equation
(17) gives \(b=5/24\).  The case \(a=0\) has an additional factor
\(q\) in the three reduced minors.  For \(a\ne0\), contact forces
\[
9a^2-68a+144=0,                                   \tag{29}
\]
with
\[
x=\frac{9a-32}{96},\quad
\lambda=-\frac{19a-64}{32},\quad
\mu=\frac{15a}{1024}-\frac{15}{256}.              \tag{30}
\]
Modulo (29), the \(p^3r^2\)-coefficient of \(E_5\) is
\[
\frac5{16}(3a-10).                                \tag{31}
\]
It cannot vanish because
\[
\operatorname{Res}_a(9a^2-68a+144,3a-10)=156.     \tag{32}
\]
This exhausts every nonzero contact in the second residual chart.

## 5. Zero contact

If \(x=y=0\), the degree-six shifted syzygy block is injective: its
required row degrees are \((1,1,0)\), below both minimal
\(\{1,1\}\) Hilbert--Burch columns in (3).  Consequently every
nonlinear term is binary.  After linear source and target changes, the
map is a plane Keller map of degree at most four over
\(\mathbb C(r)\), together with a triangular shear.  The unconditional
plane low-degree theorem makes it birational; a birational Keller map is
a polynomial automorphism.

Thus neither zero nor nonzero contact can support a counterexample,
proving the candidate theorem.

## 6. Verification and disclosure

`verify_mixed_k11_sympy.py` reconstructs both residual charts, the
Hilbert--Burch columns, the projective contact decomposition, every
higher-gcd routing, the full-lower top-only assertion, both resultants,
and the \(c=16\) endpoint.

`verify_mixed_k11_pari.gp` independently reconstructs the raw Jacobians
and determinant coefficients in PARI/GP.  It obtains (12) by a different
iterated-resultant elimination and independently checks (22), (26),
(27), and (32).  The strict wrapper rejects optimized Python and PARI
runs that do not reach their terminal certificate.

These exact checks are evidence about the encoded algebra, not peer
review.  The residual group-action normal forms and zero-contact
plane-field exit remain subject to independent hostile checking.  AI
systems materially assisted this work.
