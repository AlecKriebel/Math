# Independent Lean review: permutations, witnesses, and target probabilities

Date: 2026-09-16. Completion estimate: 100% of the assigned source-level witness/permutation review. Scope: the delivered `package/lean_formalization` against its own `reference/manuscript/main.tex`, not an earlier repository version. No package files were edited and no Lean builds were run by this reviewer; the coordinating reviewer owns fresh compilation and axiom verification. Passing self-reports, recorded logs, and coverage inventories were not treated as evidence.

## Verdict

**The core all-dimensional first- and second-family counterexamples are represented by meaningful physical theorem statements. I found no circular maximality assumption, substituted probability table, coefficient normalization assumption left on an endpoint, or adjoint/sign mismatch in the reviewed construction.** The d=4 code independently constructs actual projective strategies and derives the stated 1/32, 3/32 probabilities and Bell values.

There is one identifiable literal coverage omission: the complete second-family first-harmonic matrix, for all d Alice inputs, is not explicitly proved invariant under permutation. The generic conditional permutation invariance theorem has only two Alice inputs and does not itself cover that assertion. Thus I would approve the construction/counterexample coverage in this scope, subject to the independent build, but would not describe every clause of manuscript Theorem `thm:second` as formally reproduced without either adding the short missing theorem or stating this limitation.

All source paths below are relative to `package/lean_formalization/`.

## Finding P2: explicitly complete the second-family correlator claim

The manuscript at `reference/manuscript/main.tex:1012–1013` asserts invariance of the **complete** complex first-harmonic matrix. The displayed derivation at lines 1066–1085 proves

    <A_l B_y> = lambda_l omega^(-l y),
    <A_l B_d> = delta_(l,0),

and vanishing local first moments for every l, y. Those are stronger data than an unchanged Bell sum.

The delivered proof establishes Fourier compression in `CyclicBell/GeneralSecondWitness.lean:97–111` and the real weighted term in `secondPermutation_term` at lines 135–150. It establishes total attainment at lines 153–167. None of these theorem statements supplies the entire individual correlator matrix. The only dedicated additional second-family correlator endpoint I found is `secondPermutation_aligned_correlator` in `GeneralCorrelationValues.lean:137`, which supplies the real part at Alice input 0 and extra Bob input only.

The apparently broader results `linear_permutation_all_harmonics_invariant` (`GeneralCoveragePermutation.lean:160`) and `conditional_permutation_complete_harmonics` (`GeneralCoverageWitness.lean:86`) quantify over `x : Fin 2` for the generic affine two-Alice-setting construction. They do not instantiate the d distinct second-family Alice rows, and there is no theorem transferring them to those rows. `firstPermutation_harmonics` (`GeneralFirstWitness.lean:93`) likewise covers the first family's two rows.

I searched the actual Lean files for `secondAlice`, `secondPermutation`, harmonic/invariance terms, and the displayed lambda/character product; I found no alternate theorem expressing the missing second-family matrix result. This is not evidence that it is false: the existing `phi_weighted`, `sum_permuted`, `polarTransform_shift`, and `polarTransform_compression` lemmas give a short proof. Recommended repair: state and prove the two literal formulas above, both local-moment statements, and a permutation-invariance corollary for `secondPermutationStrategy`. This closes a manuscript claim without changing the construction or the principal counterexample endpoints.

Concrete proposed endpoints, written in the delivered namespace and notation (proposals only, not compiled during this audit):

```lean
theorem secondPermutation_correlator (hd : 2 ≤ d)
    (κ : Equiv.Perm (Ix d)) (l y : Ix d) :
    expectation (maximallyEntangled d)
      (kron (encoded (secondAlice hd κ l))
        (encoded (permutationBob κ (some y)))) =
      generalLambda l * chi (-(l*y)) := by
  -- prove from actual weighted encodings and Fourier compression

theorem secondPermutation_extra_correlator (hd : 2 ≤ d)
    (κ : Equiv.Perm (Ix d)) (l : Ix d) :
    expectation (maximallyEntangled d)
      (kron (encoded (secondAlice hd κ l))
        (encoded (permutationBob κ none))) =
      if l = 0 then 1 else 0 := by
  -- character orthogonality after removing the permutation
```

The intended proof of the first endpoint is concrete: `secondAlice_encoding`, `permutationBob_some`, and `weighted_entry_conjugate` reduce to two weighted cycles. `phi_weighted` (`GeneralCycles.lean:55`) gives `(sum_j star(secondWeight l (κ j))*star(polarPhase y (κ j)))/d`. `sum_permuted` removes κ. Expanding `secondWeight` and using `polarTransform_shift` with commuting scalar factors gives `star(secondPrefactor l)*chi(-(l*y))*polarTransform l/d`; compression plus `secondPrefactor_unit` gives the literal lambda formula. The second endpoint uses the same calculation with Bob's constant weight one and `character_sum`. Local moments use `phi_local_left`, `phi_local_right`, and `weighted_trace_zero`, with the explicit encodings. These generic lemmas make the omitted result straightforward to derive; they do not themselves state it.

A smaller packaging omission is that manuscript `thm:second` says every SOS residual annihilates the state. There is an explicit d=4 theorem `Attainment.lean:164`, but no explicit all-dimensional second-witness residual-zero theorem. The all-dimensional code instead proves scalar attainment directly and proves the universal SOS separately. This alternative proof fully suffices for maximality, so it is not a correctness blocker. If every sentence of `thm:second` is claimed as a literal formal endpoint, add that short residual statement too.

## Physical definitions and absence of circular assumptions

`GeneralModel.lean:14–24` defines a state by a positive semidefinite density matrix of trace one and a measurement by positive, complete, pairwise orthogonal idempotent effects. `StrategyOn` at lines 40–44 consists only of that state and Alice/Bob measurement families. It does not assume a Bell upper bound, equality spectrum, attained value, rank, or target probability. The local coordinate types are independent arbitrary finite types; upper-bound comparisons are not confined to dimension d.

`encoded` at `GeneralModel.lean:26` is the ordinary character-weighted sum of effects; `kron` at line 28 is the actual Kronecker product; `bornProbability` and `behavior` at lines 34–48 evaluate the actual density/effects. `Option.none` represents the extra Bob input d, while `some y` is reduced input y. This matches the manuscript's input alphabets.

The conditional theorem's `PermutationData` (`GeneralPermutation.lean:151–160`) **does** have scalar equality and phase alignment fields. Here that is legitimate: these are precisely the hypotheses of the manuscript's conditional sufficient theorem, not a definition of arbitrary physical strategy. They are accompanied by an explicit scalar cap in `conditional_permutation_theorem` at line 241. In the concrete cyclic-family construction, the unit/product/alignment/equality facts are separately proved; they do not remain user-supplied maximality assumptions.

## Coverage map and source inspection

| Manuscript content | Actual Lean evidence inspected | Assessment |
|---|---|---|
| Conditional phase-permutation construction, simple spectrum, order, and invariance (`main.tex:606–722`) | `GeneralPermutation.lean:151–253`; `GeneralCoveragePermutation.lean:86–178`; `GeneralCoverageWitness.lean:22–147`; `GeneralCycles.lean:30`, `GeneralCycleCharpoly.lean:84` | Substantive coverage. The generic upper bound includes an arbitrary-Hilbert C*-algebra extension, zeros of affine factors, and all two-row first moments/correlators. Simple spectrum is an eigenspace dimension-one theorem, not merely a set of roots. |
| Equality roots and phase normalization (`main.tex:734–756`) | `GeneralPhases.lean:69,96`; `GeneralChirp.lean:85`; `GeneralPolarPhases.lean:13–16,111–146`, plus `polarPhase_product` later in that file | Parity convention is correct. Polar phases are explicit signed half-angle expressions, then proved equal to the quotient in the paper. Product-one constraints are proved. |
| First actual permutation strategy (`main.tex:760–773`) | `GeneralFirstWitness.lean:14–47` | Genuine complete PVMs are constructed from phase bases; Bob uses entrywise conjugation of the weighted cycle. Extra Bob is X. |
| Actual first-family attainment and arbitrary-dimensional competition | `GeneralFirstWitness.lean:72–90,122–127,132–152`; upper-bound endpoint in `GeneralFirstBound.lean` | Maximality is a proved conclusion. The witness theorem does not infer maximality merely from SOS annihilation or a matching numerical value. |
| Fourier table and d^-3 normalization (`main.tex:790–828`) | `GeneralWitness.lean:225–251`; `GeneralFourier.lean:228–278`; `GeneralFirstWitness.lean:105–118` | Born rule is reduced through rank-one amplitudes to the Fourier table, including the negative `(a+b)` index and d^-3. Actual first-strategy target effects are connected to that table. |
| Canonical flatness and small d boundary | `GeneralChirp.lean:88–102`; `GeneralOrbitConsequences.lean:26–65` | Correctly about this orbit. d=2,3 flatness is not inflated into a theorem about all Bell maximizers. |
| Final-two swap and nonuniformity (`main.tex:850–911`) | `GeneralSwap.lean:13–15,28,95–107,149`; `GeneralGuessing.lean:63–80,138–166` | The exact swap is `Equiv.swap (-2) (-1)` on `ZMod d`; it has the intended representatives for d>=4. Nonzero lag-two autocorrelation and the displayed quantitative lower bound are derived, not assumed. |
| Second source coefficients (`main.tex:916–967`) | `GeneralSecondCoefficients.lean:12–40,56–74,197–227` | Literal exponential/sine formula and exceptional l=0 sign are present. Normalization is proved by Fourier compression plus Parseval, a valid alternate derivation to the manuscript's cosecant identity. |
| Second physical operators and exact compression (`main.tex:991–1065`) | `GeneralSecondWitness.lean:12–69,71–111` | Correct r_l, character orientation, entrywise conjugation, order-d product, and exact complex lambda phase. |
| Second target equality with first strategy | `GeneralSecondWitness.lean:116–132,169–185` | Equality of encoded observables is lifted to equality of actual outcome effects by measurement reconstruction. No hidden output relabeling is needed. |
| Second maximality and d>=4 biased table | `GeneralSecondWitness.lean:153–218`; `GeneralSecondBound.lean:14–45` | Genuine arbitrary-finite-competitor theorem, exact value d+1, normalized marginals, nonuniform target, and quantitative bias. No coefficient-normalization premise remains. |
| Behavioral inequivalence under local output permutations (`main.tex:1150–1169`) | `GeneralOrbitConsequences.lean:69–98` | Actual canonical/swapped strategies have inequivalent designated tables for every pair of local output permutations. Scope is correct. |
| Exact d=4 physical example (`main.tex:1728–1782`) | `D4.lean:17–64,73–134`; `Witness.lean:21–100,157–175,177–224`; `Attainment.lean:18–62,106,147`; `Endpoints.lean:31–56` | Tables come from actual states and PVMs, Bell values from actual functionals, maximality from independent upper bounds. Conjugation conventions match the manuscript. |

## Sign, coefficient, and normalization checks

1. `chi` is `ZMod.stdAddChar` (`GeneralFourier.lean:21`) with explicit exponential bridges at lines 70–78. `fourier` at line 100 uses the plus Fourier sign. `fourierTable` at line 228 evaluates it at `-(a+b)` and divides by d^3, matching the paper.
2. `weightedCycle` (`GeneralWitness.lean:35`) has entry w_j at row j+1, column j, hence is X diag(w), not diag(w) X. This is consistent with the prefix recurrence and target phase basis.
3. `generalLambda` uses the natural power `(-1)^(l.val+1)` to avoid natural subtraction at zero. `sign_exponent_bridge` and `generalLambda_literal` (`GeneralSecondCoefficients.lean:24–40`) prove equivalence with integer exponent l-1, including l=0. There is no accidental `(-1)^0` substitution.
4. `secondPrefactor` is exp[-pi i l(l-1+delta_d)/d], and `secondWeight` multiplies it by chi(-l*j). `secondAlice_encoding` is the entrywise conjugate of the corresponding weighted matrix. `secondPermutation_compression` proves the exact operator factor d lambda_l, not just its modulus.
5. The second functional takes `star(generalLambda l)` times Alice tensor Bob's plus-sign Fourier sum (`GeneralSecondBound.lean:14–17`). It is the manuscript's Hermitian score through real state evaluation. The SOS prefactor is 1/(2d), explicitly instantiated at `GeneralSecondBound.lean:39–45`.
6. The d=4 physical implementation uses a distinct `sourceLambda` in `Functionals.lean:30–34`; it likewise has integer exponents. `ScalarData.lean:254` proves its equality to the algebraic four-entry coefficient array, rather than substituting the array without justification.
7. `Witness.lean:168` explicitly proves Bob is the entrywise conjugate of the printed polar-exponent matrix. `Witness.lean:199` explicitly proves Alice is the entrywise conjugate of the printed D_l. `Attainment.lean:52` proves Fourier compression with that literal D_l. These are appropriate safeguards against the paper's source-convention ambiguity.

I did not find a generic theorem explicitly transporting all probabilities under the alternative convention B -> B†, b -> -b. There is a useful existing constructor, `negateMeasurement` (`GeneralPhaseTables.lean:23–29`), whose effects are definitionally `M.effect (-b)`. However it is only used there to define Fourier-phase-basis tables; no theorem proves that its encoded observable is `(encoded M).conjTranspose`, and no theorem applies it to the cyclic strategy or transported functional. The main formal construction consistently uses the paper's chosen no-adjoint convention, so this does not affect its counterexample. A claim of literal coverage of the alternative-convention sentence should be qualified or supplemented.

The appropriate repair is to prove `encoded (negateMeasurement M) = (encoded M).conjTranspose`, then construct the strategy with every Bob PVM negated and prove its behavior at `(x,y,a,b)` equals the original behavior at `(x,y,a,-b)`. For the Bell-value transport, explicitly define the alternate convention's functional using adjointed Bob observables; merely negating Bob outcomes while leaving the same coefficient functional fixed does **not** establish unchanged value. With the transported functional, maximality, nonuniformity, and guessing probability follow by the involutive outcome relabeling. This matches the paper's convention note and avoids accidentally formalizing a false invariance of the fixed functional.

## Quantitative proof difference: a valid strengthening

`GeneralGuessing.lean:82–135` proves a sharper generic Fourier estimate than the manuscript uses:

    max_m |q-hat_m|^2 >= d + |R_t|   (t != 0).

It subtracts the maximum Fourier power from the Fourier inversion sum. The resulting nonnegative deficits have total d(max-d); the triangle inequality yields the displayed bound. This is valid. For the final swap it gives a probability at least

    1/d^2 + 4 sin(pi/d) sin(3pi/d)/d^3.

`swappedTarget_quantitative` at lines 138–156 explicitly weakens this to the manuscript's stated bound, using d>=4. Therefore the endpoint is neither weakened nor shifted by a normalization error. The proof difference is favorable and worth recording if the manuscript is later revised.

## What this review does and does not establish

- Source inspection supports the semantic faithfulness of the principal all-dimensional and exact d=4 constructions.
- No `sorry`, `admit`, `axiom`, or `native_decide` was found in the construction/theorem files searched in this scope; this is not a substitute for the root reviewer's complete dependency/axiom audit.
- This reviewer did not run a fresh build and makes no build-success claim. Statements above describe the delivered source and its intended proof terms, conditional on the independent compilation result.
- Full q/qa/qc set definitions, closure arguments, arbitrary Eve optimization, support-rigidity, and the entire external source bibliography are assigned to other review work. The counterexample endpoints inspected here do not assume those results to construct their physical witnesses.
- Recommended disposition in this scope: accept the central witness/counterexample formalization after a clean build, while addressing or explicitly disclosing the second-family all-correlator coverage omission before claiming a complete literal formalization of every manuscript assertion.
