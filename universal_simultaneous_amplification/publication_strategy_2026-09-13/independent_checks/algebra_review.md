# Independent response-algebra and reduced-chain review

Checkpoint: 2026-09-14 00:42 UTC (2026-09-13 local date). Completion: 100% of this bounded algebra/reduced-chain review; this is not a percentage estimate of the theorem's truth or a complete analytic proof audit.

## Scope and result

Reviewed the current paper's definitions, construction, effective dyadic diagonal, gate rate table and sweep argument, response formulas, sextic tangency, fixed-parameter optimization, and rational-edge corollary. Read the certificate implementations before running them; did not rely on historical audit verdicts. No algebraic or reduced-chain error found.

The exact result being claimed is an asymptotic lower bound R_sim >= 1.5028569127905696... for one fitness-independent weighted undirected graph family. For each fixed r in the open interval (1,R_hyb), sufficiently large members amplify both update rules relative to their respective same-size complete graphs. The sufficiently-large population can depend on r. This is not simultaneous amplification for all r>1, not a uniform finite population guarantee, and not a proof that R_hyb is the unrestricted threshold. The optimized endpoint has vanishing first-order corrections, so the theorem correctly excludes it.

## Independent deductions

* The four gate rates have the correct parent/death weighting and pair establishment factors. In particular, the dB factor 1/r when a resident invades a mutant module is essential and appears in the manuscript. K2 establishment is r/(r+1) under Bd and 1/2 under dB.
* For the stated macro chain, any failure starting from a mutant center requires a center reversal before the q possible pair conversions. The union bound q C'/(B+C') is valid even though a reversal need not imply failure. Starting from one mutant pair gives A/(A+D) times fixation from (1,1). The equivalent identity with P_H follows from the first event at (1,0). These arguments include repeated adverse reversals.
* Clearing the positive denominators reduces simultaneous positivity to a quadratic in sigma. Its unrestricted minimum equals -P(r)/(4(r-1)), giving the stated tangency. The derivative sign argument is valid on the required interval, since 0<sigma_*<1 and (r-1)^2<0.51^2 there. Immediately above R_hyb even the unrestricted real-sigma minimum is positive, proving the claimed first-order model bound, not a bound on all graphs.
* An additional independent computation proves the rational parameters (19/137,20/27) give both corrections positive on the entire rational interval (1,1.5017], already enough to cross 3/2 without requiring the optimized algebraic parameters.
* The dyadic choice fixes weights before fitness is selected. Real-algebraic quantifier elimination supplies computability in principle, conditional on the finite-trace convergence proposition. It supplies no usable population or edge-size bound; there is no verified practical-size construction in these checks.

## Replayed and new checks

Python 3.14.6, SymPy 1.14.0 imported directly from the paper's vendored wheel, with the matching mpmath wheel. No installation or source modification was needed. All invocations set PYTHONDONTWRITEBYTECODE=1.

Common environment, relative to repository root:

```
PYTHONDONTWRITEBYTECODE=1
PYTHONPATH=universal_simultaneous_amplification/phase4_landmark_closure/paper_hybrid_threshold/vendor/sympy-1.14.0-py3-none-any.whl:universal_simultaneous_amplification/phase4_landmark_closure/paper_hybrid_threshold/vendor/mpmath-1.3.0-py3-none-any.whl
```

Each listed path was run using `python3 PATH` with that environment; all exited 0:

| Path | Observed output |
|---|---|
| phase4_landmark_closure/paper_hybrid_threshold/certificates/verify_leading_algebra.py | PASS exact sextic threshold, tangency, and monotonicity algebra; R_hyb 1.50285691279056963, sigma 0.130677282287048377, lambda 0.750806483031880492 |
| phase4_landmark_closure/paper_hybrid_threshold/certificates/verify_hybrid_coefficients.py | PASS exact hybrid coefficient and phase-polynomial audit; rational margins Bd=232/17361, dB=65/12123; rational threshold 1.50176815223369 |
| phase4_landmark_closure/paper_hybrid_threshold/certificates/verify_hybrid_lumping.py | PASS exact labelled hybrid lumping: n=9, masks=512, fibres=108 |
| phase4_landmark_closure/paper_hybrid_threshold/verify_paper_claims.py | PASS: Paper II exact integration audit |
| publication_strategy_2026-09-13/independent_checks/algebra_independent.py | PASS rational witness on (1,1.5017]; PASS exact macro-chain identities and sweep bound for q=1,...,7 and two rate regimes |

All paths in the table start with `universal_simultaneous_amplification/`. The independently written final script does not import paper verifiers. One rate regime has small center-reversal rates and the other has reversals much faster than pair conversions. Its exact finite tests support the general recurrence argument; finite testing alone is not its proof.

The integrated verifier also checks literal manuscript markers. Those checks are useful consistency guards, not mathematical verification of the corresponding prose. The labelled n=9 audit graph is a test of the transition formulas, not a demonstrated finite member of the asymptotic theorem's family. This sub-review ran the local source certificate files and did not separately byte-compare them with the deposited archive.

## Remaining analytic dependencies and publication implication

The decisive dependencies are the compact-uniform weak-cut limit and the isolated center estimates at o(q/C) precision, especially reciprocal invasion bounds, pendant cleanup, stopped-process control, and uniformity of constants. Algebraic certificates do not establish these. Conditional on those inputs, I found the passage from gate rates to the claimed response optimization internally sound.

The best use of an external specialist's review is to test those analytic lemmas and their quantifiers. The human user alone can conduct any external communication. This report prepares no outreach.

## Lean return on resources

Do not make a full Lean formalization a prerequisite to journal submission. Formalizing the rational inequalities, sextic isolation/tangency, and a finite macro chain could create a clearly scoped kernel-checked algebra certificate. That is mathematically useful but would leave the main probabilistic and asymptotic burden intact, so it would have limited effect on acceptance compared with an expert audit and clearer quantitative hypotheses. A full formalization would need the original stochastic process, strong lumpability, perturbation/weak-cut limits, stopping-time arguments, uniform asymptotics, and effective diagonal. This is a substantial distinct project; no reliable person-month estimate was established here.

If funding a pilot, require an explicit statement of the exact theorem formalized and enumerate all assumed probabilistic lemmas. Do not describe a proof of the response inequalities under assumed response formulas as formal verification of the full amplifier theorem.
