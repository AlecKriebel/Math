# Entropy and nondiagonal asymptotic pairs: prior negative resolution

**Problem:** 30004994 / OWR-9790354-005  
**Status:** `already_solved`  
**Answer:** No, under the stated hypotheses.  
**Attribution:** Tom Meyerovitch, Theorem 1.2 and Section 4 of *Pseudo-orbit tracing and algebraic actions of countable amenable groups*, Ergodic Theory and Dynamical Systems 39 (2019), 2570–2591, [DOI](https://doi.org/10.1017/etds.2017.126); [author preprint, version 2](https://arxiv.org/abs/1701.01318v2).

The exact target permits a countably infinite amenable group without finite generation. Meyerovitch constructs an expansive algebraic action of a countable direct sum of finite abelian groups with positive entropy and no distinct asymptotic pair. This settles the universal equivalence negatively. The Oberwolfach source itself acknowledges this counterexample on page 141, immediately after its displayed question.

This packet verifies a known construction. It claims no new theorem, proof priority, or solution to a finitely generated restriction. The catalogue's general unresolved-status description should not be used for this exact universal claim.

## Contents

- `verification.md`: self-contained mathematical verification of a concrete instance, including all target hypotheses
- `source_map.md`: exact source locations, publication provenance, and scope checks
- `check_controls.py`: dependency-free exact finite-dimensional controls
- `controls.json`: deterministic output from those controls
- `research_log.md`: dated verification history and budget disposition
- `result.json`: machine-readable classification and explicit limits

Run `python3 check_controls.py` from this folder and compare its stdout with `controls.json`. The controls check finite identities and adversarial boundary cases; the infinite construction and entropy limit are justified in `verification.md`, not inferred from simulation.
