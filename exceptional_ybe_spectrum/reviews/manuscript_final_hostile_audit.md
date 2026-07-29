# Final hostile manuscript audit

**Manuscript:** *Tensor-Local Constraints in the Exceptional Unitary
Hecke Yang--Baxter Class*

**Audit date:** 2026-07-29

**Auditor role:** independent adversarial proof review by a separate
OpenAI model instance

## Verdict

**Pass after repairs.** No central theorem was refuted, no circular
dependency was found, and the final dimension-six corollary matches the
scope of its inputs. The note is suitable for publication as an
unrefereed structural research note, not as a complete-spectrum result.

## Required repairs and disposition

1. **Twisted-control reduction.** The draft jumped from a bipartite
   support graph to a fixed-point-free form without printing the
   load-bearing intermediate step.

   **Repair applied:** the graph is now defined with loops counted as odd
   cycles, component projections are shown to reduce the first leg, and
   every bipartite component is written explicitly as
   \[
   \widetilde H_C
   =J_C\otimes W_C+J_C^*\otimes W_C^*.
   \]
   Matched bases for the partial isometry \(J_C\) then give the
   fixed-point-free form.

2. **Minimal-projection Markov weights.** The draft used
   \[
   t_{\lambda,n}=D_\lambda/2^n
   \]
   without a sufficiently local citation.

   **Repair applied:** the manuscript now states the
   \(\mathcal C(\mathfrak{sl}_3,6)\) normalization, the generating
   object's quantum dimension \(2\), and cites Galindo--Hong--Rowell
   Section 5.6 and Wenzl Sections 2--3 at the formula.

3. **Scope of the abstract-tower limitation.** “Complete abstract
   Hecke-tower arithmetic” could be read as exhausting every possible
   abstract invariant.

   **Repair applied:** the claim is now restricted throughout to the
   simple-multiplicity, central-rank, Markov-weight, and represented
   branching arithmetic actually computed.

4. **Star-real quotient functional.** The draft chose the functional
   only on the quotient-product span.

   **Repair applied:** the proof now explicitly extends it to the full
   quotient while preserving star reality.

5. **Verifier scope.** The draft could suggest that the universal
   rank-four quotient theorem was computational.

   **Repair applied:** the verification section now says that programs
   replay finite calibrations of the quotient and sandwich identities;
   the universal implication remains a human proof.

## Central theorem audit

| Result | Verdict | Scope guard checked |
|---|---|---|
| Automatic standardness | Pass | Irreducibility is derived from Lechner's theorem, not assumed. |
| Faithful Hecke passage | Pass | Faithfulness is only after quotienting by the Markov-trace annihilator. |
| All simple multiplicities | Pass after citation repair | The categorical dimensions are not ordinary simple-module dimensions. |
| Square inheritance | Pass | A one-sided \(4+2\) restriction remains open. |
| Dimension-six leg commutants | Pass | Only \(\mathcal C_L(P)\cap\mathcal C_R(P)=\mathbb CI_6\) is proved. |
| Low operator-Schmidt rank | Pass after printed reduction repair | No four-local equivalence is treated as a Yang--Baxter equivalence. |
| Unrestricted OSR four | Pass | Sandwich injectivity is conditional; simultaneous singularity remains possible. |
| Dimension-six frontier | Pass | It is a conjunction of necessary conditions, not nonexistence. |

## Publication boundary

The complete dimension spectrum remains open. The audit does not supply
specialist peer review, validate absolute priority, or turn numerical
failure at \(d=6\) into evidence of nonexistence.
