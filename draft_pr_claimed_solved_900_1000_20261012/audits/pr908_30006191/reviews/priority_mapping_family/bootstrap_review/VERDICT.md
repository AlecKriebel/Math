# Independent adversarial review of the proposed exact-energy bootstrap

Reviewed 2026-10-14T05:10:01Z. Scope: PR 908 / problem 30006191 / current `bounded_region_v2`, original head `a35667b1bb0bafed69916709997a4684223ecc93`. The object tested is a **new audit deduction** built from the earlier localized-cluster mechanism, not a claim that the earlier manuscript literally states the same cutoff theorem.

**Verdict:** the proposed bootstrap and maximal-discontinuity deduction are valid for the frozen candidate's model and original witness vectors. No circularity, unproved propagation hypothesis, divergent constant, second-moment gap, or sign obstruction was found. The quantitative comparison error is `O(n^(-1/6)+n^(-1/2))` at the prescribed times; occupation and one-body errors also vanish. The proof below gives independently checkable details. This verdict does not certify novelty, priority, or current openness.

## Exact target and primary-source binding

The fixed model is `q=1_{B(0,4)}`, `L_n=sum_j q_j`, `T_n=sum_j(-Delta)_j`, and

\[
H_{n,k}=T_n+L_n(L_n-k),\qquad k\in\{0,1\}.
\]

The frozen original proof has SHA-256 `2b7c22cfc54049a9e51fe5eb4eb283ba911e6f27e8b6e4dc9557927bc04d7350`. Its normalized `f` is smooth, supported in `B(0,1/3)`, and its original packed Slater `Psi_n` is supported in the cube `Q=2e_1+(-1/4,1/4)^3`. Since `sqrt(3)/4 < 0.46`, this exact `Q` has closure inside `B_0=B(2e_1,0.46)`. Take `B=B(2e_1,0.6)` and `A=B(0,0.5)`. Thus `B_0` is compactly inside `B`, the closures of `A` and `B` are disjoint, and both lie inside `Lambda=B(0,4)`. The original Slater obeys

\[
T_{0,n}:=\langle\Psi_n,T_n\Psi_n\rangle\le C n^{5/3}.
\]

The earlier source inspected is Oliver Siebert, *Discontinuity of Continuum Fermion Dynamics*, [arXiv:2609.34402v1](https://arxiv.org/pdf/2609.34402v1), SHA-256 `5d35ca7805a8e1d8be3227eedcfb3e76111d85ae7df8cdcc3820d7c8fd15473c`. Complete proof text for Lemmas 3.2–3.4, pp. 9–15, was read. The source supplies the leakage-commutator, localized antisymmetrization, and cross-phase mechanisms. The improved energy closure below is a separate deduction for the exactly constant cutoff kernel. Only the current bounded-region packet and same-target primary-source material were inspected.

## 1. The sharp energy/leakage closure

Choose a fixed real smooth function `chi_B`, between zero and one, zero on a neighborhood of the closure of `B_0`, and one on `B^c`. It need not have compact support; its derivatives can be compactly supported in the fixed annulus between the two balls. Define

\[
\Psi_n(s)=e^{-isH_{n,k}}\Psi_n,\quad
F_B(s)=\langle\Psi_n(s),d\Gamma(\chi_B^2)\Psi_n(s)\rangle,
\quad M_n=n-L_n.
\]

All quantities here are for the **interacting** evolution. No interacting Slater structure is assumed. Since all initial particles are inside `Lambda`, the conserved energy is exactly

\[
\langle H_{n,k}\rangle_s=n(n-k)+T_{0,n}.
\]

The bounded-multiplier identity

\[
H_{n,k}-n(n-k)=T_n-M_n(2n-k-M_n)
\]

therefore gives

\[
\langle T_n\rangle_s
=T_{0,n}+\langle M_n(2n-k-M_n)\rangle_s
\le T_{0,n}+2n\langle M_n\rangle_s
\le C n^{5/3}+2nF_B(s).
\tag{1}
\]

The last inequality follows from the operator ordering `M_n=N_{Lambda^c} <= N_{B^c} <= dGamma(chi_B^2)`. It is not a probabilistic assumption. The factor `2n-k-M_n` is nonnegative for the relevant integer spectrum `0,...,n`, including `n=1,k=1`.

For each fixed `n`, the potential is bounded, so `D(H_{n,k})=D(T_n)`. The initial smooth Slater belongs to this domain, and its evolution remains there. Smooth bounded multiplication by `chi_B^2` preserves the kinetic domain. The commutator identity is consequently legitimate, and the potential cancels because both operators are multiplication operators:

\[
F'_B(s)=2\operatorname{Re}\sum_j
\langle\chi_{B,j}\Psi_n(s),i[-\Delta,\chi_B]_j\Psi_n(s)\rangle.
\]

The usual first-order commutator bound has uniform fixed-cutoff constants and gives

\[
|F'_B(s)|\le C\sqrt{F_B(s)}\sqrt{\langle T_n\rangle_s+n}.
\tag{2}
\]

It can alternatively be derived directly from the kinetic quadratic form. No derivative of `q` is taken.

Set `G_delta(s)=sqrt(F_B(s)+delta)`. Because `F_B(0)=0`, (1)–(2) imply, for `s>=0`,

\[
G'_\delta(s)\le Cn^{5/6}+C\sqrt n\,G_\delta(s),\qquad
G_\delta(0)=\sqrt\delta.
\]

Gronwall gives

\[
G_\delta(s)\le e^{C\sqrt n s}(\sqrt\delta+Cn^{5/6}s).
\]

Letting `delta` decrease to zero proves

\[
F_B(s)\le Cn^{5/3}s^2 e^{C\sqrt n|s|}.
\tag{3}
\]

For negative `s` apply the same argument after reversing time. For every fixed `a>0`, (3) implies

\[
F_B(s)\le C_a n^{5/3}s^2\qquad (|s|\le a/n).
\tag{4}
\]

This is a closed differential estimate. It does not transfer the central difficulty to an unsupported claim. In particular, its feedback has rate `sqrt(n)`, whose accumulated exponent on the required `1/n` timescale is uniformly bounded.

## 2. The one-body sharp cutoff causes no domain problem

Write

\[
h_k=-\Delta+(1-k)q,\qquad f_s=e^{-ish_k}f.
\]

The bounded potential gives `D(h_k)=H^2` and equivalence of the graph and `H^2` norms. Because `f` has smooth compact support strictly inside `Lambda`,

\[
h_kf=-\Delta f+(1-k)f\in C_c^\infty(A),
\]

and hence `f` belongs to `D(h_k^2)`. Functional calculus now gives

\[
\|f_s-f\|_{H^2}\le C|s|(\|h_kf\|+\|h_k^2f\|).
\tag{5}
\]

Choose a fixed real `chi_A` in `C_c^infty(A)`, between zero and one and equal to one near `supp f`. Multiplication by `1-chi_A` is bounded on `H^2`, so its tail is `O(|s|)` there, and in particular

\[
\|(1-\chi_A)f_s\|_2\le C|s|.
\tag{6}
\]

For the bounded kernel proof below, only the `L^2` version of (6) is needed; `f in D(h_k)` would already suffice for that weaker bound. The stronger source-style `H^2` propagation assertion is nevertheless valid. It does not assert that the indicator potential is differentiable, nor that `D(h_k^2)=H^4`.

## 3. Duhamel and localized antisymmetrization use only first moments

On the distinguished-particle plus antisymmetric-cluster space set

\[
\widetilde H=h_k\otimes1+1\otimes H_{n,k},\qquad
\widetilde V=2\sum_{j=1}^nq(x)q(y_j),\qquad
J_n=\sqrt{n+1}\,P^-_{n+1}.
\]

The factor two is essential: the off-diagonal pair sum is ordered. Indeed,

\[
H_{n,k}=\sum_jh_{k,j}+\sum_{i\ne j}q_iq_j,
\]

so `widetilde H+widetilde V` is exactly the full symmetric `(n+1)`-particle Hamiltonian before restricting to the fully antisymmetric subspace. Both potentials are bounded. The kinetic domains are common, permutation projections preserve them, and

\[
J_n e^{-it(\widetilde H+\widetilde V)}
=e^{-itH_{n+1,k}}J_n,\qquad J_n(f\otimes\Psi_n)=a^*(f)\Psi_n.
\]

The bounded-perturbation Duhamel identity therefore holds on all vectors. In particular its comparison error is bounded by

\[
\epsilon_n(t):=
\|e^{-itH_{n+1,k}}a^*(f)\Psi_n
-e^{-2int}a^*(f_t)\Psi_n(t)\|
\le\int_0^t\|J_n(\widetilde V-2n)(f_s\otimes\Psi_n(s))\|\,ds.
\tag{7}
\]

Let `P_B=1_{B}^{tensor n}` on the cluster space. Split the integrand vector into

\[
\chi_Af_s\otimes P_B\Psi_n(s),\quad
\chi_Af_s\otimes(1-P_B)\Psi_n(s),\quad
(1-\chi_A)f_s\otimes\Psi_n(s).
\]

The first residual vanishes exactly because `q(x)=q(y_j)=1` on `A x B^n`. The split is applied only after Duhamel; no derivative of the sharp projection `P_B` is taken.

For any cluster-antisymmetric `eta` with distinguished coordinate in `A`, the localized antisymmetrization bound is

\[
\|J_n\eta\|^2\le\langle\eta,(1+N_A)\eta\rangle.
\tag{8}
\]

This algebraic bound can be checked independently of the source by decomposing the cluster into sectors with exactly `r` particles in `A`: on that sector `J_n` acts as `sqrt(r+1)` times an orthogonal antisymmetrization projection, and its different `r` images have orthogonal local number. Thus no dynamical or kernel assumption enters (8).

Put `Phi=(1-P_B)Psi_n(s)`. The multiplier `widetilde V-2n` commutes with `N_A`, is bounded in modulus by `2n`, and preserves distinguished-coordinate support in `A`. Also

\[
1-P_B\le N_{B^c},\qquad N_AP_B=P_BN_A=0,\qquad N_A\le N_{B^c}.
\]

Consequently (8) gives the explicit bound

\[
\begin{aligned}
\|J_n(\widetilde V-2n)(\chi_Af_s\otimes\Phi)\|^2
&\le4n^2\|\chi_Af_s\|^2
   (\|\Phi\|^2+\langle\Phi,N_A\Phi\rangle)\\
&\le8n^2F_B(s).
\end{aligned}
\tag{9}
\]

Equation (9) is precisely why **no interacting second-moment estimate** is needed. Bounding `J_n` globally on this term would lose a further `sqrt(n)` and would not close the desired vanishing estimate.

For the third term use the global `||J_n||<=sqrt(n+1)`, the same multiplier bound, and (6):

\[
\|J_n(\widetilde V-2n)((1-\chi_A)f_s\otimes\Psi_n(s))\|
\le Cn^{3/2}|s|.
\tag{10}
\]

Together with (4), equations (7), (9), and (10) yield

\[
\epsilon_n(t)\le C_a(n^{11/6}+n^{3/2})t^2,
\qquad0\le t\le a/n.
\tag{11}
\]

All constants are independent of `n` and may be chosen uniformly for `k=0,1`, since there are only two bounded one-body choices. This also validates the extension from the source's `t<=1/n` to any fixed `a/n` for this bounded kernel.

## 4. Fixed creation, exact original times, and exact original annihilation vector

Use inner products linear in the second variable and define

\[
\Xi_n=a^*(f)\Psi_n,\qquad
m_n(t)=\langle e^{-itH_{n+1,k}}\Xi_n,
                  a^*(f)\Psi_n(t)\rangle.
\]

The original cluster orbitals are orthogonal to `f`, so `||Xi_n||=1`. By (11),

\[
m_n(t)=e^{2int}
\langle a^*(f_t)\Psi_n(t),a^*(f)\Psi_n(t)\rangle
+O(\epsilon_n(t)).
\tag{12}
\]

Since `||a^*(f_t)-a^*(f)||=||f_t-f||<=C|t|`, the CAR yield

\[
\langle a^*(f_t)\Psi_n(t),a^*(f)\Psi_n(t)\rangle
=1-\langle n_f\rangle_{n,t}+O(|t|).
\]

Here `n_f=dGamma(|f><f|) <= N_A <= dGamma(chi_B^2)` because `f` is normalized and supported in `A`. Thus

\[
|m_n(t)-e^{2int}|\le\epsilon_n(t)+C|t|+F_B(t).
\tag{13}
\]

At the exact candidate time

\[
t_n^{(k)}=\frac\pi{2n+1-k},
\]

one can take `a=pi/2`; (4) and (11) give

\[
F_B(t_n^{(k)})=O(n^{-1/3}),\qquad
\epsilon_n(t_n^{(k)})=O(n^{-1/6}+n^{-1/2}).
\]

The cross phase is

\[
e^{2int_n^{(k)}}=-e^{-i(1-k)t_n^{(k)}}\longrightarrow-1.
\]

For `k=0`, the **cross phase alone is not exactly minus one** at the prescribed time. Exact equality must not be asserted unless a justified one-body correction is included. Only convergence is needed, and (13) proves `m_n(t_n^(k)) -> -1` directly, with no such correction.

Now `m_n(t)` is the Heisenberg creation matrix element between `Xi_n` and `Psi_n`. It is one at zero, so

\[
2\ge\|\tau_{t_n}(a^*(f))-a^*(f)\|
\ge|m_n(t_n)-1|\longrightarrow2.
\]

Taking adjoints preserves the operator norm. More specifically, for the original annihilation difference

\[
D_n=e^{it_nH}a(f)e^{-it_nH}-a(f),
\]

\[
\langle\Psi_n,D_n\Xi_n\rangle
=\overline{m_n(t_n)-1}\longrightarrow-2.
\]

Since `||D_n||<=2`, this proves `||D_n Xi_n|| -> 2` for the **exact original candidate vector**, not a new optimized vector. The vector states `omega_n(B)=<Xi_n,B Xi_n>` therefore satisfy `omega_n(D_n^*D_n)->4`.

## Required presentation details and exact scope limit

No substantive repair is needed for the hypothesis as supplied. A complete written proof must explicitly retain: normalized `f`; fixed smooth cutoffs with `chi_A=1` near `supp f`; original `Q` compactly inside `B_0`; the bounded-perturbation intertwining/Duhamel justification; the weighted estimate (9), not a bare leakage-probability estimate; and the asymptotic cross-phase qualification for `k=0`.

The result is a quantitative deduction obtained by modifying the source's kinetic estimate, then replaying its localized antisymmetrization and phase comparison for `K(x,y)=q(x)q(y)`. The source's full-space pair-potential theorem is not literally a cutoff theorem. This review validates the new deduction, including the maximal limit and prescribed witnesses; it makes no broad claim that the deduction is novel or that it was already literally printed in the earlier source.
