# Qutrit Hodge--Plücker structure and the obstruction to orbitwise injection

## Research log

- **2026-07-28 12:46 PDT.** Began a \(d=3\) exterior-algebra attack on the
  weighted comparison between the logical symmetric square and the logical
  exterior line.  The intended mechanism was to use
  \(\Lambda ^2\mathbb C^3\simeq\overline{\mathbb C^3}\) to inject each
  antisymmetric output into three symmetric outputs.
- **2026-07-28 13:08 PDT.** Derived an exact Hodge--Walsh decomposition of
  every ordered-basis-pair orbit.  Within each orbit, all common-code
  information is carried by four Walsh transforms satisfying a pointwise
  holomorphic Plücker identity.
- **2026-07-28 13:08 PDT.** Found an exact equality code having a strictly
  negative full-difference Hodge orbit.  Thus no proof can dominate the odd
  weight orbit by orbit, even after using the pointwise Plücker relation.
  The compensation comes from different unordered-pair orbits.
- **2026-07-28 13:08 PDT.** For a four-amplitude family, the cross-orbit
  compensation combines into one Hermitian Plücker square.  The calculation
  extends to an exact all-copy sum of squares for flagged GHZ-type codes.
- **2026-07-28 13:11 PDT.** Independently replayed the full sector table
  (38) and formula (51) for \(2\leq n\leq6\) with rational arithmetic.
  The replay is only an audit; the proofs below are symbolic and uniform in
  \(n\).

No all-copy proof or counterexample is obtained here.  The exact outcome is
a structural formula, a sharp obstruction to the most direct Hodge
injection, and a nonproduct all-\(n\) subclass on which the desired
inequality is proved.

## 1. The weighted symmetric-versus-exterior target

Let
\[
H_n=(\mathbb C^3)^{\otimes n},\qquad
U:K=\mathbb C^2\longrightarrow H_n
\]
be an isometry.  Write its orthonormal columns as \(u,v\), and put
\(P=UU^\dagger\).  On two replicas of \(H_n\), let \(F_i\) swap the \(i\)-th
qutrits and set
\[
S_i=\frac{I+F_i}{2},\qquad A_i=\frac{I-F_i}{2},\qquad
\Pi_R=\prod_{i\in R}A_i\prod_{i\notin R}S_i .
\tag{1}
\]
The sector masses are
\[
p_R=\operatorname{Tr}[(P\otimes P)\Pi_R].
\tag{2}
\]
The full physical swap acts as the logical swap on
\((U\otimes U)(K\otimes K)\).  Hence
\[
\sum_{\lvert R\rvert\ {\rm even}}p_R=3,\qquad
\sum_{\lvert R\rvert\ {\rm odd}}p_R=1.
\tag{3}
\]

The positive local weight
\[
Y_i=S_i+3A_i=2I-F_i
\tag{4}
\]
preserves the logical symmetric and exterior subspaces.  Its compressed
trace on these two subspaces is respectively
\[
\sum_{\lvert R\rvert\ {\rm even}}3^{\lvert R\rvert}p_R,
\qquad
\sum_{\lvert R\rvert\ {\rm odd}}3^{\lvert R\rvert}p_R.
\tag{5}
\]
Their difference is
\[
D_n(P):=
\sum_{\lvert R\rvert\ {\rm even}}3^{\lvert R\rvert}p_R
-
\sum_{\lvert R\rvert\ {\rm odd}}3^{\lvert R\rvert}p_R
=2^nQ_n(P).
\tag{6}
\]
Thus the endpoint problem asks whether the trace on
\(\operatorname{Sym}^2K\), which has dimension three, always dominates the
single eigenvalue on \(\Lambda^2K\).

Using (3), the same global quantity has the baseline-subtracted form
\[
\mathscr W(P)=
\sum_{\substack{\lvert R\rvert\ {\rm even}}}
 (3^{\lvert R\rvert}-1)p_R
-
\sum_{\substack{\lvert R\rvert\ {\rm odd}}}
 (3^{\lvert R\rvert}-3)p_R
=D_n(P).
\tag{7}
\]
The coefficients at levels zero and one vanish.  For \(n=3\), if
\[
E_2=\sum_{\lvert R\rvert=2}p_R,
\]
then
\[
\mathscr W(P)=8E_2-24p_{\{1,2,3\}}
=8\bigl(E_2-3p_{\{1,2,3\}}\bigr).
\tag{8}
\]
Consequently the exact three-copy target is
\[
E_2\geq3p_{\{1,2,3\}}.
\tag{9}
\]

## 2. Local qutrit Hodge identities

Put \(V=\mathbb C^3\), with orthonormal basis
\(e_1,e_2,e_3\), and normalize
\[
x\wedge y=\frac{x\otimes y-y\otimes x}{\sqrt2}.
\tag{10}
\]
Let \(\epsilon_{kab}\) be the Levi--Civita symbol and define the
complex-linear Hodge map
\[
h:\Lambda^2V\longrightarrow\overline V,\qquad
h(e_a\wedge e_b)=\sum_{k=1}^3\epsilon_{kab}\,\overline e_k
\quad(a<b).
\tag{11}
\]
For the real skew matrices
\[
(L_k)_{ab}=\epsilon_{kab},
\tag{12}
\]
one has
\[
[h(x\wedge y)]_k=x^TL_ky.
\tag{13}
\]

### Lemma 2.1 (Levi contraction)

For \(x,y\in V\) and \(M\in M_3(\mathbb C)\),
\[
\sum_{k=1}^3|x^TL_ky|^2
=\|x\|^2\|y\|^2-|\langle x,y\rangle|^2,
\tag{14}
\]
and
\[
\boxed{\qquad
\sum_{k=1}^3L_kM^TL_k^\dagger
=\operatorname{Tr}(M)I-M.
\qquad}
\tag{15}
\]
In particular, \(h\) is unitary.

#### Proof

The elementary epsilon contraction is
\[
\sum_k\epsilon_{kia}\epsilon_{kjb}
=\delta_{ij}\delta_{ab}-\delta_{ib}\delta_{aj}.
\tag{16}
\]
The \((i,j)\) entry of the left side of (15) is therefore
\[
\sum_{k,a,b}\epsilon_{kia}M_{ba}\epsilon_{kjb}
=\delta_{ij}\sum_aM_{aa}-M_{ij}.
\]
This is (15).  Applying the same contraction directly to
\(\sum_k(x^TL_ky)\overline{(x^TL_ky)}\) gives (14).  The right side of
(14) is exactly \(\|x\wedge y\|^2\), proving that \(h\) is isometric and
hence unitary. \(\square\)

For \(g\in SU(3)\), the determinant-one epsilon identity also gives
\[
h\bigl((gx)\wedge(gy)\bigr)=\overline g\,h(x\wedge y).
\tag{17}
\]
Thus (11) is the qutrit-specific equivalence
\(\Lambda^2V\simeq\overline V\).  Formula (15) is the corresponding
reduction-map identity and is often the more useful form for contractions.

### Lemma 2.2 (the nonlinear plane lift)

Let \(E=\operatorname{span}\{x,y\}\subset V\), where \(x,y\) are
orthonormal.  There is a unique unit vector \(\nu\), up to phase, normal
to \(E\), and
\[
h(x\wedge y)=\overline\nu
\tag{18}
\]
up to the same phase convention.  Consequently
\[
P_E=I-|\nu\rangle\langle\nu|,
\qquad
\Pi_{\operatorname{Sym}^2E}
=S(P_E\otimes P_E)S,
\tag{19}
\]
where \(S=(I+F)/2\).  Moreover,
\[
\operatorname{Tr}\Pi_{\operatorname{Sym}^2E}=3,
\qquad
\operatorname{Tr}|x\wedge y\rangle\langle x\wedge y|=1.
\tag{20}
\]

#### Proof

Writing \(c_k=x^TL_ky\), the alternating determinant with two equal
columns shows \(c^Tx=c^Ty=0\).  Hence the vector with coordinates
\(\overline c_k\) is Hermitian-orthogonal to \(x,y\).  Its norm is one by
(14), proving (18).  The first identity in (19) follows.  The second is
the orthogonal projector onto the symmetric square of the range of
\(P_E\).  Finally, a two-dimensional space has symmetric-square dimension
three and exterior-square dimension one. \(\square\)

This is exactly the desired local factor \(3:1\), but it is nonlinear:
the exterior vector first determines \(\nu\), then
\(I-|\nu\rangle\langle\nu|\), and only then the three-dimensional
symmetric square.  For a general entangled code \(u,v\in V^{\otimes n}\),
there is no fixed local two-plane to which Lemma 2.2 can be applied
independently at every site.

There is also a representation-theoretic obstruction to replacing this
nonlinear lift by a canonical linear one.

### Lemma 2.3 (no equivariant linear Hodge injection into the symmetric square)

Every complex-linear \(SU(3)\)-equivariant map
\[
J:\Lambda^2V\longrightarrow\operatorname{Sym}^2V
\tag{21}
\]
is zero.

#### Proof

Apply the diagonal torus
\(\operatorname{diag}(z_1,z_2,z_3)\), where
\(z_1z_2z_3=1\).  The only vector in \(\operatorname{Sym}^2V\) with the
same torus weight as \(e_1\wedge e_2\) is a scalar multiple of
\(e_1\mathbin{\odot}e_2\).  Hence
\[
J(e_1\wedge e_2)=c\,e_1\mathbin{\odot}e_2.
\tag{22}
\]
The special unitary that exchanges \(e_1,e_2\) and sends
\(e_3\) to \(-e_3\) negates \(e_1\wedge e_2\) but fixes
\(e_1\mathbin{\odot}e_2\).  Equivariance forces \(c=-c\), so \(c=0\).
The same argument for the other two basis pairs proves \(J=0\).
\(\square\)

Lemma 2.3 does not prohibit a code-dependent nonlinear construction, but
it rules out the simplest fixed equivariant injection.

## 3. Exact Hodge--Walsh decomposition by unordered-pair orbits

The common-code constraints become transparent after decomposing the
ordered product basis into local-swap orbits.

Fix, at every site \(i\), an unordered pair of qutrit labels
\(\{\alpha_i,\beta_i\}\), allowing \(\alpha_i=\beta_i\).  Let
\[
D=\{i:\alpha_i\neq\beta_i\},\qquad m=|D|.
\tag{23}
\]
For \(T\subseteq D\), define the string \(x_T\) by selecting
\(\beta_i\) at the sites in \(T\), \(\alpha_i\) at the sites in
\(D\setminus T\), and the common label outside \(D\).  The associated
ordered-pair orbit is
\[
\mathcal O=\operatorname{span}\{
 |x_T\rangle\otimes|x_{T^c}\rangle:T\subseteq D\}.
\tag{24}
\]
These mutually orthogonal orbits partition the ordered product basis of
\(H_n\otimes H_n\).  On \(\mathcal O\), the local swap \(F_i\) sends
\(T\) to \(T\mathbin\triangle\{i\}\) for \(i\in D\), and is the identity
for \(i\notin D\).

For \(R\subseteq D\), define the normalized Walsh character
\[
|\eta_R^{\mathcal O}\rangle
=2^{-m/2}\sum_{T\subseteq D}
(-1)^{|R\cap T|}
|x_T\rangle\otimes|x_{T^c}\rangle.
\tag{25}
\]
Then \(\eta_R^{\mathcal O}\) has local antisymmetry pattern \(R\), and
\(\Pi_R\) restricts to its rank-one projector on \(\mathcal O\).  If
\(R\not\subseteq D\), the restriction of \(\Pi_R\) to \(\mathcal O\)
vanishes.

Write
\[
U(T)=\langle x_T,u\rangle,\qquad
V(T)=\langle x_T,v\rangle,
\tag{26}
\]
and define four orbit functions
\[
\begin{aligned}
q(T)&=U(T)U(T^c),\\
r(T)&=V(T)V(T^c),\\
s(T)&=\frac{U(T)V(T^c)+V(T)U(T^c)}{\sqrt2},\\
a(T)&=\frac{U(T)V(T^c)-V(T)U(T^c)}{\sqrt2}.
\end{aligned}
\tag{27}
\]
For any function \(f\) on the cube \(2^D\), use the unitary Walsh
transform
\[
\widehat f(R)=2^{-m/2}\sum_{T\subseteq D}
(-1)^{|R\cap T|}f(T).
\tag{28}
\]

### Proposition 3.1 (Hodge--Walsh orbit formula)

Let \(p_R^{\mathcal O}\) denote the contribution of the orbit
\(\mathcal O\) to \(p_R\).  Then
\[
\boxed{
\begin{aligned}
p_R^{\mathcal O}
 &=|\widehat q(R)|^2+|\widehat r(R)|^2
   +|\widehat s(R)|^2,
 && |R|\ {\rm even},\\
p_R^{\mathcal O}
 &=|\widehat a(R)|^2,
 && |R|\ {\rm odd}.
\end{aligned}}
\tag{29}
\]
Moreover,
\[
\boxed{\qquad s(T)^2-a(T)^2=2q(T)r(T)
\qquad(T\subseteq D).\qquad}
\tag{30}
\]

#### Proof

An orthonormal logical basis adapted to the full logical swap is
\[
u\otimes u,\quad v\otimes v,\quad
\frac{u\otimes v+v\otimes u}{\sqrt2},\quad
\frac{u\otimes v-v\otimes u}{\sqrt2}.
\tag{31}
\]
Their coefficients on the ordered basis vector indexed by \(T\) in
(24) are respectively \(q(T),r(T),s(T),a(T)\).  Taking the inner product
with (25) gives the four Walsh coefficients in (28).  The first three
logical vectors are globally symmetric, so their transforms vanish for
odd \(|R|\); the last is globally antisymmetric, so its transform
vanishes for even \(|R|\).  Summing the squared projection norms of the
four orthonormal logical vectors proves (29).

If
\[
\xi=U(T)V(T^c),\qquad \zeta=V(T)U(T^c),
\]
then \(s=(\xi+\zeta)/\sqrt2\), \(a=(\xi-\zeta)/\sqrt2\), and therefore
\[
s^2-a^2=2\xi\zeta
=2U(T)U(T^c)V(T)V(T^c)=2qr.
\]
This proves (30). \(\square\)

At an antisymmetric site, (25) contains a normalized wedge of two
distinct qutrit labels.  Applying \(h\) replaces that wedge by its unique
missing qutrit label and preserves its norm.  Thus (29) is also a literal
decomposition into orthogonal Hodge-labelled blocks.  Identity (30) is
the exact holomorphic Plücker relation that records the common origin of
the four block amplitudes.

The crucial issue is that (30) is pointwise before the Walsh transform,
whereas the target assigns exponentially different weights to different
Walsh frequencies.  The next example shows that (30) cannot make the
target nonnegative separately on each orbit.

## 4. Exact obstruction to every orbitwise weighted injection

Work on three copies and define
\[
u=\frac{|000\rangle+|011\rangle}{\sqrt2},\qquad
v=\frac{|100\rangle+|111\rangle}{\sqrt2}.
\tag{32}
\]
These are orthonormal.  Consider the full-difference orbit
\(\mathcal O_*\) with base pair \((000,111)\), so
\(D=\{1,2,3\}\).  With the convention of (24), the only nonzero entries
in (27) occur at
\[
T=\varnothing,\ \{1\},\ \{2,3\},\ \{1,2,3\}.
\]
They are
\[
\begin{array}{c|cccc}
T&\varnothing&\{1\}&\{2,3\}&\{1,2,3\}\\ \hline
s(T)&\frac1{2\sqrt2}&\frac1{2\sqrt2}
    &\frac1{2\sqrt2}&\frac1{2\sqrt2}\\[2mm]
a(T)&\frac1{2\sqrt2}&-\frac1{2\sqrt2}
    &\frac1{2\sqrt2}&-\frac1{2\sqrt2}.
\end{array}
\tag{33}
\]
On this orbit \(q=r=0\), so the Plücker relation (30) is satisfied
identically.  The nonzero Walsh coefficients are
\[
\widehat s(\varnothing)=\widehat s(\{2,3\})=\frac12,
\qquad
\widehat a(\{1\})=\widehat a(\{1,2,3\})=\frac12.
\tag{34}
\]
Thus this single orbit places mass \(1/4\) in each of those four sectors.
Its direct contribution to the weighted symmetric-minus-exterior
difference (6) is
\[
\frac{1+9}{4}-\frac{3+27}{4}=-5.
\tag{35}
\]
Its contribution to the baseline-subtracted expression (7) is
\[
8\cdot\frac14-24\cdot\frac14=-4.
\tag{36}
\]
Both are strictly negative.

The full code nevertheless has equality.  Indeed,
\[
P=(|0\rangle\langle0|+|1\rangle\langle1|)
\otimes|\Phi\rangle\langle\Phi|,
\qquad
|\Phi\rangle=\frac{|00\rangle+|11\rangle}{\sqrt2}.
\tag{37}
\]
On the first site, the two-dimensional projection has symmetric and
antisymmetric masses \(3\) and \(1\).  On sites \(2,3\), the two replicas
of \(\Phi\) have mass \(3/4\) in the all-symmetric sector and \(1/4\) in
the doubly antisymmetric sector.  Tensoring gives exactly
\[
\begin{array}{c|cccc}
R&\varnothing&\{1\}&\{2,3\}&\{1,2,3\}\\ \hline
p_R&\frac94&\frac34&\frac34&\frac14,
\end{array}
\tag{38}
\]
with every other \(p_R\) equal to zero.  Therefore
\[
\sum_{|R|\ {\rm even}}3^{|R|}p_R=9
=\sum_{|R|\ {\rm odd}}3^{|R|}p_R,
\qquad
Q_3(P)=0.
\tag{39}
\]
In the baseline-subtracted form, the positive contribution is
\(8(3/4)=6\), and the negative contribution is \(24(1/4)=6\).

Equations (35)--(39) prove the following obstruction.

### Corollary 4.1

There is no proof of (6) that assigns a nonnegative weighted
symmetric-minus-exterior contribution to each unordered-pair orbit (or
to each corresponding Hodge missing-label block) separately.  This
remains false even if the proof uses the full pointwise Plücker relation
(30) inside each orbit.

The conclusion persists for every \(n\geq3\): append to both \(u\) and
\(v\) the same product qutrit at every new site.  Every added site is
locally symmetric, so the negative orbit contribution (35), or (36),
is unchanged.  Globally,
\[
Q_{n+1}(P\otimes|0\rangle\langle0|)
=\frac12Q_n(P)=0.
\tag{40}
\]
Hence the missing compensation must mix distinct unordered-pair orbits,
and this obstruction is uniform in the number of copies.

## 5. A genuinely nonlinear cross-orbit square at three copies

The preceding equality is part of a larger family for which the
cross-orbit compensation can be evaluated exactly.  Let
\[
\begin{aligned}
u&=|0\rangle\otimes(a|00\rangle+b|11\rangle),\\
v&=|1\rangle\otimes(c|00\rangle+d|11\rangle),
\end{aligned}
\qquad
|a|^2+|b|^2=|c|^2+|d|^2=1.
\tag{41}
\]
The vectors are orthonormal.  Put \(P=|u\rangle\langle u|+
|v\rangle\langle v|\).

The self-pair orbit of \(u\) with difference mask \(\{2,3\}\) contributes
\[
8|ab|^2
\tag{42}
\]
to \(\mathscr W(P)\); the corresponding orbit of \(v\) contributes
\[
8|cd|^2.
\tag{43}
\]
All diagonal orbits and the cross orbits with difference mask \(\{1\}\)
have zero coefficient in (7).

It remains to calculate the one full-difference cross orbit.  Set
\[
A=ad,\qquad B=bc.
\tag{44}
\]
Its even Walsh coefficients are
\[
\begin{array}{c|cccc}
R&\varnothing&\{2,3\}&\{1,2\}&\{1,3\}\\ \hline
\widehat s(R)&(A+B)/2&(A+B)/2&(A-B)/2&(A-B)/2,
\end{array}
\tag{45}
\]
and its odd coefficients are
\[
\begin{array}{c|cccc}
R&\{1\}&\{1,2,3\}&\{2\}&\{3\}\\ \hline
\widehat a(R)&(A+B)/2&(A+B)/2&(A-B)/2&(A-B)/2.
\end{array}
\tag{46}
\]
Using the coefficients \(8\) at level two and \(-24\) at level three,
its contribution to (7) is
\[
\begin{aligned}
\mathscr W_{\rm cross}
&=2|A+B|^2+4|A-B|^2-6|A+B|^2\\
&=-16\operatorname{Re}(A\overline B).
\end{aligned}
\tag{47}
\]
Combining (42), (43), and (47), and observing that
\[
A\overline B
=ad\,\overline{bc}
=(a\overline b)\,\overline{(c\overline d)},
\]
gives the exact Hermitian Plücker square
\[
\boxed{\qquad
\mathscr W(P)
=8\left|a\overline b-c\overline d\right|^2,
\qquad
Q_3(P)=\left|a\overline b-c\overline d\right|^2.
\qquad}
\tag{48}
\]

This square is genuinely cross-orbit.  The negative term (47) comes from
the full-difference orbit, while its two positive diagonal terms come
from two different self-pair orbits.  For
\(a=b=c=d=1/\sqrt2\), (48) is the equality code (32).

## 6. An all-copy flagged-GHZ sum of squares

The mechanism in (48) survives uniformly in the number of copies.  The
following is an exact nonproduct subclass theorem.

### Theorem 6.1

Let \(m\geq1\), \(n=m+1\), and
\[
\begin{aligned}
u&=|0\rangle\otimes
   (a|0^m\rangle+b|1^m\rangle),\\
v&=|1\rangle\otimes
   (c|0^m\rangle+d|1^m\rangle),
\end{aligned}
\qquad
|a|^2+|b|^2=|c|^2+|d|^2=1.
\tag{49}
\]
For \(P=|u\rangle\langle u|+|v\rangle\langle v|\), put
\[
\delta=|a|^2-|c|^2,\qquad
z=a\overline b-c\overline d.
\tag{50}
\]
Then
\[
\boxed{\qquad
Q_n(P)=|z|^2+
2^{-m}\bigl(1-(-1)^m\bigr)\delta^2\geq0.
\qquad}
\tag{51}
\]
If \(n\) is odd, equality holds exactly when \(z=0\).  If \(n\) is even,
equality holds exactly when \(z=\delta=0\).

#### Proof

For operators on \(m\) qutrits define the Hermitian sesquilinear form
\[
\mathfrak B_m(C,D)
=\operatorname{Tr}\!\left[
 (C^\dagger\otimes D)
 \prod_{i=1}^m\left(F_i-\frac12I\right)\right],
\qquad
Q_m(C)=\mathfrak B_m(C,C).
\tag{52}
\]
It tensorizes over physical sites.  For
\(p_j=|j\rangle\langle j|\), \(j=0,1\), direct one-site contraction gives
\[
\mathfrak B_1(p_0,p_0)=\mathfrak B_1(p_1,p_1)=\frac12,
\qquad
\mathfrak B_1(p_0,p_1)=-\frac12.
\tag{53}
\]

Set
\[
x=a|0^m\rangle+b|1^m\rangle,\qquad
y=c|0^m\rangle+d|1^m\rangle,
\]
\[
A=|x\rangle\langle x|,\qquad B=|y\rangle\langle y|.
\]
Since \(P=p_0\otimes A+p_1\otimes B\), (53) and tensorization imply
\[
Q_n(P)=\frac12Q_m(A-B).
\tag{54}
\]

On the repetition subspace spanned by
\(e_0=|0^m\rangle,e_1=|1^m\rangle\), the Hermitian operator
\(C=A-B\) is
\[
C=\delta E_{00}-\delta E_{11}+zE_{01}+\overline zE_{10},
\qquad
E_{jk}=|e_j\rangle\langle e_k|.
\tag{55}
\]
The one-site contractions, followed by tensorization, are
\[
\begin{aligned}
\mathfrak B_m(E_{00},E_{00})
&=\mathfrak B_m(E_{11},E_{11})=2^{-m},\\
\mathfrak B_m(E_{00},E_{11})
&=(-1)^m2^{-m},\\
\mathfrak B_m(E_{01},E_{01})
&=\mathfrak B_m(E_{10},E_{10})=1,
\end{aligned}
\tag{56}
\]
and every pairing between a displayed diagonal and off-diagonal unit, or
between \(E_{01}\) and \(E_{10}\), is zero.  Substituting (55) into (56)
therefore gives
\[
Q_m(C)=2|z|^2+
2^{1-m}\bigl(1-(-1)^m\bigr)\delta^2.
\tag{57}
\]
Equations (54) and (57) prove (51).  The equality statement follows
because the displayed summands are nonnegative, and the coefficient of
\(\delta^2\) vanishes exactly when \(m\) is even, equivalently when
\(n\) is odd. \(\square\)

For \(n=3\), the \(\delta\)-coefficient vanishes and Theorem 6.1 reduces
exactly to (48).  Thus the three-copy Hodge square is the first member of
a uniform parity-sensitive sum-of-squares family.

## 7. Consequences for the full program

The qutrit Hodge route exposes both a useful nonlinear invariant and a
precise limitation.

1. Proposition 3.1 is an exact structural formula for arbitrary codes.
   It reduces every Hodge-labelled orbit to four Walsh transforms tied by
   the pointwise Plücker identity (30).
2. The local \(3:1\) dimension ratio is real, but Lemma 2.3 rules out a
   fixed equivariant linear injection from the exterior representation
   into the symmetric square.
3. Corollary 4.1 is stronger than the absence of a convenient estimate:
   an individual Hodge orbit can have strictly negative weighted deficit
   even inside a global equality code.  Any successful injection or sum
   of squares must move weight between different unordered-pair orbits.
4. The pointwise holomorphic relation \(s^2-a^2=2qr\) is insufficient by
   itself.  In the negative orbit it reduces to \(s^2=a^2\).  The repairing
   identity (48) instead uses Hermitian products and normalization across
   self-pair and cross-pair orbits.
5. Theorem 6.1 shows that this cross-orbit mechanism is not confined to a
   finite-copy numerical pattern: on a nonproduct family it gives a
   closed exact formula for every \(n\).

What remains open is a global analogue of (48) for arbitrary amplitude
tensors.  A viable Hodge proof would have to organize all unordered-pair
orbits simultaneously, using the fact that their amplitudes come from the
same two vectors \(u,v\).  A code-dependent nonlinear lift or a global
Hermitian Plücker/Gram identity remains possible; an orbitwise lift does
not.
