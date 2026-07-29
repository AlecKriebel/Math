# A completely positive certificate for the qubit anchored map

## Status

This note proves a stronger version of the anchored Gram inequality when
every physical coefficient space is a qubit.  In fact the result holds
for every copy number, not only for three copies.

The proof also identifies the exact obstruction to extending this
certificate to higher local dimension: the Choi matrix used below is an
orthogonal projection only in dimension two and acquires a negative
identity direction in dimension at least three.  Thus this is a useful
certificate for the qubit boundary, but it is not a proof of the
unrestricted three-copy problem.

## 1. The two complementary local maps

On \(M_2\), define
\[
 L(X)=X-\frac12\operatorname{Tr}(X)I,
 \qquad
 M(X)=\operatorname{Tr}(X)I-\frac12X.
 \tag{1}
\]
For \(n\) qubit factors put
\[
 {\cal L}_n=L^{\otimes n},\qquad
 {\cal K}_n=M^{\otimes n}.
 \tag{2}
\]
The map \({\cal K}_3\) is exactly the map appearing in the anchored
formulation:
\[
 {\cal K}_3(V)=
 \sum_{S\subseteq[3]}
 \left(-\frac12\right)^{|S|}
 \operatorname{Tr}_{\bar S}(V)\otimes I_{\bar S}.
 \tag{3}
\]

Use column vectorization and the unnormalized maximally entangled vector
\[
 |\Phi_2\rangle=|00\rangle+|11\rangle.
 \tag{4}
\]
The Choi matrix of \(M\) is
\[
 J(M)=I_4-\frac12|\Phi_2\rangle\langle\Phi_2|
 =:\pi.
 \tag{5}
\]
Since \(\|\Phi_2\|^2=2\), \(\pi\) is the orthogonal projection onto the
three-dimensional subspace orthogonal to \(\Phi_2\).

The same projection represents \(L\) on Hilbert--Schmidt space:
\[
 \operatorname{vec}(L(X))=\pi\,\operatorname{vec}(X).
 \tag{6}
\]
Consequently, up to the harmless regrouping of tensor factors,
\[
 J({\cal K}_n)=\Pi_n:=\pi^{\otimes n},
 \qquad
 \operatorname{vec}({\cal L}_n(X))
 =\Pi_n\operatorname{vec}(X).
 \tag{7}
\]
In particular, \(\Pi_n\) is an orthogonal projection.

## 2. Complete positivity of the anchored map

### Theorem 2.1

Let \(w\in(\mathbb C^2)^{\otimes n}\), not necessarily normalized, and
write
\[
 P_w=|w\rangle\langle w|,\qquad
 A_w={\cal L}_n(P_w),\qquad
 a=\langle P_w,{\cal L}_n(P_w)\rangle_{\rm HS}.
 \tag{8}
\]
Then the map
\[
 \Theta_w(V)=a{\cal K}_n(V)-A_wVA_w
 \tag{9}
\]
is completely positive.

Hence, for all \(u,v\in(\mathbb C^2)^{\otimes n}\),
\[
 \left|
 {\cal B}_n(P_w,|u\rangle\langle v|)
 \right|^2
 \leq
 Q_n(P_w)Q_n(|u\rangle\langle v|).
 \tag{10}
\]

### Proof

Set
\[
 x=\operatorname{vec}(A_w).
 \tag{11}
\]
Equations (7) and (8), together with
\(\Pi_n=\Pi_n^\dagger=\Pi_n^2\), give
\[
 x=\Pi_n\operatorname{vec}(P_w),\qquad
 \Pi_nx=x,\qquad
 \|x\|^2
 =\langle\operatorname{vec}(P_w),
       \Pi_n\operatorname{vec}(P_w)\rangle
 =a.
 \tag{12}
\]
The map \(V\mapsto A_wVA_w\) has the single Kraus operator \(A_w\);
therefore its Choi matrix is \(|x\rangle\langle x|\).  Equations
(7) and (12) now yield
\[
 J(\Theta_w)=a\Pi_n-|x\rangle\langle x|
 =a\left(\Pi_n-\frac{|x\rangle\langle x|}{\|x\|^2}\right)
 \succeq0
 \tag{13}
\]
when \(x\ne0\).  The operator in parentheses is the orthogonal
projection onto
\(\operatorname{ran}\Pi_n\cap x^\perp\).  If \(x=0\), then \(a=0\)
and (13) is the zero operator.  Thus \(\Theta_w\) is completely
positive in every case.

For \(V=P_v\), complete positivity gives
\[
 aK_v-A_wP_vA_w=\Theta_w(P_v)\succeq0.
 \tag{14}
\]
Taking its expectation in \(u\), and using the exact identities
\[
 \langle u,K_vu\rangle=Q_n(|u\rangle\langle v|),
 \qquad
 \langle v,A_wu\rangle
 ={\cal B}_n(P_w,|u\rangle\langle v|),
 \tag{15}
\]
proves (10).
\(\square\)

## 3. Equality and the GHZ stress test

The Choi certificate is sharp.  Its kernel contains both
\(\ker\Pi_n\) and the one-dimensional direction \(x\).  Thus it does
not introduce a fictitious strict gap.

For the three-qubit vectors
\[
 w_\pm=\frac{|000\rangle\pm|111\rangle}{\sqrt2},
 \tag{16}
\]
one has
\[
 Q_3(P_{w_+})=Q_3(P_{w_-})=\frac12,
 \qquad
 A_{w_+}w_-=-\frac12w_-.
 \tag{17}
\]
Taking \(u=v=w_-\) in (10) gives equality:
\[
 |\langle w_-,A_{w_+}w_-\rangle|^2
 =\frac14
 =Q_3(P_{w_+})Q_3(P_{w_-}).
 \tag{18}
\]
This is the boundary example that invalidates the state-independent
operator-norm replacement of \(K_v\).  The complete-positive
certificate retains \(K_v\) and therefore captures the equality
exactly.

## 4. Why this certificate stops at local dimension two

For local dimension \(d\), the same calculation gives
\[
 J(M_d)=I_{d^2}-\frac12|\Phi_d\rangle\langle\Phi_d|.
 \tag{19}
\]
Its eigenvalue along \(\Phi_d\) is
\[
 1-\frac d2.
 \tag{20}
\]
It is a projection for \(d=2\), is singular with a negative direction
for every \(d>2\), and hence is not a Choi matrix of a completely
positive map in the first unresolved dimension \(d=3\).

The algebraic identity
\[
 \operatorname{vec}({\cal L}_n(P_w))
 =J({\cal K}_n)\operatorname{vec}(P_w)
 \tag{21}
\]
continues to hold, but (13) becomes a rank-one subtraction from an
indefinite metric.  Proving block positivity on the decomposable Choi
vectors \(\overline v\otimes u\), rather than positivity on the whole
Choi space, is exactly the remaining higher-dimensional anchored
problem.

## 5. An arbitrary-dimensional crossing identity

Although complete positivity stops at qubits, there is an exact identity
in every finite local dimension that explains why the diagonal case
\(v=w\) of the anchored inequality is easy.

For arbitrary \(x,y\in{\cal H}\), define the polarized operators
\[
 A_{x,y}={\cal L}_n(|x\rangle\langle y|),\qquad
 K_{x,y}={\cal K}_n(|x\rangle\langle y|).
 \tag{22}
\]
Then, for all \(x,y,z,t\in{\cal H}\),
\[
 \boxed{\qquad
 \langle t,A_{x,y}z\rangle
 =\langle y,K_{x,t}z\rangle .
 \qquad}
 \tag{23}
\]

To prove (23), fix \(S\subseteq[n]\).  In product bases, both sides of
\[
 \left\langle t,
   \bigl(\operatorname{Tr}_S|x\rangle\langle y|\otimes I_S\bigr)z
 \right\rangle
 =
 \left\langle y,
   \bigl(\operatorname{Tr}_{\bar S}|x\rangle\langle t|
          \otimes I_{\bar S}\bigr)z
 \right\rangle
 \tag{24}
\]
are the same complete contraction of the four tensors
\(\overline t,x,\overline y,z\).  Multiplying (24) by
\((-1/2)^{|S|}\) and summing over \(S\) gives (23).

Taking \(x=y=z=w\) in (23) gives the vector identity
\[
 \boxed{\qquad A_ww=K_ww. \qquad}
 \tag{25}
\]
It can also be seen term by term from a Schmidt decomposition of \(w\)
across \(S:\bar S\): the two complementary reduced density operators,
inserted on their respective sides of the cut, have the same action on
\(w\).

Since \(K_w\succeq0\), equations (23)--(25) prove the diagonal anchored
inequality in arbitrary dimensions:
\[
\begin{aligned}
 |\langle w,A_wu\rangle|^2
 &=|\langle A_ww,u\rangle|^2\\
 &=|\langle K_ww,u\rangle|^2\\
 &\leq
 \langle w,K_ww\rangle\langle u,K_wu\rangle\\
 &=Q_n(P_w)Q_n(|u\rangle\langle w|).
\end{aligned}
 \tag{26}
\]

There is also a useful exterior-algebra form of the failure of \(A\)
and \(K\) to agree away from the diagonal.  Put
\[
 D_{x,y}=A_{x,y}-K_{x,y}.
 \tag{27}
\]
The trilinear map \(D_{x,y}z\) is alternating in its two holomorphic
arguments:
\[
 \boxed{\qquad D_{x,y}z=-D_{z,y}x. \qquad}
 \tag{28}
\]
Indeed, (25) says \(D_{w,w}w=0\).  Polarizing this identity and taking
the coefficient of the monomial
\(\alpha\overline\beta\gamma\) in
\(w=\alpha x+\beta y+\gamma z\) gives (28).  Since
\[
 D_{x,y}^\dagger=D_{y,x},
 \tag{29}
\]
the associated four-linear form
\[
 d(x,y,z,t)=\langle t,D_{x,y}z\rangle
 \tag{30}
\]
is alternating in both pairs:
\[
 d(x,y,z,t)=-d(z,y,x,t)=-d(x,t,z,y).
 \tag{31}
\]
Thus \(d\) descends to a Hermitian form on
\(\bigwedge^2{\cal H}\).  In particular, the genuinely
higher-dimensional correction to the diagonal proof is supported on
the two exterior vectors
\[
 w\wedge u,\qquad w\wedge v.
 \tag{32}
\]
This isolates the remaining obstruction without discarding the common
anchor.  Positivity of \(K_w\) proves (26); the unrestricted anchored
problem requires controlling the additional exterior pairing in (31)
when \(v\ne w\).

## 6. Exact even/odd completely-copositive splitting

The exterior correction has a state-independent channel
factorization.  Let
\[
 {\cal E}_n={\cal K}_n-{\cal L}_n.
 \tag{33}
\]
For arbitrary local dimensions, the local Choi matrices are
\[
\begin{aligned}
 J(L_i)&=|\Phi_{d_i}\rangle\langle\Phi_{d_i}|-\frac12I,\\
 J(M_i)&=I-\frac12|\Phi_{d_i}\rangle\langle\Phi_{d_i}|.
\end{aligned}
 \tag{34}
\]
After partial transpose on the Choi input spaces,
\[
\begin{aligned}
 J({\cal L}_n)^\Gamma
 &=\bigotimes_i\left(F_i-\frac12I\right),\\
 J({\cal K}_n)^\Gamma
 &=\bigotimes_i\left(I-\frac12F_i\right).
\end{aligned}
 \tag{35}
\]
Let \(\Pi_T\) project onto the sector that is locally antisymmetric
exactly at the sites in \(T\).  On this sector the two operators in
(35) have eigenvalues
\[
 2^{-n}(-3)^{|T|},\qquad 2^{-n}3^{|T|},
 \tag{36}
\]
respectively.  Therefore
\[
 \boxed{\qquad
 J({\cal E}_n)^\Gamma
 =2^{1-n}\sum_{\substack{T\subseteq[n]\\|T|\ {\rm odd}}}
 3^{|T|}\Pi_T\succeq0.
 \qquad}
 \tag{37}
\]
Thus \({\cal E}_n\) is completely copositive.  More symmetrically,
\[
 {\cal K}_{n,+}=\frac{{\cal K}_n+{\cal L}_n}{2},\qquad
 {\cal K}_{n,-}=\frac{{\cal K}_n-{\cal L}_n}{2}
 \tag{38}
\]
are completely copositive maps supported on even and odd local
antisymmetry parity, respectively, and
\[
 {\cal K}_n={\cal K}_{n,+}+{\cal K}_{n,-},\qquad
 {\cal L}_n={\cal K}_{n,+}-{\cal K}_{n,-}.
 \tag{39}
\]

The Choi eigenvectors in the odd sectors vectorize globally
skew-symmetric Kraus matrices.  Hence \({\cal E}_n\) has a
copositive Kraus representation
\[
 {\cal E}_n(X)=\sum_\mu R_\mu X^T R_\mu^\dagger,
 \qquad R_\mu^T=-R_\mu.
 \tag{40}
\]
For every \(w\),
\[
 \langle w,R_\mu\overline w\rangle=0,
 \tag{41}
\]
so positivity of every summand gives
\[
 {\cal E}_n(P_w)w=0.
 \tag{42}
\]
Equation (42) is the Kraus/exterior explanation of (25).

For \(n=3\), (37) has coefficient \(3/4\) on each sector with one
locally antisymmetric site and coefficient \(27/4\) on the
all-three-antisymmetric sector.  Any sum-of-squares proof of the
general anchored inequality can therefore be sought as a recoupling
inequality between the even and odd copositive Kraus families in
(38), with the common-anchor annihilation (41) imposed exactly.
