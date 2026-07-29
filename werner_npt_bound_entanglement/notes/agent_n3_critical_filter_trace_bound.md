# A cubic-basis trace bound for full-support pair-sector critical points

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
\boxed{352w_1+1121f+66w_3\le894,}                     \tag{1}
\]
and consequently
\[
\boxed{f\le\frac{894}{1121}=0.797502\ldots.}           \tag{2}
\]

The elementary adapted-basis argument proposed in the research log is
correct and gives \(f\le78/97\).  It is not optimal, however.  The
traceless-Hermitian cubic
\[
q(F)=\operatorname{Tr}(F^3)
\]
shows that one can choose the seven undistinguished basis vectors with
a strictly larger total spectral-radius square.  The exact extra gain
is \(3/11\) in the local spectral-radius sum, which yields (1).

This remains short of the required \(f\le2/3\), so it does not close
the unrestricted three-copy theorem.  It is an exact nonlinear
restriction on every hypothetical full-support critical violator.

The independent symbolic checker is
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

## 2. The elementary adapted-basis identities

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
Every \(F\in n^\perp\) is traceless Hermitian of Hilbert--Schmidt norm
one, and hence \(r(F)^2\ge1/2\).  This proves the elementary bound
\[
\sum_ar(B_a)^2\ge\frac72+p.                            \tag{12}
\]
Equations (7), (12), (4), and (5) indeed give
\[
\operatorname{Tr}_{HS}{\cal G}
\le\frac{13}{3}-\frac72f,                              \tag{13}
\]
and hence \(32w_1+97f+6w_3\le78\).  Thus the proposed \(78/97\)
calculation and all of its constants are correct.

The next sections improve the freely chosen orthonormal completion of
\(n\).

## 3. Spectral radius and the qutrit cubic

### Lemma 3.1

If \(F\in V\), \(\|F\|_2=1\), and \(q(F)=\operatorname{Tr}(F^3)\),
then
\[
\boxed{
r(F)^2\ge\frac12+\frac{|q(F)|}{\sqrt6}.}               \tag{14}
\]
Also
\[
|q(F)|\le\frac1{\sqrt6}.                               \tag{15}
\]

#### Proof

After possibly replacing \(F\) by \(-F\), let \(r\ge0\) be an
eigenvalue of maximal modulus.  If the other eigenvalues are \(x,y\),
then
\[
x+y=-r,\qquad x^2+y^2=1-r^2.
\]
It follows that \(xy=r^2-\tfrac12\), and Newton's identities give
\[
|q(F)|=3|\det F|=3r\left(r^2-\frac12\right).           \tag{16}
\]
The norm and trace constraints imply
\[
\frac12\le r^2\le\frac23.
\]
Since \(3r/\sqrt6\le1\), equation (16) proves (14).  The maximum in
(16) over this interval occurs at \(r^2=2/3\) and equals
\(1/\sqrt6\), proving (15). \(\square\)

An immediate consequence of (15) is
\[
\boxed{\frac{|q(F)|}{\sqrt6}\ge q(F)^2.}               \tag{17}
\]

## 4. Cubic mass in an adapted seven-frame

Let
\[
T(A,B,C)=\frac16\sum_{\pi\in S_3}
\operatorname{Tr}(A_{\pi(1)}A_{\pi(2)}A_{\pi(3)})
=\frac12\operatorname{Tr}\bigl(A(BC+CB)\bigr)          \tag{18}
\]
be the real symmetric polarization of \(q\) on \(V\).  Thus
\(T(F,F,F)=q(F)\).

Fix a unit \(n\in V\), put \(W=n^\perp\), and let \(T_W\) be the
restriction of \(T\) to \(W^3\).  Its trace vector is the vector
\(t_W\in W\) defined by
\[
\langle t_W,x\rangle
=\sum_{a=2}^8T(x,F_a,F_a)                              \tag{19}
\]
for any orthonormal basis \(F_2,\ldots,F_8\) of \(W\).

### Lemma 4.1

Writing \(q_n=q(n)\), the following invariant identities hold:
\[
\boxed{
\|T_W\|^2=\frac{14}{3}-q_n^2,\qquad
\|t_W\|^2=\frac16-q_n^2.}                              \tag{20}
\]

#### Proof

For a Hilbert--Schmidt orthonormal basis of \(V\), the standard
traceless-matrix completeness relation is
\[
\sum_{a=1}^8(F_a)_{ij}(F_a)_{kl}
=\delta_{il}\delta_{jk}-\frac13\delta_{ij}\delta_{kl}. \tag{21}
\]
Direct contraction of (18) with (21) gives
\[
\|T\|^2=\frac{20}{3},\qquad
\sum_aT(x,F_a,F_a)=0,\qquad
\|T(n,\cdot,\cdot)\|^2=\frac56.                        \tag{22}
\]
For completeness, set
\[
v=n^2-\frac13I.
\]
The qutrit trace identities
\[
\operatorname{Tr}(n^4)=\frac12,\qquad
\langle v,n\rangle=q_n
\]
give
\[
\|v\|^2=\frac16,\qquad
\|v-q_nn\|^2=\frac16-q_n^2.                            \tag{23}
\]
The vector \(v-q_nn\) represents \(T(n,n,\cdot)\) on \(W\).
Decomposing the last norm in (22) into its \(n\)-\(n\),
\(n\)-\(W\), and \(W\)-\(W\) blocks yields
\[
\|T(n,\cdot,\cdot)|_{W\times W}\|^2
=\frac12+q_n^2.                                        \tag{24}
\]
Finally decompose the full symmetric tensor according to the number
of \(n\)-indices:
\[
\begin{aligned}
\frac{20}{3}
={}&q_n^2
+3\left(\frac16-q_n^2\right)
+3\left(\frac12+q_n^2\right)
+\|T_W\|^2.
\end{aligned}
\]
This gives the first identity in (20).  The middle identity in (22)
implies
\[
t_W=-(v-q_nn),
\]
which, with (23), gives the second. \(\square\)

### Lemma 4.2

There is an orthonormal basis \(F_2,\ldots,F_8\) of \(W\) such that
\[
\boxed{\sum_{a=2}^8q(F_a)^2\ge\frac3{11}.}             \tag{25}
\]

#### Proof

For a uniform random vector \(U\) on the unit sphere in a real
\(m\)-dimensional space and a symmetric cubic tensor \(S\), the exact
sixth spherical moment is
\[
\mathbb E\,S(U,U,U)^2
=\frac{6\|S\|^2+9\|\operatorname{tr}S\|^2}
       {m(m+2)(m+4)}.                                  \tag{26}
\]
This follows by pairing the six coordinates in the rotationally
invariant sixth-moment tensor: six pairings contract all three
indices across the two copies of \(S\), and nine produce the squared
trace vector.

Take a Haar-random orthonormal basis of the seven-dimensional space
\(W\).  Each basis vector is uniform on its unit sphere.  Lemma 4.1
and (26) therefore give
\[
\begin{aligned}
\mathbb E\sum_{a=2}^8q(F_a)^2
&=\frac{6\|T_W\|^2+9\|t_W\|^2}{9\cdot11}\\
&=\frac{\frac{59}{2}-15q_n^2}{99}\\
&\ge\frac3{11},
\end{aligned}                                         \tag{27}
\]
where the last inequality uses \(q_n^2\le1/6\), from (15).
At least one orthonormal basis attains at least its expectation,
proving (25). \(\square\)

Combining Lemma 3.1, (17), and Lemma 4.2, this completion satisfies
\[
\boxed{
\sum_{a=2}^8r(F_a)^2
\ge\frac72+\frac3{11}.}                               \tag{28}
\]

## 5. The improved one-site and global bounds

For \(\sigma\ne0\), choose the completion in Lemma 4.2.  Equations
(11) and (28) give
\[
\boxed{
\sum_{a=1}^8r(B_a)^2
\ge\frac72+p+\frac3{11}.}                             \tag{29}
\]
If \(\rho=I/3\), choose any unit \(F_1=n\) and then the completion of
Lemma 4.2.  In that case \(B_a=F_a\) for every \(a\), and the extra
bound \(r(F_1)^2\ge1/2>p=1/3\) proves (29) as well.

Sum (4) over this basis.  Using (5), (7), and (29),
\[
\begin{aligned}
\operatorname{Tr}_{HS}{\cal G}
&\le fp+\frac23(3-p)
 -(f-\tfrac23)\left(\frac72+p+\frac3{11}\right)\\
&=\boxed{
\frac{13}{3}-\frac72f-\frac3{11}
\left(f-\frac23\right).}
\end{aligned}                                         \tag{30}
\]
All dependence on the one-site purity again cancels.

The established common-origin identity for the three left sites is
\[
\sum_{i=1}^3\operatorname{Tr}_{HS}{\cal G}_i^L
=\frac{16}{3}w_1+\frac{17}{3}f+w_3.                  \tag{31}
\]
Summing (30) and comparing with (31) gives
\[
\frac{16}{3}w_1+\frac{17}{3}f+w_3
\le13-\frac{21}{2}f-\frac9{11}\left(f-\frac23\right).
\tag{32}
\]
Multiplication by \(66\) and collection of terms gives exactly
\[
352w_1+1121f+66w_3\le894,
\]
which is (1).  Since \(w_1,w_3\ge0\), (2) follows.  The right-site
identities give the same scalar inequality.

## 6. Exact audit of the elementary constants

The elementary bound (12) can be attained by one particular adapted
basis, even though another completion has the cubic improvement
(28).  Take
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
to do better.  Lemma 4.2 is precisely the missing optimization.

## 7. Remaining gap

The cubic frame average lowers the critical ceiling from
\[
\frac{78}{97}=0.804123\ldots
\quad\text{to}\quad
\frac{894}{1121}=0.797502\ldots,
\]
but still does not exclude \(f>2/3\).

Possible continuations of this route are now sharply separated:

* determine the exact minimum, over \(n\in V\), of the maximum cubic
  mass \(\sum q(F_a)^2\) over orthonormal bases of \(n^\perp\);
* replace the two relaxations in (14), (17) by the exact nonlinear
  relation (16);
* retain correlations among the three site frames, or between the
  left and right site frames, induced by the common rank-two \(C\);
* prove that full-support rank-two realizability forces positive
  \(w_1\) or \(w_3\) in (1).

No claim is made here that \(3/11\) is the optimal cubic-frame
constant.
