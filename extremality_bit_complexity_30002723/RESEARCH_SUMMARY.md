# Research outcome: rational one-row extremality in polynomial bit time

20 October 2026. Row 1827, ID 30002723.

## Result

A complete authored reduction gives a polynomial-bit-time decision algorithm for the exact sparse rational input model, including two-sided-discontinuous input and unrestricted valid-function competitors. It reduces the complete Basu–Hildebrand–Köppe 4q-grid tight system to polynomially described signed interval-orbit systems and a polynomial-size residual rank computation, using Agol–Hass–Thurston's existing orbit algorithms.

The completed reviews and a fresh final independent audit found no mathematical gap. This is a newly authored proof subject to further external review, not a claim of journal acceptance or independently established priority. There is no implemented compressed AHT-based extremality solver in this package.

Package disposition: **CLAIMED_SOLVED, 5/5 substantive attempts**, with the limits below. The final acceptance and reproducibility details are in `ACCEPTANCE_REPORT.md`.

## Five substantive attempts

1. ATTEMPT_1.md: exact source theorem and binary encoding, plus an exact counterexample to same-grid rigidity implying extremality.
2. ATTEMPT_2.md: sparse interval-pairing compression and a complete continuous-subclass route.
3. ATTEMPT_3.md: exact all-discontinuity local factorization into slopes, jumps, spikes, and coarse endpoint sectors.
4. ATTEMPT_4.md: signed two-sheet orbit dimension, dimension cutoff, representative extraction, weighted reconstruction.
5. ATTEMPT_5.md: full theorem, algorithm, correctness, and bit-complexity assembly.

## Independent review

- AUDIT_FULL_THEOREM.md: fresh final PASS for the complete theorem; independent tests include 739 local comparisons and 20 end-to-end dense simulations.

- AUDIT_ORBIT_COMPRESSION.md: independent acceptance audit of Attempts 3–5, with six obligations checked and 434 independent algebra checks.
- structural/FULL_REDUCTION_REVIEW.md: separate review of the entire direct 4q reduction.
- structural/SIGNED_ORBIT_COMPRESSION_LEMMA.md and structural/LIMITING_EDGE_LOCAL_AUDIT.md: separate detailed derivations.

## Exact verification

All tests below passed. They use dense finite matrices/union-find to check the mathematical reduction, not to demonstrate the asymptotic AHT runtime.

- A minimal q=5 function is rigid on its coarse grid but not extreme; an explicit 1/15-grid perturbation is checked with epsilon=5/18.
- 35 sparse rational minimal inputs, including five two-sided-discontinuous inputs: full, structured, and joint matrix ranks agree.
- Five genuine 4q refinements: exact full/structured/joint ranks agree, including a two-sided-discontinuous extreme example and a two-sided-discontinuous non-extreme example.
- Four end-to-end signed-orbit reconstruction cases: residual nullities 0,32,0,2 agree with the complete 4q systems.
- 204 random signed graphs and 230 rational trace reconstructions: all pass.
- 70 recorded continuous discovery-run cases and one stored all-covered non-extreme example: agree with exact 4q references. The 70 individual discovery inputs were not saved, so only the separately stored example is part of exact saved-input replay.
- 739 fresh independent local row-space comparisons and 20 independent compressed-decision simulations pass, including the D>K cutoff.

Reproduce all saved exact inputs without rerunning floating-point LP discovery using `python replay.py`. Selected direct commands are:

    python checks/verify_counterexample.py
    python checks/verify_discontinuous_reduction.py --saved
    python checks/verify_fourfold_refinements.py
    python checks/verify_orbit_pipeline.py
    python checks/audit_signed_reconstruction.py

Python 3, SymPy, NumPy, and SciPy are used. Floating-point LP is only a discovery step in the optional generation mode; every stored case and stated rank claim is checked using exact rationals.

## Boundaries

Ordinary polynomial bit complexity only, not strong polynomiality. Rational sparse input only, not irrational encodings or higher dimensions. Decision only: no promise of printing exponentially many perturbation breakpoint values. Copied scholarly sources and original problem-dataset records remain outside this authored artifact package.
