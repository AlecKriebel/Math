# Unrestricted complex qutrit four-copy falsifier

## Research log

- **2026-07-28 16:14--16:32 PDT.** Implemented an unrestricted complex
  Stiefel search over \(U:\mathbb C^2\to(\mathbb C^3)^{\otimes4}\), with
  exact tensor-contraction formulas evaluated in floating point for all
  sixteen swap moments and sectors.
- **2026-07-28 16:22 PDT.** Targeted the permutation-symmetric formal point
  (106) in `agent_n4_qubit_reference.md`.  Twenty-four independent target
  searches converged to a positive nearest stationary family, not to the
  formal point.
- **2026-07-28 16:28--16:29 PDT.** Eighty-start direct stress searches for
  \(Q_4\) and for the stronger \(H_1\) reached only numerical zero
  (\(10^{-14}\) scale), never a robust negative value.
- **2026-07-28 16:32--17:00 PDT.** Isolated the exact ``uniform odd''
  condition hidden in the formal point.  Constrained searches strongly
  suggest a sharp bound \(p_{1234}\geq1/8\), attained by the repetition
  code, but no proof of that bound has been obtained.
- **2026-07-28 17:09 PDT.** Added an independent evaluator and adversarial
  search for the local balanced-kernel Hessian from Proposition 20.1.
  It exactly reproduces the sparse rational stress examples in
  `agent_n4_crossed_kernel.md`.  Random and hill-climbing searches have
  found no code for which the Hessian is positive definite on its
  compression kernel.

All searches in this note are discovery evidence only.  No negative
four-copy code and no proof of four-copy positivity is claimed.

## 1. Exact data of the symmetric formal target

The normalized purification layer masses are
\[
(e_0,e_1,e_2,e_3,e_4)
=\left(\frac{79}{160},\frac18,\frac{39}{160},
       \frac18,\frac1{80}\right).
\]
Multiplication by four converts them to code-projector sector masses.
Per individual subset of weight \(r\), these are
\[
\boxed{\quad
p_0=\frac{79}{40},\quad p_1=\frac18,\quad
p_2=\frac{13}{80},\quad p_3=\frac18,\quad
p_4=\frac1{20}.
\quad}                                                     \tag{1}
\]
Their Walsh moments, again per individual subset of a fixed size, are
\[
\boxed{\quad
A_0=4,\quad A_1=\frac{77}{40},\quad A_2=\frac{17}{10},
\quad A_3=\frac{77}{40},\quad A_4=2.
\quad}                                                     \tag{2}
\]
The exact endpoint values are
\[
Q_4=-\frac1{80},\qquad
H_1=e_2+6e_4-3o_3=-\frac9{40}.                              \tag{3}
\]

Unlike the two older formal tables, (1) passes the elementary qutrit
purity, nesting, conditional, grouped, and filter-average tests presently
available.  In particular, its one-qutrit reduction has trace \(2\) and
purity \(77/40>4/3\), so it does not violate the elementary rank-three
purity lower bound.

## 2. Uniform odd sectors are exactly complement balance

Diagonalize a putative code projection as
\[
P=|u\rangle\langle u|+|v\rangle\langle v|,
\qquad \langle u,v\rangle=0.
\]
For \(T\subseteq[4]\), put
\[
g_T=\operatorname{Tr}(\rho_T^u\rho_T^v)
   =\langle u\otimes v|F_T|u\otimes v\rangle.
\]
Pure-state complementary purities give the exact identity
\[
\boxed{\quad A_T-A_{\bar T}=2(g_T-g_{\bar T}).\quad}        \tag{4}
\]
If
\[
\omega=\frac{u\otimes v-v\otimes u}{\sqrt2},
\]
then
\[
\langle\omega|F_T|\omega\rangle=g_T-g_{\bar T}.             \tag{5}
\]
Consequently (2) says precisely that every proper nonempty local-swap
moment of the logical bivector vanishes.  Fourier inversion on the parity
cube then gives
\[
\boxed{\quad
\|\Pi_R\omega\|^2=\frac18
\quad\text{for every odd }R\subseteq[4].
\quad}                                                     \tag{6}
\]
Thus any exact separator for (1) must couple this exterior/bivector data
to the three logical symmetric-square vectors.  Odd-sector positivity
alone cannot exclude the point.

## 3. An exact scalar relaxation which the target passes

The target even passes the natural decomposition into self-sector and
cross-sector scalar masses.  Consider the permutation-symmetric formal
pure-state moments
\[
x=(1,\frac{53}{80},\frac{11}{20},\frac{53}{80},1)
\]
and cross overlaps
\[
g=(1,\frac3{10},\frac3{10},\frac3{10},0).
\]
Their Walsh transforms, per subset, are
\[
\begin{array}{c|ccccc}
r&0&1&2&3&4\\ \hline
\alpha_r&53/80&0&9/160&0&0\\
c_r&13/40&1/16&1/40&1/16&1/40 .
\end{array}                                                \tag{7}
\]
Every displayed number is nonnegative.  Taking two identical formal
self distributions and the two ordered cross terms gives
\[
p_R=2\alpha_R+2c_R,
\]
which reproduces (1) exactly.  Thus sector positivity, pure-state
complementarity, cross-overlap positivity, and scalar
Cauchy--Schwarz do not exclude the target.

Moreover, the pure-state moment row \(x\) is itself realizable.  Let
\[
|W_4\rangle=\frac12\sum_{i=1}^4|0\cdots010\cdots0\rangle
\]
and
\[
|\phi\rangle=a|0000\rangle+b|W_4\rangle,\qquad
|b|^2=\frac3{\sqrt{10}},\quad |a|^2=1-\frac3{\sqrt{10}}.
\]
A direct reduction gives
\[
\operatorname{Tr}(\rho_i^\phi)^2
=1-\frac38|b|^4=\frac{53}{80},\qquad
\operatorname{Tr}(\rho_{ij}^\phi)^2
=1-\frac12|b|^4=\frac{11}{20}.
\]
Hence the unresolved obstruction is genuinely the common-\((u,v)\)
compatibility of (7), not feasibility of either self row separately.

## 4. Unrestricted complex searches

The discovery program is
`discovery/search_n4_complex_sector_target.cpp`.  It uses a complex
\(81\times2\) Stiefel variable, exact partial-trace contractions in
floating point, tangent projection, QR retraction, and backtracking.

For the full target (1), twenty-four starts converged to loss
\[
1.0154873108\times10^{-3}
\]
with approximately layer-symmetric sectors
\[
(1.96985,\ 0.13709,\ 0.158787,\ 0.112908,\ 0.077427).
\]
The corresponding values were
\[
Q_4\approx0.186043,\qquad H_1\approx0.062376.
\]
The one-site reduction spectra at this nearest family are approximately
\[
(0.03030,\ 0.9839,\ 0.9858)
\]
at every site, so the active numerical obstruction is not merely a
vanishing \(3\times3\) local-support determinant.

Direct eighty-start searches gave only
\[
\min Q_4=-7.9\times10^{-15},\qquad
\min H_1=-2.4\times10^{-14},
\]
which are cancellation-level zeros.  No robust negative value occurred.

When only (6) is imposed with penalty \(10^6\), all twenty starts converge
to
\[
p_\varnothing=\frac{17}{8},\qquad
p_R=\frac18\quad(R\ne\varnothing),
\]
up to the expected \(10^{-6}\) penalty displacement.  This is exactly the
repetition-code table, with
\[
p_{1234}=\frac18,\qquad H_1=0,\qquad Q_4=\frac14.
\]
Twenty-four separate minimizations of \(p_{1234}\) subject to (6) also
converged to \(0.124995\), again the \(10^{-6}\)-displaced value \(1/8\).
This motivates the exact but presently unproved slice inequality
\[
\boxed{\quad
A_T=A_{\bar T}\ (0<|T|<4)
\ \Longrightarrow\ p_{1234}\ge\frac18.
\quad}                                                     \tag{8}
\]
The formal target violates (8) because \(p_{1234}=1/20\).

## 5. Independent local-kernel Hessian evaluator

The second discovery program is
`discovery/search_n4_kernel_hessian.cpp`.  For each site it constructs
\[
\mathcal C(A)=U^\dagger(A\otimes I)U,\qquad
\mathcal K=\ker\mathcal C
\]
in orthonormal real Hermitian bases, reconstructs
\[
\mathcal N(A)=
\operatorname{Tr}\!\left[(P\otimes P)(A\otimes A)K_4\right]
\]
from the exactly quadratic effect polynomial, and diagonalizes
\(\mathcal N|_{\mathcal K}\).

As independent audits, it reproduces:

1. the exact kernel-trace counterexample with
   \[
   F=\frac{121}{450},\quad
   \operatorname{spec}(\mathcal N|_{\mathcal K})
   =\left(-\frac1{18},-\frac1{36},-\frac1{36},
           \frac1{12},\frac1{12}\right);
   \]
2. the exact unrestricted-inertia counterexample with full inertia
   \((6,3,0)\) and crossed-kernel inertia \((2,3,0)\);
3. common-local-qubit frames, for which
   \(\mathcal N|_{\mathcal K}=0\) to \(10^{-12}\).

Thus neither unrestricted positive inertia at most four nor
\(\operatorname{Tr}(\mathcal N|_{\mathcal K})\le F/8\) is valid.
The surviving statement is the genuinely crossed assertion
\[
\boxed{\qquad
\lambda_{\min}(\mathcal N|_{\ker\mathcal C})\le0.
\qquad}                                                     \tag{9}
\]
Twelve dense random frames gave least eigenvalues between \(-0.105\)
and \(-0.071\).  Random hill climbing moved toward zero or toward
lower-support boundary families but did not cross it.  This evidence is
not a proof of (9).

## 6. Current exact and numerical status

What is exact:

1. the conversions (1)--(3);
2. the complement-balance/uniform-bivector equivalence (4)--(6);
3. the feasible scalar decomposition (7);
4. the exact sparse Hessian audits described in Section 5.

What is not resolved:

1. no exact separator excluding (1) from the full Grassmannian is known;
2. the numerical slice bound (8) is unproved;
3. the crossed-kernel assertion (9) is unproved;
4. no negative four-copy code was found;
5. nothing here supplies an all-copy conclusion.

