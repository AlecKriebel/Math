# Rank-two leg-commutant branches in dimension six

**Date:** 2026-07-29
**Status:** PROVED for the factor branch; exact reduction and assumption
audit for the three-central-atom branch
**Scope:** arbitrary exceptional solutions; no Pauli, sparsity, or
irreducibility assumption

## 1. Executive conclusion

Let \(d=6\), and let
\[
\mathcal C_L(P)=\{x\in M_6:[x\otimes I,P]=0\},\qquad
\mathcal C_R(P)=\{x\in M_6:[I\otimes x,P]=0\}.
\]
The odd-leg-projection theorem implies that every projection in either
algebra has even ordinary rank.  One of the largest surviving algebra
types in the arithmetic audit was
\[
M_3(\mathbb C)\otimes I_2.
\]
It is in fact impossible:

> **Factor no-go.**  No exceptional solution in dimension \(d=2m\), with
> \(m\) odd, can have \(M_m(\mathbb C)\otimes I_2\) in either one-leg
> commutant.

The mechanism is elementary.  Commutation with the factor reduces the
first local leg to a qubit.  Automatic standardness removes the scalar
Pauli coefficient.  Involutivity then forces the three operator
coefficients to commute, so the *opposite* leg becomes rank-one
controlled.  A rank-one opposite-leg projection contradicts
\[
8\mid d^2.
\]

For \(d=6\), this removes every branch containing the factor algebra
\(M_3\otimes I_2\), including the factor--factor branch.  It also gives an
invariant explanation for the failure of the crossed \(3\times2\) model
when its rank-three color algebra is upgraded to the corresponding full
matrix factor.

The genuinely surviving three-color case is weaker:
\[
\mathbb C I_2\oplus\mathbb C I_2\oplus\mathbb C I_2.
\]
Its three rank-two central atoms do **not** supply the matrix units used in
the factor proof.  The nine two-site cells may be unrelated
two-qubit projections, and the two three-color decompositions on the
middle site may be in arbitrary relative position in \(U(6)\).  The
uniform endpoint counts \((3,9,3)\) are not automatic in this branch.

## 2. The factor no-go

### Theorem 2.1

Let \(V\cong\mathbb C^{2m}\), where \(m\) is odd, and let
\[
P=P^*=P^2\in\operatorname{End}(V\otimes V)
\]
be an exceptional projection.  Thus
\[
\operatorname{rank}P=\frac{d^2}{2},\qquad d=2m,
\]
and
\[
P_{12}P_{23}P_{12}-P_{23}P_{12}P_{23}
=\frac13(P_{12}-P_{23}).
\tag{1}
\]
Then neither \(\mathcal C_L(P)\) nor \(\mathcal C_R(P)\) contains a unital
subalgebra unitarily conjugate to
\[
M_m(\mathbb C)\otimes I_2.
\tag{2}
\]

### Proof

It suffices to treat the left leg.  Choose the tensor coordinates
\[
V_1=\mathbb C^m\otimes\mathbb C^2
\]
in which the assumed algebra is \(M_m\otimes I_2\).  Put
\[
H=I-2P.
\]
Since \(H\) commutes with
\[
(M_m\otimes I_2)\otimes I_{V_2},
\]
the finite-dimensional commutant theorem gives
\[
H=I_m\otimes K,
\qquad
K\in\operatorname{End}(\mathbb C^2\otimes V_2).
\tag{3}
\]
Here and below the tensor order is
\[
\mathbb C^m\otimes\mathbb C^2\otimes V_2.
\]

Automatic standardness for arbitrary exceptional solutions says
\[
\operatorname{Tr}_{V_1}H=0.
\tag{4}
\]
Taking the first-site partial trace of (3) yields
\[
0=m\,\operatorname{Tr}_{\mathbb C^2}K,
\]
and hence
\[
\operatorname{Tr}_{\mathbb C^2}K=0.
\tag{5}
\]
Hermiticity and involutivity of \(H\) give
\[
K=K^*,\qquad K^2=I.
\tag{6}
\]

Expand \(K\) in the Pauli basis.  Equation (5) removes the identity
coefficient exactly, so
\[
K=X\otimes B_1+Y\otimes B_2+Z\otimes B_3,
\qquad B_j=B_j^*.
\tag{7}
\]
The Pauli multiplication table gives
\[
\begin{aligned}
K^2={}&I\otimes(B_1^2+B_2^2+B_3^2)\\
&+iX\otimes[B_2,B_3]
+iY\otimes[B_3,B_1]
+iZ\otimes[B_1,B_2].
\end{aligned}
\tag{8}
\]
The four Pauli matrices \(I,X,Y,Z\) are linearly independent.  Comparing
their coefficients in \(K^2=I\) therefore gives the four *separate*
identities
\[
B_1^2+B_2^2+B_3^2=I,
\tag{9}
\]
\[
[B_2,B_3]=[B_3,B_1]=[B_1,B_2]=0.
\tag{10}
\]
Thus (10) is not one epsilon-weighted cancellation: the three commutators
are respectively the \(X,Y,Z\) coefficients.

The \(B_j\) are a commuting family of Hermitian matrices, so there is an
orthonormal basis \(\{\psi_s\}_{s=1}^d\) of \(V_2\) and real numbers
\(b_{js}\) such that
\[
B_j\psi_s=b_{js}\psi_s.
\]
Equation (9) says
\[
b_{1s}^2+b_{2s}^2+b_{3s}^2=1.
\tag{11}
\]
Writing \(n_s=(b_{1s},b_{2s},b_{3s})\in S^2\), equations (3) and (7)
become
\[
\boxed{
H=\sum_{s=1}^d
\left(I_m\otimes(n_s\cdot\sigma)\right)
\otimes|\psi_s\rangle\langle\psi_s|.
}
\tag{12}
\]
Consequently every rank-one projection
\[
\Pi_s=|\psi_s\rangle\langle\psi_s|
\]
belongs to the opposite one-leg commutant:
\[
I\otimes\Pi_s\in\{P\}'.
\tag{13}
\]

The invariant controlled-leg theorem applies to every projection of rank
\(r\) in a one-leg commutant and gives
\[
8\mid r d^2.
\tag{14}
\]
Using \(r=1\) in (13) yields
\[
8\mid d^2.
\tag{15}
\]
But \(d=2m\) with \(m\) odd has \(v_2(d^2)=2\), contradicting (15).
This proves the left-leg case.  Tensor flip proves the right-leg case.
\(\square\)

### Corollary 2.2

For a hypothetical \(d=6\) exceptional solution, neither leg commutant can
have type \(M_3(\mathbb C)\otimes I_2\).

This is stronger than the all-strand multiplicity audit.  That audit
correctly showed that the factor type passes every central-rank and
endpoint transportation equation.  The obstruction above uses spatial
involutivity before the braid arithmetic: a local qubit with no scalar
Pauli coefficient forces a rank-one algebra on the other leg.

## 3. Correct bookkeeping for three rank-two central atoms

Now assume only that the two leg commutants contain decompositions
\[
I=L_0+L_1+L_2,\qquad
I=R_0+R_1+R_2,
\tag{16}
\]
where all \(L_a,R_b\) have rank two,
\[
L_a\in\mathcal C_L(P),\qquad
R_b\in\mathcal C_R(P).
\]
No matrix units joining different \(L_a\)'s or \(R_b\)'s are assumed.

### 3.1 The nine two-site cells

The projections \(L_a\otimes R_b\) commute with \(P\), so
\[
Q_{ab}=(L_a\otimes R_b)P
\tag{17}
\]
is a projection on the four-dimensional cell \(L_aV\otimes R_bV\).
Put
\[
n_{ab}=\operatorname{rank}Q_{ab}\in\{0,1,2,3,4\}.
\tag{18}
\]
Automatic standardness gives
\[
\boxed{
\sum_b n_{ab}=6,\qquad
\sum_a n_{ab}=6.
}
\tag{19}
\]
More strongly,
\[
\boxed{
\sum_b\operatorname{Tr}_{R_bV}Q_{ab}=3I_{L_aV},
\qquad
\sum_a\operatorname{Tr}_{L_aV}Q_{ab}=3I_{R_bV}.
}
\tag{20}
\]
Thus the nine cells need not be signature-\((2,2)\) reflections.  The
assumption that all \(n_{ab}=2\), made in the first mixed-color search, is
a proper subansatz.

There are exactly \(217\) labelled integer matrices satisfying
(18)--(19).  Modulo independent row and column permutations, transpose,
and complementation
\[
n_{ab}\longmapsto4-n_{ab},
\]
there are nine rank-pattern orbits.  All \(217\) pass the stronger
standardness identities (20).  Indeed, for every
\(r\in\{0,1,2,3,4\}\), there is a two-qubit rank-\(r\) projection \(Q^{(r)}\)
with
\[
\operatorname{Tr}_1Q^{(r)}
=\operatorname{Tr}_2Q^{(r)}
=\frac r2I_2.
\tag{20a}
\]
Use \(0\), a maximally entangled rank-one projection, the span of
\(|00\rangle,|11\rangle\), the complement of the rank-one projection, and
\(I_4\), respectively.  Assigning \(Q_{ab}=Q^{(n_{ab})}\) makes (20)
follow from the row and column sums.  Therefore neither rank uniformity nor
blockwise trace zero can be derived from automatic standardness.

### 3.2 Endpoint conditional operators

Define positive operators on the middle copy of \(V\) by
\[
X_a=\operatorname{Tr}_1\bigl((L_a\otimes I)P\bigr),
\qquad
Y_b=\operatorname{Tr}_2\bigl(P(I\otimes R_b)\bigr).
\tag{21}
\]
They obey
\[
0\leq X_a,Y_b\leq2I,\qquad
\operatorname{Tr}X_a=\operatorname{Tr}Y_b=6,
\tag{22}
\]
\[
\sum_aX_a=\sum_bY_b=3I.
\tag{23}
\]
The \(X_a\)'s are block diagonal for the \(R_b\)-decomposition, while the
\(Y_b\)'s are block diagonal for the \(L_a\)-decomposition.

On three sites put \(p=P_{12}\), \(q=P_{23}\), and
\[
e=\frac32pqp-\frac12p.
\tag{24}
\]
This is the full common-one projection of \(p,q\).  Since
\[
\Pi_{ab}=L_a\otimes I\otimes R_b
\]
commutes with both \(p\) and \(q\), the endpoint compression
\[
e_{ab}=\Pi_{ab}e
\tag{25}
\]
is a projection.  Let
\[
k_{ab}=\operatorname{rank}e_{ab}.
\tag{26}
\]
The one-sided controlled-sector theorem gives the exact margins
\[
\boxed{
\sum_bk_{ab}=9,\qquad
\sum_ak_{ab}=9.
}
\tag{27}
\]
Inside the \(24\)-dimensional endpoint corner \(\Pi_{ab}V^{\otimes3}\),
the two projections \(p,q\) both have rank \(12\).  Their complete
two-projection decomposition is
\[
\boxed{
\begin{array}{c|ccc}
&\text{common one}&\text{generic blocks}&\text{common zero}\\ \hline
\text{multiplicity}&k_{ab}&12-k_{ab}&k_{ab}.
\end{array}
}
\tag{28}
\]
Here “generic blocks” counts two-dimensional blocks with squared
principal-angle cosine \(1/3\).

Taking the trace of \(pq\) in the endpoint corner in two ways yields
\[
\boxed{
\operatorname{Tr}(X_aY_b)
=4+\frac23k_{ab}.
}
\tag{29}
\]
Equivalently,
\[
\boxed{
k_{ab}
=3+\frac32\operatorname{Tr}\bigl((X_a-I)(Y_b-I)\bigr).
}
\tag{30}
\]

Equations (27)--(30) expose the exact missing spatial datum.  The matrix
\((k_{ab})\) is an arbitrary *a priori* nonnegative integral
\(3\times3\) matrix with row and column sums \(9\), constrained further by
the existence of the nine cells and their shared middle-site position.
The uniform value
\[
k_{ab}=3
\tag{31}
\]
is only one transportation solution.  It follows, for example, if all
\(X_a=I\) or all \(Y_b=I\), but it does not follow from the rank-two atoms
alone.

There are \(1540\) labelled nonnegative integral \(3\times3\) matrices
with the margins (27), or \(56\) orbits under row permutations, column
permutations, and transpose.  Each entry \(0\leq k_{ab}\leq9\) admits the
abstract \(24\)-dimensional two-projection block (28).  This does not build
a spatially shifted pair \(P_{12},P_{23}\), but it proves that endpoint
block arithmetic alone cannot select the uniform matrix.

If the left algebra is upgraded from its diagonal
\(\mathbb C^3\) to \(M_3\otimes I_2\), its matrix units make the three
\(X_a\)'s unitarily identical.  Equation (23) then forces \(X_a=I\) and
(29) forces (31).  Theorem 2.1 shows that this upgraded branch is
nevertheless empty.

## 4. The two rank-two color decompositions cannot share an atom

The other exactly tractable endpoint of the relative-position problem is
when the two central color algebras share even one of their three atoms.

### Theorem 4.1

There is no \(d=6\) exceptional solution for which
\[
\boxed{L_a=R_b\text{ for some }a,b.}
\tag{32}
\]

### Proof

Relabel the shared atom as
\[
W=L_0V=R_0V,\qquad \dim W=2.
\]
The two-site cell
\[
H_{00}=H\big|_{W\otimes W}
\]
is a Hermitian involution.  The subspace \(W^{\otimes3}\) is invariant
under both adjacent copies of \(H\), so \(H_{00}\) is a base-dimension-two
solution of the same cubic relation.  Its negative spectral rank is
\(0,1,2,3\), or \(4\).

- Ranks \(1\) and \(3\) are impossible by the rank-one compression
  determinant lemma: the cubic forces the two eigenvalues of
  \(Q_{12}Q_{23}Q_{12}\) on \(\operatorname{ran}Q_{12}\) into
  \(\{1,1/3\}\), so its determinant is at least \(1/9\), while writing
  \(Q=|\operatorname{vec}S\rangle\langle\operatorname{vec}S|\) gives the
  upper bound \(|\det S|^4\leq1/16\).  Complementation treats rank \(3\).
- Rank \(2\) is the established empty exceptional class in base dimension
  two.

Consequently
\[
H_{00}=\varepsilon I_4,\qquad\varepsilon\in\{+1,-1\}.
\tag{34}
\]

For every right color \(b\), the subspace
\[
W\otimes W\otimes R_bV
\]
is invariant.  On it, the first reflection is the scalar
\(X=\varepsilon I\), while the second is
\(Y=I_W\otimes H_{0b}\).  Since \(X^2=Y^2=I\),
\[
XYX-YXY=Y-X.
\]
The cubic relation says
\[
Y-X=\frac13(X-Y),
\]
hence \(Y=X\) and
\[
H_{0b}=\varepsilon I_4
\qquad(b=0,1,2).
\tag{35}
\]

Automatic standardness now gives an immediate contradiction.  Restrict
\(\operatorname{Tr}_2H=0\) to the first-site atom \(W=L_0V\).  The
right-color block decomposition and (35) give
\[
\begin{aligned}
0
&=\sum_{b=0}^2\operatorname{Tr}_{R_bV}H_{0b}\\
&=\sum_{b=0}^2 2\varepsilon I_W
=6\varepsilon I_W,
\end{aligned}
\tag{36}
\]
which is impossible. \(\square\)

This theorem explains exactly why numerical optimization of the relative
unitary often collapses toward a color permutation but stops at a nonzero
residual.  More strongly, any solution in the central-atom branch must
put the two rank-two decompositions in a relative position with no common
two-dimensional atom.  In particular, the relative unitary cannot
normalize either color algebra.

## 5. Remaining branch after the theorems

For \(d=6\), the exact factor no-go removes the algebra type
\[
M_3\otimes I_2
\]
from either leg.  The principal non-scalar survivor is therefore the
central rank-two color algebra
\[
\mathbb C^3\cong
\mathbb C I_2\oplus\mathbb C I_2\oplus\mathbb C I_2,
\tag{37}
\]
possibly paired with itself in arbitrary relative position.

The unrestricted version of this survivor consists of:

1. two decompositions of \(\mathbb C^6\) into three two-dimensional
   subspaces, related by an arbitrary unitary in \(U(6)\);
2. nine arbitrary projections \(Q_{ab}\in M_4(\mathbb C)\), with ranks
   satisfying (18)--(20);
3. the full-intersection conditions (24)--(30) in every endpoint corner;
4. the generic \(1/3\)-angle blocks, not merely the intersection ranks.

The earlier mixed-color search imposed both
\[
n_{ab}=2
\]
and a relative unitary of the special form \(U_3\otimes I_2\).  Its
negative numerical result therefore does not classify (37).

No nonexistence theorem for the full central-atom branch is claimed here.
The exact gain is the removal of the factor branch and a corrected,
basis-free target for the remaining three-color cell problem.

## 6. Broader numerical falsifier for the central-atom branch

The earlier `mixed 3x2` search restricted the relative unitary to
\(U_3\otimes I_2\).  The new script

```text
scripts/d6_threecolor_full_relative_search.py
```

keeps nine arbitrary signature-\((2,2)\) reflection blocks but optimizes
the relative position over the full group \(U(6)\).  Thus it removes the
coordinate-factor restriction, while still retaining the proper subansatz
\(n_{ab}=2\).

The implementation exactly reassembles the retained \(d=4\) mixed-color
candidate, with reassembly difference \(0\) and cubic residual
\[
9.835750823083491\times10^{-11}.
\]
A separate combined block/\(U(6)\) finite-difference check is retained in
`results/d6_threecolor_full_relative_gradient_check.txt`.

Four reproducible \(d=6\) runs used seeds
\[
26072961,\quad26072962,\quad26072963,\quad26072964.
\]
One began at \(F_3\otimes I_2\), and three used random full unitaries.  The
final residuals were
\[
6.016164130958445,\quad
12.846575404445833,\quad
11.066163490720236,\quad
6.010858542676606.
\]
The complete logs are in
`results/d6_threecolor_full_relative_runs.jsonl`.

This is negative numerical evidence only.  It neither proves
nonexistence in the all-rank-two-cell subansatz nor addresses the other
rank matrices allowed by (18)--(20).

### 6.1 All nine cell-rank orbits

The companion script

```text
scripts/d6_threecolor_rankpattern_search.py
```

removes the remaining rank-\(2\)-per-cell restriction.  For each of the
nine orbits among the \(217\) tables, it initializes an arbitrary
Hermitian reflection of the prescribed negative rank in every
four-dimensional cell and varies both all nine cell reflections and the
relative position in the full group \(U(6)\).  The iterations preserve
Hermiticity, involutivity, the nine cell ranks, and total trace zero.
They do not impose scalar partial traces as an extra numerical constraint;
this deliberately avoids excluding a candidate through a potentially
incorrect implementation of a condition that is already automatic at
zero cubic residual.

The seeds and search budget were fixed before the runs in
`results/d6_threecolor_rankpattern_seed_manifest.json`.  One run in each
orbit gave:
\[
\begin{array}{c|c}
\text{orbit}&\text{final cubic residual}\\ \hline
0&14.587306030418496\\
1&14.605934866804485\\
2&14.219218422935047\\
3&13.856406460551014\\
4&16.552374914369093\\
5&13.980392492726544\\
6&12.708559374193320\\
7& 6.000000000000004\\
8&11.060368577447303
\end{array}
\]
The joint block/\(U(6)\) descent direction was checked against an
independently assembled directional derivative; the \(10^{-6}\) central
difference had relative error
\[
7.013199327717132\times10^{-9}.
\]

These nine runs now sample every discrete cell-rank orbit, but only at one
initial point per orbit.  They are therefore still negative numerical
evidence, not an exhaustive certificate even within the
\(\mathbb C^3/\mathbb C^3\) branch.  In particular, the residual \(6\)
stationary point in orbit \(7\) is not a solution.

## 7. Exact replay

The independent verifier is

```text
/Users/alec/Documents/Math/.venv/bin/python \
  verifiers/verify_factor_m3_opposite_control_no_go.py
```

It checks:

- the Pauli coefficient identity (8) on independent exact matrices;
- that the three coefficients are the three individual commutators;
- an exact balanced \(d=6\) factor-form involution and its opposite
  rank-one control projections;
- both scalar partial traces of that guard;
- a nonzero exact cubic coefficient, confirming that standardness and the
  commutant pattern alone are not being mistaken for Yang--Baxter;
- the divisibility contradiction \(8\nmid36\);
- the semimagic endpoint bookkeeping (19), (27), and (28).
- the rank-one determinant gap and scalar propagation used in the shared
  color theorem.  The rank-two diagonal-cell case is explicitly recorded
  as a dependency on the established empty \(d=2\) exceptional class.

The guard is deliberately not an exceptional solution.  Its role is to
exercise every tensor orientation and to prevent a silent swap of the
left and right commutants.

The full-\(U(6)\) numerical runs are replayed by

```text
/Users/alec/Documents/Math/.venv/bin/python \
  scripts/d6_threecolor_full_relative_search.py \
  --seed 26072961 --mixing lifted_fourier --max-iterations 1200 \
  --progress-every 100 \
  --output results/d6_threecolor_full_relative_runs.jsonl

for seed in 26072962 26072963 26072964; do
  /Users/alec/Documents/Math/.venv/bin/python \
    scripts/d6_threecolor_full_relative_search.py \
    --seed "$seed" --mixing random --max-iterations 1200 \
    --progress-every 200 \
    --output results/d6_threecolor_full_relative_runs.jsonl
done

PYTHONPATH=scripts /Users/alec/Documents/Math/.venv/bin/python \
  scripts/check_d6_threecolor_full_relative_gradient.py
```

The all-rank-pattern falsifier is replayed by

```text
for orbit in 0 1 2 3 4 5 6 7 8; do
  seed=$((26073600 + orbit))
  /Users/alec/Documents/Math/.venv/bin/python \
    scripts/d6_threecolor_rankpattern_search.py \
    --rank-pattern-index "$orbit" --seed "$seed" \
    --max-iterations 800 --progress-every 200 \
    --output results/d6_threecolor_rankpattern_runs.jsonl
done

/Users/alec/Documents/Math/.venv/bin/python \
  scripts/check_d6_threecolor_rankpattern_gradient.py
```

Provenance:

- work began from commit
  `5da3dcfe4285e45506a1c38df080642e7f3fda61`;
- run completion: `2026-07-29 00:28 PDT`;
- platform and dependency versions are printed in every start record;
- SHA-256, full-\(U(6)\) search:
  `c1a96aa5329d71cf124016208f8fc598c10198fa21b58ac759b87c84bab38937`;
- SHA-256, raw run log:
  `fff243097a85cc9af6b9be54968dfd336afc4d7173d8d7981796c12c844a4dbc`;
- SHA-256, gradient/calibration script:
  `8cf02bf4fb4a684c665fd6167c6d53db571723675f420d0401444f11a45199b6`;
- SHA-256, gradient/calibration record:
  `e7def137406375ac767a3ae962b076de5379dc1708d14df504ca1372182737cc`;
- SHA-256, exact verifier:
  `9b5d98943babe489817036ec5fc0e91e05cc17263ac2f21b9369c19e643cd87d`;
- SHA-256, exact verifier output:
  `c218a897d5e65d194b8a38bd7f24350218db22bf06c881c241e52d3b54914f00`.
- SHA-256, all-rank-pattern search:
  `51b2e87f5fe36888d0cb47575734a7352b0f79c1bd48122a748c9cfc7797355f`;
- SHA-256, all-rank-pattern run log:
  `6ee2f054a4f3eb733f259f7be8d7e5683f7d5b85f6a42f8eef70e85d733d4936`;
- SHA-256, all-rank-pattern gradient guard:
  `f91e8d4c8526729196037127267bda9ec1fb0bd32663451e8dfcb1f973f9c7f1`;
- SHA-256, all-rank-pattern gradient record:
  `bfd95600b7d7c77dfc2461ec9967efc764492d7a7fc7237bfe65ad65914d460b`.

No external communication was made.
