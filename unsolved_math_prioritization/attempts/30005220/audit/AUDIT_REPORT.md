# Independent adversarial audit

**Problem:** Sylow Restrictions and Character Fields of Values; 30005220 / OWR-11101920-004; rank 485.  
**Audit date:** 3 October 2026.  
**Verdict:** **PASS — partial research packet only.**  
**Original problem:** **UNSOLVED, five attempts completed.**  
**Full-resolution promotion:** **HOLD.** No proof of the original conjecture, and no counterexample satisfying its hypotheses, appears in the packet.

## 1. Scope, independence, and preservation

The audit examined every mathematical claim in the five frozen attempt notes, the public summary and source gate, and the supplied verifier. It independently reconstructed the key arguments, checked primary sources, replayed the supplied verifier in a separate directory, and wrote a separate exact-arithmetic checker.

All ten files listed in the freeze manifest have the expected byte counts and SHA-256 digests, both before and after the checks. The external freeze manifest agrees byte-for-byte with the release manifest. The frozen release was not edited. All audit writes are confined to this audit directory. No remote state was changed. No publisher PDF, complete source text, access record, or private research-history file is included here.

The verdict certifies the packet's explicitly bounded claims. It is not a certification of a general solution, novelty, or an exhaustive literature search.

## 2. Exact problem and primary-source gate

Write Q_n = Q(ζ_n). The question requires a finite group G, a prime p, a Sylow p-subgroup P, and an **irreducible** ordinary character χ with **p not dividing χ(1)**. If its least cyclotomic conductor is c(χ) = p^a m with p not dividing m, the proposed conclusion is

    p does not divide [Q_(p^a) : Q(χ_P)].

This is the statement on printed p.2276, Conjecture A, of Navarro's contribution to OWR 39/2022. Both the publisher PDF and the rendered mathematical page were inspected. The correct publisher file is [46976](https://ems.press/content/serial-article-files/46976). File [46974](https://ems.press/content/serial-article-files/46974) is instead OWR 32/2022, an algebraic-geometry report. The [publisher record](https://ems.press/journals/owr/articles/11101920) matches the report number, DOI, pagination, and publication date. The catalogue landing page was again inaccessible, so its live contents were not independently verified.

The earlier statement is Conjecture C in [Navarro–Tiep, Forum of Mathematics, Pi 9 (2021), e2](https://doi.org/10.1017/fmp.2021.1). Its Lemmas 7.1–7.2 establish the inclusion and odd-prime reformulation, while Theorem 7.3 covers normal Sylow subgroups. The nearby theorem about global fields of odd-degree characters must not be substituted for the Sylow-restriction conjecture.

Existing-result attribution is correct:

- [Isaacs–Navarro, Journal of Algebra 653 (2024), 42–53](https://www.sciencedirect.com/science/article/pii/S0021869324002345) proves the p-solvable case. The original report already announces it.
- [Hung–Schaeffer Fry, Nagoya Mathematical Journal 261 (2026), e7](https://www.cambridge.org/core/journals/nagoya-mathematical-journal/article/prationality-of-heightzero-characters/87ECC6D075A7DFA1AE0835729B72DD14), Theorem D, covers prime degree different from p; levels at most one are automatic for the original index question. Lemmas 4.2–4.3 and Theorem 4.4 supply the stated induction background. The normalizer/height-zero conjecture is a separate statement.
- [Hung's May 2026 survey](https://arxiv.org/abs/2512.18042v3), Conjecture 5.2 and Question 5.3, continues to distinguish the original field assertion from the stronger modular-level assertion.
- [Linckelmann, arXiv:2604.01351v1](https://arxiv.org/abs/2604.01351v1), Theorem 1.1 and Corollary 1.2, detect the conductor through individual generalized decomposition coordinates, not through their degree-weighted scalar sums.

### New source found during this audit

[Hung, *On the p-rationality of Deligne–Lusztig characters*, arXiv:2608.17871v1, 18 August 2026](https://arxiv.org/html/2608.17871v1), §4.2 and Theorem 4.5, still treats the Navarro–Tiep assertion as a conjecture and gives an additional defining-characteristic finite-reductive-group case. This source postdates the packet's inspected survey. It supports keeping the general problem unresolved. Its omission is nonblocking because the frozen packet explicitly disclaims an exhaustive literature search. Its displayed root subscripts should not be copied as a replacement for the precise original statement; the audit anchors the formulation in the original source.

## 3. Field and conductor distinctions

The preliminary inclusion is valid. Values on a p-group lie in a p-power cyclotomic field; intersecting with Q_(p^a m) puts E = Q(χ_P) inside Q_(p^a). Thus the displayed extension index is defined.

The cases a = 0 and a = 1 cause no problem for the index statement. At p = 2, a minimal conductor never has 2-adic valuation one, since Q_(2m) = Q_m for odd m. A reformulation using Q_p E = Q_(p^a) needs its stated a ≥ 1 qualification: for odd p and a = 0, its left side already contains Q_p. The packet correctly avoids that degenerate reformulation.

For odd p and a ≥ 2, Gal(Q_(p^a)/Q) is cyclic and its unique order-p subgroup fixes Q_(p^(a−1)). Accordingly the target fails exactly when E lies in that smaller field. Preserving the top conductor level therefore suffices for odd p.

For p = 2, the whole ambient degree is a power of two, so the target requires E = Q_(2^a). Equality of conductor alone does not imply this. The Q(√2) example has conductor eight but degree two, whereas Q_8 has degree four. No odd-prime cyclic-Galois argument has been incorrectly extended to p = 2 in the packet.

## 4. Proof-by-proof adversarial findings

### Attempt 1: positive degree less than p — PASS

For any nonzero ordinary character Ψ with Ψ(1) < p, its restriction to P has only linear constituents, because all nonlinear irreducible degrees of a p-group are divisible by p. A p-subgroup of the Galois stabilizer permutes those constituents with constant positive multiplicities. Every nontrivial orbit would require degree at least p, so every constituent is fixed.

After factoring out the representation kernel, the image of P has exponent p^b. Since its representation is diagonal, one constituent has order p^b, and that constituent generates Q_(p^b). Thus the p-subgroup stabilizer is trivial. The conductor divides the finite-image exponent, giving a ≤ b. The field tower E ⊆ Q_(p^a) ⊆ Q_(p^b) transfers the prime-to-p index to the required field. This also covers b = 0 and the Q_2 = Q degeneracy. Neither irreducibility nor an unjustified cancellation assumption is used.

The restriction Ψ(1) < p is essential to this proof. A full orbit of p high-order constituents plus one fixed constituent is allowed at degree p+1.

### Attempt 2: normal Sylow and reductions — PASS

Clifford theory gives χ_P = e(λ_1 + ... + λ_t). The common irreducible degree is a power of p dividing χ(1), so all λ_i are linear; both e and t are prime to p. Conjugacy makes their orders equal. A p-group acting on the t constituents has a fixed point, which now necessarily has the same maximal order as every other constituent. This forces the stabilizer's p-part to vanish. The finite-image exponent argument used to pass to the global conductor remains valid.

The faithful-quotient reduction preserves both fields. The direct-product reduction is also sound: evaluation with one coordinate the identity recovers each factor field after division by a nonzero integer degree; the conductor of the compositum is the least common multiple of the factor conductors. A factor with maximal p-part then supplies the requisite index divisibility. These reductions do not reduce all cases to normal Sylow subgroups.

### Attempt 3: lifting and modular criterion — PASS

The lifting argument is valid, including at p = 2. To spell out its ambient field, choose N at least a and at least the p-exponent of P, and let r be restriction from Gal(Q_(p^N)/E) onto Gal(Q_(p^a)/E). For a Sylow p-subgroup S of the latter, r^−1(S) has a Sylow p-subgroup T mapping onto S. Indeed a surjective finite-group homomorphism maps Sylow subgroups onto Sylow subgroups; here the kernel is itself a p-group because a ≥ 2.

Every element of T fixes χ_P, so it permutes Irr(P) and preserves multiplicities. On the order-p^a linear constituents, every orbit not fixed by all of T has p-divisible size. If their total multiplicity s_a is nonzero modulo p, a T-fixed constituent exists. Its value field is Q_(p^a), forcing the image S to be trivial. This requires a group-fixed point, not merely a different fixed point for each element; the orbit argument supplies exactly that.

The sentence about extending the Galois group is therefore sound. Explicitly naming Q_(p^max(a,b)) would improve exposition but is not a missing mathematical hypothesis. What remains unproved is the application of this criterion to every irreducible p′-degree character: the top global conductor need not be detected by a nonzero s_a for an arbitrary ordinary character.

### Attempt 4: proper-subgroup and general-index Mackey congruences — PASS

For H < P, the possible linear extensions of a fixed linear character of H form either an empty set or a coset λ_0 A. Here A is dual to P/(HP′), even if H is not normal. The quotient exists because P′ is normal. It is nontrivial: HP′ = P would imply HΦ(P) = P, contradicting the Frattini property unless H = P.

Intersecting λ_0 A with the characters of order dividing p^j gives either zero extensions or a coset of A[p^j]. For j ≥ 1 its nonzero cardinality is divisible by p. Subtracting the counts at j = i and j = i−1 proves the exact-order congruence only for i ≥ 2. The excluded case i = 1 really fails, as induction of the trivial character from 1 to C_p gives p−1 order-p constituents.

In Mackey's formula for P ≤ K ≤ G, all proper-intersection terms vanish modulo p by that lemma. A P-fixed coset gK satisfies g^−1 P g ≤ K; Sylow conjugacy inside K gives a representative in N_G(P). Thus the surviving cosets are indexed by N_G(P)/N_K(P), and their restrictions are twists by automorphisms of P. This proves the coefficient [N_G(P):N_K(P)] for arbitrary p′ index. No primality-of-index assumption is needed. The coefficient is prime to p because both normalizers have P as a Sylow subgroup.

For χ = Ind_K^G λ, λ linear, p′ degree implies P can be conjugated into K. If λ_P has order p^b with b ≥ 2, the congruence gives s_b nonzero modulo p. If a < b, the p-group Gal(Q_(p^e)/Q_(p^max(a,1))) fixes χ_P and has no fixed order-p^b linear character, a contradiction. Conversely, induction places Q(χ) inside Q(λ), so a ≤ b. Hence a = b and Attempt 3 applies. The b ≤ 1 cases are automatic; no false equality between order and conductor at binary level one is used.

The conclusion for monomial irreducible p′-degree characters is correct even without assuming G is p-solvable. It does not cover primitive nonlinear characters or prove the needed conductor-to-modular-level assertion for arbitrary inducing characters. No novelty claim is warranted from this audit.

### Attempt 5: decomposition coordinates — PASS as an obstruction analysis

At a p-element u, generalized decomposition coordinates satisfy χ(u) = Σ_φ d^u_(χ,φ) φ(1). A maximal-conductor coordinate can disappear in this sum. The packet's explicit reducible family realizes that cancellation exactly. Linckelmann's theorem therefore does not provide the omitted noncancellation theorem by itself.

The stated conditional result for odd p is valid: if a conductor-detecting u has p-group centralizer, there is just one irreducible Brauer character, so the coordinate equals χ(u). Conjugating u into P does not change its value. Its conductor then forces the desired index by the odd-prime field criterion. The condition is genuinely additional, and the packet does not claim it always holds. The binary caveat remains necessary.

## 5. Reducible examples and hypothesis checks

For G = C_(p^2) × C_q with q > p prime, the displayed Ψ has p+1 distinct linear constituents. Its degree is p+1 and its norm is p+1, so it is ordinary, positive, and p′-degree, but **not irreducible**.

The product-coordinate Galois stabilizer is trivial: the unique nonprincipal constituent with trivial C_q component pins the p^2 component, and then the constituent with exponent j = 1 pins the q component. Hence the global field is Q_(p^2 q); that cyclotomic field has least conductor p^2 q also when p = 2, because then it is divisible by four.

On P the sum is 1 outside its subgroup of order p, and equals 1+pζ_p^t on x^(pt). Its restriction field is exactly Q_p, rational for p = 2. The index is p. At u = x the generalized decomposition coordinates have the asserted primitive p^2-root contributions but sum to 1. These facts invalidate proposed proofs using only positivity, degree prime to p, and conductor detection. They do **not** invalidate the original conjecture.

The binary character 1+λ+λ^−1 on C_8 is likewise reducible, with norm three. It is a correct warning about field generation, not an odd-degree irreducible counterexample.

## 6. Reproducible exact checks

The original verifier was copied into `replay/` and executed there. Its generated JSON is byte-identical to the frozen recorded output. It must not be executed in the frozen release directory because it writes its results beside itself.

`independent_checks.py` uses only the Python standard library and imports none of the release code. Its cyclic-field engine constructs Φ_n recursively and evaluates the character at every element in Z[X]/(Φ_n), then computes Galois invariance from those exact values. This checks the spectrum-based implementation through a different representation.

Results, recorded in `independent_results.json`:

- All **7,229** bounded cyclic-character instances pass. Per-plan counts are 8, 24, 54, 189, 1,080, 3,275, 1,325, and 1,274.
- All **748** proper cyclic induction congruences pass through a separate divisibility/compatibility count.
- The **five** reducible examples at p = 2, 3, 5, 7, 11 pass in direct product coordinates; exact cyclotomic arithmetic verifies every displayed restriction cancellation.
- The binary conductor-eight/index-two example passes.
- **Three additional composite-index Mackey controls** pass: S_5 × C_9 at indices 10 and 20, with normalizer coefficients 1 and 2; and S_5 × C_4 at index 15, with nonabelian D_8 Sylow factor. In the last case the linear multiplicities are 4, 1, 2, 2, giving s_2 = 9, congruent to the coefficient 1 modulo two. Thus the test is not merely equating total degree with linear multiplicity.
- **96 finite Galois-lifting controls** pass, including six using noncyclic binary Galois p-groups. These are supplementary sanity checks; the argument in §4 supplies the proof.
- All **ten frozen hashes** remain unchanged.

The composite-index controls are tests of the ordinary-character induction lemma; no irreducibility is asserted for their induced permutation characters. None of these finite computations searches all irreducible characters or proves the original conjecture.

## 7. Findings and release boundary

**Blocking mathematical defects in the stated partial claims:** none found.

**Nonblocking improvements:** make the ambient extension in Attempt 3 explicit; add the August 2026 primary-source status update in a future, separately versioned source gate. The present frozen files should remain unchanged.

**Unresolved gap:** for arbitrary irreducible χ of degree prime to p, establish survival of the top global p-conductor in the Sylow restriction; at p = 2, also establish full cyclotomic field generation. Showing that the highest nonzero-mod-p linear-constituent level equals the global level would suffice. The packet does not prove that assertion, and none of its examples violates irreducibility-preserving hypotheses.

**Permitted summary:** an independently checked, accurately attributed partial research record with correct special-case proofs, exact reducible obstructions to shortcuts, and an explicit unresolved step.

**Not permitted:** a complete solution, a disproof of the original conjecture, a first-result claim, or a claim that the finite controls exhaust arbitrary finite groups.

## 8. Running the audit controls

From this directory:

    python3 independent_checks.py --output independent_results.json
    python3 replay/verify_spectral_obstructions.py

The independent mathematical checks are portable. When copied away from the adjacent frozen packet, the script reports the hash-integrity check as skipped rather than pretending to have verified missing files. The mathematical controls still run. Source inspection is documented above and is not automated by this script.
