# Independent adversarial operator audit

Checkpoint: 2026-09-14T00:41:51Z (2026-09-13 local). Completion estimate: 100% of the assigned, bounded operator-proof review; this is not an estimate that all manuscript claims have been independently verified.

## Scope and verdict

I independently reconstructed the proofs in `main.tex` of the polar positive-factor identity, scalar extremum and equality set, sharp commuting-operator bound, canonical attainment, equal supported multiplicities, and reflection-product rank bound. I did not consult earlier audit verdicts. I also inspected relevant source files in `qubit_povm_pvm_minimum_settings/bell_lean` to assess actual reuse.

**No mathematical blocker found in this scope.** The upper bound is genuinely valid for arbitrary Hilbert spaces with commuting party algebras. The stronger multiplicity conclusion is proved only in the stated finite-dimensional tensor-product setting. The latter restriction is real and correctly maintained. This is a human-readable mathematical review, not a Lean verification or a guarantee of the paper's entire correctness or novelty.

## Reconstructed proof checks

### Polar identity and commuting-model upper bound

For the canonical polar factorization `C = V |C|`, set `H = |C|^(1/2)` and `J = |C*|^(1/2)`. The identities `JV = VH`, `V*V H = H`, and cross-party commutation give, for `P = J − VHB`,

`P*P = |C*| + |C| − CB − B*C*`.

This checks all cross terms and the normalization of the claimed half-gap. The canonical partial isometry is sufficient; a unitary extension is unnecessary. The claim remains valid when `C` has a kernel. The strong-limit formula `C(|C| + εI)^−1 → V` is justified by the bounded spectral functions `t/(t+ε)`, and it places `V` in Alice's von Neumann algebra. Hence the commutation needed in the expansion is available even if the original algebra is not norm or strongly closed.

With `U=A0* A1`, normality of `I+ω^y U` gives the two absolute values in the manuscript. Summing the polar identity and applying continuous functional calculus to the scalar bound yields the stated operator inequality. No finite-dimensional trace or order-d condition enters this upper bound. The complete gap has exactly three kinds of positive terms and the coefficients are consistent.

### Scalar extremum

Writing `z=e^(2is)` reduces the sum to twice `Σ |cos(s+yπ/d)|`. Its period is `π/d` because a shift permutes the terms modulo the π period of absolute cosine. On the odd-d fundamental interval, centered reindexing makes all cosines nonnegative; on the even-d interval the sign split occurs exactly after the first `d/2` terms, including endpoints where a cosine may vanish. Summing the finite geometric series gives the displayed cosine expressions. Their strict maxima within the fundamental intervals prove precisely `z^d=(-1)^(d−1)`; there are no omitted equality phases. The bad polar-kernel roots instead have d-th power `(-1)^d` and are disjoint from this set.

### Attainment

The weighted shift `W_y=ω^y Z*X` has d-th power `(-1)^(d−1)I` and simple spectrum equal to the equality roots. None is −1, so the inverse used in the *explicit attaining strategy* is legitimate, unlike an unjustified inverse on an arbitrary strategy. The order-d calculation for the polar Bob observable works because the scalar product of its d phase factors is `(1−(−λ)^d)/|1−(−λ)^d|=1`. In an eigenbasis of `W_y`, conjugation by `Z` cycles the distinct eigenvalues; this also justifies the weighted-cycle argument for complete simple measurement spectrum.

The maximally entangled trace identity requires Bob's transpose. The manuscript's `B_y=Q_y^T=overline(V_y)` has the correct convention. The added `Z ⊗ Z*` term attains one. Thus finite-dimensional attainment genuinely matches the upper bound and establishes all three claimed values via set inclusion and continuity.

### Support cancellation and support invariance

The proof correctly distinguishes the equality-root spectral subspace `L` from the reduced-state support `K`. Initially one knows only `K ⊆ L`, not that `K` is invariant under `U`. The Schmidt-support equivalence for Alice operators is exact for nonfaithful reduced states.

The augmented stabilizer gives `A0 K=K`. This is the necessary additional mechanism used before polar cancellation. Because the bad-root projection kills `K`, the final polar support projection fixes `K`. Therefore `q=(I−V_y B_y)Ψ` lies simultaneously in the final support and its orthogonal kernel when `P_y Ψ=0`; consequently `q=0`. There is no inverse, hidden full-rank assumption, or illicit cancellation here.

Taking a partial trace gives `ρ_A=V_y ρ_A V_y*`. Together with the fact that `V_y` is isometric on `K`, this gives `V_y K=K`. Thus `S_y=A0*V_y` is unitary on `K`. The identity `s_y(z)^2=ω^y z` on the equality roots now implies that `U` preserves `K`; finite-dimensional unitarity upgrades inclusion to equality and gives a reducing subspace. The proof does not assume this conclusion prematurely.

### Adjacent phases and multiplicity

For each root, the half-angle phase changes by `η=e^(πi/d)` between adjacent y values except at the unique crossing of the negative-real cut, where it changes by `−η`. The exceptional root index is exactly `[k+y]_d=floor((d−1)/2)`. The same formula holds for the wrap from `y=d−1` to `y=0`, so every root is singled out once.

The stabilizer and cross-party commutation imply `V_y^d Ψ=Ψ`; support cancellation then gives `V_y^d=I` on `K`. Together with the adjacent-phase identity and `η^d=−1`, this produces the hypotheses of the reflection-rank lemma for every root projection.

The ordered factorization `(TR)^d=T^d (T^(−d+1)RT^(d−1))⋯(T^(−1)RT)R` is correct. Rank subadditivity applied to `I−AB=(I−A)+A(I−B)` gives `rank(I−R_(d−1)⋯R_0)≤dr`, whereas the product is `−I`, so the left side is n over ℂ. Every root projection therefore has rank at least `n/d`. Since the d mutually orthogonal projections sum to identity, all these lower bounds are equalities. Missing roots, unequal root multiplicities, and `dim K<d` are thus excluded, with no commutativity assumption between `T` and the reflection.

The conclusion does not prove a unique measurement ordering, a Weyl representation, maximally entangled state, full self-testing, approximate rigidity, or private randomness. None of those stronger statements should be inferred from this theorem.

## Sampled checks, separate from proof

Both existing focused regression programs were also rerun successfully in this review. `verification/verify_rigidity.py` passed 89,439 supported-phase triples for d=2..64, 840 exact-rational hostile rank products, and 16,128 multiplicity/divisibility count cases (d=2..64, dimensions 1..256). `verification/verify_exact_benchmarks.py` passed the d=2..6 radical table and d=4 entropy, cosecant-square/coefficient normalization through d=100 with hostile general shifts, and 77 source/polar/Fourier Bob-operator comparisons for d=2..12, including the explicit qutrit formula. The programs exited zero. These finite regressions do not independently prove their all-d mathematical targets.

An independent Python calculation using only `cmath`, `math`, and `json` checked all adjacent phase ratios, including wraparound, for every `(d,y,k)` with `2≤d≤100`. It also checked the scalar value at every equality root and at a 301-point circle grid per d. Maximum phase error was `4.587422696419812e−13`; equality-value error was `2.7000623958883807e−13`; the largest apparent upper-bound excess was `2.5579538487363607e−13`, consistent with floating-point roundoff. This corroborates indexing and parity conventions only; the preceding algebra, not these samples, proves the assertions.

Reproduction of the central sampled check:

```python
import cmath, math
phase_error = 0.0
for d in range(2, 101):
    w = cmath.exp(2j * math.pi / d)
    eta = cmath.exp(1j * math.pi / d)
    for y in range(d):
        for k in range(d):
            z = cmath.exp(1j * math.pi * (2*k + (d % 2 == 0)) / d)
            a = 1 + w**y * z
            b = 1 + w**((y+1) % d) * z
            sign = -1 if (k+y) % d == (d-1)//2 else 1
            phase_error = max(phase_error,
                abs((a/abs(a)).conjugate()*(b/abs(b)) - sign*eta))
print(phase_error)
```

## Lean: useful optional verification, not a submission gate

The most useful formal target is the new finite-dimensional supported-multiplicity theorem, including the bridge from actual quantum strategies to support restrictions. This is where dependencies are least transparent to a quick reader. A standalone formal reflection-rank lemma is a small, reusable first milestone, but it certifies only the last step; it would add limited legitimacy by itself. Likewise, formalizing the polar expansion while assuming all spectral and support consequences would leave the essential analytical/modeling work outside the checked boundary.

A sensible sequence is: general complex finite-dimensional reflection-rank bound; ordered roots and adjacent phases; support cancellation plus stabilizer invariance; the entire finite-dimensional multiplicity endpoint. An independent exact four-outcome counterexample is another compact target, but its arbitrary-d upper-bound dependency must be visibly accounted for if claiming it is a verified *maximizer*. Full arbitrary-Hilbert-space commuting-operator formalization adds substantial functional-calculus and operator-algebra work and should not delay feedback or submission of a sound ordinary proof.

Actual reuse from the existing Lean project is limited:

- `Bell/Quantum.lean` fixes `Qubit := Fin 2` and the joint space to two qubits; it is not a ready arbitrary-d Bell framework.
- `Bell/Purification.lean` contains useful matrix-square-root, trace, positivity, and transpose patterns, but its physical purification implementation is qubit-specific.
- `Bell/ProjectionSupport.lean` proves qubit projector facts by explicit two-by-two Cayley–Hamilton algebra. It does not provide arbitrary-dimensional reduced-state support cancellation or the reflection-rank theorem.
- `Bell/FiniteLinearAlgebra.lean` is chiefly real incidence linear algebra; its general patterns may help, but it does not already contain the required complex spectral proof.
- The existing build, negative controls, theorem-dependency audit, and independent statement contracts are useful process templates. Their existing success receipts do not certify any claim of this cyclic Bell paper. I inspected source but did not rerun that project's compiler or audit its complete dependency graph.

Recommendation: treat Lean as a targeted optional companion if resources permit, with explicit theorem coverage. Do not make it the immediate prerequisite for seeking substantive expert criticism or journal consideration. Formal proof would improve confidence in precisely defined claims; it would not establish novelty, impact, correct source attribution, or acceptance by a journal. No resource estimate is asserted without first piloting the arbitrary-dimensional support infrastructure.

## Remaining limits of this assigned review

No exact blocker was found for the reviewed operator results. This audit did not independently establish literature novelty, review every permutation or second-family proof, review every randomness benchmark, or verify journal policies. Those are separate tasks. There was no external contact and no manuscript change.
