# Sylow restrictions and character fields of values

**Problem:** 30005220 / OWR-11101920-004  
**Assessment date:** 3 October 2026  
**Outcome:** Unsolved after five substantive approaches. No complete proof or irreducible counterexample is claimed.

## Question

Let P be a Sylow p-subgroup of a finite group G, and let χ∈Irr(G) have degree prime to p and conductor c(χ)=p^a m, with p∤m. Is

p∤[Q_(p^a):Q(χ_P)]?

Here Q_n=Q(ζ_n). The conductor is the least positive integer n for which the field is contained in Q_n. In particular Q_2=Q, and a minimal conductor never has 2-adic valuation 1.

## Main findings

1. The primary statement is Navarro's Conjecture A, printed p.2276 of OWR 39/2022. It already appeared as Navarro–Tiep's Conjecture C in 2021. The catalogue's supplied PDF link points to the wrong report; [the correct PDF is 46976](https://ems.press/content/serial-article-files/46976).
2. The p-solvable case was announced in the original talk and is due to Isaacs–Navarro (2024). Prime-degree characters are covered by Hung–Schaeffer Fry (2026). These are existing results, not resolutions obtained here.
3. The notes give full proofs of limited statements: the target holds for any ordinary character of positive degree less than p; it holds for irreducible characters with normal Sylow subgroup; and the published modular-multiplicity induction mechanism implies it for monomial irreducible characters of p′-degree. No novelty claim is made for these statements or proofs.
4. A reducible ordinary-character family on C_(p^2)×C_q, q>p prime, has degree p+1, global conductor p^2q, and restriction field Q_p. The tested index equals p. These examples explicitly fail irreducibility and are NOT counterexamples to the question. They explain why p′-degree and local orbit counting alone cannot prove the desired statement.
5. A newer theorem detecting the global conductor through generalized decomposition numbers does not rule out cancellation in the degree-weighted sums giving χ(u). The missing irreducible-character noncancellation step remains unresolved. At p=2, preserving the conductor level alone also leaves a separate field-generation issue.

## Contents

- [Source and status check](SOURCE_GATE.md)
- [Five-approach research log](RESEARCH_LOG.md)
- [Attempt 1: Galois detection and small degree](turn_01.md)
- [Attempt 2: Clifford homogeneity](turn_02.md)
- [Attempt 3: multiplicity criterion and reducible obstructions](turn_03.md)
- [Attempt 4: Mackey induction](turn_04.md)
- [Attempt 5: generalized decomposition numbers](turn_05.md)
- [Exact verifier](checks/verify_spectral_obstructions.py)
- [Recorded verification output](checks/verification_results.json)

Run from this directory:

    python3 checks/verify_spectral_obstructions.py

The script uses only the Python standard library. It passed 7,229 small-degree cyclic-character instances, 748 proper cyclic-subgroup induction congruences, five reducible obstruction examples, and the binary conductor-only warning. The checks use exact exponent multiplicities and Galois stabilizers; they are not an exhaustive search over irreducible character tables.

This is a research record, not a claimed solution or a refereed publication. The general conjecture is still presented as such in the latest directly inspected survey (May 2026); the literature search is not claimed exhaustive.
