# The rank-one no-promotion pair selector

## 1. Exact split and claim boundary

The two-active atlas has 310 ordered support pairs with at least one
closed rank-one flat phase. Exactly 77 of them also have an
affine-feasible two-active promotion failure. Removing those gives

\[
 310-77=233.
\tag{1.1}
\]

For all 233 pairs, every affine-feasible failed descriptor with at least
two active coordinates is now handled by one common rate-corrected
factorial potential:

- every two-active failure is a rank-one flat episode covered by Theorem
  1.1 of *rank_one_corrected_factorial_endpoint.md*;
- there is no two-active promotion failure and no rank-two failure;
- the all-active branch is either one of 154 safe reversible
  rate-adjusted pairs, one of 67 directed-triple factorial-linear pairs,
  or absent for twelve pairs; and
- on all-active passing descriptors the fixed linear correction has bounded
  jump increments and does not change the Anderson--Kim tier descent.

The all-active/two-active compatibility certificate proves that the
whole-top support is the same in both dimensions. The finite selector
also checks the stronger fact needed here: each of the 310 rank-one pairs
has one common whole-top mask across all its rank-one descriptors.

Thus the 233-pair statement is a certified
**dimension-at-least-two common-potential theorem**. It is not automatically
a recurrence theorem because 92 of the 233 pairs still have an
affine-feasible one-active failed descriptor. The recently refuted
universal one-active old-debt theorem is not used here.

### 1.1 Discrete transfer on the 154 reversible all-active pairs

The all-active Proposition 5.2 of
*three_active_shell_gluing_gate.md* is written for the continuous
rate-adjusted entropy

\[
 U_\theta(x)=\sum_i\left[
   x_i\left(\log{x_i\over\theta_i}-1\right)+\theta_i
 \right],
\tag{1.2}
\]

whereas the rank-one endpoint theorem uses the exact discrete potential

\[
 {\cal F}_\theta(x)=\sum_i\{\log(x_i!)-x_i\log\theta_i\}.
\tag{1.3}
\]

The following transfer is needed before these can be called one common
potential.

There is an exact discrete proof which is stronger than a formal Stirling
comparison. Write \(z=y+\zeta\), let
\(\alpha=\kappa_{yz}\), \(\beta=\kappa_{zy}\), and put

\[
 \lambda(x)=\alpha(x)_{\underline y},\qquad
 \mu(x)=\beta(x)_{\underline z}.
\tag{1.4a}
\]

Detailed balance of the correction in (1.3), the exact jump identity
(2.2) of *rank_one_corrected_factorial_endpoint.md*, and
\(\log u\le u-1\) give

\[
\begin{split}
 \lambda(x)\Delta_\zeta{\cal F}_\theta(x)
 &\le\mu(x+\zeta)-\lambda(x),\\
 \mu(x)\Delta_{-\zeta}{\cal F}_\theta(x)
 &\le\lambda(x-\zeta)-\mu(x).
\end{split}
\tag{1.4b}
\]

Therefore, retaining only enabled terms,

\[
 {\cal L}_T{\cal F}_\theta(x)
 \le\beta\{(x+\zeta)_{\underline z}-(x)_{\underline z}\}
   +\alpha\{(x-\zeta)_{\underline y}-(x)_{\underline y}\}.
\tag{1.4c}
\]

Each bracket is a bounded first finite difference of a falling-factorial
polynomial of degree at most two. Its positive part is a finite sum of the
changed-coordinate curvature-cofactor monomials (with a bounded boundary
remainder). Thus Proposition 5.2's cofactor hypothesis makes (1.4c)
\(O(\beta_n)\) directly. The forced lower-linkage exit, evaluated with the
exact factorial jump identity, has drift divided by \(\beta_n\) tending
to minus infinity. This already proves the discrete all-active theorem.

> **Lemma 1.1 (Stirling finite-difference transfer).** Let
> \(D_\theta={\cal F}_\theta-U_\theta\), up to an irrelevant additive
> constant. For every reaction jump \(\nu\) in the binary complex set,
> \[
>  |D_\theta(x+\nu)-D_\theta(x)|
>  \le C_\nu\sum_{i:\nu_i\ne0}{1\over x_i\vee1}.
> \tag{1.4}
> \]
> Consequently every reversible all-active pair satisfying the
> curvature-cofactor hypothesis of Proposition 5.2 also satisfies
> \[
>  {\cal L}{\cal F}_\theta(x_n)\longrightarrow-\infty
> \tag{1.5}
> \]
> on each of its failed all-active exact-tier sequences. The same
> \({\cal F}_\theta\) retains the Anderson--Kim descent on every passing
> sequence.

To prove (1.4), put

\[
 d(m)=\log(m!)-m\log m+m,\qquad d(0)=0.
\tag{1.6}
\]

For a unit increment,

\[
\begin{split}
 d(m+1)-d(m)
 &=1-m\log(1+1/m)=O((m\vee1)^{-1}),
\end{split}
\tag{1.7}
\]

and the unit decrement is the same estimate shifted by one. Every binary
reaction changes a coordinate by at most two, so telescoping proves
(1.4), including the finite boundary values after enlarging \(C_\nu\).

Now let \(T=\{y,z\}\) be the flat reversible all-active top, let
\(\alpha_n=x_n^y\asymp x_n^z\), and let
\(\beta_n=\max_{u\in R}x_n^u\) for the lower linkage. By (1.4),

\[
 |{\cal L}_TD_\theta(x_n)|
 \le C\alpha_n\sum_{i:(z-y)_i\ne0}{1\over x_{n,i}\vee1}.
\tag{1.8}
\]

For every changed coordinate, the corresponding
\(\alpha_n/(x_{n,i}\vee1)\) is, up to a bounded flat-tier factor, the
curvature-cofactor monomial in Proposition 5.2. Its certified hypothesis
makes (1.8) \(O(\beta_n)\). Every lower propensity is at most
order \(\beta_n\), and (1.4) is bounded globally, so

\[
 ({\cal L}_RD_\theta(x_n))^+=O(\beta_n).
\tag{1.9}
\]

Equivalently, the continuous-entropy proof supplies the forced lower exit

\[
 {{\cal L}_RU_\theta(x_n)\over\beta_n}
 \longrightarrow-\infty,
\tag{1.10}
\]

while \({\cal L}_TU_\theta=O(\beta_n)\). Equations
(1.8)--(1.10) prove (1.5).

On a passing exact-tier sequence, the forced descending-source edge has
negative reward of order \(-g_n\) after normalization by its maximal
source propensity. Equation (1.4) adds only a bounded normalized term;
every positive lower-tier edge is still controlled by
\(g e^{-g}\). Thus replacing \(U_\theta\) by
\({\cal F}_\theta\) does not change the ordinary Anderson--Kim
conclusion. This proves that the potential used by the two-active endpoint
is literally the potential used in the all-active and passing regions.

## 2. The 141-pair recurrence theorem

The feasible-failure active-count profiles of the 233 pairs are

\[
\begin{array}{c|r}
\text{active counts appearing}&\text{pairs}\\ \hline
\{1,2,3\}&92\\
\{2,3\}&129\\
\{2\}&12 .
\end{array}
\tag{2.1}
\]

Therefore exactly

\[
 233-92=141
\tag{2.2}
\]

pairs have no one-active failed descriptor. Their all-active split is

\[
 72+57+12=141,
\tag{2.3}
\]

for safe reversible, directed triple, and no all-active failure,
respectively.

### Theorem 2.1 (pair-level common-potential composition)

For each of these 141 pairs, fix the potential

\[
 {\cal F}_*(x)=\sum_i\log(x_i!)+\ell_*\mathbin{\cdot}x
\tag{2.4}
\]

selected by its unique rank-one top mask and actual rates. Fix a closed
irreducible population class \(\Gamma\). Then every divergent exact-tier
subsequence in \(\Gamma\) has one of the following alternatives:

1. it is a two-active failed flat sequence, and the audited physical
   episode has expected \({\cal F}_*\)-drift tending to \(-\infty\);
2. it is an all-active failed sequence, and the audited all-active
   generator theorem, together with Lemma 1.1 in the reversible case,
   gives \({\cal L}{\cal F}_*\to-\infty\); or
3. it is a passing descriptor, and the ordinary descending-source
   argument is unchanged by the fixed linear correction.

There is no feasible one-active failed sequence by definition of the
141-pair selector. A zero-active population sequence lies in a finite
set. The ten possible *zero_boundary_phase_only* incidences do not create
a fourth alternative in \(\Gamma\): at their displayed inactive cap the
lower linkage is disabled, the top linkage preserves that zero coordinate
and \(H_w\), and Proposition 4.1 of
*two_active_promotion_phase.md* confines \(\Gamma\) to one finite top
shell. Thus no divergent sequence in a fixed \(\Gamma\) realizes such an
incidence.

Lemma 3.1 of *physical_entropy_gluing_lemma.md* turns the
sequence-local flat episodes into a finite exceptional set, and Theorem
2.1 there glues them to the generator-good region using the same proper
potential (2.4).

Population-increasing reactions in a binary network have at most affine
propensity: a bimolecular source cannot increase total molecular count.
Comparison with a linear pure-birth chain gives nonexplosion. The
classwise corollary of the common-entropy gluing theorem therefore gives
positive recurrence on every closed irreducible class.

An independent replay checked the pair selector, unique common top mask,
the discrete reversible transfer in Lemma 1.1, the directed-triple branch,
all passing descriptors, the sequence-to-finite-exception step, endpoint
and duration integrability, common-potential gluing, nonexplosion, and the
classwise positive-return conclusion. It found no remaining gap.
It also checked exact disjointness from the 151 affine, fourteen rank-two,
51 all-active-only, and twelve \(H_b\)-seam selectors.

Therefore every closed irreducible class of each of these 141 support pairs
is positive recurrent. The other 92 pairs in the 233-pair local branch are
not included: each retains at least one affine-feasible one-active failed
descriptor.

## 3. Exact hashes and reproduction

The 233-pair dimension-local fingerprint is

    afc4f8e121cdd6893f31edfdc5461f4d5f4d5b8340e37b64a222adcd7994114c

The 141-pair recurrence fingerprint is

    bc3540674c5ec8eef96fe4272e15c1f3d220a06fe7ad890189d2f745e6c22e67

The full selector-row fingerprint is

    6b3bc0cfb7dfae535f40d90a6d8faa6e7056902f75e3a578567652397a008809

Run

    PYTHONPATH=src python3 -B src/rank_one_no_promotion_branch.py
    PYTHONPATH=src python3 -B -m unittest \
      tests/test_rank_one_no_promotion_branch.py -v

The certificate turns on the audited dimension-at-least-two
common-potential and exact 141-pair recurrence flags. Global T3-2 remains
uncertified.
