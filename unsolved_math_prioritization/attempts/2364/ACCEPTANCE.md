# Acceptance report for the restricted edition

The original fixed-scale result for Erdős Problem 885 was accepted without a mathematical correction. The complete elementary square criterion, divisor enumeration, support deduction, transposition argument, and rational rectangle equivalence are retained in PROOF.md. Parity, positivity, the zero-difference endpoint, injectivity, and completeness of the finite enumeration remain explicit.

For the exact source sets identified in PROOF.md, the independently checked evidence establishes both two-sided closures, the transposed k=4 configuration, and the absence of a k>=5 configuration containing two fixed differences from S or two from T. The S-pair three-difference bound is four, with a sharper bound of three for its second and fourth elements. The T proof uses a three-support intersection condition, because supports of size five occur.

The publication edition explicitly treats the seed and finite evidence as premises P1–P4. The separate arithmetic checks are reported and identified, rather than reproduced. General proofs of the reductions do not certify the omitted finite outputs. The source-fixed theorem is not an arbitrary-scale theorem, and it does not settle unrestricted k=5 or the universal target.

ACCEPTANCE.json binds this edited proof, audit, and acceptance report to their exact bytes and identifies the original accepted documents. Editorial omission of restricted numerical content is not a proof correction and is not a claim that the edited proof is byte-identical to the original.

## Publication and review boundary

This AI-assisted work is unrefereed. Acceptance means an independent internal AI audit of the original report and its separate exact evidence. No external human peer review, journal acceptance, or formal proof-assistant certification is claimed. No mathematical correction was required.

This edition omits the numerical seed lists, raw tables, individual witnesses, certificate contents, executable code, and copied source documents. The finite saturation and support claims cannot be independently reproduced from this edition alone. This is not a complete self-contained proof of the seed-specific computational claims or a complete computational reproduction package. The general mathematical reductions and conditional deductions are complete. The explicitly identified finite premises were checked separately; hashes alone do not prove the omitted arithmetic. The universal arbitrary-k assertion, including unrestricted k=5, remains unresolved by this work. No novelty, priority, or exhaustive literature-status claim is made.

## Sources and attribution

1. P. Erdős and M. Rosenfeld, *The factor-difference set of integers*, Acta Arithmetica 79(4) (1997), 353–359, Section 3, especially Proposition 3.1 and Conjecture 1. [Original PDF](https://matwbn.icm.edu.pl/ksiazki/aa/aa79/aa7944.pdf). The finite-factorization method is credited to this source and re-proved in full here.
2. Sam Mausberg, *Two Formalized Partial Results Related to Erdős Problem E885*, retained April 2026 authored note, Section 2, at commit 05c3837a998a6a71ed1f2ce05985bc67f8e1c35a. [Pinned authored TeX](https://github.com/SamMausberg/lean-formalizations/blob/05c3837a998a6a71ed1f2ce05985bc67f8e1c35a/FormalConjectures/Problems/Erdos/E885/ForumNote/erdos885_forum_note.tex). This identifies the exact seed and its limitation concerning k=5.

The earlier candidate and independent audit record full reading of the retained original extracted text and the inert TeX/README, and visual inspection of printed page 355 of the original article. Preparing this edition involved no fresh scholarly-source retrieval or inspection and no new mathematical computation. The source author's description of Lean-backed work is attributed only; no Lean compilation, formal replay, or acceptance of that formalization is asserted. The full 1999 and 2019 papers were not audited and are not dependencies of the present arguments. This is not a global statement about current literature.
