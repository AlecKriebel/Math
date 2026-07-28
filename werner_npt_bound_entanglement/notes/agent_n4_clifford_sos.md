# Four-copy Clifford frames and the three-replica obstruction

## Research log and status

- **2026-07-28 14:13 PDT.** Rewrote the proposed four-copy purity
  inequality both as a sum of double-reduction quadratic forms and as a
  two-replica swap-sector inequality.
- **2026-07-28 14:13 PDT.** Proved a sharp covariance inequality for one
  commuting and three pairwise anticommuting Hermitian contractions.  Its
  application to the four normalized logical Pauli reductions has an exact
  factor-of-two constant gap from the desired inequality.
- **2026-07-28 14:13 PDT.** Constructed an exact qutrit code showing that
  the constant in this normalized-singleton Clifford method cannot be
  improved.  In particular, the natural all-six-pair moment inequality
  which would prove the target is false.
- **2026-07-28 14:13 PDT.** Lifted the target to three replicas and used
  the absence of the sign representation on three copies of the logical
  qubit.  The resulting averaged operator is nevertheless negative on an
  explicit globally invariant representation sector: its expectation is
  exactly \(-4\).

The four-copy inequality itself is **not proved or refuted here**.  No
counterexample to it was found.  The exact results below instead close two
natural proof routes: neither normalized singleton Clifford frames nor
state-independent positivity on the admissible \(S_3\) representation
sectors can prove the target without an additional cross-sector identity.

## 1. Equivalent forms of the target

Let
\[
U:\mathbb C^2\longrightarrow A_1\otimes A_2\otimes A_3\otimes A_4
\]
be an isometry, put \(P=UU^\dagger\), and take
\[
|\Psi\rangle
=\frac{|0\rangle U|0\rangle+|1\rangle U|1\rangle}{\sqrt2}.
\tag{1}
\]
Thus \(\rho_K=I_2/2\) and the physical marginal is \(P/2\).  With
\(\sigma_0=I,\sigma_1=X,\sigma_2=Y,\sigma_3=Z\), define
\[
X_a=\frac12U\sigma_a^{\mathsf T}U^\dagger,\qquad
X_{a,T}=\operatorname{Tr}_{\bar T}X_a,\qquad
q_{a,T}=\|X_{a,T}\|_2^2.
\tag{2}
\]
The maximally entangled expansion is
\[
|\Psi\rangle\langle\Psi|
=\frac12\sum_{a=0}^3\sigma_a\otimes X_a.
\tag{3}
\]
Consequently
\[
\operatorname{Tr}\rho_{KT}^2
=\frac12\sum_{a=0}^3q_{a,T},
\qquad
\operatorname{Tr}\rho_T^2=q_{0,T}.
\tag{4}
\]

### Lemma 1.1 (Pauli-complement identity)

For every \(T\subseteq\{1,2,3,4\}\),
\[
\boxed{\qquad
\sum_{a=0}^3q_{a,T}=2q_{0,\bar T}.
\qquad}
\tag{5}
\]
In particular,
\[
\boxed{\qquad
\sum_{i<j}\sum_{a=1}^3q_{a,ij}
=\sum_{i<j}q_{0,ij}.
\qquad}
\tag{6}
\]

#### Proof

Since (1) is pure, the reductions on \(KT\) and \(\bar T\) have the
same nonzero eigenvalues and hence the same purity.  Equation (4) gives
(5).  If \(|T|=2\), sum (5) over all six pairs.  Complementation
permutes the six pairs, so
\[
\sum_{i<j}\sum_{a=0}^3q_{a,ij}
=2\sum_{i<j}q_{0,ij}.
\]
Subtracting the \(a=0\) terms proves (6). \(\square\)

Write
\[
\mathcal I(\Psi)
=6\operatorname{Tr}\rho_K^2
+\sum_{i<j}\operatorname{Tr}\rho_{ij}^2
-3\sum_i\operatorname{Tr}\rho_{Ki}^2.
\tag{7}
\]
Since \(\operatorname{Tr}\rho_K^2=1/2\), equations (4)--(6) give
\[
\boxed{\quad
2\mathcal I
=6+\sum_{i<j}\sum_{a=0}^3q_{a,ij}
-3\sum_i\sum_{a=0}^3q_{a,i}
=6+2B-3S,
\quad}
\tag{8}
\]
where
\[
S=\sum_i\sum_{a=0}^3q_{a,i},\qquad
B=\sum_{i<j}q_{0,ij}
 =\sum_{i<j}\sum_{a=1}^3q_{a,ij}.
\tag{9}
\]
Thus the proposed inequality is exactly
\[
\boxed{\qquad 3S\leq 6+2B.\qquad}
\tag{10}
\]

There is also a useful reduction-map form.  On a qutrit site let
\[
\mathcal R_i(Z)=\operatorname{Tr}_i(Z)\otimes I_i-Z.
\tag{11}
\]
Partial-trace adjointness gives
\[
\begin{aligned}
\langle P,\mathcal R_i\mathcal R_j(P)\rangle
={}&\|\operatorname{Tr}_{ij}P\|_2^2
-\|\operatorname{Tr}_iP\|_2^2
-\|\operatorname{Tr}_jP\|_2^2+\|P\|_2^2.
\end{aligned}
\tag{12}
\]
Purity equality for complementary reductions of (1), together with
\(\|P\|_2^2=2\), now yields
\[
\boxed{\qquad
\mathcal I(\Psi)
=\frac14\sum_{i<j}
\langle P,\mathcal R_i\mathcal R_j(P)\rangle.
\qquad}
\tag{13}
\]

For completeness, let \(\Pi_R\) be antisymmetric on the two replicas of
the physical sites in \(R\) and symmetric on the remaining sites, and put
\[
p_R=\operatorname{Tr}[(P\otimes P)\Pi_R],\qquad
e_r=\sum_{|R|=r}p_R.
\tag{14}
\]
Writing \(F_T=\prod_{i\in T}F_i\), the swap trick and (12) give the
exact two-replica identity
\[
\langle P,\mathcal R_i\mathcal R_j(P)\rangle
=\operatorname{Tr}\!\left[
(P\otimes P)F_{\overline{\{i,j\}}}(I-F_i)(I-F_j)
\right].
\]
On the sector \(\Pi_R\), this vanishes unless
\(\{i,j\}\subseteq R\); if it does not vanish, its eigenvalue is
\(4(-1)^{|R|-2}\).  Summing over the pairs gives
\[
\sum_{i<j}\langle P,\mathcal R_i\mathcal R_j(P)\rangle
=4e_2-12e_3+24e_4.
\tag{15}
\]
Hence
\[
\boxed{\qquad \mathcal I=e_2-3e_3+6e_4.\qquad}
\tag{16}
\]
This form displays the difficult negative three-antisymmetry layer.

## 2. A sharp commuting--Clifford covariance inequality

The following elementary lemma is the strongest useful statement found
for the proposed four-observable construction.

### Lemma 2.1

Let \(\omega\) be a state, let \(C=C^\dagger\) be a Hermitian
contraction, and let \(A_1,\ldots,A_m\) be pairwise anticommuting
Hermitian contractions which commute with \(C\).  Set
\[
c=\operatorname{Tr}(\omega C),\qquad
x_r=\operatorname{Tr}(\omega A_r),\qquad
z_r=\operatorname{Tr}(\omega CA_r).
\tag{17}
\]
Then
\[
\boxed{\qquad
c^2+\sum_{r=1}^m x_r^2
\leq 1+\sum_{r=1}^m z_r^2.
\qquad}
\tag{18}
\]

#### Proof

First dilate \(C\) to the Hermitian involution
\[
\widehat C=
\begin{pmatrix}
C&(I-C^2)^{1/2}\\
(I-C^2)^{1/2}&-C
\end{pmatrix}.
\tag{19}
\]
Use \(\widehat A_r=A_r\oplus A_r\) and
\(\widehat\omega=\omega\oplus0\).  Functional calculus and
\([C,A_r]=0\) show that \(\widehat C\) commutes with every
\(\widehat A_r\).  The dilation preserves all three quantities in
(17), so it is enough to assume \(C^2=I\).

Put \(E_\pm=(I\pm C)/2\),
\[
p_\pm=\operatorname{Tr}(\omega E_\pm),\qquad
u_{\pm,r}=\operatorname{Tr}(\omega E_\pm A_r).
\tag{20}
\]
On each \(C\)-eigenspace the \(A_r\)'s remain pairwise anticommuting
contractions.  Their expectation vector lies in the Euclidean unit
ball; in homogeneous form,
\[
\sum_r u_{\pm,r}^2\leq p_\pm^2.
\tag{21}
\]
Here is a proof of this standard one-line estimate.  If \(y_r\) are
the normalized expectations and \(Y=\sum_r y_rA_r\), then
\[
Y^2=\sum_r y_r^2A_r^2\leq
\left(\sum_r y_r^2\right)I.
\]
But the expectation of \(Y\) is \(\sum_r y_r^2\), so
\(\sum_r y_r^2\leq\sqrt{\sum_r y_r^2}\).

Now \(x_r=u_{+,r}+u_{-,r}\), \(z_r=u_{+,r}-u_{-,r}\), and
\(c=p_+-p_-\).  Cauchy--Schwarz and (21) give
\[
\begin{aligned}
\sum_r(x_r^2-z_r^2)
&=4\sum_r u_{+,r}u_{-,r}\\
&\leq4p_+p_-=1-c^2,
\end{aligned}
\]
which is (18). \(\square\)

When \(C\) is already an involution, equality in (18) requires, apart
from zero-weight eigenspaces, that both conditional expectation vectors
saturate their anticommuting unit balls and point in the same direction.
Thus (18) is sharp.

## 3. What the normalized logical frame proves

Fix a site \(r\), and biject the other three sites with the three
nonidentity Pauli labels by
\[
\pi:\{1,2,3,4\}\setminus\{r\}\longrightarrow\{1,2,3\}.
\tag{22}
\]
For every nonzero \(X_{a,i}\), set
\[
G_{a,i}=\frac{X_{a,i}}{\|X_{a,i}\|_2};
\tag{23}
\]
set \(G_{a,i}=0\) when \(X_{a,i}=0\).  These are Hermitian
contractions because operator norm is bounded by Hilbert--Schmidt norm,
and their Hilbert--Schmidt norms are at most one.

On the purification space define
\[
C=I_K\otimes G_{0,r}^{(r)},\qquad
A_s=\sigma_{\pi(s)}^{(K)}\otimes
G_{\pi(s),s}^{(s)}\quad(s\ne r).
\tag{24}
\]
The three \(A_s\)'s anticommute pairwise and commute with \(C\).  From
(3),
\[
\langle C\rangle^2=q_{0,r},\qquad
\langle A_s\rangle^2=q_{\pi(s),s}.
\tag{25}
\]
Moreover,
\[
\left|\langle CA_s\rangle\right|^2
\leq q_{\pi(s),rs},
\tag{26}
\]
because the physical test operator
\(G_{0,r}\otimes G_{\pi(s),s}\) has Hilbert--Schmidt norm at most one.
Lemma 2.1 therefore proves the exact frame inequality
\[
\boxed{\quad
q_{0,r}+\sum_{s\ne r}q_{\pi(s),s}
\leq1+\sum_{s\ne r}q_{\pi(s),rs}.
\quad}
\tag{27}
\]

Sum (27) over the four choices of \(r\) and the six bijections \(\pi\).
Every singleton \(q_{a,i}\), including \(a=0\), occurs six times.
Every \(q_{a,ij}\) with \(a\ne0\) occurs four times on the right: either
endpoint of \(\{i,j\}\) may carry the scalar label, and the two unused
Pauli labels may be assigned in two orders.  Thus
\[
6S\leq24+4B,
\]
or
\[
\boxed{\qquad 3S\leq12+2B.\qquad}
\tag{28}
\]
Comparison with (10) shows an exact additive gap of \(6\).

There is an especially natural attempted repair.  In each frame (24),
include all six pair products.  If both labels are nonidentity, multiply
the product by \(i\) when needed to make it Hermitian.  In every case its
expectation magnitude \(m_{ij}\) is bounded by the Hilbert--Schmidt norm
of the appropriate nonidentity two-site logical reduction.  The estimate
\[
q_{0,r}+\sum_{s\ne r}q_{\pi(s),s}
\stackrel{?}{\leq}
\frac12+\frac12\sum_{i<j}|m_{ij}|^2
\tag{29}
\]
would prove (10): every singleton again occurs six times, while every
nonidentity pair component occurs eight times among all frames, four
times with labels \(\{0,a\}\) and four times with the complementary two
Pauli labels.  Summing (29) would give
\[
6S\leq12+4B.
\tag{30}
\]
The next section gives an exact counterexample to (29).

## 4. Exact obstruction to improving the frame constant

On three qutrits define
\[
|\phi_0\rangle
=\frac{|000\rangle+|111\rangle+|222\rangle}{\sqrt3},
\qquad
|\phi_1\rangle
=\frac{|012\rangle+|120\rangle+|201\rangle}{\sqrt3}.
\tag{31}
\]
On four qutrits take
\[
u=|0\rangle\otimes|\phi_0\rangle,\qquad
v=|0\rangle\otimes|\phi_1\rangle,
\qquad P=|u\rangle\langle u|+|v\rangle\langle v|.
\tag{32}
\]
The two vectors are orthonormal because their product-basis supports
are disjoint.

For each of the last three qutrits, both codewords have reduced state
\(I_3/3\).  The one-site reduction of
\(|\phi_0\rangle\langle\phi_1|\) is zero: no support string in (31)
agrees with a support string of the other codeword on the two traced
coordinates.  It follows directly from (2) that
\[
X_{a,s}=0\quad(a=1,2,3;\ s=2,3,4).
\tag{33}
\]
At the first, flagged site,
\[
X_{0,1}=|0\rangle\langle0|,\qquad q_{0,1}=1.
\tag{34}
\]

Choose \(r=1\) in (22).  Then every nonidentity normalized singleton
test in (23) is zero.  Hence every pair-product moment \(m_{ij}\) in
(29) is zero, while the left side of (29) is one.  The proposed
inequality reads
\[
1\leq\frac12,
\]
and is false.

This example also shows that the constant \(1\) in (27) is sharp even
inside the encoded-qutrit setting with \(\rho_K=I/2\).  Logical
information can vanish from all three one-site reductions while
remaining present in two-site reductions.  A tensor product of
singleton-adaptive observables cannot see that information.

The code (32) is not a counterexample to the target.  Its purities are
\[
\operatorname{Tr}\rho_{Ki}^2=
\begin{cases}
1/2,&i=1,\\
1/6,&i=2,3,4,
\end{cases}
\qquad
\operatorname{Tr}\rho_{ij}^2=
\begin{cases}
1/3,&1\in\{i,j\},\\
1/6,&1\notin\{i,j\}.
\end{cases}
\tag{35}
\]
Therefore
\[
\mathcal I
=3+\left(3\cdot\frac13+3\cdot\frac16\right)
-3\left(\frac12+3\cdot\frac16\right)
=\frac32>0.
\tag{36}
\]

## 5. The exact three-replica \(S_3\) obstruction

Let \(\tau\) run over the three transpositions in \(S_3\), and let
\(V_{\tau,T}\) apply \(\tau\) to the three replicas at every party in
\(T\).  For any reduced state \(\rho_T\),
\[
\langle\Psi|^{\otimes3}V_{\tau,T}|\Psi\rangle^{\otimes3}
=\operatorname{Tr}\rho_T^2,
\tag{37}
\]
because \(\tau\) swaps two replicas and fixes the third.  Consequently
\(\mathcal I\) is the expectation on \(|\Psi\rangle^{\otimes3}\) of
\[
\mathsf M
=\frac13\sum_{\tau}
\left(
6V_{\tau,K}
+\sum_{i<j}V_{\tau,i}V_{\tau,j}
-3\sum_iV_{\tau,K}V_{\tau,i}
\right).
\tag{38}
\]

The tensor cube \(|\Psi\rangle^{\otimes3}\) is invariant under the
simultaneous \(S_3\) action on all five parties.  Also,
\(\Lambda^3K=0\), so the sign representation is absent from
\(K^{\otimes3}\).  It is tempting to prove that \(\mathsf M\) is
positive on the globally invariant subspace after excluding that
logical sign representation.  The following exact sector disproves
this.

Let \(\mathbf 1,\mathbf s,\mathbf v\) denote the trivial, sign, and
two-dimensional standard representations of \(S_3\).  Choose the local
representation labels
\[
(K,A_1,A_2,A_3,A_4)
=(\mathbf v,\mathbf1,\mathbf s,\mathbf s,\mathbf v).
\tag{39}
\]
All these representations occur in the corresponding tensor cubes:
\(\mathbf v\) occurs for a qubit, and all three occur for a qutrit.
Explicitly, the permutation orbit of \(|001\rangle\) contains a
two-dimensional zero-sum subspace carrying \(\mathbf v\), both for
qubits and for qutrits.  For qutrits, \(|000\rangle\) supplies
\(\mathbf1\), while
\[
\frac1{\sqrt6}\sum_{g\in S_3}\operatorname{sgn}(g)
\,V_g|012\rangle
\]
supplies \(\mathbf s\).  An alternating three-tensor on a
two-dimensional qubit space is zero, which is the elementary reason
that the logical sign sector is absent.
Let \(\pi\) be a real orthogonal model of \(\mathbf v\), with
orthonormal basis \(e_1,e_2\), and couple the two standard factors by
\[
|\eta\rangle
=\frac{e_1\otimes e_1+e_2\otimes e_2}{\sqrt2}.
\tag{40}
\]
Tensor (40) with unit vectors in the three one-dimensional factors.
Because \(\mathbf s\otimes\mathbf s=\mathbf1\) and (40) is invariant
under \(\pi(g)\otimes\pi(g)\), the resulting vector is globally
\(S_3\)-invariant.  The latter invariance follows directly by identifying
(40) with \(\operatorname{vec}(I_2)/\sqrt2\):
\((\pi(g)\otimes\pi(g))\operatorname{vec}(I_2)
=\operatorname{vec}(\pi(g)\pi(g)^{\mathsf T})
=\operatorname{vec}(I_2)\).

For a transposition \(\tau\),
\[
\operatorname{Tr}\pi(\tau)=0,\qquad
\langle\eta|\pi(\tau)\otimes\pi(\tau)|\eta\rangle=1.
\tag{41}
\]
The first term in (38) therefore has expectation zero.  Among physical
pairs, the three one-dimensional pairs contribute
\[
(+1)(-1)+(+1)(-1)+(-1)(-1)=-1,
\tag{42}
\]
and every pair containing the lone standard physical factor has zero
expectation.  Among the four \(K\)-physical pairs, only the
standard--standard pair has nonzero expectation, equal to one.  Hence,
for every transposition separately,
\[
\langle\mathsf M\rangle
=0+(-1)-3(1)
=\boxed{-4}.
\tag{43}
\]

Thus \(\mathsf M\) is not positive on the globally invariant subspace
allowed by the qubit dimension.  The missing restriction is nonlinear:
the actual test vector is the diagonal cube
\(|\Psi\rangle^{\otimes3}\), not an arbitrary invariant vector.  Any
successful \(S_3\) proof must use those tensor-cube (Veronese) relations
between representation sectors, not only their nonnegative weights.

## 6. Exact positive and equality subclasses

The target has large equality families, which helps explain why direct
optimization is attracted to its boundary.

### 6.1 A logical flag gives equality

Suppose, after local unitaries,
\[
|\Psi\rangle
=|\Omega_2\rangle_{KA_1}\otimes|\phi\rangle_{A_2A_3A_4}.
\tag{44}
\]
Put
\[
s_j=\operatorname{Tr}
\left(\operatorname{Tr}_{\{2,3,4\}\setminus\{j\}}
|\phi\rangle\langle\phi|\right)^2.
\]
The sum of the six physical pair purities is
\[
\frac12\sum_{j=2}^4s_j+\sum_{j=2}^4s_j
=\frac32\sum_{j=2}^4s_j,
\]
while
\[
\sum_i\operatorname{Tr}\rho_{Ki}^2
=1+\frac12\sum_{j=2}^4s_j.
\]
Substitution in (7) gives
\[
\boxed{\mathcal I=0}
\tag{45}
\]
for every pure three-qutrit state \(\phi\).

### 6.2 A pure physical flag reduces exactly to the three-site theorem

Suppose instead
\[
|\Psi\rangle=|0\rangle_{A_1}\otimes
|\Phi\rangle_{KA_2A_3A_4},
\qquad \rho_K=I_2/2.
\tag{46}
\]
Complementary purity in the four-party pure state \(\Phi\) gives
\[
\mathcal I
=\frac32+\sum_{j=2}^4\operatorname{Tr}\rho_j^2
-2\sum_{j=2}^4\operatorname{Tr}\rho_{Kj}^2.
\tag{47}
\]
For the three-site encoded Pauli reductions, (4) turns this into
\[
\mathcal I
=\frac32-\sum_{j=2}^4\sum_{a=1}^3
\|X_{a,j}\|_2^2.
\tag{48}
\]
This is nonnegative by the following short self-contained sign-frame
argument.  For a permutation \(\pi\) of the three Pauli axes, take
\[
G_j=\operatorname{sgn}(X_{\pi(j),j}),\qquad
O_j=\sigma_{\pi(j)}\otimes G_j.
\]
The three \(O_j\)'s anticommute, so the argument inside the proof of
Lemma 2.1 gives
\[
\sum_j\|X_{\pi(j),j}\|_1^2\leq1.
\tag{49}
\]
Every \(X_{a,j}\) with \(a\ne0\) is traceless.  If its positive
eigenvalues sum to \(t\), so do the absolute values of its negative
eigenvalues; hence
\[
\|X_{a,j}\|_1^2=4t^2
\geq2\|X_{a,j}\|_2^2.
\tag{50}
\]
Sum (49)--(50) over the six permutations.  Every pair \((a,j)\)
occurs twice, giving
\[
\sum_{j,a\ne0}\|X_{a,j}\|_2^2\leq\frac32.
\]
Together with (48), this proves
\[
\boxed{\mathcal I\geq0}
\tag{51}
\]
for every pure physical-flag code.

### 6.3 The repetition code

For
\[
|\Psi\rangle
=\frac{|0\rangle_K|0000\rangle+|1\rangle_K|1111\rangle}{\sqrt2},
\tag{52}
\]
every physical pair and every \(K\)-physical pair has purity \(1/2\).
Thus
\[
\mathcal I=3+6\left(\frac12\right)
-3\cdot4\left(\frac12\right)=0.
\tag{53}
\]

## 7. What the Clifford/SOS attack establishes

1. The target is exactly the double-reduction sum (13), or the sector
   inequality \(e_2+6e_4\geq3e_3\).
2. Lemma 2.1 is a sharp covariance inequality for the proposed
   \(I,X,Y,Z\) observable pattern.  Applied to normalized reduced
   correlations, it yields (28), with an irreducible additive gap of
   \(6\) from the target.
3. The exact code (31)--(34) refutes the all-six-pair frame inequality
   (29) that would close that gap.  Pair-adaptive information is
   essential when all singleton logical reductions vanish.
4. The three-replica identity (38) faithfully represents the target,
   but its operator has the exact negative invariant sector (39)--(43).
   Positivity of \(S_3\) sector weights and the absence of the logical
   sign representation are therefore insufficient.
5. The logical-flag, physical-flag, and repetition families satisfy the
   target exactly, with the first and third families saturating it.

The remaining plausible SOS mechanism must couple either different
normalized frames or different \(S_3\) sectors through the fact that all
amplitudes come from one common isometry \(U\).  Neither independent
frame inequalities nor a linear representation-sector certificate
contains that information.

## 8. Tiny exact arithmetic audit

The scalar arithmetic in the two explicit obstructions and examples can
be replayed with:

```python
from fractions import Fraction as F

# The hidden-singleton code (32).
pair_sum = 3*F(1, 3) + 3*F(1, 6)
K_single_sum = F(1, 2) + 3*F(1, 6)
assert 3 + pair_sum - 3*K_single_sum == F(3, 2)

# The invariant S_3 sector (39): physical-pair contribution -1,
# one standard--standard K-pair contribution +1.
assert 6*0 + (-1) - 3*1 == -4

# The repetition equality code (52).
assert 3 + 6*F(1, 2) - 3*4*F(1, 2) == 0
```

This audit only checks the displayed rational evaluations; the
structural statements are proved above.
