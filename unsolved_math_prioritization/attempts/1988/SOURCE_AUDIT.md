# Source and dependency audit

This is the candidate’s historical source assessment. SOURCE_METADATA.json adds the independent audit’s fresh retrieval and inspection records. Edition preparation performed no new scholarly-source retrieval or inspection. Source-status statements below describe the recorded inspection, not an exhaustive current literature determination.

Checked on 2026-10-10 against authenticated local PDF bytes. Source documents and rendered source pages are excluded from the authored packet. Public titles, URLs, sizes, hashes, inspection coverage, and mathematical assessments are recorded here.

## Controlling historical statement

Timothy D. LeSaulnier and Sujith Vijay, *On Permutations Avoiding Arithmetic Progressions*, arXiv:1004.1740v1.

- URL: https://arxiv.org/pdf/1004.1740
- PDF size: 64,364 bytes
- SHA256: 46662dfb1b596a8568617a8ced810d440691c1c705c17e3c77fc48add3499c6e
- Inspection: all four PDF pages through authenticated text extraction; the definition and exact two-set question are on PDF pages 3-4.
- Use: fixes positive-integer ground set and arbitrary-subsequence avoidance.
- Caution: its conjectural upper-density equality 1/2 is not current; the next source disproves it.

## Positive-density construction

Jesse Geneson, *Density bounds for permutations avoiding monotone arithmetic progressions*, arXiv:2608.12604v1, August 2026.

- URL: https://arxiv.org/pdf/2608.12604
- PDF size: 266,695 bytes
- SHA256: f71bc1992ae1c11df30db54f7c06416896f95ab816b48110872b615aa7113cd7
- Inspection: PDF pages 1-5, with definitions, Theorem 1.1, and the complete positive-integer construction and proof in Section 3.
- Use: upper-density lower bound 2/3 and the adjustable separated-block construction underlying Proposition 7. The packet supplies its own complete proof of the adjusted statement.
- Caution: neither a dense single subset nor a supremum statement constructs the requested partition.

## Finite ordering obstruction

William Kasel, *Structural rigidity in the Erdős–Graham two-set permutation problem*, author manuscript, August 2026.

- URL: https://raw.githubusercontent.com/Wkasel/erdos197/main/paper/main.pdf
- PDF size: 205,129 bytes
- SHA256: 89736e1eec491ae3f249e30efb1d1133fabb4c528757e0ae246cbde818605c8a
- Inspection: definitions and general obstructions; Sections 5-6 including the full C3 proof and its supporting lemmas (PDF pages 7-14); relevant appendices on finite versus omega ordering. The flood proof on PDF page 12 was separately rendered and visually inspected in this pass.
- Adopted mathematical dependency: Theorem 22, reconstructed in PROOF.md as a complete four-case argument from the midpoint-extremal rule and mirror propagation. Its finite instances are independently corroborated by newly authored elementary proof certificates and a separate replay checker.
- Not adopted as proof dependencies: the manuscript's standalone SAT verdicts, DRAT certificates, code, all-residue conjecture, or full surrounding proof package. No third-party code was run.
- Scope: the manuscript excludes the exact canonical dyadic candidate and explicitly leaves the general two-set question unresolved. The bounded-deficit theorem here is a consequence of the finite lemma, not an importation of the main dyadic result as a solution.
- Correction: Remark 3 misses translation as an equivalence between the zero-based and positive-integer partition questions. The packet gives the two-direction proof. This is logically separate from the finite C3 lemma.

## Limits of literature assessment

This is a bounded source and dependency assessment. No exhaustive priority search was performed, and neither global novelty nor a proof of current global openness is claimed. The requested two-set question is unresolved by this packet. Adjacent four-term results are not used.
