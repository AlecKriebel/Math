# Public mathematical review edition: target 30004906

This unrefereed review edition records an internal AI audit. It has not received human peer review or formal proof-assistant certification. It is not a computational reproduction package. The unrestricted target remains unresolved by this work. AI tools were used in research, drafting, and checking. No novelty or present-day openness certification is claimed.

The complete candidate argument, source repair, and independent rational algorithm supplement follow as Parts I–III. The supplement hardens the actual algorithm and leaves the reduction and guarantee unchanged.

## Part I. Candidate proof

# Maximum nonsymmetric principal determinants: a rank-boundary reduction and route obstructions

Target: 30004906 / OWR-8415356-017. Status: **proved partial result; unrestricted target unresolved**. No novelty claim is made.

## 1. Exact scope and results

Given a real matrix L with H=(L+Lᵀ)/2 positive semidefinite and 1≤k≤n, write f(S)=det L[S,S] and OPT=max over |S|=k of f(S). The target is a polynomial-time algorithm with f(S)≥2^(−Ck)OPT for an absolute C. This is a determinant ratio, not a guarantee for log determinant or a parameterized running time.

This report proves:

1. **Rank boundary.** If rank L≤k+1, there is a deterministic polynomial-time 2^O(k)-approximation. In fact, when rank L=k+1 and h=rank H>0, a factor 2h k^k/k! suffices, and hence a factor (4e)^k suffices. The reduction uses h rational Gram-determinant objectives and handles singular H. If rank L=k there is one Gram objective; if rank L<k the optimum is zero. The h=0, rank L=k+1 branch also has zero optimum.
2. **Robust local-search obstruction.** For every fixed radius ρ≥1 and arbitrarily large k, explicit rational, strictly nonsymmetric matrices with L+Lᵀ positive definite have a strict ρ-local maximum whose gap from a displayed competitor is at least (4k/(17ρ²))^k. Thus the statement “every constant-radius local optimum is a 2^O(k)-approximation” is false even without singularities or zero minors.
3. **A precise failure of the rank-boundary extension.** The symmetric first cofactor form used in result 1 is PSD; its direct second-compound analogue can be indefinite even when H=I. An explicit rational 4×4 example has a negative quadratic value −6. This rejects that particular PSD-decomposition route at rank k+2, not all possible algorithms.

All three results have written arguments below. Finite exact checks are supporting tests, not proofs of universal assertions. Historical validation used newly written exact-arithmetic checks; no source-author code was run. No optimizer was implemented or benchmarked. Part III below supplies the complete independently written rational polynomial-bit optimization and exact-rounding proof.

## 2. Source baseline and later claims

The original problem is Anari's contribution in [OWR 53/2021](https://doi.org/10.4171/owr/2021/53), printed pp. 2944–2945, PDF pp. 52–53. The permitted class includes pure skew matrices. For a rectangular A, the skew block matrix [0 A; −Aᵀ 0] links even-size principal minors with squared nonprincipal minors; this is only a special case.

[Anari–Vuong, COLT 2022](https://proceedings.mlr.press/v178/anari22a.html), Definition 3, Corollary 7 and Theorem 8, supplies the k^O(k) ratio. Sections 3–4 use induced-marginal initialization, multiplicative-improvement local search and a polynomial-loss exchange inequality; Appendix A supplies the two-step mixing input. Proposition 31 exponentiates the exchange loss. Appendix B gives the stated arithmetic running time O(n⁴k+n²k⁵ log n). This runtime statement is not a numerical error or rational-bit analysis. The exact algorithm/proof chain was inspected, with external spectral/stability dependencies not independently reproved. Appendix C explains why one-step search can fail without any bounded ratio.

The constant-radius obstruction is already present in the symmetric setting: [Anari–Vuong, APPROX 2020, §3, Remark 9](https://arxiv.org/abs/2004.13018) uses a Hadamard construction. Section 5 below is an explicitly rational, strictly accretive, strictly nonsymmetric variant, with quantitative margins; it is not presented as a new general local-search lower bound.

Two later-looking claims were checked against primary sources. [Mahabadi–Vuong's coreset paper](https://arxiv.org/abs/2211.00289), dated October 8, 2025 in the inspected manuscript and listed by the author for AISTATS 2026, works with Gram/strongly Rayleigh objectives and improves local-search running time in its setting. Its statements do not establish the unrestricted target here. [Du et al., EMNLP 2025](https://aclanthology.org/2025.emnlp-main.1376/) gives, in the inspected appendix, conditioning-dependent guarantees for log determinant inherited from earlier work. Such guarantees do not give a uniform determinant ratio 2^O(k).

These are bounded source checks, not a certification of current openness or priority. SOURCES.json records historical bytes, hashes and inspection limits. Part II below records the proof chain and a local repair of one sector-angle slip in the 2022 exposition.

## 3. Algebraic preliminaries, including degeneracies

**Lemma 1 (nonnegative determinants).** If B=G+A is real, G is symmetric PSD and A is skew, then det B≥0. If B is invertible, det B>0.

For ε>0, conjugation by (G+εI)^(−1/2) gives a real skew matrix K. Its eigenvalues occur as pairs ±it, with possibly zeros. Therefore

  det(B+εI)=det(G+εI) ∏(1+t_j²)>0.

Taking ε↓0 proves nonnegativity. An invertible matrix has nonzero determinant, so its determinant is positive. This argument applies to every principal compression. In particular, all f(S) are nonnegative and the approximation guarantee is meaningful even when OPT=0.

**Lemma 2 (common row and column spaces).** An accretive real L has ker L=ker Lᵀ.

If Lx=0, then 0=xᵀLx=xᵀHx. PSD implies Hx=0, so Ax=Lx−Hx=0 and Lᵀx=Hx−Ax=0. Apply the same argument to Lᵀ for the reverse inclusion. Taking orthogonal complements proves range L=range Lᵀ.

Consequently, if r=rank L>0 and U is any n×r full-column-rank basis matrix for range L, there is an invertible r×r matrix C with

  L=U C Uᵀ,    (C+Cᵀ)/2 PSD,    det C>0.

For an explicit rational construction, take U to consist of pivot columns of rational L, let P=(UᵀU)^(−1)Uᵀ and C=P L Pᵀ. The common-range statement proves the factorization. Congruence proves accretivity of C; rank proves its invertibility; Lemma 1 proves det C>0. Also rank((C+Cᵀ)/2)=rank H.

If r<k, every size-k minor is zero. If r=k, then for every |S|=k,

  f(S)=det C · det(U[S,:])².

Thus the rank-k case is exactly a positive constant times a symmetric Gram determinant, including invertible pure-skew C when k is even.

## 4. The rank-(k+1) theorem

### 4.1 Exact positive decomposition

Assume r=k+1. For a k×r matrix B define its signed cofactor vector q(B) by

  q_j(B)=(−1)^(r+j) det B[:,[r] minus {j}],    1≤j≤r.

Then det([B;vᵀ])=q(B)ᵀv. Applying Cauchy–Binet twice, or the adjugate identity, gives

  det(B C Bᵀ)=det C · q(B)ᵀ C^(−1) q(B).

For clarity about orientation, the double Cauchy–Binet sum uses complementary minors C[−i,−j]; its coefficient is (−1)^(i+j)det C[−i,−j]=adj(C)_{j,i}. Transposing this coefficient matrix does not change its scalar quadratic form. Hence the displayed formula holds without any symmetry assumption on C.

Put G=(C+Cᵀ)/2. The symmetric matrix

  Q=det C · (C^(−1)+C^(−ᵀ))/2
   =det C · C^(−ᵀ) G C^(−1)

is PSD and has rank h=rank H. Since a skew quadratic form vanishes,

  f(S)=q(U[S,:])ᵀ Q q(U[S,:]).                       (1)

A pivoted rational LDL decomposition supplies

  Q=Σ_(j=1)^h d_j v_j v_jᵀ,    d_j>0.

No square roots are required. If Q=0, equation (1) proves f(S)=0 for every S, and the algorithm returns any k-set.

For each nonzero v=v_j, pick p with v_p≠0. Define an r×k matrix T_v whose columns, in increasing i≠p order, are

  e_i − (v_i/v_p)e_p.

The columns span v's orthogonal hyperplane. The cofactor vector of T_vᵀ equals ±v/v_p: it is perpendicular to the k rows, and its p-th coordinate is ±1. Thus Cauchy–Binet gives, for every k×r B,

  det(B T_v)² = (q(B)ᵀv)² / v_p².

Define W_j=U T_(v_j) and w_j=d_j(v_j)_p²>0. Each W_j has full column rank k. Substituting in (1) proves the exact identity

  det L[S,S] = Σ_(j=1)^h w_j det(W_j[S,:])².          (2)

Every summand is a positive multiple of a principal size-k determinant of the rational symmetric PSD matrix W_j W_jᵀ. In particular, singular symmetric parts and zero individual minors require no division by those minors.

### 4.2 Approximation algorithm

Given an α(k)-approximation subroutine for a rank-k Gram determinant:

1. Compute r=rank L. Handle r<k and r=k as in Section 3.
2. For r=k+1 compute Q and the h Gram components (2). If h=0 return any k-set.
3. For each j run the PSD subroutine on W_j W_jᵀ and obtain a k-set S_j.
4. Return a candidate S_j having largest original determinant det L[S_j,S_j].

If S* maximizes f, some component j has w_j det(W_j[S*,:])²≥OPT/h. For that j,

  f(S_j) ≥ w_j det(W_j[S_j,:])²
         ≥ (w_j/α(k)) max_|S|=k det(W_j[S,:])²
         ≥ OPT/(h α(k)).

This proves the claimed h α(k) ratio. The rank-k branch needs only α(k). The factor h is merely the certified guarantee of this selection argument; no lower bound claiming it is necessary is made.

### 4.3 Exponential PSD subroutine and computation model

The input model for the polynomial-bit assertion is rational L, with signed integer numerators and positive integer denominators in binary. Rank, kernel, accretivity tests, inverses and the pivoted PSD decomposition are exact rational operations. Their output bit lengths are polynomial in n and the input length: after clearing denominators, elimination entries are ratios of minors, whose bit sizes are polynomial by the determinant expansion/Hadamard bound. T_v, W_j and w_j involve only polynomially many rational operations on these bounded-size elimination outputs. At most k+1 PSD calls are used. Determinants used to compare the returned candidates are computed exactly.

For completeness, the needed PSD guarantee is the full-rank-vector case of [Nikolov, Randomized Rounding for the Largest Simplex Problem](https://arxiv.org/abs/1412.0036), Theorems 10 and 19 (also Theorem 18 for general selected size). A rational additive-1/2 approximate D-optimal-design solution gives a deterministic factor at most

  α(k)=2 k^k/k!.

Here is the mechanism. If the rows of W are a_iᵀ, approximately maximize log det(Σ c_i a_i a_iᵀ), subject to c_i≥0 and Σ c_i=k. An indicator of an optimal k-set is feasible. For p_i=c_i/k, k independent draws have expected squared volume

  k! det(Σ p_i a_i a_iᵀ)
  ≥ (k!/k^k)e^(−1/2) max_|S|=k det(W[S,:])².

The equality follows by determinant multilinearity and cancellation of repeated-row terms. Deterministic conditional expectation preserves at least this value. Conditional expectations are coefficients of determinant polynomials and can be computed with rational arithmetic: after fixing t distinct rows F, the expectation of the final squared determinant is

  (k−t)! [z^(k−t)] det(W_FᵀW_F + z Σ p_i a_i a_iᵀ).

This follows by expanding over the remaining rank-one draws; the rank-t fixed matrix forces all t fixed-row contributions at that coefficient. Greedily choosing a next row whose conditional expectation is at least the current expectation ends at a distinct k-set whenever the starting expectation is positive. Full column rank ensures this positivity. The cited convex-optimization subroutine is used in the ordinary rational weak-optimization model, with a fixed additive tolerance; exact real convex optimization is not being assumed. No optimizer execution or floating-point stability bound is claimed. Part III supplies a complete rational fixed-step implementation proof, with polynomial iteration and denominator bounds, the leverage stopping certificate, and exact deterministic rounding, giving this same factor without an external optimizer.

Since k!≥(k/e)^k and h≤k+1≤2^k,

  h α(k) ≤ 2(k+1)e^k ≤ (4e)^k.

Thus the rank-boundary theorem has an absolute exponential ratio and polynomial running time in the rational encoding length. For unrestricted exact real inputs, the algebraic reduction remains valid and gives the corresponding real-arithmetic/oracle statement; it is not a claim that arbitrary real numbers have finite encodings.

### 4.4 Edge cases

- k=1 is also solvable exactly by the largest diagonal entry, without any rank restriction.
- rank L<k: OPT=0, so any k-set is correct.
- rank L=k: the nonzero factor det C is positive even if G is singular or zero.
- rank L=k+1 with H=0: Q=0, so all size-k principal minors vanish. An invertible skew C has even r, making k odd, consistently with skew parity.
- Other odd k are not discarded; mixed symmetric/skew inputs can have positive odd-size minors and are covered by (2).
- Rectangular skew-block inputs are included whenever they meet the rank boundary, but they do not substitute for general L.

## 5. A strictly nonsymmetric constant-radius trap

Fix a positive integer radius ρ. Let k≥ρ be a power of two, and let R be the Sylvester Hadamard matrix, so R Rᵀ=kI. Set

  t=1/(2ρ),   δ=1/(16k),   ε=t/(2k),
  a=1+δ,      b=t+ε,       c=t−ε,      d=kt²+δ,

and define the 2k×2k rational matrix

  L = [ aI     bR  ]
      [ cRᵀ    dI  ].

It is strictly nonsymmetric because b≠c. Its symmetric part is [aI tR; tRᵀ dI], which is positive definite: a>0 and

  ad−kt²=δ+δkt²+δ²>0.

Let S be the first k indices. Its determinant is a^k. A k-set obtained by replacing s≤ρ of these indices removes a row set I from R and inserts a column set J, both of size s. Write D=R[I,J]. Orthogonality gives R[[k] minus I,J]ᵀ R[[k] minus I,J]=kI_s−DᵀD. The Schur complement therefore yields the exact ratio

  f((S minus I) union (k+J))/f(S)
    =det(γ I_s+β DᵀD),

  γ=(ad−kbc)/a²,    β=bc/a²>0.

All eigenvalues in this determinant are positive. Since D has s² entries of squared value 1, its Gram trace is s². Arithmetic–geometric mean on eigenvalues gives

  det(γ I_s+β DᵀD) ≤ (γ+βs)^s.

Now

  ad−kbc=δ+δkt²+δ²+kε²
         ≤1/16+1/64+1/256+1/16=37/256,

and βs≤t²ρ=1/(4ρ)≤1/4. Thus

  0 < f(neighbor)/f(S) ≤(101/256)^s <2^(−s)<1.

S is a strict ρ-local maximum, with a fixed loss for every nontrivial move in its neighborhood. Meanwhile the last k indices have determinant d^k and

  OPT/f(S) ≥ (d/a)^k ≥ (4k/(17ρ²))^k,

because d≥k/(4ρ²) and a≤17/16. For fixed ρ this exceeds every prescribed 2^(Ck) for large enough k. Matrix entries have O(log k+log ρ) bit length.

This proves a barrier to guarantees based solely on reaching an arbitrary fixed-radius local optimum. It does **not** prove that a globally informed initialization, a special tie policy, a larger nonconstant neighborhood, or a different algorithm cannot meet the target. In particular, no assertion is made that the induced-greedy initialization in the 2022 algorithm reaches this particular trap.

## 6. Why the immediate cofactor extension fails

At rank r=k+1, the dual exterior power has degree one and the symmetric inverse is PSD. At rank r=k+2 the analogous form involves the second compound. PSD is no longer available even for strict accretivity.

Take

  C=[ 1  2  0  0 ]
    [−2  1  0  0 ]
    [ 0  0  1  2 ]
    [ 0  0 −2  1 ].

Its symmetric part is I and det C=25. Let C₂(M) denote the matrix of all 2×2 minors, in index order 12,13,14,23,24,34. Direct determinant calculation gives

  25 Sym(C₂(C⁻¹)) =
  [5 0  0  0 0 0]
  [0 1  0  0 4 0]
  [0 0  1 −4 0 0]
  [0 0 −4  1 0 0]
  [0 4  0  0 1 0]
  [0 0  0  0 0 5].

The vector z=(0,1,0,0,−1,0) has quadratic value −6. Therefore this form cannot have a decomposition as a sum of nonnegative rank-one quadratic forms, and the rational-PSD-decomposition step in Section 4 does not extend verbatim. The vector is not a decomposable bivector; nonnegativity of determinants on actual subspaces is not contradicted. The Hodge sign/permutation changes relating complementary minors are invertible orthogonal congruences and do not remove this negative direction.

There is also a support-level obstruction to replacing every nonsymmetric objective by one PSD Gram objective. For the pure-skew block diagonal J⊕J with J=[0 1;−1 0], the positive size-two subsets are exactly {1,2} and {3,4}. Gram determinants are positive exactly on linearly independent pairs. If v₁,v₂ and v₃,v₄ were independent pairs while all cross pairs were dependent, v₃ would have to lie in both distinct lines spanned by v₁ and v₂, forcing v₃=0, a contradiction. Hence no PSD matrix reproduces this support. This is an obstruction to an exact single-Gram replacement, not a hardness theorem for approximation.

Finally, optimizing only H is not a uniform approximation: on diag(2I₂, [1 M;−M 1]), the symmetric-part optimum has determinant 4, while the last pair has original determinant 1+M². Letting rational M grow makes the ratio unbounded at fixed k=2.

## 7. Validation and remaining question

Historical candidate validation used exact rational arithmetic and explicit exceptions rather than assertions. It checked the factorization and sum-of-Grams identity on deterministic generated inputs, every relevant principal subset of those inputs, local-neighbor Schur identities, the compound obstruction, skew parity, zero/rank branches, and the conditional-expectation identity. It also rejected intentionally invalid assumptions and altered coefficients. These finite synthetic checks supplement the written proofs.

Historical normal, -O, and -OO runs and separate expected-failure probes are summarized with authenticated receipt identities in VERIFICATION.json. No finite enumeration is a proof of the rank-boundary algorithm, asymptotic local-search lower bound, or general approximation target. No convex PSD optimizer was executed; candidate-selection tests used exhaustive exact component maximization only on small finite instances. Executable checks and raw generated inputs/results are not distributed in this prose edition.

**Residual:** the desired uniform 2^O(k) approximation for arbitrary rank≥k+2 (apart from separate trivial regimes such as k=1) remains unresolved in this work. Rank k+2 is the first place this specific PSD cofactor argument can fail. It is not established here as a computational hardness threshold. The source searches do not establish novelty or rule out later results.


## Part II. Complete source repair and dependency audit

# Primary proof inspection and two exact-model clarifications

This is a targeted source audit, not an independent reproving of every cited stability, spectral, convex-optimization, or complexity theorem. Its historical scope and reading locations are recorded in SOURCES.json. No claim is made that the general problem is solved.

## Baseline chain

The 2022 PMLR PDF was checked at Definition 3; Theorems 2, 5, 8 and 32; Corollary 7; Algorithms 2–3; Lemmas 18, 26 and 30; Proposition 31; and Appendices A–C. The recorded inspection included the algorithm and proof sections. The crucial ratio loss is a polynomial-in-k exchange factor raised to as much as k. Faster mixing with the same polynomial type alone does not turn that argument into an absolute exponential ratio.

External results about sector stability and local-to-global spectral gaps remain imported. The PSD approximation primitive in the main report is anchored to Nikolov's deterministic rounding theorem, rather than being inferred from experiments. The cofactor and strict-nonsymmetry arguments in Part I are independently written mathematical arguments.

## An exact rational implementation of the baseline initialization

This paragraph gives its own finite-encoding clarification; it does not attribute a bit-complexity theorem to the PMLR arithmetic-runtime statement.

For any Y⊆[n] with |Y|≤k, let

  m(Y)=Σ_{S⊇Y, |S|=k} det L[S,S].

The determinant's diagonal expansion gives exactly

  m(Y)=[λ^(n−k)] det(L+λ diag(1_[n]\Y)).

Hence n+1 rational evaluations and polynomial interpolation compute m(Y) exactly. No inverse of a possibly singular principal minor is required. After clearing denominators of rational input, evaluations at 0,1,…,n and the Vandermonde inverse have polynomial bit length. Fraction-free elimination/interpolation therefore gives polynomial bit complexity, albeit not necessarily the sharper arithmetic count printed in the source.

If m(∅)=0, every size-k determinant is zero by nonnegativity and any k-set is valid. Otherwise,

  Σ_{i∉Y} m(Y∪{i})=(k−|Y|)m(Y).

Inductively maximizing these marginals yields det L[S₀,S₀]≥m(∅)/binom(n,k)≥OPT/binom(n,k)>0. A local search accepting only improvements strictly larger than a factor of two takes at most log₂ binom(n,k) successful moves. Each fixed-radius neighborhood is polynomial-sized. Determinants and comparisons can be computed exactly with polynomial-bit rational arithmetic. The imported exchange theorem then provides the known k^O(k) ratio. This argument explicitly handles the support/zero case before using logarithms.

## Sector-angle slip: a self-contained repair of the needed coefficient step

The rendered PMLR PDF, p.18, says that a root with argument π/q is inside Γ_α under q>1/α. That literal membership is false, for example α=1/2 and q=3: 1/3>1/4. The needed and correct region is Γ_(2α). This is a local exposition issue; the following elementary argument supplies a valid sector for the intended step. It does not invalidate the theorem or improve its approximation ratio.

Recall Γ_α={z≠0: |arg z|<απ/2}. Fix α=1/r for a positive integer r, q>r, and a polynomial

  p(z)=Σ_{j=0}^q a_j z^j,    a_j≥0,

with a₀a_q>0, having no zero in Γ_(2α). We claim

  Σ_{j=1}^{q−1} a_j ≥ sin(π/(4r)) min(a₀,a_q).       (A)

Write p=p₀+p₁, with p₀=a₀+a_q z^q. Put

  θ=(π/q+min(2π/q,απ))/2,
  η=qθ−π=min(π,(αq−1)π)/2.

Then π/q<θ<απ, and π/(2r)≤η≤π/2. The truncated sector |arg z|<θ lies within Γ_(2α) and contains the two roots of p₀ of arguments ±π/q, once its inner and outer radii surround their modulus. On each boundary ray z=R exp(±iθ), set x=a₀ and y=a_qR^q. Direct calculation gives

  |x+y exp(i(π+η))|²
    =(x−y)²+4xy sin²(η/2)
    ≥sin²(η/2)(x+y)².

Thus |p₀(z)|≥sin(π/(4r)) min(a₀,a_q) max(1,R^q), while |p₁(z)|≤(Σ_middle a_j)max(1,R^q). If (A) fails strictly, |p₁|<|p₀| on the two rays. On an inner circular arc sufficiently near zero, p₀ tends to nonzero a₀ while p₁ tends to zero. On a sufficiently large outer arc, the degree-q endpoint dominates the lower-degree p₁. Rouché's theorem on this bounded annular sector forces p to have the same positive number of zeros as p₀ inside Γ_(2α), a contradiction. This proves (A).

For the associated loop-free weighted graph cut, write A and C for the weights of q-sets wholly on the two sides and B for weights of crossing q-sets. Each crossing set contributes at least q−1 to cut weight and at most q(q−1) to either side's volume. Consequently

  conductance ≥ B/[q(min(A,C)+B)].

When A,C>0, (A) supplies B≥σ min(A,C), σ=sin(π/(4r)), giving conductance at least σ/[q(1+σ)]. If one endpoint weight is zero, a positive-volume cut necessarily has B>0, and the same calculation gives at least 1/q. This repairs the needed polynomial cut bound before the source's external local-to-global step. No author code or unverified floating-point root test is involved.

## Later-source discrimination

The coreset manuscript inspected here is the complete 21-page arXiv PDF, but only its title, abstract, definitions and main-result discussion were read closely (PDF pp.1–5); its remaining proofs were not audited. It concerns symmetric Gram and strongly Rayleigh objectives, including constrained settings. Its cited speedup changes a running-time dependence, not the unrestricted nonsymmetric determinant ratio.

The EMNLP 2025 paper's relevant appendix was inspected for the stated greedy guarantee. It is a bound on log determinant with singular-value conditions/corrections, not the requested uniform multiplicative determinant factor. The paper's empirical conclusions are not evaluated here.


## Part III. Complete independent rational polynomial-bit supplement

# A fully rational PSD approximation primitive

This is an independently written proof-hardening supplement for the candidate's rational polynomial-time assertion. It does not alter the candidate or its guarantee. It removes the need to leave the precise weak-optimization implementation implicit. No optimizer, including the procedure below, was executed in this audit. The exact tests check only its one-step determinant formula and rational constants. The construction is a standard vertex-direction/D-optimal-design argument; no novelty is asserted.

## 1. Input and aim

Let W be an n-by-k rational matrix of column rank k, with row vectors a_i^T. We need a deterministic polynomial-bit algorithm returning a k-set S with

    det(W[S,:])^2 >= (k! / (2 k^k)) max_{|T|=k} det(W[T,:])^2.

The full-rank case of Nikolov's [Randomized Rounding for the Largest Simplex Problem](https://arxiv.org/abs/1412.0036), Theorem 10, gives the design-to-volume argument, and Theorem 19 gives deterministic rounding. The following direct rational construction makes the optimization and rounding model explicit.

Find k independent rows by rational elimination. Start with probability p_i=1/k on these rows and zero elsewhere. Then

    D(p) = sum_i p_i a_i a_i^T

is positive definite. Set tau=1/(4k^2), a rational constant. At each iteration compute all rational leverage values

    g_i = a_i^T D(p)^(-1) a_i,
    g = max_i g_i.

If g <= k+1/2, stop. Otherwise choose an attaining i and replace

    p <- (1-tau)p + tau e_i.

The update preserves a probability vector and positive definiteness, since D(new) >= (1-tau)D(old) > 0. Every decision uses rational arithmetic only.

## 2. Termination and its bit bound

The matrix determinant lemma gives the exact update ratio

    det D(new) / det D(old)
      = (1-tau)^(k-1) (1+tau(g-1)).

This is increasing in g. On a performed step, g>k+1/2. Put x=tau(k-1/2). Using

    log(1-tau) >= -tau - tau^2/[2(1-tau)],
    log(1+x) >= x-x^2/2,

we obtain

    log det D(new) - log det D(old)
      >= tau/2 - (tau^2/2)[(k-1)/(1-tau)+(k-1/2)^2]
      >= tau/2 - tau^2 k^2
      = 1/(16k^2).

For the second inequality, tau<=1/4 implies (k-1)/(1-tau)<=2(k-1), while (k-1/2)^2<=k^2 and k^2+2k-2<=2k^2 for every integer k>=1. The logarithmic inequalities follow from their power series, or by integrating 1/(1-t) and 1/(1+t); no numerical logarithm is needed by the algorithm.

To bound the possible number of steps, clear all input denominators with one integer Delta, and write a_i=u_i/Delta with integer coordinates |(u_i)_j|<=A and A>=1. Delta and A have polynomial bit length in the rational input encoding. For any probability vector, every eigenvalue of D is at most max_i ||a_i||^2<=kA^2/Delta^2, hence

    det D <= (kA^2/Delta^2)^k.

For the selected nonsingular integer row matrix B_int, |det B_int|>=1. Therefore the initial determinant is

    det D(start) = det(B_int)^2/(k^k Delta^(2k))
                 >= 1/(k^k Delta^(2k)).

The logarithm of the ratio between the upper bound and the initial value is at most 2k(log k+log A). Thus there are at most 32k^3(log k+log A) performed steps, with an immaterial final integer rounding. This is polynomial in the input encoding length.

Crucially, this is a fixed rational step. After T iterations every p_i has a common denominator dividing k(4k^2)^T. The probability bit lengths are O(log k+T log k), not the output of uncontrolled adaptive rational recurrences. D, its inverse, and each leverage value have polynomial bit length by rational elimination and bounds on minors. Each iteration uses polynomially many rational operations. This proves polynomial bit complexity without invoking an exact-real or unspecified-precision optimizer.

## 3. The stopping certificate

Let p* maximize det D over the probability simplex. A positive optimum exists because the initial design is positive definite. For positive definite D and D*, the scalar inequality log x<=x-1 applied to the eigenvalues of D^(-1/2)D*D^(-1/2) gives

    log det D* - log det D <= tr(D^(-1)D*)-k
                           = sum_i p_i* g_i-k
                           <= g-k <= 1/2.

Thus the returned rational p is additive-1/2 optimal for log determinant. Equivalently c_i=kp_i is additive-1/2 optimal in the candidate's sum-c_i=k formulation.

For a k-set T, the uniform probability vector on T is feasible and has det D=det(W[T,:])^2/k^k. Hence

    det D(p) >= exp(-1/2) OPT_Gram/k^k.

## 4. Exact deterministic rounding

Draw k independent row indices with replacement from p. Repeated indices have zero squared determinant. Cauchy-Binet yields

    E[det(selected rows)^2] = k! det D(p).

After t row indices F=(i_1,...,i_t) have been fixed, let A_F=sum_{s=1}^t a_{i_s}a_{i_s}^T. The conditional expectation over the remaining k-t independent draws is

    (k-t)! [z^(k-t)] det(A_F+zD(p)).

To justify the coefficient, apply Cauchy-Binet to the rank-one columns contributing to A_F and D. A term of degree k-t in z must choose all t fixed columns; if they are dependent, both sides vanish. Each distinct set of remaining columns occurs in (k-t)! draw orders. This proves the displayed identity, including dependent prefixes. It conditions on a fixed ordered prefix, not on the different event that a set is somewhere contained in a random multiset.

Evaluate det(A_F+zD) at z=0,1,...,k and interpolate exactly to obtain its coefficient. These matrices, determinants, and interpolation denominators have polynomial bit lengths. For each possible next index, compute the new conditional expectation and choose the largest. Their p-weighted average is the current value, so the chosen value is at least the current one. A repeated or dependent prefix has zero continuation value; since the starting expectation is positive, the resulting k indices are distinct and independent. Their squared determinant is at least

    (k!/k^k) exp(-1/2) OPT_Gram
      > (k!/(2k^k)) OPT_Gram.

There are k stages with n candidate continuations and k+1 determinant evaluations per continuation. This is polynomial time and polynomial bit complexity.

## 5. Consequence for the audited reduction

Applying this primitive to each of the candidate's h positive rational Gram components and comparing original determinants returns a factor 2h k^k/k! approximation. For rank L=k one component suffices. The algebraic decomposition and singular/zero branches need no change. This proof supplements the candidate's correctly stated imported optimizer guarantee; it does not turn the general-rank problem into a solved problem.
