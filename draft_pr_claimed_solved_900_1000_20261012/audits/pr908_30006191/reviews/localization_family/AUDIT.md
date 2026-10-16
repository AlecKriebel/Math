# Adversarial audit: continuum/PDE localization family

Problem 30006191 / OWR-14299085-005; eligible saved candidate associated with draft PR 908. Audit date: 14 October 2026 UTC. Candidate head supplied by the coordinating audit: a35667b1bb0bafed69916709997a4684223ecc93. This family does not independently repeat the live PR gate or novelty assessment.

**Verdict: PASS for the mathematical localization/comparison mechanism and the resulting stated three-dimensional existential counterexample.** The universal analytic estimate is proved, not inferred from numerical samples. No mandatory repair was found. The candidate remains unchanged, and this verdict does not certify historical priority, current problem status, CAR-algebra invariance, or claims beyond its stated scope.

## Audited claim and success criteria

The exact target is the following: on fermionic Fock space over L²(R³), with kinetic energy dΓ(-Δ) on all of R³, fixed Λ=B(0,4), and a fixed smooth even nonnegative compactly supported plateau interaction V, define sectorwise H_n=T_n+L_n(L_n-σ), σ∈{0,1}. There is a fixed normalized f∈C_c∞(B(0,1/2)) and the supplied explicitly packed Slaters Ξ_N in sector N+1 such that, at t_N=π/(2N+1-σ),

\[
\|(e^{it_NH}a(f)e^{-it_NH}-a(f))\Xi_N\|\to2,
\qquad
\|e^{it_NH}a(f)e^{-it_NH}-a(f)\|\to2.
\]

Success requires: (i) the bounded-region Hamiltonian is actually the stated model; (ii) its sector and Fock direct-sum evolutions exist; (iii) all localization constants are independent of N and of the actual particle number n=N or N+1; (iv) a genuine second-moment estimate controls the leaked number; (v) the Duhamel comparison uses only a reference Slater and tends to zero; (vi) the neighboring-sector phase and CAR matrix element give a norm lower bound tending to the sharp upper bound 2; (vii) the topology and boundary cases are correctly qualified. Each requirement is met by the independent equations L1–L15.

## Independence and input identity

The primary proof was read first. Its mechanism was reconstructed and written in INDEPENDENT_DERIVATION.md before reading any older audit or candidate code. No old audit reports or candidate verification code were subsequently read or run: they were not needed for this family's conclusion. The independent controls here were authored for this audit.

Observed candidate SHA-256: 2b7c22cfc54049a9e51fe5eb4eb283ba911e6f27e8b6e4dc9557927bc04d7350. Observed original PACKAGE_MANIFEST.json SHA-256: 828280cc131c38e1f651b48b655dff177f880ba3505bba54e049510d81827795. Both match the supplied immutable identities. The proof is 12,771 bytes. Final rechecks are recorded in RESULT.json. No candidate file was edited.

Read the private source record for statement identification, then directly consulted printed pages 364, 365, and 371 of the [official Oberwolfach Report 7/2025](https://ems.press/content/serial-article-files/51350). Page 371 displays kinetic energy on R^d and interaction variables in Λ×Λ. Page 364 identifies bounded Λ in the regularized discussion. Page 365 explicitly distinguishes strong-operator continuity from the norm continuity meant for a C*-dynamical system. These checks support the model/topology reading used here. The private source record's dated literature assessment is not used as evidence that the problem remains open today. No raw third-party source is included in this public audit package.

## Mechanism reconstructed independently

The potential has a plateau on every possible displacement of two points in Λ. Thus the interaction counts particles inside Λ exactly: L² or L(L-1), depending on diagonal convention. It does not confine the kinetic energy. The constant-number reference K_n=T_n+n(n-σ) has a simple scalar phase while retaining free kinetic evolution.

Packing N orthogonal compactly supported orbitals into a fixed cube costs kinetic energy O(N^(5/3)). A fixed smooth cutoff commutator controls each freely evolved orbital's exterior norm by C|s| times its H¹ norm. Squaring and summing yields mean exterior particle number λ_n(s)≤C s²n^(5/3). On a Slater, the exact exchange correction gives variance at most λ, so ||M_nΦ_n(s)||≤sqrt(λ)+λ. This is substantially stronger than a generic estimate based only on the mean.

The exact Hamiltonian difference is -M_n(2n-σ-M_n). Duhamel places that difference on the freely evolved reference state and yields

\[
E_n(t)\le\beta n^{11/6}|t|²+\tfrac23\beta²n^{8/3}|t|³.
\]

With t=O(N^(-1)), n=N or N+1, the two terms are O(N^(-1/6)) and O(N^(-1/3)). Replacing both neighboring-sector evolved vectors separately then transfers the reference's scalar phase -1 to the true matrix element. The fixed one-particle f has a strongly continuous free orbit. The resulting annihilation norm approaches 2.

## Domain, indicator, and direct-sum attack

**Attack:** the sharp spatial indicator might invalidate differentiation, introduce a boundary distribution, or prevent self-adjointness on the kinetic domain.

**Resolution:** on a fixed sector W_n=L_n(L_n-σ) is a bounded real multiplication operator, permutation invariant, with norm at most n². It does not need to preserve H². Adding it to T_n gives a self-adjoint operator on D(T_n). For completeness, for Im z large enough, (1+W_n(T_n-z)^(-1)) is invertible by a Neumann series. Both half-plane resolvents exist; together with symmetry this verifies self-adjointness. The antisymmetric subspace is reducing for both operators.

The proof never differentiates p=1_Λ or q=1_{Λ^c}. It differentiates the fixed smooth χ with compact support strictly inside Λ. On the commutator path, free evolution preserves H² and χ maps H² into H²; strong differentiation is therefore legitimate. The estimate then depends only on the H¹ norm. Large N-dependent H² norms have not entered the error bound.

Direct sums use maximal sector domains and the direct sum of the sector resolvents. Their resolvent norms are bounded uniformly by |Im z|^(-1); hence the Fock direct sum is self-adjoint. No unsupported assertion about equality of global algebraic-sum domains is needed. Finite Slaters lie in individual sector domains and suffice for all differentiated paths.

**Outcome:** attack rejected. No domain or boundary-distribution gap.

## Fixed constants and grid-boundary attack

**Attack:** increasing orbital frequency could hide an N-dependent cutoff constant, or ceil(N^(1/3)) could fail on perfect cubes or the first N.

**Resolution:** the fixed cutoff can be chosen explicitly with plateau radius 3 and support radius 7/2. Its derivative suprema are finite numbers determined before N is chosen. With B=1+16||∇φ||²+||∇f||² and β=Cχ√B, all analytic constants are explicit in terms of fixed functions. The only N dependence is in stated powers.

At every N≥1, m³≥N and m≤2N^(1/3). The orbitals are supported strictly within the scaled cubes; adjacent faces create neither overlap nor derivative jumps. The cube Q lies inside B(0,3), while f lies inside B(0,1/2) and is disjoint from Q. Normalization and orthogonality follow by change of variables and exact disjoint supports. The exact integer controls include values immediately below, at, and above perfect cubes, as well as N=1.

**Outcome:** attack rejected. Uniform constants and every integer grid boundary are covered analytically.

## Slater second moment and state-admissibility attack

**Attack:** mean leakage could be small while rare leakage of many particles makes ||MΦ|| large. Alternatively, the interacting state could lose the Slater property.

**Resolution:** both attacks would be valid objections to a mean-only proof. Here the exact Slater formula is supplied and independently derived:

\[
\langle M²\rangle=\lambda²+\lambda-\operatorname{Tr}(PqPq),
\qquad
\operatorname{Var}(M)=\sum_j\nu_j(1-\nu_j)\le\lambda,
\]

where ν_j are eigenvalues of PqP on the occupied space. The operator is a positive contraction and P has finite rank, so all traces are valid. The minus exchange sign is correct. Even when free propagation destroys spatial disjointness, it preserves orthonormality and the Slater structure. Disjoint supports are used only at initialization.

The Duhamel integrand uses e^(-isK_n)Φ_n, a scalar multiple of the freely evolved Slater. There is no claim that e^(-isH_n)Φ_n remains Slater, and no variance estimate is applied to a mixed state formed by adding a particle to an interacting state. Both Ψ_N and Ξ_N are normalized fermionic vectors, and a(f)Ψ_N=0 exactly.

The exact finite-dimensional controls compute occupation moments by enumerating exterior coefficients of rational orthonormal orbitals, independently of the trace formula. Eight particle numbers, including vacuum and fully filled finite mode space, match the formula exactly. These controls support the algebraic identity; the continuum estimate is established by its analytic derivation.

**Outcome:** attack rejected. Actual second moments, rather than leakage probabilities alone, control the comparison.

## Comparison, sign, and phase attack

**Attack:** a Duhamel sign or orientation could put the interacting state into the leakage estimate, or the scalar phase could have the wrong sign.

**Resolution:** strong differentiation of exp(-i(t-s)H_n)exp(-isK_n) gives the bounded perturbation integrand on the K-evolved vector. Its sign is irrelevant after taking norms, but its state placement is essential and correct. The cutoff identity has sign -i because differentiating U(s-r)χU(r) gives +iU(s-r)[h,χ]U(r); subtracting endpoint values reverses the order. Negative times give the same |t| estimate through oriented integration.

For the matrix element, moving the left unitary to its vector gives e^(-itH_{N+1})Ξ_N, so E_{N+1}(t) and E_N(t) are exactly the appropriate errors. The scalar phase has sign +it(c_{N+1}-c_N), with difference 2N+1-σ. At the chosen positive or negative t_N this phase is -1. Free covariance uses e^(ith)f for the stated Heisenberg sign convention. The CAR reduction needs only the initial orthogonality a(f)Ψ_N=0; evolved-f orthogonality is not assumed.

Adjunction gives <Ψ_N,D_NΞ_N>=conjugate(F_H(t_N)-1). Consequently

\[
2\ge\|D_N\|\ge\|D_N\Xi_N\|
\ge2-2C_1N^{-1/6}-2C_2N^{-1/3}-\|hf\|\pi/(2N),
\]

with C_1 and C_2 explicitly fixed in L12. This is a complete quantitative bridge from the localization estimate to every norm assertion of the theorem.

**Outcome:** attack rejected. Sign, orientation, state placement, and the sharp upper/lower norm bridge are consistent.

## Boundary and limiting cases

| Case | Verified behavior and scope |
|---|---|
| n=0 vacuum | H_0=K_0=0; no leakage; self-adjoint direct-sum definition includes vacuum. |
| N=0 time formula | Excluded: theorem starts at N≥1; σ=1 denominator would otherwise be zero. |
| N=1 | m=1, one packed smooth orbital; both t formulas are finite; the estimates hold although their coarse lower bound need not be positive. |
| n=1, σ=1 | L(L-1)=0 and n(n-1)=0, so R_1=0 exactly; the general bound remains valid. |
| n=1, σ=0 | R_1=-q; no anomalous spectral factor. |
| M=0 or M=n | Factorization and bound are valid at both extreme leakage values. |
| Boundary of B(0,4) | The boundary is Lebesgue null; either indicator convention on it represents the same L² multiplication operator. |
| Packed cube faces | Orbital supports remain compactly inside subcubes, so faces do not create overlap or discontinuities. |
| |x|=8 or 9 in V | V has smooth plateau/zero endpoints; denominator never vanishes. |
| t=0 | All comparison errors vanish, F_H(0)=1, and D(0)=0. |
| Negative t | Commutator and comparison estimates depend on |t|; -t_N also gives phase -1. |
| Large |t| | The bound remains valid but may be very coarse; only t_N→0 is used. |
| Fixed N continuity | For a creation block from n to n+1, the difference from the free block is ≤|t|(||W_n||+||W_{n+1}||); the free block difference is ≤||e^(ith)f-f||. It tends to zero. |
| Fixed Fock vector | Strong-operator continuity follows from unitary strong continuity and boundedness of a(f). |
| N→∞ | Uniform constants and t_N≈1/N yield the two negative exponents; the witness vector changes sector. |
| d=1 or 2 | This estimate gives nondecaying powers; no claim in these dimensions is certified. |

## Rejected alternative estimates and exact gaps

This audit attempted two weaker controls as falsification probes. Neither suffices, and neither is substituted into the proof:

1. Global operator-norm Duhamel uses ||H_n-K_n||=O(n²), giving O(n²t), which does not vanish at t≈1/N.
2. Generic number control uses M²≤nM and λ≤Cs²n^(5/3), giving ||MΦ||≤C|s|n^(4/3), then error O(n^(7/3)t²)=O(N^(1/3)).

These routes are blocked because they discard the supplied Slater exchange information; there is no missing estimate to borrow from them. The actual route closes the central difficulty with L9–L11. No route is labeled successful by transferring the difficulty to an unsupported leakage-number or domain assumption.

This audit found no mathematical gap in the stated theorem. Its remaining limitations are substantive scope restrictions: one existential smooth plateau potential and bounded ball; d=3; unconstrained high-density finite-particle test states; pointwise operator-norm discontinuity; no statement of failure for every V/Λ, fixed-density thermodynamic states, CAR invariance/non-invariance, or physical experiment. Historical novelty and current eligibility are handled separately by the coordinating audit.

## Model assumptions and units

The model is a nonrelativistic mathematical quantum Hamiltonian. It fixes h=-Δ with ℏ=1 and absorbed kinetic coefficient, interaction coefficient one, and dimensionless chosen radii. Including a different pair-counting coefficient would require the corresponding explicit scalar-phase/time normalization; the audited candidate defines its coefficient consistently through L(L-σ). The smooth χ is a proof device, not UV smearing of fields and not a modification of H.

No finite-speed propagation assumption is used. Schrödinger evolution has immediate tails; the norm of those tails is controlled on short times using H¹. No empirical or numerical assumption underlies the theorem. The finite controls check exact algebra and bookkeeping; they neither simulate the interacting continuum system nor establish the infinite-N limit.

## Reproducibility and required repairs

Read INDEPENDENT_DERIVATION.md for every analytic equation and explicit error constants. Running `python3 check_controls.py` from this directory regenerates CONTROL_RESULTS.json using only the Python standard library and exact rational arithmetic. It checks 8 Slater cases, 22,952 sector identities, 20,000 neighboring-sector phase identities, 15 integer-grid boundary cases, and dimension exponents. All pass.

Required mathematical repairs: **none**. Optional exposition improvements are already supplied in this independent supplement: an explicit χ, the global direct-sum domain, signed-time estimates, exact fixed constants, and the quantitative lower bound L15. They clarify existing arguments and do not alter the candidate or consume a new proof-search turn.

The accompanying RESULT.json records the exact strongest verified claim, assumptions, boundaries, evidence, limitations, and PASS verdict. MANIFEST.json lists only intentionally public audit files and their hashes/byte counts; it excludes itself, temporary files, private material, and raw third-party sources. No external outreach, PR/sheet mutation, branch change, commit, push, or release was performed by this family.
