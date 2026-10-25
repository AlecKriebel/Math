# Independent adversarial derivations for the pinned upstream EPnI

Date: 2026-10-25 UTC. This document records direct mathematical checking of the proof, not an inference from the theorem's label or from earlier favorable audits. The full pinned 32-page text was read; §§3–6 were additionally checked against TeX acquired from exactly commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. This audit did not consult sibling or historical upstream audit reports.

## 1. Exact target and logical dependency

The necessary statement is: for every finite integer n≥1, every n-mode density operator ρ with Tr ρN<∞, every t∈[0,1], and an independent n-mode vacuum input,

    S(L_t^{⊗n}(ρ))/n ≥ g(t g^{-1}(S(ρ)/n)).                 (VE)

Here g(r)=(r+1)log(r+1)−r log r, and L_t is the identical one-mode quantum-limited attenuator on each mode. The modes of ρ can be entangled. VE follows from the upstream two-input theorem by setting ρ_B=|0⟩⟨0|^{⊗n}, because S(ρ_B)=0 and g^{-1}(0)=0. This specialization does not by itself verify the premise. The remainder checks its full central proof.

The proof uses the classical spectral theorem, elementary Hilbert space trace-ideal estimates, the harmonic Poisson representation/Herglotz argument, elementary complex inverse-function/covering arguments, and scalar calculus. The specialized claims on interpolation, regularized minimizers, Hessian contractions and limiting states are actually proved in the source and checked below. No multimode Gaussian optimizer theorem or unproved entropy inequality is imported.

## 2. Interpolation: general linear maps really are allowed

Suppose each of the four diagonal weights satisfies Q_X,0(Z)≥Σ_i w_i Q_X,i(L_iZ). Pointwise positive combinations preserve this statement. Parallel sums do too, by the exact variational formula

    (X:Y)|z|² = min_{u+v=z} (X|u|²+Y|v|²).

Crucially, the source minimizers are U=Y/(X+Y) Z and V=X/(X+Y) Z. The source test space is invariant under these multipliers. One never identifies L_iU with the target pointwise minimizer. Instead, L_iU+L_iV=L_iZ and the target variational minimum supplies the inequality in the needed direction. Thus there is no hidden commutation or intertwining assumption between L_i and diagonal modular frequencies.

For a source test supported on finitely many parameter values, pointwise convergence of weights implies convergence of its source quadratic form, even if it has an infinite identity tail. Target nonnegative sums are handled by Fatou, rather than an unsupported interchange with an unbounded multiplier. The two displayed integral identities in (3.6) implement the logarithmic mean and its complementary mean using only positive combinations and parallel sums. They do not assert arbitrary multiplication preservation.

For f(x)=x/sinh x and b(x)=x coth x, one has

    f(x)e^{±x}=b(x)±x,
    ℓ(mf(x)e^x,mf(x)e^{-x})=m,
    [mf(x)e^x][mf(x)e^{-x}]/m=m f(x)².

Therefore m, ms, mt are available, with s=f(x)² and t=f(y)².

### 2a. The Stieltjes ingredient checked without assuming its conclusion

For real x>0, differentiation of s=f(x)² and B(s)=b(x) gives

    s'=2s(1−B)/x,      b'=(B−s)/x,
    −B'(s)=1/(2s)+(1−s)/(2s(B−1)).                         (A)

The assertion that −B' is Stieltjes is stronger than scalar monotonicity. The source supplies the following mechanism, which I checked:

* Set a(u)=sin u/u. For u=p+iq with q>0, restrict 0<p<p_*(q), where p_*tan p_*=−q tanh q. Since p tan p increases on (π/2,π), this boundary is unique and continuous.
* Direct real/imaginary parts put a(D) in the fourth quadrant. Finite boundary pieces map to its axes; as q→∞, |a|≥sinh q/(π²+q²)^{1/2}→∞ uniformly in p. Hence preimages of compact subsets of the quadrant stay compact in D. The corners 0 and π map to boundary values 1 and 0, so they do not evade this argument.
* Im(u cot u)=[q sin(2p)−p sinh(2q)]/[cosh(2q)−cos(2p)]<0, because sin(2p)≤2p and sinh(2q)>2q. Thus a' has no zero: a'=0 would force u cot u=1.
* A proper local inverse makes a an onto covering of the connected quadrant. A connected covering of this simply connected quadrant has one sheet. Thus its inverse is holomorphic; this is not a merely local selection of a possibly multivalued inverse.
* With s in the upper half-plane, s^{-1/2} lies in that quadrant. Define u=a^{-1}(s^{-1/2}) and B=u cot u. Then Im B<0. On the positive real s-axis, the two boundary inverses are u=iq for 0<s<1 and u∈(0,π) for s>1. Their monotonic boundary parametrizations and nonzero derivatives give continuation. At s=1 the use of u² gives B(1)=1 and B'(1)=−1. This includes the possible branch corner.

Apply the Herglotz representation to −B and subtract at 1. The result is

    G(s)=(B(s)−1)/(1−s)
        =β+∫_{r≤0} [(1−r)(s−r)]^{-1} dμ(r),   β≥0.

For s>0 it is positive, including G(1)=1. H(s)=sG(s) has nonnegative imaginary part in the upper half-plane, term by term. It has no zero there: an interior zero would force its nonnegative harmonic imaginary part to be identically zero, then H constant, and positivity on the positive axis excludes the zero constant. Accordingly R=1/H is positive on (0,∞) and −R is Herglotz. Subtracting its representation at 1 gives, for s>1,

    0≤R(1)−R(s)=β̃(s−1)+∫[1/(1−r)−1/(s−r)]dμ̃(r)≤R(1).

The positive terms force β̃=0 and ∫(1−r)^{-1}dμ̃≤R(1). Hence R has a Stieltjes representation with a nonnegative constant. Equation (A), continued analytically, yields the claimed representation of −B'. This check is essential: anti-Pick character of B alone would not imply that its derivative is Stieltjes.

Thus 1/E=(2/m)∫_0^1−B'(θs+(1−θ)t)dθ consists of positive combinations of reciprocals of θ(ms)+(1−θ)(mt)+rm and of 1/m. Finite positive quadratures followed by inversion give permitted parallel sums. The integrability at infinity needed for the approximation follows from the proved Stieltjes measure bound. This establishes E comparison without importing the desired target weight.

### 2b. Final scalar minimization, including coincident cases

With a=b(x)+b(y), e=E/m, the source scalar quadratic has minimum

    (m/2)[a−(x−y)²/(a+2e)] |ξ|².

When x²≠y², E=m(t−s)/(2(B(s)−B(t))) and b²=f²+x² give

    (a+2e)(b(x)−b(y))=x²−y².

Substitution produces m[yb(x)+xb(y)]/(x+y)=m f(x)f(y)/f(x+y), by the sinh addition formula. At y=x the minimum is mb(x). At y=−x≠0, e=s(b−1)/(b−s) and b+e=x²/(b−s), so the minimum is ms. At x=y=0, E=m/2 and the minimum is m. Therefore none of the apparent diagonal/antidiagonal singularities is an omitted case. The coordinatewise minimizer remains an allowed source multiplier. This completes the actual proof of the four-weight interpolation statement.

## 3. Negative regularized minimum and sufficient domains

A strict EPnI violation survives number cutoffs: the cutoff approximations have bounded energies; passive mixing preserves a common combined energy bound; all entropies converge. If both input entropies were zero, the proposed inequality would just be nonnegativity of output entropy, so at least one entropy photon number a_i is positive. One may choose strictly positive r_i near a_i. At an a_i=0 boundary, g(r_i)/h(r_i)→0, while the output reference mean remains positive. This verifies the strict negative witness reduction without assuming strict positive input entropy.

The third thermal port creates both positive slack gaps λ_Dr_D and λ_D(r_D+1). Thus a fixed ε>0 can satisfy both inequalities (4.2). After these choices κ can be made as small as needed; its later bound depends only on fixed references and ε. Finally ζ>0 is small enough for a negative witness value uniformly bounded away from zero. Only ζ tends to zero in the final argument.

Expanding the functional gives, apart from fixed constants,

    S(ρ_0)/h_0 −Σ_i [(1+ε)w_i/h_i]S(ρ_i)
       +εΣ_i w_i Trρ_iN_i +ζΣ_i Trρ_iW_i⁴.

The linear energy terms dominate the negative O(log(1+energy)) entropy terms. This bounds both energies on the relevant sublevel uniformly in ζ. For fixed ζ it also bounds fourth moments. Compactness and entropy continuity then give a minimum, with energy/moment terms lower semicontinuous. This does not require energy convergence.

Output replacement gives ρ_0≥κτ_{r_0}, hence 0≤−logρ_0≤CW_0 by the logarithm resolvent/inverse-order formula. Positive slicing therefore yields 0≤T_iH_0≤C_iW_i. Replacing output entropy by its cross entropy against the minimizing output gives a majorant touching at that minimum. Its unique Gibbs minimizer has Hamiltonian

    K_i=k_iW_i⁴+W_i^{1/2}B_iW_i^{1/2},     k_i>0, B_i≥0 bounded.

This supplies the exact log identity (4.4); it does not assume Frechet differentiability of infinite-dimensional entropy.

The regularity lemma is a real domain estimate, not just a formal Gibbs ansatz. Set C=kI+W^{-3/2}BW^{-3/2}. The form is ||C^{1/2}W²ψ||², and its inverse is U=W^{-2}C^{-1}W^{-2}, compact, positive and injective. If Kψ_j=u_jψ_j, then ||W²ψ_j||²≤u_j/k, and the coordinate form equation gives

    kW^{7/2}ψ_j=u_jW^{-1/2}ψ_j−BW^{1/2}ψ_j.

The right side is square summable with polynomial bound in u_j. The min-max bound U≤k^{-1}W^{-4} gives polynomial eigenvalue counting. Weighting by exp(−u_j) therefore gives Trρ_iW_i⁷<∞. This proves faithfulness and enough moments for all later weighted traces; uniform seventh-moment bounds as ζ→0 are not needed.

## 4. Hessian contraction rederived with its constants

For a one-input change the exact logarithm identity gives

    J(ρ̃_i)−J(ρ_i)
      =[(1+ε)w_i/h_i]D(ρ̃_i||ρ_i)−D(ρ̃_0||ρ_0)/h_0 ≥0.

Take a traceless Hermitian perturbation A on a finite input eigenblock. It is admissible for two-sided sufficiently small t and has finite fourth moment because every selected eigenvector has finite seventh moment. The input relative entropy has quadratic form Q_i(A)=Σ|A_lr|²/ℓ(p_l,p_r). For a centered finite output eigenblock test Z, the variational Gibbs lower bound on the output relative entropy has t² coefficient

    (1−κ)Tr A T_iZ−||Z||_0²/(2h_0).

This lower bound avoids assuming the actual output perturbation has finite spectral support. With α=(1+ε)w_i h_0/h_i, optimization yields

    2(1−κ)Tr A T_iZ−αQ_i(A) ≤ ||Z||_0²/h_0,
    (1−κ)²||T_iZ−⟨T_iZ⟩I||_i² ≤ (1+ε)w_i||Z||_0².

To justify optimization, trace is continuous for Q_i, and finite eigenblock truncation with one fixed diagonal trace correction is dense in the trace-zero space. The dual metric is precisely the centered logarithmic mean. Dividing by λ_i and using w_i=(1−κ)λ_i proves (4.10). This is a contraction only at the selected minima; no universal sharpened data processing inequality is smuggled in.

Bounded-output compression converges in both arithmetic weighted norms. Complete positivity/Schwarz of the slice and ρ_0≥(1−κ)γ identify the continuous extension with the actual slice on every bounded observable. Finite eigenblock centered tests are invariant under all frequency multipliers: every diagonal entry, including the infinite identity tail, has zero frequency. These observations verify the exact hypotheses of Section 3's interpolation theorem.

## 5. Product-port projection, centered defects and noncommutativity

In either arithmetic inner product, centered one-port observable subspaces are mutually orthogonal under the product input state. The partial-expectation slice is the orthogonal projection onto that subspace. This proves the R_± comparisons simultaneously over i. It does not impose any product structure among modes within a port. The separate Hessian comparisons plus the two slack inequalities supply the r_s and r_s+1 families. Set m_s=1/h_s, x_s=h_sv_s/2, y_s=−h_s/2 in the checked interpolation theorem. The outcome is

    F_s(v)=[b_s(v)−(r_s+1/2)v]/(1−v),
    ℓ(p_l,p_r)F_s(v)=ℓ(r_sp_l,(r_s+1)p_r).

At fixed r_s>0 this positive continuous weight has finite nonzero limits r_s and r_s+1 at the two infinities. Thus it is bounded above and away from zero uniformly in the minimizing state.

The centered defect q_j(Z) has coordinates K_lr overline(d'_lr), where K_lr=(r+1)p_r−rp_l. Since

    K_lr/[hℓ(p_l,p_r)]=(1−v)F(v),

its representing vector is (1−v)d', with exact dual square Σ(1−v)K_lr|d'_lr|². This represents a linear functional on the centered space: q(I)=0, and F(0)=1/h makes the orthogonality condition exactly zero ρ-mean. No diagonal restriction on ρ or d is used.

The required sums are finite. H≤CW⁴ and TrρW⁷<∞ give crossed logarithmic sums bounded by C TrρW⁵, since W²d' costs at most W^{5/2}. For uncrossed terms, ⟨W⁴⟩⟨W⟩≤⟨W⁵⟩, by nonnegative covariance of increasing scalar functions of W. This also establishes absolute summability of both |K| and |vK| coefficients. In particular the signed entropy-production sums are not conditionally rearranged.

For raw convolution, the coefficient-one parts of q add from d_0=Σ_s√λ_s d_s. For the r_s commutator parts, each original creation operator has retained coefficient √λ_s; a discarded-mode commutator has zero partial trace. The total coefficient is Σ_sλ_sr_s=r_0. Finite energy makes dρ, d†ρ and their right-hand counterparts trace class via Hilbert–Schmidt factorization; number cutoffs of discarded operators justify that zero weak commutator even for arbitrary bounded retained Z. There is no assertion that Z preserves an unbounded operator domain.

The complex mean correction under replacement is exactly

    q_0=Σ_iw_i q_i∘L_i
          +κ(1−κ) overline(μ_γ) Tr[(γ−τ_{r_0})·].

The overline is present in the pinned TeX. For scalar J(Z)=√[κ(1−κ)]Tr[(γ−τ)Z], mixture variance gives both arithmetic comparisons with scalar target weight 1. The already proved logarithmic-mean operation gives |J(Z)|²≤||Z||_0²/h_0≤C_0²||Z||_{F_0}². Therefore

    ||q_0||_*≤A_*+√(2κ)C_0M_*.

Young's inequality gives (5.10) when κ≤ε²/[4(ε+2)C_0²], exactly the published condition. The positive margin is uniform in ζ and in the minimizing states.

## 6. Weighted generator algebra, exact cancellation, and the limiting state

For T=W³ρW³ trace class, each term of W²LρW² is a product of bounded factors around T. For example W²dW^{-3} is bounded; likewise the anticommutator factor NW^{-1}. Number cutoffs converge in this weighted trace norm. The same construction works on the combined ports, whose total number is invariant under passive rotation. Weighted partial trace is continuous by insertion of (W_0^k⊗I)W_tot^{-k}, of norm ≤1. Thus the elementary covariance calculation extends from finite number support and gives

    δ_0=(1−κ)Σ_iΦ_i(δ_i),
    Trδ_0H_0=(1−κ)Σ_iTrδ_iT_iH_0.

These are genuine trace-class identities. H_s≤C_sW_s⁴ means W_s^{-2}H_sW_s^{-2} is bounded; its pairing with W_s²δ_sW_s² defines the logarithmic trace. Decomposing the latter's positive/negative parts and conjugating back justifies slicing on a difference of finite-fourth-moment positive operators. One is not differentiating entropy along an unbounded flow, nor treating ρ+tδ as a two-sided state curve.

Pairing the exact Gibbs log identities with δ_i now gives (6.4). In an eigenbasis, direct dissipator expansion gives

    σ_s=Trδ_sH_s/h_s=−Σ_{j,l,r}v_s(l,r)K_{s,lr}|d'_{s,j,lr}|².

Subtracting this from the checked dual norm leaves ΣK|d'|²=(r+1)e'−r(e'+n)=e'−nr, using the full Fock CCR. The absolute summability above and the W³ρW³ convergence justify these expansions. Consequently σ_s=||q_s||_*²−(e'_s−nr_s).

The other exact identities are Trδ_iN_i=−(e'_i−nr_i)−|μ_i|² and

    Trδ_iW_i⁴ = Trρ_i{(r_i+1)N_i[N_i⁴−(N_i+1)⁴]
              +r_i(N_i+n)[(N_i+2)⁴−(N_i+1)⁴]}.

The bracket is a degree-four polynomial with leading coefficient −4 independent of r_i and n. Thus it has a finite uniform upper bound. Although individual terms before cancellation involve a fifth moment, the established seventh moment makes that computation legitimate.

For centered energies, independence across ports gives

    e'_0−nr_0=Σ_iw_i(e'_i−nr_i)+κ(1−κ)|μ_γ|².

Insert all three identities into stationarity. Every centered-energy term cancels with the displayed coefficients, leaving exactly

    0=||q_0||_*²−(1+ε)A_*²−εM_*²
          −κ(1−κ)|μ_γ|²+ζP,
    0≤−(ε/2)(A_*²+M_*²)+Cζ.

Thus means and defect norms vanish as ζ→0. A uniform energy bound gives a trace-norm convergent input subsequence. Fixed finite number-basis tests have uniformly bounded centered F norms, and d†Z and Zd† are bounded finite rank. Consequently weak defects pass to the limit without assuming energy or first-moment convergence. The limit obeys

    (r_i+1)d_j ρ̂_i=r_iρ̂_i d_j  for every j.

For a matrix entry with p_j>0 this says

    (r_i+1)√p_j (ρ̂_i)_{p,b}
       =r_i√b_j (ρ̂_i)_{p−e_j,b−e_j}.

If p_j>b_j, iteration reaches a zero right side; if p_j<b_j, use self-adjointness. All off-diagonal entries vanish. Diagonal entries have ratio r_i/(r_i+1) under each coordinate increment. Trace one forces the entire n-mode product thermal state. This removes arbitrary internal correlations as well as coherences; internal independence was a conclusion for the limit, not an assumption on the original state.

The output limit is thermal with parameter r_0. All three entropies converge under the common energy bounds. The entropy part of J_ζ therefore tends to zero; the two penalties remain nonnegative. This contradicts the fixed negative minimum bound. No energy-convergence claim, penalty-vanishing claim, or interchange of the other regularization limits is needed. This completes the full two-input finite-energy theorem and hence VE.

## 7. Falsification controls and their proper status

`verify_controls.py` is independent standard-library code. It checks the stationarity cancellation and fourth-moment leading coefficient by exact rational polynomial algebra. Changing the energy penalty coefficient produces a nonzero symbolic residual. It checks the scalar minimization at x=y, x=−y, x=y=0 and unequal signed values; doubling E produces a detected residual. These finite scalar checks support transcription, not the universal interpolation proof.

The code additionally uses a faithful noncommuting four-dimensional density matrix with nonzero complex annihilation mean. It evaluates the dissipator trace and the centered spectral defect norm directly. A finite Fock annihilator obeys [d,d†]=I−D|top⟩⟨top|, so the actual identity has correction rDρ_top,top. The code obtains that nonzero residual (0.7) if infinite CCR is incorrectly assumed, and a corrected-identity residual of approximately −4.44×10^{-16}. This is an explicit negative control against a common false finite-truncation validation. It is not a numerical proof of EPnI or evidence that finite dimensions satisfy exact CCR.

## 8. Boundary and scope conclusions

VE at t=0 is the vacuum output, and at t=1 is equality. At S(ρ)=0 the asserted bound is nonnegative entropy; it also follows from the full theorem. Finite energy ensures finite entropy and finite attenuated output energy. Any finite n is covered by finite number-sector degeneracy and the n-coordinate thermal recurrence. Nothing in the proof restricts internal entanglement, separability, number diagonality, or Gaussianity. Independence between input ports is essential and explicitly used. This audit establishes no infinite-energy, infinitely-many-mode, input-environment-correlated, amplifier, or heterogeneous-attenuator extension.

Adversarial conclusion: no substantive error or unresolved central gap found in the full proof chain. VE is supported in precisely the scope required. This is a mathematical source audit with checkable derivations; it is not a claim of a compiled formal proof.
