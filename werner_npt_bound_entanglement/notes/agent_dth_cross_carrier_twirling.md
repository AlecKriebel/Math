# Exact local-unitary reduction of the corrected mixed-PPT DTH cone

## Status

This note resolves the symmetry part of the cross-carrier question for the
corrected first-degree DTH cone.  Averaging over the diagonal local-unitary
group is lossless: it preserves the holomorphic range equations, positivity,
partial-transpose positivity, the mixed support range equation, trace, and the
witness objective.  Consequently, coherences between inequivalent local
unitary types can always be removed.

Coherences between different multiplicity copies of the *same* local-unitary
type cannot be removed by this averaging.  They are the only cross-carrier
coherences that remain.  The complete first-degree decision is therefore an
exact coupled block semidefinite problem on multiplicity spaces.  The coupling
is a local partial-transpose crossing transform; it factors over the three
physical sites.

This is a lossless finite reduction of the corrected cone, not a sign
determination for that cone and not a proof of DTH.  In particular, the
seven-dimensional binary carrier of type
\([4,1]\otimes[4,1]\otimes[3,2]\) is a multiplicity carrier, not a full
local-unitary isotypic component.  Testing densities supported only on its
chosen highest-weight vectors does not test the invariant density on the
whole isotypic component.

The dependency-free checker is
`verification/agent_dth_cross_carrier_twirling.py`.

## 1. The two group actions

Put

\[
 V=(\mathbb C^3)^{\otimes3},\qquad A=\wedge^2V.
\]

Embed the holomorphic five-replica space in \(V^{\otimes5}\), with replicas
\((1,2)\) carrying the first bivector, replicas \((3,4)\) the second, and
replica \(5\) the vector.  For

\[
 g=g_1\otimes g_2\otimes g_3,\qquad g_i\in U(3),
\]

define

\[
 T(g)=g^{\otimes5}.
\tag{1}
\]

After transposing the first bivector slot, the mixed action is

\[
 \widehat T(g)=\bar g^{\otimes2}\otimes g^{\otimes3}
\tag{2}
\]

on \(\bar A\otimes A\otimes V\).  If \(\Theta_1\) denotes partial
transpose on replicas \(1,2\), then direct substitution in matrix entries
gives

\[
 \boxed{
 \Theta_1\!\left(T(g)RT(g)^\dagger\right)
 =\widehat T(g)\Theta_1(R)\widehat T(g)^\dagger.
 }
\tag{3}
\]

No representation theorem is needed for (3): on an elementary operator
\(|a\otimes q\rangle\langle b\otimes r|\), partial transpose replaces the
first factor by
\(|\bar b\rangle\langle\bar a|\), and the two sides coincide.

The exact covariance results already established for the constraint maps can
be summarized as follows.  There are unitary target representations such
that

\[
 \begin{aligned}
 \mathcal A_4T(g)&=T_4(g)\mathcal A_4,\\
 \mathcal C_\Omega T(g)&=T_\Omega(g)\mathcal C_\Omega,\\
 \mathcal C_{\rm supp}\widehat T(g)
   &=T_{\rm supp}(g)\mathcal C_{\rm supp}.
 \end{aligned}
\tag{4}
\]

For the Omega map, \(T_\Omega(g)\) contains the scalar character
\(\prod_i\det g_i\); this does not affect its kernel.  The witness
\(\widetilde{\mathcal O}_0\) is made from local replica swaps and hence
commutes with every \(T(g)\).  It follows from (4) that both
\(\mathscr K_{\rm hol}\) and
\(L=\ker\mathcal C_{\rm supp}\) are invariant.

## 2. Lossless twirling theorem

Let \(G=U(3)^3\), with normalized invariant measure, and define

\[
 \mathbb E_G(R)=\int_GT(g)RT(g)^\dagger\,dg.
\tag{5}
\]

The integral in (5) means entrywise integration of continuous functions on
the compact finite-dimensional group.  Only linearity, positivity of an
average, and invariance under a change of integration variable are used.

### Theorem 2.1

If \(\rho\) is feasible for the corrected cone \(\mathfrak C_1\), then
\(\bar\rho=\mathbb E_G(\rho)\) is feasible and

\[
 \operatorname{Tr}\bar\rho=\operatorname{Tr}\rho,
 \qquad
 \operatorname{Tr}(\widetilde{\mathcal O}_0\bar\rho)
 =\operatorname{Tr}(\widetilde{\mathcal O}_0\rho).
\tag{6}
\]

Consequently the minimum of the corrected first-degree problem is attained
by a \(G\)-invariant density operator.

### Proof

Every conjugate \(T(g)\rho T(g)^\dagger\) is positive, so its average is
positive.  Equation (3) gives

\[
 \bar\rho^{\Gamma_1}
 =\int_G\widehat T(g)\rho^{\Gamma_1}widehat T(g)^\dagger\,dg\succeq0.
\]

Because the holomorphic constraint space is invariant, its orthogonal
projector commutes with \(T(g)\), so the holomorphic range condition is
preserved.  If
\(\mathcal C_{\rm supp}\rho^{\Gamma_1}=0\), then (4) gives

\[
 \mathcal C_{\rm supp}
 \widehat T(g)\rho^{\Gamma_1}\widehat T(g)^\dagger=0
\]

for every \(g\), and hence for the average.  Trace is unchanged by unitary
conjugation.  Finally, commutation of the witness with \(T(g)\) and cyclicity
of trace prove the objective identity in (6).  Invariance of the average
follows by changing \(g\) to \(hg\) in (5).  \(\square\)

The same proof permits a second average over permutations of the three
physical sites.  Thus site-permuted local-type triples may also be identified.

## 3. What twirling does and does not remove

Choose unitary decompositions of the two five-slot representations into
inequivalent local-unitary types:

\[
 \begin{aligned}
 \mathscr B&=\bigoplus_{\boldsymbol\lambda}
 R_{\boldsymbol\lambda}\otimes M_{\boldsymbol\lambda},\\
 \widehat{\mathscr B}&=\bigoplus_{\boldsymbol\mu}
 \widehat R_{\boldsymbol\mu}\otimes N_{\boldsymbol\mu}.
 \end{aligned}
\tag{7}
\]

Here a bold index is a triple, one type for each physical site.  The first
factor in each summand is irreducible for \(G\), and the second is its
multiplicity space.  A direct matrix-unit argument proves that an operator
commuting with \(G\) has the form

\[
 \bigoplus_{\boldsymbol\lambda}
 I_{R_{\boldsymbol\lambda}}\otimes X_{\boldsymbol\lambda}.
\tag{8}
\]

Indeed, independent diagonal phase rotations kill maps between inequivalent
weight spaces; the raising and lowering matrix units then make the operator
scalar on each irreducible factor, while they do not act on multiplicity
indices.  This is also the elementary proof that no group average can erase
an arbitrary entry of \(X_{\boldsymbol\lambda}\): the group acts as the
identity on that factor.

Since the two constraint spaces are invariant, there are subspaces

\[
 K_{\boldsymbol\lambda}\subseteq M_{\boldsymbol\lambda},
 \qquad
 L_{\boldsymbol\mu}\subseteq N_{\boldsymbol\mu}
\tag{9}
\]

such that

\[
 \begin{aligned}
 \mathscr K_{\rm hol}
 &=\bigoplus_{\boldsymbol\lambda}
 R_{\boldsymbol\lambda}\otimes K_{\boldsymbol\lambda},\\
 L
 &=\bigoplus_{\boldsymbol\mu}
 \widehat R_{\boldsymbol\mu}\otimes L_{\boldsymbol\mu}.
 \end{aligned}
\tag{10}
\]

The witness restriction likewise has the form

\[
 \widetilde{\mathcal O}_0|_{\mathscr K_{\rm hol}}
 =\bigoplus_{\boldsymbol\lambda}
 I_{R_{\boldsymbol\lambda}}\otimes O_{\boldsymbol\lambda}.
\tag{11}
\]

Therefore twirling removes all operator coherences between distinct
\(\boldsymbol\lambda\), but retains the complete matrix
\(X_{\boldsymbol\lambda}\) on each multiplicity space.  In particular, a
highest-weight carrier calculation tests multiplicity vectors, not the
normalized identity on the corresponding irreducible carrier.

## 4. Exact local sizes

At one site the holomorphic representation is \(\mathbf3^{\otimes5}\).  Its
irreducible types, irreducible dimensions, and multiplicities are

\[
\begin{array}{c|ccccc}
\lambda &[5]&[4,1]&[3,2]&[3,1,1]&[2,2,1]\\ \hline
\dim R_\lambda&21&24&15&6&3\\
\dim M_\lambda&1&4&5&6&5.
\end{array}
\tag{12}
\]

Both identities

\[
 21+24\cdot4+15\cdot5+6\cdot6+3\cdot5=243,
 \qquad
 1^2+4^2+5^2+6^2+5^2=103
\tag{13}
\]

are exact.  The first line may be constructed by applying row symmetrizers
and column antisymmetrizers for the five displayed diagrams.  Counting
standard fillings gives the second row of (12); counting semistandard
three-letter fillings gives the first row.  Equivalently, the two counts are
given by the directly checkable finite products

\[
 \dim M_\lambda={5!\over\prod_{b\in\lambda}h(b)},
 \qquad
 \dim R_\lambda=
 \prod_{1\le i<j\le3}
 {\lambda_i-\lambda_j+j-i\over j-i}.
\tag{14}
\]

At one site the mixed representation is
\(\bar{\mathbf3}^{\otimes2}\otimes\mathbf3^{\otimes3}\).  Direct
symmetrization and trace splitting give

\[
\begin{array}{c|rrrrrr}
\mu&(3,2)&(2,1)&(1,0)&(1,3)&(0,2)&(4,0)\\ \hline
\dim\widehat R_\mu&42&15&3&24&6&15\\
\dim N_\mu&1&6&6&2&5&1.
\end{array}
\tag{15}
\]

Again

\[
 42+15\cdot6+3\cdot6+24\cdot2+6\cdot5+15=243,
 \qquad
 1^2+6^2+6^2+2^2+5^2+1^2=103.
\tag{16}
\]

Thus partial transpose maps one 103-dimensional local commutant onto the
other.  Constructively, if \(P_\pi\) is the operator permuting five
covariant replicas, then

\[
 D_\pi=\Theta_{12}(P_\pi)
\tag{17}
\]

commutes with the mixed action.  The 120 operators \(P_\pi\) span a
103-dimensional space in local dimension three; partial transpose is an
invertible permutation of matrix entries, so the \(D_\pi\) also span a
103-dimensional space.  Equation (16) shows that this is the complete mixed
commutant.  This gives an exact rational diagram basis for the crossing map,
without constructing dense \(243\times243\) change-of-basis matrices.

For three sites the full commutant dimension is

\[
 103^3=1,092,727.
\tag{18}
\]

There are \(5^3=125\) holomorphic type triples and \(6^3=216\) mixed type
triples.  Before the range constraints, their largest multiplicity blocks
have size \(6^3=216\) on both sides.  Physical-site averaging reduces the
type triples to \(\binom{5+3-1}{3}=35\) and
\(\binom{6+3-1}{3}=56\) unordered triples, with the appropriate stabilizer
symmetry retained inside repeated-type multiplicity blocks.

## 5. The partial-transpose crossing transform

Let

\[
 U_{\boldsymbol\lambda}:
 R_{\boldsymbol\lambda}\otimes M_{\boldsymbol\lambda}
 \longrightarrow\mathscr B,
 \qquad
 \widehat U_{\boldsymbol\mu}:
 \widehat R_{\boldsymbol\mu}\otimes N_{\boldsymbol\mu}
 \longrightarrow\widehat{\mathscr B}
\]

be the unitary inclusions in (7), and write
\(d_{\boldsymbol\lambda}=\dim R_{\boldsymbol\lambda}\) and
\(\widehat d_{\boldsymbol\mu}=\dim\widehat R_{\boldsymbol\mu}\).
Extend an operator on \(K_{\boldsymbol\lambda}\) by zero to
\(M_{\boldsymbol\lambda}\).  Define

\[
 \mathcal I_{\rm hol}(X)
 =\sum_{\boldsymbol\lambda}
 U_{\boldsymbol\lambda}
 \left({I_{R_{\boldsymbol\lambda}}\over d_{\boldsymbol\lambda}}
       \otimes X_{\boldsymbol\lambda}\right)
 U_{\boldsymbol\lambda}^\dagger.
\tag{19}
\]

The exact crossing maps are

\[
 \boxed{
 \mathfrak C_{\boldsymbol\mu}(X)
 =\operatorname{Tr}_{\widehat R_{\boldsymbol\mu}}
 \left[
 \widehat U_{\boldsymbol\mu}^\dagger
 \Theta_1(\mathcal I_{\rm hol}(X))
 \widehat U_{\boldsymbol\mu}
 \right].
 }
\tag{20}
\]

Equations (3) and (8) imply the reconstruction formula

\[
 \Theta_1(\mathcal I_{\rm hol}(X))
 =\sum_{\boldsymbol\mu}
 \widehat U_{\boldsymbol\mu}
 \left({I_{\widehat R_{\boldsymbol\mu}}\over
              \widehat d_{\boldsymbol\mu}}
       \otimes\mathfrak C_{\boldsymbol\mu}(X)\right)
 \widehat U_{\boldsymbol\mu}^\dagger.
\tag{21}
\]

The normalization in (20) is fixed by
\(\operatorname{Tr}_{\widehat R}(I_{\widehat R}/\widehat d)=1\).
In particular,

\[
 \sum_{\boldsymbol\mu}
 \operatorname{Tr}\mathfrak C_{\boldsymbol\mu}(X)
 =\sum_{\boldsymbol\lambda}\operatorname{Tr}X_{\boldsymbol\lambda}.
\tag{22}
\]

Because both the representation and partial transpose factor over physical
sites, (20) factors into one-site crossing maps.  On an elementary tensor of
multiplicity operators,

\[
 \mathfrak C_{\boldsymbol\mu,\boldsymbol\lambda}
 (X_1\otimes X_2\otimes X_3)
 =\bigotimes_{i=1}^3
 \mathfrak c_{\mu_i,\lambda_i}(X_i),
\tag{23}
\]

and arbitrary multiplicity operators follow by linear extension.  The local
maps \(\mathfrak c_{\mu,\lambda}\) can be built exactly from (17), row and
column symmetrizers, and rational Gram matrices.  No raw
\(3,326,427\)-dimensional density matrix is required.

## 6. The exact coupled multiplicity-block SDP

Combining the preceding results, the corrected first-degree value is exactly

\[
\boxed{
\begin{aligned}
 \mu_1=\min\quad&
   \sum_{\boldsymbol\lambda}
   \operatorname{Tr}(O_{\boldsymbol\lambda}
                     X_{\boldsymbol\lambda})\\
 \text{subject to}\quad&
   X_{\boldsymbol\lambda}\succeq0
       \quad\text{on }K_{\boldsymbol\lambda},\\
 & \sum_{\boldsymbol\lambda}
      \operatorname{Tr}X_{\boldsymbol\lambda}=1,\\
 & Z_{\boldsymbol\mu}:=
      \mathfrak C_{\boldsymbol\mu}(X)\succeq0,\\
 & Z_{\boldsymbol\mu}
      =P_{L_{\boldsymbol\mu}}Z_{\boldsymbol\mu}
       P_{L_{\boldsymbol\mu}}
       \quad\text{for every }\boldsymbol\mu.
\end{aligned}}
\tag{24}
\]

The first positive cone in (24) is exactly \(\rho\succeq0\).  By (21), the
second family of positive cones is exactly
\(\rho^{\Gamma_1}\succeq0\).  The last line is exactly the mixed support
range condition.  Equations (11) and (19) give the objective.  Therefore
(24) is neither an outer approximation nor a symmetry ansatz: it has exactly
the same optimum as the corrected full cone.

## 7. Consequence for the remaining cross-carrier problem

No feasible minimizer needs coherences between inequivalent local-unitary
type triples.  The only remaining couplings are:

1. matrix coherences inside each holomorphic multiplicity block
   \(K_{\boldsymbol\lambda}\);
2. the linear crossing transform (20), which sums contributions from the
   holomorphic blocks into each mixed block;
3. the mixed support subspaces \(L_{\boldsymbol\mu}\).

Thus the complete global calculation should not enumerate arbitrary pairs of
highest-weight carriers.  It should compute the local 103-dimensional
crossing transform once, tensor it over three sites, insert the exact
holomorphic multiplicity spaces from the source/Omega census, and impose the
mixed kernels block by block.  A negative solution of (24) is an exact
higher-rank pseudomoment obstruction unless its holomorphic density has rank
one; positivity of (24) proves DTH.

What remains unresolved here is the sign of (24).

## 8. Exact audit of the support-ideal dual

The dual certificate (23) of `agent_dth_mixed_module.md` permits every
Hermitian mixed operator \(Y\) whose compression to
\(L=\ker\mathcal C_{\rm supp}\) is positive.  A useful restricted ansatz is

\[
 Y=\mathcal C_{\rm supp}^\dagger T\mathcal C_{\rm supp},
\tag{25}
\]

because its compression to \(L\) vanishes.  If any certificate of the form
(25) exists, averaging makes \(T\) local-unitary invariant, site-permutation
invariant, and fixed by entrywise conjugation without changing the
certificate inequality.

At one site the target representation is

\[
 \mathbf3\otimes\mathbf3\otimes\bar{\mathbf3}
 =(2,1)\oplus2(1,0)\oplus(0,2).
\tag{26}
\]

One direct derivation first splits the two covariant factors:

\[
 \begin{aligned}
 \operatorname{Sym}^2(\mathbf3)\otimes\bar{\mathbf3}
   &=(2,1)\oplus(1,0),\\
 \wedge^2(\mathbf3)\otimes\bar{\mathbf3}
   &=(0,2)\oplus(1,0).
 \end{aligned}
\]

The dimensions are \(15+3+6+3=27\).  Hence the local target commutant has
dimension

\[
 1^2+2^2+1^2=6.
\tag{27}
\]

An explicit Hermitian basis is

\[
 I,\quad s,\quad e,\quad ses,\quad se+es,
 \quad i(se-es),
\tag{28}
\]

where \(s\) swaps the two covariant slots and \(e\) is the unnormalized
contraction projector between the second covariant and contravariant slots.
The first five matrices in (28) are real and the last is purely imaginary.
Thus a general invariant three-site \(T\) has \(6^3=216\) Hermitian
coefficients.  Site averaging restricts it to
\(\operatorname{Sym}^3(\mathbb R^6)\), of dimension \(56\).  Entrywise
conjugation removes monomials containing an odd number of the last basis
element.  The surviving count is

\[
 \binom{5+3-1}{3}+5=35+5=40.
\tag{29}
\]

Therefore the advertised 40-parameter family is genuinely the complete
site- and conjugation-averaged family **within the quadratic ansatz (25)**.

There is a further exact redundancy.  The support target contains a global
bivector in its first two covariant replica slots, so it is compressed by

\[
 P_-={I-s\otimes s\otimes s\over2}.
\tag{30}
\]

Exact Hilbert--Schmidt Gram elimination gives

\[
 \boxed{
 \dim\operatorname{span}_{\mathbb R}{
 P_-TP_-:T\text{ in the 40-parameter family}}=14.
 }
\tag{31}
\]

Before the conjugation restriction, the 56 site-symmetric Hermitian
monomials have compressed rank 16.  These are exact rational ranks; the
checker builds the six integer/Gaussian-integer matrices (28), expands
(30), and gives modular full-pivot certificates.  Thus only fourteen real
quadratic support corrections need be tested, not forty.

### 8.1 Why the quadratic family is not the general affine ideal

Let \(C=\mathcal C_{\rm supp}\).  Every Hermitian operator with zero
compression to \(L=\ker C\) can be written

\[
 \boxed{Y=C^\dagger R+R^\dagger C}
\tag{32}
\]

for a linear map \(R\) from the mixed source to the support target.  To prove
this, decompose the source as \(L\oplus L^\perp\).  The restriction
\(A=C|_{L^\perp}\) is invertible onto \(\operatorname{ran}C\).  A Hermitian
zero-compression operator has blocks

\[
 Y=\begin{pmatrix}0&B\\B^\dagger&D\end{pmatrix}.
\]

Taking, on the two source summands,

\[
 R_L=(A^\dagger)^{-1}B^\dagger,
 \qquad
 R_{L^\perp}={1\over2}(A^\dagger)^{-1}D
\]

and viewing their ranges inside \(\operatorname{ran}C\) proves (32) by
block multiplication.

In contrast, \(C^\dagger TC\) annihilates \(L\) on both its left and right.
It cannot produce the off-diagonal blocks \(B\).  Thus (25) is strictly
smaller than the general affine ideal whenever both \(L\) and \(L^\perp\)
are nonzero.

The exact local size of the general equivariant \(R\) is also small enough
to state explicitly.  Comparing (15) with (26), only three common types
occur, and

\[
 \boxed{
 \dim\operatorname{Hom}_{U(3)}
 (\bar{\mathbf3}^{\otimes2}\otimes\mathbf3^{\otimes3},
  \mathbf3^{\otimes2}\otimes\bar{\mathbf3})
 =6\cdot1+6\cdot2+5\cdot1=23.
 }
\tag{33}
\]

For three physical sites the equivariant intertwiner space therefore has
dimension \(23^3\).  Its site-symmetric part has complex dimension

\[
 \boxed{\binom{23+3-1}{3}=2300}
\tag{34}
\]

before imposing the conjugation reality condition.  Consequently the most
general invariant zero-on-\(L\) affine correction is obtained from (32) with
this site-symmetric \(R\), not from the fourteen effective quadratic
parameters in (31).

For a completely general dual certificate, add an invariant positive
operator \(Y_L\succeq0\) supported on \(L\), and seek

\[
 \begin{aligned}
 Y&=Y_L+C^\dagger R+R^\dagger C,\\
 O_K-\gamma I_K-
   \iota_K^\dagger\Theta_1(Y)\iota_K&\succeq0.
\end{aligned}
\tag{35}

Equation (35) is exactly the invariant form of the full dual, because every
invariant \(Y\) with positive compression to \(L\) splits into its positive
\(L\)-compression plus a zero-compression remainder, and (32) represents the
latter.  Whether the fourteen-parameter quadratic subfamily already repairs
every negative holomorphic carrier is a separate exact rank/feasibility
calculation; symmetry alone cannot justify that restriction.

## 9. Exact no-go for the quadratic dual on the cloud carrier

The separate rank/feasibility calculation in the preceding sentence can be
completed exactly on the canonical seven-dimensional highest-weight
multiplicity carrier

\[
 [4,1]\otimes[4,1]\otimes[3,2].
\]

Let \(\nu_1,\ldots,\nu_7\) be the exact rational carrier basis constructed
in `agent_dth_block_census.py`, and put

\[
 Q_{ij}=\langle\nu_i,\widetilde{\mathcal O}_0\nu_j\rangle.
\]

For the fourteen effective monomials selected from (28), let

\[
 K^{(a)}_{ij}
 =\left\langle\nu_i,
 \Theta_1(C^\dagger T_aC)\nu_j\right\rangle,
 \qquad 1\le a\le14.
\tag{36}
\]

All entries in (36) are rational.  They are constructed without forming a
dense mixed operator, using self-adjointness of partial transpose:

\[
 K^{(a)}_{ij}
 =\operatorname{Tr}\!\left(
 C\Theta_1(|\nu_j\rangle\langle\nu_i|)C^\dagger T_a
 \right).
\tag{37}
\]

There is an exact rank-one relation among the first four corrections,

\[
 -3K^{(1)}+11K^{(2)}-8K^{(3)}+4K^{(4)}
 =-{5\over96}rr^{\mathsf T},
\qquad
 r=(3,-6,5,-2,-4,-7,-14)^{\mathsf T}.
\tag{38}
\]

Define the \(7\times6\) integer matrix \(B\) by

\[
 B_{j,j-1}=3\ (1\le j\le6),
 \qquad
 B_{0,j-1}=-r_j,
\]

with all other entries zero.  Thus \(B^{\mathsf T}r=0\).  Let

\[
G=\begin{pmatrix}
3/128&7651/1440000&-40681/2880000&19/2000&3/1000&-1/500\\
7651/1440000&13/2000&-17/2000&9/1000&-1/500&1/1000\\
-40681/2880000&-17/2000&43/2000&-7/500&-1/500&1/2000\\
19/2000&9/1000&-7/500&37/2000&-1/200&3/2000\\
3/1000&-1/500&-1/500&-1/200&3/500&-1/400\\
-1/500&1/1000&1/2000&3/2000&-1/400&3/2000
\end{pmatrix}.
\tag{39}
\]

Exact elimination gives the diagonal pivots

\[
\begin{gathered}
{3\over128},\quad
{257362199\over48600000000},\quad
{15826251843\over2058897592000},\\
{7006171723\over1266100147440},\quad
{54168407301\over43788573268750},\quad
{137174154077\over866694516816000},
\end{gathered}
\tag{40}
\]

all strictly positive.  Hence

\[
 H=BGB^{\mathsf T}\succeq0
\]

has rank six.  Direct rational contraction gives

\[
 \boxed{
 \operatorname{Tr}(HK^{(a)})=0\quad(1\le a\le14),
 \qquad
 \operatorname{Tr}(HQ)=-{44943\over4096000}<0.
 }
\tag{41}
\]

If a quadratic correction made
\(Q-\sum_at_aK^{(a)}\succeq0\), pairing it with \(H\succeq0\) would be
nonnegative.  Equation (41) makes that pairing strictly negative.  Therefore

\[
 \boxed{
 \text{no invariant quadratic support correction }C^\dagger TC
 \text{ repairs even this one negative carrier.}
 }
\tag{42}
\]

This is an exact proof-complexity obstruction, not a pseudomoment or physical
DTH counterexample.  It proves that a support-ideal certificate must use the
affine cross terms (32), a positive \(L\)-block, or a different mechanism.
The exact checker is
`verification/agent_dth_quadratic_support_dual_no_go.py`.

There is also a clean exact reason that the full affine terms have enough
freedom on this individual carrier.  Define

\[
 \Phi:\operatorname{End}(\mathscr B_7)\longrightarrow
 \operatorname{Hom}(\widehat{\mathscr B},\mathscr T),
 \qquad
 \Phi(E)=C\Theta_1(E),
\]

where \(\mathscr B_7\) is the seven-dimensional carrier and
\(\mathscr T\) the support target.  The established exact support-rank
calculation says that \(\Phi\) is injective.  For every \(E\) and \(R\),
self-adjointness of partial transpose gives

\[
 \left\langle E,
 P_{\mathscr B_7}\Theta_1(C^\dagger R)P_{\mathscr B_7}
 \right\rangle_{\rm HS}
 =\langle C\Theta_1(E),R\rangle_{\rm HS}.
\tag{43}
\]

Thus the one-sided affine pullback in (43) is exactly \(\Phi^\dagger\).
Injectivity of \(\Phi\) implies surjectivity of \(\Phi^\dagger\): its range
has dimension equal to the rank of \(\Phi\), namely \(7^2\).  Given an
arbitrary Hermitian \(A\) on the carrier, choose \(R\) with
\(\Phi^\dagger(R)=A/2\).  Then

\[
 P_{\mathscr B_7}\Theta_1(C^\dagger R+R^\dagger C)
 P_{\mathscr B_7}=A.
\tag{44}
\]

Therefore the full affine ideal can repair an arbitrary Hermitian matrix on
this carrier.  The same conclusion applies separately to every carrier with
full support-map rank in the exact census.  It does **not** yet give one
globally equivariant \(R\) that repairs all isotypic components
simultaneously; that compatibility is the remaining dual block problem.
