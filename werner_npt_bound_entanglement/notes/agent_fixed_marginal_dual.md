# Fixed-reference-marginal dual and the sharp three-site correlation bound

Checkpoint: 2026-07-28 12:32 PDT.

This note studies the three-site logical-Pauli inequality through the
fixed-reference-marginal variational problem.  The main result is stronger
than the pure code inequality: it holds for every mixed state whose reference
qubit is maximally mixed.  No assumption on the dimensions of the three
physical systems is needed.

## 1. Setup and normalization

Let \(K=\mathbb C^2\), let \(A=A_1A_2A_3\), and let
\[
 {\cal F}=\left\{\rho_{KA}\succeq0:
       \operatorname{Tr}_A\rho_{KA}=I_K/2\right\}.
\]
The trace condition is automatic from the marginal constraint.  Write
\(\sigma_1,\sigma_2,\sigma_3\) for the Pauli matrices.  Transposes below are
only a vectorization convention; in particular,
\(\sigma_2^T=-\sigma_2\), which does not change any norm or
anticommutation relation.

For \(\rho\in{\cal F}\), define the one-site correlation operators
\[
 C_{ai}(\rho)
 =
 \operatorname{Tr}_{K A_{\bar i}}
 \left[(\sigma_a^T\otimes I_A)\rho\right]
 \in {\cal B}(A_i).
 \tag{1}
\]
They are Hermitian, and
\[
 \operatorname{Tr}C_{ai}
 =
 \operatorname{Tr}(\rho_K\sigma_a^T)=0.
 \tag{2}
\]
For local Hermitian test matrices \(Y_{ia}\), put
\[
 H_Y=\sum_{i=1}^3\sum_{a=1}^3
          \sigma_a^T\otimes Y_{ia}^{(i)}.
 \tag{3}
\]
Then
\[
 \operatorname{Tr}(\rho H_Y)
 =\sum_{i,a}\operatorname{Tr}(C_{ai}Y_{ia}).
 \tag{4}
\]

The scalar part of every \(Y_{ia}\) is invisible on \({\cal F}\).  Thus
write
\[
 Y_{ia}^0=Y_{ia}-\frac{\operatorname{Tr}Y_{ia}}{\dim A_i}I_{A_i},
 \qquad
 N(Y)=\sum_{i,a}\|Y_{ia}^0\|_2^2.
 \tag{5}
\]

For a pure code isometry \(U:\mathbb C^2\to A\), let
\[
 |\Psi_U\rangle
 =\frac1{\sqrt2}\sum_{r=0}^1|r\rangle_K\,U|r\rangle_A.
 \tag{6}
\]
If
\[
 E_{ai}=\operatorname{Tr}_{A_{\bar i}}
              (U\sigma_aU^\dagger),
 \tag{7}
\]
then (up to the harmless Pauli transpose convention)
\[
 C_{ai}(|\Psi_U\rangle\langle\Psi_U|)=\frac12E_{ai}.
 \tag{8}
\]
Consequently the desired code inequality
\[
 \sum_{i,a}\|E_{ai}\|_2^2\le 6
 \tag{9}
\]
is the same as
\[
 \sum_{i,a}\|C_{ai}\|_2^2\le\frac32.
 \tag{10}
\]

## 2. Exact fixed-marginal SDP and quotient norm

For an arbitrary Hermitian \(H\) on \(K\otimes A\), define
\[
 h_{\rm fm}(H)
 =
 \max_{\rho\in{\cal F}}\operatorname{Tr}(\rho H).
 \tag{11}
\]

### Proposition 1 (exact SDP dual)

\[
 h_{\rm fm}(H)
 =
 \min_{Z=Z^\dagger}
 \left\{\frac12\operatorname{Tr}Z:
       Z\otimes I_A\succeq H\right\}.
 \tag{12}
\]
Equivalently,
\[
 h_{\rm fm}(H)
 =
 \min_{\boldsymbol z\in\mathbb R^3}
 \lambda_{\max}\!\left(
 H-\boldsymbol z\mathbin{\cdot}\boldsymbol\sigma^T\otimes I_A
 \right).
 \tag{13}
\]

#### Proof

Introduce a Hermitian multiplier \(Z\) for
\(\operatorname{Tr}_A\rho=I/2\).  The Lagrangian is
\[
 \begin{aligned}
 L(\rho,Z)
 &=\operatorname{Tr}(\rho H)
   +\operatorname{Tr}\left[
       Z\left(I/2-\operatorname{Tr}_A\rho\right)\right]\\
 &=\frac12\operatorname{Tr}Z
   +\operatorname{Tr}\left[
       \rho(H-Z\otimes I_A)\right].
 \end{aligned}
 \]
Its supremum over \(\rho\succeq0\) is finite precisely when
\(Z\otimes I_A\succeq H\), and is then
\(\operatorname{Tr}Z/2\).  The primal has a strictly positive feasible
point, for example \(I_K/2\otimes\tau_A\) with \(\tau_A\succ0\), and the
dual is strictly feasible after taking \(Z=tI_K\) with sufficiently large
\(t\).  Hence finite-dimensional SDP duality gives equality and attainment.

Write \(Z=tI_K+\boldsymbol z\cdot\boldsymbol\sigma^T\).  Since
\(\operatorname{Tr}Z/2=t\), the least admissible \(t\) for fixed
\(\boldsymbol z\) is the largest eigenvalue in (13).  Minimizing over
\(\boldsymbol z\) proves (13). \(\square\)

Formula (13) is a quotient norm: arbitrary logical Pauli fields
\(\boldsymbol z\cdot\boldsymbol\sigma\) may be shifted away because their
expectation is fixed to zero by \(\rho_K=I/2\).

### Pure fixed-marginal states are not the whole SDP

A pure member of \({\cal F}\) is exactly a state (6), hence exactly a pair
of orthonormal code columns.  The mixed feasible set in (11), however, is
larger than the convex hull of such pure states.  Thus “fixed marginal” and
“orthonormal code columns” are equivalent only after explicitly imposing
purity.

Here is an exact example.  Embed one output qubit \(Q\) in \(A_1\), keep all
other factors fixed, and set
\[
 |\psi_0\rangle=\frac1{\sqrt2}|0_K0_Q\rangle
                  +\frac12|1_K1_Q\rangle,
 \qquad
 |\psi_1\rangle=\frac12|1_K0_Q\rangle,
 \tag{14}
\]
\[
 \rho=|\psi_0\rangle\langle\psi_0|
      +|\psi_1\rangle\langle\psi_1|.
 \tag{15}
\]
Then \(\operatorname{Tr}_Q\rho=I_K/2\).  A vector in the support of
\(\rho\) has the form \(a\psi_0+b\psi_1\).  Its two diagonal \(K\)-weights
are equal only if \(|a|=|b|\), whereas its off-diagonal \(K\)-entry
vanishes only if \(a^*b=0\).  No nonzero vector in the support therefore
has \(K\)-marginal \(I/2\).  Since every vector in a positive rank-one
decomposition of \(\rho\) must lie in its support, (15) cannot be a convex
combination of pure members of \({\cal F}\).

The exact pure-code support function is instead the nonconvex variational
quantity
\[
 h_{\rm iso}(H)
 =
 \max_{U^\dagger U=I_2}
 \langle\Psi_U|H|\Psi_U\rangle,
 \qquad
 h_{\rm iso}(H)\le h_{\rm fm}(H).
 \tag{16}
\]
The sharp estimate below holds on the larger SDP set, so this relaxation
gap causes no loss for the Frobenius bound.

## 3. Two elementary lemmas

### Lemma 2 (anticommuting expectation bound)

Let \(O_1,\ldots,O_m\) be Hermitian operators satisfying
\[
 O_iO_j+O_jO_i=0\quad(i\ne j),
 \qquad O_i^2\preceq I.
 \tag{17}
\]
For every state \(\rho\),
\[
 \sum_{i=1}^m\bigl(\operatorname{Tr}\rho O_i\bigr)^2\le1.
 \tag{18}
\]

#### Proof

Put \(c_i=\operatorname{Tr}\rho O_i\), \(s=\sum_i c_i^2\), and
\(L=\sum_i c_iO_i\).  Anticommutation gives
\[
 L^2=\sum_i c_i^2O_i^2\preceq sI.
 \]
On the other hand \(\operatorname{Tr}\rho L=s\).  Cauchy--Schwarz in the
state \(\rho\) gives
\[
 s^2=(\operatorname{Tr}\rho L)^2
 \le\operatorname{Tr}(\rho L^2)\le s.
 \]
Thus \(s\le1\). \(\square\)

### Lemma 3 (trace norm controls Frobenius norm)

For every Hermitian \(X\),
\[
 2\|X\|_2^2
 \le \|X\|_1^2+(\operatorname{Tr}X)^2.
 \tag{19}
\]
In particular, if \(\operatorname{Tr}X=0\), then
\[
 2\|X\|_2^2\le\|X\|_1^2.
 \tag{20}
\]

#### Proof

Let \(p\) be the sum of the positive eigenvalues of \(X\), and let \(q\)
be the absolute sum of its negative eigenvalues.  Then
\[
 \|X\|_1=p+q,\qquad \operatorname{Tr}X=p-q.
 \]
The sum of the squares of the positive eigenvalues is at most \(p^2\),
and the analogous negative sum is at most \(q^2\).  Hence
\[
 2\|X\|_2^2\le2(p^2+q^2)
 =(p+q)^2+(p-q)^2.
 \]
This is (19), and (20) follows immediately. \(\square\)

Equality in (20) requires at most one nonzero positive eigenvalue and at
most one nonzero negative eigenvalue.  For traceless \(X\), this means that
the nonzero spectrum is \(\{s,-s\}\).

## 4. Sharp three-site theorem

### Theorem 4 (dimension-free fixed-marginal correlation bound)

For arbitrary finite-dimensional \(A_1,A_2,A_3\) and every
\(\rho\in{\cal F}\),
\[
 \boxed{\displaystyle
 \sum_{i=1}^3\sum_{a=1}^3
       \|C_{ai}(\rho)\|_2^2\le\frac32.}
 \tag{21}
\]
The constant \(3/2\) is sharp.  Consequently every pure rank-two code
obeys (9).

#### Proof

For a Hermitian matrix \(X\), let \(\operatorname{sgn}X\) be \(+1\) on
its positive eigenspace, \(-1\) on its negative eigenspace, and \(0\) on
its kernel.  Thus
\[
 G=\operatorname{sgn}X=G^\dagger,\qquad G^2\preceq I,\qquad
 \operatorname{Tr}(XG)=\|X\|_1.
 \tag{22}
\]

Fix a permutation \(\pi\) of the three Pauli axes.  On \(K A_1A_2A_3\)
define
\[
 O_i=
 \sigma_{\pi(i)}^T\otimes
 \bigl(\operatorname{sgn}C_{\pi(i),i}\bigr)^{(i)},
 \qquad i=1,2,3.
 \tag{23}
\]
The physical sign operators in two different \(O_i\)'s commute because
they act on different sites.  The distinct Pauli matrices anticommute.
Therefore the three \(O_i\)'s anticommute pairwise, and \(O_i^2\preceq I\).
Moreover, by (1) and (22),
\[
 \operatorname{Tr}(\rho O_i)
 =\operatorname{Tr}\!\left[
 C_{\pi(i),i}\operatorname{sgn}C_{\pi(i),i}\right]
 =\|C_{\pi(i),i}\|_1.
 \]
Lemma 2 gives, for every \(\pi\in S_3\),
\[
 \sum_{i=1}^3\|C_{\pi(i),i}\|_1^2\le1.
 \tag{24}
\]
Sum (24) over all six permutations.  Each ordered pair \((a,i)\) occurs
in exactly two permutations, so
\[
 \sum_{i,a}\|C_{ai}\|_1^2\le3.
 \tag{25}
\]
Every \(C_{ai}\) is traceless by (2).  Applying (20) termwise to (25)
proves
\[
 2\sum_{i,a}\|C_{ai}\|_2^2
 \le\sum_{i,a}\|C_{ai}\|_1^2\le3.
 \]
This is (21).  Finally, (8) gives (9). \(\square\)

### Sharpness and equality mechanisms

There are at least two inequivalent equality mechanisms.

1. **Localized quantum information.**  Let \(K\) be maximally entangled
   with a two-dimensional subspace of \(A_1\), and let \(A_2,A_3\) be
   fixed.  Then \(C_{a1}=\sigma_a/2\) in that subspace and all other
   \(C_{ai}\)'s vanish.  Hence the left side of (21) is
   \(3\operatorname{Tr}(\sigma_a^2)/4=3/2\).

2. **Classical repetition.**  Take
   \[
   |\Psi\rangle=
   \frac{|0\rangle_K|000\rangle_A+
         |1\rangle_K|111\rangle_A}{\sqrt2}.
   \]
   For each site,
   \(C_{3i}=(|0\rangle\langle0|-|1\rangle\langle1|)/2\), while the two
   transverse correlations vanish.  The three nonzero squared Frobenius
   norms are each \(1/2\).

The proof also gives necessary equality conditions.  Every nonzero
\(C_{ai}\) must have nonzero spectrum \(\{s,-s\}\), and all six
anticommuting-observable inequalities (24) must be saturated.  A complete
classification of all equality states was not needed here and has not
been derived.

## 5. Sharp Frobenius dual bound

### Corollary 5

For \(H_Y\) in (3),
\[
 \boxed{\displaystyle
 h_{\rm fm}(H_Y)\le\sqrt{\frac32\,N(Y)}.}
 \tag{26}
\]
The constant is sharp, even when the optimization is restricted to pure
orthonormal-column code states.

#### Proof

Equations (4), (5), Cauchy--Schwarz, and Theorem 4 give
\[
 \operatorname{Tr}(\rho H_Y)
 \le
 \left(\sum_{i,a}\|C_{ai}\|_2^2\right)^{1/2}
 \left(\sum_{i,a}\|Y_{ia}^0\|_2^2\right)^{1/2}
 \le\sqrt{\frac32N(Y)}.
 \]
Take the supremum over \(\rho\in{\cal F}\).  Either equality example above,
with \(Y_{ia}^0\) proportional to \(C_{ai}\), attains equality. \(\square\)

Combining (13) and (26) gives the exact quotient-norm inequality
\[
 \min_{\boldsymbol z\in\mathbb R^3}
 \lambda_{\max}\!\left(
 H_Y-\boldsymbol z\cdot\boldsymbol\sigma^T\otimes I_A
 \right)
 \le\sqrt{\frac32N(Y)}.
 \tag{27}
\]

There is also an exact quadratic variational identity.  For a pure code
state and \(E_{ai}=2C_{ai}\),
\[
 \sum_{i,a}\|E_{ai}\|_2^2
 =
 \sup_{\{Y_{ia}^0\}}
 \left\{
 4\langle\Psi_U|H_Y|\Psi_U\rangle-N(Y)
 \right\}.
 \tag{28}
\]
Thus (9), (26), and the homogeneous support estimate
\[
 h_{\rm iso}(H_Y)\le\sqrt{\frac32N(Y)}
 \tag{29}
\]
are equivalent at the sharp constant.

### Why the unrestricted operator norm is the wrong quantity

Let
\[
 D=\frac1{\sqrt3}\operatorname{diag}(2,-1,-1),
 \qquad \|D\|_2^2=2,
 \]
and take \(Y_{i3}=D\) for all three sites, with every other \(Y_{ia}=0\).
Then \(N(Y)=6\), and
\[
 H_Y=\sigma_3\otimes B,\qquad
 B=D^{(1)}+D^{(2)}+D^{(3)}.
 \]
The extremal eigenvalues of \(B\) are \(2\sqrt3\) and \(-\sqrt3\).  Hence
\[
 \|H_Y\|_\infty=2\sqrt3>3=\sqrt{\frac32N(Y)}.
 \tag{30}
\]
The unshifted operator norm therefore fails at the sharp constant.

By contrast, the quotient in (13) centers the spectrum:
\[
 \min_z\lambda_{\max}\bigl(\sigma_3\otimes(B-zI)\bigr)
 =\frac{\lambda_{\max}B-\lambda_{\min}B}{2}
 =\frac{3\sqrt3}{2}<3.
 \tag{31}
\]
This is precisely the removal of an inadmissible polarized-\(K\)
contribution.

## 6. Grouped three-block inequalities do not generate the higher-copy
singleton functional

This is a separate exact cone test prompted by the three-block theorem.
It records an obstruction, not a realizable rank-two counterexample.

For a rank-two projection \(P\) on \(n\) tensor factors, define local swap
parity weights
\[
 r_T=\operatorname{Tr}\left[(P\otimes P)\Pi_T\right]\ge0,
\]
where \(\Pi_T\) is antisymmetric on the sites in \(T\) and symmetric on
the remaining sites.  The code symmetric square has dimension \(3\), and
the code exterior square has dimension \(1\), so
\[
 \sum_{|T|\ {\rm even}}r_T=3,\qquad
 \sum_{|T|\ {\rm odd}}r_T=1.
 \tag{32}
\]

For a partition \(\pi\) of the sites into \(k\) superblocks,
\[
 Q_\pi
 =
 \operatorname{Tr}\left[
 (P\otimes P)\prod_{B\in\pi}
 \left(\prod_{i\in B}F_i-\frac12I\right)\right]
 =
 \sum_T 2^{-k}(-3)^{o_\pi(T)}r_T,
 \tag{33}
\]
where \(o_\pi(T)\) is the number of blocks meeting \(T\) in odd
cardinality.  The exact three-block theorem gives \(Q_\pi\ge0\) for
\(|\pi|\le3\).

The following symmetric nonnegative parity tables satisfy (32) and every
grouped inequality, but make the singleton functional negative.  Thus the
singleton functional is not in the cone generated by the grouped
one-, two-, and three-block inequalities, even after adjoining coordinate
nonnegativity and the mass equality (32).

### Four sites

Let \(r_T=c_{|T|}\), with
\[
 (c_0,c_1,c_2,c_3,c_4)
 =
 \left(\frac65,0,\frac3{10},\frac14,0\right).
 \tag{34}
\]
The total masses at weights \(0,\ldots,4\) are
\[
 (R_0,R_1,R_2,R_3,R_4)
 =
 \left(\frac65,0,\frac95,1,0\right).
 \]
For the three nontrivial block-size types,
\[
 Q_{(1,3)}=\frac95,\qquad
 Q_{(2,2)}=\frac{12}{5},\qquad
 Q_{(1,1,2)}=0.
 \tag{35}
\]
Nevertheless,
\[
 Q_{\rm singleton}
 =
 \sum_{t=0}^4 2^{-4}(-3)^tR_t
 =-\frac35.
 \tag{36}
\]

### Five sites

Let
\[
 (c_0,c_1,c_2,c_3,c_4,c_5)
 =
 \left(0,\frac3{50},\frac3{10},0,0,\frac7{10}\right).
 \tag{37}
\]
The weight totals are
\[
 (R_0,\ldots,R_5)
 =
 \left(0,\frac3{10},3,0,0,\frac7{10}\right).
 \]
The four nontrivial grouped types give
\[
 \begin{array}{c|cccc}
 \text{type}&(1,4)&(2,3)&(1,1,3)&(1,2,2)\\ \hline
 Q_\pi&12/5&18/5&0&12/5,
 \end{array}
 \tag{38}
\]
whereas
\[
 Q_{\rm singleton}
 =
 \sum_{t=0}^5 2^{-5}(-3)^tR_t
 =-\frac92.
 \tag{39}
\]

These tables are abstract points of the parity linear relaxation.  No
claim is made that either table is realizable by an actual rank-two
projection.  They prove that any higher-copy argument using grouped
three-block inequalities must also exploit nonlinear realizability
constraints on the parity weights.

## 7. Discovery and verification log

- Numerical Stiefel searches over real and complex Stinespring isometries,
  including environment ranks \(1,2,3\), repeatedly reached \(6\) and
  never exceeded it.  These computations were used only for conjecture
  selection.
- A proposed standalone overlap inequality between the two orthogonal
  Stinespring columns was numerically false.  The missing compensation is
  exactly the local mixedness term; this route was discarded.
- The decisive observation was to choose the test observable
  state-dependently as \(\operatorname{sgn}C_{ai}\), assign the three
  distinct Pauli axes bijectively to the three physical sites, and use
  anticommutation.  This gives an exact proof with no optimization or
  dimension-dependent estimate.
- Exact rational arithmetic was used to obtain (34)--(39).  These
  certificates can be checked using only the formula (33), binomial
  multiplicities, and fraction arithmetic.
- No additional hardware would materially improve this proof or its
  verification.

## 8. What this resolves

This note proves, exactly:

1. the fixed-marginal SDP dual and quotient formula (12)--(13);
2. the sharp mixed-state three-site Frobenius bound (21);
3. the sharp dual norm inequality (26)--(27);
4. the pure-code logical-Pauli marginal inequality (9), in every local
   dimension;
5. the failure of the grouped-\(\le3\)-block linear cone to imply the
   singleton \(n=4\) or \(n=5\) functional.

It does **not** by itself prove an all-copy Werner theorem.  In particular,
the parity tables in Section 6 are not physical counterexamples, and the
remaining higher-copy problem is to identify and use the nonlinear
rank-two realizability constraints that exclude such abstract tables, or
to realize a genuinely negative one.
