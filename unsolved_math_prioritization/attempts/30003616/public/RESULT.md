# Five approaches to the Fibonacci spectral-ray question

**Status: `unsolved 5/5`.** There is no claimed full solution and no Fibonacci-potential counterexample. Set-theoretic examples below refute proposed inference rules only.

## Exact problem and conventions

Let `α=(sqrt(5)-1)/2` and, at phase zero, put

\[
\omega_n=\lfloor(n+1)\alpha\rfloor-\lfloor n\alpha\rfloor,
\qquad n\in\mathbb Z.
\]

Given real `f0,f1 in L²([0,1))`, extend the pieces by zero outside their tile and set `Vω(n+x)=fωn(x)` for `0<=x<1`. For `λ>0`, let `Hλ=-d²/dx²+λVω` be the canonical lower-semibounded self-adjoint form operator on `L²(R)`, and write `Σλ=σ(Hλ)`. The operator of interest is

\[
L_{\lambda_1,\lambda_2}
=H_{\lambda_1}\otimes1+1\otimes H_{\lambda_2}
=-\Delta+\lambda_1V_\omega(x)+\lambda_2V_\omega(y)
\quad\hbox{on }L^2(\mathbb R^2).
\]

The target is

\[
\forall f_0,f_1\in L^2([0,1);\mathbb R),\quad
\forall\lambda_1,\lambda_2>0,\quad
\exists E_*\in\mathbb R:\quad [E_*,\infty)\subseteq\sigma(L_{\lambda_1,\lambda_2}).
\]

If the question is phrased after fixing the tile pair, the same universal tile-pair scope is understood. There is no spatial half-line, no Dirichlet/Neumann/Robin choice, and no boundary eigenvalue question. The phase-zero convention is the source's convention; minimality gives the same full-line spectrum throughout the Fibonacci hull.

The finite tile family has uniformly bounded local `L²` norms. The one-dimensional potential forms are infinitesimally form-bounded relative to the kinetic form, so the stated lower-semibounded realizations are well defined. Nothing in this package assumes that the tile functions are bounded or positive.

## Approach 1: tensor reduction and exact spectral scope

### Proposition 1

\[
\sigma(L_{\lambda_1,\lambda_2})=\Sigma_{\lambda_1}+\Sigma_{\lambda_2}.
\]

**Proof.** The joint spectral theorem for operators on the two tensor factors gives the closure of the Minkowski sum as the spectrum. That sum is already closed: if `an+bn` converges and `an>=m1`, `bn>=m2`, both sequences are bounded above as well as below. A subsequence has limits `a in Σλ1`, `b in Σλ2`, with the prescribed sum. For the other inclusion directly, tensor products of approximate eigenvectors for `a` and `b` are approximate eigenvectors for `a+b`. This also checks the use of the form-sum realization. ∎

Each one-dimensional spectrum is perfect: in the aperiodic case the cited continuum Fibonacci theorem gives Cantor spectrum; in the periodic case the usual band spectrum is perfect. A sum of a nonempty perfect set with another nonempty set, when closed, is perfect: keep one summand fixed and approach the other by distinct points. Consequently the full-plane spectrum has no isolated spectral points, and

\[
\sigma_{\rm ess}(L_{\lambda_1,\lambda_2})=\sigma(L_{\lambda_1,\lambda_2})
\]

for the usual essential spectrum obtained by deleting isolated eigenvalues of finite multiplicity. This statement does **not** assert absolute continuity, nor does it exclude embedded eigenvalues solely from perfectness.

For equal constant pieces `f0=f1=c`, Fourier transformation gives the completely explicit case

\[
\sigma(L_{\lambda_1,\lambda_2})=[(\lambda_1+\lambda_2)c,\infty).
\]

The established constant-tile result for unequal pieces and equal couplings is substantially deeper. Neither the tensor identity nor perfectness fills gaps in a sum of two Cantor spectra.

**Outcome and remaining gap.** Exact reduction and domain clarification, but the entire Minkowski-sum ray problem remains. A boundary-condition or discrete-lattice calculation would not address this target.

## Approach 2: a uniform high-energy invariant estimate

This approach gives a quantitative partial result for arbitrary pieces; it does not produce thickness.

For real `qj in L¹([0,ℓj])`, let `Aj(E)` be the transfer matrix across the `j`th tile for `-u''+qju=Eu`. Define

\[
x=\tfrac12\operatorname{tr} A_0,
\quad y=\tfrac12\operatorname{tr} A_1,
\quad z=\tfrac12\operatorname{tr}(A_0A_1),
\qquad I(E)=x^2+y^2+z^2-2xyz-1.
\]

The order in the product does not affect its trace. The transfer matrices have determinant one.

### Proposition 2

Put `M=||q0||₁+||q1||₁`. For every real `E>0`,

\[
\boxed{|I(E)|\leq\big(e^{M/\sqrt E}-1\big)^2.}
\]

In particular `I(E)=O(E^{-1})` as `E` tends to infinity. The estimate holds off the spectrum too; it is an absolute-value estimate and does not assert positivity there.

**Proof.** Write `k=sqrt(E)` and use the state vector `(u,u'/k)^t`. This is the **same** conjugation `diag(1,1/k)` for both tiles, so all the traces defining `I` are unchanged. In this normalization the fundamental matrix satisfies

\[
U'_j(t)=\left(kJ+\frac{q_j(t)}{k}P\right)U_j(t),\qquad
J=\begin{pmatrix}0&1\\-1&0\end{pmatrix},\quad
P=\begin{pmatrix}0&0\\1&0\end{pmatrix}.
\]

Use the Euclidean operator norm. The free propagator `R(kt)=exp(ktJ)` is orthogonal, and `||P||=1`. The integral equation and Grönwall's inequality give, for `0<=t<=ℓj`,

\[
\|U_j(t)\|\leq\exp\left(k^{-1}\int_0^t|q_j(s)|ds\right),
\quad
\|U_j(t)-R(kt)\|\leq
\exp\left(k^{-1}\int_0^t|q_j(s)|ds\right)-1.
\]

These bounds require only integrability and are uniform in `t`. At the endpoints write `Aj=Rj+Dj` and `δj=exp(||qj||₁/k)-1`. Then `||Dj||<=δj`. The rotations `R0,R1` commute, even when the lengths differ. Expanding the additive commutator yields

\[
\|A_0A_1-A_1A_0\|
\leq2(\delta_0+\delta_1+\delta_0\delta_1)
=2(e^{M/k}-1).
\]

For determinant-one two-by-two matrices, the Fricke identity is

\[
4I=-\det(A_0A_1-A_1A_0).
\]

It follows from Cayley–Hamilton, or direct polynomial expansion subject to the two determinant-one identities. Since `|det B|<=||B||²` for a two-by-two matrix in this norm, the boxed estimate follows. ∎

The exact polynomial identity is also checked in `checks/check.py`; this finite check is a supplement to, not a replacement for, the argument.

### Corollary 2.1: local-dimension consequence

In the aperiodic continuum Fibonacci setting where the established dimension formula applies,

\[
\dim_H^{\rm loc}(\Sigma;E)=D(I(E)),\qquad
1-D(I)\leq C\sqrt I\quad(0\leq I\leq I_0).
\]

Here `D` is the universal function in Fillman–Mei, Theorem 2.3, recalling Damanik–Fillman–Gorodetski; `I(E)>=0` for spectral energies is another imported theorem. Therefore, for all sufficiently large `E in Σ`,

\[
\dim_H^{\rm loc}(\Sigma;E)
\geq1-C(e^{M/\sqrt E}-1)
\geq1-C_q E^{-1/2}.
\]

For `qj=λfj`, `M=λ(||f0||₁+||f1||₁)`. On every bounded coupling interval the invariant bound and the resulting large-energy estimate can be made uniform. Constants are independent of the phase. No assertion of uniformity for all unbounded positive couplings is made. The dimension conclusion for periodic pieces can instead be read directly from band structure; the aperiodic dimension theorem is not silently applied to a periodic model.

**Why this does not close the problem.** The trace-map thickness argument needs control of relative variation, of the form `|dI/dk|<=C I` on suitable long windows, together with positivity and geometric transversality. An upper bound on `|I|` does not give this. Even an analytic function such as `k^{-2} sin²k` has an upper bound `O(k^{-2})` while its logarithmic derivative has poles at arbitrarily large zeros. This example is a logical warning, not a proposed spectral invariant for the target. No verified all-shape family of thickness windows has been supplied.

## Approach 3: test whether large dimension alone can fill the ray

The following exact counterexample shows that even maximal local dimension everywhere, zero measure, and bounded gaps do not imply that a self-sum contains any interval.

### Proposition 3

There is a closed perfect semibounded set `S`, with bounded gaps and local Hausdorff dimension one at every point, such that `S+S` has Lebesgue measure zero.

**Construction.** For `j>=1`, put `bj=2(j+1)`, `Qn=product(j=1..n) bj=2^n(n+1)!`, and define

\[
K=\left\{\sum_{j=1}^\infty\frac{d_j}{Q_j}:d_j\in\{0,1,\ldots,j\}\right\},
\qquad S=\mathbb Z_{\geq0}+K.
\]

The set `K` is compact and perfect. Since `dj <= (bj-1)/2` and the full mixed-radix tail telescopes, `K subset [0,1/2]`, and a level-`n` cylinder has diameter at most `1/(2Qn)`. There are `Nn=(n+1)!` such cylinders, with distinct left endpoints in the lattice `Qn^{-1}Z`. In particular `K` has measure zero, because their total length is at most `2^{-n-1}`.

**Dimension.** Give each allowed digit independent uniform mass. Every level-`n` cylinder has mass `1/Nn`. If an interval `J` of length `r` satisfies `1/Qn<=r<1/Q(n-1)`, it meets at most `rQn+2<=3rQn` cylinders. Thus

\[
\mu(J)\leq3\,2^n r.
\]

For every fixed `0<s<1`,

\[
2^n r^{1-s}\leq2^n Q_{n-1}^{-(1-s)}\longrightarrow0,
\]

since `Q(n-1)=2^{n-1}n!`. Enlarging a constant for finitely many initial scales gives `μ(J)<=Cs r^s`. The mass-distribution principle proves `dim_H K>=s` for every `s<1`, hence `dim_H K=1`. The same proof with a finite digit prefix fixed applies to each cylinder. Every neighborhood of every point of `K` contains a sufficiently small cylinder, so its local Hausdorff dimension is one.

**Self-sum.** Addition of two expansions produces digits `0,...,2j=bj-2`, without carrying. At level `n`, `K+K` is covered by

\[
D_n=\prod_{j=1}^n(2j+1)
\]

intervals of length at most `1/Qn`. Their total length is

\[
\frac{D_n}{Q_n}=\prod_{j=1}^n\left(1-\frac1{2j+2}\right)\longrightarrow0,
\]

because the sum of the omitted fractions diverges. Thus `K+K` is a compact null set. The locally finite union `S` is closed and perfect; it contains every nonnegative integer, so all gaps have length at most one. Its local dimensions are one. Finally,

\[
S+S=\mathbb Z_{\geq0}+(K+K)
\]

is a countable union of null sets, and therefore contains no interval. ∎

**Outcome and remaining gap.** The high-energy local-dimension limit, even supplemented by bounded gaps, cannot by itself prove the target. This `S` is not claimed to be a Fibonacci spectrum. The spectral dynamics may impose stronger geometry, but that extra theorem must be proved.

## Approach 4: a precise mixed-spectrum thickness route

The next result separates the required one-dimensional geometric input from the elementary assembly of a ray. It accommodates different couplings without equating their spectra.

### Lemma 4: a paired-block criterion

Let `An,Bn` be Cantor subsets of closed semibounded sets `A,B`, with ordered disjoint hulls

\[
\operatorname{hull} A_n=[a_n,b_n],\quad
\operatorname{hull} B_n=[c_n,d_n],
\quad a_n,c_n\longrightarrow\infty.
\]

Suppose, for all sufficiently large `n`, both pairs `(An,Bn)` and `(An,B(n+1))` satisfy:

1. the product of their Newhouse thicknesses exceeds one;
2. the largest bounded gap of each set is at most the diameter of the other.

Suppose also

\[
c_{n+1}-d_n\leq b_n-a_n,
\qquad
a_{n+1}-b_n\leq d_{n+1}-c_{n+1}.
\]

Then `A+B` contains a half-line.

**Proof.** The gap-lemma consequence stated as Damanik–Fillman–Gorodetski, Lemma 2.1, makes the following sums full intervals:

\[
I_n=A_n+B_n=[a_n+c_n,b_n+d_n],
\quad J_n=A_n+B_{n+1}=[a_n+c_{n+1},b_n+d_{n+1}].
\]

The first displayed inequality says `In` overlaps `Jn`; the second says `Jn` overlaps `I(n+1)`. Their increasing right endpoints tend to infinity. The union from any sufficiently large index is therefore an entire closed ray contained in `A+B`. ∎

### Corollary 4.1: a square-energy sufficient condition

Suppose that for `j=1,2` the square-root spectral sets contain Cantor sets `K(j,n)` whose hull endpoints are

\[
nP+\alpha_j+o(1),\qquad nP+\beta_j+o(1),
\]

where `P>0`, `0<Wj=βj-αj<P`, and `W1+W2>P`. Assume their thicknesses tend to infinity. Then the corresponding two energy spectra have a sum containing a ray.

**Proof.** At large positive `k`, the squaring map on each bounded-width hull distorts a length ratio by at most the quotient of its maximal and minimal derivatives. Thus

\[
\tau(\{k^2:k\in K_{j,n}\})
\geq\frac{\min\operatorname{hull}K_{j,n}}{\max\operatorname{hull}K_{j,n}}
\tau(K_{j,n})\longrightarrow\infty.
\]

Their energy diameters are `2nP Wj+o(n)`, and consecutive energy gaps are `2nP(P-Wj)+o(n)`. Therefore the two overlap inequalities in Lemma 4 hold with strict asymptotic margin `2nP(W1+W2-P)+o(n)`.

For completeness, a Cantor set of diameter `D` and thickness `τ` has each bounded gap of length at most `D/(1+2τ)`: in any presentation, the bridges at the two endpoints of a gap of length `g` lie within the left and right portions of its hull, whose lengths add to `D-g`; use presentations approaching the thickness supremum. Since the adjacent block diameters here have finite positive limiting ratios and thicknesses diverge, the mutual largest-gap conditions also hold. Apply Lemma 4 to the squared sets. ∎

**Outcome and remaining gap.** This is a conditional theorem, not a construction of its hypotheses for arbitrary tile shapes. Existing high-energy trace convergence and the bound in Approach 2 do not establish these growing-thickness blocks. The missing task is uniform distortion/relative-invariant control on sufficiently wide windows, simultaneously for the two fixed couplings. Merely asserting such blocks would restate the hard part.

## Approach 5: test equal-coupling and approximation transfers

### Proposition 5: two self-sum rays need not give a mixed ray

There are closed semibounded zero-measure Cantor-type sets `A,B` such that both `A+A` and `B+B` contain rays, but `A+B` has arbitrarily high gaps.

**Proof.** Let `C` be one half of the standard middle-thirds Cantor set. The elementary identity `C+C=[0,1]` follows, for instance, from balanced ternary expansions and the symmetry of the standard Cantor set. Put

\[
A_0=\{0,1,2,4,5,9\},\qquad
B_0=\{0,3,7,8,10,11\}=-A_0\pmod {12},
\]

\[
A=\bigcup_{m\geq0,\ a\in A_0}(12m+a+C),\quad
B=\bigcup_{m\geq0,\ b\in B_0}(12m+b+C).
\]

These unions are locally finite, so the sets are closed, perfect, nowhere dense, and null. The residues `A0+A0` include all residues modulo 12. Indeed integers `0,...,11` themselves have witnesses

\[
0+0,\ 0+1,\ 0+2,\ 1+2,\ 0+4,\ 0+5,\
1+5,\ 2+5,\ 4+4,\ 0+9,\ 1+9,\ 2+9.
\]

Together with `C+C=[0,1]`, this gives `A+A=[0,infinity)`. Since `B0=-A0` modulo 12, `B0+B0` also covers all residues. Every representative sum lies between 0 and 22; adding nonnegative multiples of 12 consequently gives `[12,infinity) subset B+B`.

However, `A0-A0` misses residue 6: `A0` contains exactly one element from each antipodal pair modulo 12. Thus `A0+B0` misses 6. Every component of `A+B` has the form `[h,h+1]` with integer `h` of an allowed residue. Hence

\[
(12m+6,12m+7)\cap(A+B)=\varnothing\qquad(m\geq0).
\]

This proves the claim. The small residue calculation is verified exactly by the supplied script. ∎

This example does not refute a mixed-coupling Fibonacci theorem. It shows why a self-sum theorem cannot be applied to a mixed sum without additional shared geometry.

There is a second obstruction to a simple approximation argument. With `S` from Proposition 3, the closed sets `Sj=j^{-1}S` have Hausdorff distance at most `1/j` from `[0,infinity)`, because they contain the grid `j^{-1}Z>=0` and lie in the ray. Nevertheless every `Sj+Sj` is null. Thus the ray property is not preserved under arbitrary small Hausdorff perturbations, even for perfect semibounded null sets. Conversely, the sets `(S intersect [0,n]) union [n,infinity)` converge locally to `S` and have self-sum rays with thresholds tending to infinity. A family of finite or periodic approximations, each possessing a high-energy ray, needs a uniform threshold and a justified spectral limiting argument; bare existence at each approximation level is insufficient.

**Outcome and final gap.** The five approaches leave the original arbitrary-shape, every-positive-coupling target unresolved. No finite spectral plot, finite transfer calculation, or periodic approximant supplies the missing infinite-energy, all-scale thickness theorem. The most concrete next mathematical requirement is the general-tile block construction in Approach 4, or a genuinely spectral counterexample that evades it. Neither has been obtained here.

## Verification limits

The script checks only algebraic identities, finite residue covers, and overlap formulas. The analytic and infinite-set conclusions rely on the written proofs and the explicitly named literature inputs. They require fresh independent review before promotion. This package makes no claim to the first discovery of its elementary partial lemmas and is not a solved-problem publication.

