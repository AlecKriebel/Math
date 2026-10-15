# Independent cutoff mapping and the exact quantitative distinction

Scope: PR 908, problem 30006191, current `bounded_region_v2`, original head `a35667b1bb0bafed69916709997a4684223ecc93`. This is a priority implication audit. It does not change the frozen candidate, and it does not establish historical novelty.

The source is Oliver Siebert, *Discontinuity of Continuum Fermion Dynamics*, [arXiv:2609.34402v1](https://arxiv.org/pdf/2609.34402v1), submitted 28 September 2026. Its stated main theorem concerns difference kernels on all space. Its cluster leakage, localized antisymmetrization, and relative-phase proof occur in Lemmas 3.1-3.4 and Section 3.3; Proposition 2.6 gives maximal norm 2 for a full-space constant interaction. The cutoff deductions below are this audit's own derivations using that mechanism. They are not quoted or relabeled statements of the source.

## 1. Exact model, coefficients, and domain

Write `q=1_{B(0,4)}`, `L_n=sum_j q(x_j)`, `T_n=sum_j(-Delta_j)`, and

\[
 H_{k,n}=T_n+L_n(L_n-k),\qquad k\in\{0,1\}.
\]

The candidate's smooth potential equals one on all differences of points in the interaction region, so its actual two-variable kernel is `K(x,y)=q(x)q(y)`. In particular,

\[
 H_{k,n}=\sum_j h_{k,j}+\sum_{i\ne j}K(x_i,x_j),\qquad
 h_k=-\Delta+(1-k)q.
\tag{D1}
\]

The second sum is ordered. Adding one particle produces `2 sum_j K(x,y_j)`, with no half factor. For the density product including its CAR contraction, the diagonal is `V(0)L_n=L_n`; omitting it gives `L_n(L_n-1)`. Formula (D1) handles both conventions without a product of distributions. If the entire interaction were multiplied by a different positive coupling, the times and the one-body diagonal term would have to be rescaled consistently.

On each fixed sector these potentials are bounded real multiplication operators, symmetric under particle permutations. Thus the all-space kinetic domain is unchanged and the direct sum is self-adjoint on its maximal domain. The interaction is not uniformly bounded over all sectors. No hard wall, momentum cutoff, or preservation of the CAR algebra is used.

For `h_k`, bounded perturbation gives `D(h_k)=H^2(R^3)`. More explicitly,

\[
 \|\Delta v\|\leq\|h_kv\|+\|v\|,\qquad
 \|h_kv\|\leq\|\Delta v\|+\|v\|,
\]

which proves equivalence of its graph norm and the `H^2` norm. Put
`Omega=B(0,4) union {x:|x|>4}`. If `u` is smooth compactly supported in `Omega`, it vanishes on an open neighborhood of the boundary, so `q u` and `h_k u` are smooth compactly supported. Consequently `u in D(h_k^2)`. For `w_t=(exp(-it h_k)-1)u`, functional calculus yields

\[
 \|w_t\|_{H^2}\leq C(\|w_t\|+\|h_kw_t\|)
 \leq C|t|(\|h_ku\|+\|h_k^2u\|).
\tag{D2}
\]

The displayed spectral estimate holds for all real t for these test functions; in particular it verifies the required local propagation estimate with `m=2>3/2`. It does not assert that multiplication by the discontinuous `q` preserves `H^2` for arbitrary functions. Only a bounded perturbation and test functions away from its jump are used.

## 2. Concrete geometry and packing

Take a cluster region `B=B(2e_1,3/5)` and `B_0=B(2e_1,23/50)`; the closure of the frozen packing cube `Q=2e_1+(-1/4,1/4)^3` lies in `B_0`. The closed balls `B_0 subset B subset Lambda` stay away from the cutoff boundary. Let `A_1=B(0,1/2)` and `A_2=B(6e_1,1/4)`. Their closures are disjoint from each other and from `B`, and both closures lie in `Omega`. The candidate's fixed normalized `f`, supported in the ball of radius `1/3`, is eligible in `A_1`.

On `A_j x B`, `K=c_j` exactly, where `c_1=1` and `c_2=0`. No translation symmetry is presumed. For every `y`, `||K(.,y)v||_2 <= ||v||_2`; this replaces all translation-uniform singular-potential multiplier estimates.

Disjoint rescaled smooth orbitals in a fixed cube give normalized Slaters `Psi_n` supported in `B_0^n` and

\[
 E^{\rm kin}_n:=\langle\Psi_n,T_n\Psi_n\rangle\leq Cn^{5/3}.
\tag{D3}
\]

Initially `L_n=n`, hence the exact initial total energy is

\[
 \langle\Psi_n,H_{k,n}\Psi_n\rangle=n(n-k)+E^{\rm kin}_n.
\tag{D4}
\]

The evolved cluster is not assumed to remain a Slater.

## 3. Direct qualitative mapping

Choose a smooth real `chi_B` equal to zero near the closure of `B_0` and equal to one on `B^c`, with values in `[0,1]`. In `Psi_n(s)=exp(-is H_{k,n})Psi_n`, put

\[
 F_n(s)=\langle d\Gamma(\chi_B^2)\rangle_{n,s},\quad
 E_n(s)=\langle T_n\rangle_{n,s}.
\]

Every potential in (D1) is a multiplication operator and commutes with `dGamma(chi_B^2)`. Only the kinetic commutator contributes. Its first-order bound and Cauchy-Schwarz give

\[
 |F_n'(s)|\leq C\sqrt{F_n(s)}\sqrt{E_n(s)+n}.
\tag{D5}
\]

The initial smooth Slaters are in the operator domain. Bounded perturbation gives `D(H_{k,n})=D(T_n)`, and the full unitary group preserves this common domain. Smooth localization preserves the domain. One can therefore differentiate the expectation directly, or use the source's form-domain regularization. No derivative of `q` or `K` occurs.

The coarse energy bound `E_n(s)<=C n^2` and `F_n(0)=0` imply `F_n(s)<=C n^2s^2`. Since `N_{B^c}<=dGamma(chi_B^2)`, this controls cluster leakage and occupation of either probe region.

On the distinguished-particle plus antisymmetric cluster space, let `J_n=sqrt(n+1)P^-_{n+1}`. If the distinguished variable lies in `A`, decompose the cluster by the number `r` of its particles in `A`. On each component `J_n` has squared norm at most `r+1`, and its images have distinct local particle number. Thus

\[
 \|J_n\eta\|^2\leq\langle\eta,(1\otimes(1+N_A))\eta\rangle.
\tag{D6}
\]

It is isometric when the distinguished support and all cluster supports are disjoint. This algebraic statement is independent of the kernel. The `sqrt(n+1)` global estimate alone would not suffice.

Define `tilde H_n=h_k tensor 1+1 tensor H_{k,n}` and `C_n=2sum_j K(x,y_j)`. The symmetric full operator is `tilde H_n+C_n` on the same all-space kinetic domain. Permutations preserve this domain and commute with it, so `J_n` intertwines this operator and its unitary group with `H_{k,n+1}`. Boundedness of `C_n` permits the exact Duhamel identity comparing it with `2nc_j`.

For a fixed normalized `u` supported in `A_j`, write `u_s=exp(-is h_k)u`. Choose `chi_A` supported in `A_j`, equal to one near `supp u`, and let `P_B=1_B^{tensor n}`. Split the Duhamel input into

\[
 \chi_Au_s\otimes P_B\Psi_n(s),\quad
 \chi_Au_s\otimes(1-P_B)\Psi_n(s),\quad
 (1-\chi_A)u_s\otimes\Psi_n(s).
\tag{D7}
\]

The first term has zero integrand because `C_n=2nc_j` on its support. For the second, (D6), `||C_n-2nc_j||<=2n`, and commutation of these multipliers with `N_A` bound the integrand by `C n sqrt(F_n(s))`. Indeed `||(1-P_B)Psi_n(s)||^2<=F_n(s)` and `N_A P_B=0`, so its weighted occupation is also at most `F_n(s)`. For the third, (D2), the global norm of `J_n`, and the same bounded multiplier give `C n^(3/2)|s|`. Therefore the coarse leakage estimate gives, for `t<=a/n` with any fixed `a`,

\[
 \|e^{-itH_{k,n+1}}a^*(u)\Psi_n
       -e^{-2inc_jt}a^*(u_t)\Psi_n(t)\|
 \leq C_a n^2t^2.
\tag{D8}
\]

The source's displayed `t<=1/n` is a convenient restriction, not a new domain assumption: the proof above works for every fixed `a/n`. Here (D2) is global in time, and graph-domain invariance also bounds `||u_s||_{H^2}` uniformly, so the estimates apply to all positive particle numbers.

Two-probe CAR matrix elements now give a fixed gauge-invariant observable `A=a^*(u_1)a(u_2)` with

\[
 \|\tau_t(A)-A\|\geq|e^{2int}-1|-C_a(n^2t^2+|t|).
\tag{D9}
\]

At `t=theta/n`, sufficiently small fixed positive `theta` makes the lower limit positive. A direct one-probe application of (D8) also gives positive discontinuity for the candidate's fixed interior `f`: compare with `a^*(f)Psi_n(t)`, whose squared norm is `1-<n_f> >=1-F_n(t)`, and use `||f_t-f||<=C|t|`. Thus the qualitative conclusion need not depend on a polarized probe containing an exterior component.

## 4. New audit bootstrap: maximal 2 follows after one extra estimate

This section is a new deduction produced during the audit. It is not a theorem stated in the earlier paper and is not needed for the already validated qualitative priority implication.

Let `M_n=n-L_n`. Since `B subset Lambda`,

\[
 0\leq M_n\leq N_{B^c}\leq d\Gamma(\chi_B^2).
\]

The exact identity

\[
 H_{k,n}-n(n-k)=T_n-M_n(2n-k-M_n)
\tag{D10}
\]

and conservation of (D4) imply

\[
 E_n(s)\leq Cn^{5/3}+2nF_n(s).
\tag{D11}
\]

This is not a presumed small kinetic-energy bound: it closes an inequality in the same leakage quantity already being differentiated. Inserting it into (D5) and regularizing `G_delta=sqrt(F_n+delta)` gives

\[
 |G_\delta'(s)|\leq Cn^{5/6}+C\sqrt n G_\delta(s).
\]

Gronwall, `G_delta(0)=sqrt(delta)`, and the limit `delta downarrow0` yield

\[
 F_n(s)\leq Cn^{5/3}s^2 e^{C\sqrt n|s|}.
\tag{D12}
\]

Constants depend on fixed geometry and the fixed orbital template but not on particle number; they can be chosen for both `k=0,1`. For `|s|<=a/n`, the exponential is uniformly bounded. Replacing the coarse leakage in the second term of (D7) by (D12) proves

\[
 \|e^{-itH_{k,n+1}}a^*(f)\Psi_n
       -e^{-2int}a^*(f_t)\Psi_n(t)\|
 \leq C_a(n^{11/6}+n^{3/2})t^2.
\tag{D13}
\]

At `t_n=pi/(2n+1-k)`, take `a=pi/2`; then (D12) is `O(n^{-1/3})` and (D13) is `O(n^{-1/6}+n^{-1/2})`. The phase `exp(2in t_n)` tends to `-1` for either ordering. There is no need for it to be exactly `-1` in this comparison, because the small one-body correction is controlled by (D2).

Use inner products linear in the second variable, and let `Xi_n=a^*(f)Psi_n`. Since the initial supports are disjoint, `||Xi_n||=1`. Set

\[
 Z_n(t)=\langle e^{-itH_{k,n+1}}\Xi_n,
                    a^*(f)e^{-itH_{k,n}}\Psi_n\rangle.
\]

By (D13),

\[
 Z_n(t_n)=e^{2in t_n}
   \langle a^*(f_{t_n})\Psi_n(t_n),a^*(f)\Psi_n(t_n)\rangle+o(1).
\]

Replacing `f_{t_n}` by `f` costs at most `C t_n`; the remaining inner product is `1-<n_f>` and `<n_f><=F_n(t_n)`. It tends to one by (D12), so `Z_n(t_n)->-1`. At time zero the corresponding matrix element is one. Thus

\[
 \|\tau_{t_n}(a^*(f))-a^*(f)\|\to2.
\tag{D14}
\]

The upper bound is `2||a^*(f)||=2`. Taking adjoints preserves the operator norm. More precisely, for `D_n=\tau_{t_n}(a(f))-a(f)`,

\[
 \langle\Psi_n,D_n\Xi_n\rangle=\overline{Z_n(t_n)-1}\to-2,
\]

so `||D_n Xi_n||->2` and the vector-state value of `D_n^*D_n` tends to 4. These are changing norm-test vectors, not a discontinuity in a fixed normal state.

The same strengthened two-probe calculation makes (D9)'s errors vanish and yields maximal 2 for that fixed transition observable. No universal potential or dimension claim is made. The powers in (D3) and (D12) are specific here to dimension three; the analogous packing exponent gives vanishing error only for `d>2`.

## 5. Required priority framing

The earlier stated theorem is not literally a cutoff theorem: simultaneous translations change `q(x)q(y)` while leaving `x-y` unchanged. A fixed one-body term cannot remove the entire quadratic discrepancy in all sectors. Nevertheless, the earlier proof adapts directly to the cutoff and supplies its qualitative conclusion. A cutoff qualifier therefore does not justify calling this the first qualitative solution.

The earlier paper explicitly states maximal 2 for the full-space constant-number reference, not this spatial cutoff. Section 4 shows that one additional energy bootstrap allows its localized phase mechanism to reach the candidate's quantitative conclusion, including its fixed orbital, times, and state witness. This new audit derivation is not evidence that this cutoff strengthening was publicly stated before the candidate. It does remove any argument that maximal 2 is intrinsically inaccessible through the prior mechanism. Neither a first-result claim nor novelty of the free-Slater variance method is certified by this audit.
