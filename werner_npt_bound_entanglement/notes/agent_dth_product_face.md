# An exact 2266-dimensional physical mixed face

## Status

This note constructs a finite ensemble of exact physical DTH monomials and
determines the rank of its local-unitary-twirled mixed moment **over the
rationals**:

\[
 \boxed{\operatorname{rank} Z_{\rm prod}=2266.}
\]

The rank is distributed over 198 of the 216 mixed local-type blocks.  The
range is therefore an explicit rational face candidate inside the
9197-dimensional mixed support space.  Exact pivot columns of the 216 block
matrices give a rational basis of this range.

This is a facial-structure theorem for a finite physical ensemble.  It does
not yet prove that every feasible corrected DTH moment lies in this face.
That stronger statement requires an exact positive exposing operator whose
holomorphic pullback vanishes.  Such an operator has only been seen
numerically so far.

The independent exact programs are

- `verification/agent_dth_product_face_rank.py` (two prime fields);
- `verification/agent_dth_product_face_rank_rational.py` (integer/rational
  replay).

No floating-point rank decision occurs in either verifier.

## 1. The 27 physical product branches

For each allocation

\[
 (i,j,k)\in\{0,1,2\}^3,
\]

choose real nonzero integer vectors

\[
 a_s,b_s,c_s\in\mathbb Z^3,\qquad s=0,1,2,
\]

such that

\[
 c_i^{\mathsf T}a_i=0,\qquad
 c_j^{\mathsf T}b_j=0,\qquad
 \det(c_k,a_k,b_k)=0.
\tag{1}
\]

The verifier gives deterministic small-integer choices, including all cases
where two or three of the sites in (1) coincide.  It also checks that at
least one local pair \((a_s,b_s)\) is independent.  Hence the global product
vectors

\[
 u_0=a_0\otimes a_1\otimes a_2,
 \qquad
 u_1=b_0\otimes b_1\otimes b_2
\]

are independent.  Put

\[
 z=c_0\otimes c_1\otimes c_2,
 \qquad w=u_0\wedge u_1.
\]

The support equations factor:

\[
 \langle z,u_0\rangle=\prod_s c_s^{\mathsf T}a_s=0,
 \qquad
 \langle z,u_1\rangle=\prod_s c_s^{\mathsf T}b_s=0.
\tag{2}
\]

Thus \(W^\dagger z=0\).  The alternating Hodge scalar also factors, up to
the fixed nonzero normalization in the definition of the local Hodge maps:

\[
 \operatorname{Tr}(D_zW)
 \ \propto\
 \prod_s\det(c_s,a_s,b_s)=0.
\tag{3}
\]

Consequently

\[
 h_{ijk}=w\otimes w\otimes z
\]

is an exact physical rank-one point of the corrected DTH moment cone for
every one of the 27 allocations.  No claim about the sign of its DTH
objective is used.

## 2. Rational twirling in the 103-diagram bridge

At one physical site, write \(P_b\), \(1\leq b\leq103\), for the selected
covariant permutation diagrams and

\[
 D_b=\Theta_{12}(P_b)
\]

for their mixed partial transposes.  Their common Hilbert--Schmidt Gram
matrix is

\[
 G_{ab}=3^{c(\pi_a^{-1}\pi_b)}.
\tag{4}
\]

Let \(B\in M_{103}(\mathbb Z)\) be the exact mixed highest-weight
restriction matrix from the local crossing bridge.  If \(m\) is the vector
of diagram moments of a local rank-one ket--bra, its mixed block coordinate
vector is

\[
 BG^{-1}m.
\tag{5}
\]

The apparently large inverse in (5) reduces exactly to

\[
 \boxed{BG^{-1}=\frac1{7560}\,T,\qquad T\in M_{103}(\mathbb Z),}
\tag{6}
\]

with

\[
 \max_{a,b}|T_{ab}|=7560.
\]

Thus every block of the twirled ensemble is rational with one known common
denominator.  The factor \(7560^{-3}\), and the common factor \(1/4\) from
the two bivectors, do not affect its range.

For one product triple the density expansion has only 16 terms.  Therefore
the full 27-point ensemble

\[
 Z_{\rm prod}
 =\sum_{i,j,k}\mathbb E_{U(3)^3}
 \left(|\bar w\otimes w\otimes z\rangle
       \langle\bar w\otimes w\otimes z|\right)
\tag{7}
\]

is a sum of 432 tensor products of the exact local block vectors (5).

## 3. Exact rank theorem

### Theorem

For the deterministic 27-point ensemble (7), the sum of the rational ranks
of its 216 mixed multiplicity blocks is

\[
 \boxed{2266.}
\tag{8}
\]

Exactly 198 blocks are nonzero.

### Verification

The fast verifier evaluates all matrices over each of

\[
 \mathbb F_{1000003},\qquad \mathbb F_{1000033}.
\]

Both fields give total rank 2266, the same 198 active blocks, and the same
pivot columns.  The serialized pivot list has SHA-256 digest

\[
 \mathtt{2297a5d32caba44ac2dd6a8d26983a9fe61b7bf11d73e7daba06af251a050955}.
\tag{9}
\]

This supplies an exact lower bound and explicit candidate range columns.
The rational verifier independently constructs the integer numerator of
every block using (6) and computes its rank over \(\mathbb Q\).  The exact
ranks again sum to 2266.  Equality of the rational and finite-field ranks
proves that the pivot columns in (9), interpreted as columns of the rational
block matrices, are a basis of the range.  This proves (8), including both
directions.

Four blocks are exceptionally ill-conditioned in floating point.  In the
mixed-type index order

\[
 ((3,2),(2,1),(1,0),(1,3),(0,2),(4,0)),
\]

their exact ranks are

\[
 \begin{aligned}
 (2,2,2)&:51,\\
 (2,4,4)&:36,\\
 (4,2,4)&:36,\\
 (4,4,2)&:36.
 \end{aligned}
\tag{10}
\]

An early modular experiment incorrectly added one direction in each of
these blocks because a five-factor `int64` product overflowed before its
modular reduction.  The verifier now reduces after every factor.  The two
prime fields and the independent integer replay both give (10).

## 4. Relation to the numerical common face

The complete invariant linear-consistency solver independently approached a
mixed rank of 2266.  The exact physical ensemble (7) therefore supplies a
rational model of precisely the same observed dimension.  A floating-point
range basis in the solver's orthonormal mixed-support coordinates was also
constructed from (7); it is a convenience for discovery only, while (8)--
(10) are the exact certificate.

The numerical exposing normal has the following additional pattern.

- Its kernel agrees with the 2266-dimensional range from (7).
- On 193 of the 216 mixed blocks its compression to the complementary
  subspace is scalar, with the scalar proportional to the square root of the
  mixed carrier dimension.
- The remaining 23 blocks are exactly the triples in
  \(\{(2,1),(1,0),(0,2)\}^3\), except \((2,1)^3\) and the three permutations
  of \((2,1),(0,2),(0,2)\).  Their departure from the scalar floor has small
  aggregate rank numerically.

These observations sharply reduce the next exact reconstruction, but they
are not yet a theorem.  The unweighted orthogonal projector onto the
complement of (7) does **not** work: its holomorphic pullback is indefinite.
The exposing operator needs nontrivial positive weights, specifically the
23-block correction above.

## 5. Logical scope

What is proved:

1. all 27 generators obey the physical support and Omega equations exactly;
2. their mixed local-unitary twirl has exact rational rank 2266;
3. explicit rational block columns give a basis of that range.

What is not proved:

1. that every feasible corrected first-level moment lies in this range;
2. existence of an exact PSD exposing normal with zero holomorphic pullback;
3. positivity of the corrected first-level objective;
4. DTH, square-zero positivity, unrestricted three-copy positivity, or any
   all-copy Werner statement.

The immediate next lemma is now finite and smaller: reconstruct the weighted
PSD exposing normal on the rational complement of (8), with only 23
non-scalar mixed blocks, and verify its holomorphic pullback vanishes exactly.
