# Independent acceptance: exact overlap refinement and asymmetric relaxation

Date: 12 October 2026 UTC.

## Verdict and accepted scope

**ACCEPTED as a substantive partial result and an exact optimization of the explicitly listed continuous relaxation. No substantive correction is required.**

The accepted input is the author's original asymmetric proof identified in `INPUT_PINS.json` with 15,960 bytes and SHA-256 `6881b190414305d49c7f189e240fb2aaeca7d0af7e1f06f1d973329434e25c5c`, as pinned by author freeze SHA-256 `8a04b28cba0ba896772aca7f39e53d6e0c5bc0a08ec478b902f993aa5e1c2b20`. The complete proof was read, the controlling weighted proof was inspected, and all eight author-freeze entries and five provenance pins were verified against bytes on disk.

Accepted conclusions are:

1. The exact occupied-positive-difference identity and capacity inequality, including midpoint and complementary-pair cases.
2. The finite window inequality retaining window variance, core–unpaired overlap, and the complementary-pair correction.
3. The necessary colored difference and sum convolution dominations; the resulting absolute continuity, L² bounds, overlap penalty, and equality structure.
4. At fixed core mass K in [0,√2], the exact maximum total mass of the stated length-one continuous relaxation with symmetric core is 1+(1−1/√2)K.
5. After imposing every stated centered core-mass bound with parameter κ in [0,√2], its exact maximum is 1+(1−1/√2)κ.
6. In the additional uniform/proportional-profile subclasses, the bound √(1+κ²/2), and its attainment by the displayed uniform continuous model.
7. The conditional finite transfer from a hypothetical symmetric-core theorem, with κ=2/√3 yielding 1+(2−√2)/√3=1.338203957451… .

This acceptance does **not** establish the symmetric-core target theorem, any unrestricted leading constant below √2, the full 2/√3 conjecture, any integer realization of either continuous model, any integer counterexample, or novelty/current literature status. No publication or repository mutation was performed.

## 1. Finite reflection and occupied-difference audit

If distinct positive-difference pairs (a,b) and (c,e) have the same difference, a+e=c+b. Their two unordered sum pairs are different: equality would either identify the original difference pairs or force a=b. Therefore both sums equal the unique exceptional sum T. This forces (c,e)=(T−b,T−a), puts every endpoint in C, and rules out a third distinct representation.

Reflection acts on the positive-difference pairs within C. A pair is fixed exactly when its endpoints sum to T. At a given difference there is at most one such fixed pair; if present, no second pair can occur. Hence r_C(d) is 0, 1, or 2, with the value 1 exactly at the occupied fixed-pair sites. Thus c(d)=(r_C(d)+p(d))/2 is precisely the occupied-site indicator. Any mixed or U-only collision would have to be a doubled reflected core difference, which is impossible if one endpoint lies in U. This proves (1), the identity in (2), and its sharpened right side 1−p(d)/2.

The argument covers a core midpoint T/2. It neither discards that midpoint nor treats a fixed complementary pair as a doubled difference. If no sum repeats, the declared C=∅ convention reduces every statement to its Sidon case.

## 2. Window coefficients, variance, and the conditional constant

The integer support interval has exactly L+h points, including both endpoints. Each source point contributes to h windows. The diagonal square term is h(u+k/2)=hQ. A positive difference d<h contributes twice its triangular weight h−d. Inserting the capacity bound gives hQ+h(h−1)−P_h, with coefficient −1, not −1/2, on P_h.

The pointwise identity is

F_A²−F_C²/2 = F_U²+F_C²/2+2F_CF_U
             = F_w²+(2−√2)F_CF_U.

Subtracting the constant mean hW/(L+h) gives the exact variance identity used in (3). Its variance, overlap, and complementary-pair terms are nonnegative. Dropping only variance and P_h gives precisely (4), including its factor (L+h)/h². All finite h≥1 are covered by this proof; h=1 and singleton sets are included. The empty set requires no diameter definition.

For the conditional asymptotic implication, the difference multiplicity bound gives m=O(√N), hence Q=O(√N). Taking h of order N^(3/4) in the weighted inequality yields W≤√N+O(N^(1/4)). Inserting k≤κ√N+o(√N) into m=W+(1−1/√2)k proves (C). This finite deduction does not depend on a continuum realization or on the core's location. The numerical specialization in the author proof is correct and exceeds 2/√3.

## 3. Weak limits and the L² step

The total masses of both empirical measures are uniformly bounded, with support in the fixed compact interval I. Their product measures, and hence their sum and difference convolution measures, converge weakly along a common subsequence. For nonzero lattice difference d/N the coefficient is exactly (r_A(|d|)−r_C(|d|)/2)/N≤1/N. The atom at zero has mass Q/N=o(1). Testing against continuous nonnegative functions and using the lattice Riemann sums proves (D) on the real line.

For (S), half the ordered count agrees with the off-diagonal unordered count. Its diagonal discrepancy has mass m/(2N)=o(1). The exceptional sum contains at most floor(m/2)+1 unordered representations, so its entire scaled contribution also vanishes. No exceptional atom of positive limiting mass was omitted.

Here is the functional-analytic justification for the concise mollification passage. Let ρ_ε be a nonnegative normalized symmetric interval indicator and q_ε=ρ_ε*ρ_ε. Then

‖γ*ρ_ε‖²₂ = (γ*tilde(γ)*q_ε)(0) ≤ 2,
‖υ*ρ_ε‖²₂ = (υ*tilde(υ)*q_ε)(0) ≤ 1.

These follow directly by integrating the nonnegative kernel q_ε against the dominated autocorrelation measures. Weak L² compactness and distributional approximate-identity convergence identify the original measures with nonnegative densities g,v in L². This is a valid way to deduce absolute continuity; it does not assume density existence in advance.

Convolving the full (D) with q_ε and evaluating at zero gives

(1/2)‖g*ρ_ε‖²₂ + 2⟨g*ρ_ε,v*ρ_ε⟩ + ‖v*ρ_ε‖²₂ ≤ 1.

Strong L² approximate-identity convergence, with Cauchy–Schwarz for the cross term, gives (5). Thus no unjustified pointwise evaluation of an unsmoothed weak limit is used. Expanding the variance of g/√2+v on the interval of length one gives (6). Equality in W≤1 forces both nonnegative losses to vanish, producing exactly the measurable segregation form (7).

The general core center in Section 3 is correctly retained. Section 5 is read within Section 4's zero-centered symmetric-core relaxation; for an actual off-center core, its centered truncations are centered at its own reflection center. The claimed conditional global estimate does not require center zero.

## 4. Continuous maximizers and all centered truncations

For the endpoint set E_s and central complement, the pairwise overlap splits into core–core, central–central, and mixed pairs. Their (D) weights are respectively 1, 1, and √2 per unit overlap. This gives H_s(t)=(1−t)_++(√2−1)z_s(t) for t≥0, with the correct cross-term coefficient.

A mismatched pair crosses at least one of the two interior boundaries. Each boundary contributes a set of starting points of length at most t, so z_s(t)≤2t. Consequently H_s(t)≤1−(3−2√2)t≤1 on [0,1]; outside the support it vanishes. The same proof covers s=0 and s=1, where some intervals degenerate.

Both component densities are even. Therefore the ordinary-sum convolution in (S) is no larger than the (D) convolution; their difference is g_s*v_s+(1/2)v_s*v_s≥0. The two profiles are segregated and have constant weighted density one on I, so W=1. Combined with the universal upper bound W≤1, this proves the fixed-K exact maximum without assuming an integer realization.

For K=κ and s=κ/√2, the centered truncation of length t has core mass √2 max(0,t−1+s). For t≥1−s, its comparison with κ√t reduces to

t−1+s−s√t = (√t−1)(√t+1−s)≤0.

The other range has zero core mass. This proves the whole continuum of constraints, including the endpoints. The full-interval constraint K≤κ and W≤1 give the matching upper bound. For actual centered core truncations, passage to these inequalities is justified at every fixed positive radius because the established L² limit has no boundary atoms; radius zero is immediate.

The term “exact maximum” is properly restricted to the displayed relaxation. The proof does not assert that this relaxation captures every microscopic necessary condition. The centered constraints concern subcores with the original core's reflection center; taking any smaller such symmetric subcore cannot increase its mass relative to the corresponding full centered truncation.

## 5. Additional profile hypotheses and residual limitations

If g is constant K, (5) is at least K²/2+2KU+U² by Cauchy–Schwarz for v. The same calculation applies when v is constant U. If g=Kp and v=Up with unit-mass p, the expression is (K²/2+2KU+U²)∫p², and ∫p²≥1. This proves M²−K²/2≤1 in the claimed subclasses only.

For the uniform model, write M=√(1+κ²/2) and v=M−κ. Nonnegativity follows from κ≤√2. The difference coefficient is M²−κ²/2=1, and the sum coefficient is M²/2≤1. Its truncated core mass is κt≤κ√t. The uniform subclass maximum is therefore attained in its relaxation. At κ=2/√3 its value √(5/3)=1.290994448736… remains above the target.

The discussion of discrete residuals is careful. Neither disjoint lattice occupancies nor U∩(T−U)=∅ is passed through weak convergence as a disjoint-support statement. The example's symmetric unpaired weak density is explicitly not treated as a second finite reflected core. Exact sitewise product exclusions are retained only as finite facts. The suggested need for further microscopic information is a limitation statement, not a proved new incompatibility.

## 6. Independent diagnostic record

The independent verifier was written before inspecting the author's verifier. It imports no author code and evaluates window counts directly from the input subsets. Exact comparisons in Q(√2) are reduced to rational square comparisons; executable checks use explicit failures rather than Python assertions, so they remain active under optimization.

All three independent runs, normal, `-O`, and `-OO`, passed with identical mathematical output:

- Every subset of {1,…,N}, for each 1≤N≤17: 262,142 inputs, including 22,447 admissible sets.
- 384,102 window cases, with every h=1,…,N+2 on every nonempty admissible set.
- 339,242 positive-difference cells.
- 7,328 admissible midpoint cases, 11,292 cases with both colors nonempty, and 20,721 self-reflected difference occurrences.
- 16,705 exact-rational colored-convolution cases on s=i/64 and t=j/64, including negative shifts and shifts beyond the support.
- 4,225 centered-truncation cases and 65 uniform-profile parameter checks.

The independently enumerated per-N admissible counts agree with the author's counts throughout their N≤16 range. The author's three diagnostic files report 131,070 inputs, 15,057 admissible sets, and 243,711 windows; their hashes were checked, and their verifier was inspected after the independent implementation was complete. The author runs were not rerun by this auditor; the independent runs are the executed verification basis.

The rational grids are diagnostics, not proofs of all real parameters. The analytic arguments above establish the full continuous statements. Finite enumeration is likewise supplemental to the finite symbolic proof.

## Final disposition

No blocking error or required mathematical correction was found. The packet is suitable to retain as a verified partial advance with the limitations stated above. The unrestricted problem remains unresolved by this packet.

## Public edition notice

The preceding text is the complete accepted historical proof or audit, with only the locator edits recorded in [EDITION_MAP.md](EDITION_MAP.md). Statements about accompanying diagnostic programs, original input records, or the absence of publication describe the original research or review stage. This prose-only edition distributes no executable program, detailed diagnostic collection, source PDF or image, or private record. Original and accepted file identities are recorded in [INPUT_PINS.json](INPUT_PINS.json); public-file identities are recorded in [MANIFEST.json](MANIFEST.json). [VERIFICATION.json](VERIFICATION.json) distinguishes exact finite checks, floating-point diagnostics, and integrity checks. This notice changes no mathematical argument, verdict, or hypothesis.
