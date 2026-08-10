# Stoichiometric feasibility of the twelve tier gates

## 1. Scope and outcome

The twelve rows in the analytic gate table are support-level tier
obstructions.  Their original realizing sequences were allowed to move
between affine stoichiometric classes.  A tier sequence used on a fixed
closed population class cannot do that.

This note supplies the exact missing filter.  For a support pair \(P\), let
\(S(P)\subseteq\mathbb R^3\) be its full stoichiometric subspace.  Given a
tier descriptor, the filter decides whether one nonnegative sequence
realizing that descriptor can be contained in one affine set

\[
 (x_*+S(P))\cap\mathbb R_{\ge0}^3.                         \tag{1.1}
\]

The result of the exhaustive calculation and its classwise Foster
consequence is:

\[
\begin{array}{c|r}
\text{residual support pairs}&2511\\
\text{failing pair--descriptor incidences}&12886\\
\text{affine-stoichiometrically feasible incidences}&9913\\
\text{affine-stoichiometrically impossible incidences}&2973\\
\text{pairs with at least one feasible failing descriptor}&2360\\
\text{pairs with no feasible failing descriptor}&151\\
\text{classwise entropy-Foster closures}&151\\
\text{pairs still requiring another argument}&2360.
\end{array}                                                \tag{1.2}
\]

The last split is \(2169+143\) in the positive-invariant family and
\(191+8\) in the signed family.  Every one of the 151 filtered pairs has
stoichiometric rank two.  Section 4 proves that all 151, not just the
invariant-axis subfamily, are positive recurrent on every closed
irreducible population class.

Feasibility by itself is not a recurrence theorem.  In particular, the 2360
pairs that retain a feasible obstruction are not asserted to be null
recurrent, transient, or positive recurrent.  Feasibility merely says that
affine invariants do not rule out that tier geometry.  The positive
recurrence conclusion for the other 151 uses the absence of *every*
class-feasible failing descriptor, not feasibility of a displayed gate.

## 2. The finite flag criterion

Fix a primitive nonnegative integral descriptor weight

\[
 w=(w_A,w_B,w_C).
\tag{2.1}
\]

Let its distinct positive coordinate levels be

\[
 r_1>r_2>\cdots>r_k>0.
\tag{2.2}
\]

At level \(r\), define

\[
 E_r=\{i:w_i=r\},\qquad
 H_r=\{i:w_i\ge r\},\qquad
 L_r=\{i:w_i<r\}.                                        \tag{2.3}
\]

Thus \(E_r\) is the coordinate block that must begin diverging at the
current order, \(H_r\) contains that block and all higher-order blocks, and
\(L_r\) contains every lower-order or bounded coordinate.

> **Theorem 2.1 (affine tier-feasibility criterion).**  Let
> \(\mathcal A=x_*+S\) be a fixed rational affine stoichiometric class.
> A descriptor is realized by a **real nonnegative sequence** in
> \(\mathcal A\) if
> and only if both of the following hold.
>
> 1. There is a base \(b\in\mathcal A\) having the prescribed eventual
>    values in every zero-weight coordinate: cap zero means \(b_i=0\), cap
>    one means \(b_i=1\), and cap two means \(b_i\ge2\).
> 2. For every positive level \(r\), there is a vector \(v_r\in S\) such
>    that
>    \[
>      (v_r)_i=0\quad(i\in L_r),\qquad
>      (v_r)_i>0\quad(i\in E_r).                           \tag{2.4}
>    \]
>    No sign restriction is imposed on coordinates in \(H_r\setminus E_r\).

For existence in *some* affine class, the base condition is automatic:
take the zero-weight coordinates equal to their displayed caps and define
the affine class through that point.  Hence the support-level enumeration
uses only (2.4).  The implementation also exposes the base test for a
specified \(x_*\).

### 2.1 Why the criterion is necessary

Put

\[
 W_r=S\cap\{v:v_i=0\text{ for }i\in L_r\}.                 \tag{2.5}
\]

Suppose (2.4) fails.  Gordan's theorem of alternatives gives a vector
\(y\in\mathbb R_{\ge0}^{E_r}\), \(y\ne0\), that annihilates the projection
of \(W_r\) onto \(E_r\).  Extend \(y\) by zero outside \(E_r\).
Since

\[
 W_r^\perp
 =S^\perp+\operatorname{span}\{e_i:i\in L_r\},             \tag{2.6}
\]

there is an affine invariant \(q\in S^\perp\) satisfying

\[
 q_i=0\quad(w_i>r),\qquad
 q_i=y_i\ge0\quad(w_i=r),                                 \tag{2.7}
\]

with at least one strict inequality in the second group.  The values of
\(q_i\) at lower levels are unrestricted.

Along a sequence realizing the descriptor, coordinates in \(E_r\) have
the same asymptotic order, all higher coordinates have zero coefficient in
\(q\), and every lower coordinate is negligible relative to that order.
After division by any coordinate in \(E_r\), (2.7) therefore gives a
strictly positive limit for \(q\cdot x_n\).  This contradicts the affine
identity

\[
 q\cdot x_n=q\cdot x_*.
\tag{2.8}
\]

This dual invariant is the exact certificate for the two common failure
mechanisms:

- a nominally active coordinate is constant on every affine class;
- an invariant forces another coordinate to co-diverge at the same order,
  contrary to the displayed one-active or multiscale descriptor.

### 2.2 Why the criterion is sufficient

All spaces and inequalities are rational, so every feasible vector in
(2.4) may be chosen rational and then scaled to an integral vector.  With
\(b\) from the base condition, put

\[
 x(n)=b+\sum_{\ell=1}^k n^{r_\ell}v_{r_\ell}.              \tag{2.9}
\]

For a coordinate \(i\) with \(w_i=r_\ell\), every term of higher degree
vanishes in that coordinate by (2.4), the degree-\(r_\ell\) coefficient is
strictly positive, and all later terms have smaller degree.  Hence

\[
 x_i(n)=(v_{r_\ell})_i n^{w_i}(1+o(1)).                   \tag{2.10}
\]

Every zero-weight coordinate remains at its base value.  The sequence is
therefore nonnegative for all sufficiently large \(n\), stays in the one
affine class \(b+S\), and has

\[
 x(n)^y=C_y n^{w\cdot y}(1+o(1))                          \tag{2.11}
\]

for every enabled complex \(y\).  Equation (2.11) realizes the complete
D-tier partition, including equalities such as \(2w_A=w_B\), while the
base caps realize the exact S-tier availability pattern.  This proves
sufficiency.

## 3. Exact finite implementation

For each level, the program computes a rational basis of \(W_r\).  If its
basis is \(u_1,\ldots,u_d\), condition (2.4) is the finite rational system

\[
 \sum_{j=1}^d a_j(u_j)_i\ge1,\qquad i\in E_r.              \tag{3.1}
\]

Strict positivity is equivalent to (3.1) by homogeneous rescaling.
The certificate solves (3.1) by exact Fourier--Motzkin elimination over
\(\mathbb Q\).  When it is infeasible, the same elimination solves the
dual Gordan system and extends the dual vector to the explicit invariant
(2.7).  Thus every decision has either a primal direction or a dual
invariant witness.

The twelve displayed gate rows form an overlapping greedy cover, not the
complete family of failed descriptors.  It would be invalid to delete a
pair merely because its displayed greedy gate is infeasible: another one of
the 259 exact descriptors might still be both feasible and failing.
Accordingly, the complete pair split in (1.2) checks every one of the
12,886 failing incidences.  The twelve-row table below is reported only to
show how the canonical gate library changes.

## 4. Class-restricted tier-Foster corollary

The finite filter closes precisely the 151 pairs having no feasible failing
descriptor.

> **Corollary 4.1 (classwise entropy Foster).**  Let \(P\) be one of those
> 151 support pairs.  Give each linkage an arbitrary strongly connected
> orientation and arbitrary positive rate constants.  The stochastic
> mass-action CTMC is nonexplosive, and every state in every closed
> irreducible population class is positive recurrent.

### Proof

Fix a closed irreducible class \(\Gamma\).  It lies in one affine
stoichiometric class \(x_*+S(P)\).  If \(\Gamma\) is finite there is nothing
to prove, so suppose it is infinite.

Use the entropy

\[
 V(x)=\sum_{i=A,B,C}\{x_i(\log x_i-1)+1\},                 \tag{4.1}
\]

with \(0\log0=0\).  We claim that

\[
 {\cal L}V(x)\le-1
 \quad\text{for all }x\in\Gamma\setminus K_\Gamma          \tag{4.2}
\]

for some finite \(K_\Gamma\).

If (4.2) failed, there would be an unbounded sequence
\(x_n\in\Gamma\) with \({\cal L}V(x_n)>-1\).  Passing to a subsequence gives
a tier sequence.  The completeness argument for the 259 descriptors
assigns it one exact D-tier/availability descriptor.

If the actual strongly connected orientation had no descending reaction
sourced in the global top S-tier along this sequence, the support-level
universal-orientation test would fail on its descriptor.  The descriptor
would therefore be one of the failing descriptors checked by the present
certificate.  But \(x_n\subset x_*+S(P)\), so necessity in Theorem 2.1
would make that descriptor affine-stoichiometrically feasible.  This
contradicts the defining property of the 151-pair set.  Hence every tier
sequence contained in \(\Gamma\) has a top-S descending source.

The contradiction proof of Theorem 4.2 in Anderson and Kim, *Some network
conditions for positive recurrence of stochastically modeled reaction
networks* (arXiv:1710.11263), is class-local: it begins with an arbitrary
unbounded sequence on which \({\cal L}V>-1\), extracts a tier subsequence,
and proves \({\cal L}V(x_n)\to-\infty\).  It never requires a state outside
that sequence.  Applying that same proof to sequences in \(\Gamma\) gives
(4.2).  The continuous-time Foster theorem applied to the CTMC restricted
to the closed countable class \(\Gamma\) proves positive recurrence.

Finally, the process is nonexplosive.  A reaction with a bimolecular source
cannot increase total population because every complex has molecularity at
most two.  Every population-increasing reaction therefore has source
molecularity zero or one, so the total positive jump intensity is bounded
by \(C(1+A+B+C)\), and all jumps are bounded.  A Yule-process comparison
prevents escape of total population in finite time; on each fixed total
population sublevel there are finitely many states and bounded total rates.
\(\square\)

The exact new branch table is

\[
\begin{array}{c|rrr}
\text{family}&\text{input residual}&
\text{classwise tier-Foster}&\text{remaining}\\ \hline
\text{positive-invariant}&2312&143&2169\\
\text{signed}&199&8&191\\
\text{total}&2511&151&2360.
\end{array}                                                \tag{4.3}
\]

No conclusion is drawn for the 2360 remaining pairs.

## 5. The twelve canonical rows

The columns count canonical pair-orbit representatives in the existing
gate table.  Rows overlap and must not be summed.

| gate | \(w\) | cap | listed | feasible | impossible |
|---|---:|---:|---:|---:|---:|
| G1 | \((0,0,1)\) | \((0,0,2)\) | 653 | 598 | 55 |
| G2 | \((0,1,0)\) | \((0,2,0)\) | 1026 | 933 | 93 |
| G3 | \((0,1,1)\) | \((0,2,2)\) | 37 | 32 | 5 |
| G4 | \((1,1,0)\) | \((2,2,0)\) | 206 | 191 | 15 |
| G5 | \((1,1,1)\) | \((2,2,2)\) | 26 | 20 | 6 |
| G6 | \((1,1,2)\) | \((2,2,2)\) | 54 | 25 | 29 |
| G7 | \((1,2,0)\) | \((2,2,0)\) | 180 | 144 | 36 |
| G8 | \((1,2,1)\) | \((2,2,2)\) | 3 | 1 | 2 |
| G9 | \((1,2,3)\) | \((2,2,2)\) | 23 | 22 | 1 |
| G10 | \((1,3,2)\) | \((2,2,2)\) | 2 | 1 | 1 |
| G11 | \((2,2,1)\) | \((2,2,2)\) | 165 | 159 | 6 |
| G12 | \((2,3,1)\) | \((2,2,2)\) | 23 | 23 | 0 |

The incidence split by number of unbounded coordinates is

\[
\begin{array}{c|rrr}
\#\text{ unbounded coordinates}&\text{failing}&\text{feasible}&
\text{impossible}\\ \hline
1&8365&6256&2109\\
2&3028&2388&640\\
3&1493&1269&224.
\end{array}                                                \tag{5.1}
\]

Thus the largest pruning occurs in the one-active gates, but the affine
flag test also removes multiscale two- and three-active descriptors.

## 6. Pair sets and fingerprints

The pair fingerprints use the existing canonical support-pair encoding.

\[
\begin{array}{c|r|l}
\text{set}&\#&\text{SHA-256}\\ \hline
\text{positive with a feasible failure}&2169&
\mathtt{6763a44c9c312c440997a054f7966347d101e3236cdef9ecb90599226de10458}\\
\text{positive without a feasible failure}&143&
\mathtt{f48882aa1ff52c1594a71fd217fa559492c7010e950285a9fa2e60e02b487b76}\\
\text{signed with a feasible failure}&191&
\mathtt{f5c7a694bec0241a67b5cf588e1d074c11e00fb9ae3fbc1cee5570f84e9b4483}\\
\text{signed without a feasible failure}&8&
\mathtt{aead73fd44d08789019326cffcd706a776addf0cbc841979a3d54e8c80c5f88d}\\
\text{all 151 without a feasible failure}&151&
\mathtt{55e243945f86d106b920a27e2249a20b7077b5dc718ec06918cca4368e4a6c96}.
\end{array}                                                \tag{6.1}
\]

The fingerprint of all 9913 feasible pair--descriptor incidences, encoding
the pair together with the descriptor weight and caps, is

\[
 \mathtt{2ef26eb13a33bf6e4339b92d001ea78c8c63efa6b8a16dfb9e9463c48e686c6b}.
\tag{6.2}
\]

The complete deterministic certificate hash is

\[
 \mathtt{d330193b1a1a835118f5f1ce5c26031ea2948ab5665a2f67ed38ec4dadb3c2f5}.
\tag{6.3}
\]

The executable JSON also records separate feasible and impossible
fingerprints for each of G1--G12 and the histogram of the number of feasible
failing descriptors per support pair.

## 7. Interpretation and limitations

1. Affine impossibility is stronger than failure of the particular explicit
   sequence formerly attached to a gate.  The dual invariant rules out
   every sequence with that descriptor in every affine class of the
   support pair.
2. Affine feasibility is weaker than realizability in a particular closed
   irreducible communication class.  Boundary disabling, lattice
   congruences, or class-specific constant coordinates can remove more
   sequences.  The fixed-class base test captures affine cap compatibility,
   but it does not pretend to solve reachability.
3. The 151-pair set has no affine-feasible failed descriptor among the
   complete 259-descriptor list.  Corollary 4.1 converts exactly this
   absence into a classwise recurrence branch.
4. The remaining 2360 pairs have at least one feasible failed descriptor.
   No stochastic conclusion follows.  They still require a valid
   multi-step Foster, service, averaging, or lower-dimensional argument.

## 8. Reproduction

Run

    PYTHONPATH=src python3 src/stoichiometric_gate_feasibility.py
    PYTHONPATH=src python3 -m unittest \
      tests/test_stoichiometric_gate_feasibility.py -v

The tests verify the primal and dual witnesses for every failed incidence,
the fixed-class cap condition, all counts in (1.2), (4.3), and (5.1), the
twelve canonical rows, and the hashes in Section 6.
