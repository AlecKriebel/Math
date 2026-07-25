# Full-matrix centered/tight endpoint

This continuation studies the weighted strongly-regular identity
\[
B^2=\frac{77}{5}I+\frac{287}{5}J-\frac{72}{5}B,\qquad
B_{ii}=0,\qquad 0\leq B_{ij}\leq3.
\]
It is deliberately separate from the earlier pair/triple endpoint work.
Nothing in this directory addresses non-centered or non-tight codes.

## Exact equivalence warning

There cannot be a symmetric countermodel satisfying all three displayed
conditions but failing to be a Gram realization.  Indeed, the matrix
identity implies \(BJ=JB\).  Thus \(B{\bf1}=r{\bf1}\), where
\[
5r^2+72r-11844=0.
\]
Nonnegativity selects \(r=42\), rather than \(r=-282/5\).  Setting
\[
G=\frac{I+J-B}{2}
\]
then gives
\[
G{\bf1}=0,\qquad G^2=\frac{41}{5}G,\qquad G_{ii}=1.
\]
Hence \(G\succeq0\), \(\operatorname{rank}G=5\), and
\(-1\leq G_{ij}\leq1/2\).  Such a \(B\) is exactly a centered unit-norm
tight 41-point kissing configuration.

Accordingly, any relaxation countermodel below must state precisely which
common-source part of the matrix equation it drops.

An equivalent scaled involution is
\[
 H=5B-5J+36I.
\]
It obeys
\[
 H^{\mathsf T}=H,\qquad H^2=41^2I,\qquad
 H{\bf1}=41{\bf1},
\]
with diagonal \(31\) and off-diagonal interval \([-5,10]\).  Hence every
row satisfies
\[
 \sum_{j\ne i}H_{ij}=10,\qquad
 \sum_{j\ne i}H_{ij}^2=720,
\]
and every pair of distinct rows satisfies the full covariance equation
\[
 \sum_{k\notin\{i,j\}}H_{ik}H_{kj}=-62H_{ij}.
\]
The spectrum is \(41^{36},(-41)^5\).  This formulation retains the whole
common-source equation; replacing its last display by averages is a genuine
relaxation.

## Type-conditional relaxation

For a base pair with inner product \(t\), write the other two inner
products in a distinct triple as \(u,v\).  The complete matrix identity
implies, separately for every individual base pair,
\[
\begin{aligned}
\#\{k\}&=39,\\
\sum_k u_k&=-1-t,\\
\sum_k u_k^2&=\frac{36}{5}-t^2,\\
\sum_k u_kv_k&=\frac{31}{5}t.
\end{aligned}
\]
The discovery program asks only that these equations hold after averaging
over all base pairs having the same atomic value \(t\).  This is strictly
weaker than a labeled matrix equation.

`search_conditional_bv.py` searches this conditional relaxation together
with corrected common-pair capacities and finitely many full-radial
Bachoc--Vallentin blocks.  Its floating output is discovery-only.

## Exact conditional countermodel

`conditional_identity_capacity_pseudodistribution.json` is a sparse exact
46-orbit measure.  The standard-library verifier proves:

- all eleven type-conditional mass, first, square, and cross identities;
- triangle Gram positivity for every supported orbit;
- the exact global tight-frame pair and cubic trace moments;
- the robust-depth pair counts;
- all 48 corrected stratified capacity rows and both weighted rows.

This does **not** realize the matrix identity.  It replaces one equation
for every labeled base pair by one averaged equation for every one of the
eleven atomic base types.  The distinction is concrete: its \(k=0\)
full-radial BV node block has the negative principal minor on node indices
\(\{5,8\}\)
\[
-\frac{
2830461431707995511321694029528648251232619878927921793
}{
47487042874438301580423367503413578715200000000000000
}<0.
\]
Thus the artifact is a barrier only to arguments using the type-averaged
conditional moments and capacities without common-source positivity.

Reproduce it with

```sh
python3 \
  experiments/centered_tight_full_matrix_identity/verify_conditional_identity.py
python3 -m unittest discover \
  -s experiments/centered_tight_full_matrix_identity \
  -p 'test_*.py' -v
```

Current SHA-256 values are

```text
5dd04104e27ff7cb5c631d32359ef9bd2e352de822f798a8559d01b727840eb3  conditional_identity_capacity_pseudodistribution.json
e22024339d336735c9d653dafdac845a3953fd15929e1d362cd7318617635e9c  verify_conditional_identity.py
```

## Exact degree-twelve BV countermodel

The sparse witness above deliberately fails common-source positivity.
The stronger artifact
`conditional_bv_degree12_rationalization.json` instead reconstructs a
strictly positive rational weight on all 246 feasible triple orbits.  Its
standard-library verifier proves exactly that it satisfies:

- all 45 total and type-conditional equations;
- all 48 corrected stratified capacity rows and both weighted rows;
- the complete appended \(k=0\) radial block;
- every positive-degree full-radial Bachoc--Vallentin block for
  \(1\leq k\leq12\).

The JSON contains rounded free weights and identifies 40 pivot weights.
The verifier solves the corresponding nonsingular \(40\)-by-\(40\)
rational system, checks all 45 equations rather than only the reconstruction
rows, and then performs only exact `Fraction` arithmetic.

The singular low-degree blocks are not accepted merely from numerical
eigenvalues.  For \(k=0\), the verifier checks the three independent exact
kernels forced by fixed cardinality, centering, and tightness, then proves
an exact \(9\)-by-\(9\) principal block positive definite by
\(LDL^{\mathsf T}\).  For \(k=1\) and \(k=2\), it similarly checks the two
and one forced kernels and positive-definite complementary principal
blocks.  The blocks for \(3\leq k\leq12\) are proved positive definite
directly.

The cutoff is precise only for this witness.  Its degree-thirteen block has
a strictly negative principal minor on node indices \(\{2,7,10\}\).  This
does not prove that the degree-thirteen relaxation is infeasible; it proves
only that the stored witness stops at degree twelve.

Consequently, type-conditional matrix identities, the present cap
capacities, and finitely many full-radial BV blocks through degree twelve
still do not recover a labeled common-source matrix.  The artifact is not a
matrix, Gram matrix, or spherical code.

Reproduce the stronger certificate with

```sh
python3 \
  experiments/centered_tight_full_matrix_identity/verify_conditional_bv_degree12.py
python3 -m unittest discover \
  -s experiments/centered_tight_full_matrix_identity \
  -p 'test_*.py' -v
```

Its SHA-256 values are

```text
708768158349c97e46c44c7451604284c17522b34b27549fd2c805410d99118f  conditional_bv_degree12_rationalization.json
5582e66c2cba8633d7c0cb990c2afb2a614b16fe062b515a1b44dfecf0e42554  verify_conditional_bv_degree12.py
```

## Exact degree-thirteen obstruction for the fixed atom table

The witness-specific negative minor above suggested a genuine cutoff.
`fixed_atomic_degree13_dual_certificate.json` proves a stronger exact
statement: **no** nonnegative triple-orbit measure using this fixed
eleven-node pair table and the fixed multiplicities
\[
(2,2,4,2,2,2,2,8,2,2,12)
\]
can satisfy the selected type-conditional equations, the stratified
capacity rows, and the radial BV blocks through degree thirteen.

This result remains sharply restricted.  Centering and tightness do not
force inner products to lie in these eleven values, and they do not force
the displayed multiplicities.  Therefore this certificate is not a
universal obstruction to a centered tight 41-point code, much less to an
arbitrary 41-point code.

Here is the exact dual identity checked by the verifier.  Write the 40
selected conditional equations as \(A\nu=b\), the 48 capacities as
\(C\nu\leq d\), and the reduced radial matrices as
\[
R_k(\nu)=D_k+\sum_j\nu_jF_{kj}\succeq0.
\]
The certificate supplies nonnegative capacity multipliers \(z\), rational
Gram factors for matrices \(Q_k\succeq0\), and rational equality
multipliers \(y\).  With
\[
f_j=\sum_k\langle Q_k,F_{kj}\rangle,\qquad
s=C^{\mathsf T}z-f+A^{\mathsf T}y,
\]
the verifier proves every coordinate of \(s\) is strictly positive and
\[
\theta=
\sum_k\langle Q_k,D_k\rangle+z^{\mathsf T}d+y^{\mathsf T}b
=-\frac{30000003358470861}{10^{22}}<0.
\]
If a feasible \(\nu\geq0\) existed, then
\[
\begin{aligned}
0
&\leq \sum_k\langle Q_k,R_k(\nu)\rangle\\
&=\sum_k\langle Q_k,D_k\rangle+f^{\mathsf T}\nu\\
&=\sum_k\langle Q_k,D_k\rangle
  +z^{\mathsf T}C\nu+y^{\mathsf T}b-s^{\mathsf T}\nu\\
&\leq\theta<0,
\end{aligned}
\]
a contradiction.  PSD is exact by construction: each \(Q_k\) is stored as
a sum of 18 rational rank-one Gram factors.  The smallest exact coordinate
of \(s\) is
\[
\frac{
6660330108054478083325266562799
}{
11561737688261718750000000000000000000000
}>0.
\]

The floating search and rationalization use Python 3.14.6, NumPy 2.5.1,
CVXPY 1.9.2, and Clarabel 0.11.1.  Solver status is used only for
discovery.  The final verifier uses the Python standard library and
recomputes every sign exactly.

Reproduce discovery, rationalization, and exact verification with

```sh
.venv/bin/python \
  experiments/centered_tight_full_matrix_identity/search_degree13_reduced.py \
  --maximum-degree 13 --capacity-indices all \
  --output \
  experiments/centered_tight_full_matrix_identity/degree13_reduced_discovery.json
.venv/bin/python \
  experiments/centered_tight_full_matrix_identity/rationalize_fixed_atomic_degree13_dual.py
python3 \
  experiments/centered_tight_full_matrix_identity/verify_fixed_atomic_degree13_obstruction.py
```

The exact artifacts have hashes

```text
09f8162a4b208ce0c2c5c06dc12b3822628757237af726491a0ffa5cdf624df5  degree13_reduced_discovery.json
7618f1c453e69661ee367c36e29627a0970c053a6202bbee1aee876ad5a0a269  fixed_atomic_degree13_dual_certificate.json
39a3ce12dee723b459f3e8f6fbe59aacd8b92503e3039dfb8e0f90413f98138e  verify_fixed_atomic_degree13_obstruction.py
```

## A low-rank nonnegative transform

For a genuine endpoint matrix define entrywise
\[
 W_{ij}=B_{ij}(3-B_{ij}).
\]
Then \(W\geq0\), \(W_{ii}=0\), and
\[
 W{\bf1}=\frac{266}{5}{\bf1}.
\]
Let \(H_2=(5G\circ G-J)/4\) be the degree-two harmonic Gram matrix.
Since \(H_2\succeq0\), \(\operatorname{rank}H_2\leq14\), and
\[
 W-4I=\frac65J-2G-\frac{16}{5}H_2,
\]
we have
\[
 \operatorname{rank}(W-4I)\leq20.
\]
Consequently \(4\) is an eigenvalue of \(W\) with multiplicity at least
21.  Combining this with the Perron eigenvalue \(266/5\), trace zero, and
Cauchy--Schwarz on the remaining 19 eigenvalues gives
\[
 \operatorname{tr}W^2\geq\frac{394912}{95}.
\]
The elementary entrywise bound
\[
 [b(3-b)]^2\leq\frac94b(3-b)
\]
only gives
\[
 \operatorname{tr}W^2\leq41\cdot\frac{1197}{10},
\]
so this transform alone does not contradict feasibility.  Any continuation
must add a sharper row-pair or common-source bound, not merely repeat the
spectral multiplicity calculation.
