# Reproducibility and finite verification

## Requirements and commands

Python 3.10 or newer and its standard library are sufficient. No network, compiled binaries, external dataset, or source PDF is needed. Run from the extracted public directory:

    python3 -I -B verify_package.py
    python3 -I -B run_checks.py
    python3 -I -B check_tamper_controls.py

The integrity verifier checks every public file against the manifest, refuses missing or additional files, rejects symbolic links and unsafe paths, checks the exact model and UNSOLVED status, verifies mathematical audit bindings, and checks local document links. The manifest excludes only itself; the outer archive receipt pins the manifest and the archive separately. Hashes establish byte identity and bindings, not independent mathematical truth or a cryptographic authorship signature.

The replay wrapper runs all nine mathematical checkers in isolated disposable copies in normal Python, -O, and -OO. Each output must be byte-identical to its included baseline. Explicit runtime guards remain active in all modes; no proof-critical Python assert is used. The wrapper deliberately forces one guard per checker, mutates six mathematical formulas, and corrupts a rational fixture. All these controls must fail at the expected guard. The package-level test separately exercises changed, missing, additional, duplicated and unsafe files; false solved status; and rehashed semantic changes to the cap, adaptivity, sampling law, covering event, affirmative and negative probability quantifiers, concentration denominator and audit binding.

No checker modifies the source package. Replay outputs are printed to standard output. If redirecting a fresh run, put it outside the public directory, since an extra file inside that directory is intentionally rejected by the inventory verifier.

## Included finite mathematics

- check_residual_profiles.py rebuilds 168 exact profiles for all nonempty set sizes at primes 2,3,5,7. It checks 11,766 improved-m swap inequalities, 5,311 same-A amplification inequalities, 12,314 integer failure thresholds, 1,239 greedy upper bounds, and 1,239 hypergeometric means. Its direct subset recurrence does not consume the historical census.
- check_amplification_scores.py preserves the study audit implementation. It checks 13,836 two-budget inequalities, 4,612 iterated repair inequalities, 307 Markov bridges, 684 optimized-score comparisons, 3,060 score-swap bounds, and the specified finite counterexamples. Its output exactly matches the accepted historical audit output.
- check_restriction_exchange.py checks 16,248 random-restriction mean identities, the same number of Jensen inequalities, 375 discrete second differences, 134,105 joint-hole probabilities, 2,969 exchange second moments, 2,969 variance descent bounds, and 1,298 no-improvement variance bounds.
- check_adaptive_flux.py checks 45 selector/parameter cases, 42,390 direct selector exchanges, 8,575 pointwise birth/death counts, and the strict negative-flux example with exact fractions. It explicitly distinguishes omitted and reversed flux.
- check_frontier_independently.py is the final study audit's distinct implementation of key cylinder, flux, and graph checks. Its output exactly matches the accepted final independent audit receipt.
- check_additive_graphs.py preserves the final exact implementation's cycle functions. It checks 238,423 vertex assignments, 222,480 permutation labelings, and 38,900 collision-partition terms in three synthetic parameter cases. Fourier orthogonality is checked by exact character-residue counts rather than approximate complex arithmetic. All graphs in these tiny cases happen to be feasible; this is not empirical evidence about asymptotic graph sparsity.
- check_cylinders_products.py enumerates coordinate conditionings, verifies the p=19 six-centre integral separation, and checks the representation-product inequalities by exact integer powers. Required affine representatives are regenerated directly from finite subsets; there is no dependency on the historical large census.
- check_canonical_normalization.py checks 20,616 selected labelled representation graphs and exact canonical weighting, as well as compact independent exchange and restriction examples. At the auxiliary case p=11,k=3,t=4, the correct success proportion is 1/3, dropping canonicality gives 11/3, and double division gives 1/6.
- check_moment_certificates.py verifies rational positive-support laws of degrees 4,10,20,30, finite-difference zero-free matching through degree 99, and Charlier certificates for eight parameters including the degree-201 certificate at 100. Synthetic rational fixtures are included. Numerical optimization originally suggested some supports; accepted positivity and all moments are rechecked exactly. These profiles are not asserted to be realizable translate convolutions.

The exact recorded counts and results are in the corresponding fixtures/check_*.json files. CHECK_REPLAY.json and TAMPER_CONTROLS.json record the completed public-package runs. CHECKER_IDENTITIES.json distinguishes unchanged checkers from public adaptations. Adaptations remove output-file writing or external historical-profile dependencies; they do not silently relabel a different computation as the original replay.

## Larger historical verification and its boundary

The study's earlier exact census tested all floor-size A at primes through 23, with affine-orbit accounting. The later all-cardinality profile census covers primes through 17; its p=19,23 extensions cover only the floor-size case. Two distinct C++ enumeration schemes and both optimized and NDEBUG builds were checked in the historical study. Those full raw census tables, binaries, and recovery packages are not needed or bundled here. Their final audit metadata is preserved as provenance, without claiming the lightweight public wrapper reruns them.

The final exact package and the final audit are separately hash-bound in AUDIT_BINDINGS.json. All 21 original mathematical reports are linked to the stage audit that pinned their original bytes. Public editorial adaptations have separately recorded byte identities.

At the small diagnostic primes, the original coefficient-100 cap exceeds the group size. Auxiliary budgets and alternative finite sizes test algebra and invalid implications, not the original probability limit. Neither successful replay nor a finite counterexample to a proposed shortcut proves an asymptotic answer. General partial theorems depend on the written proofs and the stated scholarly inputs.
