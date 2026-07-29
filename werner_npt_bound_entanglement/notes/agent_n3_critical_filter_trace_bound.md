# An extremal adapted-frame bound for full-support pair-sector critical points

## Status

This note audits equations (26), (45), and (48) of
`agent_n3_full_support_filter_classification.md` and proves a new exact
restriction on an interior critical point of the qutrit three-copy
pair-sector problem.

Let
\[
f=\|\Pi _2C\|_2^2
\]
at a normalized rank-two critical point, and write \(w_k\) for the
squared mass of \(C\) in local traceless degree \(k\).  If all one-site
left and right densities are positive definite, then
\[
\boxed{16w_1+53f+3w_3\le42.}                          \tag{1}
\]
In particular,
\[
\boxed{f\le\frac{42}{53}=0.7924528301\ldots.}          \tag{2}
\]

The key qutrit fact is elementary but nonlinear: for every unit
traceless Hermitian direction \(n\), the seven-dimensional hyperplane
\(n^\perp\) contains three orthonormal matrices, each having spectrum
\[
\frac1{\sqrt6}(2,-1,-1).
\]
Thus an adapted seven-frame can always be chosen with three directions
at the maximal spectral radius squared \(2/3\); the other four retain
the universal floor \(1/2\).

The proposed basis average in the research log is also correct and
gives \(f\le78/97\).  A subsequent cubic Haar average improves that to
\(f<51/64\).  The explicit three-extremal-direction construction in
this note is stronger than both.

This remains short of the required \(f\le2/3\), so it does not close
the unrestricted three-copy theorem.  It is an exact nonlinear
restriction on every hypothetical full-support critical violator.

The independent exact checker is
`verification/verify_n3_critical_filter_trace_bound.py`.

## 1. One-site filter equations

Let \(\rho>0\) be a normalized one-site density:
\[
\operatorname{Tr}\rho=1,\qquad p=\operatorname{Tr}\rho^2.             \tag{3}
\]
Put
\[
c=\frac23,\qquad \delta=f-c.
\]
At a hypothetical critical point with \(f>2/3\), the established
one-site residual inequality is
\[
\boxed{
\|T_0(B)\|_2^2+\delta\,r(B)^2
\le c\,{\cal N}(B,B)
\quad\text{if }\operatorname{Tr}(B\rho)=0,}            \tag{4}
\]
where
\[
{\cal N}(A,B)=\operatorname{Tr}(A^\dagger B\rho)
\]
and \(r(B)\) denotes spectral radius.  The corresponding one-site
Gram trace is
\[
\boxed{
\operatorname{Tr}_{HS}{\cal G}
=fp+\operatorname{Tr}_{HS}(T_0^\dagger T_0).}          \tag{5}
\]

## 2. The adapted-basis identities

Let \(F_1,\ldots,F_8\) be a Hilbert--Schmidt orthonormal basis of the
real space \(V\) of traceless Hermitian \(3\times3\) matrices.  Put
\[
\mu_a=\operatorname{Tr}(F_a\rho),\qquad
B_a=F_a-\mu_aI.                                       \tag{6}
\]
Then \(\operatorname{Tr}(B_a\rho)=0\), and \(T_0(B_a)=T_0(F_a)\)
because \(T_0(I)=0\).

### Lemma 2.1

For every such basis,
\[
\boxed{\sum_{a=1}^8{\cal N}(B_a,B_a)=3-p.}             \tag{7}
\]

#### Proof

Hilbert--Schmidt completeness, after adjoining \(I/\sqrt3\), gives
\[
\sum_{a=1}^8F_a^2=\frac83I.                            \tag{8}
\]
Writing \(\sigma=\rho-I/3\), Parseval gives
\[
\sum_a\mu_a^2=\|\sigma\|_2^2=p-\frac13.                \tag{9}
\]
Moreover
\[
{\cal N}(B_a,B_a)
=\operatorname{Tr}(F_a^2\rho)-\mu_a^2.
\]
Summing and using (8)--(9) proves (7). \(\square\)

Assume first that \(\sigma\ne0\), choose
\[
F_1=n:=\frac{\sigma}{\|\sigma\|_2},                    \tag{10}
\]
and complete \(n\) orthonormally.  Then
\[
\mu_1=\sqrt{p-\frac13},\qquad \mu_a=0\quad(a\ge2).
\]
For the distinguished direction,
\[
\|B_1\|_2^2=3p,
\]
so
\[
r(B_1)^2\ge p.                                         \tag{11}
\]
Every unit \(F\in n^\perp\) is traceless Hermitian and obeys
\[
r(F)^2\ge\frac12.                                      \tag{12}
\]
Indeed, write the largest positive and negative eigenvalue magnitudes
as \(u,v\), so the third eigenvalue is \(v-u\).  If, say, \(u\ge v\),
then
\[
1=u^2+v^2+(u-v)^2
=2u^2-2v(u-v)\le2u^2;
\]
the other ordering is symmetric.
This proves the elementary estimate
\[
\sum_ar(B_a)^2\ge\frac72+p.                            \tag{13}
\]
Substitution in (4)--(5) gives
\[
\operatorname{Tr}_{HS}{\cal G}
\le\frac{13}{3}-\frac72f,
\]
and hence \(32w_1+97f+6w_3\le78\).  Thus the proposed
\(f\le78/97\) calculation and all of its constants are correct.

The next section improves the freely chosen orthonormal completion of
\(n\).

## 3. Three extremal matrices in every qutrit hyperplane

For a unit vector \(z\in\mathbb C^3\), define
\[
E_z=\sqrt{\frac32}\left(|z\rangle\langle z|-\frac13I\right)
=\frac{3|z\rangle\langle z|-I}{\sqrt6}.                \tag{14}
\]
Then \(E_z\in V\), \(\|E_z\|_2=1\), and
\[
\operatorname{spec}(E_z)
=\frac1{\sqrt6}(2,-1,-1),\qquad
r(E_z)^2=\frac23.                                      \tag{15}
\]
Also
\[
\langle E_z,E_y\rangle
=\frac32\left(|\langle z,y\rangle|^2-\frac13\right).
\tag{16}
\]

### Lemma 3.1 (zero-expectation probability vector)

Let \(\lambda_0+\lambda_1+\lambda_2=0\).  There is a probability
vector \(w=(w_0,w_1,w_2)\) such that
\[
\sum_kw_k\lambda_k=0,\qquad
\sum_kw_k^2=\frac59.                                   \tag{17}
\]

#### Proof

The uniform vector \(u=(1/3,1/3,1/3)\) has zero expectation and
\(\|u\|_2^2=1/3\).  The intersection
\[
\left\{w\ge0:\sum_kw_k=1,\ \sum_kw_k\lambda_k=0\right\}
\]
is a line segment through \(u\), unless every \(\lambda_k=0\), in
which case the conclusion is immediate.

After changing the common sign and permuting coordinates, write
\[
(\lambda_0,\lambda_1,\lambda_2)=(a,b,-a-b),
\qquad a,b\ge0.
\]
If \(a\ge b\), the endpoint on the edge \(w_0=0\) is
\[
w^*=\left(0,\frac{a+b}{a+2b},\frac{b}{a+2b}\right),
\]
and
\[
\|w^*\|_2^2-\frac59
=\frac{2(a-b)(2a+b)}{9(a+2b)^2}\ge0.                  \tag{18}
\]
If \(b\ge a\), the symmetric endpoint on \(w_1=0\) obeys the same
bound.  On the segment from \(u\) to this endpoint, squared norm is
continuous and increases from \(1/3\) to at least \(5/9\).  It
therefore assumes the value \(5/9\), proving (17). \(\square\)

### Lemma 3.2 (three-extremal-direction lemma)

For every unit \(n\in V\), there are three Hilbert--Schmidt
orthonormal matrices
\[
E_0,E_1,E_2\in n^\perp
\]
such that
\[
r(E_j)^2=\frac23\qquad(j=0,1,2).                       \tag{19}
\]

#### Proof

Conjugate \(n\) unitarily to
\[
n=\operatorname{diag}(\lambda_0,\lambda_1,\lambda_2).
\]
Choose \(w\) from Lemma 3.1 and let
\[
\omega=e^{2\pi i/3},\qquad
|z_j\rangle
=\sum_{k=0}^2\sqrt{w_k}\,\omega^{jk}|k\rangle
\quad(j=0,1,2).                                       \tag{20}
\]
Every \(z_j\) is a unit vector and
\[
\langle z_j,nz_j\rangle=\sum_kw_k\lambda_k=0.
\]
Therefore \(E_j:=E_{z_j}\) lies in \(n^\perp\).

For \(j\ne\ell\),
\[
|\langle z_j,z_\ell\rangle|^2
=\left|\sum_kw_k\omega^{(\ell-j)k}\right|^2
=\frac{3\sum_kw_k^2-1}{2}
=\frac13.                                             \tag{21}
\]
Equations (15)--(16) now give (19) and
\(\langle E_j,E_\ell\rangle=0\).  Undoing the unitary conjugation
finishes the proof. \(\square\)

### Corollary 3.3 (adapted spectral-radius sum)

The orthonormal triple from Lemma 3.2 can be completed to an
orthonormal basis \(F_2,\ldots,F_8\) of \(n^\perp\).  Equations
(12), (19) give
\[
\boxed{
\sum_{a=2}^8r(F_a)^2
\ge3\left(\frac23\right)+4\left(\frac12\right)=4.}     \tag{22}
\]

## 4. The improved one-site and global bounds

For \(\sigma\ne0\), choose the completion in Corollary 3.3.  Equations
(11), (22) give
\[
\boxed{\sum_{a=1}^8r(B_a)^2\ge4+p.}                   \tag{23}
\]
If \(\rho=I/3\), choose any unit \(F_1=n\), followed by the same
completion.  Then \(B_a=F_a\) for every \(a\), and
\[
\sum_ar(B_a)^2\ge\frac12+4>\frac{13}{3}=4+p,
\]
so (23) holds in this case too.

Sum (4) over this basis.  Using (5), (7), and (23),
\[
\begin{aligned}
\operatorname{Tr}_{HS}{\cal G}
&\le fp+\frac23(3-p)
 -(f-\tfrac23)(4+p)\\
&=\boxed{\frac{14}{3}-4f.}
\end{aligned}                                         \tag{24}
\]
All dependence on the one-site purity cancels exactly.

The established common-origin identity for the three left sites is
\[
\sum_{i=1}^3\operatorname{Tr}_{HS}{\cal G}_i^L
=\frac{16}{3}w_1+\frac{17}{3}f+w_3.                  \tag{25}
\]
Summing (24) over the three sites and comparing with (25) gives
\[
\frac{16}{3}w_1+\frac{17}{3}f+w_3
\le14-12f.                                             \tag{26}
\]
Multiplication by three and collection of terms gives exactly
\[
16w_1+53f+3w_3\le42,
\]
which is (1).  Since \(w_1,w_3\ge0\), (2) follows.  The right-site
identities give the same scalar inequality.

## 5. Exact audit of the elementary constants

The elementary bound (13) can be attained by one particular adapted
basis, even though Corollary 3.3 gives a better prover-chosen
completion.  Take
\[
\rho_*=\operatorname{diag}\left(\frac12,\frac14,\frac14\right),
\qquad p_*=\frac38,
\]
and
\[
F_1=\frac1{\sqrt6}\operatorname{diag}(2,-1,-1),\qquad
F_2=\frac1{\sqrt2}\operatorname{diag}(0,1,-1),
\]
together with the six normalized Hermitian off-diagonal matrix
units.  Then
\[
r(B_1)^2=p_*=\frac38,\qquad
r(B_a)^2=\frac12\quad(a=2,\ldots,8),
\]
so
\[
\sum_ar(B_a)^2=\frac{31}{8}=\frac72+p_*.
\]
This confirms the constants in the proposed \(78/97\) derivation,
but it does **not** show that a prover-optimized completion is unable
to do better.  The three-extremal-direction lemma supplies such a
completion for every \(n\).

## 6. What is and is not resolved

The exact critical ceiling is reduced along this route as follows:
\[
1
\quad\longrightarrow\quad
\frac{78}{97}=0.804123\ldots
\quad\longrightarrow\quad
\frac{51}{64}=0.796875
\quad\longrightarrow\quad
\frac{42}{53}=0.792452\ldots.
\]
The last arrow is the theorem of this note.  It does not exclude the
interval \(2/3<f\le42/53\).

At the most degenerate normal direction the construction reduces to
a trine in a complex two-dimensional support.  No claim is made that
the total spectral-radius sum \(4\) in (22) is the best possible
adapted-frame constant.

There is, however, an exact obstruction to finishing the theorem by
optimizing only this scalar frame sum.  Define
\[
K(n)=\sup_{\substack{F_2,\ldots,F_8\ {\rm ON}\\F_a\in n^\perp}}
\sum_{a=2}^8r(F_a)^2,
\qquad
K_*=\inf_{\|n\|_2=1}K(n).                              \tag{27}
\]
Corollary 3.3 proves \(K_*\ge4\).  If a stronger universal constant
\(K\le K_*\) were known, the calculation in Section 4 would give
\[
\operatorname{Tr}_{HS}{\cal G}
\le2+\frac23K-Kf                                      \tag{28}
\]
and therefore
\[
\boxed{
16w_1+(17+9K)f+3w_3\le18+6K.}                        \tag{29}
\]
After dropping \(w_1,w_3\), its scalar ceiling is
\[
B(K)=\frac{18+6K}{17+9K}.                              \tag{30}
\]
For every finite \(K\),
\[
B(K)-\frac23
=\frac{20}{3(17+9K)}>0.                               \tag{31}
\]
In fact every unit traceless Hermitian qutrit has
\(r(F)^2\le2/3\), so
\[
K_*\le7\left(\frac23\right)=\frac{14}{3}.             \tag{32}
\]
The function \(B(K)\) is decreasing.  Thus even granting the
impossible ideal that all seven frame vectors are extremal gives only
\[
\boxed{f\le B(14/3)=\frac{46}{59}>\frac23.}           \tag{33}
\]
Consequently no improvement of the **scalar, separately summed**
adapted-frame spectral-radius constant can prove the desired
\(f\le2/3\).  A successful continuation must retain matrix-valued or
cross-site information discarded by the trace.

Further progress must therefore use at least one of:

* correlations among the three site frames induced by the same
  rank-two \(C\), before taking their traces;
* simultaneous left/right density information;
* positive \(w_1\) or \(w_3\) forced by full-support rank-two
  realizability.
