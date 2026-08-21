# A degree-four invariant-SOS obstruction at four copies

## Checkpoint

**2026-07-28 18:05 PDT.**  This note studies the actual four-copy
rank-two projection target
\[
 {\cal Q}(P)=e_2-3e_3+10e_4\stackrel{?}{\geq}0.
\tag{1}
\]
It does not prove or refute (1).  It gives two exact reductions and one
no-go theorem:

1. (1) is a single coefficient-\(10\) global Pluecker norm inequality;
2. an individual decomposable Hodge orbit can still have a negative
   coefficient-\(10\) contribution inside an exact zero code;
3. no sum of squared quadratic covariants, even modulo all degree-four
   affine identities of rank-two qutrit code isometries, can prove (1).

The third statement is stronger than observing that the displayed
sector coefficients have a negative entry.  The exact verifier exhibits
sixteen sparse code isometries whose sector vectors have the maximum
affine dimension permitted by the two logical-parity identities.  Thus
there is no unrecorded affine Pluecker identity at this degree which can
change the conclusion.

## 1. The exact coefficient-\(10\) Pluecker inequality

Let \(u,v\in(\mathbb C^3)^{\otimes4}\) be orthonormal and
\[
 P=|u\rangle\langle u|+|v\rangle\langle v|.
\]
On two replicas put \(A_i=(I-F_i)/2\).  For \(i<j\), define
\[
\begin{aligned}
 q_{ij}(x)&=2A_iA_j(x\otimes x),\\
 s_{ij}(u,v)&=A_iA_j(u\otimes v+v\otimes u),\\
 r_{ij}(u,v)&=A_iA_j(u\otimes v-v\otimes u),
\end{aligned}
\tag{2}
\]
and take the orthogonal direct sums over the six physical pairs:
\[
 q(x)=\bigoplus_{i<j}q_{ij}(x),\qquad
 s=\bigoplus_{i<j}s_{ij},\qquad
 r=\bigoplus_{i<j}r_{ij}.
\tag{3}
\]
Finally let
\[
 e_4=\operatorname{Tr}[(P\otimes P)A_1A_2A_3A_4].
\tag{4}
\]

### Proposition 1

The four-copy target (1) is equivalent to
\[
\boxed{\quad
 \|r\|^2\leq
 \|s\|^2+\frac{\|q(u)\|^2+\|q(v)\|^2}{2}+8e_4.
 \quad}
\tag{5}
\]

#### Proof

Let
\[
 {\cal B}(H)=
 6\operatorname{Tr}H^2+
 \sum_{|S|=2}\|\operatorname{Tr}_S H\|_2^2
 -3\sum_{|S|=1}\|\operatorname{Tr}_S H\|_2^2.
\tag{6}
\]
Direct two-replica polarization gives
\[
 {\cal B}(P)
 =\|q(u)\|^2+\|q(v)\|^2
  +2\|s\|^2-2\|r\|^2.
\tag{7}
\]
On the other hand, the swap-sector calculation gives
\[
 {\cal B}(P)=4(e_2-3e_3+6e_4).
\tag{8}
\]
Consequently
\[
 4{\cal Q}(P)
 ={\cal B}(P)+16e_4.
\tag{9}
\]
Substitution of (7) in (9), followed by division by two, proves the
equivalence with (5). \(\square\)

Compared with the stronger homogeneous Pluecker conjecture, the actual
projection problem has precisely one additional compensation channel:
\(8e_4\).

There is a second useful form.  Write \(q_{ij}\) for the mass in the
two-site sector, \(r_\ell\) for the mass in the three-site sector
\([4]\setminus\{\ell\}\), and
\[
 u_\ell=\sum_{j\ne\ell}q_{\ell j}.
\]
The four conditioned three-party slacks are
\[
 C_\ell=e_2-u_\ell-3r_\ell\geq0.
\tag{10}
\]
Since every pair is incident to two sites,
\[
 \sum_\ell C_\ell=2e_2-3e_3.
\tag{11}
\]
Thus (1) is also exactly
\[
\boxed{\quad e_2\leq\sum_{\ell=1}^4C_\ell+10e_4.\quad}
\tag{12}
\]
This formulation shows what a coefficient-\(10\) SOS must accomplish:
it must control the reuse of every pair sector in two different
conditioned three-party inequalities.

## 2. A decomposable orbit remains negative

The additional \(e_4\) term does not make the target nonnegative
orbit-by-orbit.  Take
\[
\begin{aligned}
 u&=\frac{|0000\rangle+|0110\rangle}{\sqrt2},\\
 v&=\frac{|1000\rangle+|1110\rangle}{\sqrt2}.
\end{aligned}
\tag{13}
\]
This is the three-party logical-flag/Bell equality code with a common
fourth-site product factor.

In the full-difference orbit on the first three sites, the only
nonzero target sectors have masses
\[
 p_{\{2,3\}}^{\cal O}=\frac14,\qquad
 p_{\{1,2,3\}}^{\cal O}=\frac14.
\tag{14}
\]
The fourth site is symmetric, so the orbit has no four-site mass.
Its contribution to (1) is therefore
\[
 \frac14-3\frac14=-\frac12.
\tag{15}
\]
The complete code nevertheless has
\[
 e_2=\frac34,\qquad e_3=\frac14,\qquad e_4=0,
\qquad {\cal Q}(P)=0.
\tag{16}
\]
Hence a valid SOS must mix different unordered-pair/Hodge orbits.
The common decomposable bivector does not permit an orbitwise
coefficient-\(10\) injection.

## 3. Multiplicity-free quadratic covariants

Let
\[
 V_i=\mathbb C^3,\qquad K=\mathbb C^2,\qquad
 U:K\longrightarrow V_1\otimes\cdots\otimes V_4
\]
be a code isometry.  Regard \(U\otimes U\) as a quadratic covariant.
For \(R\subseteq[4]\), its physical local-swap component lies in
\[
 W_R=
 \bigotimes_{i\notin R}\operatorname{Sym}^2V_i
 \otimes
 \bigotimes_{i\in R}\Lambda^2V_i.
\tag{17}
\]
The total physical swap equals the logical swap.  Hence the logical
factor is \(\operatorname{Sym}^2K^*\) when \(|R|\) is even and
\(\Lambda^2K^*\) when \(|R|\) is odd.  Its squared norm is exactly
\[
 p_R=\operatorname{Tr}[(P\otimes P)\Pi_R].
\tag{18}
\]

The representations (17) are pairwise inequivalent under the
independent local group
\[
 G=U(3)^4.
\]
Indeed, at the first site where \(R\) and \(R'\) differ, one
representation contains \(\operatorname{Sym}^2V_i\) and the other
contains \(\Lambda^2V_i\), which have different dimensions and
different diagonal-torus weights.  Both local representations are
irreducible: their standard symmetric and alternating tensor bases are
connected by elementary two-coordinate unitaries.  Tensor products over
independent group factors remain irreducible.

It follows directly, without naming an external result, that a
\(G\times U(2)\)-invariant Hermitian quadratic form on the quadratic
covariants is
\[
 \sum_{R\subseteq[4]}\lambda_Rp_R.
\tag{19}
\]
To see this, average any Gram matrix over diagonal local unitaries.
Different torus weights become orthogonal.  Averaging next over
two-coordinate rotations makes the coefficient constant on every
irreducible block \(W_R\), while inequivalent blocks cannot mix.
If the Gram matrix is positive semidefinite, then
\[
 \lambda_R\geq0\quad\text{for every }R.
\tag{20}
\]
Permutation invariance merely makes \(\lambda_R\) depend on \(|R|\);
it supplies no new cross-sector Gram entries.

Thus every sum of squared holomorphic quadratic covariants, after
averaging over the symmetries of the target, is a nonnegative sector
combination.  The only possible escape at degree four is to use
identities imposed by the isometry equations.  The next section
exhausts those affine identities exactly.

## 4. Exact affine span of physical rank-two codes

Every rank-two code obeys
\[
 \sum_{|R|\ {\rm even}}p_R=3,\qquad
 \sum_{|R|\ {\rm odd}}p_R=1.
\tag{21}
\]
These are the squared norms of the three-dimensional logical symmetric
square and the one-dimensional logical exterior line.

### Proposition 2

For four qutrits, (21) span all affine linear identities among the
sixteen functions \(p_R\) on rank-two code isometries.

#### Proof

The two equations in (21) show that the affine dimension is at most
\(14\).  The verifier accompanying this note constructs sixteen
explicit sparse code isometries.  In each code the two columns have
disjoint computational-basis supports and coefficients \(\pm1/\sqrt k\),
so orthonormality is exact.  It computes every \(p_R\) by the rational
Walsh transform
\[
 p_R=\frac1{16}\sum_{T\subseteq[4]}
 (-1)^{|R\cap T|}
 \left\|\operatorname{Tr}_{\bar T}P\right\|_2^2.
\tag{22}
\]
Gaussian elimination over the rational numbers gives rank \(15\) for
the fifteen augmented rows
\[
 (p_R)_{R\subseteq[4]}\oplus(1).
\tag{23}
\]
Their affine span therefore has dimension \(14\).  Since (21) already
gives codimension two, no further affine identity exists. \(\square\)

The certificate is finite, deterministic, and uses only integer and
rational arithmetic.  No numerical rank decision is involved.

## 5. No invariant quadratic SOS modulo the isometry identities

### Theorem 3

There is no identity on rank-two four-qutrit code isometries of the form
\[
 {\cal Q}(P)=c+\sum_j\|F_j(U,U)\|^2,
\qquad c\geq0,
\tag{24}
\]
where the \(F_j\) are homogeneous quadratic covariants.  The conclusion
continues to hold if arbitrary degree-four multiples of the isometry
constraints are allowed before restricting to the Stiefel manifold.

#### Proof

Average a proposed positive Gram matrix over local unitaries, logical
unitaries, and physical permutations.  Positivity is preserved.
Section 3 then turns the squared part of (24) into
\[
 \sum_R\lambda_Rp_R,\qquad \lambda_R\geq0.
\tag{25}
\]
By Proposition 2, equality with the target on every isometry can differ
only by the two identities (21).  Hence there are real
\(\alpha,\beta\) such that
\[
 w_R-\lambda_R=
\begin{cases}
\alpha,&|R|\ {\rm even},\\
\beta,&|R|\ {\rm odd},
\end{cases}
\qquad
c=3\alpha+\beta,
\tag{26}
\]
where the target coefficients are
\[
 (w_0,w_1,w_2,w_3,w_4)=(0,0,1,-3,10).
\tag{27}
\]
Nonnegativity of the weight-zero squared coefficient gives
\[
 \lambda_\varnothing=-\alpha\geq0,
\qquad\text{so }\alpha\leq0.
\tag{28}
\]
Nonnegativity of a weight-three squared coefficient gives
\[
 \lambda_R=-3-\beta\geq0,
\qquad\text{so }\beta\leq-3.
\tag{29}
\]
Equations (26), (28), and (29) imply
\[
 c=3\alpha+\beta\leq-3,
\tag{30}
\]
contradicting \(c\geq0\).

An invariant degree-four multiplier of the isometry constraints
restricts to an affine linear identity among the invariant functions
\(p_R\).  Proposition 2 says that every such identity is already a
combination of (21), which is exactly the freedom represented by
\(\alpha,\beta\) in (26).  Thus allowing those multipliers does not
alter the contradiction. \(\square\)

## 6. Consequences and exact scope

Theorem 3 does **not** show that (1) is false.  It shows that the most
natural fixed Gram/SOS proof is impossible even after using every
degree-four affine consequence of the rank-two isometry equations.

A successful proof must therefore use at least one of:

1. higher-degree consequences of decomposability and then divide or
   cancel using normalization;
2. a state-dependent nonlinear Gram matrix, such as adaptive sign
   observables;
3. an inequality rather than a polynomial identity;
4. cross-orbit Hermitian Pluecker products whose positivity is obtained
   only after a nonlinear common-code estimate.

The coefficient \(10\) does provide the explicit \(8e_4\) compensation
in (5), but (13)--(16) show that it cannot repair the deficit locally in
each Hodge orbit.  The unresolved mathematical statement remains the
global inequality (5), or equivalently (12).
