# v1.1.4 feedback disposition

Status: **ACCEPTED FOR BOUNDED REVISION**

This revision addresses only the cited real-algebraic proof, the formal local
containment notation, Omega auditability, bibliography metadata, and Figure 7.
It does not alter or weaken the theorem statements.

| Feedback | Disposition | Reason and action |
|---|---|---|
| Make the Figure 7 edge from leaf 2 to `D` visually unambiguous | **Adopted** | Leaf 2 was moved left of `D`; its pendant edge is now visibly distinct from the `C-D` path and the reticulation edges in both panels. |
| Replace the proof of the semialgebraic finite-cover lemma | **Adopted after source audit** | The proof now reduces through a finite semialgebraic atlas and cites exactly Theorem 2.8.8 and Propositions 2.8.2, 2.8.4, 2.8.5(i), and 2.8.13 of Bochnak--Coste--Roy.  The relatively open set `U` remains arbitrary; a semialgebraic neighborhood `V` is chosen inside it. |
| Say that Theorem 2.2.1 is applied iteratively | **Adopted** | This precisely explains projection from more than one eliminated coordinate. |
| Tighten the genericity paragraph's dimension language | **Adopted** | The finite-union citation now names Proposition 2.8.5(i), the closure-difference inequality is printed literally, and Theorem 2.8.8 is described as preservation of dimension by semialgebraic bijections. |
| Define projective local one-sided containment | **Adopted** | A distinct relation `\preceq_{\mathrm{proj}}` is defined on regular projective local model germs and used in the local theorem and restoration marginals.  The global relation `\preceq_{\mathrm{JC}}` is unchanged. |
| Remove an internal definition reference from the abstract | **Adopted** | The abstract now states the convention directly. |
| Relabel the finite atlas theorem and remove its boxed minipage | **Adopted** | The label is now `thm:atlas`; all references were updated and the theorem uses the ordinary theorem layout. |
| Correct Cox and Sullivant bibliography metadata | **Adopted after primary-source check** | The first author is Shelby Cox.  Sullivant's first-submission year is 2025, with the 2026 v2 revision recorded in the note. |
| State the base directory for Appendix C | **Adopted** | The appendix now declares all evidence paths relative to the project root inside the tagged monorepository. |
| Clarify the roles of the four Omega rank-nine minors | **Adopted** | The two displayed-rooting minors are identified as the lower-rank and regularity certificates; the two alternative-rooting minors are identified as the rooted-presentation invariance check.  The supplement now prints the alternative ordered twelve-arc array. |
| Expose the alternative-rooting Omega parameter vectors | **Adopted after adversarial review** | The supplement now prints both strict N26 vectors in the declared edge/inheritance order.  The clean-room output stores and validates them, and a targeted mutation changes one coordinate and must be rejected. |
| Make the verifier-entrypoint capsule fail closed on missing members | **Adopted after adversarial review** | The extracted-package verifier carries an independently declared exact member set and rejects a capsule that deletes a required verifier and recomputes its internal checksum manifest. |
| Narrow the final Englander comparison | **Adopted** | The text now states only that the type-(2a) result does not extend to all type-(2c) relabellings and reiterates that Omega is outside their strong class. |
| Add the attributed three-sunlet factorization | **Not added** | The exact sign polynomial, its attribution, and the open-cube sign dichotomy are already stated.  Printing an additional inherited factorization would add notation and citation surface without strengthening a proof dependency. |
| Create a Zenodo DOI during this revision | **Not authorized** | No DOI is created or invented.  Deposit and DOI insertion remain explicit human release steps. |
