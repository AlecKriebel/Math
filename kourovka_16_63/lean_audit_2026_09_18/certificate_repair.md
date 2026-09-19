# Certificate compiler repair audit

## Final status

Certificate-module compiler repair is complete (100% of this bounded subtask). All **41** current modules under `Kourovka/Certificates` compile, and each has an object newer than its source. This does **not** mean the complete Kourovka theorem has been formalized.

Final UTC checkpoint: 2026-09-19T04:43:12.517126+00:00

## Verified results

- Exact complete scalar kernels over residue rings, including valuation zero and valuation equal to the modulus depth.
- Complete diagonal-system counts, free columns, zero output padding, and invertible kernel transport.
- Sound decoding of swaps, shears, and supplied units; acceptance of a complete basis identity implies equivalence of complete kernels. Nonunit and same-coordinate negative tests compile.
- The actual 14,415 × 961 derivation matrix, its entry formula, and equivalence between its complete kernel and derivations.
- Exact lexicographic row/column indexing bijections.
- All **900** scalar identities of the supplied 30 × 30 rational left-inverse witness, followed by the extractor identity and injectivity for every parameter vector.
- Transport of that exact witness to every characteristic-zero field.
- Actual Jacobi-based inclusion of inner derivations in the kernel and the resulting **rank upper bound 931**, over both the rationals and every characteristic-zero field.

## Repairs

The proof repairs address Lean coercions, subtype arithmetic, ring-identity simplification, finite-sum unfolding, skew addition order, and overly aggressive extensionality. Statements were not weakened and no admission, custom axiom, or native decision oracle was introduced.

Large exhaustive decisions use `decide +kernel`, which leaves the computation to Lean's trusted kernel. A proved integer coefficient evaluator is used before rational arithmetic; it is linked by theorem to the actual sparse bracket. It is not an externally trusted replacement matrix.

The numerical witness was split into `InnerWitnessData`, thirty `InnerChecks/RowNN` modules, and `InnerWitness`. Its scalar-extension prefix was split into `InnerScalarWitness`. Original declaration names are preserved. These splits permit reusable checkpoints and bounded-memory compilation.

`DerivationMatrix` now imports the scaled data it actually needs; `InnerRank` explicitly imports the checked integral Jacobi development.

## Evidence

- `certificate_compilation_inventory.json`: all 41 current certificate modules have fresh objects.
- `inner_rows/summary.json` and per-row logs: all thirty row compilations returned exit code 0, generally in 36–41 seconds per row.
- `CertificateAxioms.lean` and `certificate_axioms.log`: eleven representative main declarations, including both rank bounds, depend only on `propext`, `Classical.choice`, and `Quot.sound`. No `sorryAx` or native-evaluation axiom appears.
- `certificate_data_integrity.json`: the supplied `selectedRow` and `inverseCoeff` source-data section is byte-for-byte unchanged from the user ZIP, SHA-256 `d4e30db745dca98c3fafca52ac177627b2811d6ba4ad1446f538f4ec9cb04430`.
- `InnerWitnessGenericCheck.lean` and `RankGenericCheck.lean` are successful isolated proof diagnostics with explicit hypotheses. They are not substituted for the unconditional actual modules, which now also compile.

Commands used the pinned Lean 4.19.0/mathlib environment, one Lean worker and a 64 MB thread stack. Heavy modules disable asynchronous elaboration. Two numerical row workers were used, with no change to the proof trust model. Early monolithic attempts exceeded reasonable memory or thread-stack limits and were interrupted; these were never counted as successful checks.

## Exact remaining mathematical gap

`Elementary.check_sound` is conditional on actual circuit acceptance. No concrete replay/acceptance proof for the supplied 931-pivot Smith plan is provided by these modules. In particular, the verified rank upper bound and left inverse do not themselves prove the Smith valuation multiplicities or the full group-automorphism cardinality statement. The project's larger incompleteness must remain visible in its publication status.
