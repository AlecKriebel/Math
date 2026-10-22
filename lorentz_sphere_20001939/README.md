# Projectively equivalent indefinite metrics on the three-sphere

Problem: [UnsolvedMath 20001939 / AIM-GEOMETRY-0277](https://www.unsolvedmath.com/problems/20001939), originally Burns–Matveev, Question 12.0.6.

**Outcome: unresolved after five substantive attempts, with restricted obstruction results.** This is an AI-assisted, unrefereed research note. No full solution or historical novelty is claimed.

The original question asks whether the entire smooth three-sphere admits two nonproportional projectively equivalent indefinite metrics. It does not assume geodesic completeness, symmetry, or a fixed eigenvalue/Jordan type. The catalogue title, “Affine rigidity and a mobility-two reduction on the Lorentz 3-sphere,” describes an earlier partial result rather than replacing that question.

## Results obtained

1. A compatible tensor on a closed three-manifold with finite fundamental group has no globally simple real eigenvalue. For a hypothetical pair on S³, both ordered adjacent-eigenvalue collision sets must occur.
2. A single size-three Jordan block everywhere forces a constant eigenvalue: a canonical-frame calculation gives e₂(f)=−2f², and compactness makes the corresponding vector field complete. Together with known reductions, a nontrivial S³ pair must change algebraic type somewhere.
3. Every compact connected isometry group of either candidate metric is inherited by its partner. In particular, a left-invariant SU(2) metric cannot have an arbitrary nonproportional projective partner.
4. A standard T²-invariant Lorentz metric on S³ with nondegenerate principal torus orbits has no nonproportional indefinite projective partner. The proof allows cross terms initially.
5. At a nonstationary degenerate principal torus, invariant projective partners must share its null radical. Explicit metrics and local compatible tensors show that neither orbit degeneracy nor Jordan transitions can simply be dismissed.

The global collision/transition problem remains. The fifth attempt contains explicit scope checks showing why the preceding obstructions do not answer the original question.

## Files

- `turn_01.md` through `turn_05.md`: the five mathematical attempts, including proofs and exact gaps
- `SOURCE_GATE.md`: statement, literature, and prior-attempt checks
- `RESEARCH_LOG.md`: attempt accounting
- `verify_identities.py`, `verification.json`: four exact symbolic algebra checks

Run the checks with Python 3 and SymPy: `python verify_identities.py`. These calculations verify displayed identities, not the global proofs or the original conjecture. Fresh independent mathematical review is required before treating any new deduction as established research.
