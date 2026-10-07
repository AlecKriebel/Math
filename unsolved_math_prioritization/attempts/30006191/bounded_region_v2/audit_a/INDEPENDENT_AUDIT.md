# Independent full-proof audit: bounded-region fermion discontinuity

Problem 30006191 / OWR-14299085-005. Audited 7 October 2026.

## Verdict

**PASS.** The frozen proof establishes the requested existential norm-discontinuity counterexample for the literal spatially restricted interaction, in dimension three. No correction is required. The acceptance covers both the density-density convention and the normal-ordered convention, with one fixed bounded region, one fixed smooth compactly supported potential, and one fixed normalized test function. The explicit varying fixed-particle-number Slater states witness a norm difference converging to 2.

This is an independent mathematical review of `BOUNDED_REGION_PROOF.md`, not an inference from a full-space result or from numerical checks. No other new audit was consulted. This report counts as one audit. The original author packets and source files were not modified, and no publication was performed.

### Exact accepted bytes

- Proof: `BOUNDED_REGION_PROOF.md`, 12,771 bytes.
- Proof SHA-256: `2b7c22cfc54049a9e51fe5eb4eb283ba911e6f27e8b6e4dc9557927bc04d7350`.
- Author manifest SHA-256: `d6a0862cbf2f6500cc5fd7ee2239e0e8a2c5864c9d09a6cd9a13b1b4f99176ef`.

The final frozen proof was reread in full. Any later change to the proof requires review of the changed bytes; numerical similarity is not acceptance.

## 1. Source and quantifier alignment

The official [Oberwolfach Report 7/2025](https://ems.press/content/serial-article-files/51350), DOI [10.4171/owr/2025/7](https://doi.org/10.4171/owr/2025/7), was inspected in text and as rendered pages. Printed page 371 places both interaction variables in the same region while leaving the kinetic energy on the whole space. Printed page 364 explicitly identifies the interaction region as bounded. Printed page 365 distinguishes pointwise operator-norm continuity from strong-operator continuity. The adjacent fixed-density discussion is a separate question and does not impose a fixed-density condition here.

The inspected PDF has 407,216 bytes and SHA-256 `7eaef18918195d4911ed399f76caec0bbb1fbc1432eacf838e06f403900b09ba`. The official public URL was also opened successfully during this audit. No copied source text or source PDF is included in this public audit packet.

The proof correctly chooses d = 3 and supplies an example, rather than claiming a theorem for every potential or every dimension. Its normal-ordered companion also covers the conventional interaction used in the earlier exposition. Its argument is independent of the cited full-space discontinuity theorem. Historical priority and exhaustive literature novelty are outside this acceptance.

## 2. Potential, ordering, and operator definitions

The displayed potential is valid without hidden parameter dependence. For r² ≤ 64 its second bump term vanishes and its first is positive, so V = 1. For r² ≥ 81 the numerator vanishes and the denominator remains positive, so V = 0. In the intervening annulus both denominator terms are positive. The two bump arguments cannot both be nonpositive. Standard flatness of exp(−1/s) at s = 0 makes the quotient smooth across the two radii. It is radial, even, nonnegative, and compactly supported.

For the fixed ball Λ = B(0,4), every difference of two points of Λ lies in B(0,8). Consequently the density-density interaction is exactly the multiplication operator L_n², including the i = j contribution V(0)L_n. Removing the diagonal terms gives L_n(L_n−1). There is no unaccounted factor 1/2 in the source's ordered double integral. A convention with an additional coupling or a factor 1/2 would require the corresponding time rescaling, but that convention is not used in the accepted theorem.

Each T_n is the self-adjoint whole-space Laplacian restricted to the antisymmetric sector. The bounded real symmetric multiplication perturbations preserve antisymmetry and yield self-adjoint H_n and K_n on D(T_n). Their bounds may depend on n; no uniform boundedness over Fock space is assumed. The self-adjoint direct sums use their maximal direct-sum domains. This supplies strongly continuous unitary groups and bounded Heisenberg conjugations. It does not presuppose CAR-algebra invariance.

For M_n = n−L_n, the polynomial identity is exact:

H_n−K_n = −M_n(2n−σ−M_n).

For n ≥ 1, σ ∈ {0,1}, and every spectral value m ∈ {0,…,n}, the second factor is between 0 and 2n. Functional calculus therefore gives the norm estimate by 2n‖M_nΦ‖. The vacuum is treated separately and causes no exception.

## 3. Uniform packing and the free-leakage estimate

The concrete f has support of radius 1/3, strictly inside its stated test-function ball. The cube Q lies near 2e₁, disjoint from that support and strictly inside B(0,3). The concrete product bump for the packed orbital has compact support inside (0,1)³. Its scaled translates lie strictly inside distinct subdivision cells, so normalization and pairwise orthogonality are exact. Choosing the first N cells makes the states unambiguous even when N is not a perfect cube.

With m_N = ceil(N^(1/3)) and ℓ_N = 1/(2m_N), the exact gradient sum is 4Nm_N²‖∇φ‖². The elementary bound m_N ≤ 2N^(1/3) gives a single constant times N^(5/3). Adding f adds a fixed kinetic energy and preserves a uniform bound in the actual particle number N+1. No lower-energy claim beyond this upper bound is needed.

One fixed smooth cutoff χ can equal one on B(0,3) and vanish outside a compact subset of Λ. Its derivative constants do not depend on N. The commutator formula for h = −Δ contains only the first derivatives of the evolving orbital and the fixed first and second derivatives of χ. Differentiating the unitary product on H² gives precisely the sign in equation (4). Although the initial H² norms increase, the bound uses only H¹ norms. Free evolution preserves both spaces and is isometric on H¹.

Because χg = g and 1_(Λ complement)χ = 0, the commutator estimate bounds the outside L² norm by C|s|‖g‖_(H¹). Squaring and summing over the freely evolved orthonormal orbitals gives λ_n(s) ≤ Cs²n^(5/3), uniformly for both initial-state families. The sharp indicator is never differentiated. Finite propagation speed is not assumed.

## 4. Slater second moments and sectorwise Duhamel

The second-moment identity is correct. For the occupied projection P and the outside projection q, expansion of the two-particle Slater marginal yields

‖dΓ(q)Φ‖² = λ² + λ − Tr(PqPq), with λ = Tr(Pq).

The traces are finite rank. Positivity of the compression PqP and the identity q² = q imply 0 ≤ Var(dΓ(q)) ≤ λ. Thus the leaked-number norm is bounded by √λ + λ. A probability estimate alone would not suffice. The proof applies this identity to reference/free Slaters only; it never applies it to the interacting evolution.

H_n−K_n is bounded on each fixed sector, so the strong Duhamel formula is valid on all vectors. On the smooth initial Slaters, the alternative common-domain differentiation is also justified: the free/reference group preserves D(T_n), and H_n has that same domain. No false domain-preservation claim for multiplication by the sharp indicator is needed.

Integrating 2n times the leaked-number estimate gives the stated powers n^(11/6)t² and n^(8/3)t³. At t = π/(2N+1−σ), the estimates for n = N and n = N+1 both tend to zero, with rates N^(−1/6) and N^(−1/3). Constants can absorb the fixed ratio (N+1)/N. The method's dimension threshold is correctly stated: its general exponents are −1/2+1/d and −1+2/d, negative when d > 2. No decay conclusion in d = 1 or 2 follows from this estimate.

## 5. Matrix element, both evolved states, and adjoints

The choice Ξ_N = a*(f)Ψ_N is normalized because f is orthogonal to every occupied initial orbital. Moving the Heisenberg unitaries to the two vectors produces evolutions of Ξ_N and Ψ_N separately. Replacing both by the reference evolutions costs at most E_(N+1)+E_N. Retaining only one of those errors would generally be invalid; the independent controls include explicit finite-dimensional counterexamples to that omission.

With inner products linear in the second variable, the reference scalar phase is exp(it(2N+1−σ)). Free covariance gives a*(exp(ith)f). The CAR contraction is valid because a(f)Ψ_N = 0. It does not require exp(ith)f to remain orthogonal to the occupied orbitals. Hence the reference matrix element is exactly

exp(it(2N+1−σ)) ⟨f, exp(ith)f⟩.

Both the sign of the free evolution and the sector-energy difference are correct. The prescribed times make the scalar factor −1. The remaining one-particle inner product tends to 1 for the one fixed f. The interacting matrix element therefore tends to −1, while its initial value is 1.

The norm upper bound is 2 because ‖a*(f)‖ = 1 and conjugation is isometric. The matrix-element lower bound tends to 2. Taking adjoints gives the annihilation norm, and taking the conjugate matrix element gives the stronger stated lower bound on D_NΞ_N itself. Thus the specific pure states ω_N satisfy ω_N(D_N*D_N) → 4. These are legitimate varying fixed-particle-number states; no superposition of different particle-number sectors is needed.

## 6. Topology and scope controls

The theorem concerns failure of pointwise operator-norm continuity of one fixed observable at zero. It does not assert uniform discontinuity over a moving family of observables. Λ, V, f, and each Hamiltonian convention remain fixed; only N, the witnessing states, and the time vary.

The separate fixed-vector estimate in the proof is valid and establishes strong-operator continuity for every bounded observable under any self-adjoint H. Accordingly, there is no contradiction with Stone's theorem. The result also makes no claim of CAR non-invariance, fixed-density thermodynamic behavior, or a counterexample in dimensions one and two. These limitations do not weaken the existential bounded-region answer accepted here.

## 7. Reproducible controls and their limits

`independent_checks.py` was authored independently and run against the frozen proof. It passes 5,659 controls, including:

- exact polynomial and phase identities over many sectors, including non-cubic packing sizes;
- direct occupation-basis CAR matrices;
- 36 random finite-dimensional Slater moment calculations;
- reference matrix elements at generic times that expose phase-sign errors hidden at a π phase;
- independent numerical unitary Duhamel bounds, both-vector comparison, and the annihilation adjoint witness;
- a direct commutator-Duhamel sign calculation;
- seven rejection fixtures for invalid sign, phase, variance, ordering, dimension, or omitted-bra modifications.

The maximum measured Duhamel error/integral ratio is approximately 0.999961; numerically zero denominators are excluded from that diagnostic. All checks use documented numerical tolerances where relevant. These finite-dimensional checks corroborate identities; the analytic arguments above establish the infinite-dimensional and limiting assertions.

The author verifier was inspected and replayed successfully, including its three local source-PDF size/hash checks. Three additional changed-proof fixtures were rejected by the frozen-byte guard. Those three fixtures test integrity only, not semantic correctness. The original proof and author manifest still match their frozen hashes after all checks.

To replay the independent controls, run:

`python independent_checks.py --proof PATH_TO_FROZEN_BOUNDED_REGION_PROOF.md`

The packet contains the full control results, a concise summary, author replay, integrity rejection records, and a machine-readable acceptance. No correction patch is supplied because no correction is necessary.
