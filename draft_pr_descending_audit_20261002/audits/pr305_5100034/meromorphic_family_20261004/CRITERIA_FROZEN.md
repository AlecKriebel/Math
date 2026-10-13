# Independent complex-analytic audit criteria (frozen before source/candidate access)

UTC: 2026-10-04T22:59:18.950696+00:00
Submitted head SHA (provided by parent, not independently resolved): cc083024dbd00de06ad444cd4070f51f60d209eb
Audit subject: PR 305; problem 5100034; original submitted claimed_solved 1/5.

## Separation and allowed work
All new files remain in this dedicated directory. No candidate/input edits, inherited-review reads, shared Git/index/ref mutations, installs, external communication, publication, or PR actions. Research statements are hypotheses until checked.

## Source reconstruction criteria
Independently inspect arXiv 2004.12497 v11 Table 7 k606 and published 021-0174 Table 7 k607, preserving edition labels and exact displayed equation. Extract the ambient setting, quantifiers, polygon indexing/winding/repetition restrictions, nondegeneracy conditions, area convention, and all source-defined symbols. Do not import any stronger assertion from the candidate. Freeze a source-only target and independent proposed proof/falsification route before reading the candidate.

## Complex-analytic success criteria
A proposed meromorphic proof must give explicit parametrizations, an actual continuation domain and lattice, every pole location and order modulo that lattice, and all leading principal-part coefficients. Any claimed equality by residue/elliptic argument must control higher-order principal parts, holomorphic remainder/constant, and specialization to the intended real locus. All denominators and divisors used in division must be shown nonzero on their stated domain; generic proofs require justified extension to boundary cases. Real conjugation identities must be converted into holomorphic identities only by an explicit valid continuation.

## Independent falsification/control criteria
Construct exact small-n and limiting controls, using independently derived geometry or algebra rather than author code. Distinguish odd/even n, polygon stars, reversal and repetition, permissible limits and degeneracies. Seek source-valid counterexamples and distinguish them from counterexamples only to a stronger imported theorem. Numerics are evidence only unless exact or rigorously validated; finite tests do not prove an all-n statement.

## Result classification
Report the strongest verified theorem, exact unsupported implication, and explicit gaps. A central difficulty merely transferred to an unsupported equivalent/stronger assertion blocks that route. Do not determine priority/firstness. At checkpoints preserve UTC timestamps and best-guess percent toward completing this audit, allowing revision.

## Freeze
This file is immutable after first creation; its byte SHA-256 is recorded separately.
