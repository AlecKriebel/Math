# Adaptive sign frames for the three-copy projection problem

## Research checkpoint

**2026-07-28 12:17 PDT.**  The qutrit-specific frame bottleneck is
resolved for all positive semidefinite operators of rank at most two.
A state-dependent sign observable replaces the embedded-Pauli frame and
proves the sharp strong three-copy inequality, in fact for arbitrary
local dimensions.  The proposed stronger per-sector lemma is false by an
exact one-parameter
family, but its cyclic sum is saturated by that family.  Best-guess
completion of the bounded \(n=3\) projection task: **100%**.  This does
not resolve arbitrary nonnormal rank-two coefficient matrices or any
all-copy statement.

## 1. The theorem

Let
\[
\mathcal H=H_1\otimes H_2\otimes H_3
\]
with arbitrary finite-dimensional local spaces, and let \(P\) be a
rank-two orthogonal projection on \(\mathcal H\).  At the endpoint put
\[
Q_3(P)=
\sum_{S\subseteq\{1,2,3\}}
\left(-\frac12\right)^{|S|}
\left\|\operatorname{Tr}_S P\right\|_2^2.
\tag{1}
\]

### Theorem 1

For every such \(P\),
\[
\boxed{\qquad Q_3(P)\geq0.\qquad}
\tag{2}
\]

For three qutrits, if \(\rho=P/2\), this is equivalently
\[
\boxed{\qquad
2\sum_{i<j}\operatorname{Tr}\rho_{ij}^2
-\sum_i\operatorname{Tr}\rho_i^2
\leq\frac32.
\qquad}
\tag{3}
\]

The proof uses only two elementary inequalities.  They are included to
make the result independently checkable.

### Lemma 2: anticommuting contractions

Let \(O_1,\ldots,O_m\) be pairwise anticommuting Hermitian contractions
on a Hilbert space, and let \(\omega\) be a state.  Then
\[
\sum_{j=1}^m\bigl(\operatorname{Tr}\omega O_j\bigr)^2\leq1.
\tag{4}
\]

#### Proof

Put \(x_j=\operatorname{Tr}\omega O_j\), \(s=\sum_jx_j^2\), and
\(O=\sum_jx_jO_j\).  Pairwise anticommutation and \(O_j^2\leq I\) give
\[
O^2=\sum_jx_j^2O_j^2\leq sI.
\]
On the other hand,
\[
\operatorname{Tr}\omega O=\sum_jx_j^2=s.
\]
Thus \(s\leq\|O\|\leq\sqrt{s}\), so either \(s=0\) or \(s\leq1\).
\(\square\)

### Lemma 3: the traceless trace-norm bound

If \(X=X^\dagger\) and \(\operatorname{Tr}X=0\), then
\[
\boxed{\qquad \|X\|_1^2\geq2\|X\|_2^2.\qquad}
\tag{5}
\]

#### Proof

Write the positive eigenvalues as \(p_j\), and the absolute values of the
negative eigenvalues as \(q_k\).  Tracelessness gives
\[
\sum_jp_j=\sum_kq_k=:s.
\]
Therefore
\[
\|X\|_2^2=\sum_jp_j^2+\sum_kq_k^2\leq2s^2,
\qquad
\|X\|_1^2=(2s)^2.
\]
This proves (5).  Equality holds precisely when there is at most one
nonzero positive eigenvalue and at most one nonzero negative eigenvalue.
\(\square\)

### Proof of Theorem 1

Choose an isometry
\[
V:\mathbb C^2\longrightarrow\mathcal H,\qquad P=VV^\dagger,
\]
and purify \(P/2\) by
\[
|\Psi\rangle
=\frac1{\sqrt2}\sum_{r=0}^1|r\rangle_K\otimes V|r\rangle .
\tag{6}
\]
Let
\[
\sigma_0=I,\quad \sigma_1=X,\quad\sigma_2=Y,\quad\sigma_3=Z
\]
be the Pauli matrices, and define
\[
X_a=\frac12V\sigma_a^{\mathsf T}V^\dagger,\qquad
X_{a,i}=\operatorname{Tr}_{\{1,2,3\}\setminus\{i\}}X_a.
\tag{7}
\]
The maximally entangled expansion gives
\[
|\Psi\rangle\langle\Psi|
=\frac12\sum_{a=0}^3\sigma_a\otimes X_a.
\tag{8}
\]
For \(a=1,2,3\), every \(X_{a,i}\) is Hermitian and traceless.

We first recover the exact encoded-Pauli form of (1).  The reduced state
on \(K i\) is
\[
\rho_{Ki}=\frac12\sum_{a=0}^3\sigma_a\otimes X_{a,i},
\]
and Pauli orthogonality gives
\[
\operatorname{Tr}\rho_{Ki}^2
=\frac12\sum_{a=0}^3\|X_{a,i}\|_2^2.
\tag{9}
\]
Also \(\rho_i=X_{0,i}\).  Since \(|\Psi\rangle\) is pure,
complementary reductions have equal purities.  Expanding (1), using
\(\operatorname{Tr}P=\operatorname{Tr}P^2=2\), gives
\[
\begin{aligned}
Q_3(P)
&=\frac32-2\sum_i\operatorname{Tr}\rho_{Ki}^2
  +\sum_i\operatorname{Tr}\rho_i^2\\
&=\boxed{\frac32-\sum_{i=1}^3\sum_{a=1}^3
\|X_{a,i}\|_2^2}.
\end{aligned}
\tag{10}
\]

It remains to bound the last sum.  Fix a permutation
\(\pi\in S_3\).  For each physical site \(i\), let
\[
G_i=\operatorname{sgn}(X_{\pi(i),i}),
\tag{11}
\]
where the sign is \(+1\) on the positive spectral subspace, \(-1\) on
the negative spectral subspace, and \(0\) on the kernel.  Then \(G_i\)
is a Hermitian contraction and trace-norm duality is exact:
\[
\operatorname{Tr}(X_{\pi(i),i}G_i)
=\|X_{\pi(i),i}\|_1.
\tag{12}
\]
On the full purification space define
\[
O_i=\sigma_{\pi(i)}^{(K)}\otimes G_i^{(i)}.
\tag{13}
\]
The three \(G_i\)'s act on distinct physical sites and hence commute.
The three logical Pauli matrices in a permutation are distinct and
hence anticommute.  Consequently the \(O_i\)'s are pairwise
anticommuting Hermitian contractions.  Equations (8) and (12) give
\[
\langle\Psi|O_i|\Psi\rangle
=\operatorname{Tr}(X_{\pi(i),i}G_i)
=\|X_{\pi(i),i}\|_1.
\tag{14}
\]
Lemma 2 and then Lemma 3 imply
\[
1\geq\sum_i\|X_{\pi(i),i}\|_1^2
\geq2\sum_i\|X_{\pi(i),i}\|_2^2.
\tag{15}
\]

Sum (15) over all six permutations.  Every ordered pair \((i,a)\)
occurs in exactly two permutations.  Therefore
\[
4\sum_{i=1}^3\sum_{a=1}^3\|X_{a,i}\|_2^2\leq6,
\]
or
\[
\sum_{i,a}\|X_{a,i}\|_2^2\leq\frac32.
\tag{16}
\]
Substitution in (10) proves (2).  Equation (3) is the first line of
(10) rewritten in terms of \(\rho=P/2\). \(\square\)

## 1.1 The full strong rank-two theorem

The equal-spectrum assumption in Theorem 1 is not needed.  The same
argument gives the stronger result which had previously only been proved
when all local supports were qubits.

### Theorem 4

Let \(H\succeq0\) have rank at most two on
\(H_1\otimes H_2\otimes H_3\), with arbitrary finite local dimensions.
Then
\[
\boxed{\qquad
Q_3(H)\geq
\frac18\left(2\operatorname{Tr}H^2-(\operatorname{Tr}H)^2\right).
\qquad}
\tag{17}
\]

#### Proof

Take an unnormalized qubit purification
\[
|\Psi\rangle\in K\otimes H_1\otimes H_2\otimes H_3,
\qquad
\operatorname{Tr}_K|\Psi\rangle\langle\Psi|=H,
\tag{18}
\]
and put \(T=\langle\Psi|\Psi\rangle=\operatorname{Tr}H\).
There are unique Hermitian operators \(X_a\) such that
\[
|\Psi\rangle\langle\Psi|
=\frac12\sum_{a=0}^3\sigma_a\otimes X_a.
\tag{19}
\]
Here \(X_0=H\).  Set
\[
r_a=\operatorname{Tr}X_a\quad(a=1,2,3),\qquad
X_{a,i}=\operatorname{Tr}_{\bar i}X_a.
\tag{20}
\]
Thus \((T,r_1,r_2,r_3)\) are the Pauli coordinates of the unnormalized
reference state \(\rho_K\), and in particular
\[
\operatorname{Tr}\rho_K^2
=\frac12\left(T^2+|r|^2\right).
\tag{21}
\]

For clarity, derive the strong defect directly.  Write \(P_S\) for the
squared Hilbert--Schmidt norm of the reduction of
\(|\Psi\rangle\langle\Psi|\) to \(S\).  Purity equality for complementary
reductions of a pure vector gives
\[
\operatorname{Tr}H^2=P_K,\qquad
\|\operatorname{Tr}_iH\|_2^2=P_{Ki},\qquad
\|\operatorname{Tr}_{ij}H\|_2^2=P_k.
\tag{22}
\]
Consequently
\[
\begin{aligned}
\Delta_3(H)
&:=Q_3(H)-\frac18\left(2\operatorname{Tr}H^2-T^2\right)\\
&=\frac14\left(3P_K+\sum_iP_i-2\sum_iP_{Ki}\right).
\end{aligned}
\tag{23}
\]
The expansion (19) gives
\[
P_{Ki}=\frac12\sum_{a=0}^3\|X_{a,i}\|_2^2,
\qquad
P_i=\|X_{0,i}\|_2^2.
\tag{24}
\]
Using (21), all \(a=0\) terms cancel in (23), leaving
\[
4\Delta_3(H)
=\frac32\left(T^2+|r|^2\right)
-\sum_{i=1}^3\sum_{a=1}^3\|X_{a,i}\|_2^2.
\tag{25}
\]

We need the nontraceless version of Lemma 3:
\[
\boxed{\qquad
2\|X\|_2^2\leq\|X\|_1^2+(\operatorname{Tr}X)^2
\quad(X=X^\dagger).
\qquad}
\tag{26}
\]
Indeed, if the sums of the positive and negative eigenvalue magnitudes
are \(p,q\), then
\[
\|X\|_2^2\leq p^2+q^2
=\frac12\left((p+q)^2+(p-q)^2\right),
\]
which is (26).

Fix \(\pi\in S_3\), take
\(G_i=\operatorname{sgn}(X_{\pi(i),i})\), and define the three
anticommuting contractions \(O_i\) as in (13).  The proof of Lemma 2,
with a positive functional of trace \(T\), gives the homogeneous form
\[
\sum_i\|X_{\pi(i),i}\|_1^2\leq T^2.
\tag{27}
\]
Since \(\operatorname{Tr}X_{a,i}=r_a\), (26) and (27) imply
\[
2\sum_i\|X_{\pi(i),i}\|_2^2
\leq T^2+\sum_i r_{\pi(i)}^2
=T^2+|r|^2.
\tag{28}
\]
Sum over the six permutations.  Every \((i,a)\) occurs twice, and hence
\[
\sum_{i,a}\|X_{a,i}\|_2^2
\leq\frac32\left(T^2+|r|^2\right).
\tag{29}
\]
Equations (25) and (29) prove (17). \(\square\)

For \(H=P\), one has \(T=2\), \(r=0\), and (17) has zero right side.
Thus Theorem 1 is also the equal-spectrum specialization of Theorem 4.

## 2. Why the adaptive frame avoids the qutrit compression loss

The fixed embedded-Pauli approach first chooses a two-plane in a qutrit
and only sees the three-dimensional copy of \(\mathfrak{su}(2)\) inside
the eight-dimensional space \(\mathfrak{su}(3)\).  The sign choice (11)
is different: it is selected after \(X_{a,i}\) is known and is the exact
dual optimizer for that whole operator.  No component of \(X_{a,i}\) is
discarded.

The only price for replacing a Pauli by an arbitrary sign observable is
the passage from trace norm to Hilbert--Schmidt norm.  Tracelessness pays
that price with the sharp factor \(2\) in (5), exactly the factor needed
in (15).  Thus the third qutrit level is not a loss.  If it carries
eigenvalue mass of both signs, (5) is stronger; equality forces the
operator back onto an effective two-dimensional signed support.

There is also a simple state-independent obstruction explaining why an
isotropic positive mixture of two-plane compressions cannot reproduce
this argument.  Let \(W_\ell\subset\mathbb C^3\) be two-planes,
\(P_\ell\) their projections, and \(w_\ell\geq0\).  Suppose
\[
M=\sum_\ell w_\ell P_\ell\otimes P_\ell
=\beta\Pi^++\alpha\Pi^-
\tag{17}
\]
is isotropic on the symmetric and antisymmetric replica sectors.  Put
\(s=\sum_\ell w_\ell\).  Each term has symmetric trace \(3\) and
antisymmetric trace \(1\), whereas those ambient sector dimensions are
\(6\) and \(3\).  Taking sector traces in (17) gives
\[
6\beta=3s,\qquad 3\alpha=s,
\qquad\text{hence}\qquad
\frac{\beta}{\alpha}=\frac32.
\tag{18}
\]
After applying the qubit inequality independently at three sites, a
two-minus/one-plus sector receives weight \(\alpha^2\beta\), while the
three-minus sector receives weight \(\alpha^3\).  Therefore this method
can yield only
\[
E_2\geq 3\frac{\alpha}{\beta}E_3=2E_3,
\tag{19}
\]
not the needed \(E_2\geq3E_3\).

The same trace obstruction persists for arbitrary positive rank-two
filters.  If the two nonzero eigenvalues of the filter effect are
\(x,y\geq0\), its two-replica symmetric and antisymmetric traces are
\[
x^2+y^2+xy,\qquad xy.
\]
Their ratio is at least \(3\), with equality only at \(x=y\).  Thus
orthogonal two-plane projections are already optimal among positive
rank-two filters for an isotropic frame.  State dependence, as in
(11), is essential.

## 3. Exact failure of the proposed per-sector lemma

Let \(\Pi_R\) be antisymmetric on the replica pairs in \(R\) and symmetric
on the other pairs.  For orthonormal \(u,v\), write
\[
a_R(w)=\|\Pi_R(w\otimes w)\|^2,\qquad
c_R(u,v)=\|\Pi_R(u\otimes v)\|^2.
\tag{20}
\]
The suggested pairwise bound
\[
c_{ABC}(u,v)
\stackrel{?}{\leq}
c_{AB}(u,v)+\sqrt{a_{AB}(u)a_{AB}(v)}
\tag{21}
\]
is false.

In fact, let \(\phi\in A\otimes C\) be any entangled unit vector, choose
orthogonal unit vectors \(|0\rangle,|1\rangle\in B\), and set
\[
u=\phi_{AC}\otimes|0\rangle_B,\qquad
v=\phi_{AC}\otimes|1\rangle_B.
\tag{22}
\]
Let
\[
s=\operatorname{Tr}\!\left[
\bigl(\operatorname{Tr}_C|\phi\rangle\langle\phi|\bigr)^2
\right],\qquad q=\frac{1-s}{2}>0.
\tag{23}
\]
On two replicas of \(\phi\), the \(A\)- and \(C\)-swap parities agree,
and the total mass in the minus-minus sector is \(q\).  On the two
orthogonal \(B\)-vectors, the symmetric and antisymmetric masses are
both \(1/2\).  On a self replica \(|0\rangle\otimes|0\rangle\) or
\(|1\rangle\otimes|1\rangle\), the \(B\)-parity is purely symmetric.
Consequently
\[
\begin{array}{c|ccc}
&AB&AC&BC\\ \hline
c_R(u,v)&0&q/2&0\\
a_R(u)&0&q&0\\
a_R(v)&0&q&0
\end{array},
\qquad
c_{ABC}(u,v)=q/2.
\tag{24}
\]
For \(R=AB\), the right side of (21) is zero while the left side is
\(q/2>0\).  The same failure occurs for \(R=BC\).

A completely explicit qutrit instance is
\[
\phi=\frac{|00\rangle+|11\rangle+|22\rangle}{\sqrt3},
\tag{25}
\]
for which \(s=1/3,\ q=1/3\), and hence
\[
c_{ABC}=\frac16,\qquad
c_{AB}=a_{AB}(u)=a_{AB}(v)=0.
\tag{26}
\]

This counterexample does not violate the cyclicly summed proposal
\[
3c_{ABC}\leq
\sum_{|R|=2}c_R+
\sum_{|R|=2}\sqrt{a_R(u)a_R(v)}.
\tag{27}
\]
Indeed, (24) makes both sides equal to \(3q/2\).  The associated code
projection factors as
\[
P=|\phi\rangle\langle\phi|_{AC}\otimes
\bigl(|0\rangle\langle0|+|1\rangle\langle1|\bigr)_B,
\tag{28}
\]
and it satisfies \(Q_3(P)=0\).  Thus cross-pair compensation is
unavoidable, and the coefficient in Theorem 1 is sharp.

## 4. Grouping consequences and the exact four-site obstruction

Because the local dimensions in Theorems 1 and 4 were arbitrary, any
collection of physical sites may be treated as one block.  This gives a
useful all-\(n\) family of necessary inequalities, but not an all-\(n\)
proof.

For a rank-two code isometry \(V\), put
\[
E_a=V\sigma_a^{\mathsf T}V^\dagger,\qquad
L_T=\sum_{a=1}^3
\left\|\operatorname{Tr}_{[n]\setminus T}E_a\right\|_2^2.
\tag{G1}
\]
If \(A,B,C\) are pairwise disjoint blocks whose union is \([n]\), apply
Theorem 1 to the tripartite system
\(H_A\otimes H_B\otimes H_C\).  Since \(E_a=2X_a\), (16) becomes
\[
\boxed{\qquad L_A+L_B+L_C\leq6.\qquad}
\tag{G2}
\]
Empty blocks may be allowed, with \(L_\varnothing=0\).  Thus (G2)
includes \(L_T+L_{\bar T}\leq6\).

More generally, take any \(m\geq3\) disjoint physical blocks and apply
the sign argument to every choice of three blocks and all six assignments
of the logical Pauli axes.  Each block-axis pair occurs in
\(2\binom{m-1}{2}\) inequalities, whereas there are
\(6\binom m3\) inequalities in total.  The same counting as in (15)
gives
\[
\sum_{\text{blocks }B}\sum_{a=1}^3
\left\|\operatorname{Tr}_{\bar B}X_a\right\|_2^2
\leq\frac m2,
\tag{G2d}
\]
or, in the \(E_a=2X_a\) convention,
\[
\sum_B L_B\leq2m.
\tag{G2e}
\]
This is sharp: a classical repetition code broadcasts one logical Pauli
axis to every block and attains \(m/2\) in (G2d).  Thus the direct
anticommuting-clique estimate necessarily grows with the number of
blocks; the special closure at \(m=3\) does not itself furnish an
all-copy invariant.

The strong Theorem 4 also gives a genuine conditional recursion.  Let
\(p_R=\operatorname{Tr}[(P\otimes P)\Pi_R]\) be the exact physical
swap-sector weights.  Fix three individual sites \(i,j,k\), condition
every other site against an arbitrary product bra, and call the
resulting positive rank-at-most-two operator on \(i,j,k\) \(H_x\).
The sector form of Theorem 4 says
\[
p_{\{i,j\}}(H_x)+p_{\{i,k\}}(H_x)+p_{\{j,k\}}(H_x)
\geq3p_{\{i,j,k\}}(H_x).
\tag{G2a}
\]
Average each conditioning vector independently with Haar measure.  The
elementary second-moment identity
\[
\int |x\rangle\langle x|^{\otimes2}\,dx
=\frac{2}{d(d+1)}\Pi^+
\tag{G2b}
\]
inserts a positive scalar times the symmetric replica projector at
every conditioned site.  The common scalar cancels from (G2a), leaving
the global necessary inequality
\[
\boxed{\qquad
p_{\{i,j\}}+p_{\{i,k\}}+p_{\{j,k\}}
\geq3p_{\{i,j,k\}}.
\qquad}
\tag{G2c}
\]
Thus the sign-frame result does propagate through positive rank-one
conditioning.  It controls the sectors in which all unselected sites
are symmetric.

For \(n=3\), (G2) on the singleton partition is exactly the desired
theorem.  For \(n=4\), all inequalities (G2), even together with
nonnegative swap-sector weights and the exact logical parity traces, do
not determine the endpoint sign.  The same certificate below also obeys
all four conditional inequalities (G2c).

Let \(p_R\) be formal two-replica sector weights indexed by
\(R\subseteq\{1,2,3,4\}\).  Set all undisplayed weights to zero and put
\[
\begin{array}{c|c}
R&p_R\\ \hline
\varnothing&21/16\\
\{2\}&1/16\\
\{1,2\},\{2,3\},\{2,4\}&1/4\\
\{1,3\},\{1,4\},\{3,4\}&5/16\\
\{1,2,3\},\{1,2,4\},\{2,3,4\}&11/48\\
\{1,3,4\}&1/4 .
\end{array}
\tag{G3}
\]
Every weight is nonnegative, and direct addition gives the necessary
rank-two parity traces
\[
\sum_{|R|\ {\rm even}}p_R=3,\qquad
\sum_{|R|\ {\rm odd}}p_R=1.
\tag{G4}
\]
Define the formal swap moments and Pauli shadows by the exact transforms
\[
A_T=\sum_R(-1)^{|R\cap T|}p_R,\qquad
L_T=2A_{\bar T}-A_T.
\tag{G5}
\]
Direct substitution in (G3) gives
\[
\begin{array}{c|c}
T&L_T\\ \hline
\varnothing&0\\
\{1\},\{3\},\{4\}&5/2\\
\{2\}&3\\
\{1,2\},\{2,3\},\{2,4\}&1\\
\{1,3\},\{1,4\},\{3,4\}&1/2\\
|T|=3&0\\
\{1,2,3,4\}&6 .
\end{array}
\tag{G6}
\]
These numbers obey every three-block inequality (G2).  This can be
checked without enumeration:

1. a \(4+0+0\) partition gives \(6\);
2. a \(3+1+0\) partition gives at most \(3\);
3. a \(2+2+0\) partition gives \(3/2\);
4. for a \(2+1+1\) partition, inspection of the six pair rows in (G6)
   gives a sum at most \(6\).

They also obey (G2c).  For the triples
\(\{1,2,3\},\{1,2,4\},\{2,3,4\}\), the two sides are respectively
\[
\frac{13}{16}\geq\frac{11}{16};
\]
for \(\{1,3,4\}\), they are
\[
\frac{15}{16}\geq\frac34.
\tag{G6a}
\]

Nevertheless the formal endpoint value is
\[
\begin{aligned}
Q_4^{\rm formal}
&=\frac1{16}\sum_R(-3)^{|R|}p_R\\
&=-\frac9{16}<0.
\end{aligned}
\tag{G7}
\]
Indeed the total weights at levels \(0,1,2,3,4\) are respectively
\[
\frac{21}{16},\quad\frac1{16},\quad\frac{27}{16},
\quad\frac{15}{16},\quad0,
\]
which verifies (G7) immediately.

The data (G3) are only a formal sector distribution; no code realizing
them is claimed.  Their role is exact and limited: an \(n=4\) proof
cannot be a nonnegative linear combination of sector positivity, parity
normalization, the grouped sign-frame inequalities (G2), and the
positive-conditioning inequalities (G2c).  Further tensor-square
realizability constraints are necessary.

There is a second, operator-level obstruction to a direct conditional
recursion.  Choose a basis on the last physical site and write a positive
rank-two operator in blocks \(H=(H_{rs})\).  If
\(\mathcal B_{n-1}(A,B)=
\langle A,\mathcal L^{\otimes(n-1)}(B)\rangle\), direct application of
\(\mathcal L(Z)=Z-\tfrac12\operatorname{Tr}(Z)I\) on the last site gives
\[
Q_n(H)=
\sum_{r,s}\mathcal B_{n-1}(H_{rs},H_{rs})
-\frac12\mathcal B_{n-1}
\left(\sum_rH_{rr},\sum_sH_{ss}\right).
\tag{G8}
\]
Every diagonal block \(H_{rr}\), and more generally every conditional
operator
\[
H_x=\sum_{r,s}\overline{x_r}x_sH_{rs},
\tag{G9}
\]
is positive semidefinite of rank at most two, so Theorem 4 applies to it
when three blocks remain.  But (G8) also contains the non-Hermitian
off-diagonal blocks \(H_{rs}\), \(r\ne s\), separately.  The sign
observable and trace-norm step use Hermiticity essentially and do not
control those terms.  This is the exact point at which positive
conditioning fails to close an induction.

## 5. Equality information and exact scope

The proof gives useful necessary conditions for equality.  If
\(Q_3(P)=0\), then equality must hold in every one of the six
permutation inequalities (15).  Moreover, every nonzero reduced encoded
Pauli \(X_{a,i}\) must have at most one positive and at most one negative
eigenvalue.  In particular its rank is at most two.  Equality also
requires the chosen sign-observable expectations to saturate the
anticommuting-contraction bound for every permutation.

These conditions include at least:

1. a logical qubit localized at one physical site;
2. the classical repetition code
   \(\operatorname{span}\{|000\rangle,|111\rangle\}\);
3. the factorized entangled family (28).

A complete classification of simultaneous equality in all six
anticommutation inequalities is not supplied here.

What is resolved is the sharp strong \(n=3\) endpoint inequality for
every positive semidefinite operator of rank at most two, in every local
dimension.  In particular, the rank-two projection problem is complete.
The argument does not prove positivity for a general rank-two
coefficient matrix \(C\), because its two left and two right singular
frames need not coincide and the reduced cross operators are not
Hermitian.  It also does not tensorize to arbitrary copy number: only
three mutually anticommuting logical Pauli directions are available,
exactly matching the three blocks in Theorems 1 and 4.  The formal
certificate (G3)--(G7) and the block identity (G8) isolate the two
corresponding four-site obstructions.
