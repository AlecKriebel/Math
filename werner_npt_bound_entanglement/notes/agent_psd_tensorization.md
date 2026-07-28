# Strong PSD tensorization: exact sparse families and obstructions

## Research log

### 2026-07-28 11:36 PDT — checkpoint 1

This note investigates the stronger endpoint conjecture
\[
Q_n(H)\geq 2^{-n}\left(2\operatorname{Tr}H^2-(\operatorname{Tr}H)^2\right)
\tag{1}
\]
for \(H\succeq0\), \(\operatorname{rank}H\leq2\), where
\[
\mathcal L(Z)=Z-\frac12\operatorname{Tr}(Z)I,\qquad
\mathcal B_n(A,B)=\langle A,\mathcal L^{\otimes n}(B)\rangle_{\rm HS},
\qquad Q_n(A)=\mathcal B_n(A,A).
\tag{2}
\]

The main exact findings are:

1. A natural mixed-subprojection induction inequality is false, with a
   small rational certificate at \(n=3\).
2. The same certificate belongs to a non-product two-parameter parity
   family for which (1) can be proved for **every \(n\geq3\)**.  For odd
   \(n\) the defect is an explicit sum of two squares.  For even \(n\) an
   exact copositivity argument proves the result.
3. At \(n=3\), (1) holds whenever all three local supports have dimension
   at most two.  The proof is a nine-observable anticommutation argument.
4. Averaging that qubit proof over two-dimensional compressions of qutrits
   loses the exact factor \(3\) to \(2\), so it does not prove the qutrit
   statement.

No proof of (1) for arbitrary qutrit-supported rank-two \(H\), and no
counterexample to it, is obtained.  Best-guess completion toward this
restricted conjecture: **45%**.  The all-\(n\) sparse-family theorem below
is complete.

## 1. The exact two-by-two condition

Put \(r_n=2^{-n}\).  Let
\[
H=\lambda A+\mu B,\qquad
A=|u\rangle\langle u|,\quad B=|v\rangle\langle v|,
\tag{3}
\]
where \(u,v\) are orthonormal and \(\lambda,\mu\geq0\).  Write
\[
a=Q_n(A),\qquad b=Q_n(B),\qquad c=\mathcal B_n(A,B).
\]
Since
\[
\operatorname{Tr}H^2=\lambda^2+\mu^2,\qquad
(\operatorname{Tr}H)^2=(\lambda+\mu)^2,
\]
the strong defect is exactly
\[
\boxed{\quad
\Delta_n(H):=
Q_n(H)-r_n\left(2\operatorname{Tr}H^2-(\operatorname{Tr}H)^2\right)
=\lambda^2(a-r_n)+\mu^2(b-r_n)+2\lambda\mu(c+r_n).
\quad}
\tag{4}
\]
Thus the conjecture is precisely copositivity of
\[
M(u,v)=
\begin{pmatrix}
a-r_n&c+r_n\\
c+r_n&b-r_n
\end{pmatrix}.
\tag{5}
\]
The rank-one endpoint inequality gives nonnegative diagonal entries.  The
only remaining issue is
\[
c+r_n\geq-\sqrt{(a-r_n)(b-r_n)}.
\tag{6}
\]

In the two-replica notation, with local swaps \(F_i\),
\[
2^n\Delta_n(H)=\operatorname{Tr}[(H\otimes H)W_n],
\qquad
W_n=\prod_{i=1}^n(2F_i-I)+I-2F_{[n]}.
\tag{7}
\]
For \(n=3\),
\[
W_3=8\left(\sum_{|R|=2}\Pi_R-3\Pi_{\{1,2,3\}}\right),
\tag{8}
\]
where \(\Pi_R\) is antisymmetric at the replica pairs in \(R\) and
symmetric at the other pairs.  It is important that the cross term in
(4) can be negative.  Consequently, the termwise proposal
\[
\sum_{|R|=2}\|\Pi_R(u\otimes v)\|^2
\stackrel{?}{\geq}
3\|\Pi_{\{1,2,3\}}(u\otimes v)\|^2
\tag{9}
\]
is false; Section 2 gives an exact rational example.  The diagonal terms
in (4) are indispensable.

## 2. Exact failure of mixed-subprojection positivity

On three qubit-supported copies, define
\[
\begin{aligned}
u&=\frac{1}{\sqrt{28}}\left(
5|111\rangle+|001\rangle+|010\rangle+|100\rangle\right),\\
v&=\frac{1}{\sqrt{21}}\left(
3|000\rangle+2|011\rangle+2|101\rangle+2|110\rangle\right).
\end{aligned}
\tag{10}
\]
The supports have opposite parity, so \(u,v\) are orthonormal.  Set
\(A=|u\rangle\langle u|\), \(B=|v\rangle\langle v|\), and \(P=A+B\).
Direct exact contraction gives
\[
Q_3(A)=\frac{11}{49},\qquad
Q_3(B)=\frac{563}{1176},\qquad
\mathcal B_3(A,B)=-\frac{117}{392}.
\tag{11}
\]
In particular,
\[
\boxed{\quad
\mathcal B_3(P,A)
=Q_3(A)+\mathcal B_3(A,B)
=-\frac{29}{392}<0.
\quad}
\tag{12}
\]
This disproves the tempting induction invariant
\(\mathcal B_n(P,A)\geq0\) for a rank-two projection \(P\) and a rank-one
subprojection \(A\leq P\).

It also disproves (9), because
\[
\langle u\otimes v|W_3|u\otimes v\rangle
=8\left(\mathcal B_3(A,B)+\frac18\right)
=-\frac{68}{49}<0.
\tag{13}
\]
Nevertheless, the complete strong matrix is positive definite:
\[
M(u,v)=
\begin{pmatrix}
\frac{39}{392}&-\frac{17}{98}\\[2mm]
-\frac{17}{98}&\frac{52}{147}
\end{pmatrix},
\qquad
\det M(u,v)=\frac1{196}>0.
\tag{14}
\]
Also
\[
Q_3(P)=\frac{125}{1176}>0.
\tag{15}
\]
Thus (10) isolates the obstruction cleanly: a single mixed term and even a
mixed subprojection derivative can be negative, while the exact spectral
Cauchy bound (6) still holds.

## 3. An all-copy non-product parity family

The example above is one member of an exactly solvable family.  It is
useful because it tests (1) at every copy number without imposing product
eigenvectors.

For \(n\geq3\), let \({\bf1}=11\cdots1\), let \(e_i\) be the binary string
with its only \(1\) in position \(i\), and put
\(\bar e_i={\bf1}-e_i\).  For \(p,q\geq0\), define
\[
\begin{aligned}
u_p&=\frac{|{\bf1}\rangle+p\sum_{i=1}^n|e_i\rangle}
{\sqrt{1+np^2}},\\
v_q&=\frac{|{\bf0}\rangle+q\sum_{i=1}^n|\bar e_i\rangle}
{\sqrt{1+nq^2}}.
\end{aligned}
\tag{16}
\]
Their supports are disjoint, hence \(u_p\perp v_q\).  Except at degenerate
parameter values, neither vector is a product vector.

Define
\[
r=2^{-n},\qquad
\kappa=\frac{n(n-1)}{2^{n-2}},\qquad
\beta=n\left(1-2^{2-n}\right),\qquad
\eta=\kappa+\frac{n^2}{2^{n-1}},
\tag{17}
\]
and \(d_p=1+np^2,\ d_q=1+nq^2\).

### Theorem 1

For every \(n\geq3\), \(p,q\geq0\), and \(\lambda,\mu\geq0\), the operator
\[
H=\lambda|u_p\rangle\langle u_p|
+\mu|v_q\rangle\langle v_q|
\tag{18}
\]
satisfies the strong inequality (1).

If \(n\) is odd, the defect is the explicit sum of squares
\[
\boxed{\quad
\Delta_n(H)
=\kappa(pX-qY)^2+n(X-Y)^2,
\qquad
X=\frac{\lambda p}{d_p},\quad
Y=\frac{\mu q}{d_q}.
\quad}
\tag{19}
\]

#### Proof: exact contractions

For one-site matrix units \(E_{ab}=|a\rangle\langle b|\),
\[
\mathcal B_1(E_{ab},E_{cd})
=\delta_{ac}\delta_{bd}-\frac12\delta_{ab}\delta_{cd}.
\tag{20}
\]
Hence an off-diagonal matrix unit pairs only with an identical
off-diagonal pattern.  If \(E_{aa}\) and \(E_{cc}\) are diagonal, their
one-site pairing is \(1/2\) when \(a=c\) and \(-1/2\) when \(a\ne c\).
Tensoring (20) gives all contractions below.

Let
\[
\widehat u=|{\bf1}\rangle+p\sum_i|e_i\rangle,\qquad
\widehat v=|{\bf0}\rangle+q\sum_i|\bar e_i\rangle,
\]
and let \(\widehat A,\widehat B\) be their unnormalized projectors.
Classifying the matrix-unit terms by their Hamming distances gives
\[
\begin{aligned}
Q_n(\widehat A)
={}&r\left(1+2n(-1)^{n-1}p^2+n^2p^4\right)
+np^2+\kappa p^4,                                      \tag{21}\\
\mathcal B_n(\widehat A,\widehat B)
={}&r\left((-1)^n-n(p^2+q^2)+n^2(-1)^np^2q^2\right)\\
&\hspace{18mm}-npq+(-1)^n\kappa p^2q^2.                 \tag{22}
\end{aligned}
\]
For completeness, the terms outside the first brackets in (21)--(22) are
the off-diagonal contributions.  There are \(2n\) ordered
\(({\bf1},e_i)\) matrix units, each with coefficient \(p\) and pairing
\(1/2\), giving \(np^2\).  There are \(n(n-1)\) ordered
\((e_i,e_j)\), \(i\ne j\), each with pairing \(2^{-(n-2)}\), giving
\(\kappa p^4\).  Across \(\widehat A,\widehat B\), the first class pairs
with \((\bar e_i,{\bf0})\) with value \(-1/2\), giving \(-npq\);
the second pairs with \((\bar e_j,\bar e_i)\) with value
\((-1/2)^{n-2}\), giving the last term of (22).  The remaining terms are
diagonal and give the displayed Hamming-sign brackets.  This proves
(21)--(22) directly from (20).

Divide (21) by \(d_p^2\), divide (22) by \(d_pd_q\), and subtract or add
the baseline \(r\) as in (5).  If \(n\) is odd, the resulting strong
matrix entries are
\[
\begin{aligned}
M_{11}&=\frac{p^2(\kappa p^2+n)}{d_p^2},&
M_{22}&=\frac{q^2(\kappa q^2+n)}{d_q^2},\\
M_{12}&=-\frac{pq(\kappa pq+n)}{d_pd_q}.
\end{aligned}
\tag{23}
\]
Substitution in (4) gives (19).

Now suppose \(n\) is even.  The entries are
\[
\begin{aligned}
M_{11}&=\frac{p^2(\kappa p^2+\beta)}{d_p^2},&
M_{22}&=\frac{q^2(\kappa q^2+\beta)}{d_q^2},\\
M_{12}&=\frac{\eta p^2q^2-npq+2r}{d_pd_q}.
\end{aligned}
\tag{24}
\]
The diagonal entries are nonnegative.  If the numerator of \(M_{12}\) is
nonnegative, copositivity is immediate.  It remains to consider
\[
h(x):=\eta x^2-nx+2r<0,\qquad x=pq.
\tag{25}
\]
After removing the positive denominators, the determinant is
\[
\begin{aligned}
D(p,q)
&=p^2q^2(\kappa p^2+\beta)(\kappa q^2+\beta)-h(pq)^2\\
&=x^2\left(\kappa^2x^2+\kappa\beta(p^2+q^2)+\beta^2\right)-h(x)^2.
\end{aligned}
\tag{26}
\]
For fixed \(x\), this is increasing in \(p^2+q^2\), whose minimum is
\(2x\).  Therefore
\[
D(p,q)\geq g(x)^2-h(x)^2,\qquad
g(x)=x(\kappa x+\beta).
\tag{27}
\]
Under (25), \(g-h>0\).  The other factor is
\[
\begin{aligned}
g(x)+h(x)
&=(\kappa+\eta)x^2+(\beta-n)x+2r\\
&=2r\left(n(5n-4)x^2-2nx+1\right)>0.                    \tag{28}
\end{aligned}
\]
The last quadratic has positive leading coefficient and discriminant
\[
(-2n)^2-4n(5n-4)=16n(1-n)<0.
\tag{29}
\]
Thus \(D(p,q)\geq0\) whenever the off-diagonal entry is negative, which is
exactly the remaining two-by-two copositivity condition.  This proves the
theorem for even \(n\), and completes the proof. \(\square\)

For odd \(n\) and positive \(p,q,\lambda,\mu\), (19) shows that equality
holds exactly when \(p=q\) and \(\lambda=\mu\).  Boundary equalities also
occur when a nonzero spectral summand is the product endpoint \(p=0\) or
\(q=0\).  The even-\(n\) proof is strict in the interior of the
negative-cross-term region.

The rational example (10) is Theorem 1 with
\[
n=3,\qquad p=\frac15,\qquad q=\frac23.
\tag{30}
\]
For the whole \(n=3\) subfamily one additionally has
\[
Q_3(A)+\mathcal B_3(A,B)
=\frac{3p(p-q)(p^2-2pq+1)}
{(1+3p^2)^2(1+3q^2)},
\tag{31}
\]
which makes the failed mixed-subprojection invariant visible without any
numerical search.

## 4. A quantitative \(n=3\) theorem on common local qubit supports

The all-copy local-qubit-support argument that only proves \(Q_n(H)\geq0\)
does not by itself imply the positive right side of (1).  At three copies,
however, an anticommutation argument gives the sharp quantitative result.

### Theorem 2

Let \(W_i\) be local subspaces with \(\dim W_i\leq2\), and suppose
\[
H\succeq0,\qquad \operatorname{rank}H\leq2,\qquad
H=P_WH P_W,\qquad W=W_1\otimes W_2\otimes W_3.
\tag{32}
\]
Then \(H\) satisfies (1) for \(n=3\).

#### Proof

It is enough to regard every \(W_i\) as a qubit, extending a
one-dimensional support by an unused basis vector if necessary.  Purify
\(H\) with one qubit \(K\):
\[
H=\operatorname{Tr}_K|\Psi\rangle\langle\Psi|,
\qquad T=\langle\Psi,\Psi\rangle=\operatorname{Tr}H.
\tag{33}
\]
Write \(P_S=\operatorname{Tr}\rho_S^2\) for the unnormalized reduced
purity of \(|\Psi\rangle\) on a subsystem \(S\).  Equality of complementary
purities of a pure vector gives
\[
\operatorname{Tr}H^2=P_K,\qquad
\|\operatorname{Tr}_iH\|_2^2=P_{Ki},\qquad
\|\operatorname{Tr}_{ij}H\|_2^2=P_k.
\tag{34}
\]
Expanding \(Q_3\) now gives
\[
\Delta_3(H)
=\frac14\left(3P_K+\sum_{i=1}^3P_i-2\sum_{i=1}^3P_{Ki}\right).
\tag{35}
\]

Let \(X,Y,Z\) denote the Pauli matrices.  For \(a,b\in\{X,Y,Z\}\), put
\[
t_{i,ab}
=\langle\Psi|\sigma_a^{(K)}\otimes\sigma_b^{(i)}|\Psi\rangle.
\tag{36}
\]
The Pauli expansion of the one- and two-qubit reduced states cancels all
one-body terms in (35), leaving
\[
3P_K+\sum_iP_i-2\sum_iP_{Ki}
=\frac12\left(3T^2-\sum_{i,a,b}t_{i,ab}^2\right).
\tag{37}
\]

We use the following elementary anticommutation bound.  If
\(O_1,\ldots,O_m\) are pairwise anticommuting Hermitian involutions and
\(\rho\succeq0\) has trace \(T\), then
\[
\sum_j(\operatorname{Tr}\rho O_j)^2\leq T^2.
\tag{38}
\]
Indeed, with \(x_j=\operatorname{Tr}\rho O_j\) and
\(O=\sum_jx_jO_j\), anticommutation gives
\(O^2=(\sum_jx_j^2)I\).  Hence
\[
\sum_jx_j^2=\operatorname{Tr}\rho O
\leq T\|O\|=T\sqrt{\sum_jx_j^2},
\]
which proves (38).

For each permutation \(\pi\) of \(\{X,Y,Z\}\), form the nine observables
\[
\mathcal C_\pi
=\left\{\sigma_{\pi(i)}^{(K)}\otimes\sigma_b^{(i)}
:i=1,2,3,\ b=X,Y,Z\right\}.
\tag{39}
\]
Within one physical site, distinct \(b\)'s anticommute.  Between different
sites, the assigned Pauli matrices on \(K\) are distinct and anticommute.
Thus every \(\mathcal C_\pi\) is a pairwise anticommuting family, and (38)
applies.  Each observable in (36) occurs in exactly two of the six
families.  Summing the six inequalities gives
\[
2\sum_{i,a,b}t_{i,ab}^2\leq6T^2.
\tag{40}
\]
Equations (35), (37), and (40) prove \(\Delta_3(H)\geq0\). \(\square\)

The theorem includes the equality mechanisms in which the logical qubit is
localized on one physical site, and the classical repetition mechanism in
which one logical Pauli component is present at all three sites.  A complete
classification of simultaneous equality in the six anticommutation bounds
has not been carried out.

## 5. The exact qutrit \(n=3\) target and the compression loss

Let \(P=VV^\dagger\) be an orthogonal rank-two projection on three qutrits,
where \(V:\mathbb C^2\to(\mathbb C^3)^{\otimes3}\) is an isometry.  Purify
the maximally mixed code state by
\[
|\Psi\rangle=\frac1{\sqrt2}\sum_{j=0}^1|j\rangle_KV|j\rangle,
\qquad
X_a=\frac12V\sigma_a^TV^\dagger\quad(a=0,1,2,3),
\tag{41}
\]
with \(\sigma_0=I_2\).  Then
\[
|\Psi\rangle\langle\Psi|
=\frac12\sum_{a=0}^3\sigma_a\otimes X_a,\qquad X_0=P/2.
\tag{42}
\]
If \(X_{a,i}=\operatorname{Tr}_{\bar i}X_a\), orthogonality of the Pauli
matrices gives
\[
\operatorname{Tr}\rho_{Ki}^2
=\frac12\sum_{a=0}^3\|X_{a,i}\|_2^2,\qquad
\operatorname{Tr}\rho_i^2=\|X_{0,i}\|_2^2.
\tag{43}
\]
Substitution in the exact three-copy expansion yields
\[
\boxed{\quad
Q_3(P)=\frac32-\sum_{i=1}^3\sum_{a=1}^3
\left\|\operatorname{Tr}_{\bar i}X_a\right\|_2^2.
\quad}
\tag{44}
\]
Thus the unresolved \(n=3\) projection case is the encoded-Pauli
monogamy inequality
\[
\sum_{i,a}\left\|\operatorname{Tr}_{\bar i}X_a\right\|_2^2\leq\frac32.
\tag{45}
\]
Theorem 2 proves (45) when the code has common local qubit supports, but
not for arbitrary qutrit reductions.

There is a precise factor loss in trying to deduce the qutrit result by
averaging qubit compressions.  Let \(W\) be a Haar-uniform
two-dimensional subspace of \(\mathbb C^3\), with projection \(P_W\).
On two replicas,
\[
\int P_W\otimes P_W\,dW
=\frac12\Pi^++\frac13\Pi^-.
\tag{46}
\]
This follows by unitary invariance and traces: the compressed symmetric
and antisymmetric subspaces have dimensions \(3\) and \(1\), while the
ambient ones have dimensions \(6\) and \(3\).

Apply independent compressions at the three physical sites to the
four-party purification in (41).  The compressed vector is a
four-qubit vector, so Theorem 2 gives
\[
\sum_{\{i,j\}}\!p_{\{i,j\}}^{\,W}
\geq3p_{\{K,1,2,3\}}^{\,W},
\tag{47}
\]
where the left sectors are antisymmetric at the indicated two physical
replica pairs and symmetric at \(K\) and the remaining physical pair.
After averaging (46), a two-minus/one-plus physical sector is multiplied
by
\[
\left(\frac13\right)^2\frac12=\frac1{18},
\]
whereas the three-minus physical sector is multiplied by \(1/27\).
Consequently (47) yields only
\[
\boxed{\quad
\sum_{\{i,j\}}p_{\{i,j\}}\geq2p_{\{K,1,2,3\}},
\quad}
\tag{48}
\]
while the desired coefficient is \(3\).  This proves exactly why the
isotropic local-compression tensorization is insufficient.

## 6. Discovery-layer searches

Floating-point optimization was used only to look for algebraic targets.
The variable was a complex \(D\times2\) matrix \(A\), with
\(H=AA^\dagger/\operatorname{Tr}(AA^\dagger)\), and the exact objective
was the homogeneous defect \(\Delta_n(H)\).  Analytic gradients were
checked against centered finite differences.

The following independent complex searches all converged to zero or a
positive value:
\[
\begin{array}{c|c|c}
(d,n)&\text{random starts}&\text{smallest returned value}\\ \hline
(2,4)&20&9.8\times10^{-17}\\
(2,5)&12&1.8\times10^{-16}\\
(3,3)&16&8.3\times10^{-17}\\
(3,4)&8&2.0\times10^{-16}.
\end{array}
\tag{49}
\]
These data are not verification evidence.  Their only role was to steer
the search toward exact zero families and away from spurious
floating-point negatives.  The parity family in Theorem 1 and the rational
certificate (10)--(15) were subsequently verified by the independent
matrix-unit calculation (20)--(29).

## 7. Status and useful obstructions

What is proved:

1. The strong conjecture reduces exactly to the two-by-two copositivity
   condition (6).
2. Termwise \(W_3\)-sector positivity and mixed-subprojection positivity
   are both false, by the exact certificate (10)--(14).
3. A genuinely non-product parity family satisfies the strong conjecture
   for every copy number; odd copy numbers have the SOS (19), and even copy
   numbers have the exact copositivity proof (24)--(29).
4. The sharp \(n=3\) strong inequality holds on common local qubit
   supports, by Theorem 2.
5. The general qutrit rank-two projection target is exactly (45), and
   random qubit compression provably loses a factor, as in (48).

What is not proved:

1. There is no all-copy proof of (1) for arbitrary rank-two PSD operators.
2. There is no counterexample to (1).
3. Even a counterexample to (1) would not automatically be a negative
   Werner witness, because (1) is stronger than \(Q_n(H)\geq0\).
4. The encoded-Pauli inequality (45) remains open when one or more local
   qutrit reductions use all three dimensions.

The most concrete remaining target exposed here is a dimension-three
replacement for the anticommuting-clique proof of Theorem 2 which reaches
the coefficient \(3\), rather than the compression-shadow coefficient
\(2\).
